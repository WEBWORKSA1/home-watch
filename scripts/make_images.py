#!/usr/bin/env python3
"""Generate the favicon, app icons and the social preview image (needs Pillow). Run once; outputs are committed."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
NIGHT, WINDOW, WHITE, MUTED = (27, 36, 64), (255, 200, 87), (255, 255, 255), (199, 206, 224)
os.makedirs(IMG, exist_ok=True)

SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#1B2440"/>
<path d="M13 31 32 15l19 16v19a3 3 0 0 1-3 3H16a3 3 0 0 1-3-3Z" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>
<rect x="25" y="32" width="14" height="13" rx="2" fill="#FFC857"/></svg>"""
open(os.path.join(IMG, "favicon.svg"), "w").write(SVG)


def house(draw, cx, cy, s, stroke=WHITE, width=None):
    w = width or max(2, int(s * 0.065))
    pts = [(cx - s * .3, cy - s * .02), (cx, cy - s * .27), (cx + s * .3, cy - s * .02)]
    draw.line(pts, fill=stroke, width=w, joint="curve")
    draw.line([(cx - s * .3, cy - s * .02), (cx - s * .3, cy + s * .28), (cx + s * .3, cy + s * .28), (cx + s * .3, cy - s * .02)], fill=stroke, width=w, joint="curve")
    draw.rounded_rectangle([cx - s * .11, cy + s * .01, cx + s * .11, cy + s * .2], radius=max(1, int(s * .02)), fill=WINDOW)


for size in (180, 192, 512):
    im = Image.new("RGB", (size, size), NIGHT)
    house(ImageDraw.Draw(im), size / 2, size / 2, size * .9)
    im.save(os.path.join(IMG, "icon-%d.png" % size))


def font(size, bold=True):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


og = Image.new("RGB", (1200, 630), NIGHT)
d = ImageDraw.Draw(og)
d.ellipse([700, 260, 1500, 1000], fill=(43, 50, 78))
house(d, 960, 300, 420, width=16)
d.text((80, 140), "Home.Watch", font=font(92), fill=WHITE)
d.text((84, 270), "Your home is empty.", font=font(46), fill=WINDOW)
d.text((84, 330), "It shouldn't be unwatched.", font=font(46), fill=WINDOW)
d.text((84, 450), "Home watch pros, free tools and live alerts", font=font(30, False), fill=MUTED)
d.text((84, 492), "for seasonal and second homes.", font=font(30, False), fill=MUTED)
og.save(os.path.join(IMG, "og.png"), optimize=True)
print("images written")
