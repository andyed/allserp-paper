# dd_top differentiation in the typed-AOI layer

_Draft note for the AllSERP arXiv update. Numbers from
`attentional-foraging/scripts/validate_typed_aoi_migration.py` (2026-06-07), canonical
flavor `aoi-typed`._

## What changed

The base AdSERP release provides ad-boundary bounding boxes but no unified per-element
typing of the result page. The AllSERP typed-AOI layer assigns every detected SERP card
to one of 13 element types and, critically, **separates the two ad surfaces** that prior
work pooled:

- **`dd_top`** — the top sponsored *product/shopping carousel* ("direct display" block
  above the organic stream).
- **`native_ad`** — in-stream sponsored results interleaved among organics.
- **`organic`** — unpaid results.

Differentiating `dd_top` from `native_ad` and from `organic` is what lets per-element-type
attention and click-attribution analyses treat the top product carousel as its own surface
rather than folding it into a generic "ad" or, worse, into organic rank.

## Coverage (canonical `aoi-typed`, n = 2,776 trials)

| element type | AOIs | trials | CV-placed |
|---|--:|--:|--:|
| organic | 22,530 | 2,776 | 22,354 (99.2%) |
| native_ad | 9,217 | 2,647 | 100% |
| **dd_top** | **1,582** | **1,582 (57.0%)** | **1,582 (100%)** |
| dd_right | 861 | 861 | 100% |
| knowledge_panel | 826 | 767 | 90.3% |
| paa | 769 | 769 | 100% |
| image_pack | 1,600 | 1,580 | 99.0% |
| (others: top_places, related_searches, pagination, chrome, unknown/other_widget) | | | |

- **`dd_top` appears in 57.0% of trials** — exactly one carousel per trial that has one —
  and is **100% CV-anchored** (every `dd_top` block sits on the main scroll axis with a
  resolved bounding box).
- Null-bounding-box AOIs (organic 176, knowledge_panel 80, image_pack 16, …) are all
  off-axis / below-fold elements marked `position = -1` (HTML-known but not rendered in the
  captured screenshot). There are **zero** anomalous null boxes (a placed, main-axis element
  missing geometry) — the typing is internally consistent.

## Provenance

`dd_top` differentiation is present in the typed flavors (`aoi-typed`,
`aoi-typed-gapfill`) and **absent** in the pre-typing `aoi-html-types` layer (HTML-only, no
CV boxes). Re-run the validator after any pipeline change as a regression guard.

> **Scope note:** the CIKM submission used the dataset **prior to full typing**. Any
> re-analysis under the typed layer is a sensitivity check against a newer substrate, not a
> correction to the CIKM numbers.
