#!/usr/bin/env python3
"""news-image-20261119 — make.fun entry.

Writes one image summing up the world news of Thursday 19 November 2026
to /output/entry.png. The image is held in this repository as image.png
(a 1024x1024 PNG, 550,864 bytes, under the 1 MiB cap); the program copies
it byte-for-byte, so both runs write the same bytes. No network access.
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "image.png")

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def validate_png(path: str) -> tuple:
    """Fail loudly unless path is a valid PNG of the expected size.

    Checks the 8-byte PNG signature and the IHDR width/height, so a
    truncated or wrong-size image is caught here instead of being
    submitted silently.
    """
    with open(path, "rb") as fh:
        header = fh.read(33)
    if len(header) < 33 or header[:8] != PNG_SIGNATURE:
        raise ValueError(f"{path}: not a PNG file (bad signature)")
    if header[12:16] != b"IHDR":
        raise ValueError(f"{path}: not a PNG file (no IHDR chunk)")
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            f"{path}: expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, "
            f"got {width}x{height}"
        )
    return width, height


def main() -> int:
    try:
        validate_png(SRC)
    except (OSError, ValueError) as exc:
        print(f"error: source image invalid: {exc}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    try:
        validate_png(dest)
    except (OSError, ValueError) as exc:
        print(f"error: output image invalid: {exc}", file=sys.stderr)
        return 1
    src_size = os.path.getsize(SRC)
    size = os.path.getsize(dest)
    if size != src_size:
        print(
            f"error: output size {size} != source size {src_size}",
            file=sys.stderr,
        )
        return 1
    print(f"wrote {dest} ({size} bytes, {EXPECTED_WIDTH}x{EXPECTED_HEIGHT})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
