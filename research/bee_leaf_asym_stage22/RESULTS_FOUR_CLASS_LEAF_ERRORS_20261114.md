# Stage22: the direction of paid-leaf recognition errors matters

**14 November 2026 | EXACT MATHEMATICAL RESULT, MOCK SOURCE QA ONLY. No original live-animal data in this Stage22 study.**

The prior Stage21 theorem assumed that a paid V cue had one symmetric error rate: P(report0|true0)=P(report1|true1). Stage22 removes that assumption and uses the full source confusion matrix separately for U and V, while keeping Stage20's two-class root-cue recognition.

## Fixed finite decision world

Original hidden binary world R~Bern(.5), U~Bern(q), V~Bern(.5), mutually independent, with an IID fresh hidden world for every trial (sampling WITH replacement). The true correct target is U if R=0 and V if R=1. The root cue Z has independent class-conditional errors s0=P(Z0|R0), s1=P(Z1|R1), and both experimental access modes receive Z. Once voluntarily requested, each U/V cue produces a potentially incorrect observation and can be purchased at most once; an optional second distinct source remains available.

Four paid cue recognition probabilities are:

- aU0=P(report0|true U0), aU1=P(report1|true U1).
- aV0=P(report0|true V0), aV1=P(report1|true V1).

All six class-conditional recognition rates lie in [.5,1] in this theorem. Correct final target gives one normalized reward, wrong gives zero; each actually purchased cue costs c normalized reward units. The contingent agent chooses initial SKIP/U/V **after** Z; precommitted chooses initial SKIP/U/V **before** Z but can conditionally buy a second cue. This is a hypothetical Bayesian decision system, NOT measured bee behavior or real metabolic fitness.

## Exact sharp result for q=1/5 and c=1/4

Across all s0,s1,aU0,aU1,aV0,aV1∈[.5,1], the exact Fraction-valued eight-world dynamic optimization finds:

\[
\boxed{\Delta=\max\!\left[0,\quad
\frac{s_1}{4}\left(a_{V0}+a_{V1}-\frac32\right)
+(1-s_0)\left(\frac3{20}a_{V0}-\frac3{20}a_{V1}-\frac{11}{40}\right)\right].}
\]

The best precommitted first action is SKIP, with value 13/20=.65. Contingent access after observed Z0 also SKIPs; after observed Z1 it buys V if and only if the expression inside the max is positive. In this restricted q=.2,c=.25 game, **neither aU0 nor aU1 changes the optimal access-value contrast**, because U is too low-value to justify the .25 charge. This is **not** a general conclusion about U or any particular pollinator sense: it may fail with different q, costs or task topology.

One way to see the formula is that the net gain from revealing V after observed Z1, relative to retaining the unqueried target0 prediction, is the excess expected correct-choice probability after a possible V=1 readout minus c times the probability of observing Z1. The Vobs=0 readout does not reverse the target0 choice within the stated domain. Exact dynamic programming independently evaluates every choice of initial SKIP/U/V and optional second leaf for all eight worlds, verifying that no alternative policy is more valuable in this domain.

Setting aV0=aV1=aV exactly reduces to the prior Stage21 formula:

\[
\Delta=\max(0,[s_1(a_V-\tfrac34)-\tfrac{11}{20}(1-s_0)]/2).
\]

## Counterexample: equally accurate V channels have unequal decision value

For s0=.8 and s1=.6, the theorem simplifies to

\[
\boxed{\Delta=\max(0,\ 0.18a_{V0}+0.12a_{V1}-0.28).}
\]

| V0 correctly recognized | V1 correctly recognized | Balanced V hit rate | Theoretical access benefit |
|---:|---:|---:|---:|
| 100% | 90% | **95%** | **+0.008** |
| 90% | 100% | **95%** | **+0.002** |
| 90% | 90% | 90% | 0 |
| 100% | 100% | 100% | +0.020 |

Therefore, at fixed priors/costs/root reliability, V0-specificity has greater marginal value than V1-sensitivity in the *positive-benefit* region: coefficients .18 and .12. Their ratio is 1.5. The exact result answers a more nuanced question than whether a cue is “95% accurate.” The source's error direction matters. The 4-fold difference +.008 vs +.002 is a math construction, **not** a fourfold change in actual bee reward or reproductive fitness.

## Verified source-free implementation

- **[Stage22 original mathematical and mock source CI #43458226946](https://github.com/zuizui0223/adaptive-gain/actions/runs/43458226946): SUCCESS, 14 focused tests.**
- Production \`leaf_bit_confusion.py\` uses exact Fraction joint-probability dynamic programming. Independently written \`test_leaf_bit_confusion.py\` uses normalized posterior choice optimization for q∈{0,.2,.5}, c∈{0,.1,.25,.4}, four root-confusion pairs and five paid-leaf channel profiles (**240 independently checked parameter combinations**). Further tests check the sharp formula and reduction to Stage21, payoff/action invariances and equal-average counterexamples. A separate mathematical grid has 108 specified source-free channel configurations.
- Initial dedicated run #43457768715 failed only because the required grid contained 72 rather than >=100 configurations; repaired to 108 without changing the theorem or outcomes. A test-first mock-pilot RED run then preceded the final GREEN run #43458226946.
- A *synthetic-only* U/V recognition pilot records 80 imagined classification rows across two fictional colony/bee identities, 10 true0 and 10 true1 per U/V source for each. Root, other leaf and reward-location cues are hidden; response precedes correctness feedback; original ID and timestamp checks are fail-closed. Mock class rates pool to U0=.85,U1=.75,V0=.95,V1=.95. The two fabricated colony-level theory gains are .008 and .002. This verifies correct **source grain** and never estimates an actual biological sensory rate.
- The real source data from He et al. (2026) were NOT reanalyzed in Stage22. Earlier published uncertainty-related information seeking remains prior art, not a new discovery here.

## Conditions needed for prospective empirical identification

An independent approved animal pilot must estimate the FULL confusion matrix for each source channel from *separately blinded true0/true1 presentations*, per bee and original independent colony, without simplifying observed class biases into one accuracy. True U=1 is naturally rare under the intended q=.2 task, so learning success must be measured separately from an uninformative always-0 response. Root confusion s0/s1, the animal's learned asymmetric branch priors, actual source-initiated SKIP/U/V and second requests, video timing, source feeder mapping, actual paid delay and blank-corrected reward require separate, source-authenticated observation.

Real finite-pilot estimated class rates should NOT be forced to match; record uncertainty instead. The exact inequality above is a **hypothetical utility model under perfectly known priors, class errors and c**, not proof that a real animal has those calibrated abilities. If class-specific recognition falls outside the [.5,1] label-orientation assumption or costs depend on source, a newly frozen model is necessary.

**STOP:** no real bee observations, consent/animal ethics approval, independent pilot variance, field sampling, calibrated sucrose intake, individual source queries, population p-value or evolutionary fitness outcome is part of this PR. Do not merge theoretical results into frozen empirical Stage9b–13 or earlier Stage14–21 claims.
