#!/usr/bin/env python3
"""analyze-domain-age intro: Beaux Arts subway tile station, architecture and light only, nothing readable.
Blank mosaic panels, bench, window shafts, blurred passing light behind columns on the right."""
import random, sys
from PIL import Image, ImageDraw, ImageFilter
random.seed(31)
V1 = "--v1" in sys.argv
W, H = 1200, 520
CREAM = (238, 228, 200); TAN = (196, 164, 116); VIOLET = (62, 48, 96); CHROME = (196, 200, 204)
img = Image.new("RGB", (W, H), (36, 32, 52)); d = ImageDraw.Draw(img, "RGBA")
# vaulted ceiling lost in shadow
d.rectangle([0, 0, W, 120], fill=(28, 26, 44))
for i in range(6):
    d.arc([-100 + i * 60, -80, 700 + i * 60, 220], 0, 180, fill=(52, 48, 72), width=5)
# tiled wall in long recession: arches shrinking to the right into violet gloom
def arch(x, y, w, h, blank=True):
    d.rectangle([x, y + h * 0.28, x + w, y + h], fill=CREAM)
    d.pieslice([x, y, x + w, y + h * 0.56], 180, 360, fill=CREAM)
    d.rectangle([x, y + h * 0.28, x + w, y + h], outline=TAN, width=4)
    d.pieslice([x, y, x + w, y + h * 0.56], 180, 360, outline=TAN, width=4)
    # glazed tile grid
    for gx in range(x + 8, x + w - 4, 26):
        d.line([(gx, y + h * 0.3), (gx, y + h - 4)], fill=(222, 210, 178), width=1)
    for gy in range(int(y + h * 0.34), int(y + h) - 4, 20):
        d.line([(x + 4, gy), (x + w - 4, gy)], fill=(222, 210, 178), width=1)
    # mosaic band near the top
    for bx in range(x + 6, x + w - 8, 16):
        d.rectangle([bx, y + h * 0.30, bx + 12, y + h * 0.30 + 12], fill=VIOLET if (bx // 16) % 2 else TAN)
    # blank violet panel inside: no date, no device
    pw, ph = w * 0.52, h * 0.34
    d.rectangle([x + (w - pw) / 2, y + h * 0.44, x + (w + pw) / 2, y + h * 0.44 + ph], fill=VIOLET, outline=CHROME, width=2)
    # chrome keystone at crown
    kx = x + w / 2
    d.polygon([(kx - 9, y - 2), (kx + 9, y - 2), (kx + 5, y + 16), (kx - 5, y + 16)], fill=CHROME)
arch(40, 92, 300, 330)
arch(370, 108, 240, 280)
arch(636, 122, 192, 232)
arch(850, 134, 150, 196)
if not V1:
    arch(1018, 144, 116, 160)
# window shafts from high left, dust inside
for (x0, x1) in [(90, 300), (300, 520), (520, 700)]:
    d.polygon([(x0, 0), (x0 + 70, 0), (x1 + 60, 430), (x1 - 30, 430)], fill=(246, 238, 206, 42))
for _ in range(240):
    x, y = random.uniform(80, 760), random.uniform(10, 420); d.point((x, y), fill=(250, 244, 216))
# columns on the right and a blurred wash of moving light behind them
for cx in (880, 990, 1100):
    d.rectangle([cx, 120, cx + 34, 430], fill=(44, 40, 64))
wash = Image.new("RGB", (W, H), (0, 0, 0)); wd = ImageDraw.Draw(wash)
wd.rectangle([850, 210, 1200, 268], fill=(112, 92, 168))
wd.rectangle([850, 226, 1200, 240], fill=(210, 200, 220))
wash = wash.filter(ImageFilter.GaussianBlur(14))
img.paste(Image.blend(img, wash, 0.32), (0, 0)); d = ImageDraw.Draw(img, "RGBA")
for cx in (880, 990, 1100):
    d.rectangle([cx, 120, cx + 34, 430], fill=(44, 40, 64))
# bench under the middle arch, empty, dark wood
d.rectangle([408, 348, 580, 362], fill=(74, 54, 36)); d.rectangle([408, 376, 580, 388], fill=(74, 54, 36))
for lx in (420, 556):
    d.rectangle([lx, 362, lx + 10, 424], fill=(52, 38, 26))
# platform stone foreground, worn channel, fallen leaves, one loose cream tile face up
d.rectangle([0, 424, W, H], fill=(104, 96, 88))
d.polygon([(0, 436), (W, 428), (W, 448), (0, 458)], fill=(88, 80, 72))
for _ in range(700):
    x, y = random.uniform(0, W), random.uniform(428, H); d.point((x, y), fill=random.choice([(118, 110, 100), (94, 86, 78)]))
for _ in range(26):
    x, y = random.uniform(20, 640), random.uniform(424, 470)
    d.ellipse([x, y, x + 15, y + 6], fill=random.choice([(150, 116, 66), (128, 96, 54)]))
d.polygon([(742, 452), (796, 446), (802, 470), (748, 476)], fill=CREAM, outline=TAN, width=2)  # loose tile, glazed side up
d.line([(748, 458), (798, 452)], fill=(250, 244, 220), width=3)
img = img.filter(ImageFilter.GaussianBlur(0.4))
out = "scratch/intro-v1.png" if V1 else "intro-banner.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
