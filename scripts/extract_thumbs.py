#!/usr/bin/env python3
"""Pull a usable thumbnail out of each paper PDF.

Strategy per paper: take the largest embedded raster image on pages 1-3;
if the paper is all vector art, render the teaser band of page 1 instead.
"""

import io
import os
import sys
import urllib.request

import pymupdf
from PIL import Image

OUT_DIR = os.path.join("images", "publication_imgs")
TMP_DIR = os.path.join("preview", "_tmp_pdf")

PAPERS = {
    "upocr": "https://raw.githubusercontent.com/mlresearch/v235/main/assets/peng24e/peng24e.pdf",
    "marior": "https://arxiv.org/pdf/2207.11515",
    "beyondtoken": "https://arxiv.org/pdf/2501.19036",
    "ocrgenbench": "https://arxiv.org/pdf/2507.15085",
    "smallerbetter": "https://arxiv.org/pdf/2502.14005",
    "lego": "https://arxiv.org/pdf/2408.02036",
    "higherlevel": (
        "https://openaccess.thecvf.com/content/ACCV2022/papers/"
        "Ren_Looking_from_a_Higher-level_Perspective_Attention_and_Recognition_Enhanced_Multi-scale_ACCV_2022_paper.pdf"
    ),
    "m6doc": (
        "https://openaccess.thecvf.com/content/CVPR2023/papers/"
        "Cheng_M6Doc_A_Large-Scale_Multi-Format_Multi-Type_Multi-Layout_Multi-Language_"
        "Multi-Annotation_Category_Dataset_CVPR_2023_paper.pdf"
    ),
}


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (homepage-build)"})
    with urllib.request.urlopen(req, timeout=90) as resp, open(dest, "wb") as fh:
        fh.write(resp.read())
    return os.path.getsize(dest)


def largest_raster(doc, max_pages=3):
    best = None
    for page in doc.pages(0, min(max_pages, len(doc))):
        for img in page.get_images(full=True):
            try:
                info = doc.extract_image(img[0])
            except Exception:  # noqa: BLE001
                continue
            w, h = info["width"], info["height"]
            if w < 500 or h < 150:
                continue
            area = w * h
            if best is None or area > best[0]:
                best = (area, info["image"], w, h)
    return best


def render_teaser(doc):
    page = doc[0]
    rect = page.rect
    # Teaser figure usually sits below the title/abstract block.
    clip = pymupdf.Rect(rect.x0, rect.y0 + rect.height * 0.16, rect.x1, rect.y0 + rect.height * 0.62)
    pix = page.get_pixmap(clip=clip, dpi=200)
    return Image.open(io.BytesIO(pix.tobytes("png")))


def caption_crop(doc):
    """Render only the artwork that sits directly above the 'Figure 1' caption."""
    for page_no in (0, 1):
        page = doc[page_no]
        prect = page.rect
        hits = page.search_for("Figure 1") or page.search_for("Fig. 1")
        hits = [h for h in hits if h.y0 > prect.height * 0.12]
        if not hits:
            continue
        cap = hits[0]

        # Collect graphic elements: embedded images and vector drawings.
        rects = []
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") == 1:
                rects.append(pymupdf.Rect(block["bbox"]))
        try:
            for drawing in page.get_drawings():
                r = drawing["rect"]
                if r.width > 40 and r.height > 40:
                    rects.append(r)
        except Exception:  # noqa: BLE001
            pass

        # Keep the artwork whose bottom edge is just above the caption.
        gap = prect.height * 0.18
        near = [r for r in rects if r.y1 <= cap.y0 + 4 and cap.y0 - r.y1 < gap]
        if not near:
            continue

        bbox = near[0]
        for r in near[1:]:
            bbox = bbox | r

        # Trim to the caption width when the artwork spans a narrow column.
        clip = pymupdf.Rect(
            max(prect.x0, bbox.x0 - 6),
            max(prect.y0, bbox.y0 - 6),
            min(prect.x1, bbox.x1 + 6),
            min(bbox.y1 + 6, cap.y0 - 2),
        )
        if clip.width < 150 or clip.height < 60:
            continue
        pix = page.get_pixmap(clip=clip, dpi=220)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        ratio = img.size[1] / img.size[0]
        if 0.2 < ratio < 1.1:
            return img
    return None


def save_thumb(image, path, width=640):
    if image.mode in ("RGBA", "P", "LA"):
        image = image.convert("RGBA")
        bg = Image.new("RGB", image.size, (255, 255, 255))
        bg.paste(image, mask=image.split()[-1])
        image = bg
    else:
        image = image.convert("RGB")
    w, h = image.size
    if w > width:
        image = image.resize((width, round(h * width / w)), Image.LANCZOS)
    image.save(path, "JPEG", quality=88, optimize=True)
    return image.size


def main():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)

    only = set(sys.argv[1:])
    for key, url in PAPERS.items():
        if only and key not in only:
            continue
        pdf_path = os.path.join(TMP_DIR, key + ".pdf")
        if not os.path.exists(pdf_path) or os.path.getsize(pdf_path) < 20000:
            try:
                size = fetch(url, pdf_path)
            except Exception as exc:  # noqa: BLE001
                print(f"[{key}] download failed: {exc}")
                continue
        else:
            size = os.path.getsize(pdf_path)

        doc = pymupdf.open(pdf_path)
        image, source = None, None

        cropped = caption_crop(doc)
        if cropped is not None:
            image, source = cropped, "figure-1 crop"

        if image is None:
            best = largest_raster(doc)
            if best:
                _, data, w, h = best
                image, source = Image.open(io.BytesIO(data)), f"raster {w}x{h}"

        if image is None:
            image, source = render_teaser(doc), "rendered teaser"

        out = os.path.join(OUT_DIR, key + ".jpg")
        size_out = save_thumb(image, out)
        print(f"[{key}] pdf={size//1024}KB  from={source}  -> {size_out}  {os.path.getsize(out)//1024}KB")
        doc.close()


if __name__ == "__main__":
    sys.exit(main())
