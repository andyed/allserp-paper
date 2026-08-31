# TODO

## arXiv v4 revision (target: after AF substrate fixes merge)

Driven by the 2026-08-30 substrate review in `attentional-foraging`
(`docs/JOURNEY-2026-08-30.md`, `docs/aoi-fidelity-baseline-2026-08-30.md`,
harness `scripts/aoi_fidelity.py`). Order matters: items 2--4 need upstream
work to land first; item 1 is done in-tree.

1. **[DONE in working tree] Restate the within-carousel $\rho = -1.0$** (paper.tex,
   §Inventory, "Within-carousel composition"). Positions 1 and 2 are not ordered
   under any click-attribution denominator tried, so the perfect monotone is not
   supportable. Direction holds (4.3 % → 2.0 %, leftmost → fifth). Restated as a
   directional decline with endpoints and no rank coefficient, plus an inline
   v3-erratum note. **No replacement coefficient is established** — do not
   substitute the −0.900 from the zero-paging analysis; that number scored
   `vplaurlt`/`platop` ids that double-count right-rail cells and is one of the
   review's documented wrong turns.

2. **Re-derive all per-cell numbers from DOM-derived cells.** Every cellsplit
   number in the paper (31.7 % leftmost share, 4.3 %/2.0 % CTR endpoints, the
   ρ = −0.94 fixation/dwell gradients, Fig. cellsplit both panels) is computed on
   cells from a **frozen 2026-05-24 snapshot with no producer in the repo**. The
   cell layer scores **29.1 % agreement (451/1,551)** against DOM ground truth in
   the `aoi_fidelity.py` cell check; the export is short on 902/1,551 carousels,
   median shortfall exactly 1 cell (trailing-drop). AF's stated next step is a
   DOM-derived cellsplit; regenerate `nb23_cellsplit_rank` /
   `nb25_cellsplit_composition` from it, then re-render the figure and re-run the
   numbers here.

3. **Disclose cell-layer fidelity where "100 % aligned" appears.** The
   "100 % aligned to the block-level bboxes" claims (§Validation "Top-ads cell
   subdivision" ¶, and the `typed_gapfill_cellsplit` CSV bullet in §Release) are
   internal consistency against the block bbox, not DOM fidelity. Add the 29.1 %
   DOM-agreement number and the frozen-snapshot provenance so the two aren't
   conflated.

4. **Mouse-stream coordinate-space fix ripples into click attribution.** evtrack
   records document space (1403 px), AOIs are screenshot space (1280 px);
   anisotropic scale x 0.9123 / y 0.9000. Conversion moves click-in-AOI
   containment 78.0 % → 96.2 %. Once AF's `fix/coordinate-space-loader` +
   `fix/wire-cursor-conversion` (and `fix/aoi-card-collision`) merge, re-derive
   Table 1, the 91.7 % X+Y attribution figure, and re-run the 38,250
   ad-classification check. Fixation → AOI attribution was never affected;
   gaze-anchored numbers stand.

5. **Optional v4 addition — zero-paging finding.** Across 1,582 carousels and 272
   cell clicks, zero clicks landed on a card not already on screen (27 DOM cells,
   ~5 visible). Settles the definitional question for the DOM-derived cellsplit:
   visible cells are what participants experienced. Good one-paragraph resource
   note if it fits.

6. **Draft the arXiv v4 change-note + Comments field** in CHANGELOG.md once 2--4
   land (pattern of the 2026-07-10 v3 entry).
