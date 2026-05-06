#!/bin/bash
# Build paper PDFs.
#
# Usage:
#   ./build.sh                # markdown working copy via pandoc -> paper.pdf
#   ./build.sh --acmart       # ACM SIGIR / CHIIR submission via acmart -> paper-acmart.pdf
#   ./build.sh --anonymous    # anonymized version of the markdown copy
#
# acmart is bundled in ./texmf/ (via local TEXINPUTS); no system-wide install needed.
set -euo pipefail
cd "$(dirname "$0")"

ANON=0
ACMART=0
for arg in "$@"; do
  case "$arg" in
    --anonymous) ANON=1 ;;
    --acmart)    ACMART=1 ;;
  esac
done

if (( ACMART )); then
  # acmart pipeline: xelatex + bibtex passes against locally-installed packages
  export TEXMFHOME="$(pwd)/usertexmf"
  export TEXINPUTS=".:$(pwd)/usertexmf/tex//:${TEXINPUTS:-}"
  export BSTINPUTS=".:$(pwd)/usertexmf/bibtex/bst//:${BSTINPUTS:-}"
  export BIBINPUTS=".:$(pwd)/bib//:${BIBINPUTS:-}"
  rm -f paper.aux paper.bbl paper.blg paper.log paper.out paper.toc
  XELATEX="/Library/TeX/texbin/xelatex -interaction=nonstopmode -halt-on-error"
  $XELATEX paper.tex > /tmp/allserp-tex-pass1.log 2>&1 || { tail -30 /tmp/allserp-tex-pass1.log; exit 1; }
  /Library/TeX/texbin/bibtex paper > /tmp/allserp-bib.log 2>&1 || { tail -30 /tmp/allserp-bib.log; exit 1; }
  $XELATEX paper.tex > /tmp/allserp-tex-pass2.log 2>&1
  $XELATEX paper.tex > /tmp/allserp-tex-pass3.log 2>&1
  mv paper.pdf paper-acmart.pdf
  echo "wrote paper-acmart.pdf ($(du -h paper-acmart.pdf | cut -f1))"
  echo "logs: /tmp/allserp-tex-pass[1-3].log /tmp/allserp-bib.log"
  exit 0
fi

# Markdown working copy via pandoc -------------------------------------------

# Convert LaTeX-style \cite{...} into pandoc [@...]
sed -E 's/\\cite\{([^}]+)\}/\[@\1\]/g; s/; *@/; @/g' paper.md \
  | sed -E 's/\[@([^]]+),([^]]+)\]/[@\1; @\2]/g' \
  > .paper.tmp.md

if (( ANON )); then
  python3 - <<'PY'
import re, pathlib
src = pathlib.Path('.paper.tmp.md').read_text()
src = re.sub(
    r'(## Acknowledgments\s+).*?(\n\n|$)',
    r'\1[Acknowledgments redacted for double-blind review.]\2',
    src, count=1, flags=re.DOTALL,
)
src = src.replace('https://github.com/andyed/attentional-foraging',
                  'https://anonymous.4open.science/r/aoi-typing-pipeline')
src = src.replace('github.com/andyed/attentional-foraging',
                  'anonymous.4open.science/r/aoi-typing-pipeline')
src = src.replace('https://github.com/andyed/approach-retreat',
                  'https://anonymous.4open.science/r/cursor-episode-library')
src = src.replace('github.com/andyed/approach-retreat',
                  'anonymous.4open.science/r/cursor-episode-library')
src = src.replace('https://andyed.github.io/approach-retreat/replay/',
                  'https://anonymous-replay.example/replay/')
src = src.replace('andyed.github.io/approach-retreat/replay/',
                  'anonymous-replay.example/replay/')
src = re.sub(
    r'@misc\{edmonds2026allserp,\s*\n\s*author\s*=\s*\{Edmonds, Andy\},',
    '@misc{anonymous2026allserp,\n  author        = {Anonymous Authors},',
    src,
)
src = src.replace('edmonds2026allserp', 'anonymous2026allserp')
src = src.replace('Edmonds 2026', 'Anonymous 2026')
pathlib.Path('.paper.tmp.md').write_text(src)
PY
  TITLE_ARGS=( --metadata title="AllSERP: Exhaustive Per-Element Enrichment of the Versatile AdSERP Dataset" \
               --metadata author="Anonymous Authors" )
  OUT=paper-anonymous.pdf
else
  TITLE_ARGS=( --metadata title="AllSERP: Exhaustive Per-Element Enrichment of the Versatile AdSERP Dataset" \
               --metadata author="Andy Edmonds" )
  OUT=paper.pdf
fi

pandoc .paper.tmp.md \
  --from=markdown \
  --to=pdf \
  --pdf-engine=xelatex \
  --bibliography=bib/allserp.bib \
  --citeproc \
  "${TITLE_ARGS[@]}" \
  --metadata date="$(date +%Y-%m-%d)" \
  -V geometry:margin=1in \
  -V fontsize=10pt \
  -V linkcolor=blue \
  -o "$OUT"

rm -f .paper.tmp.md
echo "wrote $OUT ($(du -h $OUT | cut -f1))"
