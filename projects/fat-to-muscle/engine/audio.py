"""SFX track from episode.py: the 2 bundled swooshes (alternated) on plate/flat changes, slide-ins and every Z emphasis zoom;
soft synth pop on box labels / prop pops / red X; low thud on big numbers. Output PROJ/work/sfx.f32 (44.1k stereo float)."""
import numpy as np, subprocess, os, sys
PROJ = os.path.abspath(os.environ.get('PROJ', '.')); sys.path.insert(0, PROJ)
from episode import SHOTS, END
E = os.path.dirname(os.path.abspath(__file__)); SR = 44100
def load(f):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(r, np.float32).reshape(-1, 2).copy(); return x / max(1e-6, np.abs(x).max())
N = int((END + 0.5) * SR); sfx = np.zeros((N, 2), np.float32)
sw = [load(os.path.join(E, 'snd', 'sw1.mp3')), load(os.path.join(E, 'snd', 'sw2.mp3'))]
def add(x, t, g):
    i = int(max(0, t) * SR); n = min(len(x), N - i)
    if n > 0: sfx[i:i + n] += x[:n] * g
tt = np.arange(int(0.12 * SR)) / SR
pop = (np.sin(2 * np.pi * (700 - 1800 * tt) * tt) * np.exp(-tt * 38)).astype(np.float32); pop = np.stack([pop, pop], 1)
t2 = np.arange(int(0.25 * SR)) / SR
thud = (np.sin(2 * np.pi * (120 - 150 * t2) * t2) * np.exp(-t2 * 16)).astype(np.float32); thud = np.stack([thud, thud], 1)
k = 0; prev = None
for s in SHOTS:
    t0 = s['t']; kind = 'plate' if s['bg'].startswith('B') else 'flat'
    trw = kind == 'plate' or prev == 'plate' or s['bg'] == 'split'
    if trw: add(sw[k % 2], t0 - 0.12, 0.55); k += 1
    prev = kind
    for (at, mult) in s.get('Z', []):
        if at > 0.15 or not trw: add(sw[k % 2], t0 + at - 0.06, 0.42); k += 1
    for L in s.get('L', []):
        o = L[4] if len(L) > 4 else {}
        if o.get('in') in ('slideL', 'slideR') and o.get('at', 0) > 0: add(sw[k % 2], t0 + o['at'] - 0.05, 0.5); k += 1
        if o.get('in') == 'pop': add(pop, t0 + o.get('at', 0), 0.35)
    for T in s.get('T', []):
        if T[1] == 'box': add(pop, t0 + T[4], 0.28)
        if T[1] == 'num': add(thud, t0 + T[4], 0.6)
    for X in s.get('X', []): add(pop, t0 + X[3], 0.4)
os.makedirs(os.path.join(PROJ, 'work'), exist_ok=True)
sfx.astype(np.float32).tofile(os.path.join(PROJ, 'work', 'sfx.f32'))
# build kbkenj0zqj
