# TODO — arXiv v4 revision

## 2026-09-07 — v4 draft state

`paper.tex` restructured and rebuilt (8 pp, 0 prose-lint findings); bundle at
`allserp-arxiv.tar.gz`. Item status against §A below:

| item | status |
|---|---|
| 1 ρ = −1.0 restated | done (footnote in §4) |
| 2 cell-layer limitations | done (§5 Coverage table + §3.2) |
| 3 cell-audit denominator | done (29.5 % full-corpus) |
| 4 widget-slot callout | done (§2.2; 353 trials / 352 main-axis / 0 mis-shifted; the "35 strictly between organics" clause dropped, no producer) |
| 4b contamination reframe | done (§2.4; 23.9 → 3.91 % reproduced today) |
| 5 data statement | done (§7.2 substrate identity; harness triple in §3.2; the 92.4/93.3 sample pair stays out of the paper) |
| 6 coordinate ripple | **done for Table 1** via new `allserp_descriptives.py --space screenshot` (AF commit today). 38,250 check re-run 2026-09-05, unchanged. `is_main_axis_click` re-base still queued upstream; paper discloses it. |
| 7 zero-paging paragraph | in (§5); selector-scope re-verification still open, paragraph says so |
| 8 bundle + upload | bundle built; upload pending the title decision below |

Decisions left: keep the title? (kept for citation stability); upload timing
(the downstream citing draft's deadline is in the private note); push of the approach-retreat replay commit
(`b348e2c`, labelled log LF/HF tracks) so the deployed viewer matches Fig. 2.

## Landing checklist before the arXiv v4 upload (surveyed 2026-09-07)

Nothing below is pushed; every step is one command.

1. **attentional-foraging** — `origin/main` is at 2026-06-03, 90 commits behind
   `release/allserp-v1.1.0`, so the paper's GitHub link serves the pre-v1.1.0 substrate
   (`docs/allserp-v1.1.0-migration.md` 404s on main). Local `main` is now fast-forwarded to
   the release branch (it was a clean ancestor). Push both:
   `git push origin release/allserp-v1.1.0 main` (14 commits on the release branch,
   102 files, no blobs > 20 MB; tag `allserp-v1.1.0` already on origin). Tests under
   Homebrew python: carousel 76, fidelity 30, export 3, audit-space 9, all pass.
2. **approach-retreat** — 8 commits ahead of `origin/main` (replay LF/HF tracks, substrate
   stamp, curation disclosure, rebuilt `dist/`). `git push origin main` triggers the Pages
   deploy (`npm ci && npm run build`, 30/30 vitest, verified locally).
3. **allserp-paper** — ahead of origin (v4 draft). Public repo: downstream-paper
   coordination now lives in `notes/private-todo.md` (gitignored), done 2026-09-07.
4. Then re-verify from the outside: the migration-guide URL on main returns 200, the
   deployed replay page for p010-b2-t6 shows the labelled tracks, and `make-arxiv-bundle.sh`
   is re-run if anything in `paper.tex` moves.
5. Optional but citable: a GitHub Release `allserp-v1.1.0` on attentional-foraging with the
   four corpus CSVs attached (latest release there is v0.2.1 from May). Zenodo was timing
   out today; the records URL in the paper is unchanged.

Substrate: `attentional-foraging` at `release/allserp-v1.1.0` post `574218b6`
(typed maps content hash `2cb789eb8febd234`, 2,764 trials, 12 exclusions)
unless noted. Driven by the 2026-08-30 substrate review
(`AF/docs/JOURNEY-2026-08-30.md`, `AF/docs/aoi-fidelity-baseline-2026-08-30.md`,
harness `AF/scripts/aoi_fidelity.py`).

## Full-corpus carousel check — 2026-09-04

[LAB, AdSERP, typed-parent candidate] All **2,776 trials** were measured. After
the existing 12 exclusions, the old source matches **465/1,575 top-parent
counts**; the candidate admits **1,570/1,575 matching subdivisions**, with
**7,265 cards**. The **5 rejected cases** remain unadmitted and stay
in the denominator. Eight additional preselected pages confirm captured card
order for 34 cards; this does not certify SKU identity or merchant destinations.

Sources: AF `docs/methodology/carousel-full-corpus-validation.md`,
`docs/methodology/carousel-source-adoption.md`, and
`docs/evidence/carousel-2026-09-04/corpus/`. The exporter exclusion leak is fixed
and 109 focused tests pass. Released exports and behavioral claims remain unchanged.

Next: resolve single-card validation and the recorded-height scale discrepancy,
then version the top-cell source against the current parent baseline, validate
click attribution, then migrate NB23/NB25 together. Both read snapshots directly;
NB25 also uses old parent boxes and an X-ignoring attribution fallback. A CSV swap
alone is insufficient. Preserve old outputs/K IDs and record new source-specific
populations before updating per-cell claims.

## Carousel candidate improvement — 2026-09-04

Upstream screenshot registration increases candidate count agreement from the
released snapshot's **19/61 to 61/61** on the same fixed comparison cohort
(**279 visible cards**). Every candidate card has original-screenshot border
support; three HTML/screenshot layout shifts are repaired. Six separately selected
spelling-mismatch cases match the reviewer's original-screenshot counts and pass
registration with unchanged thresholds. This is targeted candidate validation,
not a corpus-wide accuracy estimate or semantic identity check.

Source: AF `docs/methodology/carousel-screenshot-registration.md` and
`docs/evidence/carousel-2026-09-04/registration/`. The released cells, behavioral
figures, and paper's legacy-snapshot disclosures remain unchanged until the
versioned-source adoption gate. The current candidate CSV is an audit adapter, not
the released enrichment schema.

## Carousel repair update — 2026-09-04

First implementation slice is complete upstream: corrected count audit plus a
DOM candidate and original-screenshot fixtures. The candidate is **not yet the
released cell source**. Five positive screenshot cases pass; one count-matching
layout mismatch is correctly rejected. Source/commands/gates:
`attentional-foraging/docs/methodology/carousel-dom-candidate.md`.

The old **451/1,551 (29.1%)** and **18/58 (31.0%)** cell-count figures are retired
as fidelity estimates: the old export counter mixed top, organic and right-rail
cells and omitted zero/missing comparisons. The repaired exact retained sample
has **19/61 (31.1%) matching top-parent counts**, **37 short**, **5 over**;
**59/120** trials have no top-carousel comparison. This is count agreement,
not a per-card accuracy rate or a new full-corpus result.

**Superseded for publication 2026-09-05:** the full-corpus check above
(**466/1,582 = 29.5%**, 961 short, 155 over, 1,194 absent, 0 unresolved) is the
figure the paper now quotes — same metric, 26× the denominator, and independently
reproduced by a second corpus run. Keep the 19/61 sample as provenance only.
The v5 cell-result regeneration gate remains open.

## 0 · Critical path

v4 must be live before a downstream paper that cites this resource as its AOI-substrate
authority is submitted; the coordination details are in a private, gitignored note.
Verified 2026-08-31: arXiv v3 (live since Jul 23) still asserts the within-carousel
ρ = −1.0 and describes the pre-collision-fix substrate. Target: **v4 uploaded by end of
September** (announce takes 1–2 days).

**v4 does NOT wait on the DOM-derived cellsplit rebuild** (AF Stage 4, the "real
build"). The restated §results paragraph already discloses the frozen-snapshot
provenance and the DOM-agreement score; full per-cell re-derivation is a v5 item (§B
below). Overridable call — but waiting couples the erratum fix to an unscheduled build.

## A · v4 items (ship by end of September)

1. **[DONE — merged to main 2026-08-31] Restate the within-carousel ρ = −1.0**
   (§Inventory, "Within-carousel composition"). Restated as directional decline
   (4.3 % → 2.0 %, leftmost → fifth), no rank coefficient, inline v3-erratum
   note + audit disclosure. **Do not substitute the −0.900 from the zero-paging
   analysis** — it scored `vplaurlt`/`platop` ids that double-count right-rail
   cells; a documented wrong turn.

2. **[DONE locally — 2026-09-04] Disclose cell-layer limitations**
   The Validation paragraph and Release CSV bullet now distinguish internal
   parent alignment from card-level fidelity and identify the frozen source.

3. **[DONE locally — 2026-09-04] Correct the cell-audit denominator**
   **Updated 2026-09-05:** the results paragraph now uses the **full-corpus**
   466/1,582 (29.5%) comparison, not the retained-sample 19/61 it was first
   drafted against; the evidence pointer moves from `audit-retained120.json` to
   `corpus/comparison.json`. The old 29.1% full-corpus rate remains retired.
   Provenance: AF `docs/evidence/carousel-2026-09-04/`.

4. **Callout: widget blocks are first-class slots in the typed flavor**
   (taxonomy/flavors section). Local packs type as `top_places`, main-axis
   display order: **353/2,776 trials (12.7 %)** contain one; **352 main-axis**.
   `organic_rank` numbers within organics only, so a widget slot never shifts
   organic ranks — and the producer now measures this rather than asserting it
   (`n_mis_shifted: 0`).

   Re-derived 2026-09-05 from `AF scripts/audit_local_pack_aois.py` on the
   shipped substrate (AF `d12f50a4`): `n_trials_with_local_content` **353**.
   **353 was already the committed value in AF's own output sidecar, so the
   draft's 354 is a transcription error, not substrate drift** — the only
   thing the collision fix actually moved here is `aois_below_pack`
   (3,603 → 3,613). `n_typed_top_places_main` **352** (unchanged),
   `n_mis_shifted` **0**, pack location 268 out-of-rso-main / 85 in-rso,
   3,613 AOIs below the pack (mean 10.26). **The "35 strictly between organics"
   figure is not emitted by that script** — find its producer or drop the clause;
   same cite-blocked category as item 4b's 3.91 %. Contrast with `organic` /
   `organic_hybrid` where widgets are not slots — flavor semantics, not a
   coverage gap. Honest caveat: local packs were the hard alignment cases;
   the 12 excluded trials are the pathological-widget pages — quarantined,
   not silently mislabeled.

4b. **Data statement: the conversion reframes gapfill — and the 23 % was
   mostly a coordinate bug.** `typed_gapfill` was invented to mop up a 22.7 %
   contamination of `approached & clicked`. In screenshot space that
   contamination is **3.91 %**, and the bucket collapse says why:

   | bucket | document space | screenshot space |
   |---|--:|--:|
   | `in_column_edge` (bbox-edge near miss) | 510 | **5** |
   | `right_chrome` | 91 | **1** |
   | `dd_right` | 66 | **102** |
   | **contamination rate** | **23.94 %** | **3.91 %** |

   The 510 "bbox-edge near misses" were never near misses. With X unscaled,
   right-rail clicks landed inside the main column's *apparent* X range and
   were classified as geometry failures; converting moves them where they
   always belonged, and dd_right nearly doubles (66 → 102). So the residual
   gapfill legitimately recovers is real inter-result-gap clicks at ~4 %, and
   the headline 23 % was a coordinate-space defect wearing a geometry costume.
   **That is a stronger and more honest claim than "gapfill mops up less than
   we thought"** — write it that way.

   **Prereq DONE (2026-09-05, AF `f926466e`).** `--space {screenshot,document}`
   on all four audits, defaulting to screenshot, with the space printed in a
   banner on every run. Both published figures now reproduce from repo
   scripts, exactly:

   ```
   .venv/bin/python scripts/audit_cascade_contamination.py --space screenshot
   #   contamination rate of 'approached & clicked' pop: 3.91%
   .venv/bin/python scripts/audit_dd_right.py --space screenshot
   #   final clicks landing inside a dd_right rect: 103  (3.71% of final clicks)
   ```

   Thresholds travel with the points (the 162/702 column bounds and `doc_h`
   are document-space constants), and `scripts/test_audit_space.py` carries a
   fixture the flag must trip. Quote these commands beside the numbers — the
   convention item 5 should adopt too.

5. **Data statement: collision fix + substrate re-pin.** Document the
   2026-08-30 aoi-card-collision fix (two-phase DOM-node claiming in
   `measure_card_geometry`; collisions 454 → 0, orphaned main-column trials
   17.3 % → 6.0 %, 454 typed maps changed per flavor). Re-pin identity: hash
   `2cb789eb8febd234`, exclusion list **12** trials (membership changed from
   the 14-trial list — consumers must re-read). Point at the harness triple
   **on the full corpus** (click 87.7 % = 2,433/2,775; AOI IoU≥0.5 90.8 % =
   2,520/2,776; cell count agreement 29.5 % = 466/1,582, with its separate
   denominator) as the standing quality measurement.

   **Do not publish the 92.4 % / 93.3 % pair** — verified 2026-09-05, those are
   the 120-trial retained sample (110/119 and 112/120), reproduced to the digit,
   and they run ~2.5 pp optimistic against the corpus. The baseline doc's
   93.4 % (2,593/2,776) is full-corpus but **pre-collision-fix**; the shipped
   substrate now measures 90.8 %. The 73-trial gap is not explained — no
   full-corpus 08-30 JSON survives to diff against, only the doc's prose — so
   disclose it, do not attribute it. Confirmed NOT a harness artifact: the
   committed harness (`AF 86b7a44e`) and the current working copy return
   identical click and AOI figures; the working copy's uncommitted changes
   touch only the cell check. That same committed harness reproduces the
   retired 451/1,551 = 29.1 % exactly, which independently validates retiring it.

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
   Recheck its selector scope and denominator before using it to define exposure
   for the DOM-derived cellsplit; snapshot visibility alone does not establish paging history. One paragraph if it fits.

8. **Bundle + upload.** `make-arxiv-bundle.sh` (AppleDouble fix `6798895`
   in). CHANGELOG v3 → v4 change-note mirroring the v3 entry. Comments field
   draft: `v4: restates the within-carousel click decline as directional
   (v3's ρ = −1.0 does not survive a 2026-08-30 substrate audit; cell-layer
   DOM agreement reported); documents the aoi-card-collision fix and re-pins
   the substrate identity (2,764 trials, 12 alignment exclusions); adds
   widget-slot semantics callout for the typed flavor.` After announce:
   downstream citing drafts pin v4 (see the private note).

## B · v5 — after AF Stage 4 (DOM-derived cellsplit producer)

**Re-derive all per-cell numbers from DOM-derived cells.** Every cellsplit
number (31.7 % leftmost share, 4.3 %/2.0 % endpoints, ρ = −0.94 fixation/dwell
gradients, Fig. cellsplit both panels) comes from the frozen 2026-05-24
snapshot with no in-repo producer. The corrected full-corpus count diagnostic is now complete (see above).
When AF adopts the versioned DOM-derived source and resolves the NB23/NB25
coordinate, parent-lineage and denominator requirements: regenerate `nb23_cellsplit_rank` / `nb25_cellsplit_composition`,
re-render the figure, re-run the numbers.

## Standing cautions

- **Resolved 2026-08-31:** the NB26/NB30 reversal annotations and regenerated
  `notebook-key-claims.md` were reviewed and committed (AF `ceb95cb0`), with
  a propagation warning — the K27/K29 tables still carry May values; quote
  the 2026-08-30/31 producer outputs, not the tables, until re-transcribed.
- `allserp-arxiv/` at the repo root is the extracted **v3** bundle (Jul 10),
  now stale vs `paper.tex` — gitignored; don't source anything from it.
