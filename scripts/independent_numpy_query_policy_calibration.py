"""Independent NumPy/SciPy Monte Carlo check of held-out query-policy inference.

Optional packages: numpy, scipy. Not imported by package core or CI.
This script independently computes the same synthetic *design* as
scripts/simulate_randomized_query_policy_validation.py, but uses an
independent vectorized NumPy algorithm and an independent RNG.

It does NOT sample real bee data and does NOT estimate fitness or a
realistic sample size. Shared Gaussian colony-level logit effects model
within-cluster dependence. Exactly 12 binary-reward encounters are
generated in each old-report x (passive,sham,query) arm per cluster.
A frozen report-to-query/passive schedule is learned on TRAIN clusters.
Validation uses disjoint HELDOUT clusters; the stricter lower-bound
test must show positive differences from BOTH fixed programs.

Original reproducible audit:
--main: 250 Monte Carlo experiments, 400 HELDOUT cluster bootstrap
        samples each, 30+30 clusters, colony random logit sd=0.55.
--grid: 200 experiments and 300 bootstrap samples in each of
        18 null/alternative x cluster number x sd settings.

NB: The nominal 0.04 conditional reward gain is defined at colony random
effect zero. The true colony-MARGINAL alternative gain is about 0.03953
at sd=0.55. Do not present the nominal 0.04 as its exact marginal value.
"""
from __future__ import annotations

import argparse
import json

import numpy as np
from scipy.special import expit, logit

P_NULL=np.array([[.70,.65,.70],[.80,.70,.80]],dtype=float)
P_MIXED=np.array([[.70,.65,.90],[.80,.70,.75]],dtype=float)
WEIGHTS=np.array([.2,.8],dtype=float)


def simulation_once(
    *,
    seed: int,
    probabilities: np.ndarray,
    ntrain: int,
    ntest: int,
    per_cell_trials: int=12,
    bootstrap_repetitions: int=400,
    colony_logit_sd: float=.55,
) -> dict:
    rng=np.random.default_rng(seed)
    colony_intercepts=rng.normal(
        0,colony_logit_sd,(ntrain+ntest,1,1))
    probabilities_with_clusters=expit(
        logit(probabilities)[None,:,:] + colony_intercepts
    )
    observed=rng.binomial(
        per_cell_trials,probabilities_with_clusters
    ).astype(float)/per_cell_trials
    train,test=observed[:ntrain],observed[ntrain:]
    rule=np.where(
        train.mean(axis=0)[:,2]>train.mean(axis=0)[:,0],2,0
    )

    def rewards(data):
        means=data.mean(axis=0)
        conditional=np.sum(
            WEIGHTS*means[np.arange(2),rule]
        )
        passive=np.sum(WEIGHTS*means[:,0])
        query=np.sum(WEIGHTS*means[:,2])
        return conditional-passive,conditional-query,conditional-max(passive,query)

    training=rewards(train)
    heldout=rewards(test)
    sampled_indices=rng.integers(
        0,ntest,size=(bootstrap_repetitions,ntest)
    )
    resampled_means=test[sampled_indices].mean(axis=1)
    conditional=np.sum(
        WEIGHTS*resampled_means[:,np.arange(2),rule],
        axis=1
    )
    against_passive=conditional-np.sum(
        WEIGHTS*resampled_means[:,:,0],axis=1
    )
    against_query=conditional-np.sum(
        WEIGHTS*resampled_means[:,:,2],axis=1
    )
    lowp,lowq=np.quantile(
        against_passive,.025),np.quantile(against_query,.025)
    return {
        "naive_gain":float(training[2]),
        "held_gain":float(heldout[2]),
        "held_dp":float(heldout[0]),
        "held_dq":float(heldout[1]),
        "passes_both_lower_bounds":bool(lowp>0 and lowq>0),
        "mixed_rule":bool(rule[0]!=rule[1]),
        "correct_mixed_rule":bool(tuple(rule)==(2,0)),
        "simultaneous_lower_bound":float(min(lowp,lowq)),
    }


def scenario(
    *, case: str, ntrain: int, ntest: int,
    colony_logit_sd: float,replications: int,
    bootstrap_repetitions: int,per_cell_trials: int,
    seed: int,
) -> dict:
    probabilities=P_NULL if case=="null" else P_MIXED
    if case not in ("null","mixed"):
        raise ValueError("case must be null or mixed")
    simulated=[
        simulation_once(
            seed=seed+i*17,
            probabilities=probabilities,ntrain=ntrain,ntest=ntest,
            colony_logit_sd=colony_logit_sd,
            per_cell_trials=per_cell_trials,
            bootstrap_repetitions=bootstrap_repetitions,
        )
        for i in range(replications)
    ]
    means={
        key:float(np.mean([item[key] for item in simulated]))
        for key in simulated[0]
    }
    return {
        "scenario":case,
        "train_clusters":ntrain,
        "heldout_clusters":ntest,
        "per_cluster_trials":6*per_cell_trials,
        "colony_logit_sd":colony_logit_sd,
        "monte_carlo_repetitions":replications,
        "cluster_bootstrap_draws_each":bootstrap_repetitions,
        "seed":seed,
        "mean_metrics":means,
        "fraction_naive_gain_positive":float(np.mean(
            [item["naive_gain"]>0 for item in simulated])),
        "fraction_heldout_gain_positive":float(np.mean(
            [item["held_gain"]>0 for item in simulated])),
    }


def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("--grid",action="store_true")
    cli.add_argument("--output")
    args=cli.parse_args()
    if args.grid:
        results=[
            scenario(
                case=case,ntrain=clusters,ntest=clusters,
                colony_logit_sd=sd,replications=200,
                bootstrap_repetitions=300,per_cell_trials=12,
                seed=975311,
            )
            for case in ("null","mixed")
            for clusters in (12,30,60)
            for sd in (0,.55,.9)
        ]
    else:
        results=[
            scenario(
                case=case,ntrain=30,ntest=30,
                colony_logit_sd=.55,replications=250,
                bootstrap_repetitions=400,per_cell_trials=12,
                seed=519280,
            )
            for case in ("null","mixed")
        ]
    obj={
        "schema":"adaptive-gain-independent-numpy-heldout-policy-monte-carlo-v1",
        "scenarios":results,
        "status":"SYNTHETIC_ONLY__OPTIONAL_NUMPY_SCIPY_VALIDATION",
        "claim_ceiling":"Sensitivity not a real bee power estimate or evidence of heritable fitness.",
    }
    payload=json.dumps(obj,indent=2)+"\n"
    if args.output:
        with open(args.output,"w",encoding="utf-8") as f:
            f.write(payload)
    else:
        print(payload,end="")


if __name__=="__main__":
    main()
