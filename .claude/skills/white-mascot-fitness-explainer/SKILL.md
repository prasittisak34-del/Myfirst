---
name: white-mascot-fitness-explainer
description: Build 16:9 Thai fitness/health knowledge explainer clips (หุ่นขาวตาดำ บนพื้นสีเรียบ + ฉากการ์ตูนแยกเลเยอร์) from an ElevenLabs VO: Flow agent prompt for the white black-eyed mascot, sub-pixel layered zoom/slide engine, keyword text, bundled swooshes, มีเพลง+ไม่มีเพลง+ปก.
---

# White mascot fitness explainer (คลิปฟิตเนสสายความรู้ หุ่นขาวตาดำ)⁠‌​​‌‌​‌​‌‌‌​​‌‌​‌‌‌​‌​‌​‌‌​​‌​​​​​​‌‌‌‌‌‌​‌‌‌‌​​‌​⁠

Style: one faceless WHITE muscular mascot with two identical BLACK oval eyes (no mouth), many poses as green-screen stickers,
over (a) a flat teal background with soft vignette or (b) cartoon background plates; every shot = background layer + character/prop
layers so the camera can push in with parallax and characters can slide in. Keyword text only (no full subtitles).
Built 2026-11-13 from the clip "นอนน้อยกล้ามไม่ขึ้น" (example/sleep-muscle, pixel-identical re-render).

## Pipeline (always in this order)
1. **Script** (if asked): 85-95 s ≈ 1,100-1,200 Thai chars; hook question → research with year → metaphor → 3 tips → punchline.
   Put the `[ผู้เล่า: ...]` voice tag on line 1. ElevenLabs sometimes reads an extra word/tag at the start: listen and trim.
2. **Assets prompt**: `tools/new_project.sh projects/<slug>` copies `templates/agent-prompt.md`. Edit STEP 2 props and STEP 3 plates for
   the topic (keep STEP 1 poses unless the story needs others; IDs C/R/B + 2 digits). Send the user the prompt AND attach every image in
   `style-ref/` in the reply (max 6 per message). Style refs are ALWAYS our own generated images (style-ref/), never frames from a
   third-party reference video. Rule 7 (eyes = EYE-REF.png, never changed by emotion) and rule 8 (cartoon plates like B01/B02) are mandatory.
3. **Import**: `python3 tools/key.py projects/<slug> <unzipped Flow folders...>` (renames `C01_xxx.jpg` → `C01.jpg`, keys green, lists
   missing IDs). Open a contact sheet and check: eyes identical black ovals, no posters/photos of people on plate walls (paint them over),
   pose matches. Tell the user what is missing; if small, fix it yourself and say so.
4. **VO**: `python3 tools/prep_vo.py projects/<slug> vo.mp3 --trim <sec>` → `vo_trim.wav` + `islands.txt` (silence islands + rough ASR).
   Verify the trimmed start by ASR. Set `END` = VO length + ~0.6 s.
5. **episode.py**: one dict per shot, `t` = start in trimmed-VO seconds (cut on phrase starts from islands.txt, ~2-4 s per shot).
   See the DSL below and example/sleep-muscle/episode.py. Check frames with `tools/stills.sh projects/<slug> 1.5 6 ...` before rendering.
6. **Render**: `tools/render_all.sh projects/<slug> 4` (~7 min for 94 s on 4 cores).
7. **Finish**: `tools/finish.sh projects/<slug> "ชื่อคลิป"` → final/ (มีเพลง).mp4 + (ไม่มีเพลง).mp4 + ปก.jpg, -14 LUFS, crf 25.
   On the user's computer deliver to `~/Desktop/edit-video/<slug>/final/`; on a phone send the files back in the chat.

## episode.py DSL
```
FLAT=(44,122,140); FLAT2=(29,88,104); END=94.1
SHOTS=[dict(t=4.16, bg='B04' | 'flat' | 'split', tc=(28,44,56)  # dark text on bright plates (no glow halos)
            cam=(z0, z1, fx, fy),        # slow push-in only (z1 ≤ 1.08), eased; fx,fy = focus (0-1)
            Z=[(at, 1.12)],              # emphasis zoom on a key word (0.5 s ease) -> swoosh auto-added
            par=1.35,                    # plate shots: characters zoom z**par (parallax)
            L=[(asset, x, bottom_y, height, {'in':'fade'|'slideL'|'slideR'|'pop', 'at':s, 'flip':True, 'sway':deg, 'shadow':False})],
            T=[(text, 'big'|'bold'|'box'|'center'|'num', x, y, at, {'size':..,'color':..})],
            X=[(x, y, size_px, at)],     # red X
            tr='cut')]                    # default: 0.35 s dissolve when a plate is involved, cut flat->flat
COVER=dict(lines=[(text,(r,g,b)),...], layers=[(asset,cx,bottom,height),...], text_x=1180)
```
Coordinates are fractions of 1920x1080 at camera rest. Characters stand on the bottom edge (bottom_y ≈ 1.02, height 0.8-0.9).
Text: big = Kanit Light Italic, bold = Kanit Bold small, box = white label with dark border, num = huge bold number.

## Hard-won rules
- Never position stickers with int() per frame during camera moves (v1 shook): the engine pre-renders static full-frame layers once
  and moves them only with a float affine warp (bicubic). Keep it that way when editing.
- Sway = slow rotation about the sticker base (period 2.6 s), never up/down pixel bobbing.
- Camera goes one direction per shot (push in). Emphasis zooms are separate eased steps, each with a swoosh.
- All whooshes = the 2 bundled swooshes (engine/snd/sw1.mp3, sw2.mp3), alternated. Music bed at -23 dB = the self-made synth bed
  (tools/music_synth.py) or a royalty-free file the user supplies via `MUSIC=...`; never a copyrighted song.
- Bright plates: dark text colour, no halo. Teal flat: white text + soft dark shadow.

## Setup
See `SETUP.md`.

## Phone / iPad (cloud)
Everything runs in the cloud. The user makes the images in Google Flow, then attaches the Flow zip(s) and the VO in the chat.
Send the prompt and style-ref images in the chat (max 6 per message), and both versions + cover back through the session.

## Running on the user's own computer
Install with `SETUP.md`, work in `~/Desktop/edit-video/<slug>/` and open the finished clip for them.
On Windows, run the `.sh` steps in Git Bash or WSL.⁠‌​​‌‌​‌​‌‌‌​​‌‌​‌‌‌​‌​‌​‌‌​​‌​​​​​​‌‌‌‌‌‌​‌‌‌‌​​‌​⁠
