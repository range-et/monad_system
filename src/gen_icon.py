"""
Generate assets/icon.png — the Monad System icon.

Leibniz monad: a circle with a center point.
Pure Python, no dependencies. Supersampled 4x for anti-aliasing.
"""

import struct
import zlib
import os

SIZE  = 512
SCALE = 4
S     = SIZE * SCALE

BG   = (18, 18, 18)    # #121212
BLUE = (3, 169, 244)   # #03A9F4

def generate(out_path: str) -> None:
    cx = cy = S // 2
    outer_r = int(S * 0.35)
    stroke  = int(S * 0.018)
    dot_r   = int(S * 0.030)

    # render at SCALE×
    hi = []
    for y in range(S):
        row = []
        for x in range(S):
            dx, dy = x - cx, y - cy
            d = (dx * dx + dy * dy) ** 0.5
            if d <= dot_r or (outer_r - stroke / 2 <= d <= outer_r + stroke / 2):
                row.append(BLUE)
            else:
                row.append(BG)
        hi.append(row)

    # downsample → SIZE × SIZE
    scanlines = []
    for y in range(SIZE):
        row = []
        for x in range(SIZE):
            rs = gs = bs = 0
            for dy in range(SCALE):
                for dx in range(SCALE):
                    r, g, b = hi[y * SCALE + dy][x * SCALE + dx]
                    rs += r; gs += g; bs += b
            n = SCALE * SCALE
            row.extend([rs // n, gs // n, bs // n])
        scanlines.append(bytes([0]) + bytes(row))

    raw = zlib.compress(b"".join(scanlines), 9)

    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", SIZE, SIZE, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", raw)
        + chunk(b"IEND", b"")
    )

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "..", "assets", "icon.png")
    generate(os.path.normpath(path))
    print(f"Icon saved → {os.path.normpath(path)}")
