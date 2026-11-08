#!/usr/bin/env python3
"""Generate high-res (_full) variants of publication cover images for the lightbox.

- Genuine HD from original sources where available (PDFs on desktop, M6Doc big png,
  RedundancyLens repo figure).
- Otherwise upscale the existing 640px thumbnail to 1280px via LANCZOS (better than
  in-browser bilinear upscale; swap in true originals later for real HD).
"""
import io
import os
import fitz
import urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images", "publication_imgs")
TARGET_W = 1280


def save_full(name, im):
    im = im.convert("RGB")
    if im.width > TARGET_W:
        im = im.resize((TARGET_W, round(im.height * TARGET_W / im.width)))
    out = os.path.join(IMG, name + "_full.jpg")
    im.save(out, "JPEG", quality=90)
    print("wrote", os.path.basename(out), im.size)


def from_pdf(path, page, clip, name):
    doc = fitz.open(path)
    pg = doc[page]
    pix = pg.get_pixmap(clip=fitz.Rect(*clip), dpi=400)
    save_full(name, Image.open(io.BytesIO(pix.tobytes("png"))))


def from_url(url, name):
    data = urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    ).read()
    save_full(name, Image.open(io.BytesIO(data)))


# --- Genuine HD sources ---
from_pdf(r"C:/Users/76177/Desktop/NC.pdf", 2, (120, 100, 495, 260), "qttextsr")
from_pdf(r"C:/Users/76177/Desktop/prcv (6)-zjx.pdf", 2, (120, 100, 495, 260), "docshrnet")
from_url("https://raw.githubusercontent.com/HCIILAB/M6Doc/main/img/m6doc_example.png", "m6doc")
for branch in ("main", "master"):
    try:
        from_url(
            f"https://raw.githubusercontent.com/L-Hugh/RedundancyLens/{branch}/figures/image.png",
            "beyondtoken",
        )
        break
    except Exception as e:
        print("beyondtoken branch", branch, "failed:", e)

# --- Upscale the rest from existing 640px thumbnails ---
special = {"qttextsr", "docshrnet", "m6doc", "beyondtoken"}
for f in sorted(os.listdir(IMG)):
    base, ext = os.path.splitext(f)
    if base.endswith("_full") or ext.lower() not in (".jpg", ".png"):
        continue
    if base in special:
        continue
    im = Image.open(os.path.join(IMG, f)).convert("RGB")
    up = im.resize((TARGET_W, round(im.height * TARGET_W / im.width)), Image.LANCZOS)
    save_full(base, up)

print("done")
