# Bumblebee public-data routeability bridge v1

Date: 2026-10-02

Status: prospective public-data analysis plan. This document defines the
strongest bumblebee analyses that can be run without relabeling ordinary
multicue effects as direct validation of the deterministic routeability theorem.

## Decision

The public-data landscape is no longer adequately described as simply
"no public validation data".

A more accurate three-level assessment is:

1. **Exact theorem validation:** not yet located in one public dataset.
2. **Strong empirical bridge:** yes — Spaethe et al. (2026) plus Eckel et al.
   (2025) jointly test two core operational ingredients of routeability.
3. **Direct biological precedent for branch-specific cue relevance:** yes —
   Essenberg et al. (2015), although a reusable raw dataset for that exact
   experiment has not been located.

The theory paper may therefore include a small public-data concordance section
or supplementary panel, provided it is explicitly labelled an **empirical
bridge** rather than a measurement of \(C_A<C_F\).

---

## 1. The exact validation target

For a direct empirical test of the current deterministic theorem, one dataset
would ideally expose:

- one common physical cue environment;
- a focal target/action map;
- at least one early observation with multiple realized outcomes;
- different later cues becoming relevant after different early outcomes;
- measurable cue-acquisition cost or delay;
- an adaptive route and a fixed-bundle comparison;
- a finite common budget;
- trial- or trajectory-level raw data.

The discriminating object is not merely cue weighting. It is:

\[
q_0=a \Longrightarrow q_i \text{ is the useful continuation},
\qquad
q_0=b \Longrightarrow q_j \text{ is the useful continuation}.
\]

No single public bumblebee dataset located so far exposes all of these fields.

---

## 2. Public-data bridge A — Spaethe et al. 2026

Paper:
**Bees flexibly adjust decision strategies to information content in a
foraging task**, *Science Advances* 12:e adw9320,
DOI 10.1126/sciadv.adw9320.

Species: *Bombus terrestris*.

Public assets:
- source data: Figshare share `c4c912de7dd7e24a9ec8`;
- analysis repository:
  `stoeckl-lab/Spaethe_et_al_2024_beeDecisions`;
- archived code: Zenodo DOI 10.5281/zenodo.15911965.

### Biological structure

Flowers carry two visual attributes:
- colour;
- pattern or shape.

Colour discriminability is manipulated:
- **distant/easy** colour pairs;
- **close/hard** colour pairs.

The paper reports that bees rely almost exclusively on colour when colour is
easy to discriminate and fail to learn the secondary pattern/shape attribute.
When colour is difficult to discriminate, they learn both attributes.

This is the closest public dataset currently located to the routeability
prediction that organisms should avoid provisioning information that is not
needed for the focal decision.

### Prospective primary quantity

For each individual in the cue-conflict test define the
**secondary-cue recruitment index**

\[
R=1-p_{\rm primary},
\]

where \(p_{\rm primary}\) is the fraction of conflict-test choices following
the trained colour rather than the trained pattern/shape.

Primary contrast:

\[
\Delta_R
=
E[R\mid \text{close/hard colour}]
-
E[R\mid \text{distant/easy colour}].
\]

Registered direction:

\[
\boxed{\Delta_R>0.}
\]

Interpretation:
when the primary cue is insufficiently discriminable, a larger fraction of
decisions recruits the secondary cue.

### Confirmatory analyses

Analyse pattern and shape experiments separately.

Primary tests:
- one-sided rank/permutation comparison of \(R\) between close and distant
  colour conditions;
- report raw mean/median difference and a bootstrap confidence interval.

Secondary, stronger endpoint if Figshare trial data can be retrieved:
- post-training performance on the secondary attribute alone;
- test whether secondary-attribute learning is above chance for close colours
  but not for distant colours.

### Claim ceiling

Spaethe et al. do **not** provide a within-visit routing event in which one
realized cue outcome selects which later cue to inspect. The authors explicitly
describe the strategy as stable across visits within a sensory context.

Therefore this dataset tests:

> **conditional provisioning of cue sets according to decision difficulty**

and not:

> exact branchwise routeability or \(C_A<C_F\).

---

## 3. Public-data bridge B — Eckel et al. 2025

Paper:
**Visual place learning by walking bumblebees in virtual reality**,
*Journal of Experimental Biology* 228:jeb250485,
DOI 10.1242/jeb.250485.

Species: *Bombus terrestris*.

Public dataset:
Bielefeld University DOI **10.4119/unibi/3004993**.

The paper states that all relevant data and analysis scripts are publicly
available.

### Why this dataset adds something Spaethe cannot

The closed-loop VR system records the bee's movement through cue space.
Therefore information acquisition has an observable physical cost:

- elapsed time;
- path length;
- distance to diagnostic cue constellations;
- number of inspected regions/objects;
- commitment before versus after entering a diagnostic-cue neighbourhood.

The experiments also include **reversal learning**, changing reward/punishment
associations while preserving the visual scene. That provides a relational
action-map manipulation much closer to the theory's claim that the same
physical environment can support different decision structures.

### Prospective quantities

If the public files expose the timestamped camera/trajectory coordinates
described in the paper, compute for each trial:

\[
\tau_{\rm decision}=t_{\rm target}-t_0,
\]

\[
L_{\rm path}=\sum_t \|x_{t+1}-x_t\|,
\]

and, for each diagnostic cue set \(j\),

\[
d^{\min}_j=\min_t d(x_t,Q_j).
\]

Define an **acquisition-depth proxy** as the number of diagnostic cue
neighbourhoods entered before target commitment.

### Registered tests

1. Cue-proximity test:
   decisions requiring near/local visual information should incur greater
   approach depth than decisions resolvable from more distal information.

2. Reversal test:
   with the physical scene unchanged, changing reward valence should alter
   target-directed trajectories/commitment.

3. Cost–accuracy relation:
   greater diagnostic-cue approach should predict correct target choice when
   that cue is required.

### Claim ceiling

Trajectory cost is not identical to the model's abstract cue cost, and head/gaze
direction was not recorded. The analysis therefore supports **sequential
accessibility cost** and **action-map relativity**, not exact \(C_A\) or \(C_F\).

---

## 4. Closest biological routeability precedent — Essenberg et al. 2015

Paper:
**The value of information in floral cues: bumblebee learning of floral size
cues**, *Behavioral Ecology* 26:1335–1344,
DOI 10.1093/beheco/arv061.

Species: *Bombus impatiens*.

The same array contains two flower types, identifiable by colour and scent.

- Informative branch:
  large flowers predict sucrose and small flowers quinine.
- Uninformative branch:
  flower size does not predict reward.

Bees simultaneously learn to use size in the informative flower type and
ignore size in the uninformative type.

This is almost exactly the qualitative dependency:

\[
\text{flower type = informative}
\Rightarrow
\text{size cue relevant},
\]

\[
\text{flower type = uninformative}
\Rightarrow
\text{size cue irrelevant}.
\]

It is therefore the strongest natural-history precedent located for
**branch-specific cue relevance**.

### Why it is not yet the public reanalysis

The target/reward in the uninformative branch is stochastic, so the current
deterministic exact-resolution theorem is not a literal model of the task.
More importantly, no stable public raw dataset for the 2015 experiment itself
was located in the present audit.

This study should nevertheless be cited prominently because it shows that the
key conditional architecture is biologically realizable in bumblebees.

---

## 5. Additional public datasets — useful but secondary

### Robert, Tarapata & Nityananda 2024

**Learning modifies attention during bumblebee visual search**,
DOI 10.1007/s00265-024-03432-z.

The paper includes public CSV/R code in its supplementary material and records
individual-level visual-search/inspection time. It establishes that learned
reward changes how bees allocate search effort.

Use:
- external validation that information acquisition effort is measurable and
  plastic.

Do not use:
- as a direct branchwise routeability test.

### Graver et al. 2026

**Timing impacts responses to color and odor in a model insect, the bumblebee
Bombus impatiens**, DOI 10.1242/jeb.251126.

The paper reports that cue weighting changes with the spatiotemporal scale of
encounter: local tasks emphasize colour, whereas intermediate-scale flight
uses colour and odour more jointly. Relevant data are stated to be in the
article/supplement.

Use:
- external scope for spatial/temporal modulation of cue relevance.

### Dale et al. 2005

**Weak and strong priming cues in bumblebee contextual learning**,
DOI 10.1242/jeb.01370.

A priming/context cue changes which later target should be chosen. This is
direct evidence that bumblebees can use sequential context to condition a later
decision.

Use:
- cognitive feasibility of sequential conditional actions.

No reusable public raw dataset has been located.

---

## 6. What can now go into the theory paper

A compact empirical-concordance paragraph may state:

> Public bumblebee experiments independently establish the three biological
> ingredients required by the theory: animals economize the number of cues
> learned when one cue is sufficient, cue acquisition carries measurable
> search/time costs, and contextual cues can change the relevance of later
> information. These studies do not themselves measure the exact adaptive
> versus fixed resolution costs defined here.

If a data panel is included, it should contain only:
1. Spaethe: secondary-cue recruitment, easy versus hard primary cue.
2. Eckel: trajectory/time acquisition-cost proxy, if raw files are
   successfully retrieved and the registered analysis is executable.

Do not combine heterogeneous published effect sizes into a meta-analysis.

---

## 7. Direct experiment still required for the strongest claim

The public-data bridge is valuable because it removes three biological
plausibility objections:

- bumblebees can economize cue use;
- bumblebees pay real costs to obtain/inspect information;
- bumblebees can condition later choices on context.

The remaining missing causal test is narrower:

> holding one physical cue environment fixed, does changing the
> action-conditioned branch structure create the predicted middle-budget
> adaptive advantage?

That is the dedicated routeability experiment.

## Stop rule

Do not continue broad public-data searching after these two bridge datasets
unless a candidate explicitly contains:
- an early realized cue outcome,
- alternative later cue acquisitions,
- trial-level acquisition order/cost,
- and a public raw dataset.

Otherwise treat new examples as ecological precedent, not a reason to delay
the theory submission.
