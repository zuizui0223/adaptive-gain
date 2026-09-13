from __future__ import annotations

from fractions import Fraction
from html import escape
from pathlib import Path
import math

from adaptive_gain.routing_layer_modality import (
    aggregate_layer_weights,
    aggregate_modal_tilt_threshold,
    distance_layer_degeneracy,
    full_layer_stationary_mass,
    minimum_population_size_for_stationary_majority,
    minimum_population_size_for_unique_modal_full_layer,
    weakest_branch_layer_degeneracy,
)

OUT = Path(__file__).resolve().parent
W, H = 1600, 900
BLACK = "#111111"
MID = "#61666c"
LIGHT = "#f2f3f4"
GRID = "#d7dadd"
WHITE = "#ffffff"


def text(x, y, value, size=22, weight="normal", anchor="start", fill=BLACK):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" fill="{fill}">{escape(str(value))}</text>'
    )


def rect(x, y, w, h, fill=WHITE, stroke=BLACK, sw=2, rx=10):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def line(x1, y1, x2, y2, stroke=BLACK, sw=2, dash=None, arrow=False):
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    marker = ' marker-end="url(#arrow)"' if arrow else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{stroke}" stroke-width="{sw}"{dashed}{marker}/>'
    )


def circle(cx, cy, r, fill=LIGHT, stroke=BLACK, sw=2):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"/>'
    )


def polyline(points, stroke=BLACK, sw=3, dash=None):
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{pts}" fill="none" stroke="{stroke}" stroke-width="{sw}"{dashed}/>'


def base(title, subtitle=None):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="{WHITE}"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#111111"/></marker></defs>',
        '<style>text{font-family:Arial,Helvetica,sans-serif}</style>',
        text(50, 55, title, 34, "bold"),
    ]
    if subtitle:
        parts.append(text(50, 88, subtitle, 19, fill=MID))
    return parts


def finish(parts, filename, out_dir=OUT):
    parts.append("</svg>")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def _axis(parts, x0, y0, x1, y1, xlabel=None, ylabel=None):
    parts.extend([line(x0, y0, x1, y0), line(x0, y0, x0, y1)])
    if xlabel:
        parts.append(text((x0 + x1) / 2, y0 + 48, xlabel, 17, anchor="middle"))
    if ylabel:
        parts.append(text(x0 - 38, (y0 + y1) / 2, ylabel, 17, anchor="middle"))


def _majority_root_q2_k3():
    return (7.0 + 5.0 * math.sqrt(5.0)) / 2.0


def figure1(out_dir=OUT):
    q, k = 2, 3
    counts = tuple(weakest_branch_layer_degeneracy(q, k, r) for r in range(q + 1))
    assert counts == (19, 7, 1)

    p = base(
        "Finite routing representation creates an exact gain-layer multiplicity profile",
        "Running example: q = 2 gain steps, k = 3 routing branches",
    )
    p += [text(45, 145, "A", 28, "bold"), text(85, 145, "Weakest-branch routing map", 25, "bold")]

    coords = [(160, 240), (330, 240), (500, 240)]
    for i, (x, y) in enumerate(coords, start=1):
        p += [rect(x, y, 120, 90, LIGHT), text(x + 60, y + 35, f"x{i}", 19, "bold", "middle"), text(x + 60, y + 68, "0,1,2", 20, anchor="middle")]
    p += [line(620, 285, 735, 285, arrow=True), rect(755, 235, 310, 100, LIGHT), text(910, 272, "g(x) = min(x1,x2,x3)", 21, "bold", "middle"), text(910, 307, "gain is set by the weakest branch", 18, anchor="middle", fill=MID)]

    p += [text(45, 420, "B", 28, "bold"), text(85, 420, "Exact genotype counts by gain", 25, "bold")]
    chart_x0, chart_y0, chart_w, chart_h = 130, 740, 760, 250
    _axis(p, chart_x0, chart_y0, chart_x0 + chart_w, chart_y0 - chart_h, "gain r", "genotype count")
    maxc = max(counts)
    bar_w = 130
    positions = [250, 500, 750]
    for r, c, cx in zip(range(3), counts, positions):
        bh = chart_h * c / maxc
        p += [rect(cx - bar_w / 2, chart_y0 - bh, bar_w, bh, LIGHT), text(cx, chart_y0 - bh - 18, c, 22, "bold", "middle"), text(cx, chart_y0 + 30, r, 18, anchor="middle")]

    p += [rect(980, 445, 510, 270, WHITE), text(1235, 485, "General layer formula", 23, "bold", "middle"), text(1235, 535, "D_r = (q-r+1)^k - (q-r)^k", 23, anchor="middle"), text(1235, 585, "A_s = (s+1)^k - s^k", 23, anchor="middle"), text(1235, 625, "s = q-r", 18, anchor="middle", fill=MID), text(1235, 675, "Adjacent layer: A_1 = 2^k - 1", 21, "bold", "middle")]
    p += [rect(980, 750, 510, 85, LIGHT), text(1235, 785, "Unique full-gain genotype: D_q = 1", 20, "bold", "middle"), text(1235, 816, "but D_(q-1) = 2^k - 1", 19, anchor="middle", fill=MID)]
    return finish(p, "figure1_routing_layers.svg", out_dir)


def figure2(out_dir=OUT):
    q, k = 2, 3
    T = aggregate_modal_tilt_threshold(k)
    assert T == 7
    root = _majority_root_q2_k3()
    p = base(
        "One layer hierarchy generates two stationary occupancy transitions",
        "Aggregate mode and stationary majority are distinct estimands",
    )

    # Panel A: nested-chain certificate.
    p += [text(45, 145, "A", 28, "bold"), text(85, 145, "All lower layers reduce to one adjacent obstruction", 24, "bold")]
    boxes = [(115, 220, "S1"), (315, 220, "S2")]
    for x, y, lab in boxes:
        p += [rect(x, y, 150, 85, LIGHT), text(x + 75, y + 34, lab, 19, "bold", "middle"), text(x + 75, y + 66, "nonempty subset", 16, anchor="middle", fill=MID)]
    p += [line(265, 262, 315, 262, arrow=True), text(290, 245, "⊆", 22, "bold", "middle"), text(115, 355, "nested chains", 19, "bold"), text(115, 390, "A_s = (s+1)^k - s^k", 19), text(115, 425, "≤ (2^k - 1)^s", 22, "bold"), text(115, 457, "strict for k≥2, s≥2", 17, fill=MID)]

    # Panel B: layer weights as theta changes.
    p += [text(565, 145, "B", 28, "bold"), text(605, 145, "Aggregate gain-layer weights", 24, "bold")]
    x0, y0, x1, y1 = 620, 465, 1090, 210
    _axis(p, x0, y0, x1, y1, "stationary tilt θ", "unnormalized W_r")
    theta_max = 12.0
    max_weight = max(float(max(aggregate_layer_weights(q, k, t))) for t in range(1, 13))
    def xp(theta): return x0 + (theta - 1.0) / (theta_max - 1.0) * (x1 - x0)
    def yp(weight): return y0 - weight / max_weight * (y0 - y1)
    for r in range(3):
        pts = []
        for i in range(111):
            th = 1.0 + (theta_max - 1.0) * i / 110.0
            d = weakest_branch_layer_degeneracy(q, k, r)
            pts.append((xp(th), yp(d * (th ** r))))
        p.append(polyline(pts, stroke=[MID, BLACK, BLACK][r], sw=[2, 3, 4][r], dash=["8 6", "5 5", None][r]))
    p += [line(xp(T), y0, xp(T), y1, MID, 2, "6 5"), text(xp(T), y1 - 12, "mode θ=7", 16, "bold", "middle")]
    for th in (1, 4, 7, 10, 12):
        p += [line(xp(th), y0, xp(th), y0 + 7), text(xp(th), y0 + 28, th, 14, anchor="middle")]
    p += [text(970, 260, "W2=θ²", 16, "bold"), text(970, 315, "W1=7θ", 16, "bold"), text(970, 390, "W0=19", 16, fill=MID)]

    # Panel C: full mass curve.
    p += [text(45, 565, "C", 28, "bold"), text(85, 565, "Stationary majority occurs later", 24, "bold")]
    mx0, my0, mx1, my1 = 120, 815, 760, 610
    _axis(p, mx0, my0, mx1, my1, "stationary tilt θ", "P(full)")
    def mx(theta): return mx0 + (theta - 1.0) / 12.0 * (mx1 - mx0)
    def my(prob): return my0 - prob * (my0 - my1)
    mass_pts = []
    for i in range(121):
        th = 1.0 + 12.0 * i / 120.0
        d0, d1, d2 = counts = (19.0, 7.0, 1.0)
        mass = d2 * th * th / (d0 + d1 * th + d2 * th * th)
        mass_pts.append((mx(th), my(mass)))
    p += [polyline(mass_pts, BLACK, 4), line(mx0, my(0.5), mx1, my(0.5), MID, 2, "6 5"), text(mx1 - 5, my(0.5) - 10, "1/2", 15, anchor="end", fill=MID), line(mx(T), my0, mx(T), my1, MID, 2, "5 5"), line(mx(root), my0, mx(root), my1, BLACK, 2, "6 4"), text(mx(T), my1 - 10, "7", 15, "bold", "middle"), text(mx(root), my1 - 10, "θ₁/₂≈9.09", 15, "bold", "middle"), text(465, 785, "P_full(7)=49/117≈0.419", 17, "bold", "middle")]

    # Panel D: canonical population-size staircase.
    p += [text(840, 565, "D", 28, "bold"), text(880, 565, "Canonical Moran consequence (a=2)", 24, "bold")]
    p += [rect(895, 625, 600, 165, WHITE), text(1195, 665, "k=q+1", 20, "bold", "middle"), text(1195, 705, "first unique aggregate mode: N=q+2", 20, anchor="middle"), text(1195, 742, "first stationary majority: N=q+3 (q≥2)", 20, "bold", "middle"), text(1195, 775, "largest class ≠ majority", 18, anchor="middle", fill=MID)]
    p += [rect(870, 820, 650, 55, LIGHT), text(1195, 855, "T_k < θ₁/₂(q,k) < 2T_k  for q≥2", 21, "bold", "middle")]
    return finish(p, "figure2_occupancy_thresholds.svg", out_dir)


def figure3(out_dir=OUT):
    p = base(
        "The exact thresholds are conditional on representation and neutral mutation measure",
        "Same phenotype-level fitness does not identify stationary occupancy",
    )

    # Panel A: representation contrast.
    p += [text(45, 145, "A", 28, "bold"), text(85, 145, "Representation contrast at q=2, θ=2", 24, "bold")]
    p += [rect(85, 205, 610, 250, WHITE), text(390, 245, "Compressed gain chain", 22, "bold", "middle"), text(390, 285, "one genotype per gain", 18, anchor="middle", fill=MID), text(390, 335, "weights = (1, 2, 4)", 22, anchor="middle"), text(390, 375, "P(full) = 4/7", 22, "bold", "middle"), text(390, 415, "full gain: unique mode + majority", 19, "bold", "middle")]
    p += [rect(785, 205, 730, 250, WHITE), text(1150, 245, "Branch-product routing", 22, "bold", "middle"), text(1150, 285, "multiplicity = (19, 7, 1)", 18, anchor="middle", fill=MID), text(1150, 335, "weights = (19, 14, 4)", 22, anchor="middle"), text(1150, 375, "P(full) = 4/37", 22, "bold", "middle"), text(1150, 415, "full gain: nonmodal + minority", 19, "bold", "middle")]
    p += [line(695, 330, 785, 330, MID, 2, arrow=True), text(740, 312, "same gains", 15, anchor="middle", fill=MID), text(740, 350, "same θ", 15, anchor="middle", fill=MID)]

    # Panel B: fixed-support mutation-measure contrast.
    p += [text(45, 555, "B", 28, "bold"), text(85, 555, "Fixed support still does not identify occupancy", 24, "bold")]
    p += [text(255, 625, "gain path", 18, "bold", "middle")]
    node_x = [120, 255, 390]
    for x, lab in zip(node_x, ["0", "1", "2"]):
        p += [circle(x, 690, 34), text(x, 698, lab, 18, "bold", "middle")]
    p += [line(154, 690, 221, 690, MID, 3), line(289, 690, 356, 690, MID, 3)]
    p += [text(255, 765, "same support, same θ=2", 17, anchor="middle", fill=MID)]

    p += [rect(520, 605, 440, 215, WHITE), text(740, 645, "Neutral measure A", 21, "bold", "middle"), text(740, 690, "selected occupancy", 18, anchor="middle", fill=MID), text(740, 735, "(1/10, 1/10, 4/5)", 23, "bold", "middle"), text(740, 780, "full gain = 80%", 20, anchor="middle")]
    p += [rect(1040, 605, 440, 215, WHITE), text(1260, 645, "Neutral measure B", 21, "bold", "middle"), text(1260, 690, "selected occupancy", 18, anchor="middle", fill=MID), text(1260, 735, "(9/20, 9/20, 1/10)", 23, "bold", "middle"), text(1260, 780, "full gain = 10%", 20, anchor="middle")]

    p += [rect(310, 840, 980, 45, LIGHT), text(800, 870, "representation + neutral mutation measure + selection tilt → stationary gain occupancy", 19, "bold", "middle")]
    return finish(p, "figure3_scope_controls.svg", out_dir)


def generate_all(out_dir=OUT):
    return (figure1(out_dir), figure2(out_dir), figure3(out_dir))


if __name__ == "__main__":
    for path in generate_all():
        print(path)
