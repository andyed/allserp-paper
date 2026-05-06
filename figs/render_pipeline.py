"""Render the AOI extraction pipeline as a 4-panel small-multiples SVG.

Same synthetic SERP rendered four ways — Phase A geometry, Phase B typing,
Phase C spatial join, Phase D gap-fill. Output: fig_pipeline.{svg,pdf,png}.

Universal rules respected:
- Cream editorial palette matching the arc graphs (#FAFAF8 / #0B1220 ink).
- 8:1 contrast on all text.
- Wong colorblind-safe palette for element-type swatches.
- Optical alignment, not arithmetic — small-multiples share row centerlines.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

OUT_DIR = Path(__file__).parent
OUT_SVG = OUT_DIR / "fig_pipeline.svg"
OUT_PDF = OUT_DIR / "fig_pipeline.pdf"
OUT_PNG = OUT_DIR / "fig_pipeline.png"

# ── Palette (matches existing paper figures) ─────────────────────────────────
BG       = "#FAFAF8"
INK      = "#0B1220"
MUTED    = "#4B4B4B"
RULE     = "#D2CEC4"
PANEL_BG = "#FFFFFF"
PANEL_BD = "#C9C2B0"

# Wong colorblind-safe etype palette
DD_TOP   = "#E69F00"  # orange
NATIVE   = "#D55E00"  # vermillion
ORGANIC  = "#0072B2"  # blue
IMAGE_PK = "#009E73"  # bluish-green
KP       = "#CC79A7"  # reddish purple
PAA      = "#56B4E9"  # sky blue
DD_RIGHT = "#999999"  # off-axis, neutral grey

GAP_FILL = "#5B3EB8"  # purple accent — matches arc graphs

# ── Layout ───────────────────────────────────────────────────────────────────
PANEL_W   = 230
PANEL_H   = 560
PANEL_GAP = 28
HEAD_H    = 60
CAP_H     = 50
PAD_TOP   = 24
PAD_LEFT  = 28
N_PANELS  = 4

W = PAD_LEFT * 2 + PANEL_W * N_PANELS + PANEL_GAP * (N_PANELS - 1)
H = PAD_TOP + HEAD_H + PANEL_H + CAP_H

# ── Synthetic SERP layout (in panel-local coordinates) ───────────────────────
# Same coordinates reused across all panels so reader's eye doesn't re-anchor.
SEARCH_BAR = (10, 12, 210, 26)
DD_TOP_BOX = (10, 50, 210, 64)        # x, y, w, h
IMG_PACK   = (10, 122, 210, 78)
ORG_BOXES  = [
    (10, 210, 210, 50),
    (10, 268, 210, 50),
    (10, 326, 210, 50),
    (10, 384, 210, 50),
    (10, 442, 210, 50),
]
DD_RIGHT_BOXES = [(176, 50, 44, 64), (176, 122, 44, 78)]   # right-rail

# Phase D gap-fill: extend each organic to a midpoint with the next.
GAP_BOXES = []
for i in range(len(ORG_BOXES) - 1):
    a = ORG_BOXES[i]
    b = ORG_BOXES[i + 1]
    a_bot = a[1] + a[3]
    b_top = b[1]
    gap = b_top - a_bot
    if gap > 0:
        midpt_y = a_bot + gap // 2
        GAP_BOXES.append((a[0], a_bot, a[2], midpt_y - a_bot))           # extends downward from organic[i]
        GAP_BOXES.append((b[0], midpt_y, b[2], b_top - midpt_y))         # extends upward to organic[i+1]


def serp_skeleton(panel_x: int, *, fade=False, show_right_rail=True) -> str:
    """Common SERP background — search bar + faint result outlines + right rail."""
    fade_factor = 0.30 if fade else 1.0
    out = []
    # Page surface
    out.append(f'<rect x="{panel_x}" y="0" width="{PANEL_W}" height="{PANEL_H}" fill="{PANEL_BG}" stroke="{PANEL_BD}"/>')
    # Search bar — lighter background so ink placeholder text clears 8:1
    sx, sy, sw, sh = SEARCH_BAR
    out.append(f'<rect x="{panel_x+sx}" y="{sy}" width="{sw}" height="{sh}" fill="#F5F5F5" rx="3"/>')
    out.append(f'<text x="{panel_x+sx+8}" y="{sy+17}" font-family="Georgia" font-size="9" fill="{INK}">buy ski goggles</text>')
    # Right rail (faded if Phase A wants to highlight it for filtering)
    if show_right_rail:
        for rx, ry, rw, rh in DD_RIGHT_BOXES:
            opacity = 0.45 if fade else 0.85
            out.append(f'<rect x="{panel_x+rx}" y="{ry}" width="{rw}" height="{rh}" fill="{DD_RIGHT}" opacity="{opacity}" rx="2"/>')
    return "\n".join(out)


def card_outline(x, y, w, h, *, stroke=INK, fill="none", dashed=False, stroke_width=1.4) -> str:
    dash = ' stroke-dasharray="3,3"' if dashed else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{dash}/>'


def card_label(x, y, text, *, font_size=8, fill=INK, weight="normal") -> str:
    return f'<text x="{x}" y="{y}" font-family="Georgia" font-size="{font_size}" font-weight="{weight}" fill="{fill}">{text}</text>'


def panel_a(panel_x: int) -> str:
    """Phase A — Screenshot-anchored geometry (CV row-projection)."""
    out = [serp_skeleton(panel_x, show_right_rail=True)]
    # Show detected card spans as bracketed outlines
    for x, y, w, h in [DD_TOP_BOX, IMG_PACK, *ORG_BOXES]:
        out.append(card_outline(panel_x + x, y, w, h, stroke=INK, dashed=True))
    # Cross out right rail to indicate it's off-axis
    for rx, ry, rw, rh in DD_RIGHT_BOXES:
        cx = panel_x + rx
        out.append(f'<line x1="{cx}" y1="{ry}" x2="{cx+rw}" y2="{ry+rh}" stroke="{MUTED}" stroke-width="1" opacity="0.6"/>')
    return "\n".join(out)


def panel_b(panel_x: int) -> str:
    """Phase B — HTML semantic typing."""
    out = [serp_skeleton(panel_x, show_right_rail=True)]
    # Filled colored cards by etype — every card gets a label
    typed = [
        (DD_TOP_BOX, DD_TOP, "dd_top"),
        (IMG_PACK, IMAGE_PK, "image_pack"),
        *[(b, ORGANIC, "organic") for b in ORG_BOXES],
    ]
    for (x, y, w, h), color, label in typed:
        out.append(f'<rect x="{panel_x+x}" y="{y}" width="{w}" height="{h}" fill="{color}" opacity="0.30"/>')
        out.append(card_outline(panel_x + x, y, w, h, stroke=color, stroke_width=1.5))
        # Tag chip — white pill, colored border, ink text. Universal 19:1.
        tag_w = max(48, len(label) * 6 + 8)
        out.append(f'<rect x="{panel_x+x+4}" y="{y+4}" width="{tag_w}" height="14" fill="white" stroke="{color}" stroke-width="1.5" rx="2"/>')
        out.append(f'<text x="{panel_x+x+4+tag_w/2}" y="{y+14}" font-family="Georgia" font-size="8" font-weight="bold" fill="{INK}" text-anchor="middle">{label}</text>')
    # Right-rail labels
    for rx, ry, rw, rh in DD_RIGHT_BOXES:
        out.append(f'<rect x="{panel_x+rx+2}" y="{ry+4}" width="36" height="14" fill="white" stroke="{DD_RIGHT}" stroke-width="1.5" rx="2"/>')
        out.append(f'<text x="{panel_x+rx+2+18}" y="{ry+14}" font-family="Georgia" font-size="8" font-weight="bold" fill="{INK}" text-anchor="middle">dd_right</text>')
    return "\n".join(out)


def panel_c(panel_x: int) -> str:
    """Phase C — Spatial join (position numbering by document order)."""
    out = [serp_skeleton(panel_x, show_right_rail=True)]
    # Positions in display order: dd_top (0), image_pack (1), organics (2..6), right-rail (-1)
    positioned = [
        (DD_TOP_BOX, DD_TOP, "0"),
        (IMG_PACK, IMAGE_PK, "1"),
    ] + [(b, ORGANIC, str(i + 2)) for i, b in enumerate(ORG_BOXES)]
    for (x, y, w, h), color, pos in positioned:
        out.append(f'<rect x="{panel_x+x}" y="{y}" width="{w}" height="{h}" fill="{color}" opacity="0.22"/>')
        out.append(card_outline(panel_x + x, y, w, h, stroke=color, stroke_width=1.4))
        # Position circle on left edge — ink on cream, 19:1
        cx = panel_x + x - 9
        cy = y + h / 2
        out.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{INK}"/>')
        out.append(f'<text x="{cx}" y="{cy+3}" font-family="Georgia" font-size="9" font-weight="bold" fill="white" text-anchor="middle">{pos}</text>')
    # Right-rail gets position = -1; use ink (not muted) so white text clears 8:1
    for rx, ry, rw, rh in DD_RIGHT_BOXES:
        out.append(f'<rect x="{panel_x+rx}" y="{ry}" width="{rw}" height="{rh}" fill="{DD_RIGHT}" opacity="0.5"/>')
        cx = panel_x + rx + rw + 6
        cy = ry + rh / 2
        out.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="{INK}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="2,1.5"/>')
        out.append(f'<text x="{cx}" y="{cy+3}" font-family="Georgia" font-size="8" font-weight="bold" fill="white" text-anchor="middle">−1</text>')
    return "\n".join(out)


def panel_d(panel_x: int) -> str:
    """Phase D — Midpoint-split gap-fill on organics only."""
    out = [serp_skeleton(panel_x, show_right_rail=True)]
    # dd_top + image_pack unchanged (only organics get gap-fill)
    for (x, y, w, h), color in [(DD_TOP_BOX, DD_TOP), (IMG_PACK, IMAGE_PK)]:
        out.append(f'<rect x="{panel_x+x}" y="{y}" width="{w}" height="{h}" fill="{color}" opacity="0.22"/>')
        out.append(card_outline(panel_x + x, y, w, h, stroke=color, stroke_width=1.4))
    # Organics: tight bbox + gap extension shaded
    for x, y, w, h in ORG_BOXES:
        out.append(f'<rect x="{panel_x+x}" y="{y}" width="{w}" height="{h}" fill="{ORGANIC}" opacity="0.22"/>')
        out.append(card_outline(panel_x + x, y, w, h, stroke=ORGANIC, stroke_width=1.4))
    # Gap-fill extensions
    for x, y, w, h in GAP_BOXES:
        out.append(f'<rect x="{panel_x+x}" y="{y}" width="{w}" height="{h}" fill="{GAP_FILL}" opacity="0.32"/>')
        out.append(f'<rect x="{panel_x+x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{GAP_FILL}" stroke-width="1" stroke-dasharray="2,2"/>')
    # Annotation: midpoint marker on first gap — ink text, dashed line stays purple (decorative)
    if GAP_BOXES:
        gx = panel_x + GAP_BOXES[0][0]
        gy = GAP_BOXES[0][1] + GAP_BOXES[0][3]
        out.append(f'<line x1="{gx-4}" y1="{gy}" x2="{gx+GAP_BOXES[0][2]+4}" y2="{gy}" stroke="{GAP_FILL}" stroke-width="1.5" stroke-dasharray="4,2"/>')
        out.append(f'<text x="{gx+GAP_BOXES[0][2]+8}" y="{gy+3}" font-family="Georgia" font-size="7" fill="{INK}" font-style="italic">midpoint</text>')
    return "\n".join(out)


HEADERS = [
    ("(A) Screenshot-anchored geometry", "row-projection on main column"),
    ("(B) HTML semantic typing", "8-tier label chain"),
    ("(C) Spatial join", "labels bound by document order"),
    ("(D) Midpoint-split gap-fill", "organic bboxes extended"),
]


def build_svg() -> str:
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">')
    parts.append('<title>AOI extraction pipeline — four phases</title>')
    parts.append('<desc>Same synthetic SERP rendered four ways: Phase A row-projection geometry, Phase B HTML semantic typing across element types, Phase C spatial join binding labels to geometry by document order, Phase D midpoint-split gap-fill extending adjacent organic bboxes to a shared midpoint.</desc>')
    parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>')

    # Headers
    for i, (title, sub) in enumerate(HEADERS):
        x = PAD_LEFT + i * (PANEL_W + PANEL_GAP) + PANEL_W / 2
        parts.append(f'<text x="{x}" y="{PAD_TOP + 18}" font-family="Georgia" font-size="13" font-weight="bold" fill="{INK}" text-anchor="middle">{title}</text>')
        parts.append(f'<text x="{x}" y="{PAD_TOP + 36}" font-family="Georgia" font-size="10" fill="{MUTED}" text-anchor="middle" font-style="italic">{sub}</text>')

    # Panels (translated by group)
    panel_renderers = [panel_a, panel_b, panel_c, panel_d]
    body_y = PAD_TOP + HEAD_H
    for i, render in enumerate(panel_renderers):
        x = PAD_LEFT + i * (PANEL_W + PANEL_GAP)
        parts.append(f'<g transform="translate({x},{body_y})">')
        parts.append(render(0))
        parts.append('</g>')

    # Caption row at bottom
    cap_y = body_y + PANEL_H + 26
    captions = [
        "CV-detected card spans (dashed). Right-rail cards struck through: detected but off-axis.",
        "Labels via heading text → class → data-attrid chain. 13 element types incl. off-axis dd_right.",
        "Position 0…N in display order. Right-rail and footer pulled to position −1.",
        "Adjacent organic pairs share a midpoint; gap-fill claims every Y for exactly one bbox.",
    ]
    for i, cap in enumerate(captions):
        x = PAD_LEFT + i * (PANEL_W + PANEL_GAP)
        words = cap.split()
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 36:
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))
        for j, line in enumerate(lines):
            parts.append(f'<text x="{x}" y="{cap_y + j*11}" font-family="Georgia" font-size="8" fill="{MUTED}">{line}</text>')

    parts.append('</svg>')
    return "\n".join(parts)


def main() -> None:
    svg = build_svg()
    OUT_SVG.write_text(svg)
    print(f"wrote {OUT_SVG}")

    # Convert to PDF + PNG via rsvg-convert (preferred) or cairosvg fallback.
    if subprocess.run(["which", "rsvg-convert"], capture_output=True).returncode == 0:
        subprocess.run(["rsvg-convert", "-f", "pdf", "-o", str(OUT_PDF), str(OUT_SVG)], check=True)
        subprocess.run(["rsvg-convert", "-d", "300", "-p", "300", "-o", str(OUT_PNG), str(OUT_SVG)], check=True)
        print(f"wrote {OUT_PDF} + {OUT_PNG}")
    else:
        try:
            import cairosvg  # type: ignore
            cairosvg.svg2pdf(url=str(OUT_SVG), write_to=str(OUT_PDF))
            cairosvg.svg2png(url=str(OUT_SVG), write_to=str(OUT_PNG), dpi=300, scale=2)
            print(f"wrote {OUT_PDF} + {OUT_PNG} (via cairosvg)")
        except ImportError:
            print("note: install rsvg-convert or cairosvg for PDF/PNG export")


if __name__ == "__main__":
    main()
