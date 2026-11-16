# Setup (for the AI to run)

The user opened this folder in Claude Code and typed something like "ติดตั้งสกิล" (or "อ่าน SETUP.md แล้วติดตั้งทุกอย่างให้หน่อย").

## 0. Shared tools — check what this machine already has (do this first)
Everything this skill needs is installed from this file. Never send the user to a website or another download for setup.
- Look for `~/.tadmaipen/setup-done.json` (Windows: `%USERPROFILE%\.tadmaipen\setup-done.json`).
- **Found:** the shared tools are already installed. Skip every step below that only installs Homebrew/winget, ffmpeg,
  Node, Python, Git/Git LFS, libraqm, numpy, scipy, pillow, soundfile, opencv-python-headless, pythainlp, sherpa-onnx,
  the Whisper turbo model in `~/asr/sherpa-onnx-whisper-turbo`, Playwright Chromium or the HyperFrames plugin.
  Do only what is specific to this skill.
- **Not found:** install what this skill needs yourself, right here, using the steps below — don't ask the user to
  download anything else. Check each tool first (`ffmpeg -version`, `node -v`, `python3 --version`,
  `python3 -m pip show <package>`, `npx playwright --version` …) and install only what is missing.
  If `SKILL.md` needs a tool this file doesn't cover, install it the usual way (Mac `brew`, Windows `winget`, `pip`, `npm`).
  Don't create `~/.tadmaipen/setup-done.json` — that file means every shared tool is installed, not just this skill's.
- The self-test / example render (if this file has one) is optional: skip it unless the user asks for a test clip.

## 1. Skill-specific tools
If `setup-done.json` was found, the machine already has ffmpeg, Python 3 + numpy soundfile, Pillow with libraqm (Thai shaping), sherpa-onnx and the
Whisper turbo model in `~/asr/sherpa-onnx-whisper-turbo`. Fonts (Kanit, OFL), the 2 swooshes and the synth music bed
(`tools/music_synth.py`) are bundled. Nothing else to install.
Check Thai shaping: `python3 -c "from PIL import features; print(features.check('raqm'))"` must print True.
If the shared tools are missing (no `setup-done.json`): ffmpeg (Mac `brew install ffmpeg libraqm`, Windows `winget install Gyan.FFmpeg`),
`pip3 install numpy soundfile pillow sherpa-onnx` (Pillow must find libraqm), then
`mkdir -p ~/asr && cd ~/asr && curl -LO https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-turbo.tar.bz2 && tar xjf sherpa-onnx-whisper-turbo.tar.bz2`.

## 2. Install the skill
Copy this folder so every new Claude Code session knows it, from any folder:
- Mac: `mkdir -p ~/.claude/skills && cp -R <this folder> ~/.claude/skills/white-mascot-fitness-explainer`
- Windows: copy the folder to `%USERPROFILE%\.claude\skills\white-mascot-fitness-explainer`

## 3. Finish
Tell the user in Thai, in 2-3 short lines, that the skill is ready and what to type next (see HOW-TO-USE.md if present).
