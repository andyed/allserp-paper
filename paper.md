## Abstract

We release **AllSERP**, a typed AOI and per-element behavioral enrichment of the AdSERP commercial-intent SERP corpus \cite{latifzadeh2025adserp}. AdSERP ships 2,776 trials of full-page screenshots, captured SERP HTML, 150 Hz Gazepoint eye tracking, evtrack mouse telemetry, scroll, and pupil signals against real Google SERPs collected before AI Overviews — but its bounding boxes cover only ad surfaces (15.5 % of attributable clicks). AllSERP adds pixel-accurate organic and widget bboxes via screenshot-anchored CV, semantic types across thirteen element types via an HTML parser, an inter-result gap-fill flavor (`typed_gapfill`), and X+Y click attribution that reaches 91.7 % of the corpus while flagging the rest at trial level. The Phase C ad-vs-non-ad partition is internally consistent with the shipped ad rectangles (0 disagreements across 38,250 classifications). We ship the pipeline, per-trial JSONs, a corpus CSV, and a browser-based replay viewer; everything is reproducible from the AdSERP Zenodo volume. The release enables per-element click, fixation, regression, and above-fold analyses that the shipped ads-vs-organic split could not resolve.

---

## §1. Introduction

AdSERP \cite{latifzadeh2025adserp} is the only public IR dataset that combines eye gaze, cursor, scroll, pupil, and click telemetry against ground-truth screenshots and captured SERP HTML on commercial-intent Google SERPs at thousands-of-trials scale. Two early uses prove what the substrate carries: AdSight \cite{villaizan2025adsight} predicts per-slot fixation time at NDCG = 96.07 ± 0.04 from cursor trajectories alone, and pupil-cognitive-load methods are being developed against AdSERP gaze on this corpus — real-time LF/HF \cite{duchowski2026rtlfhf} and per-fixation arousal via RIPA2 \cite{jayawardena2025ripa2}. AllSERP raises the resolution at which work like these can run by replacing AdSight's four-slot taxonomy with a nine-element-type taxonomy and by typing every main-axis card the user sees.

The shipped ad rectangles cover only ad surfaces: roughly **15.5 % of attributable clicks**. The remaining ~84.5 % land on organics, knowledge panels, image packs, People-Also-Ask widgets, and other untyped surfaces. Per-rank claims on AdSERP that pool ads with organics under "absolute rank," or estimate organic geometry from h3 heading counts (which assume uniform result heights — actual layouts vary by 80–320 px), have inherited that gap. AllSERP closes it.

**Anticipated user community.** Click-model researchers (cascade / DCM / UBM lineage and successors), attention and cognitive-load groups using AdSERP for pupil-method development, AdSight-style cursor-attention modelers, and IR replication researchers comparing pre-AI-Overviews behavior against post-rollout SERPs.

### Contributions

1. **Screenshot-anchored typed AOI extraction** with per-trial JSON output covering organic, dd_top, native_ad, dd_right, top_places, knowledge_panel, paa, image_pack, related_searches, pagination, other_widget, unknown_widget, and chrome surfaces.
2. **Inter-result gap-fill and X+Y bbox-aware click attribution** — the gap-fill flavor extends adjacent organic bboxes via midpoint-split and uses X+Y containment, with a trial-level filter flagging off-axis clicks (right-rail ads, page chrome, far-off-target).
3. **Internal-consistency validation** against shipped ground truth — 38,250 ad-classification comparisons, 0 disagreements; structural rather than independent-annotator (§3).
4. **Descriptive observed-behavior inventory** for nine main-axis element types: click share, fixation coverage, regression rate, above-fold incidence, on the full 2,776-trial corpus.
5. **Public release.** Single-script pipeline, per-trial JSONs, corpus CSV, and a browser-based replay viewer (§6.2). MIT code, CC-BY-4.0 derived data, matching the AdSERP corpus license.

---

## §2. Pipeline

![The four-phase pipeline applied to a synthetic SERP. **(A)** CV row-projection on the main column produces card spans (dashed outlines); right-rail dd_right cards are detected but routed off-axis. **(B)** Each main-axis card receives a label from an 8-tier HTML chain. **(C)** Labels are bound to geometry by document order, with each main-axis card receiving a position 0…N; right-rail and footer cards get position −1. **(D)** Adjacent organic pairs share a midpoint; the upper bbox extends down and the lower extends up, so every Y in the column belongs to one bbox. dd_top and image_pack are unchanged.](figs/fig_pipeline.png)

### 2.1 Why screenshot-anchored

The AdSERP team's published methodology extracted AOIs from the DOM at collection time \cite{latifzadeh2025adserp} — the cleanest source when the page is live. For *downstream reuse*, that route fails: re-rendering the saved 2022–2023 HTML in a 2026 browser produces 13–45 px layout drift relative to the original screenshots, well within three years of separation. Drift sources include missing external assets, Chrome version differences, font drift, and Google's continual A/B-testing of SERP rendering. The shipped fixation and cursor streams are pixel-coordinated against the screenshots, so AllSERP anchors AOI geometry to those screenshots via CV and uses HTML only for structural labels. This complements the AdSERP team's collection-time DOM approach: the DOM is cleanest at capture; the screenshots are what survive for downstream reuse.

### 2.2 Four phases

Phase A produces card spans by per-row standard-deviation row-projection on the main column, with shipped ad rectangles taking precedence on overlap and a composite-trigger height triggering inner subdivision for image_pack / paa / top_stories. Phase B walks the saved HTML and assigns each card a type label via an 8-tier priority chain (heading text → structural class signatures → `data-attrid` → fallback structural patterns), producing 13 etypes including a `chrome` sweep for footer artifacts. Phase C binds labels to geometry by document order — the only stable axis when HTML and screenshot don't share a coordinate space. Phase D adds the `typed_gapfill` flavor by extending each pair of adjacent organic bboxes to their shared midpoint, clamped so an organic never crosses an ad or widget. Both flavors are released — the **tight-bbox flavor** (`typed`, Phase A → C) and the **gap-fill flavor** (`typed_gapfill`, Phase A → D); analyses can pick the attribution semantics that match their use. Source code, parameter values, and per-trial outputs ship in the upstream repository (§6.2).

### 2.3 Click attribution and trial filter

Click attribution under the gap-fill flavor requires X *and* Y containment in a main-axis AOI bbox, with a small ±5 X / ±10 Y tolerance fallback for link-padding clicks. Y-only attribution would route right-rail ads, page chrome, and far-off-target clicks into adjacent main-axis AOIs that share their Y; X containment refuses those. The `is_main_axis_click(trial_id)` helper returns True iff a trial's final click lands in a main-axis AOI under this rule. In the AdSERP corpus, 231 trials are flagged at trial level: 67 dd_right (right-rail ad clicks), 91 page-chrome / search-tools / far-off-target, 73 with no clicks recorded or pathological click coordinates. Producers computing click-outcome features drop these trials.

---

## §3. Validation

The shipped ad rectangles \cite{latifzadeh2025adserp} were extracted by the AdSERP authors against the same screenshots the gaze and cursor streams were recorded against, so they are pixel-anchored to the same truth source as our extraction. Phase C ad propagation matches the shipped rectangles across all three ad etypes (`dd_top`, `native_ad`, `dd_right`) with **0 disagreements across 38,250 individual classifications**, mean IoU = 1.000, and 0 of 26,590 Phase A `organic_result` bboxes overlapping any shipped ad rectangle. We frame this as an **internal-consistency check** rather than independent-annotator validation: Phase C inherits ad identity by spatial overlap and is then checked against the same rectangles. The deeper non-ad partition (organic vs paa vs image_pack vs the rest) lacks an external label set; we validate it against the HTML structure that Phase B's chain consumes and against visual spot-check on the curated 147-trial replay set. Independent-annotator validation on a held-out subset is named as future work.

![Replay-viewer rendering of trial p010-b2-t6; the viewer ships with the repo (§6.2). Coloured rectangles are typed AOIs (image_pack carousel at top, organics below, inline native_ad); numbered circles are gaze fixations sized by dwell; the orange polyline is the cursor trajectory. Sparklines below: cursor speed, XY delta, pupil, LF/HF, gaze X/Y, AOI presence.](figs/fig4_replay_p010-b2-t6.png)

---

## §4. Element-Type Inventory

Population: 2,775 trials processed (1 trial dropped: missing meta or fixations); 37,142 typed AOI rows under the gap-fill flavor. Table 1 reports the per-element-type behavioral inventory; column denominators differ — see notes below.

**Table 1.** Per-element-type behavioral inventory under the gap-fill flavor. Etypes ordered by AOI count, descending.

| etype | n_aois | fixated % of aois | n_clicks | click % of clicks | regressive % of fixated | above-fold % of trials |
|---|---:|---:|---:|---:|---:|---:|
| organic        | 22,346 | 55.6 %     | 2,084 | 79.1 % | 57.8 % | 97.3 % |
| native_ad      |  9,214 | 36.4 %     |   156 |  5.9 % | 46.9 % | 37.8 % |
| image_pack     |  1,584 | 52.0 %     |    55 |  2.1 % | 59.3 % | 20.5 % |
| dd_top         |  1,582 | **99.7 %** |   254 |  9.6 % | 83.4 % | 57.0 % |
| unknown_widget |    788 | 17.4 %     |     7 |  0.3 % | 26.3 % |  0.0 % |
| paa            |    769 | 40.6 %     |    44 |  1.7 % | 45.8 % | 11.3 % |
| knowledge_panel|    745 | 48.6 %     |    31 |  1.2 % | 44.5 % |  3.5 % |
| top_places     |     84 | 54.8 %     |     1 |  0.0 % | 50.0 % |  2.1 % |
| other_widget   |     50 | 58.0 %     |     2 |  0.1 % | 44.8 % |  1.1 % |

**Column notes.** *Fixated %* is over the etype's full AOI population. *Click %* is over 2,634 click events attributed to a gap-fill AOI (89 % of total click events; the residual 11 % are intermediate cursor clicks that landed off any main-axis AOI). The 91.7 % corpus-level rate quoted in the abstract counts trials whose *final* click lands main-axis under the trial filter — a different denominator. *Regressive %* is over the fixated subset and is therefore not directly comparable across etypes whose fixation rates differ widely (organic 56 %, dd_top 99.7 %). *Above-fold %* is the share of the 2,776 trials in which at least one AOI of that etype sits in the initial viewport.

**Read.** dd_top reaches near-universal fixation but only 9.6 % of clicks — the click-fixation dissociation is preserved at element-type granularity, sharper than at the ad-vs-organic level the original AdSERP analysis used. The pattern (36.4 % vs 5.9 % for native_ad; 99.7 % vs 9.6 % for dd_top) matches an attention-without-commitment account. Organic results occupy the initial viewport on 97 % of trials and capture 79 % of clicks; widgets and ads dominate above-fold geometry but not click outcomes.

![Click rate by position under the two main flavors AllSERP releases. **Left: organic-only flavor** — position 0 is the topmost organic and the click heavyweight (39.5 %); ranks decline to 4–8 % by position 7+ (Spearman ρ = −0.624). **Right: organic-hybrid flavor** — position 0 is the topmost main-axis card, often a `dd_top` ad (orange bar; 19.9 %); the click peak shifts to position 1 (25.6 %), where the top organic now sits (ρ = −0.939). Two flavors, two stories: consumers should pick the one that matches their question ("what does the top organic earn?" vs "what does the topmost SERP slot earn?").](figs/fig_rank_effects.png)

---

## §5. How to Use

The release is one corpus CSV plus per-trial JSONs. A 12-line worked example loads the typed AOIs for one trial, filters to organics, and computes click rate by position:

```python
import json, polars as pl
csv = pl.read_csv("adserp_aois_by_trial_id_typed_gapfill.csv")
organics = csv.filter(pl.col("etype") == "organic")
clicks = (organics
          .group_by("position")
          .agg(pl.col("was_clicked").mean().alias("click_rate"),
               pl.len().alias("n_records"))
          .sort("position"))
print(clicks)  # rank → click rate, n
trial = json.load(open("aoi-typed-gapfill/p010-b2-t6.json"))
print([(a["etype"], a["position"], a["bbox"]) for a in trial["aois"]])
```

`scripts/build_aois.py --trial p010-b2-t6` regenerates the per-trial JSON from the AdSERP screenshot and HTML; `--all` runs the full corpus. Existing AdSERP signal files (cursor approach features, pupil power-ratio, saccade orientation) carry per-AOI etype tags after the join, so any rank-conditioned analysis already coded against AdSERP gains a per-element conditioning axis without re-collecting data.

---

## §6. Limitations and Public Release

### 6.1 Scope and provenance

**Forced-choice task design.** AdSERP elicits one click per query within a 1-minute window (extended to 2 minutes after a confirmation prompt) on a single query phrase per trial. The corpus does not sample query refinement, query reformulation, pagination, abandonment, multi-query sessions, or decision arcs longer than the forced-choice envelope. Behavioral statistics in §4 are properties of constrained-choice SERP evaluation, not of free Google search.

**Pre-AI-Overviews snapshot.** Data were collected between 2022-12-16 and 2023-03-13 (verified from per-trial entry timestamps), predating Google's AI Overviews / SGE rollout (limited test May 2023, broad deployment May 2024) and Bard's launch (March 21, 2023, three days after collection ended). This is a *feature*: AllSERP is the canonical pre-SGE snapshot of commercial-intent Google SERP behavior, an artifact whose value as a baseline grows over time. Replications on post-May-2024 SERPs need an additional `ai_overview` etype, and the AI answer card has substantively different click-fixation dynamics; the four-phase pipeline shape is era-agnostic and only Phase B's label set needs to grow.

**Phase D heuristic.** The midpoint-split is a heuristic for the boundary between adjacent organic results, not DOM-derived ground truth. Misattribution is bounded by inter-result gap size (typically 5–60 px). We ship both flavors so consumers pick.

**Right-rail coverage.** The pipeline tracks shipped `dd_right` rectangles for off-axis classification but does not recover right-rail organic-style results. ~1 % of trials show a right-rail click that has no shipped rectangle; this is a property of the original release.

**Provenance.** AdSERP collection followed the original team's approved IRB \cite{latifzadeh2025adserp}; AllSERP processes only de-identified telemetry and screenshots already released under CC-BY-4.0.

### 6.2 Public release

- **Code.** `attentional-foraging` (https://github.com/andyed/attentional-foraging) and `approach-retreat` (https://github.com/andyed/approach-retreat) under MIT license. Single-script entry point at `scripts/build_aois.py`.
- **Derived data (CC-BY-4.0).** Per-trial gap-fill AOI JSONs (~19 MB across 2,776 trials), corpus CSV (37,142 rows), per-(trial, position) content-feature file (lexical, query-overlap, semantic-cosine — see repo README for the methodology and a snippet-TTR rank-confound caveat that consumers must partial out before per-position content claims).
- **Replay viewer.** https://andyed.github.io/approach-retreat/replay/ renders typed AOIs on the source SERP screenshots for 147 curated trials.
- **Underlying corpus.** AllSERP requires the AdSERP Zenodo volume (https://zenodo.org/records/15236546) — AdSERP authors release it CC-BY-4.0; AllSERP does not redistribute screenshots or HTML.

### 6.3 Citation

Cite both papers — AllSERP for the typed AOI extraction, AdSERP for the underlying multimodal signals. Suggested BibTeX in the upstream README.

---

## §7. Conclusion

AllSERP is a typed AOI and per-element behavioral enrichment of the AdSERP corpus. The pipeline anchors bbox geometry to the shipped screenshots, types every element via an 8-tier HTML parser, and fills inter-result Y gaps via midpoint-split. The Phase C ad partition is internally consistent with shipped ground truth across 38,250 classifications; click attribution under X+Y containment reaches 91.7 % of the corpus. The descriptive observations in §4 surface click-fixation dissociation, regressive return rates, and above-fold geometry at per-element granularity that the prior ad-vs-organic split did not resolve.

The substrate the enrichment unlocks is broader than the four metrics inventoried here. With per-element labels and geometry now joined to the multimodal telemetry the AdSERP team released, several lines of work become tractable on the existing 2,776-trial corpus without re-collecting data. Cursor approach-retreat episode geometry can be computed per AOI rather than per rank, exposing the shape of the decision moment as a function of element type. Pupillometric and LF/HF cognitive-load signals \cite{duchowski2026rtlfhf,jayawardena2025ripa2} can be conditioned on element type, separating the load profile of an organic-result inspection from a knowledge-panel scan or an ad-card glance. Content-feature analyses can be paired with element-type and behavioral outcomes to ask which content properties co-vary with engagement on which surfaces — information-foraging theory \cite{pirolli1999foraging,fu2007snifact} provides a natural theoretical lens, with query-snippet semantic cosine and query-token overlap as operational proxies for information scent at the per-AOI level.

What ships here is the geometric and typing layer those next steps depend on. The behavioral inventory in §4 is the descriptive baseline; the analyses it enables are the work the field can now do on a clean pre-AI-Overviews snapshot of commercial-intent SERP behavior, while the four-phase pipeline shape stays era-agnostic for replications on post-rollout SERPs. We are optimistic about the breadth of IR and HCI work the dataset can support.

## §8. AI Use

This paper was drafted in collaboration with Anthropic's Claude (Opus 4.7). Two automated audit tools were used to keep the draft honest: a citation-management tool (`science-agent`) cross-referenced every `\cite{}` against the bibliography and lit-notes verifying that prose paraphrases match each cited work's actual claims, and an argument-rigor pass flagged ungrounded comparatives, causal language in descriptive prose, and numerical mismatches across sections, tables, and figure captions. The pipeline that produced this paper's numbers is itself disciplined by stable Key-Claim identifiers in the upstream notebooks, which made mid-draft revisions cheap to recompute end-to-end without hand-typing or interpretation drift; null findings are tracked alongside positive results in the released artifact. All quantitative claims, citations, and methodological decisions were verified by the authors; the authors take full responsibility for the content.

## Acknowledgments

Thanks to Peter Dixon for code review and collaboration on downstream use cases.
