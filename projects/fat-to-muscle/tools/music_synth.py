#!/usr/bin/env python3
"""Self-made royalty-free music bed: soft synth pads (Am-F-C-G, 92 bpm) + muted pluck arpeggio + light pulse.
music_bed(seconds, sr) -> float32 mono, peak ~0.5. Deterministic (same output every run)."""
import numpy as np
def _note(m): return 440.0 * 2 ** ((m - 69) / 12)
def music_bed(sec, sr=48000, bpm=92):
    n = int(sec * sr); out = np.zeros(n + sr, np.float32); beat = 60 / bpm; bar = 4 * beat
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
    rng = np.random.RandomState(7)
    for b in range(int(sec / bar) + 2):
        ch = chords[b % 4]; i0 = int(b * bar * sr); L = int(bar * sr * 1.15); tt = np.arange(L) / sr
        if i0 >= len(out): break
        env = np.minimum(1, tt / .8) * np.minimum(1, (L / sr - tt) / .6)
        pad = sum(np.sin(2 * np.pi * _note(m) * tt + d) + .3 * np.sin(2 * np.pi * _note(m) * 1.003 * tt) for m, d in zip(ch, rng.rand(3) * 6))
        bass = .6 * np.sin(2 * np.pi * _note(ch[0] - 12) * tt)
        seg = (pad * .18 + bass * .25) * env
        for s in range(8):  # muted pluck arpeggio on 8ths
            j = int(s * beat / 2 * sr); m = ch[s % 3] + 12; pl = np.arange(int(.35 * sr)) / sr
            seg[j:j + len(pl)] += .12 * np.sin(2 * np.pi * _note(m) * pl) * np.exp(-pl * 9)
        for s in range(4):  # soft pulse on beats
            j = int(s * beat * sr); pl = np.arange(int(.18 * sr)) / sr
            seg[j:j + len(pl)] += .18 * np.sin(2 * np.pi * (60 * np.exp(-pl * 20) + 45) * pl) * np.exp(-pl * 22)
        e = min(len(out), i0 + L); out[i0:e] += seg[:e - i0]
    out = out[:n]; return (out / (np.abs(out).max() + 1e-9) * .5).astype(np.float32)
