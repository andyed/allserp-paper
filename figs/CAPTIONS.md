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

## Fig 4 — Replay viewer screenshots (4-panel grid)

**File:** `fig4_replay_examples.pdf`
**Source data:** `approach-retreat/site/replay/trials/{p005-b2-t2, p008-b3-t7, p009-b5-t2, p041-b5-t2}.html`
**Type:** 4-panel screenshot grid
**Panels:**
  1. `p005-b2-t2`: in-column-edge gap click between organics 5 and 6 — *how `typed_gapfill` resolves it*
  2. `p008-b3-t7`: right-rail dd_right click — *how `is_main_axis_click` filters it out*
  3. `p009-b5-t2`: page-chrome (search tools) click — *how trial-level filter handles non-result clicks*
  4. `p041-b5-t2`: right-rail click without shipped dd_right rect — *the dd_right blind spot named in §6*
**Caption:** "Four representative trials from the AR replay viewer (147-trial curated subset). Each panel shows the source SERP screenshot with `typed_gapfill` AOI bboxes overlaid as colored rectangles, gaze fixations as numbered circles (size proportional to dwell), cursor trajectory as a path, and the final click as a distinct marker. Panel (a) shows a click in the inter-result Y gap that the legacy tight bboxes would have lost; under `typed_gapfill` the click attributes correctly. Panels (b–d) show the three categories of off-axis click that `is_main_axis_click` flags at trial level: shipped right-rail dd_right ad (b), page-chrome click on search tools (c), and a right-rail surface without a shipped dd_right rectangle (d, the unnamed-blind-spot case)."

## Fig 5 — Above-fold geometry by element type (stacked bar)

**File:** `fig5_above_fold.pdf`
**Source data:** `per_etype_table.csv`, columns `n_trials_with_etype_above_fold`, `above_fold_trial_pct`
**Type:** horizontal stacked bar with 9 etypes
**Caption:** "Above-fold incidence per element type (above fold = AOI top_y < initial viewport height, scroll = 0). Organic results sit above the initial fold on 97.3 % of trials; widgets (knowledge_panel, paa, top_places) on 1–11 %. Per-element above-fold conditioning is therefore necessary for any analysis that joins viewport visibility with click outcome — pooling across element types averages out the dominant geometric reality."

---

## Notes on rendering

- All figures rendered from the upstream tagged data (`scripts/output/allserp_descriptives_gapfill/`); none depend on private state.
- Figure 4 (replay grid) requires the AdSERP screenshot volume mounted to render the source SERP backgrounds. Two of the four trials are in the local cache; the other two need the volume.
- Use Andy's `muriel` skill / brand tokens for color palette consistency; defer to ACM template constraints for SIGIR submission.
- Compute 8:1 contrast ratios for any text overlays (per Andy's project-wide rule).
