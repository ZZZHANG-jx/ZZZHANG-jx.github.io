#!/usr/bin/env python3
"""Render a static HTML preview of the site without needing Ruby.

Mirrors the Jekyll setup: pages under _pages/ are rendered through
_layouts/home.html, with `{% include xxx.html %}` resolved from _includes/.
The page content is raw HTML in the same class names as Shoufa Chen's
homepage, so the stylesheet in assets/css/homepage.css drives everything.
"""

import os
import re
import shutil

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "preview")

PAGES = [
    ("_pages/about.md", "index.html"),
    ("_pages/publications.md", "publications.html"),
    ("_pages/services.md", "services.html"),
]

INCLUDE_RE = re.compile(r"{%\s*include\s+([^\s%]+)\s*%}")


def read_front_matter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, match.group(2)


def resolve_includes(html):
    """Replace {% include name %} with the contents of _includes/name."""
    def repl(m):
        name = m.group(1).strip()
        path = os.path.join(ROOT, "_includes", name)
        if not os.path.exists(path):
            return f"<!-- missing include: {name} -->"
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    return INCLUDE_RE.sub(repl, html)


def render_page(site, page, body):
    layout_name = page.get("layout") or "home"
    layout_path = os.path.join(ROOT, "_layouts", f"{layout_name}.html")
    with open(layout_path, encoding="utf-8") as fh:
        layout = fh.read()

    body = resolve_includes(body).strip()
    html = layout.replace("{{ content }}", body)
    html = html.replace("{{ site.title }}", site.get("title", "Jiaxin Zhang"))

    # Preview is served from preview/ ; anchor links to the single page become
    # index.html#... so they work both from file:// and the local server.
    html = html.replace('href="/#', 'href="index.html#')
    return html


def main():
    with open(os.path.join(ROOT, "_config.yml"), encoding="utf-8") as fh:
        site = yaml.safe_load(fh) or {}

    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets", "css"), exist_ok=True)

    # Stylesheet + font folders the page needs.
    shutil.copyfile(
        os.path.join(ROOT, "assets", "css", "homepage.css"),
        os.path.join(OUT, "assets", "css", "homepage.css"),
    )
    for folder in ("webfonts", "fonts"):
        src_dir = os.path.join(ROOT, "assets", folder)
        if os.path.isdir(src_dir):
            shutil.copytree(src_dir, os.path.join(OUT, "assets", folder), dirs_exist_ok=True)

    for src, out_name in PAGES:
        page, body = read_front_matter(os.path.join(ROOT, src))
        html_out = render_page(site, page, body)
        with open(os.path.join(OUT, out_name), "w", encoding="utf-8") as fh:
            fh.write(html_out)
        print(f"wrote preview/{out_name}  ({len(html_out)} bytes)")


if __name__ == "__main__":
    main()
