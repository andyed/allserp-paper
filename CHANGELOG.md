# Changelog

## 2026-05-10 — Gaze-cursor spatial-registration validity paragraph

Added a `\paragraph{Gaze-cursor spatial registration}` to §sec:validation. The check: for each trial with a final click, take all gaze fixations whose midpoint sits in $[t_\text{click}-1500\,\text{ms}, t_\text{click}]$ and compute the minimum Euclidean distance from any such fixation to the click coordinates. Median 128.8 px, IQR 80.4--206.5, p95 446.2; 17.8 % (489 / 2,752) above 250 px ($\sim$3° visual angle). Concurrent at-click distance reported alongside (median 506.8 px) only to disambiguate the question — gaze leads cursor by several hundred milliseconds, so synchronous co-location isn't the right registration probe.

Producer: `scripts/audit_gaze_cursor_coverage.py` (in upstream `attentional-foraging`).
Output: `scripts/output/allserp/gaze_cursor_coverage.json` (provenance-stamped via `muriel.provenance`).

## 2026-05-05 — Repository scaffolded

Initial setup. Working title *AllSERP: Exhaustive Per-Element Enrichment of the Versatile AdSERP Dataset*. Target venue SIGIR 2026 Resource Paper track (primary).

### What landed

- `README.md` — project overview, scope, sources-of-truth, two-pass citation discipline.
- `CLAUDE.md` — project conventions for AI-assisted edits; sibling-track guards; voice spec.
- `paper.md` — markdown draft skeleton with section structure and stub content for §1 (Introduction), §2 (Method: Typed AOI Extraction), §3 (Element-Type Inventory), §4 (Observed Behavior).
- Directory layout: `sections/` `bib/` `figs/` `data/`.

### Empirical foundation (carried forward from upstream)

All numbers anchor to the `attentional-foraging` `bbox-y-coverage-fix` cascade (commit `ac92bbb4`, merged 2026-05-05):
- 91.7 % final-click attribution under typed_gapfill (vs 75.1 % tight typed)
- 38,250 ad-classification validation against shipped ground-truth: 0 disagreements
- 22.7 % silent contamination of approached-and-clicked records under legacy typed (refuted via X+Y bbox attribution)
- Calibration-bias hypothesis tested and refuted (`audit_screenshot_alignment.py`, `audit_calibration_bias.py`)
- K-bbox-y-* rows landed for NB21 / NB22 / NB28 / NB30

### Out-of-scope (sibling tracks)

- CIKM 2026 (algorithmic / four-class graded relevance)
- CHI 2027 Pittsburgh (OSEC task model)
- ETTAC 2026 Lyon (LF/HF cognitive load)
- Standalone RIPA pub (Gavindya/team)

The paper points to each as "what's enabled" in §5.
