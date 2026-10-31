#!/usr/bin/env python3
"""Wrap publication entries that now have a thumbnail in the .pub-row layout."""

import io

PATH = "_pages/publications.md"

FIGURES = {
    "DocAligner: Automating": ("docaligner.jpg", "DocAligner pipeline"),
    "Beyond Token Compression": ("beyondtoken.jpg", "Decoder-only vs cross-attention architectures"),
    "OCRGenBench": ("ocrgenbench.jpg", "OCRGenBench task taxonomy"),
    "UPOCR: Towards Unified": ("upocr.jpg", "UPOCR unified pixel-level OCR interface"),
    "M6Doc: A Large-Scale": ("m6doc.jpg", "M6Doc dataset samples"),
    "Smaller but Better": ("smallerbetter.jpg", "Layout generation across document types"),
    "AutoScaler: Self Scale": ("autoscaler.jpg", "AutoScaler framework"),
    "Appearance Enhancement": ("appearance.jpg", "GCDRNet architecture"),
    "LEGO: Self-Supervised": ("lego.jpg", "LEGO self-supervised pretraining"),
    "Looking from a Higher-Level": ("higherlevel.jpg", "Multi-scale scene text segmentation examples"),
    "Enhancing Document Dewarping Evaluation": ("enhancing.jpg", "Document dewarping evaluation metric"),
    "Marior: Margin Removal": ("marior.jpg", "Document dewarping comparison"),
}


def main():
    text = io.open(PATH, encoding="utf-8").read()

    for key, (img, alt) in FIGURES.items():
        idx = -1
        for prefix in ("### ", "<h3>"):
            idx = text.find(prefix + key)
            if idx != -1:
                break
        if idx == -1:
            print(f"MISS {key}")
            continue

        # Already inside a two-column row? Then the <h3> is preceded by <div class="pub-text">.
        if "pub-text" in text[max(0, idx - 80) : idx]:
            print(f"SKIP (already wrapped) {key}")
            continue

        end = text.find("</p>", idx)
        if end == -1:
            print(f"NO END {key}")
            continue
        end += len("</p>")
        block = text[idx:end]

        if "pub-row" in block:
            print(f"SKIP (already wrapped) {key}")
            continue

        first_line, rest = block.split("\n", 1)
        title = first_line.replace("### ", "").replace("<h3>", "").replace("</h3>", "").strip()

        new_block = (
            '<div class="pub-row">\n'
            f'<div class="pub-fig"><img src="../images/publication_imgs/{img}" alt="{alt}" /></div>\n'
            '<div class="pub-text">\n'
            f"<h3>{title}</h3>\n"
            f"{rest}"
            "\n</div>\n</div>"
        )
        text = text[:idx] + new_block + text[end:]
        print(f"OK   {key}")

    io.open(PATH, "w", encoding="utf-8", newline="\n").write(text)


if __name__ == "__main__":
    main()
