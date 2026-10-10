"""Held-out validation of a conditional cue-acquisition policy in a randomized assay.

Use only trials from a NEW experiment with three externally assigned regimes:
  passive: no new cue; the animal may choose permitted passive timing
  sham:    noninformative cue and matched port/time/cost
  query:   informative calibrated cue and matched port/time/cost

The policy π(O) chooses passive or query using the *old cue report* O.
Its performance and those of BOTH fixed alternatives must be evaluated on
completely held-out animals or colonies, not the data that selected π.

This estimates performance of the EXECUTED assigned-regime behavior, not
the Bayes-optimal timing policy's mathematical ceiling, free animal
choice, evolved heritable fitness, or a controlled signal-only effect
without the experimental exclusion restrictions.

Design limitations: assignment probabilities must be fixed within each
old-report stratum, nonzero for all arms, and genuinely randomized.
Targets weights for old reports are externally declared; sampling rare
states disproportionately must not silently change the deployment target.
Two one-sided Bonferroni-corrected 97.5% percentile bootstrap bounds form
a conservative simultaneous 95% confidence statement. These are
approximate cluster-bootstrap intervals, not exact randomization tests.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Iterable

ARMS = ("passive", "sham", "query")
REPORTS = (0, 1)


@dataclass(frozen=True)
class FrozenQueryPolicy:
    """A previously selected old-report -> acquisition-arm rule."""
    old_zero: str
    old_one: str

    def __post_init__(self):
        if self.old_zero not in ("passive", "query"):
            raise ValueError("old_zero must be passive or query")
        if self.old_one not in ("passive", "query"):
            raise ValueError("old_one must be passive or query")

    def arm(self, report: int) -> str:
        if report == 0:
            return self.old_zero
        if report == 1:
            return self.old_one
        raise ValueError("old_report must be 0 or 1")


@dataclass(frozen=True)
class HeldoutPolicyReceipt:
    frozen_policy: FrozenQueryPolicy
    number_of_evaluation_trials: int
    independent_clusters: int
    evaluated_cluster_bootstrap_replicates: int
    target_old_report_weights: tuple[float, float]
    recorded_randomization_probabilities: tuple[tuple[float, float, float], tuple[float, float, float]]
    conditional_reward: float
    always_passive_reward: float
    always_query_reward: float
    always_sham_reward: float
    conditional_minus_passive: float
    conditional_minus_query: float
    conditional_minus_best_fixed: float
    query_minus_sham: float
    lower_97_5_percent_passive_contrast: float
    lower_97_5_percent_query_contrast: float
    simultaneous_95_percent_gain_lower: float
    query_minus_sham_95_percent_interval: tuple[float, float]
    conditional_better_than_both_fixed_at_approx_95_percent: bool


def validate_target(target_old_report_weights: dict[int, float]) -> tuple[float, float]:
    if set(target_old_report_weights) != {0, 1}:
        raise ValueError("declare target weights for old reports 0 and 1")
    vals = tuple(float(target_old_report_weights[i]) for i in REPORTS)
    if not all(math.isfinite(v) and 0 < v < 1 for v in vals):
        raise ValueError("both target old-report states must have positive weights")
    if not math.isclose(sum(vals), 1.0, abs_tol=1e-12, rel_tol=0):
        raise ValueError("target report weights must sum to 1")
    return vals


def validate_design_probabilities(
    assignment_probabilities: dict[int, dict[str, float]]
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    """The externally preregistered arm probabilities for each old report."""
    if set(assignment_probabilities) != {0, 1}:
        raise ValueError("declare randomized arm probabilities for both old reports")
    design=[]
    for o in REPORTS:
        options=assignment_probabilities[o]
        if set(options) != set(ARMS):
            raise ValueError("all three arms must have known assignment probabilities")
        values=tuple(float(options[arm]) for arm in ARMS)
        if not all(math.isfinite(v) and 0<v<1 for v in values):
            raise ValueError("arm assignment probabilities must be strictly positive")
        if not math.isclose(sum(values),1,abs_tol=1e-12,rel_tol=0):
            raise ValueError("each old-report assignment probabilities must sum to one")
        design.append(values)
    return (design[0],design[1])


def validate_trials(records: Iterable[dict], *, min_unique_clusters: int = 2) -> list[dict]:
    rows = list(records)
    if not rows:
        raise ValueError("no trials")
    clusters = set()
    for row in rows:
        if not {"cluster", "old_report", "assigned_arm", "reward", "assignment_probability"}.issubset(row):
            raise ValueError("trial missing cluster, old_report, assigned_arm, reward or assignment_probability")
        if not isinstance(row["cluster"], str) or not row["cluster"]:
            raise ValueError("cluster identifier must be nonempty string")
        clusters.add(row["cluster"])
        if type(row["old_report"]) is not int or row["old_report"] not in REPORTS:
            raise ValueError("old_report must be 0 or 1, not delivered information")
        if row["assigned_arm"] not in ARMS:
            raise ValueError("assigned_arm must be passive, sham or query")
        try:
            v = float(row["reward"])
        except (TypeError, ValueError):
            raise ValueError("reward must be numeric") from None
        if not math.isfinite(v):
            raise ValueError("reward must be finite")
        try:
            prob=float(row["assignment_probability"])
        except (TypeError,ValueError):
            raise ValueError("assigned probability must be numeric") from None
        if not math.isfinite(prob) or not 0<prob<=1:
            raise ValueError("assigned probability must be positive and <=1")
    if len(clusters) < min_unique_clusters:
        raise ValueError("too few independent biological clusters")
    return rows


def by_cluster_holdout(
    records: Iterable[dict],
    *,
    test_fraction: float = 0.5,
    seed: int = 1492,
) -> tuple[list[dict], list[dict]]:
    """Independent train/test split by colony or bee ID, never by trial."""
    if not 0 < test_fraction < 1:
        raise ValueError("test_fraction must lie strictly between 0 and 1")
    rows = validate_trials(records)
    keys = sorted({r["cluster"] for r in rows})
    if len(keys) < 4:
        raise ValueError("at least four clusters needed to create holdout")
    rng = random.Random(seed)
    rng.shuffle(keys)
    k = min(len(keys)-2, max(2, round(len(keys)*test_fraction)))
    heldout = set(keys[:k])
    train = [r for r in rows if r["cluster"] not in heldout]
    test = [r for r in rows if r["cluster"] in heldout]
    assert not ({x["cluster"] for x in train} & {x["cluster"] for x in test})
    return train, test


def _cell_means(records: list[dict]) -> dict[tuple[int, str], float]:
    acc = {(o,a): [0,0.0] for o in REPORTS for a in ARMS}
    for r in records:
        cell=acc[(r["old_report"], r["assigned_arm"])]
        cell[0]+=1
        cell[1]+=float(r["reward"])
    if any(n == 0 for n,s in acc.values()):
        raise ValueError("randomized-trial positivity failure: empty old-report/arm cell")
    return {key: s/n for key,(n,s) in acc.items()}


def learn_query_policy(training_trials: Iterable[dict]) -> FrozenQueryPolicy:
    """Freeze a policy using training clusters only; ties favor passive."""
    means = _cell_means(validate_trials(training_trials))
    choice = [
        "query" if means[(old,"query")] > means[(old,"passive")]
        else "passive"
        for old in REPORTS
    ]
    return FrozenQueryPolicy(*choice)


def _values(
    samples: list[dict],
    policy: FrozenQueryPolicy,
    weights: tuple[float, float],
) -> tuple[float, float, float, float]:
    means = _cell_means(samples)
    conditional = sum(weights[o]*means[(o,policy.arm(o))] for o in REPORTS)
    passive = sum(weights[o]*means[(o,"passive")] for o in REPORTS)
    query = sum(weights[o]*means[(o,"query")] for o in REPORTS)
    sham = sum(weights[o]*means[(o,"sham")] for o in REPORTS)
    return conditional, passive, query, sham


def _percentile(values: list[float], fraction: float) -> float:
    if not values or not 0<=fraction<=1:
        raise ValueError("invalid bootstrap percentile")
    ordered = sorted(values)
    return ordered[min(len(ordered)-1, int(len(ordered)*fraction))]


def evaluate_frozen_policy(
    evaluation_trials: Iterable[dict],
    policy: FrozenQueryPolicy,
    *,
    target_old_report_weights: dict[int, float],
    assignment_probabilities: dict[int,dict[str,float]],
    bootstrap_repetitions: int = 1000,
    seed: int = 86023,
) -> HeldoutPolicyReceipt:
    """Check BOTH fixed policies on held-out independent clusters.

    Familywise guard: lower 2.5% bootstrap percentile for each of
    (J_conditional-J_passive) and (J_conditional-J_query). Under regularity,
    each one-sided lower bound is ~97.5%; the two simultaneously hold
    with at least ~95% nominal coverage by Bonferroni. A positive minimum
    is an approximate held-out confirmation against both fixed regimes.

    Do not report an upper-biased in-sample max over old-report actions
    as policy value. Bootstrap resamples CLUSTERS, not independent trials.
    """
    if not isinstance(bootstrap_repetitions,int) or bootstrap_repetitions<20:
        raise ValueError("at least 20 cluster-bootstrap draws required")
    weights=validate_target(target_old_report_weights)
    design=validate_design_probabilities(assignment_probabilities)
    trials=validate_trials(evaluation_trials)
    for row in trials:
        p=assignment_probabilities[row["old_report"]][row["assigned_arm"]]
        if not math.isclose(float(row["assignment_probability"]),p,
                            abs_tol=1e-12,rel_tol=0):
            raise ValueError("recorded randomization probability disagrees with declared design")
    groups={}
    for r in trials:
        groups.setdefault(r["cluster"],[]).append(r)
    cluster_ids=sorted(groups)
    if len(cluster_ids)<4:
        raise ValueError("need at least four independent held-out clusters")
    c,p,q,s=_values(trials,policy,weights)
    rng=random.Random(seed)
    ds_p,ds_q,ds_sham=[],[],[]
    for _ in range(bootstrap_repetitions):
        sampled=[]
        for _ in cluster_ids:
            sampled.extend(groups[rng.choice(cluster_ids)])
        try:
            bc,bp,bq,bs=_values(sampled,policy,weights)
        except ValueError:
            continue  # positivity failed in this cluster resample
        ds_p.append(bc-bp)
        ds_q.append(bc-bq)
        ds_sham.append(bq-bs)
    if len(ds_p)<bootstrap_repetitions*.90:
        raise ValueError("bootstrap positivity too weak: more animals/colonies per stratum needed")
    lower_p=_percentile(ds_p,.025)
    lower_q=_percentile(ds_q,.025)
    gain=min(c-p,c-q)
    return HeldoutPolicyReceipt(
        frozen_policy=policy,
        number_of_evaluation_trials=len(trials),
        independent_clusters=len(groups),
        evaluated_cluster_bootstrap_replicates=len(ds_p),
        target_old_report_weights=weights,
        recorded_randomization_probabilities=design,
        conditional_reward=c,
        always_passive_reward=p,
        always_query_reward=q,
        always_sham_reward=s,
        conditional_minus_passive=c-p,
        conditional_minus_query=c-q,
        conditional_minus_best_fixed=gain,
        query_minus_sham=q-s,
        lower_97_5_percent_passive_contrast=lower_p,
        lower_97_5_percent_query_contrast=lower_q,
        simultaneous_95_percent_gain_lower=min(lower_p,lower_q),
        query_minus_sham_95_percent_interval=(
            _percentile(ds_sham,.025),
            _percentile(ds_sham,.975),
        ),
        conditional_better_than_both_fixed_at_approx_95_percent=(
            min(lower_p,lower_q)>0
        ),
    )


def fit_then_holdout_evaluate(
    records: Iterable[dict],
    *,
    target_old_report_weights: dict[int,float],
    assignment_probabilities: dict[int,dict[str,float]],
    test_fraction: float = .5,
    split_seed: int = 1492,
    bootstrap_repetitions: int = 1000,
    bootstrap_seed: int = 86023,
) -> HeldoutPolicyReceipt:
    """Convenience workflow without contaminating the evaluation sample."""
    train,test=by_cluster_holdout(records,test_fraction=test_fraction,seed=split_seed)
    pi=learn_query_policy(train)
    return evaluate_frozen_policy(
        test,pi,target_old_report_weights=target_old_report_weights,
        assignment_probabilities=assignment_probabilities,
        bootstrap_repetitions=bootstrap_repetitions,
        seed=bootstrap_seed,
    )
