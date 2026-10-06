# Aedes opportunity-to-fitness bridge v1

Status: prospective empirical bridge for the opportunity-fitness theory. This document does not license an empirical adaptive-gain claim. It specifies how the missing time-to-performance and performance-to-fitness layers could be measured if the separate Aedes routing/comparator gates are qualified.

## 1. Why Aedes is unusually suitable

The current Aedes programme already supplies candidate state and terminal channels for a routeable four-world decision task. The missing layer is the ecological value of decision time.

Aedes has unusually direct natural-history anchors for that layer:

- host finding and landing can be video-tracked at sub-second to minute scales;
- host-associated cues are integrated sequentially and state-dependently;
- blood feeding itself lasts on the order of minutes rather than hours;
- host defensive behavior can interrupt feeding and produce partial meals;
- blood-meal amount and composition affect egg production and later host seeking;
- the same female can therefore be followed from sensory decision through feeding outcome to a reproductive proxy.

The bridge should exploit these properties rather than assigning an arbitrary lambda to each unit of sensing cost.

## 2. Existing timing anchors

### Host-location timing

Chandel et al. (2024, Nature, DOI 10.1038/s41586-024-07848-5) video-recorded Aedes host-seeking for 300 s and quantified time-resolved host-seeking activity under combinations of human odor, CO2 and thermal infrared.

The associated Dryad archive is public:

DOI 10.5061/dryad.547d7wmh3

and contains 41.70 GB of videos plus source-data mappings. The archive states that videos were recorded at 10 FPS for 300 s and provides code links for tracking.

This dataset can be used as a public-data calibration of the distribution of cue-dependent host-seeking latencies. It is not by itself a fitness or routing receipt.

### Source-location timing

Lacey et al. (2014, Physiological Entomology, DOI 10.1111/phen.12048) reported that more than 70% of Aedes females located either CO2 or human-foot-odor sources within 3 min in a wind tunnel.

Sumner et al. (2022, Journal of Insect Behavior, DOI 10.1007/s10905-022-09812-5) showed that skin-associated acids can drive takeoff, upwind flight and landing, and that added CO2 can reduce takeoff latency.

These studies support treating host-location time as an empirical random variable rather than a nominal cue count.

### Blood-feeding timing

Chadee and Beier (1997, DOI 10.1080/00034983.1997.11813130) measured blood-feeding duration under laboratory and field conditions. Wild Aedes females fed for 107-282 s, with mean 179 s in the reported field sample.

Chadee et al. (2002, PMID 12546453) reported distinct fast and slow blood-feeding phenotypes within a cohort but found similar first-cycle clutch sizes when feeding was allowed to complete. This is important: speed alone need not increase fecundity when the opportunity remains open long enough for both feeding modes to finish.

### Interruption and partial feeding

Klowden and Lea (1978, PMID 686250) reported that blood meals below about 2.5 microliter were associated with continued host seeking, whereas larger meals sharply reduced subsequent host response. The same work linked partial meals and reduced feeding success to host defensive behavior.

Shieh and Rossignol (1992, Parasitology, DOI 10.1017/S0031182000074060) explicitly considered the possibility that faster intake is advantageous when mosquitoes are interrupted before repletion even when the blood source has other nutritional costs.

Recent experimental work on partial blood meals likewise emphasizes that wild mosquitoes often encounter defensive hosts and acquire partial or repeated meals (e.g. PLOS Neglected Tropical Diseases 2023, DOI 10.1371/journal.pntd.0011703).

Together these observations provide a natural-history mechanism for the opportunity variable B: the useful host-feeding opportunity can terminate before a full decision-plus-feeding sequence is complete.

## 3. Separate the three time components

Do not collapse all time into one number.

For each encounter define

\[
T_{\rm total}
=
T_{\rm locate}
+
T_{\rm decide}
+
T_{\rm feed}.
\]

- T_locate: release to arrival at the host-associated target zone;
- T_decide: local cue sampling to the preregistered accept/probe decision;
- T_feed: probing/feeding time to a declared physiological success threshold.

The structural adaptive-gain theory is most directly about T_decide or its acquisition-cost analogue.

Fitness can depend on T_total because host availability may disappear during any stage.

The experiment must therefore record all three when possible. A routeability claim should not be inferred merely because total feeding time differs.

## 4. Define a biologically meaningful completion event

The most defensible host-branch completion event is not "first movement toward the host."

Use a nested endpoint ladder.

### H1 — host-location completion

Female reaches and begins active host-seeking/probing at the target.

Useful for reanalysis of existing video datasets.

### H2 — feeding initiation

Female inserts the proboscis and begins blood uptake.

Closer to resource acquisition, but still not a reproductive success endpoint.

### H3 — physiologically sufficient meal

Female reaches a prospectively defined blood-meal amount sufficient to trigger the focal downstream state.

A starting candidate is the historical approximately 2.5 microliter host-seeking inhibition threshold, but the actual threshold must be revalidated in the experimental strain and apparatus.

### H4 — reproductive payoff

Record:

- blood-meal mass or volume;
- probability of initiating vitellogenesis;
- eggs laid;
- hatch success where feasible.

H4 supplies the value function v or a graded replacement for it.

The paper should distinguish H1/H2 timing effects from H3/H4 fitness consequences.

## 5. Phase A — public-data timing calibration

Before new wet-lab work, use the public Chandel et al. videos/source data to estimate empirical host-seeking completion curves.

For each declared cue condition estimate

\[
\widehat F_j(t)
=
\Pr(T_j\le t),
\]

where T_j is time to a preregistered H1 event.

Priority comparisons:

1. human odor + CO2;
2. human odor + CO2 + IR;
3. time course before, during and after CO2 pulses where IR sustains host-seeking activity.

This phase asks:

- how wide are individual/trial latency distributions?
- is a deterministic C representation remotely adequate?
- at which time scales do cue combinations separate?
- can the empirical distributional overlap formulas be estimated without new model assumptions?

Claim ceiling:

Public-data Phase A can validate the feasibility and scale of the stochastic completion-time framework. It cannot establish the Aedes gonotrophic routing task or fitness selection.

## 6. Phase B — experimentally controlled opportunity windows

Use an artificial feeder or host-mimicking target so that opportunity duration can be randomized without relying on uncontrolled human defensive behavior.

Predeclare a grid of target-availability windows b spanning below and above the natural feeding-time scale. The historical 107-282 s field feeding range is a sensible scale anchor, not a frozen grid.

At each randomized window b:

1. present the declared host-associated cue background;
2. expose the target for exactly b;
3. remove or render the target inaccessible at the deadline;
4. record H1-H4 endpoints.

For architecture/condition j this directly estimates

\[
F_j(b)=\Pr(T_j\le b).
\]

This is preferable to declaring one hard budget after seeing the data.

## 7. Phase C — natural opportunity distribution

Controlled deadlines estimate the performance curve. They do not identify how often each deadline occurs in nature.

Separately estimate or justify

\[
G(b)=\Pr(B\le b),
\]

the distribution of effective host opportunities.

Possible routes, in increasing biological realism:

1. externally programmed feeder withdrawal distribution;
2. standardized mechanical disturbance or target occlusion;
3. experimentally standardized defensive-host behavior where ethically and logistically appropriate;
4. direct field-video estimates of uninterrupted feeding opportunities.

Only levels 3-4 support a strong natural-history claim about wild opportunity distributions.

The controlled levels remain useful for causal tests of the theory.

## 8. Phase D — compose performance and opportunity

Under a justified conditional-independence design,

\[
q_j
=
E_B[F_j(B)].
\]

For architectures i and j,

\[
R_{i:j}
=
vE_B[F_i(B)-F_j(B)].
\]

With baseline fitness w0 and architecture costs kappa,

\[
s_{i:j}
=
\log
\frac{w_0+vq_i}
{w_0+vq_j}
-
(\kappa_i-\kappa_j).
\]

No exponential opportunity model is required.

The empirical curves themselves can be inserted into the theory.

## 9. Critical comparator gate

Do not equate wild-type state-dependent behavior with the theoretical A architecture until the separate comparator-semantics question is closed.

Three possible comparators remain:

- U: one universal fixed acquisition programme;
- A: within-decision contingent routing;
- P: a context-preindexed repertoire selected before the focal decision.

A positive integrated finite-task gap establishes only A versus U structurally.

If gonotrophic state simply pre-indexes distinct host-seeking and oviposition programmes before the focal encounter, P may be the correct biological comparator.

Therefore the timing experiment should be downstream of, or explicitly crossed with, the state-routing experiment.

## 10. Practical first analysis that can be done now

The lowest-risk immediate analysis is public-data Phase A.

Deliverables:

1. identify the Chandel et al. source-data rows and video IDs for the CO2/odor/IR time-course experiment;
2. reconstruct trial-level or frame-level host-seeking time series;
3. define a preregistered H1 completion rule;
4. estimate F_j(t) with uncertainty for each cue condition;
5. report whether cue combinations alter mainly:
   - early-tail probability;
   - median latency;
   - late persistence;
   - or all three;
6. demonstrate the opportunity-overlap calculation across a family of hypothetical G distributions without calling them natural fitness estimates.

This would provide a real-data stress test of the new stochastic theory before any new Aedes experiment.

## 11. Candidate-system comparison

### Aedes aegypti

Strengths:
- strongest mechanistic sensory handles;
- public time-resolved behavior;
- direct feeding-to-fecundity bridge;
- natural interrupted opportunities;
- existing adaptive-gain programme.

Weakness:
- comparator semantics and the integrated gonotrophic router remain unresolved.

Current verdict: best system for mechanistic closure if those gates pass.

### Aphid parasitoid wasps

Strengths:
- host acceptance directly affects offspring production;
- host escape/defense creates explicit opportunity costs;
- handling time and attack rate are classic measurable quantities;
- sequential host assessment is natural.

Weakness:
- mapping exact finite routing architecture and heritable comparator classes is less developed.

Current verdict: strongest reserve system for direct decision-to-fitness coupling.

### Polyphagous herbivores

Strengths:
- sequential-cues hypothesis is already biologically natural;
- host breadth and decision complexity are central.

Weakness:
- direct short-timescale opportunity closure and architecture costs are harder to identify.

Current verdict: strongest conceptual generality, weaker immediate causal closure.

## 12. Decision rule

Do not broaden to another organism merely because it has sequential cues.

Stay with Aedes if public-data Phase A shows a usable time-to-decision distribution and the routing/comparator experiments remain feasible.

Promote a parasitoid system only if Aedes fails the comparator gate or cannot supply a clean decision-time-to-reproductive-payoff link.
