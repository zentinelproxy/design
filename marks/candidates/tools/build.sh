#!/usr/bin/env bash
# Rebuild the machine-traced shisa candidates in marks/candidates/.
# Needs: python3 + venv (vtracer 0.6.15, pillow, numpy, scipy), potrace 1.16,
# node (svgo 3.3.2, @resvg/resvg-js 2.6.2). See marks/PROVENANCE.md.
#
#   TOOLS_VENV=/path/to/venv TOOLS_NODE=/path/to/node_project marks/candidates/tools/build.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
HERE="$ROOT/marks/candidates"
PY="${TOOLS_VENV:?set TOOLS_VENV to a venv with vtracer pillow numpy scipy}/bin/python"
NODE_DIR="${TOOLS_NODE:?set TOOLS_NODE to a dir with svgo and @resvg/resvg-js in node_modules}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

"$PY" -I "$HERE/tools/prep.py" "$ROOT/marks/source/zentinel-mascot-1024.png" "$WORK"

# Full colour: vtracer on the pre-quantised disc.
"$PY" -I -c "import sys, vtracer; vtracer.convert_image_to_svg_py(sys.argv[1], sys.argv[2],
  colormode='color', hierarchical='stacked', mode='spline', filter_speckle=8,
  color_precision=8, layer_difference=8, corner_threshold=60, length_threshold=4.0,
  max_iterations=10, splice_threshold=45, path_precision=1)" "$WORK/colour-q.png" "$WORK/colour-raw.svg"

# One colour: potrace on the head masks.
for m in line solid fill face feat nose; do
  potrace -s -t 24 -a 1.0 -O 0.4 -o "$WORK/head-$m-raw.svg" "$WORK/head-$m.pbm"
done

"$PY" -I "$HERE/tools/assemble.py" "$WORK" "$ROOT"

for f in "$WORK"/out/*.svg; do
  "$NODE_DIR/node_modules/.bin/svgo" --config "$HERE/tools/svgo.config.cjs" -q "$f" -o "$HERE/$(basename "$f")"
done
"$PY" -I "$HERE/tools/lockup.py" "$ROOT"
"$PY" -I "$HERE/tools/page.py" "$ROOT"

# Small-size test renders (resvg).
mkdir -p "$HERE/renders"
for f in zentinel-mark-colour zentinel-mark-mono-line zentinel-mark-mono-solid favicon favicon-colour; do
  for s in 16 32 48; do
    node "$HERE/tools/render.cjs" "$NODE_DIR" "$HERE/$f.svg" "$HERE/renders/$f-$s.png" "$s"
  done
done
ls -l "$HERE"/*.svg
