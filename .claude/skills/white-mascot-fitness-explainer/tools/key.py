#!/usr/bin/env python3
"""Green-screen key: PROJ/assets_raw/*.jpg|png -> PROJ/assets_key/<ID>.png (C* and R* only).
Also normalises Flow file names: 'C01_ab12cd.jpg' -> 'C01.jpg'. Usage: python3 tools/key.py PROJ [unzipped_dir ...]"""
import sys, os, re, glob, shutil
import numpy as np
from PIL import Image, ImageFilter
P = os.path.abspath(sys.argv[1]); raw = os.path.join(P, 'assets_raw'); out = os.path.join(P, 'assets_key')
os.makedirs(raw, exist_ok=True); os.makedirs(out, exist_ok=True)
for d in sys.argv[2:]:
    for f in glob.glob(os.path.join(d, '**', '*.*'), recursive=True):
        m = re.match(r'([CRB]\d{2})', os.path.basename(f))
        if m and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            Image.open(f).convert('RGB').save(os.path.join(raw, m.group(1) + '.jpg'), quality=95)
        elif f.lower().endswith(('.jpg', '.png')): print('?? not an ID name, rename it by hand:', f)
for f in sorted(glob.glob(os.path.join(raw, '*.jpg'))):
    n = os.path.basename(f)[:-4]
    if n[0] not in 'CR': continue
    a = np.asarray(Image.open(f).convert('RGB')).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]; m = np.maximum(r, b); d = g - m
    al = np.clip(1 - (d - 25) / 45, 0, 1)
    al = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255
    g2 = np.minimum(g, m + 8)
    im = Image.fromarray(np.dstack([r, g2, b, al * 255]).clip(0, 255).astype(np.uint8), 'RGBA')
    bb = im.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    im.crop(bb).save(os.path.join(out, n + '.png')); print('keyed', n)
need = [f'C{i:02d}' for i in range(1, 24)] + [f'R{i:02d}' for i in range(1, 19)] + [f'B{i:02d}' for i in range(1, 10)]
have = {os.path.basename(x)[:3] for x in glob.glob(os.path.join(raw, '*.jpg'))}
miss = [x for x in need if x not in have]
print('MISSING (template list):', ' '.join(miss) if miss else 'none')
