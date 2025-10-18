#!/usr/bin/env python3
import io
import os
import re
import sys
import time
import tempfile
import subprocess
from typing import Dict, List, Tuple

import requests
import numpy as np
import cv2

BASE = 'https://087ba594e710a16e.247ctf.com/'

Session = requests.Session


def fetch_image(session: Session) -> np.ndarray:
    resp = session.get(BASE + 'mturk.php', timeout=4)
    resp.raise_for_status()
    img = cv2.imdecode(np.frombuffer(resp.content, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise RuntimeError('Failed to decode image')
    return img


def binarize_image(gray: np.ndarray) -> np.ndarray:
    # Adaptive threshold via OTSU, invert so foreground is white (255)
    _thr, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # Light median blur to remove salt-and-pepper
    bw = cv2.medianBlur(bw, 3)
    return bw


def segment_glyphs(bw: np.ndarray) -> List[np.ndarray]:
    # Segment by vertical projection (column sums)
    h, w = bw.shape
    col_sums = bw.sum(axis=0) // 255  # number of foreground pixels per column
    # Separator = columns with very few white pixels
    # Threshold as 5% of image height
    sep_mask = col_sums <= max(1, int(0.05 * h))

    segments: List[Tuple[int, int]] = []
    in_run = False
    start = 0
    for x in range(w):
        if sep_mask[x]:
            if in_run:
                end = x
                if end - start >= 2:
                    segments.append((start, end))
                in_run = False
        else:
            if not in_run:
                in_run = True
                start = x
    if in_run and w - start >= 2:
        segments.append((start, w))

    crops: List[np.ndarray] = []
    for xs, xe in segments:
        sub = bw[:, xs:xe]
        # Trim empty top/bottom rows
        row_sums = sub.sum(axis=1) // 255
        ys_candidates = np.where(row_sums > 0)[0]
        if ys_candidates.size == 0:
            continue
        ys, ye = int(ys_candidates[0]), int(ys_candidates[-1] + 1)
        crop = sub[ys:ye, :]
        # Filter out extremely small crops
        if crop.shape[0] >= 6 and crop.shape[1] >= 3:
            crops.append(crop)
    return crops


def normalize_glyph(g: np.ndarray, size: Tuple[int, int] = (32, 24)) -> np.ndarray:
    # Resize keeping aspect ratio into canvas of given size
    target_h, target_w = size
    h, w = g.shape
    scale = min(target_h / h, target_w / w)
    nh, nw = max(1, int(round(h * scale))), max(1, int(round(w * scale)))
    resized = cv2.resize(g, (nw, nh), interpolation=cv2.INTER_NEAREST)
    canvas = np.zeros((target_h, target_w), dtype=np.uint8)
    # center
    y0 = (target_h - nh) // 2
    x0 = (target_w - nw) // 2
    canvas[y0:y0+nh, x0:x0+nw] = resized
    return canvas


def ocr_char_with_tesseract(glyph: np.ndarray, timeout_s: float = 0.6) -> str:
    # Write temp file and call tesseract for a single character
    with tempfile.NamedTemporaryFile(suffix='.png') as tf:
        # Invert to black text on white for tesseract preference
        inv = cv2.bitwise_not(glyph)
        up = cv2.resize(inv, (inv.shape[1] * 5, inv.shape[0] * 5), interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(tf.name, up)
        try:
            # Use external timeout for CLI
            out = subprocess.check_output([
                'timeout', f'{int(timeout_s*1000)}ms',
                'tesseract', tf.name, 'stdout', '--oem', '1', '--psm', '10', '-l', 'eng',
                '-c', 'tessedit_char_whitelist=0123456789+'
            ], stderr=subprocess.DEVNULL)
            ch = re.sub(r'[^0-9+]', '', out.decode()).strip()
            return ch
        except Exception:
            return ''


def build_digit_templates(session: Session, needed: str = '0123456789', max_images: int = 60) -> Dict[str, np.ndarray]:
    templates: Dict[str, np.ndarray] = {}
    # Prime session by loading base page
    session.get(BASE, timeout=4)

    for _ in range(max_images):
        img = fetch_image(session)
        bw = binarize_image(img)
        glyphs = segment_glyphs(bw)
        for g in glyphs:
            ch = ocr_char_with_tesseract(g)
            if ch in needed and ch not in templates:
                templates[ch] = normalize_glyph(g)
                if len(templates) == len(needed):
                    return templates
    return templates


def match_digit(glyph: np.ndarray, templates: Dict[str, np.ndarray]) -> Tuple[str, float]:
    # Return best matching digit and score
    if not templates:
        return '', -1.0
    ng = normalize_glyph(glyph)
    best_char = ''
    best_score = -1.0
    for d, tmpl in templates.items():
        res = cv2.matchTemplate(ng, tmpl, cv2.TM_CCOEFF_NORMED)
        score = float(res.max())
        if score > best_score:
            best_score = score
            best_char = d
    return best_char, best_score


def solve_expression(session: Session, templates: Dict[str, np.ndarray]) -> Tuple[bool, bool, str]:
    # Returns: (got_flag, was_correct, response_text)
    img = fetch_image(session)
    bw = binarize_image(img)
    glyphs = segment_glyphs(bw)
    if not glyphs:
        # Fallback: try whole-line tesseract quickly
        with tempfile.NamedTemporaryFile(suffix='.png') as tf:
            inv = cv2.bitwise_not(bw)
            cv2.imwrite(tf.name, inv)
            try:
                out = subprocess.check_output([
                    'timeout', '800ms', 'tesseract', tf.name, 'stdout', '--oem', '1', '--psm', '7', '-l', 'eng',
                    '-c', 'tessedit_char_whitelist=0123456789+'
                ], stderr=subprocess.DEVNULL)
                line = re.sub(r'[^0-9+]+', '', out.decode())
                if '+' in line:
                    a, b = line.split('+', 1)
                    ans = str(int(a) + int(b)) if a.isdigit() and b.isdigit() else '0'
                else:
                    ans = '0'
            except Exception:
                ans = '0'
    else:
        # Classify each glyph; choose plus index as glyph with MIN best-score
        scores: List[float] = []
        chars: List[str] = []
        for g in glyphs:
            ch, sc = match_digit(g, templates)
            scores.append(sc)
            chars.append(ch)
        # If any unknown, fallback char classification via tesseract for that glyph only
        for idx, ch in enumerate(chars):
            if not ch:
                t = ocr_char_with_tesseract(glyphs[idx])
                chars[idx] = t if t.isdigit() else ''
                scores[idx] = -1.0
        # Identify plus index as glyph with lowest score among those with low width ratio
        widths = [g.shape[1] for g in glyphs]
        min_score_idx = int(np.argmin(scores)) if scores else 0
        plus_idx = min_score_idx
        # Build numbers by concatenating digits, skipping plus index
        left_digits = ''.join(chars[:plus_idx])
        right_digits = ''.join(chars[plus_idx+1:])
        if left_digits.isdigit() and right_digits.isdigit() and left_digits and right_digits:
            ans = str(int(left_digits) + int(right_digits))
        else:
            # fallback per-glyph tesseract across all glyphs
            txt = ''
            for g in glyphs:
                t = ocr_char_with_tesseract(g)
                txt += t if t else '?'
            if '+' in txt:
                a, b = txt.split('+', 1)
                ans = str(int(re.sub(r'\D', '', a) or 0) + int(re.sub(r'\D', '', b) or 0))
            else:
                ans = '0'
    # Submit answer
    resp = session.post(BASE, data={'captcha': ans}, timeout=4)
    text = resp.text
    got_flag = ('flag{' in text)
    was_correct = ('Correct!' in text)
    return got_flag, was_correct, text


def main() -> int:
    session = requests.Session()
    # Load base page to set session cookie
    session.get(BASE, timeout=4)
    # Build templates quickly
    t0 = time.time()
    templates = build_digit_templates(session)
    if len(templates) < 10:
        # Try a bit longer if missing digits
        templates = build_digit_templates(session, max_images=120)
    # Solve up to 200 attempts or until flag appears
    correct = 0
    start = time.time()
    for i in range(200):
        got_flag, ok, text = solve_expression(session, templates)
        if ok:
            correct += 1
        if got_flag:
            # Print the page to stdout to capture flag
            sys.stdout.write(text)
            sys.stdout.flush()
            break
        # Early stop if very slow
        if time.time() - start > 35:
            break
    elapsed = time.time() - start
    sys.stderr.write(f'Correct: {correct} in {elapsed:.2f}s\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
