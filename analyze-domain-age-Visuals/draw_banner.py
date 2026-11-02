#!/usr/bin/env python3
"""analyze-domain-age wordmark banner: inside the vaulted station, tile frieze with central mosaic date,
letter tiles spelling the name above it, dust shafts, train as a violet light smear behind columns."""
import random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(41)
V1 = "--v1" in sys.argv
W, H = 1200, 420
CREAM = (238, 228, 200); TAN = (196, 164, 116); VIOLET = (62, 48, 96); CHROME = (204, 208, 212)
img = Image.new("RGB", (W, H), (34, 30, 50)); d = ImageDraw.Draw(img, "RGBA")
d.rectangle([0, 0, W, 74], fill=(26, 24, 42))  # vault shadow
for i in range(5):
    d.arc([-60 + i * 40, -90, 760 + i * 40, 170], 0, 180, fill=(50, 46, 70), width=4)
# frieze wall full width
d.rectangle([0, 74, W, 330], fill=CREAM)
for gx in range(0, W, 30):
    d.line([(gx, 78), (gx, 326)], fill=(224, 212, 182), width=1)
for gy in range(84, 330, 24):
    d.line([(0, gy), (W, gy)], fill=(224, 212, 182), width=1)
# alternating mosaic band
for bx in range(0, W, 22):
    d.rectangle([bx, 92, bx + 18, 110], fill=VIOLET if (bx // 22) % 2 else TAN)
# central mosaic panel with one date
px0, py0, px1, py1 = 440, 150, 760, 300
d.rectangle([px0, py0, px1, py1], fill=VIOLET, outline=TAN, width=6)
d.polygon([(592, py0 - 16), (608, py0 - 16), (604, py0 + 2), (596, py0 + 2)], fill=CHROME)  # keystone
d.line([(600, py0 + 4), (594, py0 + 50), (602, py0 + 84)], fill=(22, 18, 34), width=2)  # crack
try:
    fdate = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/Audiowide.ttf", 44)
    fname = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/Audiowide.ttf", 27)
except Exception:
    fdate = fname = ImageFont.load_default()
d.text((600, 226), "12 · 04 · 1998", font=fdate, fill=CREAM, anchor="mm")
# name in individual letter tiles set into the frieze above the central mosaic
name = "analyze-domain-age"
tw = 30; total = len(name) * tw; sx = 600 - total / 2
for i, ch in enumerate(name):
    x = sx + i * tw
    d.rectangle([x + 2, 116, x + tw - 2, 144], fill=VIOLET, outline=CHROME, width=1)
    d.text((x + tw / 2, 130), ch, font=fname, fill=CHROME, anchor="mm")
# dust shafts from high windows on the left, landing on fixtures
for (x0, x1) in [(40, 210), (230, 400), (430, 610)]:
    d.polygon([(x0, 0), (x0 + 58, 0), (x1 + 48, 336), (x1 - 24, 336)], fill=(248, 240, 208, 40))
for _ in range(180):
    x, y = random.uniform(30, 680), random.uniform(6, 330); d.point((x, y), fill=(252, 246, 218))
# fixtures: bench, shuttered ticket window with grille, round clock with no stated hour (blank face)
d.rectangle([120, 268, 268, 280], fill=(76, 56, 38)); d.rectangle([120, 292, 268, 302], fill=(76, 56, 38))
for lx in (132, 246):
    d.rectangle([lx, 280, lx + 9, 330], fill=(54, 40, 28))
d.rectangle([872, 176, 972, 286], fill=(120, 104, 84))
for gy in range(184, 240, 9):
    d.line([(876, gy), (968, gy)], fill=(52, 46, 40), width=3)  # grille slats
d.ellipse([300, 168, 366, 234], fill=CREAM, outline=CHROME, width=5)  # clock, blank face, no hands forming characters
# platform edge and the passing train as violet smear behind columns on the right
smear = Image.new("RGB", (W, H), (0, 0, 0)); sd = ImageDraw.Draw(smear)
sd.rectangle([930, 196, 1200, 252], fill=(116, 96, 176)); sd.rectangle([930, 214, 1200, 228], fill=(216, 208, 226))
smear = smear.filter(ImageFilter.GaussianBlur(10))
img.paste(Image.blend(img, smear, 0.30), (0, 0)); d = ImageDraw.Draw(img, "RGBA")
for cx in (966, 1056, 1146):
    d.rectangle([cx, 84, cx + 26, 336], fill=(40, 36, 60))
d.rectangle([0, 330, W, H], fill=(100, 92, 84))
d.line([(0, 330), (W, 330)], fill=TAN, width=4)
img = img.filter(ImageFilter.GaussianBlur(0.4))
out = "scratch/banner-v1.png" if V1 else "banner.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
