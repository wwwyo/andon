# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools==4.68.0", "uharfbuzz==0.57.0"]
# ///
"""Generate assets/logo/*.svg from the values in design.md's Logo section.

Run from the repo root:  uv run tools/logo/build.py
The font is downloaded from google/fonts at a pinned commit and checked by sha256.
Edit the values below together with design.md, then regenerate.
"""

import hashlib
import tempfile
import urllib.request
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

FONT_URL = "https://raw.githubusercontent.com/google/fonts/ef3b6f8df2d299a7a82c68cd8743c8f9c11e1c8f/ofl/zenmarugothic/ZenMaruGothic-Bold.ttf"
FONT_SHA256 = "fe24426b9c8b5523a0146a8235c8674eccf0493af354a53ec895c3596d9eb745"

# Logo values (units: 1000 = one em of the font). Keep in sync with design.md.
TRACKING = 0
KERN = [-15, -5, -15, -15]  # A-n, n-d, d-dot, dot-n
SYM_GAP = 220
SYM_Y = -80  # + moves the symbol up; 0 = book bottom on the baseline
DOT = 90  # % of the o's outer height
SYM_SCALE = 1.25  # symbol height / cap height

INK, PAPER, LIGHT = "#2b2420", "#f6ecd8", "#f0a43a"
THEMES = {
    "": dict(text=INK, rim=INK, gut=INK),
    "-dark": dict(text="#e6edf3", rim="#cbb999", gut="#b3a183"),
}
MARGIN = 20
OUT = Path("assets/logo")


def symbol(t):
    return (
        f'<g transform="rotate(-10 32 46)"><circle cx="32" cy="36" r="17" fill="{LIGHT}"/>'
        f'<circle cx="29.4" cy="32.2" r="2.7" fill="{INK}"/><circle cx="39.4" cy="32.2" r="2.7" fill="{INK}"/></g>'
        f'<path d="M6 40 Q19 34 32 40 V56 Q19 50 6 56 Z" fill="{PAPER}" stroke="{t["rim"]}" stroke-width="3" stroke-linejoin="round"/>'
        f'<path d="M58 40 Q45 34 32 40 V56 Q45 50 58 56 Z" fill="{PAPER}" stroke="{t["rim"]}" stroke-width="3" stroke-linejoin="round"/>'
        f'<line x1="32" y1="40.5" x2="32" y2="55.5" stroke="{t["gut"]}" stroke-width="2"/>'
    )


def load_font():
    data = urllib.request.urlopen(FONT_URL).read()
    if hashlib.sha256(data).hexdigest() != FONT_SHA256:
        raise SystemExit("font sha256 mismatch")
    path = Path(tempfile.mkdtemp()) / "ZenMaruGothic-Bold.ttf"
    path.write_bytes(data)
    return path


def shape(path):
    tt = TTFont(path)
    gs = tt.getGlyphSet()
    font = hb.Font(hb.Face(hb.Blob.from_file_path(str(path))))
    buf = hb.Buffer()
    buf.add_str("Andon")
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": False})
    order = tt.getGlyphOrder()
    glyphs = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        pen, bp = SVGPathPen(gs), BoundsPen(gs)
        gs[name].draw(pen)
        gs[name].draw(bp)
        glyphs.append({"d": pen.getCommands(), "adv": pos.x_advance, "bbox": bp.bounds})
    return tt["OS/2"].sCapHeight, glyphs


def positions(glyphs, x0):
    pos, x = [], x0
    for i in range(len(glyphs)):
        if i:
            x += glyphs[i - 1]["adv"] + TRACKING + KERN[i - 1]
        pos.append(x)
    return pos


def word(glyphs, pos, t):
    s = []
    for i, g in enumerate(glyphs):
        if i == 3:
            x0, y0, x1, y1 = g["bbox"]
            r = (y1 - y0) / 2 * DOT / 100
            s.append(f'<circle cx="{pos[i] + (x0 + x1) / 2:.1f}" cy="{-(y0 + y1) / 2:.1f}" r="{r:.1f}" fill="{LIGHT}"/>')
        else:
            s.append(f'<path transform="translate({pos[i]:.1f} 0) scale(1 -1)" d="{g["d"]}" fill="{t["text"]}"/>')
    return "".join(s)


def svg(vb, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="Andon"><title>Andon</title>{body}</svg>\n'


def box(left, top, right, bottom):
    return f"{left - MARGIN:.0f} {top - MARGIN:.0f} {right - left + 2 * MARGIN:.0f} {bottom - top + 2 * MARGIN:.0f}"


def main():
    cap, glyphs = shape(load_font())
    sh = cap * SYM_SCALE
    sw = sh * 56 / 40
    k = sh / 40
    ascent = max(g["bbox"][3] for g in glyphs)
    descent = min(g["bbox"][1] for g in glyphs)
    OUT.mkdir(parents=True, exist_ok=True)
    for suf, t in THEMES.items():
        (OUT / f"andon-symbol{suf}.svg").write_text(svg("2 8.25 60 60", symbol(t)))

        pos = positions(glyphs, sw + SYM_GAP)
        ty = -sh - SYM_Y
        body = f'<g transform="translate(0 {ty:.1f}) scale({k:.4f}) translate(-4 -18)">{symbol(t)}</g>' + word(glyphs, pos, t)
        vb = box((4.5 - 4) * k, min(ty + (19.15 - 18) * k, -ascent), pos[4] + glyphs[4]["bbox"][2], max(ty + (57.5 - 18) * k, -descent))
        (OUT / f"andon-logo{suf}.svg").write_text(svg(vb, body))

        pos = positions(glyphs, 0)
        vb = box(pos[0] + glyphs[0]["bbox"][0], -ascent, pos[4] + glyphs[4]["bbox"][2], -descent)
        (OUT / f"andon-wordmark{suf}.svg").write_text(svg(vb, word(glyphs, pos, t)))


if __name__ == "__main__":
    main()
