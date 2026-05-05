"""Auto-crop the replay PNG to remove dead space below the last content row.

Scans rows from bottom; the first row whose pixel std exceeds a small
threshold is the bottom of content. Crops to that + a small margin.

Usage:
  python crop_replay.py <path/to/full.png>  → writes <path>.cropped.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

if len(sys.argv) < 2:
    print("usage: crop_replay.py <path/to/full.png>", file=sys.stderr)
    sys.exit(2)

src = Path(sys.argv[1])
img = Image.open(src).convert("RGB")
arr = np.asarray(img)
h, w = arr.shape[:2]

# Per-row std across all pixels (RGB averaged)
gray = arr.mean(axis=2)
row_std = gray.std(axis=1)

# Background pages-end is ~uniform dark grey (#111). Content rows have std > ~3.
THRESHOLD = 3.0
last_content_row = None
for y in range(h - 1, -1, -1):
    if row_std[y] > THRESHOLD:
        last_content_row = y
        break

if last_content_row is None:
    print("no content found; not cropping", file=sys.stderr)
    sys.exit(0)

# Add small margin (10 px) below last content row
margin = 10
bottom = min(h, last_content_row + margin)

cropped = img.crop((0, 0, w, bottom))
out = src.with_name(src.name.replace(".full.png", ".png"))
cropped.save(out, "PNG", optimize=True)

print(f"original: {w}×{h}")
print(f"last content row: {last_content_row}  (cropped to {w}×{bottom}, +{margin}px margin)")
print(f"removed: {h - bottom}px dead space")
print(f"wrote {out}")
