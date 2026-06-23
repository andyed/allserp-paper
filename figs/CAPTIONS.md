# Figure plan — AllSERP resource paper

This file documents intended figures + caption stubs. Figures themselves are not yet generated; they will be produced from the upstream data when the paper moves to LaTeX.

---

## Fig 1 — Element-type inventory (bar chart)

**File:** `fig1_element_type_inventory.pdf` *(not yet rendered)*
**Source data:** `attentional-foraging/scripts/output/allserp_descriptives_gapfill/per_etype_table.csv`
**Type:** stacked horizontal bar chart, 9 element types
**Bars:** total AOIs per etype (organic 22,346 ; native_ad 9,214 ; image_pack 1,584 ; dd_top 1,582 ; paa 769 ; unknown_widget 788 ; knowledge_panel 745 ; top_places 84 ; other_widget 50)
**Color overlay:** fixated proportion (light) vs not-fixated (dark)
**Caption:** "Per-element-type AOI inventory across the 2,776-trial AdSERP corpus under `typed_gapfill` attribution. Bar lengths give absolute AOI counts (37,142 total); shaded portion denotes the share of AOIs receiving at least one fixation. Note the near-universal fixation rate of `dd_top` (99.7 %) versus the ~36 % rate for `native_ad`, where most below-fold native ads are never fixated."

## Fig 2 — Click-fixation dissociation (scatter or paired-bar)

**File:** `fig2_click_fixation_dissociation.pdf`
**Source data:** same `per_etype_table.csv`
**Type:** paired-bar, 9 etypes, two bars per etype (fixated %, click-share %)
**Caption:** "Click-fixation dissociation per element type. `dd_top` reaches 99.7 % fixation coverage but receives only 9.6 % of attributable clicks (10.4× attention-to-click gap); `native_ad` shows 36.4 % fixation and 5.9 % clicks (6.2× gap). Organic results invert the ratio: 55.6 % fixation, 79.1 % click share. The dissociation present in the original AdSERP analysis at the ad-vs-organic level is preserved at finer element-type granularity, with the click-attribution gap quantified honestly under `typed_gapfill` rather than diluted by Y-band-misattributed off-axis clicks."

## Fig 3 — Audit-cascade flow diagram

**File:** `fig3_audit_cascade.pdf`
**Type:** flow diagram, 5 boxes (one per audit script) → 1 outcome box (`typed_gapfill` mitigation)
**Caption:** "The 2026-05-05 audit cascade. Five independent audit producers (`audit_unattributed_clicks`, `audit_dd_right`, `audit_cascade_contamination`, `audit_calibration_bias`, `audit_screenshot_alignment`) jointly establish: 22.7 % silent contamination of approached-and-clicked records under the legacy Y-band attribution (Q1); the gate does not filter contamination out (Q3); the calibration-bias hypothesis is refuted (opposite-direction click vs fixation bias). The mitigation — `typed_gapfill` — combines midpoint-split bbox extension, X+Y bbox-aware click attribution, and an `is_main_axis_click` trial filter."

## Fig 4 — Replay viewer single trial (full SERP height with sparklines)

**File:** `fig4_replay_p005-b2-t2.png` (rendered, auto-cropped)
**Source data:** `approach-retreat/site/replay/trials/p005-b2-t2.html` rendered via headless Chromium at 2× device-scale
**Type:** single full-height screenshot, cropped to last non-empty content row + 10 px margin
**Production:** `figs/render_replay.js` (Playwright capture) → `figs/crop_replay.py` (PIL auto-crop). Both reproducible from the upstream replay viewer + this paper's repo.
**Caption:** "An AR replay viewer trial (p005-b2-t2) rendered at full SERP height with the trial's behavioral sparklines below. The SERP screenshot (top) carries `typed_gapfill` AOI bboxes as colored overlays — outline color encodes the four-class behavioral taxonomy outcome per AOI (clicked / deferred / evaluated-rejected / not-approached). Numbered circles show gaze fixations sized by dwell duration; the orange path shows the cursor trajectory; a distinct marker indicates the trial-terminating click. The compact timeline below the SERP carries seven sparkline tracks: cursor speed, XY delta, pupil diameter, LF/HF ratio, gaze X, gaze Y, and AOI presence. The replay viewer renders 147 such trials from the curated subset; this single example lets the reader see what one trial of the AdSERP corpus looks like under the AllSERP enrichment."

## Fig 5 — Above-fold geometry by element type (stacked bar)

**File:** `fig5_above_fold.pdf`
**Source data:** `per_etype_table.csv`, columns `n_trials_with_etype_above_fold`, `above_fold_trial_pct`
**Type:** horizontal stacked bar with 9 etypes
**Caption:** "Above-fold incidence per element type (above fold = AOI top_y < initial viewport height, scroll = 0). Organic results sit above the initial fold on 97.3 % of trials; widgets (knowledge_panel, paa, top_places) on 1–11 %. Per-element above-fold conditioning is therefore necessary for any analysis that joins viewport visibility with click outcome — pooling across element types averages out the dominant geometric reality."

## Fig 6 — dd_top cell split anatomy (two-panel bar chart)

**File:** `fig_cellsplit_composition.pdf` / `.png` (rendered)
**Source data:** `attentional-foraging/scripts/output/nb25_cellsplit_composition/cells_per_carousel.csv` (left); `attentional-foraging/scripts/output/cellsplit_click_composition/by_cell_index.csv` (right)
**Production:** `figs/render_cellsplit_composition.py` (matplotlib; all text in INK ≈ 18:1 contrast on BG, well above the 8:1 floor)
**Type:** two side-by-side bar charts
**Caption:** "Anatomy of the `dd_top` cell split. Left: top-ads carousels hold 2–6 cards, modal 4 (61.9 % of 1,550 carousels). Right: of the 237 clicks landing inside a carousel, the within-carousel distribution on the modal four-cell layout (n = 142) favors the leftmost cell (31.7 % vs the 25 % uniform baseline) but spreads across all cells. The block-level `dd_top` AOI conflates this distribution; the cell-aware flavor (`typed_gapfill_cellsplit`) exposes it."

---

## Notes on rendering

- All figures rendered from the upstream tagged data (`scripts/output/allserp_descriptives_gapfill/`); none depend on private state.
- Figure 4 (replay grid) requires the AdSERP screenshot volume mounted to render the source SERP backgrounds. Two of the four trials are in the local cache; the other two need the volume.
- Use Andy's `muriel` skill / brand tokens for color palette consistency; defer to ACM template constraints for SIGIR submission.
- Compute 8:1 contrast ratios for any text overlays (per Andy's project-wide rule).
