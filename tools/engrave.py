"""Line-engraving portrait renderer (newspaper 'hedcut' style).
Every tone is drawn as ink lines whose width follows darkness, plus contour
strokes for features, so the result is an illustration rather than a filtered photo.
"""
import numpy as np
from PIL import Image, ImageFilter, ImageOps

SS = 3  # supersampling for smooth line edges


def _blur(a, r):
    return np.asarray(Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), dtype=np.float32) / 255.0


def _portrait_mask(n):
    """Soft head-and-shoulders mask so the background drops away like a drawing on paper."""
    yy, xx = np.mgrid[0:n, 0:n] / n
    head = ((xx - 0.5) / 0.36) ** 2 + ((yy - 0.42) / 0.46) ** 2
    shoulders = ((xx - 0.5) / 0.62) ** 2 + ((yy - 1.12) / 0.42) ** 2
    d = np.minimum(head, shoulders)
    return np.clip((1.15 - d) / 0.3, 0, 1)


def engrave(gray, size=320, spacing=4.2, seed=0):
    """gray: PIL 'L' image, square. Returns PIL 'L' image of ink on paper."""
    n = size * SS
    g = ImageOps.autocontrast(gray, cutoff=2).resize((n, n), Image.LANCZOS)
    a = np.asarray(g, dtype=np.float32) / 255.0
    a = _blur(a, 1.2 * SS)
    # gentle local-contrast boost so features carry
    a = np.clip(0.5 + (a - _blur(a, 18 * SS)) * 1.6 + (_blur(a, 18 * SS) - 0.5) * 0.85, 0, 1)

    mask = _portrait_mask(n)
    tone = 1 - (1 - a) * mask            # background fades to paper
    dark = np.clip(1 - tone, 0, 1) ** 0.9

    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    s = spacing * SS

    # line field: near-horizontal lines that bend with the image (displacement from blurred tone)
    flow = _blur(a, 10 * SS) * s * 2.2
    phase = ((yy + flow + 0.25 * s * np.sin(xx / (38 * SS))) % s) / s       # 0..1 across a line period
    dist = np.abs(phase - 0.5) * 2                                          # 0 at line centre, 1 at gap
    lines1 = (dist < dark * 1.05).astype(np.float32)

    # cross-hatch only in deep shadow, at an angle
    t = np.deg2rad(-35)
    p2 = (((xx * np.cos(t) + yy * np.sin(t)) + flow * 0.5) % (s * 1.15)) / (s * 1.15)
    lines2 = ((np.abs(p2 - 0.5) * 2) < np.clip((dark - 0.55) / 0.45, 0, 1) * 0.8).astype(np.float32)

    # contour strokes from edges of a smoothed image
    e = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6 * SS)).filter(ImageFilter.FIND_EDGES), dtype=np.float32) / 255.0
    e = _blur(e, 0.8 * SS)
    contour = np.clip((e - 0.05) / 0.08, 0, 1) * mask

    ink = np.clip(np.maximum(lines1, lines2) * 0.92 + contour * 0.85, 0, 1)
    out = 1 - ink * 0.9
    out = Image.fromarray((out * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)
    o = np.asarray(out, dtype=np.float32)
    o = o * (247 / 255.0) + 0  # paper tone
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8), "L")


def pen(gray, size=320, seed=0):
    """Pen-and-ink drawing: XDoG contour lines + sparse hatching in deep shadow."""
    n = size * SS
    g = ImageOps.autocontrast(gray, cutoff=1).resize((n, n), Image.LANCZOS)
    a = np.asarray(g, dtype=np.float32) / 255.0
    a = _blur(a, 0.8 * SS)
    mask = _portrait_mask(n)
    a = 1 - (1 - a) * mask

    # XDoG (Winnemöller et al. 2012)
    sigma, k, p, eps, phi = 0.9 * SS, 1.6, 20.0, 0.19, 7.0
    g1, g2 = _blur(a, sigma), _blur(a, sigma * k)
    d = (1 + p) * g1 - p * g2
    x = np.where(d >= eps, 1.0, 1.0 + np.tanh(phi * (d - eps)))
    lines = np.clip(x, 0, 1)                       # 1 paper, 0 ink

    # hatching only where it's really dark (hair, jackets)
    tone = _blur(a, 2.5 * SS)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    s = 5.0 * SS
    t = np.deg2rad(40)
    ph = ((xx * np.cos(t) + yy * np.sin(t)) % s) / s
    h1 = (np.abs(ph - 0.5) * 2 < np.clip((0.42 - tone) / 0.3, 0, 1) * 0.55).astype(np.float32)
    t2 = np.deg2rad(-50)
    ph2 = ((xx * np.cos(t2) + yy * np.sin(t2)) % (s * 1.2)) / (s * 1.2)
    h2 = (np.abs(ph2 - 0.5) * 2 < np.clip((0.22 - tone) / 0.2, 0, 1) * 0.5).astype(np.float32)
    hatch = np.maximum(h1, h2) * mask

    out = np.minimum(lines, 1 - hatch * 0.75)
    out = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)
    o = np.asarray(out, dtype=np.float32) * (247 / 255.0)
    return Image.fromarray(np.clip(o, 0, 255).astype(np.uint8), "L")
