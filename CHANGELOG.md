# Changelog

## 2026-07-10 — arXiv v3 (dd_top cell-split enrichment + within-carousel ordering)

Change-note for the arXiv:2605.04949 **v3** replacement. Baseline is the live **v2** (submitted
2026-05-19), which was v1 (`ef15946`, 2026-05-06) plus the 2026-05-18 ARS-audit / reviewer-pass
cleanup (`c20e6f0`, `bddd2bf`). Everything below landed after that v2. Bundled by
`make-arxiv-bundle.sh` from `paper.tex`.

**New content (v2 → v3):**
- **`dd_top` cell-split enrichment.** New `typed_gapfill_cellsplit` flavor subdivides the top-ads
  carousel into per-card cells (X-axis midpoint-split); within-carousel composition figure
  (Fig.~`cellsplit`); `dd_right` right-rail block shipped as a variance-reduction covariate.
- **Within-carousel rank ordering** (§Inventory). Pooled across carousel sizes and indexed by cell
  rank, click-through declines monotonically 4.3 %→2.0 % (leftmost→fifth cell, Spearman ρ = −1.0
  over 231 clicks; fixation count and dwell ρ = −0.94). Complements the layout-conditioned modal-4
  composition (leftmost 31.7 % vs 25 % uniform, n=142). Source: `nb23_cellsplit_rank`,
  `compute_nb23_cellsplit_rank.py`.

**Corrections carried since v1:** above-fold column → gap-fill values (organic 97.7, image_pack 21.0,
paa 12.2, KP 3.8); population 37,142 → 37,162 (gap-fill, 2,775-trial inventory); organic-denominator
labels disambiguated (22,346 inventory vs 22,354 CSV = the 1 dropped trial); 237 final clicks vs
Table 1's 254 all-event dd_top clicks clarified inline.

**Voice + sourcing pass (this release):**
- dd_top's 99.7 % fixation flagged as partly area/above-fold confounded (read alongside AOI area).
- Layout-drift claim (§Pipeline) sourced and made precise: ~13 px median → ~45 px at page bottom
  (was a flat "13--45 px" band). Provenance: AF `plan-demo-fix.md` / `backlog-live-resources.md`,
  DOM-anchoring commit `c225517`; original SERPs captured on Chrome 110/Windows.
- Cut the hollow-optimism closer ("optimistic about the breadth…"); dried the "This is a feature",
  "kept the draft honest", and inspection/scan/glance register.
- `jayawardena2025ripa2` citation completed and corrected from CrossRef: DOI `10.3390/jemr18060070`,
  published title *Measuring Mental Effort in Real Time Using Pupillometry* (JEMR 18(6), 2025),
  author given-names de-swapped (Gavindya Jayawardena / Yasith Jayawardana).

**arXiv Comments field (paste at upload):** `v3: adds dd_top top-ads carousel cell-split enrichment
(per-card AOIs) with within-carousel rank ordering and a dd_right variance-reduction covariate;
above-fold and population-count corrections; completed RIPA2 citation. No change to the core typing
pipeline or the 38,250-classification consistency check.`

## 2026-06-23 — paper.md deprecated; paper.tex is canonical

`paper.md` is frozen as of the 2026-05-06 acmart-format conversion (commit `ef15946`). Everything since
— ARS-audit cleanup, reviewer-pass fixes, and the `dd_top` cell split (`typed_gapfill_cellsplit`,
within-carousel figure, `dd_right`-as-variance-reduction-covariate framing; commit `51e22a9`) — lives
only in `paper.tex`, the canonical acmart source built via `./build.sh --acmart` and shipped by
`make-arxiv-bundle.sh`. `paper.md` is retained (not deleted) because `./build.sh` (default) and
`./build.sh --anonymous` still consume it via pandoc; a deprecation header now marks it frozen, and
`build.sh` warns at runtime. **Follow-up:** re-base the anonymization pipeline (`docs/anon-checklist.md`,
`./build.sh --anonymous`) onto `paper.tex` before the next double-blind submission — it currently
anonymizes stale content.

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

### Out-of-scope

Downstream model work is scoped out to sibling tracks and surfaces only
as "what's enabled" pointers in §5.
