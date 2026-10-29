"""Stage10 original-source 2016 wind / true 3D flight-heading prediction.

The biological unit is the original tagged bee, not frames or flights.
Every model is fitted without ANY trial of the evaluation bee.
This is a predictive kinematic association, not cue acquisition or fitness.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import hashlib
import io
import json
from pathlib import Path
import zipfile
import numpy as np

from source_audit import FILENAME,EXPECTED_MD5
from inspect_native_schema import PATTERN

FPS=1000.0
EARLY_RING_M=(.05,.07)
LATE_RING_M=(.015,.03)
MIN_CONTIGUOUS_FRAMES=8
MIN_PLANAR_SPEED_M_S=.02
RIDGE_ALPHA=5.0
MIN_TRIALS=60
MIN_BEES=16
MIN_BEES_PER_WIND=12
EXPECTED_SOURCE_CSVS=157
EXPECTED_SOURCE_BEES=28
EXACT_HEADER=tuple(f"pt{point}_{axis}" for point in range(1,8) for axis in "XYZ")
FROZEN_SOURCE_SHA256="9a2881e5aaf4d7bb9556c9118c45d2e2ed6a2a8b22b80d4d762a5626fdd918ec"

def contiguous_runs(mask):
    """Start/end-excl runs of consecutive TRUE *original* frames."""
    out=[];start=None
    for i,v in enumerate(mask):
        if bool(v) and start is None:start=i
        if not v and start is not None:
            out.append((start,i));start=None
    if start is not None:out.append((start,len(mask)))
    return out

def velocity_ls(coords,start,end,fps=FPS):
    """Slope from observed coordinates, not model-interpolated positions."""
    if end-start<MIN_CONTIGUOUS_FRAMES:
        raise ValueError("NO_GO_TOO_FEW_CONTIGUOUS_ORIGINAL_FRAMES")
    y=np.asarray(coords[start:end],dtype=float)
    if y.ndim!=2 or y.shape[1]!=3 or not np.all(np.isfinite(y)):
        raise ValueError("NO_GO_BAD_NATIVE_3D_COORDINATES")
    t=np.arange(start,end,dtype=float)/fps
    tc=t-t.mean()
    v=(tc[:,None]*(y-y.mean(axis=0))).sum(axis=0)/(tc**2).sum()
    if not np.all(np.isfinite(v)):
        raise ValueError("NO_GO_NONFINITE_ORIGINAL_VELOCITY")
    return v

def trial_features(source_array,metadata,source_name):
    """Only true tracking rows; explicit mutually exclusive source quality reason."""
    a=np.asarray(source_array,dtype=float)
    if a.ndim!=2 or a.shape[1]!=21 or a.shape[0]<MIN_CONTIGUOUS_FRAMES:
        return None,"source_original_matrix_shape"
    pts=a.reshape((len(a),7,3))
    valid_bee=np.all(np.isfinite(pts[:,:3,:]),axis=(1,2))
    # Source-authored point7 is ONE observed reference coordinate per trial;
    # it is not a time-indexed flower trajectory. The authors subtract it
    # from every bee coordinate using bsxfun. See source-only QA receipt.
    flower_rows=pts[:,6,:]
    recorded_flower=np.all(np.isfinite(flower_rows),axis=1)
    if int(recorded_flower.sum())!=1:
        return None,"not_exactly_one_native_observed_flower_landmark"
    flower_reference=flower_rows[recorded_flower][0]
    good=valid_bee
    if good.sum()<2*MIN_CONTIGUOUS_FRAMES:
        return None,"missing_native_bee_triangle_frames"
    bee=pts[:,:3,:].mean(axis=1)
    target=np.broadcast_to(flower_reference,bee.shape)
    dist=np.linalg.norm(bee-target,axis=1)
    early=(good & (dist>=EARLY_RING_M[0]) & (dist<=EARLY_RING_M[1]))
    late=(good & (dist>=LATE_RING_M[0]) & (dist<=LATE_RING_M[1]))
    eruns=[x for x in contiguous_runs(early) if x[1]-x[0]>=MIN_CONTIGUOUS_FRAMES]
    if not eruns:
        return None,"no_complete_original_early_ring"
    ea,eb=eruns[0]
    lruns=[x for x in contiguous_runs(late)
           if x[1]-x[0]>=MIN_CONTIGUOUS_FRAMES and x[0]>eb]
    if not lruns:
        return None,"no_later_original_landing_ring"
    la,lb=lruns[-1]
    if la<=eb:
        raise ValueError("NO_GO_NONCHRONOLOGICAL_RING_WINDOWS")
    va=velocity_ls(bee,ea,eb)
    vb=velocity_ls(bee,la,lb)
    speed_early=float(np.linalg.norm(va[:2]))
    speed_late=float(np.linalg.norm(vb[:2]))
    if speed_early<MIN_PLANAR_SPEED_M_S or speed_late<MIN_PLANAR_SPEED_M_S:
        return None,"near_zero_original_planar_velocity"
    early_rel=np.mean(bee[ea:eb]-target[ea:eb],axis=0)
    if not np.all(np.isfinite(early_rel)):
        return None,"nonfinite_source_early_relative_position"
    early_unit=va[:2]/speed_early
    late_unit=vb[:2]/speed_late
    W,P,S=metadata["w"],metadata["p"],metadata["s"]
    features0=np.array([W,P,S,W*P,W*S,P*S,W*P*S,
                        *early_rel,float(np.linalg.norm(early_rel)),speed_early],dtype=float)
    features1=np.r_[features0,early_unit,W*early_unit]
    assert len(features0)==12 and len(features1)==16
    if not np.all(np.isfinite(features1)) or not np.all(np.isfinite(late_unit)):
        return None,"nonfinite_original_features"
    return {"source_name":source_name,"bee":metadata["bee"],"tag":metadata["tag"],
            "wind":W,"orientation":P,"stiffened":S,"first_early_frame":ea,
            "last_early_frame":eb-1,"first_late_frame":la,"last_late_frame":lb-1,
            "n_early_frames":eb-ea,"n_late_frames":lb-la,
            "early_speed_m_s":speed_early,"late_speed_m_s":speed_late,
            "x0":features0,"x1":features1,"y":late_unit},None

def native_trials(zipfile_path):
    data=Path(zipfile_path).read_bytes()
    if hashlib.md5(data).hexdigest()!=EXPECTED_MD5 or hashlib.sha256(data).hexdigest()!=FROZEN_SOURCE_SHA256:
        raise ValueError("NO_GO_ORIGINAL_SOURCE_MD5_SHA256_CHANGED")
    raw_files=0;bees=set();counts=Counter();by_condition=Counter();scored=[]
    names=set()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        paths=[n for n in z.namelist() if n.startswith("kinematic data/")
               and n.endswith("xyzpts.csv") and not n.split("/")[-1].startswith("._")]
        for path in sorted(paths):
            name=path.rsplit("/",1)[-1]
            if name in names:raise ValueError("NO_GO_REPEATED_ORIGINAL_TRAJECTORY_NAME")
            names.add(name)
            m=PATTERN.fullmatch(name)
            if not m:raise ValueError("NO_GO_NATIVE_EXPERIMENT_FILENAME_SCHEMA "+name)
            metadata={k:int(v) for k,v in m.groupdict().items()}
            bees.add(metadata["bee"])
            raw_files+=1
            cond=f"S{metadata['s']}P{metadata['p']}W{metadata['w']}"
            by_condition[cond]+=1
            with z.open(path) as member:
                raw=member.read()
            # Some original 2016 CSVs use classic CR-only row breaks.
            # Normalize the line-endings IN MEMORY without changing numerical
            # tokens or the provider-verified raw source archive/checksum.
            source_text=raw.decode("utf-8-sig",errors="strict")
            normalized=source_text.replace("\r\n","\n").replace("\r","\n")
            h=normalized.split("\n",1)[0].strip().split(",")
            if tuple(h)!=EXACT_HEADER:
                raise ValueError("NO_GO_SOURCE_COORDINATE_COLUMN_NAME_DIFFERENCE "+json.dumps({"file":name,"length":len(h),"source_head":h[:4],"source_tail":h[-4:],"expected_length":len(EXACT_HEADER),"expected_head":EXACT_HEADER[:4],"expected_tail":EXACT_HEADER[-4:]}))
            a=np.genfromtxt(io.StringIO(normalized),skip_header=1,delimiter=",",dtype=float)
            record,reason=trial_features(a,metadata,name)
            if reason:
                counts[(cond,reason)]+=1
            else:
                counts[(cond,"passed")]+=1
                scored.append(record)
    if raw_files!=EXPECTED_SOURCE_CSVS or len(bees)!=EXPECTED_SOURCE_BEES:
        raise ValueError("NO_GO_SOURCE_ORIGINAL_FILE_OR_BEE_COUNT_CHANGED")
    eligible_bees={r["bee"] for r in scored}
    by_w={w:{r["bee"] for r in scored if r["wind"]==w} for w in (0,1)}
    receipt={"source_archive_verified_md5":EXPECTED_MD5,
             "source_archive_verified_sha256":FROZEN_SOURCE_SHA256,
             "original_native_xyz_csv_trials":raw_files,
             "original_distinct_tagged_bees":len(bees),
             "source_trial_condition_counts":dict(sorted(by_condition.items())),
             "source_eligible_trials":len(scored),
             "source_eligible_bees":len(eligible_bees),
             "eligible_bees_by_wind":{str(k):len(v) for k,v in by_w.items()},
             "quality_gates_by_original_source_condition":{
                 cond:{status:val for (c,status),val in sorted(counts.items()) if c==cond}
                 for cond in sorted(by_condition)},
             "eligible_trial_counts_by_wind":{
                 str(w):sum(r["wind"]==w for r in scored) for w in (0,1)},
             "eligibility_cutoffs_frozen_before_outcome":True,
             "author_primary_112_figure_tracks_NOT_equated_to_raw_157":True}
    supported=(len(scored)>=MIN_TRIALS and len(eligible_bees)>=MIN_BEES and
               all(len(by_w[w])>=MIN_BEES_PER_WIND for w in (0,1)))
    receipt["scientific_support_gate"]="PASS" if supported else "NO_GO_INSUFFICIENT_MEASURED_TRIPLES"
    return scored,receipt

def fit_ridge(train_rows,feature,alpha=RIDGE_ALPHA):
    """Training-only weighted standardization and ridge, one bee one total weight."""
    if alpha!=RIDGE_ALPHA:raise ValueError("NO_GO_TUNED_RIDGE_ALPHA")
    if not train_rows:raise ValueError("NO_GO_EMPTY_TRAINING_BEES")
    X=np.vstack([r[feature] for r in train_rows])
    Y=np.vstack([r["y"] for r in train_rows])
    nbee=Counter(r["bee"] for r in train_rows)
    w=np.array([len(train_rows)/(len(nbee)*nbee[r["bee"]]) for r in train_rows])
    w=w/w.mean()
    mu=np.average(X,weights=w,axis=0)
    sd=np.sqrt(np.average((X-mu)**2,weights=w,axis=0))
    sd[sd<1e-12]=1.0
    Z=(X-mu)/sd
    ym=np.average(Y,weights=w,axis=0)
    gram=Z.T@(w[:,None]*Z)+alpha*np.eye(Z.shape[1])
    beta=np.linalg.solve(gram,Z.T@(w[:,None]*(Y-ym)))
    return (mu,sd,ym,beta)

def predict(model,rows,feature):
    mu,sd,ym,beta=model
    return ym+((np.vstack([r[feature] for r in rows])-mu)/sd)@beta

def leave_one_bee_out(rows):
    bees=sorted({r["bee"] for r in rows})
    if len(bees)<2:raise ValueError("NO_GO_NOT_ENOUGH_INDEPENDENT_BEES")
    records=[]
    for bee in bees:
        train=[r for r in rows if r["bee"]!=bee]
        test=[r for r in rows if r["bee"]==bee]
        if not test or not train or any(r["bee"]==bee for r in train):
            raise ValueError("NO_GO_ORIGINAL_BEE_HOLDOUT_LEAKAGE")
        m0=fit_ridge(train,"x0");m1=fit_ridge(train,"x1")
        p0=predict(m0,test,"x0");p1=predict(m1,test,"x1")
        Y=np.vstack([r["y"] for r in test])
        for i,r in enumerate(test):
            s0=float(((Y[i]-p0[i])**2).sum())
            s1=float(((Y[i]-p1[i])**2).sum())
            records.append({"bee":bee,"wind":r["wind"],"orientation":r["orientation"],
                            "stiffened":r["stiffened"],"M0_sq_error":s0,"M1_sq_error":s1,
                            "gain":s0-s1})
    return records

def summarize(rows,quality):
    if quality["scientific_support_gate"]!="PASS":
        return {"status":"NO_GO_ORIGINAL_KINEMATICS_INSUFFICIENT_SUPPORT",
                "source_quality":quality,"not_fitted_a_biological_model":True}
    records=leave_one_bee_out(rows)
    bee=defaultdict(list)
    for x in records:bee[x["bee"]].append(x)
    mean=lambda vals:sum(vals)/len(vals)
    beescore={str(b):{"n_original_eligible_trials":len(r),
                      "M0_loss":mean([q["M0_sq_error"] for q in r]),
                      "M1_loss":mean([q["M1_sq_error"] for q in r]),
                      "gain":mean([q["gain"] for q in r])} for b,r in sorted(bee.items())}
    wstats={}
    for w in (0,1):
        cells={b:[x for x in r if x["wind"]==w] for b,r in bee.items()}
        cells={b:rs for b,rs in cells.items() if rs}
        vals=[mean([r["gain"] for r in rs]) for rs in cells.values()]
        wstats[str(w)]={"original_source_bees":len(cells),
                        "original_source_trials":sum(map(len,cells.values())),
                        "bee_equal_loss_gain":mean(vals),
                        "bees_with_positive_gain":sum(v>0 for v in vals)}
    positive=sum(x["gain"]>0 for x in beescore.values())
    primary=mean([x["gain"] for x in beescore.values()])
    return {"status":"REAL_2016_MEASURED_HEADING_LOBO_EVALUATED",
            "source_quality":quality,
            "model_baseline":"Original wind, orientation, stiffness 2^3, early source position/radial distance/speed",
            "model_augmented":"Baseline plus measured early XY direction and wind×direction, no future frames",
            "holdout":"all original trials from one tagged bee excluded from its train fit",
            "ridge_alpha":RIDGE_ALPHA,
            "primary_gain_bee_equal_sq_error":primary,
            "bees_with_positive_gain":positive,"bees_total":len(beescore),
            "wind_group_source_bee_equal":wstats,
            "headwind_minus_still_predictive_gain":wstats["1"]["bee_equal_loss_gain"]-wstats["0"]["bee_equal_loss_gain"],
            "source_bee_derived_model_scores":beescore,
            "one_original_study_not_multiple_colony_replication":True,
            "not_same_as_discrete_flower_choice_or_adaptive_query_gain":True,
            "not_direct_causal_internal_heading_memory":True}

def run(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    out=root/"stage10_real_heading_LOBO_results.json"
    rows,quality=native_trials(root/FILENAME)
    receipt=summarize(rows,quality)
    out.write_text(json.dumps(receipt,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE10_REAL_2016_HEADING_LOBO "+json.dumps({
        k:v for k,v in receipt.items()
        if k not in ("source_bee_derived_model_scores",)
    },ensure_ascii=False,allow_nan=False),flush=True)
    if receipt["status"].startswith("NO_GO"):
        print("STAGE10_HEADING_NO_GO",flush=True)
        raise ValueError(receipt["status"])
    print("STAGE10_REAL_HEADING_COMPLETE",flush=True)
    return receipt

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--out",default="bee_stage10_original")
    run(Path(p.parse_args().out))
