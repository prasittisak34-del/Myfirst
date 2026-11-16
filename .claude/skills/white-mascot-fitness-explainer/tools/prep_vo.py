#!/usr/bin/env python3
"""Trim the start of the VO (e.g. a voice tag / extra word read aloud by ElevenLabs) and print speech islands with rough Thai ASR.
Usage: python3 tools/prep_vo.py PROJ vo.mp3 [--trim 0.85]
Writes PROJ/vo_trim.wav and PROJ/islands.txt. ASR needs sherpa-onnx + whisper model (see SETUP in HOW-TO); without it only times are printed."""
import sys, os, re, subprocess, wave
import numpy as np
P = os.path.abspath(sys.argv[1]); src = sys.argv[2]
trim = float(sys.argv[sys.argv.index('--trim') + 1]) if '--trim' in sys.argv else 0.0
os.makedirs(os.path.join(P, 'work'), exist_ok=True)
out = os.path.join(P, 'vo_trim.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(trim), '-i', src, '-af', 'afade=t=in:d=0.02', '-ar', '44100', '-ac', '1', out], check=True)
w16 = os.path.join(P, 'work', 'vo16.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-ac', '1', '-ar', '16000', w16], check=True)
log = subprocess.run(['ffmpeg', '-i', w16, '-af', 'silencedetect=n=-32dB:d=0.12', '-f', 'null', '-'], capture_output=True, text=True).stderr
ss = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]; se = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
w = wave.open(w16); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; dur = len(a) / 16000
isl = []; p = 0
for s, e in zip(ss, se):
    if s - p > 0.05: isl.append((p, s))
    p = e
if dur - p > 0.1: isl.append((p, dur))
rec = None
_d = os.environ.get('WHISPER_DIR') or next((os.path.expanduser(f'~/asr/sherpa-onnx-whisper-{n}') for n in ('small', 'turbo') if os.path.exists(os.path.expanduser(f'~/asr/sherpa-onnx-whisper-{n}/{n}-tokens.txt'))), os.path.expanduser('~/asr/sherpa-onnx-whisper-small'))
M = _d + '/' + os.path.basename(_d).rsplit('-', 1)[-1] + '-'  # starter kit ships turbo, small also works
try:
    import sherpa_onnx
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M + 'encoder.int8.onnx', decoder=M + 'decoder.int8.onnx', tokens=M + 'tokens.txt', language='th', task='transcribe')
except Exception as ex:
    print('(no ASR:', ex, ')')
lines = []
for s, e in isl:
    t = ''
    if rec:
        st = rec.create_stream(); st.accept_waveform(16000, a[int(max(0, s - .05) * 16000):int((e + .05) * 16000)]); rec.decode_stream(st); t = st.result.text
    lines.append(f'{s:7.2f} {e:7.2f}  {t}')
open(os.path.join(P, 'islands.txt'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines)); print(f'VO length {dur:.2f} s -> set END = {dur + 0.6:.1f} in episode.py')
