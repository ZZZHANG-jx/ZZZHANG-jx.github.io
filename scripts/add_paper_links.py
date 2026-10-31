#!/usr/bin/env python3
"""Insert Paper / GitHub badges into _pages/publications.md."""

import io
import re

PATH = "_pages/publications.md"

PAPER_BADGE = "https://img.shields.io/badge/Paper-fedcba"
STAR = "https://img.shields.io/github/stars/ZZZHANG-jx/{repo}.svg?style=social&label=Star"

# key = distinctive prefix of the <h3> title
LINKS = {
    "DocAligner: Automating": (
        "https://doi.org/10.1016/j.patcog.2025.112191",
        "DocAligner",
    ),
    "AutoScaler: Self Scale": (
        "https://doi.org/10.1016/j.patcog.2025.111872",
        None,
    ),
    "Smaller but Better": (
        "https://doi.org/10.1007/s11263-025-02353-2",
        None,
    ),
    "Beyond Token Compression": ("https://arxiv.org/abs/2501.19036", None),
    "QT-TextSR": ("https://doi.org/10.1016/j.neucom.2024.129241", None),
    "OCRGenBench": ("https://arxiv.org/abs/2507.15085", None),
    "UPOCR: Towards Unified": ("https://proceedings.mlr.press/v235/peng24e.html", None),
    "M6Doc: A Large-Scale": (
        "https://openaccess.thecvf.com/content/CVPR2023/html/"
        "Cheng_M6Doc_A_Large-Scale_Multi-Format_Multi-Type_Multi-Layout_Multi-Language_"
        "Multi-Annotation_Category_Dataset_CVPR_2023_paper.html",
        None,
    ),
    "Appearance Enhancement": ("https://doi.org/10.1109/tai.2023.3321257", None),
    "Scene Table Structure": ("https://doi.org/10.1016/j.patrec.2022.12.014", None),
    "Marior: Margin Removal": ("https://doi.org/10.1145/3503161.3548214", None),
    "Looking from a Higher-Level": ("https://doi.org/10.1007/978-3-031-26293-7_38", None),
    "Complex Table Structure": ("https://doi.org/10.1007/978-3-031-21648-0_37", None),
    "Forgery-Free Signature": ("https://doi.org/10.1016/j.neucom.2022.08.017", None),
}


def badge_html(paper_url, repo):
    out = f"<a href='{paper_url}'><img src='{PAPER_BADGE}' alt='Paper'></a>"
    if repo:
        out += f"\n<a href='https://github.com/ZZZHANG-jx/{repo}'><img src='{STAR.format(repo=repo)}' alt='GitHub stars'></a>"
    return out


def main():
    with io.open(PATH, encoding="utf-8") as fh:
        text = fh.read()

    for key, (paper_url, repo) in LINKS.items():
        idx = -1
        for prefix in ("<h3>", "### "):
            idx = text.find(f"{prefix}{key}")
            if idx != -1:
                break
        if idx == -1:
            print(f"MISS  {key}")
            continue
        end = text.find("</font>", idx)
        if end == -1:
            print(f"NO FONT BLOCK  {key}")
            continue
        block = text[idx:end]
        if "badge/Paper" in block:
            print(f"SKIP (has badge)  {key}")
            continue
        text = text[:end] + badge_html(paper_url, repo) + "\n" + text[end:]
        print(f"OK    {key}")

    # Marior is published at ACM MM 2022, not only on arXiv.
    text = text.replace(
        "<i>arXiv preprint</i> arXiv:2207.11515, 2022",
        "<i>ACM MM</i>, 2022",
    )

    with io.open(PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


if __name__ == "__main__":
    main()
