"""Anatomy of the dd_top cell split (two panels).

Left:  carousel size distribution — how many cells a top-ads carousel holds
       (modal 4). Source: attentional-foraging nb25_cellsplit_composition.
Right: within-carousel click distribution on the modal 4-cell carousel —
       of clicks landing inside the carousel, which cell? Leftmost is
       favored (~32% vs 25% uniform) but clicks spread across all cells;
       the block-level dd_top AOI conflates this. Source: attentional-
       foraging cellsplit_click_composition (from the shipped flavor).

All text is rendered in INK on BG (contrast ratio ~18:1, well above the 8:1
floor); the 25% reference line and axis rules use RULE/MUTED (non-text).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).parent
OUT_PNG = OUT_DIR / "fig_cellsplit_composition.png"
OUT_PDF = OUT_DIR / "fig_cellsplit_composition.pdf"

AF = Path("/Users/andyed/Documents/dev/attentional-foraging/scripts/output")
SIZE_CSV = AF / "nb25_cellsplit_composition" / "cells_per_carousel.csv"
CLICK_CSV = AF / "cellsplit_click_composition" / "by_cell_index.csv"

ACCENT  = "#5B3EB8"
ACCENT2 = "#26A69A"
INK     = "#0B1220"   # all text: ~18:1 on BG
RULE    = "#D2CEC4"
BG      = "#FAFAF8"
DD_TOP_HUE = "#E69F00"


def read_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def render() -> None:
    size = read_csv(SIZE_CSV)          # n_cells, count, pct
    clicks = read_csv(CLICK_CSV)       # cell_index, count, pct

    n_cells = [int(r["n_cells"]) for r in size]
    size_pct = [float(r["pct"]) for r in size]
    size_n = [int(r["count"]) for r in size]
    n_carousels = sum(size_n)

    idx = [int(r["cell_index"]) for r in clicks]
    clk_pct = [float(r["pct"]) for r in clicks]
    clk_n = [int(r["count"]) for r in clicks]
    n_modal_clicks = sum(clk_n)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=BG)

    # ---- Panel A: carousel size distribution ----
    barsA = ax1.bar(n_cells, size_pct, color=ACCENT, edgecolor=INK,
                    linewidth=0.5, width=0.72)
    for nc, bar in zip(n_cells, barsA):
        if nc == 4:
            bar.set_color(DD_TOP_HUE); bar.set_edgecolor(INK)
    for x, p in zip(n_cells, size_pct):
        ax1.text(x, p + 1.0, f"{p:.1f}%", ha="center", va="bottom",
                 fontsize=9, color=INK, family="Georgia")
    ax1.set_xlabel("cells per top-ads carousel", fontsize=11, color=INK,
                   family="Georgia", labelpad=8)
    ax1.set_ylabel("% of carousels", fontsize=11, color=INK, family="Georgia")
    ax1.set_title(f"Carousel size   ·   n = {n_carousels:,} carousels",
                  fontsize=12, color=INK, family="Georgia", pad=10)
    ax1.set_xticks(n_cells)
    ax1.set_xticklabels([f"{x}\nn={c:,}" for x, c in zip(n_cells, size_n)],
                        fontsize=9, color=INK)
    ax1.set_ylim(0, max(size_pct) * 1.18)

    # ---- Panel B: within-carousel click distribution (modal 4-cell) ----
    barsB = ax2.bar(idx, clk_pct, color=ACCENT2, edgecolor=INK,
                    linewidth=0.5, width=0.72)
    barsB[0].set_color(DD_TOP_HUE); barsB[0].set_edgecolor(INK)  # leftmost
    for x, p in zip(idx, clk_pct):
        ax2.text(x, p + 0.8, f"{p:.1f}%", ha="center", va="bottom",
                 fontsize=9, color=INK, family="Georgia")
    ax2.axhline(25.0, color=INK, linestyle=(0, (4, 3)), linewidth=1.0, alpha=0.55)
    ax2.text(idx[0] - 0.42, 25.7, "25% uniform", ha="left", va="bottom",
             fontsize=9, color=INK, family="Georgia", style="italic")
    ax2.set_xlabel("cell index within carousel (0 = leftmost)", fontsize=11,
                   color=INK, family="Georgia", labelpad=8)
    ax2.set_ylabel("% of within-carousel clicks", fontsize=11, color=INK,
                   family="Georgia")
    ax2.set_title(f"Within-carousel clicks (4-cell)   ·   n = {n_modal_clicks} clicks",
                  fontsize=12, color=INK, family="Georgia", pad=10)
    ax2.set_xticks(idx)
    ax2.set_xticklabels([f"{x}\nn={c}" for x, c in zip(idx, clk_n)],
                        fontsize=9, color=INK)
    ax2.set_ylim(0, max(max(clk_pct) * 1.18, 30))

    for ax in (ax1, ax2):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(RULE)
        ax.spines["bottom"].set_color(RULE)
        ax.tick_params(colors=INK)
        ax.grid(axis="y", alpha=0.18, linewidth=0.6)
        ax.set_facecolor(BG)

    fig.text(0.5, 0.005,
             "Orange: modal 4-cell carousel (left) and its leftmost cell (right). "
             "The block-level dd_top AOI conflates the right-panel distribution.",
             ha="center", va="bottom", fontsize=9, color=INK,
             family="Georgia", style="italic")

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(OUT_PNG, dpi=160, bbox_inches="tight", facecolor=BG)
    plt.savefig(OUT_PDF, bbox_inches="tight", facecolor=BG)
    print(f"wrote {OUT_PNG}", file=sys.stderr)
    print(f"wrote {OUT_PDF}", file=sys.stderr)


if __name__ == "__main__":
    render()
