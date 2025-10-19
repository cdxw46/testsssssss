#!/usr/bin/env python3
import re
import sys
from pathlib import Path

LOG = Path("/workspace/flagportation/session.log")
OUT_BITS = Path("/workspace/flagportation/bits_parsed.txt")
OUT_BIN = Path("/workspace/flagportation/flag_parsed.bin")
OUT_TXT = Path("/workspace/flagportation/flag_parsed.txt")

RE_BASIS = re.compile(r"^Basis\s*:\s*([ZX])\s*$")
RE_M2 = re.compile(r"^Measurement of qubit 2\s*:\s*(\d+)\s*$")


def pair_from_measure(basis: str, meas: int) -> str:
    if basis == "Z":
        return "00" if meas == 0 else "01"
    else:
        return "10" if meas == 0 else "11"


def bits_to_bytes(bitstr: str) -> bytes:
    # Trim to multiple of 8
    if len(bitstr) % 8 != 0:
        bitstr = bitstr[: len(bitstr) - (len(bitstr) % 8)]
    out = bytearray()
    for i in range(0, len(bitstr), 8):
        chunk = bitstr[i : i + 8]
        out.append(int(chunk, 2))
    return bytes(out)


def main() -> int:
    if not LOG.exists():
        print("no log", file=sys.stderr)
        return 1
    bits = []
    basis = None
    for raw in LOG.read_text(errors="ignore").splitlines():
        line = raw.strip("\r\n")
        m = RE_BASIS.match(line)
        if m:
            basis = m.group(1)
            continue
        m = RE_M2.match(line)
        if m and basis is not None:
            meas = int(m.group(1))
            bits.append(pair_from_measure(basis, meas))
            continue
    bitstr = "".join(bits)
    OUT_BITS.write_text(bitstr)
    data = bits_to_bytes(bitstr)
    OUT_BIN.write_bytes(data)
    try:
        OUT_TXT.write_text(data.decode())
    except UnicodeDecodeError:
        OUT_TXT.write_bytes(data)
    sys.stdout.write(OUT_TXT.read_text(errors="ignore"))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
