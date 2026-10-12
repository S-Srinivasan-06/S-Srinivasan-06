"""Write scripts/paper.png: a small tileable grain texture for the cream panels.

A pre-rendered tile replaces a live SVG noise filter, which browsers recompute on every
animation frame. Standard library only; the output is deterministic.

  python scripts/make_paper.py
"""

import os
import random
import struct
import zlib

SIZE = 128
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paper.png")


def chunk(kind, data):
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)


def main():
    rng = random.Random(7)
    rows = []
    for _ in range(SIZE):
        row = bytearray([0])  # filter type: none
        for _ in range(SIZE):
            roll = rng.random()
            # warm brown specks: mostly clear, some faint, a few darker fibres
            alpha = 0 if roll < .55 else rng.randint(8, 22) if roll < .97 else rng.randint(30, 55)
            row += bytes((96, 78, 52, alpha))
        rows.append(bytes(row))
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b""))
    with open(OUT, "wb") as fh:
        fh.write(png)
    print("wrote", OUT, len(png), "bytes")


if __name__ == "__main__":
    main()
