# Stage9b original-source result: transferred direction survives first-order route-history control

**29 October 2026 | SOURCE-VERIFIED POST-HOC ROBUSTNESS RESULT, NOT A NEW RANDOMIZED EXPERIMENT**

## Finding

An *externally frozen* dimensionless incoming-chord turning factor (κ=1.0, previously trained on Pasquaretta et al. 2019) retains heldout predictive information beyond **both** the true 2017 Klein et al. physical flower geometry and **each bee's own early-bout first-order B→C route frequencies**, with frozen β=5. The direction-over-history contrast is **positive in all 3 arrangements and both source colonies per arrangement (6/6 source colony×array cells)**.

**This strengthens the bounded predictive claim in PR #84; it does not show measured flight inertia, knowledge acquisition order, ecological cue-processing, wind-dependent movement, memory causality, interspecific signaling, energy gain or fitness.** The experimental source has only two independent colonies and presents the arrays to the same bees in a fixed 1→2→3 order. This test was designed AFTER earlier positive Stage9 outcomes, and thus is explicitly *post-hoc*.

## Original study / reproducibility receipt

- Original study: Klein et al. 2017, *Scientific Reports* 7:4561, DOI https://doi.org/10.1038/s41598-017-04919-8.
- Real publisher S1 CSV SHA256: `e1b660125c389fc873a70eaf0edaaec053637cc814d8bcb50f1a61a01b7e3e04`.
- Real publisher S2 CSV SHA256: `68e663f50d7d741c3a162f67b03db89499aff4c328aecf09361cf15955440535`.
- Original published Figure1 JPEG SHA256: `4277dcc8ec52598037a7a4fd6d6bc47d4877a68593a400723508a2d7c0cd40ac`; plotted positions **manually digitized ±10cm**, not independently surveyed flower coordinates.
- Original **1,740 bouts; 1,720 nest-boundary-valid**, 16 incompletely bounded and 4 internally-nested removed from source route triplets only.
- **29 original tagged bees, 2 colonies, all three source arrangements, 1,958 genuine test triplets** A→B→C with A≠B and B≠C; first original bouts1–15 for all training, final bouts16–20 held out.
- **All 25 focused synthetic/source code tests passed**, publisher hash checks passed, entire parent Stage9 Mgeo/Mturn **reproduced numerically for each bee to 1e-9** before the new result was accepted.
- [Exact original-source read-only CI run #40862355605](https://github.com/zuizui0223/adaptive-gain/actions/runs/40862355605) **SUCCESS**, including original source retrieval, original Figure1, original Stage9 replication and new Stage9b scores. [PR #87](https://github.com/zuizui0223/adaptive-gain/pull/87) (draft, stacked on PR #84).

## Identical-outcome four-model comparison

Mean heldout NLL in **nats per next-different-flower triplet**, equal weight **over 29 original individuals per arrangement** (smaller is better). All four models predicted EXACTLY the same authentic next destinations.

| Arrangement | Source triplets | Mgeo | Mhistory | Mturn | Mhistory+turn | **Direction gain beyond history** | Bees improving |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 608 | 1.007672 | 0.924819 | 0.848069 | **0.813765** | **+0.111053** | 22/29 |
| 2 | 687 | 1.072200 | 0.993252 | 1.008720 | **0.960350** | **+0.032902** | 18/29 |
| 3 | 663 | 1.029743 | 0.908745 | 0.941989 | **0.884841** | **+0.023904** | 19/29 |

`Mhistory` = [N_train(B,C)+5×Mgeo(C|B)] / [sum_(D≠B)N_train(B,D)+5], where β=5 is taken **as is** from the independent 2019 source setup, not re-estimated from 2017 test data. `Mturn` and `Mhistory+turn` each multiply the respective baseline probability by exp(1.0×cosθ(A,B,C)) and renormalize over the same 3 actual alternative flowers.

The history term also improves `Mturn` when appended (bee-equal gains arrangement1 **+0.034304**, arrangement2 **+0.048370**, arrangement3 **+0.057147**). The history+turn combination therefore has the **lowest heldout NLL in all three layouts**. These gains do not algebraically decompose into independent causal mechanisms; multiplying and renormalizing predictors makes their increments depend on baseline model.

## Two real source colonies and within-source conditional null

The parent within-bee×current-flower B×array permutation rule is held fixed (199 seed=20261029 permutations). It preserves all genuine B,C outcomes and train-only fitted counts, reassigning just actual incoming A within eligible bee/B/array cells.

| Array | Source colony jimmy: gain beyond history | Source colony tristan | Actual minus source-shuffle mean (colony-equal) | Exploratory conditional p |
|---|---:|---:|---:|---:|
| 1 | +0.108616 | +0.113328 | +0.131994 | 0.005 |
| 2 | +0.021037 | +0.043976 | +0.073909 | 0.005 |
| 3 | +0.034751 | +0.013781 | +0.079891 | 0.005 |

Each original conditional Monte Carlo p is 0.005 (minimum of 1/200), **NOT 200 independent bee experiments**. Repeated individuals across arrays, two colonies, and post-hoc choice of this challenger mean p-values must not be sold as population-level confirmatory significance. No wind randomized; no true physical flight heading observed.

## Inference and stop rules

**Defensible:** A fixed geometric incoming-order feature adds transferable prediction of the next distinct floral target beyond trained individual first-order flower-transition counts, on the single independent 2017 experiment evaluated here. Direction and history supply complementary **predictive** structure for these observed routes; both survive as incremental terms in three tested layouts.

**Not established:** that bees consciously use incoming direction, that cognition remembers this context, that previous sensory cue *acquisition* affects outcome, that any information-tree adaptive advantage `C_A<C_F` occurs in nature, that wind causally changes those behaviors, or that bees from distinct species interact hierarchically.

**Next substantive gate:** independently sampled colonies with direct actual time-stamped 3D flight headings; randomized flower geometry/visibility and wind/cue order; and measured rewards/handling. The existing Stage9 prospective cue-order×wind protocol in PR #85 is only a *design*, not animal data. Do not tune any comparator or retrospective subgroup in the current 2017 records to seek larger significance.

**Freeze this result** rather than generating alternative β grids, array order adjustments, responder subsets or null-unit choices. Model-level Python code and reproducible real-original-data GitHub Actions, not copyrighted original individual trajectories, are committed.
