#!/usr/bin/env python3
"""Render a static HTML preview of the Jekyll site without needing Ruby.

Reads _config.yml, _data/navigation.yml and the Markdown pages under _pages/,
then writes plain HTML into preview/ using the real compiled stylesheet.
"""

import os
import re
import shutil
import html as html_mod

import yaml
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "preview")

PAGES = [
    # (source, output filename, layout)
    ("_pages/about.md", "index.html", "single"),
    ("_pages/publications.md", "publications.html", "archive"),
    ("_pages/services.md", "services.html", "archive"),
]

URL_MAP = {"/": "index.html", "/publications/": "publications.html", "/services/": "services.html"}


def read_front_matter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, match.group(2)


def to_html(text):
    return markdown.markdown(
        text,
        extensions=["extra", "tables", "sane_lists", "md_in_html", "attr_list", "fenced_code"],
    )


def esc(value):
    return html_mod.escape(str(value), quote=True)


def build_sidebar(author):
    parts = ['<div class="sidebar sticky">', '<div itemscope itemtype="http://schema.org/Person">']

    avatar = author.get("avatar") or ""
    if avatar:
        src = avatar if "://" in avatar else "../images/" + avatar
        parts.append(
            f'<div class="author__avatar"><img src="{esc(src)}" class="author__avatar" '
            f'alt="{esc(author.get("name", ""))}" fetchpriority="high" /></div>'
        )

    parts.append('<div class="author__content">')
    parts.append(f'<h3 class="author__name">{esc(author.get("name", ""))}</h3>')
    if author.get("pronouns"):
        parts.append(f'<p class="author__pronouns">{esc(author["pronouns"])}</p>')
    if author.get("bio"):
        parts.append(f'<p class="author__bio">{esc(author["bio"])}</p>')
    parts.append("</div>")

    rows = []
    if author.get("location"):
        rows.append(
            '<li class="author__desktop"><i class="fas fa-fw fa-location-dot icon-pad-right" '
            f'aria-hidden="true"></i>{esc(author["location"])}</li>'
        )
    if author.get("employer"):
        rows.append(
            '<li class="author__desktop"><i class="fas fa-fw fa-building-columns icon-pad-right" '
            f'aria-hidden="true"></i>{esc(author["employer"])}</li>'
        )
    if author.get("email"):
        rows.append(
            f'<li><i class="fas fa-fw fa-envelope '
            f'icon-pad-right" aria-hidden="true"></i><span class="author-email">{esc(author["email"])}</span></li>'
        )
    if author.get("googlescholar"):
        rows.append(
            f'<li><a href="{esc(author["googlescholar"])}"><i class="ai ai-google-scholar ai-fw '
            f'icon-pad-right" aria-hidden="true"></i>Google Scholar</a></li>'
        )
    if author.get("orcid"):
        rows.append(
            f'<li><a href="{esc(author["orcid"])}"><i class="ai ai-orcid ai-fw '
            f'icon-pad-right" aria-hidden="true"></i>ORCID</a></li>'
        )
    if author.get("github"):
        rows.append(
            f'<li><a href="https://github.com/{esc(author["github"])}"><i class="fab fa-fw '
            f'fa-github icon-pad-right" aria-hidden="true"></i>GitHub</a></li>'
        )

    parts.append('<div class="author__urls-wrapper">')
    parts.append('<button class="btn btn--inverse">Follow</button>')
    parts.append('<ul class="author__urls social-icons">')
    parts.extend(rows)
    parts.append("</ul></div></div></div>")
    return "\n".join(parts)


def build_masthead(site_title, nav):
    items = [
        f'<li class="masthead__menu-item masthead__menu-item--lg persist">'
        f'<a href="index.html">{esc(site_title)}</a></li>'
    ]
    for link in nav:
        target = URL_MAP.get(link["url"], link["url"])
        items.append(
            f'<li class="masthead__menu-item"><a href="{esc(target)}">{esc(link["title"])}</a></li>'
        )
    return f"""<div class="masthead">
  <div class="masthead__inner-wrap">
    <div class="masthead__menu">
      <nav id="site-nav" class="greedy-nav">
        <button><div class="navicon"></div></button>
        <ul class="visible-links">
          {chr(10).join("          " + i for i in items)}
        </ul>
        <ul class="hidden-links hidden"></ul>
      </nav>
    </div>
  </div>
</div>"""


def build_footer(site, author):
    link = ""
    if author.get("github"):
        link = (
            f'<li><a href="https://github.com/{esc(author["github"])}">'
            '<i class="fab fa-github" aria-hidden="true"></i> GitHub</a></li>'
        )
    return f"""<div class="page__footer">
  <footer>
    <div class="page__footer-follow">
      <ul class="social-icons">{link}</ul>
    </div>
    <div class="page__footer-copyright">
      &copy; 2026 {esc(site.get("name", ""))}, Powered by
      <a href="http://jekyllrb.com" rel="nofollow">Jekyll</a> &amp;
      <a href="https://github.com/academicpages/academicpages.github.io">AcademicPages</a>.
      <br />Local preview — not the deployed site.
    </div>
  </footer>
</div>"""


def wrap_page(*, site, author, nav, page, body_html, layout):
    title = page.get("title") or site.get("title", "")
    full_title = title if title == site.get("title") else f"{title} - {site.get('title', '')}"

    # Honor author_profile: false (set in front matter or _config.yml) -> drop the
    # academicpages sidebar so the page reads like a clean, custom homepage.
    page_ap = page.get("author_profile")
    site_ap = (site.get("author") or {}).get("author_profile")
    show_sidebar = not (page_ap is False or site_ap is False)

    if layout == "archive":
        page_title = (page.get("title") or "").strip()
        h1 = f'<h1 class="page__title">{esc(page_title)}</h1>\n    ' if page_title else ""
        sidebar = build_sidebar(author) if show_sidebar else ""
        content = f"""<div id="main" role="main">
  {sidebar}
  <div class="archive">
    {h1}{body_html}
  </div>
</div>"""
    else:
        content = f"""<div id="main" role="main">
  {build_sidebar(author)}
  <article class="page" itemscope itemtype="http://schema.org/CreativeWork">
    <div class="page__inner-wrap">
      <section class="page__content" itemprop="text">
        {body_html}
      </section>
    </div>
  </article>
</div>"""

    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8" />
  <title>{esc(full_title)}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="assets/css/main.css" />
  <link rel="stylesheet" href="assets/css/academicons.css" />
  <style>
    /* Preview-only: the real site hides this via greedy-nav JS. */
    .greedy-nav button {{ display: none !important; }}
    .author__urls-wrapper button {{ display: none !important; }}
  </style>
</head>
<body>
{build_masthead(site.get("title", ""), nav)}
{content}
{build_footer(site, author)}
</body>
</html>
"""


def main():
    with open(os.path.join(ROOT, "_config.yml"), encoding="utf-8") as fh:
        site = yaml.safe_load(fh)
    with open(os.path.join(ROOT, "_data", "navigation.yml"), encoding="utf-8") as fh:
        nav = (yaml.safe_load(fh) or {}).get("main", [])

    author = site.get("author", {}) or {}
    os.makedirs(OUT, exist_ok=True)

    # Assets the stylesheet expects next to itself.
    for folder in ("webfonts", "fonts"):
        src_dir = os.path.join(ROOT, "assets", folder)
        dst_dir = os.path.join(OUT, "assets", folder)
        if os.path.isdir(src_dir):
            shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

    for src, out_name, layout in PAGES:
        page, body = read_front_matter(os.path.join(ROOT, src))
        body_html = to_html(body)
        html_out = wrap_page(
            site=site, author=author, nav=nav, page=page, body_html=body_html, layout=layout
        )
        with open(os.path.join(OUT, out_name), "w", encoding="utf-8") as fh:
            fh.write(html_out)
        print(f"wrote preview/{out_name}  ({len(html_out)} bytes)")


if __name__ == "__main__":
    main()
