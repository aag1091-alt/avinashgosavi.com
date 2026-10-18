#!/usr/bin/env python3
"""Generate 1200x630 share-preview cards for posts without an `image:`.

Run from the repo root:  python3 scripts/og_cards.py
Writes assets/og/<slug>.png and adds `image:` to each post's front matter.
"""
import glob, os, re, textwrap
from PIL import Image, ImageDraw, ImageFont

BG, SURFACE, TEXT, MUTED, ACCENT = "#f5efe0", "#e8e0cc", "#352f2a", "#5c5650", "#0f766e"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
W, H, PAD = 1200, 630, 80

def card(title, tags, out):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 14, H], fill=ACCENT)
    size = 64
    while True:
        f = ImageFont.truetype(BOLD, size)
        chars = max(10, int((W - 2 * PAD) / (size * 0.58)))
        lines = textwrap.wrap(title, chars)
        if len(lines) <= 4 or size <= 40:
            break
        size -= 4
    y = PAD + 20
    if tags:
        d.text((PAD, PAD - 20), "  ·  ".join(tags).upper(), font=ImageFont.truetype(BOLD, 24), fill=MUTED)
    for line in lines[:5]:
        d.text((PAD, y + 30), line, font=f, fill=TEXT)
        y += int(size * 1.22)
    d.rounded_rectangle([PAD - 6, H - PAD - 54, PAD + 54, H - PAD + 6], 10, fill=SURFACE)
    d.text((PAD + 6, H - PAD - 44), "AG", font=ImageFont.truetype(BOLD, 30), fill=TEXT)
    d.text((PAD + 76, H - PAD - 40), "Avinash Gosavi  ·  avinashgosavi.com", font=ImageFont.truetype(REG, 28), fill=MUTED)
    img.save(out, optimize=True)

os.makedirs("assets/og", exist_ok=True)
for path in sorted(glob.glob("_posts/*.md")):
    s = open(path).read()
    end = s.index("\n---", 4)
    fm = s[:end]
    if re.search(r"^image:", fm, re.M):
        continue
    title = re.search(r'^title:\s*"?(.*?)"?\s*$', fm, re.M).group(1).replace('\\"', '"')
    tags = re.findall(r'"([^"]+)"', (re.search(r"^tags:\s*(.*)$", fm, re.M) or [None, ""])[1])
    slug = os.path.basename(path)[11:-3]
    out = f"assets/og/{slug}.png"
    card(title, tags, out)
    s = fm + f"\nimage: /{out}" + s[end:]
    open(path, "w").write(s)
    print("wrote", out)
