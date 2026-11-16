"""Stage46: plot original source-filtered Bombus modeled richness on true HEX centroids.

Georeferenced modeled source range/polygon overlap from Laborieux et al. 2026,
NOT native bee abundance or visitation. Mask pa_cutoff-excluded cells as NA
and distinguish modeled 0 from unknown. This is a diagnostic map and does
not establish any UV guide × Bombus association.
"""
from __future__ import annotations

import csv
from pathlib import Path
import math


def read_source_rows(filename):
    with open(filename,encoding="utf-8",newline="") as file:
        rd=csv.DictReader(file)
        records=list(rd)
    if len(records)!=10242:
        raise ValueError("NO_GO_GLOBAL_HEX_SOURCE_MAP_INCOMPLETE")
    groups={"positive":[],"zero":[],"unknown":[]}
    for row in records:
        lon=float(row["longitude"]);lat=float(row["latitude"])
        if not (-180<=lon<=180 and -90<=lat<=90):
            raise ValueError("NO_GO_ORIGINAL_SOURCE_CENTROID_INVALID")
        raw=row["n_source_tree_and_pa_cutoff_Bombus_taxa"]
        if raw=="":
            groups["unknown"].append((lon,lat,None))
        else:
            n=int(raw)
            if n<0:
                raise ValueError("NO_GO_NEGATIVE_MODELED_BOMBUS_TAXA")
            groups["positive" if n>0 else "zero"].append((lon,lat,n))
    if sum(map(len,groups.values()))!=10242:
        raise ValueError("NO_GO_SOURCE_MAP_CLASSIFICATION")
    return groups


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    root=Path("stage46_paper_filtered_Bombus")
    filename=root/"original_tree_and_PA_filtered_Bombus_hex_geographic_10242.csv"
    groups=read_source_rows(filename)
    fig,ax=plt.subplots(figsize=(12.6,6.45),dpi=165)
    u=groups["unknown"];z=groups["zero"];p=groups["positive"]
    if u:
        ax.scatter([x[0] for x in u],[x[1] for x in u],
                   c="0.88",s=2.6,alpha=.42,linewidth=0,
                   label="Outside source study-eligible grid")
    if z:
        ax.scatter([x[0] for x in z],[x[1] for x in z],
                   c="0.6",s=7.2,alpha=.7,linewidth=0,
                   label="0 Bombus in eligible source model")
    if p:
        points=ax.scatter(
            [x[0] for x in p],[x[1] for x in p],c=[x[2] for x in p],
            cmap="viridis",vmin=1,vmax=max(x[2] for x in p),
            s=14,alpha=.91,edgecolors="none",
            label="At least one modeled Bombus taxon")
        bar=fig.colorbar(points,ax=ax,fraction=.022,pad=.015)
        bar.set_label("Modeled Bombus species-name richness per HEX")
    ax.set_xlim(-180,180);ax.set_ylim(-80,85)
    ax.set_xticks(range(-180,181,60));ax.set_yticks(range(-60,91,30))
    ax.set_xlabel("Longitude (°)")
    ax.set_ylabel("Latitude (°)")
    ax.set_title("Global modeled Bombus range richness — authors' 3,370-species filter")
    ax.grid(alpha=.13,linewidth=.6)
    ax.legend(loc="lower left",fontsize=8,frameon=False,markerscale=1.2)
    fig.text(.125,.025,
      "Original modelled ranges / polygons, NOT observed bee abundance or local pollination. "
      "Unrepresented HEX cells are unknown, not biological absences.",
      fontsize=8,color=".4")
    fig.tight_layout(rect=[0,.05,1,1])
    root.mkdir(exist_ok=True)
    fig.savefig(root/"global_Bombus_source_filtered_predicted_hex_richness.png",
                bbox_inches="tight")
    fig.savefig(root/"global_Bombus_source_filtered_predicted_hex_richness.svg",
                bbox_inches="tight")
    plt.close(fig)
    print("STAGE46_REAL_SOURCE_BOMBUS_HEX_MAP_RENDERED",
          {"eligible_positive":len(p),"eligible_zero":len(z),
           "outside_author_eligibility":len(u),
           "max_modeled_Bombus":max((v[2] for v in p),default=None),
           "no_predicted_flower_UV_effect":True})


if __name__=="__main__":
    main()
