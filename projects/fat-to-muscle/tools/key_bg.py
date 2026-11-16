#!/usr/bin/env python3
"""Green-screen key that removes only the BACKGROUND green (colour measured from the image border),
so green parts of the subject (leaves, broccoli) stay. Usage: python3 key_bg.py PROJ"""
import sys, os, glob
import numpy as np
from PIL import Image, ImageFilter
P = os.path.abspath(sys.argv[1]); raw = os.path.join(P, 'assets_raw'); out = os.path.join(P, 'assets_key')
os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(os.path.join(raw, '*.jpg'))):
    n = os.path.basename(f)[:-4]
    if n[0] not in 'CR': continue
    a = np.asarray(Image.open(f).convert('RGB')).astype(np.float32)
    border = np.concatenate([a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3), a[:, :8].reshape(-1, 3), a[:, -8:].reshape(-1, 3)])
    bg = np.median(border, 0)
    dist = np.sqrt(((a - bg) ** 2).sum(-1))
    al = np.clip((dist - 40) / 45, 0, 1)
    al = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # spill: pull green down only on semi-transparent edge pixels
    edge = al < 0.98
    g2 = np.where(edge, np.minimum(g, np.maximum(r, b) + 8), g)
    im = Image.fromarray(np.dstack([r, g2, b, al * 255]).clip(0, 255).astype(np.uint8), 'RGBA')
    bb = im.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    im.crop(bb).save(os.path.join(out, n + '.png')); print('keyed', n, 'bg', bg.astype(int))
