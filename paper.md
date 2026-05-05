# AllSERP: A Typed AOI and Per-Element Behavioral Enrichment of the AdSERP Dataset

**Status:** Working draft, 2026-05-05. Markdown-first; LaTeX conversion deferred until content is stable.
**Target venue:** SIGIR 2026 Resource Paper track (primary).
**Tag:** `[LAB, AdSERP, typed_gapfill, AllSERP-resource-paper-draft-v0]`

---

## Abstract

The AdSERP dataset \cite{latifzadeh2025adserp} pairs full-page screenshots, 150 Hz Gazepoint eye tracking, evtrack mouse telemetry, scroll signals, and pupil diameter across 2,776 commercial-intent trials and 47 participants conducted between 2022-12-16 and 2023-03-13, before Google's introduction of AI Overviews. Participants were provided with a query phrase and were asked to act with purchase intent within a 1 minute time limit, extended to up to 2 minutes after a reminder prompt.  The dataset includes ad bounding boxes but no organic-result bboxes, no per-cell carousel subdivision, and no semantic typing of widgets. 

This paper contributes a typed AOI enrichment pipeline that closes those gaps: computer vision row-projection on the original screenshots recovers pixel-accurate bbox geometry; an 8-tier HTML parser provides semantic labels across thirteen element types; a midpoint-split post-processor (`typed_gapfill`) fills inter-result Y gaps so fixations and clicks landing in those gaps are attributable. We validate the ad-vs-non-ad partition against the shipped ad rectangles with **0 disagreements across 38,250 classifications** (F1 = 1.000), and use those same rectangles as alignment ground truth for an independent screenshot-alignment audit. A reaches **91.7 %** of the corpus, with the remaining 8.3 % flagged at trial level (right-rail ads, page chrome, far-off-target) rather than silently mis-attributed.

We release the pipeline as a single-script public API and report descriptive observed-behavior tables for nine main-axis SERP element types: click share, fixation coverage, regression rate, and above-fold incidence. The enriched dataset opens per-element behavioral analysis at finer granularity than the shipped-ads-vs-organic split previously allowed, on a multimodal substrate (eye + cursor + scroll + pupil) for commercial-intent SERPs in a clean pre-AI-Overviews window. We are honest about what AdSERP's task design does *not* sample: query refinement and reformulation, pagination, abandonment, and any decision arc longer than the 1-to-2-minute forced-choice envelope. These are real limits on generalization, named here so consumers can scope their use of the enrichment accordingly.

---

## §1. Introduction

The AdSERP dataset \cite{latifzadeh2025adserp} occupies a distinctive position in the multimodal IR resource landscape: simultaneous eye gaze, cursor, scroll, pupil, and click telemetry against ground-truth screenshots, on real Google search-result pages with realistic commercial-intent task framing. The dataset's authors framed their contribution as the first publicly available large-scale resource combining (1) eye-tracking, (2) mouse trajectories, and (3) SERP HTML amenable to programmatic AOI segmentation at thousands-of-trials scale, with eye fixations on programmatically extracted AOIs intended as ground-truth labels for inferring visual attention from mouse movements at high granularity. AdSERP supplies the substrate; the per-element AOI extraction implied by that framing was left for downstream work. This paper realizes that extraction.

The shipped ad rectangles cover only the surfaces directly relevant to AdSERP's original ad-attention focus. In the released corpus, ad surfaces (`dd_top` + `native_ad` + `dd_right`) receive roughly **15.5 % of attributable clicks** — meaning the ~84.5 % of click behavior that landed on organics, knowledge panels, image packs, People-Also-Ask widgets, and other non-ad surfaces sits outside the shipped per-element labels. Three opportunities follow for studying that broader behavior:

1. **Organic-result bounding boxes.** Ad rectangles ship with the dataset; organic-result rectangles do not. Adding them lets per-rank analyses operate on pixel-accurate organic geometry rather than estimating from h3 heading counts (which assume uniform result heights — actual layouts vary by 80–320 px per result) or pooling ads with organics under "absolute rank."

2. **Semantic typing of every result.** A "rank-1 result" might be a top-of-page ad, a knowledge panel, an image pack, an organic result, or a People-Also-Ask widget. Each receives a different click rate and triggers different cognitive operations. Adding per-card type labels lets per-rank claims disambiguate which surface they refer to.

3. **Carousel / composite subdivision.** Top-stories carousels, image packs, and product-list ads ship as single-rectangle parents; the per-product cells inside them are not enumerated. Adding cell-level rectangles enables per-product click and fixation attribution.

This paper releases a pipeline that recovers all three: pixel-accurate organic and widget bounding boxes from CV row-projection on the screenshots, HTML-anchored semantic labels via spatial join, and per-cell carousel subdivision via vertical-edge peak detection. We validate the ad-vs-non-ad partition against the shipped ad rectangles (0 disagreements across 38,250 classifications) and report descriptive observed-behavior tables for the nine main-axis element types the pipeline produces.

### Utility and limits

The enrichment opens four classes of analysis on the existing AdSERP corpus:

- **Per-element behavioral statistics** — click share, fixation coverage, regression rate, and above-fold incidence stratified by SERP element type (organic, dd_top, native_ad, dd_right, paa, image_pack, knowledge_panel, top_places, related_searches, pagination). §4 reports these for the full 2,776-trial corpus.
- **Per-element conditioning of existing signals** — cursor approach features, pupil and LF/HF cognitive-load signals, and saccade orientation can now be sliced by element type rather than pooled across surfaces.
- **Geometry-aware attribution** — fixations and clicks landing in inter-result gaps are now attributable instead of silently dropped, and clicks on off-axis surfaces (right-rail, page chrome) are flagged at trial level rather than rolled into adjacent organics.
- **Pre-AI-Overviews snapshot** — the data-collection window (2022-12-16 to 2023-03-13, §6) sits cleanly before Google's AI Overviews / SGE rollout, providing a baseline for "classic" Google SERP composition that future work can compare against.

The dataset's task design also limits what the enrichment can speak to. AdSERP elicits a **forced choice within a 1-minute time limit (extended to 2 minutes after a confirmation prompt)** on a single query phrase per trial. This means the corpus does not sample query refinement, query reformulation, pagination, abandonment, multi-query sessions, or decision arcs longer than the forced-choice envelope. The behavioral statistics in §4 are therefore properties of *constrained-choice* SERP evaluation, not of free Google search; analyses that need session-level dynamics or long-horizon decisions will need other data. We name these gaps explicitly in §6 and surface them throughout the paper so consumers can scope their use of the enrichment accordingly.

### Contributions

1. **Screenshot-anchored typed AOI extraction** with per-trial JSON output covering organic, dd_top, native_ad, dd_right, top_places, knowledge_panel, paa, image_pack, related_searches, pagination, other_widget, unknown_widget, and chrome surfaces.

2. **Inter-result gap-fill and X+Y bbox-aware click attribution** — `typed_gapfill` extends adjacent organic bboxes to fill inter-result Y gaps via midpoint-split and uses X+Y containment for click attribution rather than Y-band-only assignment, with an `is_main_axis_click()` trial filter for off-axis clicks.

3. **Validation against shipped ground truth** — 38,250 ad-classification comparisons, 0 disagreements, F1 = 1.000 on Phase C ad propagation, mean IoU = 1.000.

4. **Descriptive observed-behavior inventory** for nine main-axis element types: click share, fixation coverage, regression rate, above-fold incidence, on the full 2,776-trial corpus.

5. **Public API and reproducible artifacts.** Single-script entry point (`scripts/build_aois.py`) wrapping the four-phase pipeline. Per-trial JSON outputs and corpus CSV released alongside the upstream code.

---

## §2. Method: Typed AOI Extraction

### 2.1 Why screenshot-anchored

The AdSERP team's published methodology leveraged the DOM at collection time to extract AOIs programmatically from each SERP \cite{latifzadeh2025adserp}. That choice was correct in 2022–2023: the DOM is the structurally cleanest source of element geometry when the page is live and the rendering environment matches the capture session. The fixation and cursor streams the team released were recorded in pixel coordinates against the corresponding full-page screenshots.

The complication is temporal. Re-rendering the saved 2022–2023 SERP HTML in a 2026 browser produces 13–45 px layout drift relative to the original screenshots [ATTRIBUTE: plan-demo-fix-doc: residual median <13 px, max ~45 px at page bottom from re-rendered SERP HTML] — well under three years of separation. Three contributing failure modes: external image hosts return errors or different content, font and CSS rendering heuristics differ between Chrome versions, and saved Google SERP HTML often contains anti-bot JS that detects headless renderers and rewrites the DOM. A downstream consumer in 2026 who repeats the AdSERP team's DOM-extraction approach against the released HTML inherits this drift and ends up with bboxes that no longer align to the released gaze and cursor coordinates.

For downstream reuse, then, the shipped screenshots — not the saved HTML — are the durable truth source for geometry. AllSERP anchors bbox extraction to those screenshots via CV, with HTML used only for structural labels (semantic typing of cards) and for the spatial join, never for geometry directly. This complements rather than replaces the AdSERP team's collection-time DOM approach: at capture, the DOM is cleanest; for subsequent reuse against the released coordinate streams, screenshot-anchored extraction is what survives the drift.

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

The midpoint is a heuristic boundary, not a DOM-derived ground truth. We ship both `typed` (Phase A → C) and `typed_gapfill` (Phase A → D) flavors so analyses that prefer tight visible-text bboxes can use the former and analyses that prefer full coverage of inter-result clicks and fixations can use the latter.

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

X+Y containment matters because clicks land in three places that Y-only attribution would silently roll into adjacent main-axis AOIs: right-rail ad surfaces (`dd_right`), page chrome (search tools, pagination, header), and far-off-target clicks. Requiring X containment routes those clicks to either an off-axis AOI or to the trial-level filter (§2.7) instead of corrupting main-axis click counts.

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

The shipped ad rectangles in \cite{latifzadeh2025adserp} provide a labeled set against which Phase C's ad classifications can be checked structurally. The rectangles were extracted by the AdSERP authors against the same screenshots that the gaze and cursor streams were recorded against, so they are pixel-anchored to the same truth source as our extraction.

Phase C ad propagation matches the shipped rectangles with **F1 = 1.000** across all three ad etypes (`dd_top`, `native_ad`, `dd_right`); 0 of 26,590 Phase A `organic_result` bboxes overlap any shipped ad rectangle; mean IoU = 1.000 between matched Phase C bboxes and the shipped rectangles. There are no cross-type misclassifications across 38,250 individual classifications.

The deeper non-ad partition (organic vs paa vs image_pack vs knowledge_panel vs top_places vs related_searches vs pagination vs other_widget vs unknown_widget) lacks an external label set. It is validated against the HTML structure that Phase B's 8-tier chain consumes plus visual spot-check on representative trials. We document this validation asymmetry rather than claiming it has the same F1 = 1 character. Visual proof for the curated 147-trial replay set is browsable at [CITE: ar-replay-viewer-url], where each AOI is rendered as a colored overlay rectangle on the source SERP screenshot.

---

## §4. Element-Type Inventory and Observed Behavior

Population: 2,775 trials processed (1 trial dropped: missing meta or fixations); 37,142 typed AOI rows under the `typed_gapfill` flavor. The four tables below report descriptive observed-behavior statistics per element type — counts and fixation coverage, click distribution, regressive share, and above-fold incidence. We treat these as observations of *what users did with the SERP*, not as model claims; mechanistic interpretation belongs to the sibling tracks named in §5.

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

**Read.** Organic results capture 79 % of clicks; ads (`dd_top` + `native_ad`) capture 15.5 %; widgets capture 5.4 %. The original AdSERP non-ad-click headline \cite{latifzadeh2025adserp} survives at finer resolution: `dd_top` has near-universal fixation (99.7 %, §4.1) but receives only 9.6 % of clicks — the click-fixation dissociation is preserved at element-type granularity. The pattern is sharper for `native_ad` (36.4 % fixated, 5.9 % clicked: a 6.2× attention-to-click gap) than for `dd_top` (99.7 % vs 9.6 %: a 10.4× gap). In both cases the dissociation is what would be predicted by an attention-without-commitment account of ad-element user behavior.

The 8.3 % shortfall from full attribution (2,634 attributed clicks vs ~2,776 trial clicks) is the trial-level filter (`is_main_axis_click`, §2.7). Those trials have no main-axis click target; they are flagged at trial level rather than rolled into adjacent organics.

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

**Read.** `dd_top` has the highest regressive share (83.4 %). Position confound: `dd_top` is the highest-ranked element when present, so by construction any return to `dd_top` after the gaze advances to a lower-ranked AOI counts as regressive. The same caveat applies in weakened form to `image_pack` (59.3 %) and other surfaces that frequently sit at the top of the page. Less so to `organic` (57.8 %), which spans the full rank range. The headline is the *behavior*, not an absolute rate: users return to `dd_top` after looking past it on 83 % of trials where `dd_top` is fixated, despite committing to it on only 9.6 % of those trials. Pattern is consistent with attention capture without commitment, and the rate at which users reconsider a top-of-page ad is a property of element type (not just position) once `unknown_widget` (26.3 %, lowest) and `dd_top` (83.4 %, highest) are both held against the same denominator construction.

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

**Read.** Organic results occupy the initial viewport on 97 % of trials. `dd_top` is above fold on 57 % of trials (when present, `dd_top` is by construction at the top of the page, but the corpus contains trials with no `dd_top`). Knowledge panels and PAA widgets are predominantly below-fold (3.5 % and 11.3 %). Any analysis that conditions on above-fold exposure must stratify by element type — pooling averages out the dominant geometric reality.

Cross-table observation: `dd_top`'s above-fold incidence (57 %) and its fixation coverage (99.7 %) together imply that on the 43 % of trials where `dd_top` is *not* present, users are still allocating attention to whatever is at the top of the page. The unconditional fixation rate of `dd_top` is high precisely because top-of-page foveation is inevitable; the finding is not "ads grab attention" but "users foveate whatever sits at trial onset." The dissociation between fixation and click for `dd_top` therefore reflects a commit-vs-not-commit decision *given* attention is granted by geometry.

### 4.5 Four-class behavioral taxonomy

A four-class taxonomy partitions trial × AOI records by user behavior: **clicked** (the user committed to the AOI), **deferred** (the user approached and gaze-regressed back to it without committing), **evaluated-rejected** (the user approached without regressing), and **not-approached** (cursor `min_dist ≥ 100` px). Under `typed_gapfill` the class proportions are:

| class | proportion |
|---|---:|
| clicked | 13.0 % |
| deferred | 13.3 % |
| evaluated-rejected | 2.9 % |
| not-approached | 70.8 % |

Per-element-type breakdowns are reported in upstream notebook output [CITE: af-notebook-key-claims]. The taxonomy is descriptive — what behavior the user exhibited toward each AOI — not a relevance label; consumers needing graded-relevance signal should derive it explicitly rather than reading these labels as relevance.

---

## §5. What the enrichment opens up

The original AdSERP dataset shipped raw multimodal signals plus ad bboxes. Per-element analysis was therefore limited to ad surfaces vs everything-else. With per-element labels and geometry in place across the full main scroll axis, three classes of downstream analysis become tractable on the existing 2,776-trial corpus without re-collecting data.

### 5.1 Per-element descriptive baselines

The counts and rates in §4 are themselves a contribution: a per-element-type behavioral inventory for commercial-intent SERPs that the prior IR multimodal-data literature did not have. Click-prediction baselines that previously had to pool ads with organics now have a clean per-etype split. Reading-time and dwell analyses can stratify by widget type rather than averaging across heterogeneous surfaces. Click-fixation dissociation findings can be quantified per element type rather than at the ad-vs-organic granularity the original AdSERP analysis used.

### 5.2 Per-element conditioning of existing signals

`typed_gapfill` carries per-AOI element-type tags into every downstream feature file derived from the corpus. Existing signals — cursor approach features, pupil and LF/HF cognitive-load signals, saccade orientation, above-fold-conditioned analyses — gain a new conditioning axis they did not have before:

- **Cursor approach features** per trial × AOI with `etype` field.
- **Pupil and LF/HF cognitive-load signals** per AOI position with element-type stratification.
- **Saccade orientation** at per-position granularity.
- **Above-fold-conditioned analyses**, with the geometric confound across element types (§4.4) made explicit and addressable.

These are existing signals that gain a new conditioning axis under the enrichment, not new signals.

### 5.3 Reproducibility chain

The full reproducibility chain — released per-trial JSONs, the executable scripts that produced them, and the shipped Zenodo screenshot volume — runs without access to private state. Source-of-truth pointers are listed in §6.2.

---

## §6. Limitations and Public Release

### 6.1 Scope limits

**Forced-choice task design.** AdSERP elicits one click per query within a 1-minute time limit (extended to 2 minutes after a confirmation prompt) on a single query phrase per trial. The corpus does not sample query refinement, query reformulation, pagination, abandonment, multi-query sessions, or decision arcs longer than the forced-choice envelope. The behavioral statistics in §4 are properties of constrained-choice SERP evaluation, not of free Google search. Trial durations under typed_gapfill: median 19.7 s, p95 46.3 s, p99 57.7 s; 99.5 % of trials sit within the first one-minute window, 0.5 % continue under post-prompt conditions. Analyses that need session-level dynamics or long-horizon decisions will need other data.

**Pre-AI-Overviews collection window.** Data was collected between 2022-12-16 and 2023-03-13 (verified from per-trial `entry_t` timestamps). This window predates Google's AI Overviews / SGE rollout (limited test May 2023, broad deployment May 2024) and Bard's launch (March 21, 2023, three days after collection ended). The element-type taxonomy in this paper is exhaustive for the 2022–2023 Google rendering. Replications on post-May-2024 SERPs need an `ai_overview` etype added and face substantively different click-fixation dynamics for the AI-generated answer card.

**Right-rail coverage.** The pipeline tracks shipped `dd_right` rectangles for off-axis classification but does not recover right-rail organic-style results. Visual inspection of the 147-trial replay set surfaced a trial whose right-rail click had no shipped `dd_right` rectangle, indicating the shipped right-rail data is itself incomplete. The right-rail blind spot affects ~1 % of trials and is a property of the original shipped data; we name it rather than claim it is solved.

**Composite-widget cell labels.** Phase A subdivides composite widgets (top_stories, image_pack, PAA) into per-cell rectangles. These cells receive geometry but not Phase B semantic labels — the inner content of an image_pack cell is not typed. Per-cell behavioral analysis needs additional HTML parsing per widget subtype, named as future work.

**Phase D heuristic boundary.** The midpoint-split is a heuristic choice of where to draw the boundary between adjacent organic results, not a DOM-derived ground truth. Misattribution magnitude is bounded by the inter-result gap size (typically 5–60 px). We ship both `typed` and `typed_gapfill` so consumers can pick the flavor that matches their attribution preference.

**Descriptive only.** This paper reports observed-behavior statistics. Mechanistic interpretation — what drives the click-fixation dissociation, why regressive returns differ across surfaces, how cognitive load modulates per-element evaluation — is downstream work; per-element causal claims should not be extracted from the §4 tables in isolation.

### 6.2 Public release

- **Code.** Upstream repositories under MIT license: `attentional-foraging` ([CITE: af-repo-url]) and `approach-retreat` ([CITE: ar-repo-url]). Single-script public entry point at `scripts/build_aois.py`.
- **Derived data.** Per-trial `typed_gapfill` AOI JSONs (~19 MB across 2,776 trials) and corpus CSV (37,142 rows) at the upstream output paths.
- **Replay viewer.** [CITE: ar-replay-viewer-url] renders typed AOIs as colored overlay rectangles on the source SERP screenshots, including the curated 147-trial subset.

The full reproducibility chain — from the released per-trial JSONs through the executable scripts to the shipped Zenodo screenshot volume [CITE: AdSERP-zenodo] — runs without access to private state.

---

## §7. Conclusion

The AdSERP team positioned their dataset as the first publicly available large-scale resource combining eye-tracking, mouse trajectories, and SERP HTML amenable to programmatic AOI segmentation at thousands-of-trials scale, with eye fixations on programmatically extracted AOIs as ground-truth labels for inferring visual attention from mouse movements at high granularity. AllSERP advances that direction: per-element geometry and typing across the full main scroll axis, validated against the shipped ad rectangles with F1 = 1.000 across 38,250 classifications, click attribution that catches off-axis clicks at trial level rather than routing them silently to adjacent organics.

The descriptive observations in §4 demonstrate what the enrichment opens up: the click-fixation dissociation that the original AdSERP analysis identified at the ad-vs-organic level holds at finer element-type granularity, regressive return rates vary three-fold across surfaces, and above-fold geometry differs sharply by element type in ways that any analysis pooling across types would average out. The dataset's task design (forced-choice within a 1–2 minute envelope) means these are properties of constrained-choice evaluation rather than free Google search; the data does not sample query refinement, reformulation, pagination, or abandonment. We name those limits explicitly so consumers can scope their use of the enrichment.

The pipeline is screenshot-anchored because re-rendering 2022–2023 SERP HTML in 2026 introduces 13–45 px layout drift — measurable in less than three years between collection and reuse. Per-element analyses on this dataset can be done against bboxes that align to the released gaze and cursor coordinates. Replications on post-AI-Overviews SERPs will need an extended taxonomy and their own screenshot anchoring; the four-phase pipeline is era-agnostic in shape, and the Phase B label set is the layer that needs to grow.
