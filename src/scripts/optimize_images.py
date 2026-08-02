"""Optimize downloaded images for web (resize + recompress via Pillow)."""
import os
from PIL import Image

BASE = r"C:\Users\Admin\Desktop\Projetos\bruno-vinicius-interiores"
DIR = os.path.join(BASE, "src", "assets", "img")

SIZES = {
    "hero.jpg": 2000,
    "og.jpg": 1200,
    "project-*.jpg": 1400,
    "detalhe-*.jpg": 900,
    "blog-*.jpg": 1200,
    "studio-1.jpg": 1200,
}

def target_max(fname):
    for pat, mx in SIZES.items():
        if glob_match(pat, fname):
            return mx
    return 1600

def glob_match(pat, name):
    if "*" not in pat:
        return pat == name
    prefix, suffix = pat.split("*", 1)
    return name.startswith(prefix) and name.endswith(suffix)

for fname in os.listdir(DIR):
    if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
        continue
    path = os.path.join(DIR, fname)
    try:
        im = Image.open(path)
        im = im.convert("RGB")
        maxw = target_max(fname)
        if im.width > maxw:
            h = int(im.height * maxw / im.width)
            im = im.resize((maxw, h), Image.LANCZOS)
        if fname == "og.jpg":
            # OG standard ratio 1200x630 (crop)
            im = Image.open(path).convert("RGB")
            w, h = im.size
            target_ratio = 1200 / 630
            ratio = w / h
            if ratio > target_ratio:
                new_w = int(h * target_ratio)
                x = (w - new_w) // 2
                im = im.crop((x, 0, x + new_w, h))
            else:
                new_h = int(w / target_ratio)
                y = (h - new_h) // 2
                im = im.crop((0, y, w, y + new_h))
            im = im.resize((1200, 630), Image.LANCZOS)
            im.save(path, "JPEG", quality=80, optimize=True, progressive=True)
        else:
            im.save(path, "JPEG", quality=76, optimize=True, progressive=True)
        print(f"{fname}: {im.size} ok")
    except Exception as e:
        print(f"{fname}: ERROR {e}")

print("DONE")
