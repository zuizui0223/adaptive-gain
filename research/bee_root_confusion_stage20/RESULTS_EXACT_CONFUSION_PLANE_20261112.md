# Stage20 Results — two-class recognition errors change the value of contingent querying

**2026-11-12 | Exact mathematics, NOT an observed bee threshold.**

Same Stage19 toy game with q=.2 and normalized paid leaf query cost c=.25, but different root label error rates for each actual root class. An exact Fraction-valued Bayes optimizer and a fully separate normalized-posterior implementation agree on 192 parameter settings, including conditional optional second leaf requests. The exact result for 50–100% correct recognition of each root class is:

    Delta = max(0, (11*s0+5*s1−11)/40).

Thus **11*s0+5*s1>11**, NOT a simple average-accuracy cutoff, is the necessary-and-sufficient condition for positive optimal access benefit in this restricted model. It recovers the 68.75% threshold only on the diagonal s0=s1.

| True R0 correctly read (s0) | True R1 correctly read (s1) | Balanced accuracy | Optimal contingent advantage |
|---:|---:|---:|---:|
| 80% | 60% | 70% | **+.020** |
| 60% | 80% | 70% | **0** |
| 90% | 70% | 80% | **+.060** |
| 70% | 90% | 80% | **+.030** |

The R0 recognition error has the larger weight (11/40 vs 5/40, 2.2×) **inside the positive region only**. With s0=.6, s1 must be strictly above .88, whereas with s0=.8, every allowed s1≥.5 is already sufficient. A fixed s=1 action rule can be harmful if uncalibrated: at (s0,s1)=(.6,.8), fixed SKIP/V has −.010 versus optimal precommit, while fully rational contingent action chooses no paid cue and yields Delta=0.

## Nonlinear individual versus aggregate gain

Two fake source bees with (.9,.9) and (.5,.5) individually have idealized advantages .085 and 0. Equal-colony mean is .0425, while applying the theorem just to the mean class confusion (.7,.7) yields .005. The positive-part gain is convex; pooled calculations and a per-colony mean of gains do not commute. This illustration is NOT a measured colony effect and does not authorize population significance or claim a universally fixed direction with uneven sample weighting.

## Pilot readiness and original-source limitations

The mock root classification source contract passed 40 invented video-verified entries across two fake original colonies. It ensures independent R-only categorization and full R0/R1 counts before reward feedback. **The actual number of observed bee trials is ZERO.** A real source will require per-original-colony and per-animal confusion matrices including errors in both directions, uncertainty bounds, verified knowledge of target priors, U/V readout, paid requests and reward mapping. Individual pooled accuracy alone is not an adequate proxy.

## Verification / no-go

[Stage20 GitHub Actions #43125720023](https://github.com/zuizui0223/adaptive-gain/actions/runs/43125720023) SUCCESS: 14 test cases (9 mathematical +5 root-pilot source QA), 192 independent normalized-posterior oracle comparisons, 121 exact source-free confusion settings; mock input alone. Earlier missing-module/red tests are part of test-first development, not an observed outcome. The full Python3.10–3.12 repository matrix is a separate test gate and must be checked for this document head before promotion.

The theory may motivate an independent animal pilot, but this branch does not submit an ethics application, recruit animals, select a real trial sample size, alter the parent Stage19 manuscript, or merge into main.