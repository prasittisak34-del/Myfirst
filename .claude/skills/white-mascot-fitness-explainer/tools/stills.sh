#!/bin/bash
# check frames before a full render: tools/stills.sh PROJ 1.5 6 12.3 ...
P=$(cd "$1" && pwd); shift; E=$(cd "$(dirname "$0")/../engine" && pwd)
mkdir -p "$P/work/stills"; PROJ="$P" python3 "$E/render.py" still "$@"; echo "stills -> $P/work/stills"
