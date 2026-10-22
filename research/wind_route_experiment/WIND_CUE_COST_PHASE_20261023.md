# Wind-induced information-acquisition cost can reverse the interaction value of unrelated species' cues

**2026-10-23. EXACT EXPLORATORY SYNTHETIC RESULT.** Original result branch parent: `analysis/wind-multispecies-zero-mi-synergy-20261023`. This extension changes the **cost of obtaining habitat/other-species cues**, not their content, error probability, marginal correlation with payoff or ecological species composition. This does **not** establish a real wind effect on cognitive effort, a specific heterospecific interaction, improved pollination or evolutionary fitness. Preserve `main` and frozen manuscripts.

## One actual new conclusion

For 16 equiprobable environmental branches B, an independent target T∈{0,1}, two source species A and B revealing DIFFERENT branch bits, 16 branch-specific floral binary tests F_b, budget K=5, and independently flipped source bits with error e=10%:

| Source A/B query costs | P_correct using neither | Using A | Using B | Using A+B | Complementarity P_AB−P_A−P_B+P_0 | Improvement versus best FIXED cues |
|---|---:|---:|---:|---:|---:|---:|
| 1 / 1 | .65625 | .725 | .725 | **.80375** | **+.01000** | +.14750 |
| 1 / 2 | .65625 | .725 | .66875 | **.725** | **−.01250** | +.06875 |
| 2 / 2 | .65625 | .66875 | .66875 | **.66875** | **−.01250** | +.01250 |

Exact fractions for 1/1: P_AB=643/800, synergy=1/100; for 1/2: P_AB=29/40, synergy=−1/80. The 1→2 cost of acquiring **B's bit** produces **7.875 percentage point loss in combined optimal accuracy** and a **2.25 point shift in the factorial A×B complementarity**, without changing B's reliability, target frequencies or joint information. With source A available, adding B at cost=2 provides **exactly zero** extra correctness for K=5 although B is a distinct environmental bit.

**Crucial logical distinction:** negative factorial complementarity does NOT mean another species harms an optimal decision maker. A larger OPTIONAL information vocabulary always contains the strategies from its smaller vocabulary. All 108 cost×budget×noise grid entries respect P_AB>=max(P_A,P_B,P_0), with the negative interaction indicating subadditive gains relative to the **sum** of isolated source benefits.

## Exact model

- Worlds (B,T) uniformly in {0..15}×{0,1}, with B and T independent. `F_j=1` iff B=j AND T=1; otherwise F_j=0.
- Species A reports branch bit 0 and species B reports branch bit 1, symmetrically corrupted at the fixed rates. Joint source errors can have P(both wrong)=q in its probability-valid interval. Both species together have **zero marginal information about the target**, I(S_A,S_B;T)=0; only the NEXT flower test's identity turns them into useful routing cues.
- Every floral test costs 1 unit. Querying S_A costs c_A and querying S_B costs c_B, positive integers. Observations cannot be reused. Every sequential adaptive acquisition policy and stop/guess decision is optimized over the SAME hard integer budget K. Fixed policies choose their cues without examining outcomes; their optimal accuracy remains P_F=1/2+min(K,16)/32 as long as all source costs are positive.
- The experimental intervention is **hypothetical**: weather could increase physical access/attention/time needed to inspect species B while leaving its signal unchanged. No previous PoMS, Andrews, Crall, Balfour or wind-tunnel dataset measures this B-specific cue cost.

### Noiseless constructive benchmark and cost thresholds

For two perfect independent environmental bits, the 16-branch decision problem's cost-weighted subset-first coverage candidate, verified by direct exact dynamic program for **162** distinct (branch depth d=2..4, K=0..8, cost-pair) parameter combinations, is

[
P_A^{\mathrm{perfect}}=\frac12+\frac{1}{2n}\max_{S\subseteq\{A,B\}}\min\left\{n,2^{|S|}\max\left(0,K-\sum_{j\in S}c_j\right)\right\},\quad n=2^d.
]

For n=16, K=5, c_A=1:
- c_B=1: coverage no cues=5, A=8, B=8, AB=12; adaptive P_AB=7/8, factorial synergy **+1/32**.
- c_B=2: coverage no cues=5, A=8, B=6, AB=8; adaptive P_AB=3/4, factorial synergy **−1/32**.
- In the unsaturated two-bit-vs-A comparison, B's second bit expands potential perfect coverage beyond A alone only if `4(K−c_A−c_B)>2(K−c_A)`, equivalent to `K>c_A+2c_B`. At K=5, (c_A,c_B)=(1,2) lies exactly on the boundary. This condition is specifically for the *given* coverage construction; it is NOT a universal causal law of wind/competitors.

### Budget/reliability counterexamples

At K=5, e=.1, cA,cB=1,2, A×B complementarity is **negative (−1.25pp)**. But with the SAME two source costs and e=.1 at K=7, the complementarity is **positive (+0.50pp)**. With both costs 1 and K=5 the complementarity is +1pp, but with both costs 1 and K=7 it is **−4pp**. Thus neither more budget nor more species monotonically increases the *factorial synergy*; availability never reduces the optimal success itself.

At fixed cost (1,1) and e=.15, varying joint error probability q while keeping source-specific error marginals equal can change synergy from **−0.625pp** at q=0 (mutually exclusive errors), to **+0.21875pp** at independent q=e², to **+5pp** at q=e (fully shared errors). These error-dependence results come from the earlier base model; the new cost analysis retains the exact correlated error law rather than silently assuming independence.

## Independent computation and validation

- `costly_cues.py`: full finite exact Bayesian policy DP with positive integer per-source query costs and an explicit joint error distribution. It uses exact fractions/integer likelihood masses; the "all negative floral history" optimization is justified by the constructed source-conditioned T0 posterior dominating T1 under missing positive floral observations.
- `independent_posterior.py`: a separate Bayes DP which retains BOTH terminal target posterior masses, optimizes STOP vs every query and treats correlated error bits as explicit hidden worlds. **60** heterogeneous-cost/branch/budget/error settings agree *exactly* with the optimized routine. This audit avoids relying on the positive-hit-only shortcut.
- `test_costly_cues.py`: **178** independently run tests passed before archiving, including source costs, negative synergy but nonnegative optional cue value, cost-monotonicity, 162-point perfect candidate comparison, and correlated errors.
- `run_analysis.py`: fixed grid of **108** outcomes (K=3..8, e=0/.10/.15, six source cost pairs), **18** correlated-noise+cost contrasts, **162** perfect-cost formula checks, **60** independent posterior checks. Exact strings & decimals saved in CSV and JSON, with SHA256 code/output receipt. Derived values are **not observational sample estimates**, CI or scientific evidence of fitness.
- The original model and frozen manuscript remain untouched on the parent branch.

## Minimal discriminating ecological experiment

1. First calibrate that unrelated species A and B transmit DIFFERENT habitat/branch bits, their target I(S_A,S_B;T) is approximately zero, and each predicts a different subset of floral tests. Independent *species identity alone* is NOT proof of different information.
2. Randomize wind and independently manipulate **B cue acquisition time/visibility** while holding B's branch prediction correctness fixed; measure realized observation cost (time/energy/risk) and errors rather than importing the synthetic 1/2 units.
3. Randomize B cue present/absent with A available, match environmental branch and floral payoffs, give the animals an operational **intermediate deadline**. At a budget equivalent to K=5, test for benefit of B at low cost and *loss of its incremental benefit at higher cost* despite unchanged informational content. Use sham cues and a higher-budget condition K=7 as predeclared boundary/falsifier. Randomize forced cue order first to measure feasible accuracy; only voluntary cue choice supports actual adaptive information acquisition.
4. Separate **correct decisions**, time to suitable flower, pollen transfer/reward, and survival. Expected net benefit must subtract actual search/handling/exposure costs. No claim that changing the information budget increases genetic fitness until empirical reward and costs are measured.

**Novelty limit:** This is a finite constructed phase boundary for cost-dependent conditional information synergies, not a new proof of a general ecological interaction mechanism or an experimental test that wind changes other-species sensing costs. The broad claim "wind affects predator/prey via microhabitats" has prior experimental literature, so a paper would need the query-order and available-information distinction to add knowledge.
