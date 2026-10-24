"""Render all-AOI final-click rates from allserp_rank_inventory.py output.

Example: python figs/render_rank_effects.py --source /path/to/summary.json
The producer uses the released organic_hybrid CSV for both conventions,
screenshot-space X+Y attribution, and all AOIs including unfixated ones.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent
INK, MUTED, RULE, BG = '#0B1220', '#4B4B4B', '#D2CEC4', '#FAFAF8'


def render_panel(ax, data, color, title, label):
    rows = [r for r in data['by_position'] if 0 <= r['position'] <= 9]
    positions = [r['position'] for r in rows]
    rates = [100 * r['click_rate'] for r in rows]
    colors = ['#E69F00' if max(r['etypes'], key=r['etypes'].get) == 'dd_top' else color for r in rows]
    ax.bar(positions, rates, color=colors, edgecolor=INK, linewidth=.5, width=.78)
    for p, rate in zip(positions, rates):
        ax.text(p, rate + .7, f'{rate:.1f}%', ha='center', va='bottom', fontsize=9, color=INK)
    ax.set_title(f'{title} · n = {sum(r["n_aois"] for r in rows):,} AOIs',
                 fontsize=12, color=INK, pad=10)
    ax.set_xlabel(f'position (0 = top) · {label}', fontsize=10, color=MUTED, labelpad=8)
    ax.set_ylabel('final clicks / all AOIs at position (%)', fontsize=10, color=MUTED)
    ax.set_xticks(positions)
    ax.set_xticklabels([f'{r["position"]}\nn={r["n_aois"]:,}' for r in rows], fontsize=7.5)
    ax.set_ylim(0, max(max(rates, default=0)*1.2, 30))
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color(RULE)
    ax.tick_params(colors=MUTED)
    ax.grid(axis='y', alpha=.18, linewidth=.6)
    ax.set_facecolor(BG)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.source.read_text())
    if data['provenance']['schema'] != 'allserp-rank-inventory-v1':
        raise ValueError('Expected the audited all-AOI inventory, not historical feature caches')
    plt.rcParams['font.family'] = 'DejaVu Sans'
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), facecolor=BG)
    render_panel(axes[0], data['flavors']['organic'], '#5B3EB8',
                 'Organic-only positions', 'topmost organic = 0')
    render_panel(axes[1], data['flavors']['organic_hybrid'], '#26A69A',
                 'Organic-hybrid positions', 'topmost main-axis box = 0')
    shared_max = max(100 * r['click_rate'] for flavor in data['flavors'].values()
                     for r in flavor['by_position'] if r['position'] <= 9)
    for ax in axes:
        ax.set_ylim(0, max(shared_max * 1.2, 30))
    fig.text(.5, .015,
             f'{data["n_trials"]:,} export trials · screenshot-space X+Y final clicks · all AOIs, including those never fixated',
             ha='center', va='bottom', fontsize=9, color=MUTED)
    plt.tight_layout(rect=[0, .06, 1, 1])
    for suffix in ('png', 'pdf'):
        path = OUT_DIR / f'fig_rank_effects.{suffix}'
        fig.savefig(path, dpi=160, bbox_inches='tight', facecolor=BG)
        print(path)
    plt.close(fig)
    metadata = {'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
                'renderer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'source_provenance': data['provenance'], 'shown_positions': [0, 9],
                'note': 'Orange identifies positions where dd_top is the most frequent element type.'}
    (OUT_DIR / 'fig_rank_effects.provenance.json').write_text(json.dumps(metadata, indent=2)+'\n')


if __name__ == '__main__':
    main()
