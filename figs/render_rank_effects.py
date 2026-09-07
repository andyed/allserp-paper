"""Two-panel rank-effects: click rate × position under two attribution flavors.

Shows the choice that downstream consumers face. Position 0 means different
things under the two flavors:
  - organic-only — rank 0 is always the topmost organic result
  - organic-hybrid — rank 0 is the topmost main-axis card (often a dd_top ad)

Both flavors are released; this visual lets consumers see which one matches
their question.

Sources:
  attentional-foraging/AdSERP/data/cursor-approach-features-organic.json
  attentional-foraging/AdSERP/data/cursor-approach-features-organic-hybrid.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).parent
OUT_PNG = OUT_DIR / "fig_rank_effects.png"
OUT_PDF = OUT_DIR / "fig_rank_effects.pdf"

AF = Path("/Users/andyed/Documents/dev/attentional-foraging/AdSERP/data")

ACCENT  = "#5B3EB8"
ACCENT2 = "#26A69A"
INK     = "#0B1220"
MUTED   = "#4B4B4B"
RULE    = "#D2CEC4"
BG      = "#FAFAF8"

DD_TOP_HUE = "#E69F00"  # mark the "rank 0 = dd_top" cells under hybrid


def load_flavor(path: Path):
    data = json.load(open(path))
    n = Counter()
    clk = Counter()
    etype_at_pos = defaultdict(Counter)
    for r in data:
        pos = r["position"]
        if pos < 0 or pos > 9:
            continue
        n[pos] += 1
        if r.get("was_clicked"):
            clk[pos] += 1
        if "etype" in r:
            etype_at_pos[pos][r["etype"]] += 1
    positions = sorted(n)
    rates = np.array([100 * clk[p] / n[p] if n[p] else 0 for p in positions])
    counts = np.array([n[p] for p in positions])
    top_etype = {p: etype_at_pos[p].most_common(1)[0] if etype_at_pos[p] else None for p in positions}
    return positions, rates, counts, top_etype


def spearman_rho(x, y):
    n = len(x)
    rx = np.argsort(np.argsort(x)) + 1
    ry = np.argsort(np.argsort(y)) + 1
    d2 = float(np.sum((rx - ry) ** 2))
    return 1 - 6 * d2 / (n * (n * n - 1))


def render_panel(ax, positions, rates, counts, top_etype, *, color, title, flavor_label):
    bars = ax.bar(positions, rates, color=color, edgecolor=INK, linewidth=0.5, width=0.78)
    # Override color where the dominant etype is dd_top (e.g. hybrid pos 0)
    for p, bar in zip(positions, bars):
        if top_etype.get(p) and top_etype[p][0] == "dd_top":
            bar.set_color(DD_TOP_HUE)
            bar.set_edgecolor(INK)
    for p, r in zip(positions, rates):
        ax.text(p, r + 1.0, f"{r:.1f}%", ha="center", va="bottom",
                fontsize=9, color=INK, family="Georgia")
    rho = spearman_rho(np.array(positions), rates)
    total_n = int(np.sum(counts))
    ax.set_xlabel(f"position (0 = top)   ·   {flavor_label}", fontsize=11,
                  color=MUTED, family="Georgia", style="italic", labelpad=8)
    ax.set_ylabel("click rate (% of records at this position)", fontsize=11,
                  color=MUTED, family="Georgia")
    ax.set_title(f"{title}   ·   n = {total_n:,} AOIs   ·   ρ = {rho:+.3f}",
                 fontsize=12, color=INK, family="Georgia", pad=10)
    ax.set_xticks(positions)
    ax.set_xticklabels([f"{p}\nn={c:,}" for p, c in zip(positions, counts)],
                       fontsize=7.5, color=MUTED)
    ax.set_ylim(0, max(rates.max() * 1.18, 30))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(RULE)
    ax.spines["bottom"].set_color(RULE)
    ax.tick_params(colors=MUTED)
    ax.grid(axis="y", alpha=0.18, linewidth=0.6)
    ax.set_facecolor(BG)


def render() -> None:
    org_pos, org_rates, org_counts, org_etypes = load_flavor(AF / "cursor-approach-features-organic.json")
    hyb_pos, hyb_rates, hyb_counts, hyb_etypes = load_flavor(AF / "cursor-approach-features-organic-hybrid.json")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=BG)
    render_panel(ax1, org_pos, org_rates, org_counts, org_etypes,
                 color=ACCENT, title="Organic-only flavor",
                 flavor_label="rank 0 = topmost organic")
    render_panel(ax2, hyb_pos, hyb_rates, hyb_counts, hyb_etypes,
                 color=ACCENT2, title="Organic-hybrid flavor",
                 flavor_label="rank 0 = topmost main-axis card (often dd_top)")

    # Legend explaining the dd_top hue swap
    fig.text(0.5, 0.005,
             "Orange bar: position where dd_top dominates under the organic-hybrid flavor.",
             ha="center", va="bottom", fontsize=9, color=MUTED, family="Georgia", style="italic")

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(OUT_PNG, dpi=160, bbox_inches="tight", facecolor=BG)
    plt.savefig(OUT_PDF, bbox_inches="tight", facecolor=BG)
    print(f"wrote {OUT_PNG}", file=sys.stderr)
    print(f"wrote {OUT_PDF}", file=sys.stderr)


if __name__ == "__main__":
    render()
