# Stage17: optional information first request — source-free six-arm experiment design

**2026-11-11 | SYNTHETIC-ONLY design validation. ZERO animals tested or assigned.** This is a **new independent research extension** stacked on Stage16 PR #94. Its content is an experimental proposal, not an empirical biological result; historical Stage9b–13 source outcomes, Stage15 PR #93, Stage16 PR #94, manuscripts V5/V6 and main are untouched.

## Scientific target

Stage16 established that an animal can rationally **stop acquiring information** when the cost is too high, but ONLY if it is allowed to decline the FIRST request. Stage15 required a first U/V request and was therefore a different decision problem. Stage17 introduces explicit recorded animal-origin **SKIP/U/V** actions in BOTH contingent and precommit arms, and a three-tier physical waiting-time treatment. The hypothesis is a **middle-vs-extremes shape contrast of access-mode effects**; the future animal study is not expected to achieve the normative theoretical 1/6 by default.

**Design simplification:** No wind treatment in Stage17. Wind×information routing can be tested later if a real access effect exists. Using six arms rather than 12 preserves more independent-colony observations per mechanism contrast.

## Exactly what the new synthetic source-contract code checks

- Fake assignment: **24 entirely invented original colonies ×12 invented bee IDs ×48 mock trials =13,824** public-seed QA records. Six cost×mode combinations each have **2,304** fake trials. Three cost blocks of 16 each per bee, mode 8+8 within every block, physical 0-target side balanced 4+4 within each mode, all six cost sequences equally distributed across each 12-bee fake colony. R/U/V source worlds sampled independently with replacement on EVERY original trial; neither the root bit nor remaining possibilities become predictable through finite-deck depletion.
- A recorded animal-origin binding **SKIP/U/V before R** in precommit versus **after R** in contingent. Both arms include a source-verified neutral motor act on the opposite side of root. Actual root presentation/source bit, optional first and second original physical U/V reveal events, known original source bit values, measured per-leaf waiting time, no predictive cue leaking at feeders, two physically accessible target options, calibrated blank-corrected intake and a fixed root-anchored 30 s period are required.
- The source gate treats SKIP with **zero physical leaf events** as a valid completed action, not missing response. It rejects a controller-commanded query attributed to a bee, action after/before the wrong root time, mismatched source U/V value, a second display without an actual request, missing or delayed source telemetry and a fake no-intake zero. High/medium/low delay windows are **fictional code fixtures** (.2/1/3 seconds in the synthetic generator), NOT an independently calibrated animal experiment.
- The full fake source example includes **4,608 explicitly assigned SKIP trials** and **11,436 artificial leaf-reveal events**. These are **13,824 mock trial records** nested within 288 invented bee identities and 24 invented colonies, not independent biological replicates. The fake source policy was deliberately injected to SKIP in all high-cost cases, request in all low and medium cases. It is NOT evidence that real bees would do so.

## Pre-fixed future experimental primary (needs independent pilot)

Original future observational unit is one independently recruited colony; equally average real 8-trial mode×cost means within each real bee and then bees within colony. Let D_t=mean true intake(contingent,t)−mean true intake(precommit,t), for t∈{low,medium,high}. The **only primary future endpoint** is the *shape contrast*:

[
K = D_{medium} - rac{D_{low}+D_{high}}{2}.
]

Future actual sucrose in mg is measured within an identical 30-second interval anchored to the first root display. K has **units mg/30s** and does not estimate normalized theoretical c, physical metabolic cost or a continuous second derivative. If K>0 by an independently recruited colony-level two-sided t test and CI, it means the relative access advantage is larger at the middle of these *three chosen tiers*, **not automatically a net beneficial adaptive mechanism**: an additional D_medium>0 and genuine cue request/skip response would be needed to tell that biological story. If fewer than 12 source colonies, descriptive pilot only; never count repeated trial rows as independent colonies.

Locked diagnostics are per-tier actual SKIP probability, first and second paid physical requests, first leaf relevance conditional on observed root, final target choice success/no choice, and real calibrated intake including verified zeros and actual sensor failure flags. All outcomes and sample exclusions must be frozen independently before pilot result unblinding. The two extreme tiers must be piloted and tested by the apparatus even if all animals decline their requests; behavior alone cannot certify high-tier delay calibration.

## Actual synthetic numerical receipt

[Dedicated synthetic original-code QA run #42959593839](https://github.com/zuizui0223/adaptive-gain/actions/runs/42959593839) **SUCCESS**: 15 focused tests, original-code source chronology and cost-delay validation, exact six-arm synthetic assignment check and fake colony-equal estimator. The test-first RED run #42959088194 failed because source modules did not yet exist; the following run exposed a source error-report ordering issue, corrected without changing the underlying acceptance rules.

The mock consumption generator **intentionally adds +2 mg ONLY to contingent/middle-tier outcomes**, with small arbitrary noise and colony heterogeneity. The resulting synthetically recovered K is **+1.996554772 mg/30s**, a trivial software-recovery check, not an unexpected discovery and not a real effect size. The fake source generation chooses zero leaf requests in high-tier trials. Source mean requests across both modes are low 1.24110243, medium 1.24066840, high 0; these are imposed mock strategies, not actual biological policies.

## Pilot feasibility no-go / boundaries

Real experimental execution requires ethical review, independent origin of bee/colony IDs, actual cue learning and confusion-matrix calibration, animal ability to use all three physical **SKIP/U/V** options, pilot-locked delay ranges and their non-overlap, timing alignment of pre-root and post-root motor controls, no target cue leakage, complete source video/feeder/wind control, real measured intake with blank corrections, concealed randomization and cohort-level replication. Real delay is *opportunity time*, not a known Stage16 utility cost c; the Stage16 one-sixth optimal normalized reward difference is not expected measured sucrose. Different commitment/anticipation remains an unavoidable confound despite motor matching.

No animal testing, publication submission, ethical authorization, real cost estimates or main-branch merge is represented by these source-free methods.

## Closely related September 2026 prior art (source-only external feasibility)

The bioRxiv preprint He et al. (2026), *Uncertainty-Guided Decision-Making in Bumble Bees*, DOI https://doi.org/10.64898/2026.09.15.751944, already reports source-labeled voluntary information-platform visits and reward-costly uncertainty-guided information seeking in bumblebees. It is a preprint; independent peer-reviewed confirmation must not be assumed. The authors' public repo `Cuixiaojian21/bee_metacognition` (original source commit `7f886394b4de872ecdb19ca4ea214ec321d5dce9`) contains 192 bees × 100 source behavioral trials with an explicit real platform landing indicator. See [source-only scope ledger](EXTERNAL_REAL_BEE_INFO_REQUEST_SOURCE_AUDIT_20261111.md).

This source supports the **feasibility** of a bee voluntarily requesting one given answer, not Stage17's **selection between two different U/V information sources conditioned on a previously observed R**. Consequently generic opt-out, a paid information platform, and the simple existence of active information seeking **are not claimed as novel discoveries of this project**. The remaining possible conceptual novelty is randomized outcome-contingent *choice of information source* versus an original precommitment, with actually measured cost, available alternatives and reward consequences. Neither the preprint nor Stage17 currently demonstrates such a causal effect.
