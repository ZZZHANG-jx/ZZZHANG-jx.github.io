#!/usr/bin/env python3
"""Look up canonical paper links via Crossref, with known fallbacks."""

import json
import re
import time
import urllib.parse
import urllib.request

UA = "academic-homepage-build/1.0 (mailto:eejxzhang@gmail.com)"

PAPERS = [
    ("DocAligner: Automating the Annotation of Photographed Documents through Real-Virtual Alignment", None),
    ("AutoScaler: Self Scale Alignment for Handwritten Mathematical Expression Recognition", None),
    ("Smaller but Better: Unifying Layout Generation with Smaller Large Language Models", None),
    ("QT-TextSR: Enhancing Scene Text Image Super-Resolution via Efficient Interaction with Text Recognition", None),
    ("Appearance Enhancement for Camera-Captured Document Images in the Wild", None),
    ("Scene Table Structure Recognition with Segmentation Collaboration and Alignment", None),
    ("Looking from a Higher-Level Perspective: Attention and Recognition Enhanced Multi-Scale Scene Text Segmentation", None),
    ("Complex Table Structure Recognition in the Wild Using Transformer and Identity Matrix-Based Augmentation", None),
    ("Forgery-Free Signature Verification with Stroke-Aware Cycle-Consistent Generative Adversarial Network", None),
    ("M6Doc: A Large-Scale Multi-Format, Multi-Type, Multi-Layout, Multi-Language, Multi-Annotation Category Dataset for Modern Document Layout Analysis", None),
    ("UPOCR: Towards Unified Pixel-Level OCR Interface", None),
    ("Beyond Token Compression: A Training-Free Reduction Framework for Efficient Visual Processing in MLLMs", "https://arxiv.org/abs/2501.19036"),
    ("OCRGenBench: A Comprehensive Benchmark for Evaluating OCR Generative Capabilities", "https://arxiv.org/abs/2507.15085"),
    ("Marior: Margin Removal and Iterative Content Rectification for Document Dewarping in the Wild", "https://arxiv.org/abs/2207.11515"),
]


def norm(text):
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


def crossref(title):
    query = urllib.parse.quote(title)
    url = (
        "https://api.crossref.org/works?query.bibliographic="
        f"{query}&rows=3&select=DOI,title,container-title,issued"
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    target = norm(title)[:70]
    for item in data["message"]["items"]:
        cand = norm(item.get("title", [""])[0])[:70]
        if cand[:45] == target[:45]:
            return item["DOI"], item.get("container-title", [""])[0]
    return None, None


def main():
    results = []
    for title, fallback in PAPERS:
        doi, venue = None, None
        try:
            doi, venue = crossref(title)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! lookup failed: {exc}")
        if doi:
            link = f"https://doi.org/{doi}"
            results.append({"title": title, "link": link, "doi": doi, "venue": venue})
            print(f"DOI   {doi:42s} {title[:55]}")
        else:
            results.append({"title": title, "link": fallback, "doi": None, "venue": None})
            print(f"FALL  {(fallback or 'MISSING'):42s} {title[:55]}")
        time.sleep(1.2)

    with open("scripts/paper_links.json", "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    print("\nwrote scripts/paper_links.json")


if __name__ == "__main__":
    main()
