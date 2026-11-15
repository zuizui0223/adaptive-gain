# Stage23 — exact intermediate-cost window for conditional information access

**2026-11-15 — EXACT SOURCE-FREE MATHEMATICS ONLY. No new bees, no animal data, no ecological fitness results.** This Draft is stacked on Stage22 PR #100; main, all prior PRs, original data, V5 and V6 remain unchanged.

## Frozen eight-world task

R~Bern(1/2), U~Bern(1/5), V~Bern(1/2) independently and freshly resampled each trial. Correct target T=U for true R0 and V for true R1. Root class accuracies (s0,s1)=(4/5,3/5). Paid U class accuracies (aU0,aU1)=(1,1). Paid V class accuracies (aV0,aV1)=(1,9/10). Correct target gives 1 normalized reward, wrong target 0; each source purchase costs c>=0 in the same hypothetical reward units. Each U or V source may be bought once, with an optional second distinct source.

Both arms see the noisy root Z. The contingent arm selects first SKIP/U/V after Z. The precommit arm must select its first SKIP/U/V before Z, although its optional second paid source may depend on later observations.

## All-cost exact piecewise gain theorem

All finitely many deterministic first choices, optional second choices and final predictions can be represented as affine payoffs B-c*N, where B is expected correctness and N is the expected number of paid source purchases. Exact Fraction policy enumeration certifies the global optimal upper envelopes for every c>=0:

| Cost c | Contingent optimum | Precommitted optimum | Delta=contingent-precommit |
|---|---|---|---|
| 0 <= c <= 2/15 | 419/500 - c | 419/500 - (7/5)c | (2/5)c |
| 2/15 <= c <= 47/350 | 379/500 - (2/5)c | 419/500 - (7/5)c | c - 2/25 |
| 47/350 <= c <= 27/100 | 379/500 - (2/5)c | 13/20 | 27/250 - (2/5)c |
| c >= 27/100 | 13/20 | 13/20 | 0 |

**Strict positive benefit occurs exactly for 0<c<27/100.** The global unique maximum is at **c=47/350≈0.134286**, where **Delta=19/350≈0.054286 normalized reward units**. At c=1/4, Delta=1/125=0.008 exactly recovers the existing Stage22 result. At c=0 both arms can acquire all valuable information free; at c>=.27 both skip. These numeric thresholds are specific to this constructed model, not universal sensory thresholds.

For 0<c<2/15, the contingent agent purchases U after Z0 and V after Z1 (one query per trial), whereas precommit buys U first and then V after Z1 (expected 7/5 queries). For 2/15<c<47/350, contingent SKIPs on Z0 and buys V on Z1, while precommit still buys U. For 47/350<c<27/100, precommit SKIPs and contingent still conditionally buys V on Z1. Equal-value ties occur at some exact boundaries.

## Exhaustiveness of the certificate

The proof module research/bee_cost_window_stage23/exact_cost_frontier.py computes exact rational joint masses, propagates the Z/U/V class-conditional confusion channels, constructs every relevant deterministic first and conditional second query policy, and retains its (gross_correct, expected_query_count) pair. Domination pruning preserves the maximum for every nonnegative c. Exact intersection checks between all remaining affine lines produce both optimal envelopes on [0,infinity), not merely a sampled parameter plot.

The independent test module research/bee_cost_window_stage23/test_exact_cost_frontier.py has five tests for the full envelopes, rational values at breakpoints, a 401-value cost-grid regression, an independently normalized Bayesian posterior oracle at 85+ rational costs, and explicit no-animal provenance. The fresh c=1/4 evaluation reduces to the prior frozen Stage22 numerical example.

## Biological interpretation limits

This is a mathematically constructed counterexample to monotonic improvement of conditional access with growing information cost. It does not establish animal decision optimality, evolved cognition, reproductive fitness, field behavior, or that real bees occupy the derived cost interval. No calibrated cost in seconds/energy/sucrose, original animal source requests, separately measured six class-specific confusion rates, colony variance, learned source priors, reward exchange rates, or ethics approval were gathered. Source-specific costs and different priors require a different theorem or a new numerical phase diagram. GitHub dedicated and full-repo CI statuses require separate verification.

**Biological STOP:** do not generalize the 0.27 cutoff or the 0.134286 optimum to pollination without separately validated perceptual recognition, priors, costs, voluntary queries, independent colony replication, and a randomized precommit-vs-contingent experimental design.
