#!/usr/bin/env python3
"""analyze-domain-age logo: single arched mosaic panel, tan tile border, chrome keystone,
one date worked as pale mosaic tile inside a deep dusk violet field, hairline crack to the date."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
V1 = "--v1" in sys.argv
W, H = 900, 520
CREAM = (238, 228, 200); TAN = (196, 164, 116); VIOLET = (52, 40, 88); CHROME = (204, 208, 212)
img = Image.new("RGB", (W, H), VIOLET); d = ImageDraw.Draw(img, "RGBA")
x0, y0, x1, y1 = 250, 36, 650, 372
# arched panel: rectangle plus half circle top, border of small glazed tan tiles
d.pieslice([x0, y0, x1, y0 + (x1 - x0)], 180, 360, fill=TAN)
d.rectangle([x0, y0 + (x1 - x0) // 2, x1, y1], fill=TAN)
step = 25
for bx in range(x0 + 4, x1 - 12, step):
    d.rectangle([bx, y0 + (x1 - x0) // 2 + 4, bx + 19, y0 + (x1 - x0) // 2 + 24], fill=(210, 182, 132), outline=(168, 138, 92))
    d.rectangle([bx, y1 - 26, bx + 19, y1 - 6], fill=(210, 182, 132), outline=(168, 138, 92))
for by in range(y0 + (x1 - x0) // 2 + 30, y1 - 30, step):
    d.rectangle([x0 + 4, by, x0 + 23, by + 19], fill=(210, 182, 132), outline=(168, 138, 92))
    d.rectangle([x1 - 23, by, x1 - 4, by + 19], fill=(210, 182, 132), outline=(168, 138, 92))
# inner violet field
ix0, iy0, ix1, iy1 = x0 + 32, y0 + 44, x1 - 32, y1 - 34
d.pieslice([ix0, iy0, ix1, iy0 + (ix1 - ix0)], 180, 360, fill=(62, 48, 96))
d.rectangle([ix0, iy0 + (ix1 - ix0) // 2, ix1, iy1], fill=(62, 48, 96))
# chrome keystone at top of arch
kx = 450
d.polygon([(kx - 20, y0 - 4), (kx + 20, y0 - 4), (kx + 11, y0 + 36), (kx - 11, y0 + 36)], fill=CHROME, outline=(150, 154, 158))
# date as mosaic: pale tile blocks forming a day, month, year pattern (tile squares, not type)
# Rendered as small pale tiles grouped as digit-like columns so the field reads as a set date.
try:
    fdate = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/Audiowide.ttf", 38)
except Exception:
    fdate = ImageFont.load_default()
if not V1:
    d.text((450, 238), "12 · 04 · 1998", font=fdate, fill=CREAM, anchor="mm")
else:
    d.rectangle([330, 216, 570, 258], fill=CREAM)  # v1 flaw: plain block, reads as a label bar
# hairline crack from keystone down to the date, stopping at its edge
pts = [(450, 40), (444, 84), (452, 122), (446, 160), (450, 196)]
d.line(pts, fill=(24, 20, 36), width=2)
try:
    f = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/Audiowide.ttf", 40)
except Exception:
    f = ImageFont.load_default()
d.text((450, 440), "analyze-domain-age", font=f, fill=CHROME, anchor="mm")
img = img.filter(ImageFilter.GaussianBlur(0.3))
out = "scratch/logo-v1.png" if V1 else "logo.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out)
if not V1:
    img.resize((64, 37)).save(__file__.rsplit("/", 1)[0] + "/scratch/logo64-ship.png")
print("saved", out)
