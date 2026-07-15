#!/bin/bash
# Build arXiv submission tarball for AllSERP.
#
# Usage:
#   ./make-arxiv-bundle.sh           # rebuild first, then bundle
#   ./make-arxiv-bundle.sh --skip-build   # bundle whatever is currently built
#
# Output: allserp-arxiv.tar.gz at the repo root.
# Staging dir at .arxiv-staging/ is wiped and recreated each run.
set -euo pipefail
cd "$(dirname "$0")"

# Prevent macOS from writing AppleDouble (._*) resource-fork sidecar files
# into the tarball; arXiv strips them anyway but it's noise in the log.
export COPYFILE_DISABLE=1

SKIP_BUILD=0
for arg in "$@"; do
  case "$arg" in
    --skip-build) SKIP_BUILD=1 ;;
    *) echo "unknown arg: $arg"; exit 1 ;;
  esac
done

if (( ! SKIP_BUILD )); then
  echo "==> rebuilding paper-acmart.pdf + paper.bbl"
  ./build.sh --acmart
  echo ""
fi

STAGE=".arxiv-staging"
TARBALL="allserp-arxiv.tar.gz"

echo "==> staging into $STAGE/"
rm -rf "$STAGE"
mkdir -p "$STAGE/bib" "$STAGE/figs"

# Source + bibliography
cp paper.tex          "$STAGE/paper.tex"
cp paper.bbl          "$STAGE/paper.bbl"
cp bib/allserp.bib    "$STAGE/bib/allserp.bib"

# Figures — derived from every \includegraphics target in paper.tex, so the
# staged set cannot drift from the source. (The hardcoded list this replaced
# silently dropped fig_cellsplit_composition.png after the dd_top cell split.)
echo "==> staging figures referenced by paper.tex"
while IFS= read -r ref; do
  if [[ ! -f "$ref" ]]; then
    echo "  MISSING SOURCE: $ref (referenced in paper.tex but not on disk)"
    exit 1
  fi
  mkdir -p "$STAGE/$(dirname "$ref")"
  cp "$ref" "$STAGE/$ref"
  echo "  staged $ref"
done < <(grep -oE '\\includegraphics(\[[^]]*\])?\{[^}]+\}' paper.tex | grep -oE '\{[^}]+\}' | tr -d '{}')

# Sanity check: every \includegraphics target in paper.tex must exist in stage
echo ""
echo "==> verifying every \\includegraphics target is staged"
missing=0
while IFS= read -r ref; do
  if [[ ! -f "$STAGE/$ref" ]]; then
    echo "  MISSING: $ref"
    missing=1
  fi
done < <(grep -oE '\\includegraphics(\[[^]]*\])?\{[^}]+\}' paper.tex | grep -oE '\{[^}]+\}' | tr -d '{}')
if (( missing )); then
  echo "==> aborting: figures missing from $STAGE"
  exit 1
fi
echo "  all figure refs present"

echo ""
echo "==> packing $TARBALL"
rm -f "$TARBALL"
tar -czf "$TARBALL" -C "$STAGE" .

echo ""
echo "wrote $TARBALL ($(du -h "$TARBALL" | cut -f1))"
echo ""
echo "contents:"
tar -tzf "$TARBALL"
