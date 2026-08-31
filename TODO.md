# TODO — arXiv v4 revision

Substrate: `attentional-foraging` at `release/allserp-v1.1.0` post `574218b6`
(typed maps content hash `2cb789eb8febd234`, 2,764 trials, 12 exclusions)
unless noted. Driven by the 2026-08-30 substrate review
(`AF/docs/JOURNEY-2026-08-30.md`, `AF/docs/aoi-fidelity-baseline-2026-08-30.md`,
harness `AF/scripts/aoi_fidelity.py`).

## 0 · CRITICAL PATH — v4 live before the CHIIR submission

Verified 2026-08-31: **arXiv v3 (live since Jul 23) still asserts the
within-carousel ρ = −1.0** and describes the pre-collision-fix substrate.
The Leaky Cursor CHIIR 2027 resubmission (abstract **Oct 8**, paper **Oct 15**)
cites this paper third-person as the AOI-substrate authority and quotes v1.1.0
numbers — a reviewer who reads the cited resource finds a known-bad claim or
mismatched counts. Target: **v4 uploaded by end of September** (announce takes
1–2 days; the Oct 8 abstract should cite v4).

**v4 does NOT wait on the DOM-derived cellsplit rebuild** (AF Stage 4, the
"real build", to be scoped with Sara). The restated §results paragraph already
discloses the frozen-snapshot provenance and the DOM-agreement score; full
per-cell re-derivation is a v5 item (§B below). Overridable call — but waiting
couples the erratum fix to an unscheduled build.

## A · v4 items (ship by end of September)

1. **[DONE — merged to main 2026-08-31] Restate the within-carousel ρ = −1.0**
   (§Inventory, "Within-carousel composition"). Restated as directional decline
   (4.3 % → 2.0 %, leftmost → fifth), no rank coefficient, inline v3-erratum
   note + audit disclosure. **Do not substitute the −0.900 from the zero-paging
   analysis** — it scored `vplaurlt`/`platop` ids that double-count right-rail
   cells; a documented wrong turn.

2. **Disclose cell-layer fidelity where "100 % aligned" appears**
   (§Validation "Top-ads cell subdivision" ¶; `typed_gapfill_cellsplit` CSV
   bullet in §Release). Those claims are internal consistency against the
   block bbox, not DOM fidelity. Add the DOM-agreement number and
   frozen-snapshot provenance so the two aren't conflated.

3. **Name the denominator on every cell-agreement figure.** Two true numbers
   in play: **29.1 % (451/1,551 comparable trials, full corpus)** — use for
   the §results erratum and item 2 — and **31.0 % (120-trial fidelity-harness
   sample)** — item 5's harness triple. Same site must never mix them
   unlabeled; verify both against `aoi_fidelity.py` output before bundling.

4. **Callout: widget blocks are first-class slots in the typed flavor**
   (taxonomy/flavors section). Local packs type as `top_places`, main-axis
   display order: 354/2,776 trials (12.8 %) contain one; 352 main-axis; 35
   strictly between organics. `organic_rank` numbers within organics only, so
   a widget slot never shifts organic ranks. Contrast with `organic` /
   `organic_hybrid` where widgets are not slots — flavor semantics, not a
   coverage gap. Honest caveat: local packs were the hard alignment cases;
   the 12 excluded trials are the pathological-widget pages — quarantined,
   not silently mislabeled.

5. **Data statement: collision fix + substrate re-pin.** Document the
   2026-08-30 aoi-card-collision fix (two-phase DOM-node claiming in
   `measure_card_geometry`; collisions 454 → 0, orphaned main-column trials
   17.3 % → 6.0 %, 454 typed maps changed per flavor). Re-pin identity: hash
   `2cb789eb8febd234`, exclusion list **12** trials (membership changed from
   the 14-trial list — consumers must re-read). Point at the harness triple
   (click 92.4 % / AOI IoU≥0.5 93.3 % / cell 31.0 %, 120-trial sample) as the
   standing quality measurement.

6. **Coordinate-space ripple into click attribution — verify precondition,
   then re-derive.** evtrack records document space (1403 px), AOIs screenshot
   space (1280 px); conversion moves click-in-AOI containment 78.0 % → 96.2 %.
   Precondition: AF's `fix/coordinate-space-loader` + `fix/wire-cursor-conversion`
   merged (AF `95759f29` looks like the merge — **confirm**, don't assume).
   Then re-derive Table 1, the 91.7 % X+Y attribution figure, and re-run the
   38,250 ad-classification check. Fixation→AOI attribution never affected;
   gaze-anchored numbers stand.

7. **Optional: zero-paging paragraph.** 1,582 carousels, 272 cell clicks,
   zero clicks on a card not already on screen (27 DOM cells, ~5 visible).
   Settles the visible-cells definitional question for the DOM-derived
   cellsplit. One paragraph if it fits.

8. **Bundle + upload.** `make-arxiv-bundle.sh` (AppleDouble fix `6798895`
   in). CHANGELOG v3 → v4 change-note mirroring the v3 entry. Comments field
   draft: `v4: restates the within-carousel click decline as directional
   (v3's ρ = −1.0 does not survive a 2026-08-30 substrate audit; cell-layer
   DOM agreement reported); documents the aoi-card-collision fix and re-pins
   the substrate identity (2,764 trials, 12 alignment exclusions); adds
   widget-slot semantics callout for the typed flavor.` After announce:
   downstream citing drafts (Leaky Cursor CHIIR revision) pin v4.

## B · v5 — after AF Stage 4 (DOM-derived cellsplit producer)

**Re-derive all per-cell numbers from DOM-derived cells.** Every cellsplit
number (31.7 % leftmost share, 4.3 %/2.0 % endpoints, ρ = −0.94 fixation/dwell
gradients, Fig. cellsplit both panels) comes from the frozen 2026-05-24
snapshot with no in-repo producer; export short on 902/1,551 carousels,
median shortfall exactly 1 cell (trailing-drop). When AF ships the DOM-derived
producer: regenerate `nb23_cellsplit_rank` / `nb25_cellsplit_composition`,
re-render the figure, re-run the numbers.

## Standing cautions

- **AF has deliberately uncommitted state pending Andy's review** (NB26 / NB30
  reversal-bearing notebooks + regenerated `notebook-key-claims.md`, as of
  2026-08-31). Any number quoted from key-claims for v4 must come from the
  reviewed/committed state, not the working tree.
- `allserp-arxiv/` at the repo root is the extracted **v3** bundle (Jul 10),
  now stale vs `paper.tex` — gitignored; don't source anything from it.
