#!/usr/bin/env python3
"""news-image-20261119 — make.fun entry.

Writes one image summing up the world news of Thursday 19 November 2026
to /output/entry.png. The image is held in this repository as image.png
(a 1024x1024 PNG, 550,864 bytes, under the 1 MiB cap); the program copies
it byte-for-byte, so both runs write the same bytes. No network access.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "image.png")


def main() -> int:
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    size = os.path.getsize(dest)
    print(f"wrote {dest} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
