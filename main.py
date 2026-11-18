#!/usr/bin/env python3
"""news-image-20261118 entry: copy the front-page image to /output/entry.png.

The image is a newspaper front page summing up Wednesday 18 November 2026:
lead story the APEC summit opening in Shenzhen, with Trump in Manila for
the Quad and the first-ever Trump-Xi-Putin three-way talks set for Thursday;
plus the Crimean Bridge strikes, the US strike on an IRGC base on Qeshm
Island, Cyclone Akvan, the French cost-of-living protests, Nvidia's
103% revenue jump, and Dhoni's IPL retirement. Deterministic, no network.

Usage: python3 main.py
  Copies entry.png (next to this file) to $MAKEFUN_OUTPUT_DIR/entry.png
  (default /output/entry.png), then verifies the copy: it must start with
  the PNG magic bytes, be exactly 1024x1024 pixels, and its size and
  SHA-256 must match the source. Exits non-zero with a message on stderr
  if verification fails.
"""
import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

SRC = HERE / "entry.png"
DST = OUT / "entry.png"


def png_dimensions(data):
    """Read width and height from the PNG IHDR chunk."""
    if len(data) < 33 or data[:8] != PNG_MAGIC or data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC, DST)

# Verify the copy: PNG magic bytes, 1024x1024 dimensions, size, and
# SHA-256 must all match the source.
src_bytes = SRC.read_bytes()
dst_bytes = DST.read_bytes()
if not dst_bytes.startswith(PNG_MAGIC):
    print("error: output is not a PNG (bad magic bytes)", file=sys.stderr)
    sys.exit(1)
dims = png_dimensions(dst_bytes)
if dims != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
    print(f"error: output dimensions {dims} != "
          f"({EXPECTED_WIDTH}, {EXPECTED_HEIGHT})", file=sys.stderr)
    sys.exit(1)
if len(dst_bytes) != len(src_bytes):
    print(f"error: output size {len(dst_bytes)} != source size {len(src_bytes)}",
          file=sys.stderr)
    sys.exit(1)
if hashlib.sha256(dst_bytes).hexdigest() != hashlib.sha256(src_bytes).hexdigest():
    print("error: output SHA-256 does not match the source", file=sys.stderr)
    sys.exit(1)
print("wrote", DST,
      f"({len(dst_bytes)} bytes, 1024x1024, sha256 verified)")
