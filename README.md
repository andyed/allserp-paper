# AllSERP — Resource Paper Repository

**AllSERP: Exhaustive Per-Element Enrichment of the Versatile AdSERP Dataset**
Andy Edmonds. arXiv:[2605.04949](https://arxiv.org/abs/2605.04949).

Live on arXiv: **v3** (2026-07-23). **v4** is drafted, rebuilt, and bundled (2026-09-07);
upload is pending the landing checklist in [TODO.md](TODO.md). The change-note for each
version is in [CHANGELOG.md](CHANGELOG.md).

---

## What the paper is

A **resource / dataset-enrichment paper**. AdSERP ships 2,776 search trials with gaze,
cursor, scroll, pupil and click telemetry on real Google result pages, but its bounding
boxes cover only advertisements. AllSERP adds a typed area-of-interest (AOI) layer for
everything else: screenshot-anchored boxes for organic results, People-Also-Ask, image
packs, local packs and other widgets, labelled from the captured HTML. The paper
describes the pipeline, validates it, reports a per-element behavioural inventory, and
documents how coverage grew across and within element types.

It is **not a model paper**. Downstream model work lives in sibling tracks and appears
only as "what's enabled" pointers.

## Headline claims (v4, on AllSERP v1.1.1)

1. **Ad partition validated** against the shipped ad rectangles: 0 disagreements across
   38,250 classifications. A DOM-based harness measures box fidelity on the full corpus.
2. **Three released flavours** trade box tightness for coverage: `typed` (tight boxes),
   `typed_gapfill` (inter-result Y gaps filled by midpoint split), and
   `typed_gapfill_cellsplit` (per-card cells inside the top-ads carousel).
3. **95.7 % of final clicks** land in a typed main-axis AOI under `typed_gapfill` once
   evtrack cursor coordinates are converted into screenshot space (91.5 % on the shipped
   document-space filter). The shipped `is_main_axis_click` helper is still
   document-space; the paper discloses this as a queued substrate revision.
4. **Calibration-bias hypothesis tested and refuted**: opposite-direction click vs
   fixation bias confirms the data is screenshot-aligned.
5. **Per-element inventory** across 8 main-axis element types (organic, dd_top,
   native_ad, paa, image_pack, top_places, unknown_widget, other_widget): click share,
   fixation coverage, regression rate, above-fold incidence. Knowledge panels are
   right-rail (position −1) and no longer a main-axis row.
6. **Coverage section** (new in v4): how coverage grew across element types (organic
   boxes → HTML typing → gap-fill → geometric label verification in v1.1.0) and within
   them (the carousel cell layer). The v3 within-carousel rank claim (ρ = −1.0) is
   withdrawn and restated as directional; the released cells come from a May 2026
   snapshot and the paper says so.

**Substrate identity.** Every number is pinned to AllSERP enrichment **v1.1.1**:
2,764 analysable trials, a 12-trial alignment-exclusion list, typed-map content hash
`2cb789eb8febd234`. A stale export contains ~746 main-column knowledge-panel rows and
84 local packs; v1.1.1 contains 0 and 340.

---

## Layout

```
allserp-paper/
  paper.tex               CANONICAL source (ACM acmart). Build: ./build.sh --acmart
  paper-acmart.pdf        tracked build output, for early sharing
  paper.md                FROZEN legacy markdown draft (pre-2026-05-06); not current
  build.sh                acmart build (xelatex + bibtex); legacy pandoc paths retained
  make-arxiv-bundle.sh    rebuilds, then stages paper.tex/.bbl/bib/figs -> allserp-arxiv.tar.gz
  bib/allserp.bib         bibliography
  figs/                   figures + CAPTIONS.md + render_*.py / render_replay.js producers
  CHANGELOG.md            per-arXiv-version change-notes and decision history
  TODO.md                 v4 worklist and the pre-upload landing checklist
  CLAUDE.md               editing conventions (citation discipline, voice, commit types)
```

Not tracked: `texmf/` and `usertexmf/` (the local acmart install that `build.sh` expects
via `TEXMFHOME`), `.arxiv-staging/`, the tarball, working PDFs, and `notes/` (private
coordination). A fresh clone needs acmart installed locally before `./build.sh --acmart`
will run.

## Building

```bash
./build.sh --acmart          # paper.tex -> paper-acmart.pdf
./make-arxiv-bundle.sh       # rebuild + stage -> allserp-arxiv.tar.gz
```

Figures regenerate from `figs/render*.py` and `figs/render_replay.js`; they read the
attentional-foraging outputs listed below. `figs/CAPTIONS.md` holds the caption text.

---

## Sources of truth

The paper does not re-derive numbers. Every quantitative claim traces to a file in one
of two repositories:

- **[attentional-foraging](https://github.com/andyed/attentional-foraging)** — pipeline
  and producers. Substrate branch `release/allserp-v1.1.0`, tag `allserp-v1.1.1`
  (release publication is item 1 of the TODO landing checklist).
  - `scripts/allserp_descriptives.py --flavor typed_gapfill --space screenshot` — Table 1
  - `scripts/audit_*.py` — cite-ready audit producers (`audit_cascade_contamination.py`,
    `audit_dd_right.py --space screenshot`, and the ad-rectangle check)
  - `scripts/output/adserp_aois_by_trial_id_{typed,typed_gapfill,organic_hybrid,typed_gapfill_cellsplit}.csv`
    and `data/aoi-typed/alignment-exclusions.json` — the released exports
  - `docs/methodology/organic-result-aoi-extraction.md` — pipeline spec
  - `docs/methodology/attribution-cascade-synthesis.md` — flavour history
  - `docs/methodology/dd-top-cellsplit.md` — cell-split tiers, dd_right-as-covariate
  - `docs/methodology/carousel-full-corpus-validation.md` — DOM-derived carousel candidate
    (1,570/1,575 admitted, 7,265 cards)
  - `docs/allserp-v1.1.0-migration.md`, `docs/releases/allserp-v1.1.1.md` — substrate notes
  - `docs/notebook-key-claims.md` — Key Claim IDs cited in the text
- **[approach-retreat](https://github.com/andyed/approach-retreat)** — the
  [replay viewer](https://andyed.github.io/approach-retreat/replay/) (148 curated trials,
  labelled log-scaled LF/HF tracks as of the v4 figure).

The underlying corpus is the AdSERP Zenodo volume
([zenodo.org/records/15236546](https://zenodo.org/records/15236546), CC-BY-4.0). AllSERP
does not redistribute it.

---

## Editing

Conventions for edits (two-pass citation discipline, voice, sibling-track guard,
conventional-commit types) are in [CLAUDE.md](CLAUDE.md). Short version: no author names
or venue tokens in citation position until the source has been verified against its
abstract, and no number without a `[<flavor>, <source>]` provenance.

## History

| date | event |
|---|---|
| 2026-05-05 | repository scaffolded from the bbox-y-coverage-fix cascade |
| 2026-05-06 | arXiv **v1** submitted |
| 2026-05-19 | arXiv **v2**: ARS-audit / reviewer-pass cleanup |
| 2026-06-23 | `paper.md` frozen; `paper.tex` canonical |
| 2026-07-23 | arXiv **v3**: dd_top cell-split enrichment, within-carousel ordering |
| 2026-09-07 | **v4** drafted and bundled: restructure, re-derivation on v1.1.1, Coverage section; upload pending |

## Citation

```bibtex
@misc{edmonds2026allserp,
  title  = {AllSERP: Exhaustive Per-Element Enrichment of the Versatile AdSERP Dataset},
  author = {Edmonds, Andy},
  year   = {2026},
  eprint = {2605.04949},
  archivePrefix = {arXiv},
  url    = {https://arxiv.org/abs/2605.04949}
}
```
