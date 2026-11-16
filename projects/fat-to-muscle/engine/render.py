import sys, math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.environ.get('PROJ', '.'))
sys.path.insert(0, PROJ)
from episode import SHOTS, END, FLAT, FLAT2
FONT = {k: os.path.join(HERE, 'fonts', v) for k, v in
        dict(big='Kanit-LightItalic.ttf', bold='Kanit-Bold.ttf', box='Kanit-Medium.ttf',
             center='Kanit-SemiBoldItalic.ttf', num='Kanit-Bold.ttf').items()}
_fc = {}
def font(style, size):
    k = (style, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONT[style], size, layout_engine=ImageFont.Layout.RAQM)
    return _fc[k]

def ease(p): p = min(1, max(0, p)); return 1 - (1 - p) ** 3
def lerp(a, b, p): return a + (b - a) * p

# ---------- assets ----------
_assets = {}
def asset(name):
    if name in _assets: return _assets[name]
    if name.startswith('B'):
        im = Image.open(os.path.join(PROJ, 'assets_raw', name + '.jpg')).convert('RGB')
        im = im.resize((W, int(W * im.size[1] / im.size[0])), Image.LANCZOS)
        _assets[name] = im; return im
    im = Image.open(os.path.join(PROJ, 'assets_key', name + '.png')).convert('RGBA')
    pad = 40
    big = Image.new('RGBA', (im.size[0] + 2 * pad, im.size[1] + 2 * pad), (0, 0, 0, 0)); big.paste(im, (pad, pad))
    a = big.getchannel('A')
    if name.startswith('R'):  # sticker white outline for props
        o = a.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(1))
        st = Image.new('RGBA', big.size, (255, 255, 255, 0)); st.putalpha(o)
        st.alpha_composite(big); big = st; a = big.getchannel('A')
    sh = Image.new('RGBA', big.size, (10, 25, 35, 0))
    sh.putalpha(a.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.42)))
    _assets[name] = (big, sh, pad)
    return _assets[name]

def place(canvas, name, cx, by, h, alpha=1.0, scale=1.0, flip=False, shadow=True, rot=0):
    """cx,by: bottom-centre in px; h: target visible height px"""
    big, sh, pad = asset(name)
    vis_h = big.size[1] - 2 * pad
    k = h * scale / vis_h
    if k <= 0.01 or alpha <= 0.01: return
    sz = (max(1, int(big.size[0] * k)), max(1, int(big.size[1] * k)))
    im = big.resize(sz, Image.BILINEAR)
    s2 = sh.resize(sz, Image.BILINEAR) if shadow else None
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if s2: s2 = s2.transpose(Image.FLIP_LEFT_RIGHT)
    if rot:
        im = im.rotate(rot, Image.BICUBIC, expand=True)
        if s2: s2 = s2.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1:
        im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
        if s2: s2.putalpha(s2.getchannel('A').point(lambda v: int(v * alpha)))
    x = int(cx - im.size[0] / 2); y = int(by - im.size[1] + pad * k)
    if s2: canvas.alpha_composite_safe(s2, (x + int(14 * k * 3), y + int(10 * k * 3)))
    canvas.alpha_composite_safe(im, (x, y))

class Canvas:
    def __init__(self, base): self.im = base.convert('RGBA')
    def alpha_composite_safe(self, im, xy):
        x, y = xy
        x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + im.size[0]), min(H, y + im.size[1])
        if x1 <= x0 or y1 <= y0: return
        self.im.alpha_composite(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))

# ---------- backgrounds ----------
_flat = {}
def flat_bg(color, split=None):
    k = (color, split)
    if k in _flat: return _flat[k]
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.85)) ** 2)
    v = (1.06 - 0.28 * np.clip(r, 0, 1.2))[..., None]
    c = np.array(color, np.float32)[None, None, :]
    img = c * v
    if split:
        c2 = np.array(split, np.float32)[None, None, :]
        img = np.where((xx >= W // 2)[..., None], c2 * v, img)
    noise = np.random.default_rng(1).normal(0, 2.2, (H, W, 1))
    im = Image.fromarray(np.clip(img + noise, 0, 255).astype(np.uint8), 'RGB')
    _flat[k] = im; return im

def plate(name, z, fx, fy, dx=0):
    src = asset(name)
    # src is W x h (cover by height if needed)
    s = max(1.0, H / src.size[1])
    sw, shh = src.size[0] * s, src.size[1] * s
    # screen = f + (srcpos*s - f)*z ; inverse for transform
    Fx, Fy = fx * W, fy * H
    a = 1 / (s * z)
    # src_x = ((X - Fx)/z + Fx - offx)/s
    offx = (W - sw) / 2 + dx; offy = (H - shh) / 2
    return src.transform((W, H), Image.AFFINE,
                         (a, 0, (-Fx / z + Fx - offx) / s, 0, a, (-Fy / z + Fy - offy) / s), Image.BILINEAR)

# ---------- text ----------
def draw_text(c, txt, style, x, y, p, anchor='mm', size=None, color=(255, 255, 255)):
    if p <= 0: return
    a = ease(p / 0.22) if p < 0.22 else 1
    dy = (1 - a) * 18
    if style == 'box':
        f = font('box', size or 56)
        bb = f.getbbox(txt, anchor='mm')
        pw, ph = bb[2] - bb[0] + 60, int((size or 56) * 1.5)
        sc = 0.7 + 0.3 * ease(p / 0.18) + (0.05 * math.sin(min(1, p / 0.3) * math.pi))
        lay = Image.new('RGBA', (pw + 30, ph + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((15 + 6, 15 + 7, 15 + pw + 6, 15 + ph + 7), 10, fill=(0, 0, 0, 80))
        lay = lay.filter(ImageFilter.GaussianBlur(4)); d = ImageDraw.Draw(lay)
        d.rounded_rectangle((15, 15, 15 + pw, 15 + ph), 10, fill=(255, 255, 255, 255), outline=(40, 40, 40, 255), width=4)
        d.text((15 + pw / 2, 15 + ph / 2 + 2), txt, font=f, fill=(30, 30, 30), anchor='mm')
        lay = lay.resize((max(1, int(lay.size[0] * sc)), max(1, int(lay.size[1] * sc))), Image.BILINEAR)
        if a < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * a)))
        c.alpha_composite_safe(lay, (int(x - lay.size[0] / 2), int(y - lay.size[1] / 2)))
        return
    sizes = dict(big=104, bold=58, center=96, num=230)
    f = font(style, size or sizes[style])
    lines = txt.split('\n')
    lh = int((size or sizes[style]) * 1.2)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    for i, ln in enumerate(lines):
        yy = y + (i - (len(lines) - 1) / 2) * lh + dy
        if sum(color) > 300: ds.text((x + 4, yy + 5), ln, font=f, fill=(0, 20, 30, 150), anchor=anchor)
        d.text((x, yy), ln, font=f, fill=color + (255,), anchor=anchor)
    sh = sh.filter(ImageFilter.GaussianBlur(5 if style != 'num' else 9))
    sh.alpha_composite(lay)
    if a < 1: sh.putalpha(sh.getchannel('A').point(lambda v: int(v * a)))
    c.im.alpha_composite(sh)

def red_x(c, x, y, s, p):
    if p <= 0: return
    a = ease(p / 0.2)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    r = s * (0.6 + 0.4 * a)
    for (x0, y0, x1, y1) in ((x - r, y - r, x + r, y + r), (x - r, y + r, x + r, y - r)):
        d.line((x0 + 6, y0 + 8, x1 + 6, y1 + 8), fill=(0, 0, 0, 90), width=int(s * 0.28))
        d.line((x0, y0, x1, y1), fill=(226, 59, 59, 255), width=int(s * 0.25))
    c.im.alpha_composite(lay)

# ---------- v2: sub-pixel layer engine ----------
def eio(p): p = min(1, max(0, p)); return 0.5 - 0.5 * math.cos(math.pi * p)          # ease in-out sine
def eio3(p): p = min(1, max(0, p)); return 4*p**3 if p < .5 else 1 - (-2*p + 2)**3 / 2

def M_T(x, y): return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]], float)
def M_S(s): return np.array([[s, 0, 0], [0, s, 0], [0, 0, 1]], float)
def M_R(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]], float)

def warp(im, M, mode=Image.BICUBIC):
    inv = np.linalg.inv(M)
    return im.transform((W, H), Image.AFFINE, tuple(inv[0]) + tuple(inv[1]), mode)

_layer = {}
def layer_img(name, x, by, h, flip=False, shadow=True):
    """full-frame RGBA with the sticker placed statically at world position; returns (img, pivot)"""
    k = (name, round(x, 4), round(by, 4), round(h, 4), flip, shadow)
    if k in _layer: return _layer[k]
    big, sh, pad = asset(name)
    vis_h = big.size[1] - 2 * pad
    kk = h * H / vis_h
    sz = (max(1, int(round(big.size[0] * kk))), max(1, int(round(big.size[1] * kk))))
    im = big.resize(sz, Image.LANCZOS); s2 = sh.resize(sz, Image.LANCZOS)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT); s2 = s2.transpose(Image.FLIP_LEFT_RIGHT)
    cx, byp = x * W, by * H
    px, py = int(round(cx - sz[0] / 2)), int(round(byp - sz[1] + pad * kk))
    full = Canvas(Image.new('RGBA', (W, H), (0, 0, 0, 0)))
    full.im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if shadow: full.alpha_composite_safe(s2, (px + int(42 * kk), py + int(30 * kk)))
    full.alpha_composite_safe(im, (px, py))
    res = (full.im, (cx, byp - h * H * 0.5))
    _layer[k] = res
    return res

def with_alpha(im, a):
    if a >= 0.999: return im
    im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a))); return im

def cam_z(s, lt, dur):
    base0, base1 = s.get('cam', (1.0, 1.06 if s['bg'].startswith('B') else 1.03, 0.5, 0.55))[:2]
    z = lerp(base0, base1, eio(lt / max(dur, 0.01)))
    for (at, mult) in s.get('Z', []):
        z *= lerp(1, mult, eio3((lt - at) / 0.5))
    return z

def render_shot(s, lt, dur):
    cam = s.get('cam', (1.0, 1.06, 0.5, 0.55))
    fx, fy = cam[2] * W, cam[3] * H
    z = cam_z(s, lt, dur)
    plate_shot = s['bg'].startswith('B')
    zf = z ** s.get('par', 1.35) if plate_shot else z
    camM = M_T(fx, fy) @ M_S(z) @ M_T(-fx, -fy)
    camF = M_T(fx, fy) @ M_S(zf) @ M_T(-fx, -fy)
    if plate_shot:
        src = asset(s['bg'])
        sc = max(W / src.size[0], H / src.size[1])
        P = M_T(W / 2, H / 2) @ M_S(sc) @ M_T(-src.size[0] / 2, -src.size[1] / 2)
        base = warp(src, camM @ P, Image.BICUBIC)
    else:
        base = warp(flat_bg(FLAT, FLAT2 if s['bg'] == 'split' else None), camM, Image.BILINEAR)
    out = base.convert('RGBA')
    # static (settled) layers composite, cached per shot+state
    settled = []; anim = []
    for i, L in enumerate(s.get('L', [])):
        o = L[4] if len(L) > 4 else {}
        q = lt - o.get('at', 0)
        if q < 0 or lt > o.get('out', 99): continue
        ent = o.get('in', 'fade'); edur = {'fade': 0.3, 'slideL': 0.55, 'slideR': 0.55, 'pop': 0.35}.get(ent, 0.3)
        if q < edur or o.get('sway') or o.get('move') or o.get('scale'): anim.append((L, o, q, ent, edur))
        else: settled.append(i)
    if settled:
        key = (id(s), tuple(settled))
        if key not in _layer:
            comp = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            for i in settled:
                L = s['L'][i]; o = L[4] if len(L) > 4 else {}
                comp.alpha_composite(layer_img(L[0], L[1], L[2], L[3], o.get('flip', False), o.get('shadow', True))[0])
            _layer[key] = comp
        out.alpha_composite(warp(_layer[key], camF))
    for (L, o, q, ent, edur) in anim:
        img, (px, py) = layer_img(L[0], L[1], L[2], L[3], o.get('flip', False), o.get('shadow', True))
        loc = np.eye(3); a = 1.0
        if o.get('sway'):
            rot = o['sway'] * math.sin(2 * math.pi * (lt + o.get('at', 0)) / 2.6)
            bx, byy = L[1] * W, L[2] * H
            loc = M_T(bx, byy) @ M_R(rot) @ M_T(-bx, -byy)
        if o.get('scale'):   # (s0, s1, t0, t1) eased scale about the sticker centre, times relative to shot
            s0, s1, t0, t1 = o['scale']; sc = lerp(s0, s1, eio((lt - t0) / max(t1 - t0, 0.01)))
            loc = M_T(px, py) @ M_S(sc) @ M_T(-px, -py) @ loc
        if o.get('move'):    # (dx, dy, t0, t1) eased translation in screen fractions
            dx, dy, t0, t1 = o['move']; mp = eio((lt - t0) / max(t1 - t0, 0.01))
            loc = M_T(dx * W * mp, dy * H * mp) @ loc
        if o.get('fadeout'): # (t0, t1) fade the layer out
            f0, f1 = o['fadeout']; a = a * (1 - eio((lt - f0) / max(f1 - f0, 0.01)))
        if ent == 'fade' and q < edur:
            p = eio(q / edur); a = p
            gh = M_T((1 - p) * 70 * o.get('dir', 1), 0)
            out.alpha_composite(warp(with_alpha(img, 0.35 * (1 - p)), camF @ gh @ loc))
        elif ent in ('slideL', 'slideR') and q < edur:
            sgn = -1 if ent == 'slideL' else 1
            for g in (3, 2, 1):
                gp = eio3(max(0, q - 0.04 * g) / edur)
                out.alpha_composite(warp(with_alpha(img, 0.16 * g / 3 * (1 - q / edur)), camF @ M_T(sgn * W * 0.6 * (1 - gp), 0) @ loc))
            p = eio3(q / edur); loc = M_T(sgn * W * 0.6 * (1 - p), 0) @ loc
        elif ent == 'pop' and q < edur:
            p = q / edur
            sc = max(0.01, eio(p) * (1 + 0.1 * math.sin(p * math.pi))); a = min(1, q / 0.12)
            loc = M_T(px, py) @ M_S(sc) @ M_T(-px, -py) @ loc
        out.alpha_composite(warp(with_alpha(img, a), camF @ loc))
    c = Canvas(out); c.im = out
    for T in s.get('T', []):
        txt, style, x, y, at = T[:5]
        o = T[5] if len(T) > 5 else {}
        draw_text(c, txt, style, x * W, y * H, lt - at, anchor=o.get('anchor', 'mm'), size=o.get('size'),
                  color=o.get('color', s.get('tc', (255, 255, 255))))
    for X_ in s.get('X', []):
        red_x(c, X_[0] * W, X_[1] * H, X_[2], lt - X_[3])
    return c.im.convert('RGB')

def shot_idx(t):
    for i in range(len(SHOTS) - 1, -1, -1):
        if t >= SHOTS[i]['t']: return i
    return 0

DIS = 0.35
def render(t):
    i = shot_idx(t); s = SHOTS[i]
    t1 = SHOTS[i + 1]['t'] if i + 1 < len(SHOTS) else END
    lt = t - s['t']
    out = render_shot(s, lt, t1 - s['t'])
    prev = SHOTS[i - 1] if i > 0 else None
    tr = s.get('tr', 'dis' if prev and (s['bg'].startswith('B') or prev['bg'].startswith('B')) else 'cut')
    if prev and tr == 'dis' and lt < DIS:
        pd = s['t'] - prev['t']
        po = render_shot(prev, pd + lt, pd)
        p = eio(lt / DIS)
        if not s['bg'].startswith('B'):   # plate -> flat: wash previous toward flat colour
            po = Image.blend(po, Image.new('RGB', (W, H), FLAT), 0.55 * p)
        out = Image.blend(po, out, p)
    if t > END - 0.9:
        out = Image.blend(Image.new('RGB', (W, H)), out, max(0, (END - t) / 0.9))
    return out

OUTDIR = os.environ.get('OUTDIR', os.path.join(PROJ, 'work', 'stills'))
if __name__ == '__main__':
    if sys.argv[1] == 'still':
        for tt in sys.argv[2:]:
            render(float(tt)).save(OUTDIR + '/s_%06.2f.jpg' % float(tt), quality=88)
        sys.exit()
    i, n = int(sys.argv[1]), int(sys.argv[2])
    N = int(END * FPS)
    a, b = N * i // n, N * (i + 1) // n
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', os.path.join(PROJ, 'work', 'parts', f'p{i:02d}.mp4')], stdin=subprocess.PIPE)
    for f in range(a, b):
        p.stdin.write(render(f / FPS).tobytes())
    p.stdin.close(); p.wait()
