# AllSERP — Resource Paper Repository

**Working title:** *AllSERP: A Typed AOI and Per-Element Behavioral Enrichment of the AdSERP Dataset*

**Target venue:** SIGIR 2026 Resource Paper track (primary). Backup: CHIIR Resource paper, JEMR.

**Authors (TBD):** Andy Edmonds (lead). Co-authors gated on collaborator alignment — Latifzadeh, Gwizdka & Leiva (AdSERP authors) on courtesy review at minimum; possibly Jacek Gwizdka as senior coauthor depending on track decision.

---

## Scope

This is a **resource / dataset enrichment paper**: it describes the AOI extraction pipeline, validates it against shipped ground-truth, reports descriptive observed-behavior statistics per SERP element type, and points to enabled downstream analyses. **It is not a model paper.**

Explicit out-of-scope (other paper tracks):
- Four-class taxonomy as graded-relevance label generator → **CIKM 2026** (algorithmic; ranking).
- OSEC cognitive task model — Orient/Survey/Evaluate/Commit phase machinery → **CHI 2027** (Pittsburgh; Andy + Anderson rational-analysis lineage).
- Per-etype LF/HF cognitive load gradients → **ETTAC 2026** (Lyon, Aug 21; Duchowski coauthor).
- Per-fixation RIPA2 arousal / "lingered first time" findings → **standalone RIPA pub** (Gavindya/team track).

The AllSERP paper points to each of these via "what's enabled" pointers; it does not duplicate their findings.

---

## Headline empirical contributions

1. **Typed AOI extraction pipeline** validated against 38,250 shipped ad-rectangle classifications with **0 disagreements** (F1 = 1.000 on ad propagation, mean IoU = 1.000).
2. **`typed_gapfill` flavor** — pragmatic post-processing that fills inter-result Y gaps via midpoint-split, recovering signal previously dropped from per-AOI attribution.
3. **91.7 %** of corpus-wide final clicks attributable to a main-axis AOI under `typed_gapfill` (vs 75.1 % under tight typed bboxes; the remaining 8.3 % flagged off-axis at trial level — 158 hard-error trials [right-rail dd_right + page chrome + far-off-target] + ~73 no-click / pathological).
4. **Calibration-bias hypothesis tested and refuted** — opposite-direction click vs fixation bias confirms the data is screenshot-aligned; no coordinate-space drift to correct.
5. **Per-element-type descriptive inventory** across 9 etypes: organic / dd_top / native_ad / paa / image_pack / knowledge_panel / top_places / unknown_widget / other_widget. Click share, fixation coverage, regression rate, above-fold incidence.

---

## Layout

```
allserp-paper/
  paper.md                  — markdown draft (writing-first; LaTeX conversion later)
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

- **2026-05-05** — repository scaffolded. Markdown skeleton + introduction + methods stubs landed. Empirical numbers integrated from the bbox-y-coverage-fix cascade.
