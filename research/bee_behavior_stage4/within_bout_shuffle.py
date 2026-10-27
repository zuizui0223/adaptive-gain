"""Held-out bout-order permutation control preserving all visited flower identities.

Shuffles flower order ONLY within each last-day original individual foraging
bout. Each bee's observed number of bouts, bout lengths, flower IDs and
within-bout visit counts, together with all earlier-day fitted probabilities,
are unchanged. Conditional test of ordering beyond the heldout bout's plant/
flower multiset, NOT randomization of cognitive cue acquisition.
"""
from __future__ import annotations
import math
import random
from statistics import median
from bout_transition_analysis import history_holdout_on_bouts

SHUFFLES=199
SEED=20261028

def _last_day_shuffled(bouts,day,rng):
    shuffled=[]
    for bout in bouts:
        if bout["day"]!=day or len(bout["flowers"])<2:
            shuffled.append(bout)
        else:
            copy=dict(bout)
            flowers=list(bout["flowers"])
            rng.shuffle(flowers)
            copy["flowers"]=flowers
            shuffled.append(copy)
    return shuffled

def conditional_bout_order_test(original_bouts,permutations=SHUFFLES,seed=SEED):
    if permutations<1:raise ValueError("number of permutations must be positive")
    primary=history_holdout_on_bouts(original_bouts)
    report={
        "status":"not_run",
        "null_hypothesis":"within heldout bee-bout flower order exchangeable given observed visited flower multiset; fixed earlier-day model",
        "permutations":permutations,
        "random_seed":seed,
        "primary_status":primary["status"],
        "same_train_day_predictions_under_all_shuffles":True,
        "within_bout_multisets_fixed":True,
        "no_across_bout_transition":True,
        "not_cognitive_cue_order_or_social_displacement_test":True
    }
    if primary["status"]!="FITTED_HELDOUT_BEHAVIORAL_DESCRIPTIVE":
        report["status"]="NO_GO_PRIMARY_HOLDOUT_INSUFFICIENT"
        return report
    if len({b["bee"] for b in original_bouts})<5:
        raise ValueError("underlying independent unit count inconsistent")
    last=primary["last_source_day_heldout"]
    observed=primary["mean_per_bee_gain_nats"]
    rng=random.Random(seed)
    shuffled_gains=[]
    for i in range(permutations):
        new_bouts=_last_day_shuffled(original_bouts,last,rng)
        val=history_holdout_on_bouts(new_bouts)
        if val["status"]!="FITTED_HELDOUT_BEHAVIORAL_DESCRIPTIVE":
            raise ValueError("null shuffle unexpectedly changed bee eligibility")
        if val["bee_count_evaluable"]!=primary["bee_count_evaluable"]:
            raise ValueError("null shuffle changed per-bee scientific population")
        shuffled_gains.append(val["mean_per_bee_gain_nats"])
    sorted_gain=sorted(shuffled_gains)
    # One-tailed test of whether observed sequence ordering supports more
    # *future* predictive advantage than visit-bag permutation alone.
    n_at_least=sum(g+1e-12>=observed for g in shuffled_gains)
    report.update({
        "status":"COMPUTED_DESCRIPTIVE_CONDITIONAL_BOUT_ORDER_TEST",
        "observed_bee_mean_M1_gain_nats":observed,
        "null_mean_gain_nats":sum(shuffled_gains)/len(shuffled_gains),
        "null_median_gain_nats":median(shuffled_gains),
        "null_min_gain_nats":min(shuffled_gains),
        "null_max_gain_nats":max(shuffled_gains),
        "null_quantile05_gain_nats":sorted_gain[math.floor(.05*(len(sorted_gain)-1))],
        "null_quantile95_gain_nats":sorted_gain[math.floor(.95*(len(sorted_gain)-1))],
        "observed_minus_null_mean_gain_nats":observed-sum(shuffled_gains)/len(shuffled_gains),
        "positive_tail_monte_carlo_p":(n_at_least+1)/(permutations+1),
        "eligible_bees":primary["bee_count_evaluable"],
        "source_daily_train_and_heldout_records_untouched":True
    })
    return report
