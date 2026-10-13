# Budget-limited noise dependence: a calibration-order result

**Status:** supporting ecological identification audit for PR #68. Not a new MAIN theorem, not an observed pollinator behavior or an estimated fitness advantage. Frozen V5/V6 submission surfaces are unchanged.

## Main question and resolution

Do we need to measure three-cue error correlations when the animal can acquire only two cues? **No, not under the static nonreactive readout model.** But can the *average* of the three pairwise error correlations predict the value of contingent sensing? **No.** The identity of the correlated cue pair matters.

These two statements prevent both overmeasurement (unneeded third-order correlations for a two-query policy) and undermeasurement (a pooled pairwise correlation that discards task-relevant identity).

### Budget-limited conditional-marginal sufficiency

Let `W` be a finite ecological state with positive prior. Each cue `j` has cost `c_j>0`, may be requested at most once, and reveals one coordinate `Z_j` of a **nonreactive potential readout vector**. Requesting `Z_j` does not change other potential observations or the underlying state. Consider two environments with identical state priors, targets, query costs, hard budget `B`, and reward functions.

Suppose for **every state** `w`, every affordable subset `S` with total acquisition cost `<=B`, and every observable outcome `z_S`, both environments agree on the conditional probability `P(Z_S=z_S | W=w)`. Then every adaptive policy tree, including outcome-dependent choice of the next cue and a terminal abstain option, has the **same expected payoff** in the two environments. The optimal adaptive and fair precommitted-partial-subset values therefore agree, too.

**Proof.** Every terminal path observes a particular `z_S` on one affordable subset `S`. Its conditional probability in state `w` is the corresponding `S` marginal. The common model assigns the same decision, cost and reward to that path; each leaf's contribution to expectation is equal. Sum over leaves/states and take the maximum over a common policy class. Randomized policies follow by convex mixing.

This proposition is deliberately scoped to *static* finite cue access. If the animal's earlier sensing changes later cue values, the state, perception reliability or encounter context, a stateful sequential-observation kernel is needed. Equality of **unconditional** cue marginals alone does not suffice; calibration must account for ecological state/target.

## Complete triple-only variation has no effect with two acquisitions

Consider the existing five-state topology A (targets `0,1,1,0,0`, cues root `0,0,1,1,0`, left `0,1,0,0,0`, right `0,0,0,1,0`) and prior `(1/3,1/6,1/6,1/6,1/6)`. Its declared cue bits are independently perturbed from the latent state by a joint error vector `E=(E0,E1,E2)` that is independent of the ecological world.

Hold every cue's flip rate at `e=1/10` and every pair's simultaneous-flip probability at `h=9/200`. Let the *triple* flip probability `a=P(E0=E1=E2=1)` vary freely within the feasible closed interval `[0,9/200]`. The eight error-pattern masses are

- `P(000)=1-3e+3h-a`;
- each one-flip pattern: `e-2h+a`;
- each two-flip pattern: `h-a`;
- `P(111)=a`.

All distributions on this interval share the same **three separately labeled pairwise distributions** and one-cue marginals, though their full three-way laws are different. At budget 2 and wrong-choice loss `L=4`, each has optimal adaptive payoff `7/15` and optimal precommitted payoff `11/30`: the contingent premium is `1/10`. Tests also check multiple losses, topologies A/B and both policy classes against a separate Fraction policy-tree oracle.

If budget is raised to 3, the full three-way observation becomes affordable and its dependence can matter: at loss 4, the two endpoint laws `a=0` and `a=9/200` give overall optimal expected payoffs of `517/600` and `49/100`. With no additional query-payoff debit, precommitted full-set acquisition is already feasible, so both policy classes reach each respective optimum; this is **not** a positive contingent-acquisition premium at budget 3.

**Consequence:** for a B=2 nonreactive task, all three *individual* state-conditioned cue-pair laws are sufficient; measuring the full triple distribution is not necessary for its optimal value. For B=3, triple dependence may be relevant.

## The mean of pairwise correlations is NOT sufficient

Hold the very same task, prior, budget 2, payoff `v=1` for correct target, error cost `L=4`, and free abstention. Set controller maintenance cost `K=1/10`.

Construct two valid **world-independent** joint error laws X/Y. They keep each cue's error rate 0.1, the same all-three simultaneous-flip probability `1/50=0.02`, and the same complete distribution of the *number* of erroneous cues. Only the mapping of pair-specific error correlation onto the three **named cues** changes.

| Simultaneous misread of cues | X | Y |
|---|---:|---:|
| root + left | `1/25 = 0.040` | `1/25 = 0.040` |
| root + right | `7/100 = 0.070` | `1/40 = 0.025` |
| left + right | `1/40 = 0.025` | `7/100 = 0.070` |
| **Pairwise average** | **`9/200=0.045`** | **`9/200=0.045`** |
| all three misread | 0.020 | 0.020 |

The number-of-errors histogram is exactly the same for both X and Y:
`P(0)=163/200`, `P(1)=9/100`, `P(2)=3/40`, `P(3)=1/50`.
The pairwise Pearson error-correlation vectors are `(1/3,2/3,1/6)` and `(1/3,1/6,2/3)`, both averaging `7/18`.

An independent full Fraction oracle enumerating all feasible conditional query trees and precommitted subsets gives:

| Expected reward | X | Y |
|---|---:|---:|
| Best adaptive | `8/15` | `13/30` |
| Best precommitted | `7/20` | `7/20` |
| Gross adaptive advantage | `11/60` | `1/12` |
| Net after controller cost `K=1/10` | **`+1/12`** | **`-1/60`** |

Thus the controller's net payoff changes sign **without changing** any cue's marginal error, the pooled pairwise statistic, the three-way simultaneous flip, the error-count distribution, the prior, the target or the opportunity budget. This does **not** show an effect of hidden triple-only dependence in a two-query task; it isolates **task-aligned labeled pairwise dependence**.

This is a counterexample to adequacy of a pooled correlation statistic, not an exact bound on the worst case over all permitted joint error distributions and not evidence of real bee fitness.

## Experimental consequences

1. Record or experimentally calibrate the **specific root–left, root–right, and left–right joint confusion tables**, conditional on known true stimulus/world, rather than reporting only univariate accuracy or a pooled pair correlation. In principle, exact pair tables suffice for B=2 *within the static model*.
2. Obtain independent behavioral cue reports or verified signal-readout surrogates from the **same encounter**. A correct flower choice alone does not reveal which internal cues were misread. Retain nonresponses, latency, learning phase, actor clustering, and detection effort.
3. Cross cue-error dependence with whether the actor may select a second cue *after* observing the first, using a fair budget-matched precommitted-subset control. Match each cue's marginal confusion across treatments and verify that external perturbation dependence actually creates the intended perceptual dependence.
4. Do not generalize the numerical fractions or `K` to natural selection until errors, payoffs, acquisition costs, and heritability or invasion dynamics are independently measured.

**Prior art:** the importance of higher-order sensory correlations, and their ability to differ with unchanged lower-order statistics, is established (Cayco-Gajic, Zylberberg & Shea-Brown 2015, DOI https://doi.org/10.3389/fncom.2015.00057; Kohn et al. 2016, DOI https://doi.org/10.1146/annurev-neuro-070815-013851). The budget-limited indistinguishability argument is straightforward decision-tree reasoning. The ecological contribution here is a *precise measurement contract* for routeability, not a new general theorem family.

## Verification

- `tests/test_budget_limited_noise_identifiability.py`: 20 focused tests of exact first/pair moments, error-count matching, policy-value sign reversal, triple-only irrelevance under B=2 and effect under B=3; separately written Fraction full-outcome oracle cross-checks the existing optimizer.
- Local partial research harness: **440 tests passed, zero failures**. This is **not** a complete repository checkout. Full PR-branch GitHub Actions at the new commit is a separate status gate.
- No existing implementation or frozen manuscript was modified.
