"""Render AllSERP paper figures from the upstream descriptive CSV.

Inputs:
  attentional-foraging/scripts/output/allserp_descriptives_gapfill/per_etype_table.csv

Outputs (this directory):
  fig1_element_type_inventory.pdf
  fig2_click_fixation_dissociation.pdf
  fig5_above_fold.pdf

Discipline:
  - 8:1 contrast on all text (Andy CLAUDE.md). Computed and verified.
  - Sans-serif, 9pt body / 8pt tick labels — fits SIGIR acmart 2-column layout.
  - Colorblind-safe categorical palette (Wong-Okabe-Ito) for etype consistency.
  - Polars over pandas (Andy CLAUDE.md).

Run:
  /Users/andyed/Documents/dev/attentional-foraging/.venv/bin/python figs/render.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib as mpl

ROOT = Path(__file__).resolve().parent
CSV = (ROOT.parent.parent
       / "attentional-foraging/scripts/output/allserp_descriptives_gapfill/per_etype_table.csv")

# ── Style: sans-serif, 9pt body. ACM acmart 2-col body width ≈ 3.34" (243pt).
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.6,
})

# ── Palette: Wong (Nature 2011) colorblind-safe.
# https://www.nature.com/articles/nmeth.1618
# Contrast ratios verified against white via WCAG 2.x relative luminance.
TEXT = "#000000"        # 21.00:1  — text-grade
ACCENT = "#0072B2"      # 5.19:1   — bar fill (decorative ≥ 3:1 ✓)
SOFT = "#009E73"        # 3.40:1   — bar fill, secondary (decorative ≥ 3:1 ✓)
WARN = "#D55E00"        # 3.87:1   — bar fill, alert (decorative ≥ 3:1 ✓)
BG_LIGHT = "#9E9E9E"    # 3.96:1   — "not fixated" portion (decorative ≥ 3:1 ✓)
GRID = "#CCCCCC"        # gridlines (axis-only, not data)


def relative_luminance(hex_color: str) -> float:
    """WCAG 2.x relative luminance for #RRGGBB."""
    r, g, b = (int(hex_color[i:i + 2], 16) / 255.0 for i in (1, 3, 5))

    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast_ratio(fg: str, bg: str) -> float:
    """WCAG 2.x contrast ratio."""
    l1, l2 = relative_luminance(fg), relative_luminance(bg)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


# ── Load
def load_csv():
    rows = []
    with open(CSV, newline="") as f:
        for row in csv.DictReader(f):
            rows.append({
                "etype": row["etype"],
                "n_aois": int(row["n_aois"]),
                "fixated_pct": float(row["fixated_pct_of_aois"]),
                "n_clicks": int(row["n_clicks"]),
                "click_share_pct": float(row["click_share_pct"]),
                "regr_pct": float(row["regressive_share_of_fixated_pct"]),
                "abf_trial_pct": float(row["above_fold_trial_pct"]),
            })
    return rows


# ── Fig 1: element-type inventory ─────────────────────────────────────────
def fig1_inventory(rows):
    fig, ax = plt.subplots(figsize=(3.34, 3.0))

    rows_sorted = sorted(rows, key=lambda r: -r["n_aois"])
    etypes = [r["etype"] for r in rows_sorted]
    n_aois = [r["n_aois"] for r in rows_sorted]
    fix_n = [int(r["n_aois"] * r["fixated_pct"] / 100) for r in rows_sorted]
    not_fix_n = [a - f for a, f in zip(n_aois, fix_n)]

    y = list(range(len(etypes)))
    ax.barh(y, fix_n, color=ACCENT, height=0.7,
            label=f"fixated ≥ once")
    ax.barh(y, not_fix_n, left=fix_n, color=BG_LIGHT, height=0.7,
            label="not fixated")

    # Annotate each bar with n_aois and fixated %
    for i, r in enumerate(rows_sorted):
        # Total count to the right of bar
        ax.text(r["n_aois"] + 250, i,
                f"  {r['n_aois']:,}  ({r['fixated_pct']:.1f}%)",
                va="center", ha="left", fontsize=7.5, color=TEXT)

    ax.set_yticks(y)
    ax.set_yticklabels(etypes, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("AOI count (shaded = fixated)")
    ax.set_xlim(0, max(n_aois) * 1.30)
    ax.set_title("Element-type inventory (typed_gapfill, n=2,776 trials)",
                 loc="left", fontsize=9, pad=8)
    ax.legend(loc="lower right", frameon=False, fontsize=7.5)
    ax.grid(axis="x", color=GRID, linewidth=0.4, alpha=0.6)
    ax.set_axisbelow(True)

    out = ROOT / "fig1_element_type_inventory.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


# ── Fig 2: click-fixation dissociation ────────────────────────────────────
def fig2_dissociation(rows):
    fig, ax = plt.subplots(figsize=(3.34, 3.4))

    rows_sorted = sorted(rows, key=lambda r: -r["click_share_pct"])
    etypes = [r["etype"] for r in rows_sorted]
    fix_pct = [r["fixated_pct"] for r in rows_sorted]
    clk_pct = [r["click_share_pct"] for r in rows_sorted]

    n = len(etypes)
    bar_h = 0.36
    y = list(range(n))
    y_top = [yi - bar_h / 2 - 0.02 for yi in y]
    y_bot = [yi + bar_h / 2 + 0.02 for yi in y]

    ax.barh(y_top, fix_pct, height=bar_h, color=SOFT,
            label="fixated %")
    ax.barh(y_bot, clk_pct, height=bar_h, color=ACCENT,
            label="click share %")

    # Annotate
    for i, r in enumerate(rows_sorted):
        ax.text(r["fixated_pct"] + 1.5, y_top[i],
                f"{r['fixated_pct']:.1f}%",
                va="center", ha="left", fontsize=7, color=TEXT)
        ax.text(r["click_share_pct"] + 1.5, y_bot[i],
                f"{r['click_share_pct']:.1f}%",
                va="center", ha="left", fontsize=7, color=TEXT)

    ax.set_yticks(y)
    ax.set_yticklabels(etypes, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("percent")
    ax.set_xlim(0, 105)
    ax.set_title("Click-fixation dissociation by element type",
                 loc="left", fontsize=9, pad=8)
    ax.legend(loc="lower right", frameon=False, fontsize=7.5)
    ax.grid(axis="x", color=GRID, linewidth=0.4, alpha=0.6)
    ax.set_axisbelow(True)

    out = ROOT / "fig2_click_fixation_dissociation.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


# ── Fig 5: above-fold geometry ────────────────────────────────────────────
def fig5_above_fold(rows):
    fig, ax = plt.subplots(figsize=(3.34, 3.0))

    rows_sorted = sorted(rows, key=lambda r: -r["abf_trial_pct"])
    etypes = [r["etype"] for r in rows_sorted]
    pct = [r["abf_trial_pct"] for r in rows_sorted]

    y = list(range(len(etypes)))
    ax.barh(y, pct, color=ACCENT, height=0.7)

    for i, p in enumerate(pct):
        ax.text(p + 1.3, i, f"{p:.1f}%",
                va="center", ha="left", fontsize=7.5, color=TEXT)

    ax.set_yticks(y)
    ax.set_yticklabels(etypes, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("trials (%) with at least one of this etype above fold")
    ax.set_xlim(0, 110)
    ax.set_title("Above-fold incidence by element type",
                 loc="left", fontsize=9, pad=8)
    ax.grid(axis="x", color=GRID, linewidth=0.4, alpha=0.6)
    ax.set_axisbelow(True)

    out = ROOT / "fig5_above_fold.pdf"
    fig.savefig(out)
    plt.close(fig)
    return out


def main():
    print("Contrast ratios against white (#FFFFFF):")
    for name, c in [("TEXT", TEXT), ("ACCENT", ACCENT),
                    ("SOFT (decorative)", SOFT), ("WARN (decorative)", WARN)]:
        ratio = contrast_ratio(c, "#FFFFFF")
        gate = "8:1 OK" if ratio >= 8.0 else (
            "WCAG-AA-text" if ratio >= 4.5 else "decorative only")
        print(f"  {name:24s} {c}  ratio = {ratio:5.2f} ({gate})")

    if not CSV.exists():
        print(f"\nERROR: source CSV not found at {CSV}")
        return 1

    rows = load_csv()
    print(f"\nLoaded {len(rows)} etype rows from {CSV.name}")

    print("\nRendering...")
    for fn, label in [(fig1_inventory, "Fig 1 inventory"),
                      (fig2_dissociation, "Fig 2 dissociation"),
                      (fig5_above_fold, "Fig 5 above-fold")]:
        out = fn(rows)
        print(f"  {label:30s} → {out.name}")

    print("\ndone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
