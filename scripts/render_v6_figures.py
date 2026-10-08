"""Render the three V6 figures as editable, dependency-free SVGs.

Input is generated ONLY by scripts.build_v6_figure_data.build() from the
committed theorem functions and source-data receipts. The SVGs are
deterministic schematic/quantitative panels, not fitted ecological
selection coefficients or inferred animal fitness.

Usage: python -m scripts.render_v6_figures --output-dir v6_figures

No Matplotlib, fonts, internet, spreadsheet or full source-data re-download.
A plain-text SVG is editable in vector illustration programs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from scripts.build_v6_figure_data import build

INK="#152D41"
MUTED="#5D7080"
BLUE="#176B96"
TEAL="#047D73"
ORANGE="#BC6840"
GRID="#DCE5E9"
BG="#FFFFFF"
SOFT="#F6F9FA"
STROKE=2.6
ROOT=Path(__file__).resolve().parents[1]


def _tag(name,attrs,body=""):
    options=" ".join(f'{k.replace("_","-")}="{escape(str(v))}"'
                     for k,v in attrs.items())
    return f"<{name} {options}>{body}</{name}>"


class SVG:
    def __init__(self, name, description, width=1200, height=740):
        self.width,self.height=width,height
        self.content=[
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {width} {height}" role="img">',
            _tag("title",{},escape(name)),
            _tag("desc",{},escape(description)),
            f'<rect width="{width}" height="{height}" fill="{BG}"/>',
        ]
    def add(self,line):
        self.content.append(line)
    def rect(self,x,y,w,h,*,fill=SOFT,stroke=GRID,rounding=14):
        self.add(_tag("rect",{"x":round(x,2),"y":round(y,2),
                 "width":round(w,2),"height":round(h,2),
                 "fill":fill,"stroke":stroke,"rx":rounding}))
    def line(self,x1,y1,x2,y2,*,color=INK,width=1.4,dash=None):
        opt={"x1":round(x1,2),"y1":round(y1,2),
             "x2":round(x2,2),"y2":round(y2,2),
             "stroke":color,"stroke_width":width}
        if dash: opt["stroke_dasharray"]=dash
        self.add(_tag("line",opt))
    def circle(self,x,y,*,r=5,fill=BLUE,stroke="white"):
        self.add(_tag("circle",{"cx":round(x,2),"cy":round(y,2),
                 "r":r,"fill":fill,"stroke":stroke,"stroke_width":1.5}))
    def text(self,x,y,value,*,size=15,color=INK,weight="normal",anchor=None):
        args={"x":round(x,2),"y":round(y,2),"font_family":
              "DejaVu Sans,Arial,sans-serif","font_size":size,
              "fill":color,"font_weight":weight}
        if anchor:args["text_anchor"]=anchor
        self.add(_tag("text",args,escape(str(value))))
    def path(self,points,*,color=BLUE,width=2.8):
        if len(points)<2:return
        d="M "+" L ".join(f"{a:.2f} {b:.2f}" for a,b in points)
        self.add(_tag("path",{"d":d,"stroke":color,"fill":"none",
                              "stroke_width":width,"stroke_linecap":"round",
                              "stroke_linejoin":"round"}))
    def finish(self):
        return "\n".join(self.content+["</svg>","\n"])


def section(s,x,y,w,h,label,title):
    s.rect(x,y,w,h)
    s.text(x+18,y+32,label,size=15,weight="bold",color=BLUE)
    s.text(x+18,y+59,title,size=17,weight="bold")


def axes(s,x,y,w,h,*,xrange=(0,1),yrange=(0,1),xticks=(),yticks=(),
         xlabel="",ylabel="",format_y=None):
    # Position passed as plot data rectangle, not entire card.
    for val in yticks:
        yy=y+h-(val-yrange[0])/(yrange[1]-yrange[0])*h
        s.line(x,yy,x+w,yy,color=GRID,width=1)
        s.text(x-11,yy+5,format_y(val) if format_y else f"{val:g}",
               color=MUTED,size=12,anchor="end")
    for val in xticks:
        xx=x+(val-xrange[0])/(xrange[1]-xrange[0])*w
        s.text(xx,y+h+24,f"{val:g}",color=MUTED,size=12,anchor="middle")
    s.line(x,y,x,y+h,color=MUTED)
    s.line(x,y+h,x+w,y+h,color=MUTED)
    if xlabel:s.text(x+w/2,y+h+54,xlabel,anchor="middle",size=13,color=MUTED)
    if ylabel:s.text(x,y-18,ylabel,size=12,color=MUTED)
    def xy(a,b):
        return (x+(a-xrange[0])/(xrange[1]-xrange[0])*w,
                y+h-(b-yrange[0])/(yrange[1]-yrange[0])*h)
    return xy


def _csv(path):
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))


def _fig1(directory):
    frontier=_csv(directory/"fig1_frontier.csv")
    urgency=_csv(directory/"fig1_urgency_ranking.csv")
    by_h={int(row["adaptive_depth_h"]):int(row["sharp_fixed_cost_Ih"])
          for row in frontier}
    selected=[2,3,4]
    if tuple(by_h[i] for i in selected)!=(3,7,9):
        raise ValueError("Figure 1 canonical sharp frontier drift")
    s=SVG("Figure 1: natural history re-ranks information architectures",
          "Finite sharp cost frontier; ratio ranking; value curves crossing with urgency.")
    s.text(44,42,"Natural history re-ranks information architectures",size=27,weight="bold")
    section(s,34,78,350,585,"A","Exact structural frontier")
    axis=axes(s,91,210,253,315,xrange=(1.6,4.4),yrange=(0,10),
              xticks=selected,yticks=(0,2,4,6,8,10),
              xlabel="Adaptive worst-path cost h",ylabel="Fixed cost I(h)")
    pts=[axis(h,by_h[h]) for h in selected]
    s.path(pts,color=BLUE)
    for h,(x,y) in zip(selected,pts):
        s.circle(x,y,fill=BLUE,r=7)
        s.text(x+10,y-12,f"({h},{by_h[h]})",size=14)
    s.text(56,628,"Every displayed point is attainable",size=12,color=MUTED)

    section(s,400,78,350,585,"B","Structural ratio ranking")
    ax=axes(s,451,210,257,315,xrange=(1.5,4.5),yrange=(0,3),
            xticks=selected,yticks=(0,1,2,3),
            xlabel="Adaptive depth h",ylabel="Fixed / adaptive")
    for h in selected:
        ratio=by_h[h]/h
        x0,y0=ax(h,0);x1,y1=ax(h,ratio)
        color=ORANGE if h==3 else BLUE
        s.rect(x0-26,y1,52,y0-y1,fill=color,stroke=color,rounding=4)
        s.text(x0,y1-12,f"{ratio:.2f}",size=17,color=color,
               weight="bold",anchor="middle")
    s.text(422,628,"Ratio-optimal depth: h = 3",size=13,color=ORANGE)

    section(s,766,78,400,585,"C","Biological value changes ranking")
    xy=axes(s,826,210,300,315,xrange=(0,1.12),yrange=(0,.36),
            xticks=(0,.3,.6,.9),yticks=(0,.1,.2,.3),
            xlabel="Opportunity decay rate μ",ylabel="U(h) − U(I(h))",
            format_y=lambda v:f"{v:.1f}")
    for h,color in zip(selected,(BLUE,TEAL,ORANGE)):
        rows=sorted((r for r in urgency if int(r["adaptive_depth_h"])==h
                     and .01<=float(r["mu"])<=1.11),
                    key=lambda r:float(r["mu"]))
        s.path([xy(float(r["mu"]),float(r["robust_value"]))
                for r in rows],color=color)
    for mu in (.1546967978,.6562559792):
        xx,_=xy(mu,0)
        s.line(xx,210,xx,525,dash="5 6",color=MUTED,width=1.4)
    for x,label,color in [(827,"h=2",BLUE),(927,"h=3",TEAL),
                          (1027,"h=4",ORANGE)]:
        s.text(x,588,label,size=16,color=color,weight="bold")
    s.text(786,629,"Optimal depth shifts: 4 → 3 → 2",size=13,color=MUTED)
    s.text(34,710,"Structural ratios are not fitness. Completion value and sensing costs are model quantities.",size=15,color=MUTED)
    return s.finish()


def _fig2(directory,manifest):
    rows=_csv(directory/"fig2_arity_ceiling.csv")
    s=SVG("Figure 2: exact robust no-go regions",
          "Finite depth viability, bound on robust control cost by cue arity, and nested resource constraints.")
    s.text(44,42,"Finite information constraints impose robust limits",size=27,weight="bold")
    section(s,34,78,350,585,"A","Finite information budget")
    s.text(56,171,"Binary n=10, m=9; U(c)=exp(−0.3c)",size=15,color=MUTED)
    s.text(56,198,"Illustrative control cost K=0.25",size=15,color=MUTED)
    cases=((2,3),(3,7),(4,9))
    import math
    for j,(h,f) in enumerate(cases):
        value=math.exp(-.3*h)-math.exp(-.3*f)
        yy=259+j*99
        s.text(66,yy,f"h = {h}",size=18,weight="bold")
        s.text(162,yy,f"value {value:.3f}",size=16)
        okay=value>.25
        s.text(303,yy,"PASS" if okay else "NO-GO",
               size=15,weight="bold",color=TEAL if okay else ORANGE,anchor="end")
        s.line(54,yy+24,363,yy+24,color=GRID)
    s.text(56,626,"Viability uses net value > K",color=MUTED,size=13)

    section(s,400,78,350,585,"B","Global cue-arity ceiling")
    xy=axes(s,459,215,250,309,xrange=(2,10),yrange=(0,.58),
            xticks=(2,4,6,8,10),yticks=(0,.2,.4,.55),
            xlabel="Max query outcome arity b",ylabel="Maximum repayable K",
            format_y=lambda a:f"{a:.2f}")
    data=sorted((int(row["max_query_arity_b"]),float(row["robust_cost_ceiling"]))
                for row in rows)
    s.path([xy(a,b) for a,b in data],color=TEAL)
    for a,b in data:s.circle(*xy(a,b),r=4,fill=TEAL)
    x0,y0=xy(2,.3);x1,_=xy(10,.3)
    s.line(x0,y0,x1,y0,color=ORANGE,width=2,dash="7 5")
    s.text(x1-6,y0-9,"K=0.30",size=13,color=ORANGE,anchor="end")
    s.text(421,625,"b=2: 0.2901   ·   b=3: 0.3863",size=13,color=MUTED)
    s.text(421,645,"Minimum robust arity b=3",size=13,color=TEAL)

    section(s,766,78,400,585,"C","Three distinct limitation layers")
    for i,(head,sub) in enumerate((
        ("1   Finite n,m,b","Not enough worlds or available queries"),
        ("2   Bounded cue arity","More worlds cannot exceed the b ceiling"),
        ("3   Unlimited finite structure","Opportunity value itself has a ceiling"),
    )):
        yy=218+i*124
        s.rect(793,yy-43,348,101,fill="white",rounding=9)
        s.text(809,yy,head,size=17,weight="bold")
        s.text(809,yy+27,sub,size=13,color=MUTED)
    s.text(785,632,"Cue arity is NOT receptor number",size=14,color=ORANGE)
    s.text(34,711,"The bounds concern guaranteed target resolution, not observed reproductive selection.",size=15,color=MUTED)
    return s.finish()


def _fig3(directory,manifest):
    import math
    s=SVG("Figure 3: robust and expected information value",
          "Robust versus expected limits, finite frequency rescue, individual mosquito CDFs, aggregate cue timing.")
    s.text(44,42,"Encounter frequencies create value beyond robust guarantees",
           size=25,weight="bold")
    section(s,34,78,560,291,"A","Global robust and expected ceilings")
    upper=float(manifest["figure_3"]["expected_global_ceiling_mu03"])
    lower=float(manifest["figure_3"]["robust_global_ceiling_mu03"])
    k=.60
    xy=axes(s,106,181,450,98,xrange=(0,1),yrange=(0,.8),
            yticks=(0,.2,.4,.6,.8),xticks=(),ylabel="Potential value")
    for label,val,color,offset in (("Robust",lower,BLUE,-8),
                                   ("Expected",upper,TEAL,14)):
        y=xy(0,val)[1]
        s.line(115,y,543,y,color=color,width=3)
        s.text(539,y+offset,f"{label}: {val:.3f}",
               anchor="end",size=13,weight="bold",color=color)
    y=xy(0,k)[1];s.line(113,y,542,y,color=ORANGE,dash="5 5",width=2)
    s.text(112,342,"Cost K=0.60 lies between global ceilings",size=14,color=ORANGE)

    section(s,608,78,558,291,"B","Finite encounter-frequency rescue")
    data=_csv(directory/"fig3_expected_rescue.csv")
    xy=axes(s,670,186,448,101,xrange=(0,1),yrange=(0,.75),
            xticks=(0,.25,.5,.75,1),yticks=(0,.2,.4,.6),
            xlabel="One-step encounter mass p1",ylabel="Expected value margin",
            format_y=lambda x:f"{x:.1f}")
    s.path([xy(float(v["one_step_mass_p1"]),
                 float(v["finite_scope_expected_advantage_supremum"]))
            for v in data],color=TEAL)
    xp,yp=xy(.6166136276,.60)
    s.circle(xp,yp,fill=ORANGE,r=5)
    s.line(xp,185,xp,287,color=ORANGE,dash="5 4",width=1)
    s.text(631,344,"Finite n=10,m=9: threshold p1 ≈ 0.6166",size=14,color=MUTED)

    section(s,34,385,735,300,"C1","Individual first-probe profiles (1-minute bins)")
    xy=axes(s,95,494,610,118,xrange=(1,8),yrange=(0,1),
            xticks=(1,2,3,4,5,6,7,8),yticks=(0,.25,.5,.75,1),
            xlabel="Minute after stimulus (interval end)",
            ylabel="Fraction first probing",format_y=lambda x:f"{x:.2f}")
    raw=_csv(directory/"fig3_uehara_cdf.csv")
    species=(
        ("Aedes aegypti",BLUE,"Ae. aegypti"),
        ("Aedes albopictus",ORANGE,"Ae. albopictus"),
        ("Anopheles gambiae",TEAL,"An. gambiae"),
    )
    for name,color,short in species:
        entries=sorted((v for v in raw if v["species"]==name),
                       key=lambda v:float(v["minute_end"]))
        if len(entries)!=8:raise ValueError("missing Uehara intervals")
        s.path([xy(float(v["minute_end"]),float(v["cdf_first_probe"]))
                for v in entries],color=color,width=2.5)
    for x,(_,color,label) in zip((83,306,529),species):
        s.text(x,667,label,size=14,color=color,weight="bold")

    section(s,785,385,381,300,"C2","Aggregate infrared response timing")
    source=json.loads((directory/"fig3_chandel_timing.json").read_text(
        encoding="utf-8"))
    for i,(key,label) in enumerate((
        ("post_first_pulse","After pulse 1"),
        ("post_second_pulse","After pulse 2"),
    )):
        dat=source[key]
        yy=504+i*88
        value=float(dat["half_signed_advantage_time_s_after_pulse"])
        s.text(811,yy,label,size=15)
        s.text(1116,yy,f"{value:.1f} s",size=21,
               weight="bold",color=TEAL,anchor="end")
        s.text(811,yy+23,"Half of signed advantage accumulated",size=12,color=MUTED)
    s.text(807,674,"Aggregate effect; NOT individual latency",size=12,color=ORANGE)
    s.text(34,724,"Temporal mosquito data are process anchors, not evidence of sensing-architecture fitness.",size=13,color=MUTED)
    return s.finish()


def render(outdir: Path) -> dict:
    tables=outdir/"data"
    manifest=build(tables)
    svg={
        "figure_1":"fig1_natural_history_reranking.svg",
        "figure_2":"fig2_robust_no_go.svg",
        "figure_3":"fig3_frequency_and_temporal_anchors.svg",
    }
    contents={
        "figure_1":_fig1(tables),
        "figure_2":_fig2(tables,manifest),
        "figure_3":_fig3(tables,manifest),
    }
    for key,name in svg.items():
        (outdir/name).write_text(contents[key],encoding="utf-8")
    receipt={
        "status":"V6_SVG_FIGURES_GENERATED_FROM_FROZEN_RECEIPTS",
        "source_manifest":"data/manifest.json",
        "figures":{
            key:{
                "filename":name,
                "sha256":hashlib.sha256(contents[key].encode("utf-8")).hexdigest(),
                "content_bytes":len(contents[key].encode("utf-8")),
            }
            for key,name in svg.items()
        },
        "claim_ceiling":(
            "Structural/mathematical panels are modeled finite quantities; "
            "mosquito panels use individual interval-censored or aggregate "
            "cue response metrics, NOT evolutionary fitness estimates."
        ),
    }
    (outdir/"svg_manifest.json").write_text(
        json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return receipt


def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("--output-dir",type=Path,default=Path("v6_figures"))
    args=cli.parse_args()
    print(json.dumps(render(args.output_dir),indent=2,sort_keys=True))


if __name__=="__main__":
    main()
