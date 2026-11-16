#!/bin/bash
# usage: tools/new_project.sh projects/my-topic   (copies the example episode.py as a starting point)
set -e
S=$(cd "$(dirname "$0")/.." && pwd); mkdir -p "$1"/{assets_raw,assets_key,work,final}
cp "$S/example/sleep-muscle/episode.py" "$1/episode.py"; cp "$S/templates/agent-prompt.md" "$1/agent-prompt.md"
echo "new project at $1 : 1) send agent-prompt.md + style-ref/ to Flow  2) tools/key.py $1 <unzipped>  3) prep_vo  4) edit episode.py  5) stills -> render_all -> finish"
