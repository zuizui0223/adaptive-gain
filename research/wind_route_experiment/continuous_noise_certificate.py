"""Full-interval certification of the finite four-world Bayes cue-score formulas.

Every <=2-query deterministic decision tree uses the noisy H branch signal
at most once. Its SUCCESS PROBABILITY FOR FIXED TERMINAL ACTIONS is affine in
the error e. Exhaustively enumerate every such line. On the intervals
[0,1/4],[1/4,1/2], verify every affine line lies below the proposed linear
formula at BOTH endpoints and find an explicit policy line attaining it there.
Thus the formulas are certified on the WHOLE intervals, not sampled e values.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import json

from adaptive_gain.flower_cue_topology import catalog

WORLDS=((0,0),(0,1),(1,0),(1,1))
CUES=("F0","F1","H")
KNOTS=(F(0),F(1,4),F(1,2))

def _leaf_target_lines(tree,x,y):
    first,after0,after1=tree
    leaves=[]
    for observed,nxt in ((0,after0),(1,after1)):
        if nxt is None:
            leaves.append((observed,None,nxt))
        else:
            for out in (0,1):
                leaves.append((observed,out,nxt))
    result=[]
    for out1,out2,nxt in leaves:
        masses=[]
        for chosen_target in (0,1):
            ends=[]
            for e in (F(0),F(1,2)):
                total=F(0)
                for i,(branch,target) in enumerate(WORLDS):
                    if target!=chosen_target:continue
                    def prob(q,obs):
                        if q=="H":return 1-e if obs==branch else e
                        bit=x[i] if q=="F0" else y[i]
                        return int(bit==obs)
                    w=F(1,4)*prob(first,out1)
                    if nxt is not None:
                        w*=prob(nxt,out2)
                    total+=w
                ends.append(total)
            masses.append(tuple(ends))
        result.append(tuple(masses))
    return result

def _candidate_affine_lines(tree,x,y):
    mass=_leaf_target_lines(tree,x,y)
    for actions in product((0,1),repeat=len(mass)):
        p0=sum((mass[i][choice][0] for i,choice in enumerate(actions)),F(0))
        p_half=sum((mass[i][choice][1] for i,choice in enumerate(actions)),F(0))
        yield (p0,p_half)

def adaptive_policy_lines(x,y):
    lines={(F(1,2),F(1,2))}
    for root in CUES:
        later=(None,)+tuple(q for q in CUES if q!=root)
        for one,two in product(later,repeat=2):
            lines.update(_candidate_affine_lines((root,one,two),x,y))
    return lines

def fixed_policy_lines(x,y):
    lines={(F(1,2),F(1,2))}
    for k in (1,2):
        for qs in combinations(CUES,k):
            first=qs[0]
            second=qs[1] if k==2 else None
            lines.update(_candidate_affine_lines((first,second,second),x,y))
    return lines

def at(line,e):
    return line[0]+2*e*(line[1]-line[0])

def class_label(row):
    if row["other_species_absolute_value"]==0:
        return "no_source_value"
    if row["strict_sequential_value"]==0:
        return "source_value_fixed_sufficient"
    if row["strict_sequential_value"]==F(1,20):
        return "noise_only_adaptive_value"
    return "structural_adaptive_value"

def formula(kind,side,e):
    if kind=="no_source_value":return F(1)
    if kind=="source_value_fixed_sufficient":return 1-e
    if side=="adaptive":return 1-e/2
    if kind=="noise_only_adaptive_value":return max(1-e,F(3,4))
    if kind=="structural_adaptive_value":return F(3,4)
    raise ValueError(kind)

def certify_policy_envelope(lines,kind,side):
    knots=[(e,formula(kind,side,e)) for e in KNOTS]
    if any(at(line,e)>limit for line in lines for e,limit in knots):
        raise AssertionError(f"FAIL upper bound: {kind}/{side}")
    witnesses=[]
    for (a,fa),(b,fb) in zip(knots[:-1],knots[1:]):
        witness=next((ln for ln in lines if at(ln,a)==fa and at(ln,b)==fb),None)
        if witness is None:
            raise AssertionError(f"FAIL constructive witness: {kind}/{side}/{a}:{b}")
        witnesses.append({"interval":[str(a),str(b)],
                          "exact_affine_policy_endpoints":[str(witness[0]),str(witness[1])]})
    return {"candidate_policy_lines":len(lines),"two_interval_witnesses":witnesses}

def continuous_certificate():
    counts={"no_source_value":0,"source_value_fixed_sufficient":0,
            "noise_only_adaptive_value":0,"structural_adaptive_value":0}
    examples={}
    total=0
    for row in catalog(F(1,10)):
        if not row["correct_branch_specific"]:
            continue
        total+=1
        x,y=row["floral0"],row["floral1"]
        label=class_label(row)
        counts[label]+=1
        adaptive=certify_policy_envelope(adaptive_policy_lines(x,y),label,"adaptive")
        fixed=certify_policy_envelope(fixed_policy_lines(x,y),label,"fixed")
        examples.setdefault(label,{
          "floral_truth_table_masks":[row["floral0_mask"],row["floral1_mask"]],
          "adaptive":adaptive,"fixed":fixed,
        })
    assert total==64 and counts=={
      "no_source_value":36,"source_value_fixed_sufficient":4,
      "noise_only_adaptive_value":16,"structural_adaptive_value":8}
    return {
      "status":"CERTIFIED_ALL_64_ON_COMPLETE_ERROR_INTERVAL",
      "noise_error_interval":"0 <= e <= 1/2",
      "exact_breakpoints":["0","1/4","1/2"],
      "n_branch_valid":total,"regime_counts":counts,
      "examples_with_explicit_affine_policy_witnesses":examples,
      "proof":"all deterministic terminal-decision policy scores affine in e; max over all; endpoint upper bounds and attaining lines on each linear segment",
      "scope":"finite 4-world 2-query uniform prior; not population data or a universal noisy sensing theorem",
    }

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    cert=continuous_certificate()
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.out).write_text(json.dumps(cert,indent=2),encoding="utf-8")
    print("FULL_NOISE_INTERVAL_EXACT_CERTIFICATE_PASS",json.dumps(cert["regime_counts"]))
