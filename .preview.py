#!/usr/bin/env python3
"""Render index.md the way Jekyll would, into /tmp/rx-preview, for local preview.

This is a stand-in for `jekyll serve` (the system Ruby is too old to install the
site's Gemfile). It expands the same Liquid loops and front matter that Jekyll
would, and symlinks the real css/ and img/ so what you see is the real stylesheet.
"""
import re, pathlib, shutil, html, yaml

ROOT = pathlib.Path("/Users/zhuhan/Desktop/RunxinXu.github.io")
OUT = pathlib.Path("/tmp/rx-preview")

SITE = yaml.safe_load((ROOT / "_config.yml").read_text())
PUBS = yaml.safe_load((ROOT / "_data/publications.yml").read_text())

raw = (ROOT / "index.md").read_text()
_, fm_text, body = raw.split("---", 2)
PAGE = yaml.safe_load(fm_text)


def md_inline(t):
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', t)
    t = t.replace("'", "’").replace("--", "–")
    return t


# 1. publications loop
items = []
for p in PUBS:
    links = p.get("links") or []
    title = html.escape(p["title"])
    title = f'<a href="{links[0]["url"]}">{title}</a>' if links else title
    flag = f'<span class="pub-flag">{p["note"]}</span>' if p.get("note") else ""
    bar = ""
    if links:
        bar = '<p class="pub-links">' + '<span class="pub-sep">·</span>'.join(
            f'<a href="{l["url"]}">{l["name"]}</a>' for l in links) + "</p>"
    fig = ""
    if p.get("figure"):
        img = (f'<img src="{p["figure"]}" alt="{p.get("alt", p["title"])}" loading="lazy" />')
        inner = f'<a href="{links[0]["url"]}">{img}</a>' if links else img
        fig = f'<figure class="pub-fig">{inner}</figure>'
    items.append(
        f'<li class="pub"><div class="pub-venue">{p["venue"]}</div><div>'
        f'<div class="pub-title">{title}</div>'
        f'<p class="pub-authors">{p["authors"]}</p>{flag}{bar}</div>{fig}</li>')
# drop the has_figures probe loop, resolve its class, then expand the real loop
body = re.sub(r"\{%-? assign has_figures.*?\{%-? endfor -?%\}\s*", "", body, flags=re.S, count=1)
_has = " has-figures" if any(p.get("figure") for p in PUBS) else ""
body = body.replace('<ol class="pub-list{% if has_figures %} has-figures{% endif %}">',
                    f'<ol class="pub-list{_has}">')
body = re.sub(r"\{%-? for pub in site\.data\.publications.*\{%-? endfor -?%\}",
              "\n".join(items), body, flags=re.S)

# 2. the markdown="1" section
def md_section(m):
    out = []
    for blk in re.split(r"\n\s*\n", m.group(2).strip()):
        blk = blk.strip()
        if not blk:
            continue
        out.append(blk if blk.startswith("<") else f"<p>{md_inline(blk.replace(chr(10), ' '))}</p>")
    return m.group(1).replace(' markdown="1"', "") + "\n" + "\n".join(out) + "\n</section>"

body = re.sub(r'(<section[^>]*markdown="1">)(.*?)</section>', md_section, body, flags=re.S)

# 3. layout + remaining Liquid
page = (ROOT / "_layouts/academic.html").read_text()
nav = "".join(
    '<li><a href="{}"{}>{}</a></li>'.format(
        i["url"], ' class="is-secondary"' if i.get("secondary") else "", i["name"])
    for i in PAGE["page-nav"])
page = re.sub(r'<ul class="topbar-nav">.*?</ul>', f'<ul class="topbar-nav">{nav}</ul>', page, flags=re.S)
page = page.replace("{{ content }}", body)

VARS = {
    "site.title": SITE["title"],
    "site.description": SITE["description"],
    "site.title-separator": SITE["title-separator"],
    "site.url": SITE["url"],
    "site.author.name": SITE["author"]["name"],
    "page.meta-title": PAGE["meta-title"],
    "page.meta-description": " ".join(PAGE["meta-description"].split()),
    "page.share-img": PAGE["share-img"],
    "page.url": "/",
}
page = re.sub(r"\{%.*?%\}", "", page, flags=re.S)          # drop includes/conditionals
page = re.sub(r"\{\{\s*'([^']+)'\s*\|\s*prepend:[^}]*\}\}", r"\1", page)  # asset paths
page = re.sub(r"\{\{\s*site\.time\s*\|\s*date:\s*'%Y'\s*\}\}", "2026", page)
page = re.sub(r"\{\{\s*site\.time\s*\|\s*date:\s*'%B %Y'\s*\}\}", "October 2026", page)
def sub_var(m):
    key = m.group(1).split("|")[0].strip()
    return str(VARS.get(key, ""))
page = re.sub(r"\{\{(.*?)\}\}", sub_var, page, flags=re.S)

# 4. write it out next to symlinks of the real assets
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
(OUT / "index.html").write_text(page)
for asset in ("css", "img"):
    (OUT / asset).symlink_to(ROOT / asset)
print(f"rendered {OUT/'index.html'}  ({len(page)} bytes)")
