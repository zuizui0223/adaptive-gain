"""Monte Carlo operating-characteristic stress test of held-out query policies.

This is a self-contained *hypothetical* Bernoulli-reward experiment,
not empirical bee data and not a claim of exact cluster-bootstrap validity.

Two old reports and three randomized arms are fixed by block within each
biological cluster, with the same number of independent simulated Bernoulli
encounters in every (report, arm) cell. A shared Gaussian log-odds intercept
induces outcomes correlated WITHIN a cluster.

TRAINING and HELDOUT clusters never overlap. The training data select the
old-report -> query/passive policy. Held-out data estimate its advantage over
both fixed schedules. A cluster-percentile bootstrap provides two one-sided
lower 97.5% limits; the exploratory decision rejects only when BOTH are
strictly positive.

Do not infer required real sample sizes or selection coefficients from this
toy model. Actual randomized assignment, residual serial dependence,
animal compliance, signal accuracy, and colony structure must be studied
independently in a pilot.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import math
import random

REPORTS = (0, 1)
ARMS = ("passive", "sham", "query")
TARGET = (0.2, 0.8)
NULL_PROBABILITIES = ((.70, .65, .70), (.80, .70, .80))
MIXED_PROBABILITIES = ((.70, .65, .90), (.80, .70, .75))


def _logistic(x: float) -> float:
    if x >= 0:
        y = math.exp(-x)
        return 1/(1+y)
    y = math.exp(x)
    return y/(1+y)


def _colony_rate(p: float, log_odds_shift: float) -> float:
    if not 0 < p < 1:
        raise ValueError("simulated Bernoulli success probabilities must be in (0,1)")
    return _logistic(math.log(p/(1-p))+log_odds_shift)


def _one_colony(
    rng: random.Random,
    table: tuple[tuple[float, ...], ...],
    *,
    trials_per_cell: int,
    colony_logit_sd: float,
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    # Each colony gets a shared random effect across reports and arms.
    colony_effect = rng.gauss(0.0,colony_logit_sd)
    group=[]
    for report in REPORTS:
        scores=[]
        for j in range(3):
            probability=_colony_rate(table[report][j],colony_effect)
            successes=sum(rng.random()<probability for _ in range(trials_per_cell))
            scores.append(successes/trials_per_cell)
        group.append(tuple(scores))
    return (group[0],group[1])


def _group_mean(clusters: list[tuple[tuple[float,...], ...]]):
    if not clusters:
        raise ValueError("no independent biological clusters")
    n=len(clusters)
    return tuple(
        tuple(sum(cluster[old][arm] for cluster in clusters)/n for arm in range(3))
        for old in REPORTS
    )


def _values(means, policy):
    J_conditional=sum(TARGET[o]*means[o][policy[o]] for o in REPORTS)
    J_passive=sum(TARGET[o]*means[o][0] for o in REPORTS)
    J_query=sum(TARGET[o]*means[o][2] for o in REPORTS)
    return (
        J_conditional-J_passive,
        J_conditional-J_query,
        J_conditional-max(J_passive,J_query),
    )


def _quantile(vals: list[float], fraction: float) -> float:
    ordered=sorted(vals)
    return ordered[min(len(ordered)-1,int(len(ordered)*fraction))]


@dataclass(frozen=True)
class OperatingCharacteristicReceipt:
    scenario: str
    repetitions: int
    bootstrap_draws_per_repetition: int
    clusters_train: int
    clusters_heldout: int
    trials_per_cluster: int
    colony_logit_sd: float
    nominal_no_cluster_contingent_gain: float
    fraction_naive_training_gain_positive: float
    fraction_heldout_gain_positive: float
    fraction_joint_lower_bounds_both_positive: float
    fraction_training_learned_mixed_policy: float
    fraction_training_learned_correct_mixed_policy: float
    mean_naive_training_gain: float
    mean_heldout_gain: float
    mean_heldout_conditional_minus_passive: float
    mean_heldout_conditional_minus_query: float
    mean_simultaneous_lower_bound: float
    monte_carlo_standard_error_of_joint_pass_fraction: float
    status: str


def repeated_assay(
    *,
    scenario: str,
    repetitions: int=250,
    bootstrap_draws: int=400,
    clusters_train: int=30,
    clusters_heldout: int=30,
    trials_per_cell: int=12,
    colony_logit_sd: float=.55,
    seed: int=519280,
) -> OperatingCharacteristicReceipt:
    if scenario not in ("null","mixed"):
        raise ValueError("scenario must be null or mixed")
    if not all(isinstance(z,int) and z>0 for z in
               (repetitions,bootstrap_draws,clusters_train,clusters_heldout,
                trials_per_cell)):
        raise ValueError("repetitions, cluster counts and trial counts must be positive integers")
    if min(clusters_train,clusters_heldout)<4:
        raise ValueError("need >=4 independent clusters per phase")
    if not math.isfinite(colony_logit_sd) or colony_logit_sd<0:
        raise ValueError("colony_logit_sd must be finite and nonnegative")
    if not isinstance(seed,int):
        raise ValueError("seed must be integer")
    table=NULL_PROBABILITIES if scenario=="null" else MIXED_PROBABILITIES
    nominal_policy=(2,0)
    nominal=_values(table,nominal_policy)[2]
    stats={
        "training_positive":0,"heldout_positive":0,"detected":0,
        "mixed_policy":0,"correct_policy":0,
        "training_gain":0.,"heldout_gain":0.,
        "heldout_dp":0.,"heldout_dq":0.,"heldout_lower":0.,
    }
    # Separate deterministic seed for each Monte Carlo repetition so a
    # replication can be isolated if an unexpected calibration result occurs.
    for iteration in range(repetitions):
        rng=random.Random(seed+17*iteration)
        train=[
            _one_colony(rng,table,trials_per_cell=trials_per_cell,
                        colony_logit_sd=colony_logit_sd)
            for _ in range(clusters_train)
        ]
        heldout=[
            _one_colony(rng,table,trials_per_cell=trials_per_cell,
                        colony_logit_sd=colony_logit_sd)
            for _ in range(clusters_heldout)
        ]
        training_mean=_group_mean(train)
        frozen=tuple(
            2 if training_mean[old][2]>training_mean[old][0] else 0
            for old in REPORTS
        )
        training_gain=_values(training_mean,frozen)[2]
        heldout_dp,heldout_dq,heldout_gain=_values(
            _group_mean(heldout),frozen)
        dp,dq=[],[]
        for _ in range(bootstrap_draws):
            sample=[
                heldout[rng.randrange(clusters_heldout)]
                for _ in range(clusters_heldout)
            ]
            p,q,_=_values(_group_mean(sample),frozen)
            dp.append(p)
            dq.append(q)
        lower=min(_quantile(dp,.025),_quantile(dq,.025))
        stats["training_positive"]+=training_gain>1e-12
        stats["heldout_positive"]+=heldout_gain>1e-12
        stats["detected"]+=lower>0
        stats["mixed_policy"]+=frozen[0]!=frozen[1]
        stats["correct_policy"]+=frozen==nominal_policy
        stats["training_gain"]+=training_gain
        stats["heldout_gain"]+=heldout_gain
        stats["heldout_dp"]+=heldout_dp
        stats["heldout_dq"]+=heldout_dq
        stats["heldout_lower"]+=lower
    n=repetitions
    passes=stats["detected"]/n
    return OperatingCharacteristicReceipt(
        scenario=scenario,
        repetitions=n,
        bootstrap_draws_per_repetition=bootstrap_draws,
        clusters_train=clusters_train,
        clusters_heldout=clusters_heldout,
        trials_per_cluster=6*trials_per_cell,
        colony_logit_sd=colony_logit_sd,
        nominal_no_cluster_contingent_gain=nominal,
        fraction_naive_training_gain_positive=stats["training_positive"]/n,
        fraction_heldout_gain_positive=stats["heldout_positive"]/n,
        fraction_joint_lower_bounds_both_positive=passes,
        fraction_training_learned_mixed_policy=stats["mixed_policy"]/n,
        fraction_training_learned_correct_mixed_policy=stats["correct_policy"]/n,
        mean_naive_training_gain=stats["training_gain"]/n,
        mean_heldout_gain=stats["heldout_gain"]/n,
        mean_heldout_conditional_minus_passive=stats["heldout_dp"]/n,
        mean_heldout_conditional_minus_query=stats["heldout_dq"]/n,
        mean_simultaneous_lower_bound=stats["heldout_lower"]/n,
        monte_carlo_standard_error_of_joint_pass_fraction=math.sqrt(
            passes*(1-passes)/n
        ),
        status="SYNTHETIC_POLICY_VALIDATION_CALIBRATION_NOT_ECOLOGICAL_POWER",
    )


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--repetitions",type=int,default=250)
    p.add_argument("--bootstrap-draws",type=int,default=400)
    p.add_argument("--clusters-train",type=int,default=30)
    p.add_argument("--clusters-heldout",type=int,default=30)
    p.add_argument("--trials-per-cell",type=int,default=12)
    p.add_argument("--colony-logit-sd",type=float,default=.55)
    p.add_argument("--seed",type=int,default=519280)
    p.add_argument("--output",type=str)
    args=p.parse_args()
    common=dict(
        repetitions=args.repetitions,
        bootstrap_draws=args.bootstrap_draws,
        clusters_train=args.clusters_train,
        clusters_heldout=args.clusters_heldout,
        trials_per_cell=args.trials_per_cell,
        colony_logit_sd=args.colony_logit_sd,
        seed=args.seed,
    )
    scenarios=[asdict(repeated_assay(scenario=x,**common))
               for x in ("null","mixed")]
    output=json.dumps({
        "schema":"adaptive-gain-heldout-query-policy-monte-carlo-v1",
        "scenarios":scenarios,
        "claim_ceiling":"Synthetic clustered Bernoulli scenarios only; no bee sample-size, genetic selection or guaranteed test validity.",
    },indent=2)+"\n"
    if args.output:
        with open(args.output,"w",encoding="utf-8") as f:
            f.write(output)
    else:
        print(output,end="")


if __name__=="__main__":
    main()
