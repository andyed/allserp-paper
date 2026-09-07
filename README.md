# AllSERP — Resource Paper Repository

**Working title:** *AllSERP: Exhaustive Per-Element Enrichment of the Versatile AdSERP Dataset*

**Author:** Andy Edmonds.

---

## Scope

This is a **resource / dataset enrichment paper**: it describes the AOI extraction pipeline, validates it against shipped ground-truth, reports descriptive observed-behavior statistics per SERP element type, and points to enabled downstream analyses. **It is not a model paper.** Downstream model work is scoped out to sibling tracks and surfaces only as "what's enabled" pointers in §5.

---

## Headline empirical contributions

1. **Typed AOI extraction pipeline** validated against 38,250 shipped ad-rectangle classifications with **0 disagreements** (F1 = 1.000 on ad propagation, mean IoU = 1.000).
2. **`typed_gapfill` flavor** — pragmatic post-processing that fills inter-result Y gaps via midpoint-split, recovering signal previously dropped from per-AOI attribution.
3. **95.7 %** of corpus-wide final clicks attributable to a main-axis AOI under `typed_gapfill` once evtrack clicks are converted into screenshot space (91.5 % on the shipped document-space filter; the conversion recovers 118 flagged trials and loses none). Paper v4 reports clicks in screenshot space; the shipped `is_main_axis_click` helper is still document-space (queued substrate revision).
4. **Calibration-bias hypothesis tested and refuted** — opposite-direction click vs fixation bias confirms the data is screenshot-aligned; no coordinate-space drift to correct.
5. **Per-element-type descriptive inventory** across 8 main-axis etypes on AllSERP v1.1.0: organic / dd_top / native_ad / paa / image_pack / top_places / unknown_widget / other_widget (knowledge panels are right-rail, position −1, and no longer a main-axis row). Click share, fixation coverage, regression rate, above-fold incidence. Producer: `AF scripts/allserp_descriptives.py --flavor typed_gapfill --space screenshot`.
6. **Cell-aware flavor** (`typed_gapfill_cellsplit`) — the released frozen May snapshot contains 6,373 top-carousel cells across 1,550 trials. Its reported “100% alignment” is internal alignment to parent boxes, not card-level fidelity. Organic sub-cells and right-rail covariates remain separate tiers. A full-corpus screenshot-registered candidate now admits 1,570/1,575 eligible top subdivisions with matching independent counts (5 rejected cases remain unadmitted; not yet the released source); see [the current repair status](TODO.md#full-corpus-carousel-check--2026-09-04). The frozen export's parent rows are also stale relative to the current `typed_gapfill` export; adoption must preserve the pinned current parent baseline.
7. **Within-carousel composition (legacy snapshot)** — historical rank and click-share summaries await re-derivation from validated cells. The previously stated perfect rank correlation is retired. Current manuscript prose discloses the snapshot provenance; the repaired count audit is a diagnostic, not validation of those behavioral estimates. Producers: `scripts/cellsplit_click_composition.py`, `scripts/compute_nb23_cellsplit_rank.py` in attentional-foraging.

---

## Layout

```
allserp-paper/
  paper.tex                 — CANONICAL paper source (ACM acmart). Build: ./build.sh --acmart
  paper.md                  — FROZEN legacy markdown draft (pre-2026-05-06 acmart-format conversion; not current)
  README.md                 — this file
  CHANGELOG.md              — version + decision history
  CLAUDE.md                 — project conventions for AI-assisted edits
  sections/                 — LaTeX sections (placeholder; activate when stable)
  bib/                      — BibTeX entries
  figs/                     — figures + captions
  data/                     — derived numbers / cached extracts copied from
                              attentional-foraging at submission time
```

---

## Sources of truth

Every quantitative claim in this paper traces back to:

- **`attentional-foraging` repo** (`bbox-y-coverage-fix` branch, merged 2026-05-05):
  - `scripts/audit_*.py` — five cite-ready audit scripts
  - `scripts/output/allserp_descriptives_gapfill/` — descriptive tables
  - `docs/notebook-key-claims.md` — K-bbox-y-* row aggregates
  - `docs/null-findings/2026-05-05-bbox-y-coverage.md` — comprehensive cascade writeup
  - `docs/methodology/organic-result-aoi-extraction.md` — pipeline spec
  - `docs/methodology/attribution-cascade-synthesis.md` — flavor history
  - `docs/methodology/dd-top-cellsplit.md` — cell-split methodology, tier maturity, dd_right-as-covariate rationale
  - `scripts/output/adserp_aois_by_trial_id_typed_gapfill_cellsplit.csv` + `scripts/output/cellsplit_coverage.json` — cell-aware flavor + coverage
  - `scripts/cellsplit_click_composition.py` → `scripts/output/cellsplit_click_composition/` — within-carousel click composition (Fig. cellsplit)

- **`approach-retreat` repo** (`bbox-y-coverage-fix` branch, merged 2026-05-05):
  - `site/replay/` — visual verification on 147-trial replay set

The paper does not re-derive numbers; it cites them by file path + Key Claim ID.

---

## Two-pass citation discipline (per AF CLAUDE.md)

Every citation token in the paper goes through two passes:

- **Pass 1 — prose generation.** Use placeholders only: `[CITE: ...]`, `[ATTRIBUTE: ...]`, `[CHECK: ...]`. No author names in citation position, no venue+year tokens, no paraphrases of "what X showed."
- **Pass 2 — verification.** Walk every placeholder. Locate candidate source (bib first, then lit-notes, then WebSearch). Verify the abstract/passage matches the claim. Resolve placeholder with verified citation, or change the argument to use a source we have.

This separates prose from citation generation to prevent confabulation. See AF CLAUDE.md for the full discipline spec.

---

## Project status

- **2026-09-07** — v4 draft: restructured, re-derived on v1.1.0, new Coverage section. See CHANGELOG.
- **2026-05-05** — repository scaffolded. Markdown skeleton + introduction + methods stubs landed. Empirical numbers integrated from the bbox-y-coverage-fix cascade.
