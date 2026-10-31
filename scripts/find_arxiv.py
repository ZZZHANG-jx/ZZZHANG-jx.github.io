"""Locate arXiv preprints for papers that lack open PDFs."""

import re
import sys
import time
import urllib.parse
import urllib.request

QUERIES = {
    "lego": 'all:"LEGO Self-supervised representation learning scene text images"',
    "qttextsr": 'all:"QT-TextSR scene text image super-resolution"',
    "scenetable": 'all:"Scene table structure recognition segmentation collaboration alignment"',
    "higherlevel": 'all:"Looking from a higher-level perspective scene text segmentation"',
    "complextable": 'all:"Complex table structure recognition in the wild transformer identity matrix"',
    "forgery": 'all:"Forgery-free signature verification stroke-aware cycle-consistent"',
    "dochighlight": 'all:"DocHighlight specular highlight removal document"',
    "qdrformer": 'all:"Q-DRFormer query-position mapping flow document rectification"',
    "tpgcat": 'all:"Text prior-guided cell alignment transformer table structure"',
    "autoscaler": 'all:"AutoScaler self scale alignment handwritten mathematical expression"',
}


def main(keys):
    for key in keys:
        q = QUERIES[key]
        url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
            {"search_query": q, "max_results": 3}
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "homepage-build/1.0"})
            xml = urllib.request.urlopen(req, timeout=35).read().decode("utf-8", "ignore")
        except Exception as exc:  # noqa: BLE001
            print(f"{key:14s} ERR {exc}")
            time.sleep(3)
            continue
        ids = re.findall(r"<id>http://arxiv\.org/abs/([^<]+)</id>", xml)
        titles = [re.sub(r"\s+", " ", t).strip() for t in re.findall(r"<title>(.*?)</title>", xml, re.S)][1:]
        if not ids:
            print(f"{key:14s} none")
        for i, aid in enumerate(ids[:3]):
            title = titles[i] if i < len(titles) else ""
            print(f"{key:14s} {aid:12s} {title[:70]}")
        time.sleep(3)


if __name__ == "__main__":
    main(sys.argv[1:] or list(QUERIES))
