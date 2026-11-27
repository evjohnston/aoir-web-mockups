"""Crop AoIR-published committee headshots into square portrait photos.
Input:  _photos/<slug>.img   (not committed; downloaded from aoir.org)
Output: assets/committee/<slug>.jpg  and  assets/committee/initials-<slug>.jpg for people without a photo.
Run from the repo root:  python3 tools/sketch_portraits.py
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_photos")
OUT = os.path.join(ROOT, "assets", "committee")
SIZE = 320
PAPER = 248  # near-white paper tone

# square crop boxes (x0, y0, side) as fractions of image width/height for off-centre photos
CROPS = {
    "annette-markham": (0.28, 0.17, 0.62),   # side as fraction of height
    "adrienne-massanari": (0.10, 0.0, 0.90),
    "crystal-abidin": (0.11, 0.01, 0.88),
    "jack-qiu": (0.0, 0.0, 1.0),
    "elizabeth-buchanan": (0.0, 0.0, 1.0),
    "heidi-campbell": (0.27, 0.0, 0.7),
    "kate-oriordan": (0.29, 0.0, 0.6),
    "matthew-allen": (0.26, 0.0, 0.6),
    "caroline-haythornthwaite": (0.10, 0.12, 0.7),
    "steve-jones": (0.15, 0.08, 0.7),
    "jang-hyun-kim": (0.0, 0.0, 0.85),
    "matt-williams": (0.25, 0.0, 0.75),
    "radhika-gajjala": (0.29, 0.0, 0.75),
    "sean-cubitt": (0.25, 0.06, 0.5),
    "soraj-hongladarom": (0.38, 0.21, 0.42),
    "sun-sun-lim": (0.43, 0.0, 0.5),
    "wes-shrum": (0.22, 0.0, 0.6),
    "axel-bruns": (0.28, 0.0, 0.95),
}


def crop_square(im, slug):
    w, h = im.size
    if slug in CROPS:
        fx, fy, fs = CROPS[slug]
        side = int(fs * min(w, h)) if slug != "annette-markham" and slug != "axel-bruns" else int(fs * h)
        x0, y0 = int(fx * w), int(fy * h)
    else:
        side = min(w, h)
        x0 = (w - side) // 2
        y0 = int((h - side) * 0.25)
    return im.crop((x0, y0, x0 + side, y0 + side))


def hatch(n, angle, spacing):
    yy, xx = np.mgrid[0:n, 0:n]
    t = np.deg2rad(angle)
    d = (xx * np.cos(t) + yy * np.sin(t)) % spacing
    return (d < 1.2).astype(np.float32)


def paper(n, seed):
    rng = np.random.default_rng(seed)
    g = rng.normal(0, 1, (n // 2, n // 2)).astype(np.float32)
    g = np.asarray(Image.fromarray(((g * 18) + 128).clip(0, 255).astype(np.uint8)).resize((n, n), Image.BICUBIC), dtype=np.float32)
    return (g - 128) / 128.0


def vignette(n):
    yy, xx = np.mgrid[0:n, 0:n]
    r = np.sqrt((xx - n / 2) ** 2 + (yy - n * 0.46) ** 2) / (n / 2)
    return np.clip((r - 0.72) / 0.28, 0, 1)  # 0 centre -> 1 edge


def sketch_filter_old(slug):
    im = Image.open(os.path.join(SRC, slug + ".img"))
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, "white")
        im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    im = crop_square(im.convert("RGB"), slug).resize((SIZE, SIZE), Image.LANCZOS)
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    ga = np.asarray(g, dtype=np.float32)

    # pencil lines: colour dodge of the inverted, blurred image
    inv = ImageOps.invert(g).filter(ImageFilter.GaussianBlur(SIZE / 28))
    ia = np.asarray(inv, dtype=np.float32)
    lines = np.clip(ga * 255.0 / np.maximum(1, 255 - ia), 0, 255) / 255.0
    lines = np.asarray(Image.fromarray((lines * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), dtype=np.float32) / 255.0
    lines = lines ** 1.45                     # strengthen strokes, keep them light

    # tone -> cross-hatching
    tone = np.asarray(g.filter(ImageFilter.GaussianBlur(3)), dtype=np.float32) / 255.0
    dark = 1 - tone
    h1, h2, h3 = hatch(SIZE, 45, 5.0), hatch(SIZE, -45, 5.5), hatch(SIZE, 20, 4.2)
    shade = 1 - 0.30 * h1 * np.clip((dark - 0.38) / 0.4, 0, 1) \
              - 0.24 * h2 * np.clip((dark - 0.56) / 0.35, 0, 1) \
              - 0.20 * h3 * np.clip((dark - 0.74) / 0.3, 0, 1)
    soft = 1 - 0.22 * np.clip(dark - 0.25, 0, 1)   # graphite smudge under the hatching

    out = lines * shade * soft
    out = out + paper(SIZE, hash(slug) % 2**32) * 0.02
    v = vignette(SIZE)
    out = out * (1 - v) + 1.0 * v                 # fade edges to paper
    out = np.clip(out * (PAPER / 255.0) + (1 - PAPER / 255.0) * v * 0, 0, 1)
    Image.fromarray((out * 255).astype(np.uint8), "L").save(os.path.join(OUT, slug + ".jpg"), quality=86)


def sketch(slug):
    """Plain square-cropped photo of the published headshot."""
    im = Image.open(os.path.join(SRC, slug + ".img"))
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[-1]); im = bg
    im = crop_square(im.convert("RGB"), slug).resize((SIZE, SIZE), Image.LANCZOS)
    im.save(os.path.join(OUT, slug + ".jpg"), quality=86)


def initials_card(slug, name):
    n = SIZE
    img = Image.new("L", (n, n), PAPER)
    d = ImageDraw.Draw(img)
    # head-and-shoulders outline in pencil
    for k in range(3):
        o = k * 1.3
        d.ellipse((n * 0.33 + o, n * 0.14 + o, n * 0.67 - o, n * 0.56 - o), outline=150 - k * 20, width=1)
        d.arc((n * 0.12 + o, n * 0.58 + o, n * 0.88 - o, n * 1.32 - o), 180, 360, fill=150 - k * 20, width=1)
    a = np.asarray(img, dtype=np.float32) / 255.0
    yy, xx = np.mgrid[0:n, 0:n]
    head = ((xx - n * 0.5) / (n * 0.17)) ** 2 + ((yy - n * 0.35) / (n * 0.21)) ** 2 < 1
    body = (((xx - n * 0.5) / (n * 0.38)) ** 2 + ((yy - n * 0.95) / (n * 0.37)) ** 2 < 1) & (yy > n * 0.6)
    mask = (head | body).astype(np.float32)
    a = a * (1 - 0.18 * hatch(n, 45, 6.0) * mask)
    a = a + paper(n, hash(slug) % 2**32) * 0.03
    v = vignette(n)
    a = a * (1 - v) + (PAPER / 255.0) * v
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "L")
    d = ImageDraw.Draw(img)
    ini = "".join(p[0] for p in name.replace("-", " ").split() if p[0].isalpha())[:3].upper()
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", 64)
    except Exception:
        f = ImageFont.load_default()
    bb = d.textbbox((0, 0), ini, font=f)
    d.text(((n - (bb[2] - bb[0])) / 2, n * 0.27), ini, fill=70, font=f)
    img.save(os.path.join(OUT, "initials-" + slug + ".jpg"), quality=86)


def main():
    os.makedirs(OUT, exist_ok=True)
    sys.path.insert(0, os.path.dirname(__file__))
    from committees_data import PEOPLE
    made = 0
    for slug, name in PEOPLE.items():
        if os.path.exists(os.path.join(SRC, slug + ".img")):
            sketch(slug); made += 1
        else:
            initials_card(slug, name)
    print(f"{made} sketches, {len(PEOPLE) - made} initials cards")


if __name__ == "__main__":
    main()
