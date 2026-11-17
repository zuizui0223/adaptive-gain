# Stage63 — Noisy conditional sensory routing beyond static flower-vision/odour integration: exact Bayesian predictions and experimental falsification

Date: 2026-11-17 JST. **COMPLETED exact source-free stochastic model, NOT a new empirical pollination result or a new general Bayesian theorem.**

## What Stage63 actually accomplished

Converted the previous \`adaptive-gain\` finite deterministic routeability four-world example into a stochastic Bayesian 4-world decision problem and independently compared it with the **globally Bayes-optimal fixed cue subset** (not a unisensory strawman). Real-source GitHub Actions [run 44018919720](https://github.com/zuizui0223/adaptive-gain/actions/runs/44018919720) **SUCCESS**, seven offline-only tests (including 36 cue-error triples) PASS; original *constructed numerical result* artifact ID **14300086615**, sha256 \`5b4ca8ac3c868beabe1b1bb0831e89f2b986e44306c907c689d22d5fb99cbd48\`.

The prior empirical work is **not** used to calibrate any model parameter. No source wind speed, VOC release, individual bee receptor response, visual contrast, natural reward or pollen deposition is in the solver.

### Model target and honest biological interpretation

Latent world \`(B,T)\` has \`B\` = one of two environmental encounter branches and \`T\` = binary correct action (e.g. flower reward target). Prior four worlds are equiprobable. The early coarse cue R provides a noisy observation of B, but has **zero mutual information with T** at the start; \`P(T=1|R=r)=0.5\` exactly under symmetric errors.

The visual cue V reports T with error \`e_V\` only for B=0 and otherwise produces an independent fair-coin observation; the odour cue O reports T with error \`e_O\` only for B=1 and otherwise produces an independent fair coin. Cue outcomes are conditionally independent given (B,T). The off-branch cue being a fair coin is an explicit strong *hypothesis*—real flowers' scent and visibility can be simultaneously informative and/or correlated.

Each cue has a positive abstract acquisition cost \`c_R,c_V,c_O\`; a wrong T decision incurs loss 1. A policy can inspect any subset of three cues at most once, stop anytime, and make a posterior-optimal decision. A cue is not literally priced by a flower; time, risk and energy would need independent calibration.

**Fixed/noncontingent comparison:** choose *any of the eight possible fixed cue sets* before observing the results, pay all costs, then use the joint posterior-optimal target classifier. Stronger than unimodal baseline. \`R\` alone is uninformative about T but can inform how V/O outcomes should be interpreted in a fixed bundle.

**Adaptive policy:** after each chosen cue observation, select stop or next cue based on current posterior. Exact rational Bellman recursion:

\`\`\`text
L(P,unused) = min(
  min{P(T=0),P(T=1)},
  min_q [c_q + sum_y P(y|P,q) L(P(.|y,q), unused\{q})]
)
L_F = min_{S subset {R,V,O}} sum_{q in S} c_q
      + sum_{y_S} P(y_S) min_t P(T != t | y_S)
L_A <= L_F
\`\`\`

This is standard Bayesian sequential decision theory, not new general mathematical work. A prediction that an animal implements this particular policy requires direct animal cue-choice data.

## Exact source-free example and information-access phase change

All scenarios use \`c_R=0.05,c_V=0.10,c_O=0.10\` (units of wrong-target loss 1); all cue error probabilities are **assumed**, never fitted from published bees, wind speeds, scent VOCs or flower UV spectra.

| Assumed state (eR,eV,eO) | Exact adaptive Bayes risk | Exact best fixed Bayes risk | Gain: fixed−adaptive | Adaptive first action |
|---|---:|---:|---:|---|
| Ideal router, both terminals 5% errors (0,.05,.05) | **0.2000** (1/5) | 0.3000 (3/10) | **0.1000** (1/10) | R, then V if R=0 / O if R=1 |
| 15% router error, 5% terminals (.15,.05,.05) | **0.2675** (107/400) | 0.3675 (147/400) | **0.1000** | R, then V or O |
| Router uninformative (.50,.05,.05) | 0.375 (3/8) | 0.375 (3/8) | **0** | V or O |
| Odour noisy while vision accurate (.05,.05,.40) | 0.375 (3/8) | 0.375 (3/8) | **0** | V only |
| Vision noisy while odour accurate (.05,.35,.05) | 0.365 (73/200) | 0.375 (3/8) | 0.010 | R first |
| Both terminal modalities poor (.05,.30,.40) | 0.500 (1/2) | 0.500 (1/2) | **0** | Stop or optional tie |

**The branch cue R alone carries no information about the reward T, but can have a substantial *instrumental* decision value because it tells the receiver which terminal channel to acquire.** This is the existing routeability idea extended to a noisy illustrative decision setting. The advantage is not an intrinsic property of pigments/VOCs: it depends on cue reliabilities, availability, costs and the receiver's task. An unreliable router or poor branch-specific cue collapses the advantage. Uninformative routing is not equivalent to sensory weakness that a static backup already solves.

**No empirical wind effect was estimated.** In particular, choosing an illustrative \`e_O=.40\` does not mean any genuine speed of wind raises odour error to 40%, nor that any natural Bombus has that sensory reliability. Crall's all-scented orchid-bee bait arrivals and Chang's Bombus wind-landing motor speeds cannot be multiplied together or used to fit these cue errors.

## How this compares with real prior art (novelty firewall)

- Lawson, Whitney & Rands (2017), DOI 10.1098/rsos.170996, originally tested scent/visual **backup** under wind noise. Stage61/62 source reanalyses recover 72 original bees; only colony F shared across A/B/C, with reward-scent and colony imbalance. Original observations lack explicitly recorded *next cue chosen after a target-uninformative first cue*. The sensory backup effect is already published.
- Graver et al. (2026), DOI 10.1242/jeb.251126: *Bombus impatiens* reweights color and odor according to spatiotemporal timing/scale (direct existing prior art; NOT new in this work).
- 2026 \`Bees flexibly adjust decision strategies to information content in a foraging task\` (PMCID PMC12935042): *B. terrestris* changes visual-pattern/shape learning based on color discriminability. Thus context-dependent resource allocation and sensory weighting are **already experimental findings**.
- 2013 \`Seeing is believing: information content and behavioural response to visual and chemical cues\` (PMCID PMC3774238): prior Bayesian-like flower inspection model, showing decision-time/information trade-offs. We cannot claim Bayesian cue use is novel.
- A 2018 \`prevalence of olfactory- versus visual-signal encounter by searching bumblebees\` study (PMCID PMC6167322) modeled floral odour plume and flower visual encounter; odor discovery physics and signal access are prior art, not newly invented here.
- The source-original 305 VOC taxa and 817 visual-source taxa intersect on only **14** strict accepted source names after excluding named hybrid \`Victoria amazonica × cruziana\`; exactly **one** has original spatial UV-pattern state plus VOC evidence, and still not the same population. Another independent original FCP photo source yields **80** VOC taxonomy/photo opportunity matches, **55** with >=40 source-coarse-colour-classifiable photos, but not confirmed visible nectar guides.

**Proposed genuinely testable additional contrast:** a first sensory/environmental cue with no direct reward information nonetheless changes *which later cue* an animal actively chooses, and the observed branch-specific policy reduces error/time beyond the optimal static Bayes cue bundle at matched measured cue reliability, reward distribution and sensory costs. This is not proof of ecological novelty until measured and contrasted against 2013/2017/2026 prior work.

## Experimental core designed to identify the biological process

A feasible prospective experiment must deliberately separate *where to search next* from *which flower has reward*:

1. Randomly assign a **coarse branch** B∈{0,1} such that rewarded-left/right probability remains exactly 50% under each branch and coarse cue: \`P(T|B)=P(T)\`; pre-register exact per-colony balancing and blinded scorer. Validate empirically that the first cue alone cannot predict T. Cue identity and presentation order/latency randomized and side counterbalanced.
2. In B=0, subsequent source visual/UV-pattern cue V is diagnostic of T and odour O is matched noninformative; reverse relevance in B=1. Equalize display, flower shape/size, true VOC flux/receptor detectability and reward across conditions. **This is a constructed hypothesis for an animal assay**, not a claim that normal flowers have this informational structure.
3. Record **actual sequence** of perception/request (e.g. which cue station visited/inspected next), response time and reward-side decision. Compare target error + independently measured cue-acquisition effort/time against the **best precommitted static cue set** and backup-only cue switching, with observer-blind trials. Critically, a static policy can use both cue outcomes jointly; do not equate fixed with uninformed.
4. Manipulate an instrumented crosswind/turbulence/plume and flower-sway regime independently of the branch and late cue; manipulate/record irradiance and background. Do not fit cue error rates from velocity alone: estimate each cue's actual empirical confusion matrix \`P(y|B,T,W,receiver)\`, and use these measured likelihoods to predict held-out behavior.
5. Use replicated colonies, independent bee IDs and trials; use held-out **colonies** to compare predictive likelihood of contingent policy vs fixed/multisensory/backup baseline, and only later add actual legitimate pollen deposition, outcross/seed set on the same flowers. Do not infer pollen from color choices or successful landing alone.

**Macro extension remains contingent:** first show individual-level conditional routeability and its wind/light modifiers; only then test if repeated trait modules (spatial visible/UV guide, time-varying flower color, VOC composition) covary with independently modeled locally realized guild pools beyond native geography, climate, UV-B, phylogeny, floral source-study sampling and separate plant fitness. The cross-source 1,090 accepted-name *union* cannot establish coevolution or an ecological SEM.

## Reproducibility

\`research/floral_routeability_stage63/noisy_bayesian_conditional_routeability.py\`, unit tests and \`.github/workflows/floral-stage63-noisy-Bayes-sensory-routeability.yml\`. Exact finite rational posterior/DP and eight global fixed cue sets; source [Actions 44018919720](https://github.com/zuizui0223/adaptive-gain/actions/runs/44018919720) SUCCESS. All numerical results are constructed examples; no empirical UV×Bombus×wind×VOC coefficient or evolutionary fitness effect estimated. PR remains Draft and \`main\` untouched.
