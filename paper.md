# AllSERP: A Typed AOI and Per-Element Behavioral Enrichment of the AdSERP Dataset

**Status:** Working draft, 2026-05-05. Markdown-first; LaTeX conversion deferred until content is stable.
**Target venue:** SIGIR 2026 Resource Paper track (primary).
**Tag:** `[LAB, AdSERP, typed_gapfill, AllSERP-resource-paper-draft-v0]`

---

## Abstract

[CITE: AdSERP-original] released a multimodal SERP eye+cursor dataset with 2,776 commercial-intent trials across 47 participants, simultaneous 150 Hz gaze, mouse telemetry, scroll, pupil, full-page screenshots, and ad bounding boxes. The dataset shipped without per-element typing or per-element bounding boxes for organic results, widgets, or any non-ad SERP surface — leaving downstream consumers to either pool ads with organics under absolute rank or build their own AOI extractor.

This paper contributes (1) a screenshot-anchored AOI extraction pipeline that recovers pixel-accurate organic and widget bounding boxes via CV row-projection on the original screenshots, with HTML-derived structural labels joined onto the bbox geometry; (2) a `typed_gapfill` flavor that fills inter-result Y gaps via midpoint-split, raising honest click attribution from 75.1 % to 91.7 % of corpus-wide final clicks; (3) validation against shipped ad rectangles with 0 disagreements across 38,250 classifications (F1 = 1.000); (4) a refutation of a coordinate-space calibration-bias hypothesis using shipped ad rectangles as alignment ground truth; and (5) descriptive observed-behavior tables for nine SERP element types (organic, dd_top, native_ad, paa, image_pack, knowledge_panel, top_places, unknown_widget, other_widget) including click share, fixation coverage, regression rate, and above-fold incidence.

The pipeline is released as a single-script public API. The paper does not propose new models; it documents what the enriched dataset enables, and points to sibling work that uses the enrichment for click prediction [CITE: cikm-paper], cognitive task modeling [CITE: chi-task-model-paper], and pupillometric cognitive load analysis [CITE: ettac-paper].

---

## §1. Introduction

The AdSERP dataset [CITE: AdSERP-original] occupies a distinctive position in the multimodal IR resource landscape: simultaneous eye gaze, cursor, scroll, pupil, and click telemetry against ground-truth screenshots, on real Google search-result pages with realistic commercial-intent task framing. The 2,776-trial corpus is large enough for cross-participant LOSO validation and small enough that per-trial visual inspection is tractable.

But the shipped data leaves three structural gaps for any per-element analysis:

1. **No organic-result bounding boxes.** Ad rectangles ship with the dataset; organic-result rectangles do not. Consumers either estimate from h3 heading counts (assuming uniform result heights, which the actual layout violates by 80–320 px per result), or pool ads with organics under "absolute rank" (mixing surfaces with very different click policies).

2. **No semantic typing of results.** A "rank-1 result" might be a top-of-page ad, a knowledge panel, an image pack, an organic result, or a People-Also-Ask widget. Each receives a different click rate and triggers different cognitive operations. Per-rank claims that don't disambiguate are uninterpretable.

3. **No carousel / composite subdivision.** Top-stories carousels, image packs, and product-list ads ship as single-rectangle parents; the per-product cells inside them are not enumerated, blocking per-cell click and fixation attribution.

This paper releases a pipeline that recovers all three: pixel-accurate organic and widget bounding boxes from CV row-projection on the screenshots, HTML-anchored semantic labels via spatial join, and per-cell carousel subdivision via vertical-edge peak detection. We validate the ad-vs-non-ad partition against the shipped ad rectangles (0 disagreements across 38,250 classifications) and report descriptive observed-behavior tables for the nine main-axis element types the pipeline produces.

A 2026-05-05 audit revealed that the legacy click-attribution helper used in pre-existing work on this dataset (Y-band-only assignment with no X check) silently mis-attributes 22.7 % of approached-and-clicked records — right-rail dd_right ad clicks, page-chrome clicks, and far-off-target clicks rolled into adjacent organic positions sharing their Y coordinate. This paper introduces the `typed_gapfill` flavor: midpoint-split bbox extension plus X+Y bbox-aware click attribution plus a trial-level filter that drops trials with off-axis final clicks. The result is honest 91.7 % click attribution (vs 75.1 % under tight typed bboxes), with the 8.3 % residue flagged at trial level rather than silently mis-attributed.

The pipeline is not principled. The midpoint-split is a heuristic choice for inter-result boundaries, not a DOM-derived ground truth — re-rendering the saved 2022 SERP HTML in 2026 produces 13–45 px layout drift due to font, CSS, and external-asset changes [CITE: plan-demo-fix-doc], and the original screenshots therefore remain the single truth source for geometry. We document the heuristic explicitly, ship both legacy `typed` and new `typed_gapfill` outputs side-by-side, and name DOM-anchored extraction as future work blocked on the same lossiness ceiling.

### Contributions

1. **Screenshot-anchored typed AOI extraction** with per-trial JSON output covering organic, dd_top, native_ad, dd_right, top_places, knowledge_panel, paa, image_pack, related_searches, pagination, other_widget, unknown_widget, and chrome surfaces.

2. **`typed_gapfill` flavor** — pragmatic post-processing that fills inter-result Y gaps via midpoint-split, plus X+Y bbox-aware click attribution, plus an `is_main_axis_click()` trial filter.

3. **Validation against shipped ground truth** — 38,250 ad-classification comparisons, 0 disagreements, F1 = 1.000 on Phase C ad propagation, mean IoU = 1.000.

4. **Refutation of a corpus-wide calibration-bias hypothesis** using shipped ad rectangles as alignment ground truth — clicks bias downward (within bbox), fixations bias upward (opposite directions), confirming the data is screenshot-aligned and the apparent click drift reflects normal "click target ≠ visual fixation target" user behavior.

5. **Descriptive observed-behavior inventory** for nine element types: click share, fixation coverage, regression rate, above-fold incidence, on the full 2,776-trial corpus.

6. **Public API and reproducible artifacts.** Single-script entry point (`scripts/build_aois.py`) wrapping the four-phase pipeline. Five cite-ready audit producers covering the cascade. K-bbox-y-* numbered claim references in the upstream notebook key-claims aggregator [CITE: af-notebook-key-claims].

---

## §2. Method: Typed AOI Extraction

### 2.1 Why screenshot-anchored

The fixation and cursor streams in [CITE: AdSERP-original] were recorded in pixel coordinates against the original full-page screenshots. Re-rendering the saved HTML in a 2026 browser produces 13–45 px layout drift relative to the original Chrome 110 / Windows session that captured the screenshots [ATTRIBUTE: plan-demo-fix-doc: residual median <13 px, max ~45 px at page bottom from re-rendered SERP HTML]. Therefore: the screenshots are the truth source for geometry. HTML is used only for structural labels (semantic typing of cards) and for the spatial join, never for geometry directly.

This is the empirical refutation of the obvious DOM-anchored alternative. Any pipeline that derives bbox geometry from re-rendering the HTML will introduce 13–45 px error against the original screenshot truth. We choose the methodologically pragmatic path and anchor geometry to the screenshots via CV.

### 2.2 Phase A — CV row-projection

For each trial's full-page screenshot, slice the main column (X ∈ [162, 748]; this range is constant across the corpus, derived from the layout of the rendered SERP). Compute per-row pixel std of the grayscale slice; threshold at `ROW_STD_THRESHOLD = 3` to identify content-bearing rows. Merge runs separated by < `GAP_MERGE = 24` px (within-card text-line gaps). Filter merged runs shorter than `MIN_CARD_H = 50` px. The output is a list of `(y_top, y_bottom)` tuples, one per detected card.

Cards are then filtered against the shipped ad rectangles via `is_ad`: a card is rejected if it overlaps any ad rectangle ≥ 50 % in Y *and* the ad's X range intersects the main column. The X check is essential — without it, tall right-rail dd_right ads silently mark main-column cards as ads whenever their Y spans coincide.

A widget y-floor heuristic drops bottom-of-page refinement widgets (Related Searches, People Also Ask). The floor is the smaller of (a) HTML walk to find widget-heading h3 elements + band-y backstop, and (b) a layout-aware floor at the y of the first card after the largest anomalous inter-card whitespace gap (anomalous = > 3× median gap AND > 150 px). Either signal alone is fragile; combining them with a 60 %-of-band-y plausibility constraint provides robustness.

Composite-widget sub-segmentation handles top-stories, image packs, and PAA blocks that emerge from the row-projection as a single tall card. Cards taller than `COMPOSITE_TRIGGER_H = 320` px are subdivided via row-projection inside the parent. Top-of-column ad carousels (dd_top) are subdivided horizontally via vertical-edge peak detection on `|dx|` column-summed across bbox rows.

Phase A output is per-trial JSON at `AdSERP/data/organic-boundary-data/{tid}.json`, schema-additive to the v1 ad-boundary JSON: top-level keys for shipped ad data pass through unchanged; new keys (`organic_result`, `widget`, `organic_cell`, `dd_top_cell`, `dd_right_cell`, `_meta`) are added without restructuring v1 fields.

### 2.3 Phase B — HTML widget typing

We parse the saved SERP HTML with BeautifulSoup and walk the main result container (`#rso`, with descent into "Main results" wrappers identified by the `ULSxyf` class), the bottom-of-page container (`#botstuff`), and the right-rail container (`#rhs`). For each card, an 8-tier priority chain returns a `(type_label, signature)` tuple:

1. **Heading text** — h3/h2/role=heading text matched against widget-name patterns (highest priority because Google's heading text is the most stable label channel).
2. **Structural descendants** — child elements with known class signatures (e.g., `g-section-with-header[data-attrid="paa"]` → paa).
3. **`data-attrid`** — knowledge-card namespace (`kc:/...`) labels.
4. **Class markers** — recognizable widget classes (e.g., `b9bzG` for image packs).
5. **`ULSxyf` with image descendant → image_pack; otherwise other_widget**.
6. **Sectioned widget** — `g-section-with-header` without recognizable subtype.
7. **Class-based organic** — recognized organic-card classes (e.g., `MjjYud`, `Z0LcW`).
8. **Structural organic** — heading + outbound link as a fallback.

Cards that fail all eight tiers are labeled `unknown_widget` with `position = -1`. The full taxonomy: `organic`, `dd_top`, `native_ad`, `dd_right`, `top_places`, `knowledge_panel`, `paa`, `image_pack`, `related_searches`, `pagination`, `other_widget`, `unknown_widget`, `chrome`.

### 2.4 Phase C — Spatial join

The spatial join attaches Phase B labels to Phase A geometry by document order. For each Phase A bbox in y-order, check overlap (≥ 30 % asymmetric) with shipped ad rectangles; if overlap, the bbox IS that ad (label propagated from the shipped ad type). Non-ad bboxes are matched in y-order to HTML #rso cards in DOM order. Off-axis cards (`#botstuff` items, `#rhs` items, `dd_right`, deep short cv-only entries swept to `chrome`) get `position = -1`.

Document order is the only stable axis. A spatial-only HTML↔bbox match (nearest-y, IoU) requires both to live in the same coordinate space, which they don't — HTML has no rendered geometry and re-rendering loses 13–45 px (§2.1).

### 2.5 Phase D — Midpoint-split gap-fill (`organic_gapfill` / `typed_gapfill`)

Phase A bboxes are tight on visible text via row-projection. In practice, real clicks and fixations land in the inter-result Y gap (typically 5–60 px between adjacent organic results) where users target link padding or where the result-row content extends beyond the visible-text bounds the row-projection captured. Under tight bboxes, those signals are dropped from per-AOI attribution.

Phase D divides each inter-result gap at its midpoint. For sorted organic bboxes, each adjacent pair `(o[i], o[i+1])` has gap `g = o[i+1].top - o[i].bottom`; if `g > 0`, the midpoint is `o[i].bottom + g // 2`, and `o[i].bottom` extends to (midpoint − 1) while `o[i+1].top` extends to (midpoint + 1). Splits are clamped where ad/widget rectangles sit between adjacent organics, so an organic never extends across an ad. The very first organic's top and the very last organic's bottom are not extended (they would otherwise consume page chrome / pagination).

Phase D is **pragmatic, not principled**. The midpoint heuristic is not the correct boundary between two adjacent results — that boundary is a DOM/CSS question we do not solve. The midpoint is a defensible, reproducible choice that recovers signal previously dropped from per-AOI attribution. Both legacy `typed` (Phase A → C) and new `typed_gapfill` (Phase A → D) flavors stay queryable side-by-side for any K-claim that needs the cleaner-attribution version vs the historical version.

### 2.6 X+Y bbox-aware click attribution

Under `typed_gapfill`, click attribution requires X *and* Y containment in a main-axis AOI bbox. The rule, with pass-1 strict + pass-2 tolerance fallback:

```
attribute_click_to_typed_gapfill(click_x, click_y, trial_id, x_tol=5, y_tol=10):
  Pass 1: if any AOI bbox strictly contains (click_x, click_y),
          return the smallest-area such AOI.
  Pass 2: inflate each AOI by ±x_tol X / ±y_tol Y; pick smallest-area
          AOI whose inflated bbox contains the click.
```

Default tolerance is ±5 X / ±10 Y to capture link-padding clicks that fall just outside the row-projection bbox; most inter-result gaps are absorbed by Phase D itself, so the tolerance is small.

The legacy `click_to_position` helper in the pre-existing codebase did Y-bisect against AOI tops with no X check, silently rolling off-axis clicks into main-axis AOIs sharing their Y. The X+Y bbox-aware rule is the core fix for the 22.7 % silent contamination documented in §3.

### 2.7 Hard-error trial filter

`is_main_axis_click(trial_id)` returns True iff the trial's final click attributes to a main-axis AOI under the rule above. Producers that compute click-outcome features (cursor approach, click-prediction LOSO classifiers) drop trials where this returns False. In the AdSERP corpus, 231 trials are filtered: 67 dd_right (right-rail ad clicks), 91 right_chrome (page-chrome / search-tools / far-off-target), and ~73 trials with no clicks recorded or pathological click coordinates. These trials are not silently mis-attributed; they are flagged at trial level.

### 2.8 Public API

Single-script entry point `scripts/build_aois.py` wraps the four-phase pipeline:

```bash
.venv/bin/python scripts/build_aois.py --all                 # default flavor: typed_gapfill
.venv/bin/python scripts/build_aois.py --trial p005-b2-t2   # single trial
.venv/bin/python scripts/build_aois.py --all --skip-extract  # use cached organic bboxes
```

Output: `AdSERP/data/organic-boundary-data-gapfill/`, `data/aoi-typed-gapfill/`, and the corpus CSV at `scripts/output/adserp_aois_by_trial_id_typed_gapfill.csv` (37,142 rows × 2,776 trials).

---

## §3. Validation against shipped ground truth

[ATTRIBUTE: af-validation-typed-vs-shipped-ads: 0 disagreements across 38,250 classifications on 2,776 trials; F1 = 1.000 on Phase C ad propagation; mean IoU = 1.000]

The shipped ad rectangles in [CITE: AdSERP-original] provide a labeled gold standard for the ad / non-ad partition. Phase C ad propagation matches the shipped gold with **F1 = 1.000** across all three ad etypes (`dd_top`, `native_ad`, `dd_right`); 0 / 26,590 Phase A `organic_result` bboxes overlap any shipped ad, confirming Phase A ad-subtraction is clean; mean IoU = 1.000 between matched Phase C bboxes and shipped rectangles. There are no cross-type misclassifications.

The deeper non-ad partition (organic vs widget vs paa vs image_pack vs knowledge_panel vs top_places) lacks an external gold and is validated against the HTML structure (Phase B's 8-tier chain) plus visual spot-check on representative trials. We do not claim F1 = 1 on the deeper partition; we document the validation asymmetry honestly. Replay-set visual proof at [CITE: ar-replay-viewer-url].

### 3.1 Screenshot-alignment audit

The ad-rectangle ground truth additionally enables an independent test of whether the gaze and cursor streams themselves are screenshot-aligned. For each trial's final click and longest-fixation, we compute signed Y-distance to the nearest shipped ad-rect edge (negative = inside, positive = outside).

| stream | inside ad rect | median signed Y | near-edge ratio (inside : outside in [-50, +50] px) |
|---|---:|---|---|
| final clicks | 442 | −84 px | 152 : 39 (~4:1) |
| longest fixation/trial | 771 | −87 px | 393 : 179 (~2:1) |

A coordinate-space Y-drift would produce accumulation just-outside ad edges (clicks at signed Y = +N px where they should be inside). We see the opposite: deep median inside ads, near-edge ratios strongly favoring inside. The gaze and cursor streams are screenshot-aligned. This refutes a corpus-wide click-Y calibration bias hypothesis that arose from a small-sample visual inspection of replay trials.

[Detailed audit script: `attentional-foraging/scripts/audit_screenshot_alignment.py`. Regime tag: `[LAB, AdSERP, alignment-audit-2026-05-05]`.]

### 3.2 Click-vs-fixation directional asymmetry

Within typed bboxes (where users clicked or fixated on a result), clicks are biased slightly downward of bbox center (median +12.5 px below center; IQR −21 to +40) while fixations are biased slightly upward (median normalized position 0.440 in the [0=top, 1=bottom] range; 66.5 % of unattributed fixations are above bbox top vs only 33.5 % below). The opposite-direction bias is consistent with normal user behavior: people **look** at the title text (top of card) and **click** the link target (center / slightly below the title baseline). It is not a coordinate-space bug.

This dissociation, taken together with §3.1, refutes a class of calibration-drift hypotheses that would otherwise motivate corrective offset-adjustment of the gaze/cursor streams. No correction is applied; the streams are kept as-shipped.

---

## §4. Element-Type Inventory and Observed Behavior

Population: 2,775 trials processed (1 trial dropped: missing meta or fixations); 37,142 typed AOI rows under the `typed_gapfill` flavor.

### 4.1 Counts and fixation coverage

| etype | n_aois | % fixated ≥ once |
|---|---:|---:|
| organic | 22,346 | 55.6 % |
| native_ad | 9,214 | 36.4 % |
| image_pack | 1,584 | 52.0 % |
| dd_top | 1,582 | **99.7 %** |
| paa | 769 | 40.6 % |
| unknown_widget | 788 | 17.4 % |
| knowledge_panel | 745 | 48.6 % |
| top_places | 84 | 54.8 % |
| other_widget | 50 | 58.0 % |

**Read.** dd_top reaches near-universal fixation — every top-of-page ad in the corpus receives at least one fixation, consistent with users foveating the top of the page at trial onset. Native_ad fixation rate is 36 % — most native ads slot below the first organic and many never get fixated. Organic AOIs sit at 56 %, reflecting users typically sampling 5–6 of 10 results before committing.

### 4.2 Click distribution

2,634 clicks attributed to typed_gapfill AOIs (89 % of trial-clicks):

| etype | n_clicks | click-share % |
|---|---:|---:|
| organic | 2,084 | 79.1 % |
| dd_top | 254 | 9.6 % |
| native_ad | 156 | 5.9 % |
| image_pack | 55 | 2.1 % |
| paa | 44 | 1.7 % |
| knowledge_panel | 31 | 1.2 % |
| unknown_widget | 7 | 0.3 % |
| other_widget | 2 | 0.1 % |
| top_places | 1 | 0.0 % |

**Read.** Organic results capture 79 % of clicks; ads 15.5 %; widgets 5.4 %. The original AdSERP non-ad-click headline [CITE: AdSERP-original] survives at finer resolution: dd_top has near-universal fixation (99.7 %) but only 9.6 % of clicks — the click-fixation dissociation is preserved at element-type granularity.

### 4.3 Regressive share

A fixation is **regressive** if it lands on an AOI of rank R where R was previously fixated and R < max_seen (the highest rank ever reached in the trial). For each etype, regressive share is the fraction of fixated AOIs that received at least one regressive fixation.

| etype | regressive-share of fixated | distinct-return-share of fixated |
|---|---:|---:|
| dd_top | 83.4 % | 82.5 % |
| organic | 57.8 % | 54.7 % |
| image_pack | 59.3 % | 57.2 % |
| native_ad | 46.9 % | 42.5 % |
| top_places | 50.0 % | 45.7 % |
| knowledge_panel | 44.5 % | 41.2 % |
| other_widget | 44.8 % | 44.8 % |
| paa | 45.8 % | 42.3 % |
| unknown_widget | 26.3 % | 25.5 % |

**Read.** dd_top has the highest regressive share (83.4 %). Position confound: dd_top is the highest-ranked element, so by construction any return to dd_top after the gaze advances past it is regressive. The headline is the *behavior*: users return to dd_top after looking past it on 83 % of trials where dd_top is fixated, despite a click rate of 9.6 %. Pattern is consistent with attention capture without commitment.

### 4.4 Above-fold incidence

Initial viewport: scroll = 0, height = `screen_height` (typically 1024 px). An AOI is above the initial fold if its `top_y` < `screen_height`.

| etype | trials with ≥1 of this etype above fold | % of trials |
|---|---:|---:|
| organic | 2,700 | 97.3 % |
| dd_top | 1,581 | 57.0 % |
| native_ad | 1,049 | 37.8 % |
| image_pack | 568 | 20.5 % |
| paa | 314 | 11.3 % |
| knowledge_panel | 97 | 3.5 % |
| top_places | 58 | 2.1 % |
| other_widget | 31 | 1.1 % |
| unknown_widget | 0 | 0.0 % |

**Read.** Organic results occupy the initial viewport on 97 % of trials. dd_top is above fold on 57 % of trials (when present, dd_top is by construction at the top, but the corpus contains trials with no dd_top). Knowledge panels and PAA widgets are predominantly below-fold (3.5 % and 11.3 %). Any analysis that conditions on above-fold exposure must stratify by element type — pooling averages out the dominant geometric reality.

### 4.5 Four-class taxonomy preview (for sibling work)

The four-class behavioral taxonomy — **clicked** (was_clicked = True), **deferred** (approached non-click with gaze regression), **evaluated-rejected** (approached non-click without regression), **not-approached** (cursor `min_dist ≥ 100`) — is robust under the cascade. Class proportions invariant within ±0.3 pp across legacy `typed` vs `typed_gapfill`:

| class | typed_gapfill | typed (legacy) |
|---|---:|---:|
| clicked | 13.0 % | 13.1 % |
| deferred | 13.3 % | 13.0 % |
| evaluated-rejected | 2.9 % | 2.9 % |
| not-approached | 70.8 % | 71.0 % |

The full per-etype × class breakdown is reported in [CITE: af-notebook-key-claims], NB22 K-bbox-y-* rows. **Do not interpret the taxonomy as graded relevance here** — that interpretation belongs to the sibling CIKM track [CITE: cikm-paper].

---

## §5. Data Enablement (what's now possible)

The original AdSERP dataset shipped raw multimodal signals plus ad bboxes. Per-element analysis was therefore limited to dd_top / native_ad vs everything-else. Under `typed_gapfill`, the following analyses become tractable on the existing 2,776-trial corpus without re-collecting data:

1. **Per-widget click rates, fixation densities, and regression rates** (the four tables in §4).
2. **Per-etype cursor-approach features** — `cursor-approach-features-typed-gapfill.json` ships per-trial × per-AOI cursor approach metrics with element-type tags.
3. **Per-etype pupil and LF/HF analyses** — `butterworth-lfhf-by-position-typed.json`, `k-coefficient-by-position-typed.json` already exist under typed; gapfill recomputation is straightforward.
4. **Per-etype above-fold-conditioned analyses**, removing the geometric confound that pooled-rank pooled-etype analyses previously absorbed.
5. **Per-trial AOI-level export** — `adserp_aois_by_trial_id_typed_gapfill.csv` (37,142 rows) for downstream replay/audit work and cross-lab sharing.

### Sibling tracks (where the enrichment is consumed)

- **Click prediction with the 9-feature M4 cursor-approach vector reaches LOSO AUC 0.856 under typed_gapfill** [CITE: cikm-paper]. The four-class taxonomy is used as a graded-relevance label generator for LambdaMART / LambdaRank ranking work; that line of work is the CIKM track and is not duplicated here.
- **Cognitive task model (OSEC: Orient → Survey → Evaluate → Commit) at saccade-level granularity** [CITE: chi-task-model-paper]. Per-element phase transitions and per-element rational-analysis foraging dynamics are the CHI 2027 track.
- **Pupillometric cognitive load** (Butterworth LF/HF) per element type [CITE: ettac-paper]. The position gradient holds under typed; per-element decomposition is the ETTAC 2026 track.
- **Per-fixation arousal (RIPA2)** validated against AdSERP gaze data [CITE: ripa-pub]. Standalone Gavindya/team track.

The AllSERP enrichment is the substrate for these papers. We do not replicate their findings; we point to the cite-ready upstream artifacts.

---

## §6. Limitations and Public Release

### 6.1 What the pipeline does not solve

- **DOM-anchored geometry.** A first-principles screenshot-replacing pipeline would extract bboxes from re-rendered HTML's `getBoundingClientRect`. We documented (§2.1) that this loses 13–45 px to layout drift; the practical implication is that the screenshots remain the single truth source, and any DOM-anchored future work must still validate against them.
- **dd_right and right-rail blind spot.** The pipeline tracks dd_right ad rectangles for off-axis classification but does not attempt to recover right-rail organic-style results. The shipped dd_right rectangles also appear incomplete: visual inspection of the 147-trial replay set surfaced one trial (`p041-b5-t2`) with a clear right-rail click whose target had no shipped dd_right rectangle. The right-rail blind spot affects ~1 % of trials.
- **Composite-widget cell labels.** Phase A subdivides composite widgets (top_stories, image_pack, paa) into per-cell rectangles via row-projection or vertical-edge peak detection. These cells receive geometry but not Phase B labels — the inner content of, say, an image_pack is not typed. Per-cell behavioral analysis would require additional HTML parsing per widget subtype.

### 6.2 Anti-bot DOM mutation

Saved Google SERP HTML often contains JS that detects headless renderers and rewrites the page. Phase B parses static HTML only and does not execute JS, sidestepping this. Phase A operates on the original screenshots only; it has no exposure.

### 6.3 Public release

- **Code:** `attentional-foraging` repository (`bbox-y-coverage-fix` merge), `approach-retreat` repository (`bbox-y-coverage-fix` merge). MIT license. Single-script entry point `scripts/build_aois.py`.
- **Derived data:** per-trial typed_gapfill JSONs + corpus CSV in the upstream output paths. ~19 MB compressed.
- **Replay viewer:** [CITE: ar-replay-viewer-url] renders typed AOIs as colored overlay rectangles on the source SERP screenshots — visual proof of the pipeline's output for the curated 147-trial replay set.
- **Audit producers:** five cite-ready scripts (`audit_unattributed_clicks.py`, `audit_dd_right.py`, `audit_cascade_contamination.py`, `audit_calibration_bias.py`, `audit_screenshot_alignment.py`) covering the cascade documented in this paper.
- **K-bbox-y-* claim references:** [CITE: af-notebook-key-claims] holds the per-notebook claim numbers under typed_gapfill, side-by-side with legacy K-bbox-* under typed.

---

## §7. Conclusion

The AdSERP dataset is rich enough to underwrite a multi-paper analytical arc, but the shipped data omits per-element geometry and typing — gaps that block per-element analysis without significant reanalysis effort. AllSERP releases the pipeline that closes those gaps: screenshot-anchored bbox extraction, HTML-derived semantic labels, midpoint-split gap-fill, X+Y bbox-aware click attribution, and an honest trial-level filter that flags off-axis clicks rather than silently mis-attributing them. The pipeline is validated against shipped ground-truth (38,250 ad classifications, 0 disagreements) and the underlying gaze/cursor data is verified screenshot-aligned via independent ad-rectangle calibration audit.

The contribution is a substrate for downstream model work, not a model itself. Sibling tracks — algorithmic ranking [CITE: cikm-paper], cognitive task modeling [CITE: chi-task-model-paper], pupillometric cognitive load [CITE: ettac-paper], per-fixation arousal [CITE: ripa-pub] — consume the enrichment for findings that the original AdSERP could not have supported at element-type resolution. We close with the descriptive observed-behavior tables that document what's now measurable and visible.

---

## Appendix A — Audit cascade (2026-05-05)

The pipeline shipped in this paper carries an audit trail documenting how the `typed_gapfill` flavor came to exist. A 2026-05-05 audit during preparation of this paper surfaced 22.7 % silent contamination of approached-and-clicked records under the legacy `typed` flavor — Y-band-only click attribution rolled off-axis clicks (right-rail, page chrome, far-off-target) into adjacent main-axis AOIs sharing their Y. The five audit producers documented the cascade end-to-end:

| script | finding |
|---|---|
| `audit_unattributed_clicks.py` | 690 / 2,774 final clicks unattributed under tight bboxes (75.1 %); 80 % of those within ±10 px Y of an organic edge |
| `audit_dd_right.py` | 67 final clicks (2.41 %) on right-rail dd_right ads; typed extraction filters dd_right by design |
| `audit_cascade_contamination.py` | 22.7 % of `approached & clicked` records (391 / 1,723) come from contaminated trials |
| `audit_calibration_bias.py` | calibration-bias hypothesis refuted — opposite-direction click vs fixation bias |
| `audit_screenshot_alignment.py` | data is screenshot-aligned (4:1 inside vs outside near-edge ratio for clicks; deep median inside ads) |

The full writeup including pragmatic-not-principled framing, midpoint-split semantics, and post-cascade headline shifts (NB21 LOSO AUC 0.871 → 0.856; NB28 calibration AUC 0.842 → 0.842 invariant; NB30 LOPO AUC 0.687 → 0.701 with strengthened per-etype dissociation) lives at [CITE: af-null-finding-2026-05-05-bbox-y-coverage].

---

## Open citation placeholders (Pass 2 verification queue)

The following placeholders need resolution before submission:

- `[CITE: AdSERP-original]` — Latifzadeh, Gwizdka & Leiva, "A Versatile Dataset of Mouse and Eye Movements on Search Engine Results Pages," SIGIR '25, 3412–3421. DOI 10.1145/3726302.3730325. Verify exact citation form.
- `[CITE: cikm-paper]` — Andy + Peter; CIKM 2026 algorithmic submission. Title TBD. Cite as forthcoming.
- `[CITE: chi-task-model-paper]` — Andy; CHI 2027 Pittsburgh; arxiv → CHI 2027 path. Title TBD.
- `[CITE: ettac-paper]` — Andy + Duchowski; ETTAC 2026 Lyon, Aug 21. Title TBD.
- `[CITE: ripa-pub]` — Gavindya/team; standalone RIPA pub. Title TBD.
- `[CITE: plan-demo-fix-doc]` — Internal `attentional-foraging/docs/plan-demo-fix.md` documenting the 13–45 px DOM re-render drift. Format as URL or footnote pointing to the released repo.
- `[CITE: af-notebook-key-claims]` — `attentional-foraging/docs/notebook-key-claims.md` (the K-bbox-y-* aggregate). Format as URL.
- `[CITE: af-validation-typed-vs-shipped-ads]` — `attentional-foraging/docs/methodology/validation-typed-vs-shipped-ads.md`. Format as URL.
- `[CITE: af-null-finding-2026-05-05-bbox-y-coverage]` — `attentional-foraging/docs/null-findings/2026-05-05-bbox-y-coverage.md`. Format as URL.
- `[CITE: ar-replay-viewer-url]` — `https://andyed.github.io/approach-retreat/replay/`. Format as URL.

[ATTRIBUTE: ...] entries are paraphrases that need verification against the named source.
[CHECK: ...] entries are factual claims with uncertain source.
