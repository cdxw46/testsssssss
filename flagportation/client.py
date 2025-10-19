#!/usr/bin/env python3
import socket
import sys
import re
import time
from typing import Optional

HOST = "94.237.51.21"
PORT = 34793

# Patterns for complete lines
RE_BASIS = re.compile(r"^Basis\s*:\s*([ZX])\s*$")
RE_M0 = re.compile(r"^Measurement of qubit 0\s*:\s*(\d+)\s*$")
RE_M1 = re.compile(r"^Measurement of qubit 1\s*:\s*(\d+)\s*$")
RE_M2 = re.compile(r"^Measurement of qubit 2\s*:\s*(\d+)\s*$")

PROMPT_INSTR = b"Specify the instructions :"
PROMPT_BASIS = b"Specify the measurement basis :"


def compute_instructions(m0: int, m1: int) -> str:
    parts = []
    if m0 == 1:
        parts.append("Z:2")
    if m1 == 1:
        parts.append("X:2")
    if not parts:
        parts = ["H:2", "H:2"]
    return ";".join(parts)


def pair_from_measure(basis: str, meas: int) -> str:
    if basis == "Z":
        return "00" if meas == 0 else "01"
    else:
        return "10" if meas == 0 else "11"


def bits_to_bytes(bitstr: str) -> bytes:
    if len(bitstr) % 8 != 0:
        bitstr = bitstr[: len(bitstr) - (len(bitstr) % 8)]
    out = bytearray()
    for i in range(0, len(bitstr), 8):
        chunk = bitstr[i : i + 8]
        out.append(int(chunk, 2))
    return bytes(out)


def main() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    sock.connect((HOST, PORT))

    logf = open("/workspace/flagportation/session.log", "wb")

    buffer = bytearray()
    bit_accum = []
    basis: Optional[str] = None
    m0: Optional[int] = None
    m1: Optional[int] = None

    last_activity = time.time()

    def send_line(s: str) -> None:
        out = (s + "\n").encode()
        try:
            logf.write(b"--> "+out)
            logf.flush()
        except Exception:
            pass
        sock.sendall(out)

    try:
        while True:
            # receive chunk (non-blocking style with small timeout)
            try:
                chunk = sock.recv(4096)
            except socket.timeout:
                chunk = b""
            if chunk:
                buffer += chunk
                try:
                    logf.write(chunk)
                    logf.flush()
                except Exception:
                    pass
                last_activity = time.time()
            else:
                if time.time() - last_activity > 20:
                    break

            # Process full lines
            while True:
                nl = buffer.find(b"\n")
                if nl == -1:
                    break
                line = buffer[:nl]
                buffer = buffer[nl+1:]
                s = line.decode("utf-8", errors="ignore").rstrip("\r")

                m = RE_BASIS.match(s)
                if m:
                    basis = m.group(1)
                    continue
                m = RE_M0.match(s)
                if m:
                    m0 = int(m.group(1))
                    continue
                m = RE_M1.match(s)
                if m:
                    m1 = int(m.group(1))
                    continue
                m = RE_M2.match(s)
                if m and basis is not None:
                    meas = int(m.group(1))
                    bit_accum.append(pair_from_measure(basis, meas))
                    continue

            # Handle prompts without newline
            if PROMPT_INSTR in buffer:
                instr = "H:2;H:2"
                if basis is not None and m0 is not None and m1 is not None:
                    instr = compute_instructions(m0, m1)
                send_line(instr)
                m0 = None
                m1 = None
                # remove prompt occurrence only; keep tail
                idx = buffer.find(PROMPT_INSTR)
                buffer = buffer[:idx] + buffer[idx+len(PROMPT_INSTR):]
                last_activity = time.time()

            if PROMPT_BASIS in buffer:
                send_line(basis or "Z")
                idx = buffer.find(PROMPT_BASIS)
                buffer = buffer[:idx] + buffer[idx+len(PROMPT_BASIS):]
                last_activity = time.time()
    finally:
        try:
            sock.close()
        except Exception:
            pass
        try:
            logf.close()
        except Exception:
            pass

    bits = "".join(bit_accum)
    with open("/workspace/flagportation/bits.txt", "w") as f:
        f.write(bits)
    data = bits_to_bytes(bits)
    with open("/workspace/flagportation/flag.bin", "wb") as f:
        f.write(data)
    try:
        sys.stdout.write(data.decode())
    except UnicodeDecodeError:
        sys.stdout.buffer.write(data)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
