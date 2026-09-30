"""Summarize same-site same-week opportunity robustness."""

from __future__ import annotations
import argparse, csv, json, math
from collections import defaultdict
from pathlib import Path

SCOPES = {
    "strict_core_2008_2011": 3,
    "near_core_2007_2011": 4,
    "all_annual_2006_2011": 5,
}

def _read(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))

def _bool(x):
    return str(x).strip().lower() in {"true","1","yes","y"}

def _ll(rows, field):
    total=0.0
    for row in rows:
        y=int(row["outcome"])
        p=min(max(float(row[field]),1e-8),1-1e-8)
        total -= y*math.log(p)+(1-y)*math.log(1-p)
    return total/len(rows)

def _brier(rows, field):
    return sum((float(r[field])-int(r["outcome"]))**2 for r in rows)/len(rows)

def _auc(rows):
    y=[int(r["outcome"]) for r in rows]
    p=[float(r["model_probability"]) for r in rows]
    pos=sum(y); neg=len(y)-pos
    if pos==0 or neg==0: return None
    ordered=sorted(zip(p,y),key=lambda z:z[0])
    rank_sum=0.0; rank=1; i=0
    while i<len(ordered):
        j=i+1
        while j<len(ordered) and ordered[j][0]==ordered[i][0]:
            j+=1
        avg=(rank+(rank+j-i-1))/2
        rank_sum += avg*sum(v for _,v in ordered[i:j])
        rank += j-i; i=j
    return (rank_sum-pos*(pos+1)/2)/(pos*neg)

def _metrics(rows):
    ml=_ll(rows,"model_probability")
    nl=_ll(rows,"null_probability")
    mb=_brier(rows,"model_probability")
    nb=_brier(rows,"null_probability")
    return {
        "n":len(rows),
        "events":sum(int(r["outcome"]) for r in rows),
        "roc_auc":_auc(rows),
        "relative_log_loss_reduction":(nl-ml)/nl if nl else None,
        "brier_improvement":nb-mb,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("predictions",type=Path)
    ap.add_argument("folds",type=Path)
    ap.add_argument("output",type=Path)
    args=ap.parse_args()
    pred=_read(args.predictions)
    folds=_read(args.folds)
    grouped=defaultdict(list)
    for row in pred:
        grouped[(row["analysis_scope"],row["risk_set"],row["transition"])].append(row)
    fold_group=defaultdict(list)
    for row in folds:
        fold_group[(row["analysis_scope"],row["risk_set"])].append(row)

    scopes={}
    for scope, expected in SCOPES.items():
        transitions=sorted({t for s,_,t in grouped if s==scope})
        if len(transitions)!=expected:
            raise SystemExit(f"{scope}: expected {expected} transitions")
        endpoints={}
        for risk in ("gain","loss"):
            pooled=[]
            fm={}
            for t in transitions:
                rows=grouped[(scope,risk,t)]
                pooled.extend(rows)
                fm[t]=_metrics(rows)
            receipts=fold_group[(scope,risk)]
            converged=(
                len(receipts)==expected
                and all(
                    _bool(r["converged"])
                    and int(r["coefficient_count"])==int(r["finite_coefficient_count"])
                    for r in receipts
                )
            )
            m=_metrics(pooled)
            m["folds"]=fm
            m["all_folds_converged"]=converged
            m["positive_log_loss_folds"]=sum(
                x["relative_log_loss_reduction"]>0 for x in fm.values()
            )
            m["all_folds_positive_log_loss_skill"]=(
                m["positive_log_loss_folds"]==expected
            )
            endpoints[risk]=m
        scopes[scope]={"transitions":transitions,"endpoints":endpoints}

    primary=scopes["strict_core_2008_2011"]["endpoints"]
    result={
        "schema":"adaptive-gain-villavicencio-siteweek-opportunity-audit-v1",
        "date":"2026-09-29",
        "status":(
            "retrospective_spatiotemporal_robustness_green"
            if all(
                primary[r]["all_folds_converged"]
                and primary[r]["all_folds_positive_log_loss_skill"]
                and primary[r]["roc_auc"]>0.5
                for r in ("gain","loss")
            )
            else "retrospective_spatiotemporal_robustness_mixed"
        ),
        "analysis_status":"post-result same-site same-week robustness; not confirmatory",
        "scopes":scopes,
        "ecological_read":"If green, current-state opportunity still discriminates annual link dynamics when plant flowering and pollinator activity are required to coincide within the same site-week cell.",
        "claim_ceiling":"Spatiotemporal robustness only; no causality, sampling-effort independence, strict forecasting, decision equivalence, or routeability."
    }
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
