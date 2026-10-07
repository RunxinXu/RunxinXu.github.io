#!/usr/bin/env python3
"""Pull teaser figures out of papers for the Selected Publications column.

Requires PyMuPDF:  python3 -m pip install --user pymupdf

The figure box is derived from the actual vector/raster drawing primitives
sitting above a "Figure N:" caption, which is far more reliable than guessing
from text layout. Crops land in img/pubs/.

    # what figures does this paper have, and where?
    ./tools/pub-figures.py scan 2501.12948

    # crop Figure 1 (optionally just one half of a two-panel figure)
    ./tools/pub-figures.py crop 2501.12948 1 deepseek-r1 --half left

    # if the auto box is off, give explicit PDF-point coordinates
    ./tools/pub-figures.py crop 2412.19437 1 deepseek-v3 --page 1 --box 52,456,528,733

Then reference it from _data/publications.yml:

    figure: /img/pubs/deepseek-r1.png
    alt: "AIME accuracy of DeepSeek-R1-Zero rising over RL training"
"""
import argparse, pathlib, re, sys, urllib.request

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF missing:  python3 -m pip install --user pymupdf")

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "papers"
OUTDIR = ROOT / "img" / "pubs"
MAXEDGE = 480          # px; thumbnails render at ~136px, so this covers 3x
CAPTION = re.compile(r"^\s*(?:Figure|Fig\.?)\s*(\d+)\s*[:.|]", re.I)


def fetch(ref):
    """Accept a local path or an arXiv id; return a local PDF path."""
    p = pathlib.Path(ref)
    if p.exists():
        return p
    CACHE.mkdir(parents=True, exist_ok=True)
    dest = CACHE / f"{ref}.pdf"
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    url = f"https://arxiv.org/pdf/{ref}"
    # Try a direct connection first: a stale http_proxy in the environment is a
    # common failure here, and arXiv is reachable without one.
    for opener in (urllib.request.build_opener(urllib.request.ProxyHandler({})),
                   urllib.request.build_opener()):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with opener.open(req, timeout=120) as r:
                dest.write_bytes(r.read())
            print(f"fetched {url} -> {dest}")
            return dest
        except Exception as e:
            last = e
    sys.exit(f"could not download {url}: {last}")


def captions(doc, maxp=10):
    for pno in range(min(maxp, doc.page_count)):
        for b in doc[pno].get_text("blocks"):
            m = CAPTION.match(b[4])
            if m:
                yield pno, int(m.group(1)), fitz.Rect(*b[:4]), " ".join(b[4].split())


def figure_box(page, cap, lookup=430):
    """Union of drawing/image primitives directly above the caption."""
    parts = [d["rect"] for d in page.get_drawings()]
    for info in page.get_images(full=True):
        try:
            parts.extend(page.get_image_rects(info[0]))
        except Exception:
            pass

    keep = []
    for r in parts:
        if r.is_empty or r.height < 1.5 or r.width < 1.5:
            continue
        if r.y1 > cap.y0 + 3 or r.y1 < cap.y0 - lookup:
            continue                       # must be above the caption, but nearby
        if r.x1 < cap.x0 - 40 or r.x0 > cap.x1 + 40:
            continue                       # must overlap it horizontally
        if r.width > 0.92 * page.rect.width and r.height < 3:
            continue                       # page rules / header lines
        keep.append(r)
    if not keep:
        return None
    box = keep[0]
    for r in keep[1:]:
        box |= r
    return box


def cmd_scan(a):
    doc = fitz.open(fetch(a.paper))
    for pno, n, cap, txt in captions(doc, a.pages):
        box = figure_box(doc[pno], cap)
        desc = "%.0f,%.0f,%.0f,%.0f" % (box.x0, box.y0, box.x1, box.y1) if box else "no box found"
        size = " (%.0fx%.0f)" % (box.width, box.height) if box else ""
        print(f"  Figure {n}  page {pno+1}  box={desc}{size}")
        print(f"      {txt[:110]}")


def cmd_crop(a):
    doc = fitz.open(fetch(a.paper))
    for pno, n, cap, _ in captions(doc):
        if n != a.figure or (a.page and pno + 1 != a.page):
            continue
        if a.box:
            box = fitz.Rect(*[float(v) for v in a.box.split(",")])
        else:
            box = figure_box(doc[pno], cap)
            if not box:
                sys.exit(f"no drawing primitives above Figure {a.figure} on page {pno+1}; "
                         f"pass --box x0,y0,x1,y1")
            if a.half == "left":
                box.x1 = box.x0 + box.width / 2 - 2
            elif a.half == "right":
                box.x0 = box.x0 + box.width / 2 + 2
            box = fitz.Rect(box.x0 - a.pad, box.y0 - a.pad, box.x1 + a.pad, box.y1 + a.pad)
        box &= doc[pno].rect

        zoom = MAXEDGE / max(box.width, box.height)
        pix = doc[pno].get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=box)
        OUTDIR.mkdir(parents=True, exist_ok=True)
        out = OUTDIR / (a.name if a.name.endswith(".png") else a.name + ".png")
        pix.save(out)
        kb = out.stat().st_size // 1024
        print(f"{out.relative_to(ROOT)}  {pix.width}x{pix.height}px  {kb} KB  "
              f"(page {pno+1}, Figure {a.figure})")
        if kb > 140:
            print("  note: >140 KB — consider re-saving as JPEG")
        return
    sys.exit(f"Figure {a.figure} not found")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan", help="list figure captions and their detected boxes")
    s.add_argument("paper", help="arXiv id or path to a PDF")
    s.add_argument("--pages", type=int, default=10)
    s.set_defaults(fn=cmd_scan)

    c = sub.add_parser("crop", help="crop one figure into img/pubs/")
    c.add_argument("paper", help="arXiv id or path to a PDF")
    c.add_argument("figure", type=int, help="figure number, as printed in the paper")
    c.add_argument("name", help="output basename, e.g. deepseek-r1")
    c.add_argument("--page", type=int, help="disambiguate if the number repeats")
    c.add_argument("--half", choices=["left", "right"], help="keep only one panel")
    c.add_argument("--box", help="explicit PDF-point box x0,y0,x1,y1 (overrides detection)")
    c.add_argument("--pad", type=float, default=4.0)
    c.set_defaults(fn=cmd_crop)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
