#!/bin/bash
# usage: tools/render_all.sh PROJ [workers=4]
set -e
P=$(cd "$1" && pwd); N=${2:-4}; E=$(cd "$(dirname "$0")/../engine" && pwd)  # project-local engine (move/scale/fadeout, bigger text)
mkdir -p "$P/work/parts"
for i in $(seq 0 $((N-1))); do PROJ="$P" python3 "$E/render.py" $i $N & done; wait
: > "$P/work/cat.txt"; for i in $(seq 0 $((N-1))); do printf "file 'parts/p%02d.mp4'\n" $i >> "$P/work/cat.txt"; done
(cd "$P/work" && ffmpeg -v error -y -f concat -i cat.txt -c copy video.mp4)
echo "video -> $P/work/video.mp4"
