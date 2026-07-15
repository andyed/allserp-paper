# AllSERP Resource Paper

**Working title:** *AllSERP: Exhaustive Per-Element Enrichment of the Versatile AdSERP Dataset*

This is a **resource / dataset enrichment paper**. The contribution is the typed_gapfill AOI pipeline, the public extraction code, and the descriptive observed-behavior inventory across SERP element types. The paper does not propose new models; downstream model work lives in sibling tracks.

---

## Sources of truth

Every numeric claim traces to:
- `~/Documents/dev/attentional-foraging/scripts/output/allserp_descriptives_gapfill/` (per-etype tables under typed_gapfill)
- `~/Documents/dev/attentional-foraging/docs/notebook-key-claims.md` (K-bbox-y-* rows)
- `~/Documents/dev/attentional-foraging/docs/null-findings/2026-05-05-bbox-y-coverage.md` (audit cascade)
- `~/Documents/dev/attentional-foraging/docs/methodology/organic-result-aoi-extraction.md` (pipeline spec)
- `~/Documents/dev/attentional-foraging/scripts/audit_*.py` (five cite-ready audit producers)

If a number appears in this paper without a `[<flavor>, <source>]` regime tag, it's a citation bug.

---

## Out-of-scope (do not duplicate from sibling tracks)

- **Four-class taxonomy as graded-relevance label generator** → sibling algorithmic track.
- **OSEC cognitive task model** (Orient / Survey / Evaluate / Commit) → sibling task-model track.
- **Per-etype LF/HF / pupillometric cognitive load gradients** → sibling pupillometric-validation track.
- **Per-fixation arousal findings** → sibling arousal-analysis track.

We name each as a "what's enabled" pointer in §5 (Data Enablement), with a one-line description and a citation to the relevant sibling work. We do **not** restate their findings or compete for headline space.

---

## Two-pass citation discipline (mandatory; see AF CLAUDE.md for full spec)

When editing this paper:

**Pass 1 — Prose generation.** Do NOT write:
- Author names in citation position (e.g. "Latifzadeh et al.")
- Venue+year tokens (e.g. "[SIGIR '25]")
- Paraphrases of what specific source papers "showed" / "demonstrated" / "found"

Instead use:
- `[CITE: <topic>]` for citations
- `[ATTRIBUTE: <source-key>: <claim>]` for paraphrases
- `[CHECK: <claim>]` for any factual claim with uncertain source

**Pass 2 — Verification.** Walk every placeholder. Locate source (bib first, then lit-notes, then WebSearch/WebFetch). Verify the abstract/passage matches. Resolve or change the argument. **Do not invent.**

---

## Voice / tone (per andy:)

- No false profundity. State the fact, explain why, move on.
- No "remarkably," "surprisingly," "fascinatingly." Substance over hype.
- Direct prose. Don't oversell the contribution; the audit cascade is interesting enough on its own.
- "Pragmatic, not principled" framing for the midpoint-split. Don't claim the heuristic is the right answer; claim it is reproducible and recovers signal that was being silently dropped.

---

## Writing checkpoints

- **Voice check** — every section drafted should pass: would Andy say this in conversation, or does it feel like academic posturing? If the latter, simplify.
- **Empirical check** — every numeric claim has a `[<flavor>, <source>]` tag.
- **Sibling-track guard** — every paragraph that ventures toward a model claim gets the question: "is this scoping into a sibling track?" If yes, cut to a "what's enabled" pointer.
- **Ad-rect ground truth** — the validation gate (38,250 classifications, 0 disagreements, F1 = 1.000) is the empirical anchor. Mention it early; it's the single most paper-credibility-establishing fact.

---

## Conventional commits

`type(scope): message` per the AF / AR convention. Common types:
- `feat(paper):` — new section or substantive content
- `docs(paper):` — readme, this file, changelog
- `data(paper):` — refresh of derived numbers from upstream
- `fix(paper):` — citation or factual correction
