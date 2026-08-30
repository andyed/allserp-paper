# v4 revision TODO

Items queued for the next arXiv revision. Each entry names the claim or section
affected and the upstream evidence; numbers come from the attentional-foraging
substrate at `release/allserp-v1.1.0` post `574218b6` (typed maps content hash
`2cb789eb8febd234`) unless noted.

## 1 · Restate the within-carousel rank correlation (in progress, separate session)

The published within-carousel ρ = −1.0 (paper.tex, §results) is not supportable:
positions 1 and 2 are unordered under every denominator tried. Direction holds;
the perfect monotone does not. Restate, don't retract. Context: the carousel
cell layer scores ~31% agreement against DOM ground truth in the fidelity
harness (`attentional-foraging/scripts/aoi_fidelity.py`), and the cells derive
from a frozen 2026-05-24 snapshot with no in-repo producer.

## 2 · Callout: widget blocks are first-class slots in the typed flavor

Add an explicit callout (taxonomy/flavors section) that non-linear SERP
furniture — map/local-pack blocks in particular — is handled as first-class
AOIs in the typed flavor rather than absorbed or skipped:

- Local packs type as `top_places` with their own position and geometry, in
  main-axis display order. Corpus counts: 354 of 2,776 trials (12.8%) contain
  one; 352 on the main axis; **35 strictly between organics**.
- `organic_rank` numbers within organics only, so a widget occupying a slot
  never shifts organic ranks in any within-organic quantity. Under typed
  display order the widget deliberately counts as a slot — same treatment as
  `dd_top`, `paa`, `image_pack`.
- Contrast: in the `organic` / `organic_hybrid` flavors widgets are not slots;
  consumers choosing a flavor should understand this is a flavor semantics
  choice, not a coverage gap.
- Honest caveat to include: local packs were the hard *alignment* cases (the
  y-DP realignment), and the 12 alignment-excluded trials are precisely the
  pathological-widget pages — quarantined rather than silently mislabeled.

## 3 · Data statement: post-release substrate fix + re-pin

Document the 2026-08-30 aoi-card-collision fix (two-phase DOM-node claiming in
`measure_card_geometry`; geometry collisions 454 → 0, orphaned main-column
trials 17.3% → 6.0%, 454 typed maps changed per flavor) and re-pin the
substrate identity in the data statement: typed maps content hash
`2cb789eb8febd234`, exclusion list 12 trials (membership changed from the
14-trial list — consumers must re-read it). Point readers at the fidelity
harness (click 92.4% / AOI IoU≥0.5 93.3% / cell 31.0% on the 120-trial
sample) as the substrate's standing quality measurement.
