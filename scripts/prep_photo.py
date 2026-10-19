#!/usr/bin/env python3
"""Prepare a local photo for ASCII conversion. Source photos remain untracked."""
import sys
from pathlib import Path
from PIL import Image,ImageEnhance,ImageOps,ImageFilter
def main():
    if len(sys.argv)<2: raise SystemExit("Usage: python scripts/prep_photo.py <private-photo> [output.png]")
    source=Path(sys.argv[1]); out=Path(sys.argv[2]) if len(sys.argv)>2 else Path("source-prepped.png")
    if not source.exists(): raise SystemExit(f"Photo not found: {source}")
    im=ImageOps.exif_transpose(Image.open(source)).convert("RGB"); im.thumbnail((1200,1200))
    im=ImageOps.grayscale(im); im=ImageOps.autocontrast(im,cutoff=2); im=ImageEnhance.Contrast(im).enhance(1.25); im=ImageEnhance.Brightness(im).enhance(1.08); im=im.filter(ImageFilter.UnsharpMask(radius=1.5,percent=120,threshold=3))
    out.parent.mkdir(parents=True,exist_ok=True); im.save(out); print(f"Wrote {out}; keep the source photo and intermediate file private.")
if __name__=="__main__": main()
