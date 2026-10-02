# Public-data routeability eligibility audit v1

Date: 2026-10-02

Status: prospective evidence audit. The purpose is to decide what existing
public datasets can and cannot test **before** examining any routeability-shaped
effect estimate.

## Strong validation target

A direct empirical validation of deterministic relational routeability would
ideally contain:

1. a focal action/target that is defined independently of the analysis;
2. at least two available cues with identifiable acquisition costs or timing;
3. trial-level information about which cue outcomes were available/observed;
4. outcome-contingent acquisition or a manipulation that makes later cue access
   depend on an earlier result;
5. a finite observation/time budget, preferably manipulated;
6. enough design control to distinguish an adaptive route from a fixed bundle;
7. raw trial- or individual-level data;
8. a design in which the physical cue environment can be held fixed while the
   action mapping or decision topology changes.

A dataset failing item 4 or 6 can still show **staged cue use** or an
**empirical signature consistent with routeability**, but it cannot validate
\(C_A<C_F\).

A dataset failing item 8 cannot directly validate the new relational theorem
that the same physical environment can induce different routeability under
different focal actions.

---

## Candidate 1 — Wilmsen et al. 2017, Bombus pollen cues

Paper:
*Bumblebees require visual pollen stimuli to initiate and multimodal stimuli to
complete a full behavioral sequence in close-range flower orientation*.
Ecology and Evolution 7:1384–1393.
DOI: 10.1002/ece3.2768.

### Why it is biologically close

Flower-naive *Bombus terrestris* were exposed to artificial pollen stimuli
containing visual, olfactory, gustatory and tactile components. The recorded
behavior is explicitly staged:

\[
\text{approach}
\rightarrow
\text{antennal contact}
\rightarrow
\text{landing}
\rightarrow
\text{later handling responses}.
\]

The paper reports that visual quercetin is sufficient to elicit initial
approach, whereas additional modalities contribute to completing later stages.

That is unusually close to the ecological intuition behind outcome/stage
dependent cue relevance.

### Public-data limitation

The publisher states that all data are in supporting information, but the
public supplement is one small Word file containing Tables S1–S7 rather than a
clearly documented event-level CSV.

Current status:

- multiple cue modalities: **PASS**
- ordered behavioral stages: **PASS**
- individual animals tested: **PASS**
- publicly visible event-level raw schema: **UNCERTAIN / PARTIAL**
- observed adaptive cue acquisition: **NO**
- matched fixed-versus-contingent access: **NO**
- matched physical environment with changed action map: **NO**

### Claim ceiling

Use as:
- motivating natural-history example;
- possible empirical signature of stage-dependent cue relevance if the
  supplement supports a prospective reanalysis.

Do **not** call it a validation of routeability or of \(C_A<C_F\).

---

## Candidate 2 — Kawaguchi et al. 2026, bumblebee colour + social information

Dataset:
*Bandwagon effects in a floral market: early pollinator acquisition offsets
colour disadvantages in less attractive flowers*.
Dryad DOI: 10.5061/dryad.qfttdz0qv.

Public files include:

- \`Approach_to_Landing.csv\`
- \`CageExpData.csv\`
- \`ConsecutiveLandings.csv\`
- \`README.md\`

The dataset explicitly preserves individual bee IDs, first approach, first
landing, approach-only versus landed counts, treatment, innate preference,
social-cue treatment, and repeated landing sequences.

### Strength

This is the strongest candidate for **reproducible public reanalysis** because
the public schema is explicitly trial/individual level rather than only a
published aggregate.

### Limitation

Colour and social information are both environmental signals available in the
choice setting. The design tests their weighting and sampling consequences; it
does not create the theoretical contrast in which one realized observation
selects which later cue must be acquired.

Current status:

- multiple cues: **PASS**
- approach and landing stages: **PASS**
- individual/trial raw data: **PASS**
- prospective stage-conditional analysis possible: **PASS**
- observed adaptive cue acquisition: **NO / INDIRECT**
- fixed-versus-contingent access contrast: **NO**
- matched action-map topology contrast: **NO**

### Claim ceiling

A reanalysis could test:

> whether the contribution of a social cue differs between approach and
> approach-to-landing transition after conditioning on colour preference.

That would be a **context/stage-dependent cue-weighting result**, not direct
measurement of \(C_A\) or \(C_F\).

Use only if the analysis is frozen prospectively and adds something not already
contained in the original paper.

---

## Candidate 3 — Brzozowski et al. 2020, squash beetle host choice

Paper:
*Attack and aggregation of a major squash pest: parsing the role of plant
chemistry and beetle pheromones across spatial scales*.
Journal of Applied Ecology 57:1442–1451.
DOI: 10.1111/1365-2664.13689.

Dataset:
Dryad DOI: 10.5061/dryad.69p8cz8zg.

Public raw files explicitly separate:

- host location;
- host acceptance;
- host attack;
- induced plant volatiles.

The paper frames host choice as successive ecological decisions of host finding,
local examination/acceptance and attack.

### Strength

This is strong evidence that **successive decision stages are an established
ecological object outside pollination biology**. It broadens the ecological
scope of the routeability framing.

### Limitation

The stages are represented by different assays/data files rather than one
individual's observed branchwise acquisition trajectory through one common cue
environment.

Current status:

- successive ecological decision stages: **PASS**
- public raw data: **PASS**
- multiple plant/insect cues: **PASS**
- one common individual-level adaptive path: **NO**
- fixed-versus-contingent access: **NO**
- relational target-map contrast: **NO**

### Claim ceiling

Use as:
- external ecological precedent for hierarchical/staged decision making;
- evidence that stage-specific cues matter in a non-pollinator system.

Do not use as direct routeability validation.

---

## Candidate 4 — Yuan et al. 2026, costly active information seeking in bumble bees

Preprint:
*Uncertainty-Guided Decision-Making in Bumble Bees*.
bioRxiv DOI: 10.64898/2026.09.15.751944.

### Why it is unusually close

The active-information-seeking experiment gives bees a two-stage task. In Zone
1, a bee can voluntarily land on an Information Request platform. That action
produces no direct reward but triggers a brief cue identifying the correct
target in Zone 2. Requesting information carries an explicit opportunity cost:
a correct post-request choice earns 15% sucrose rather than the 30% available
for a correct choice made without requesting information.

The experiment therefore directly establishes three ingredients that the
routeability ecology needs to be biologically plausible:

- organisms can actively acquire information before a later action;
- information acquisition can have an explicit ecological/economic cost;
- acquisition propensity can depend on the current decision state.

Reported request rates increase strongly with task difficulty, and accuracy
after an information request exceeds 92% across difficulty levels. The
experiment also includes Random Free-Cue trials in which the predictive cue is
provided independently of the bee's request action.

### Why it still does not validate routeability

There is one optional information-request action, not a branch-specific choice
among different later cues. The realized outcome of an earlier routing cue
does not determine **which different cue should be acquired next**.

Thus the experiment is a direct precedent for costly active information
acquisition and a biological budget, but not for the structural inequality

\[
C_A<C_F
\]

generated by conditional decision topology.

The preprint states that raw trial data are represented in Table S6. A deeper
audit located the public GitHub repository
`Cuixiaojian21/bee_metacognition`, which contains the complete trial-level
file `data/4_active_information_seeking_trials.csv` (approximately 19,200
trials from 192 bees), together with analysis code. This materially upgrades
the dataset from biological precedent to a reproducible public empirical bridge.

Current status:

- active voluntary information acquisition: **PASS**
- explicit acquisition opportunity cost: **PASS**
- individual repeated trials: **PASS**
- difficulty-dependent acquisition: **PASS**
- branch-specific choice among later cues: **NO**
- fixed-versus-contingent bundle contrast: **NO**
- matched physical environment / changed action map: **NO**
- stable external raw-data repository located: **PASS**
  - GitHub: `Cuixiaojian21/bee_metacognition`
  - raw file: `data/4_active_information_seeking_trials.csv`
  - 19,200 trials from 192 individually identified bees

### Claim ceiling

Use as:
- the strongest current biological precedent for costly active information
  acquisition;
- evidence that a finite observation/information budget is biologically
  meaningful.

Do not present it as a validation of conditional decision topology.

---

## Candidate 5 — Chapman et al. 2023, multimodal artificial flowers in wild insects

Paper:
*Artificial flowers as a tool for investigating multimodal flower choice in
wild insects*. Ecology and Evolution.
DOI: 10.1002/ece3.10687.

Dataset:
Dryad DOI: 10.5061/dryad.jsxksn0h5.

The public dataset contains individual observations classified as Approach,
Landing or Feeding, along with seven experimentally manipulated flower
attributes spanning visual, olfactory and reward dimensions.

### Strength

This is a fully public, multi-attribute ecological dataset in which different
traits affect different behavioral stages. It is useful external evidence that
the relevance of floral cues can change across stages of a naturalistic
decision sequence.

### Limitation

The flower attributes are simultaneously embodied in each treatment. The
insect does not choose which cue to acquire next, and the data do not identify
a branch-specific acquisition policy. The published paper already analyses the
stage dependence, so a reanalysis would add little to the routeability theorem.

Current status:

- public individual-level observations: **PASS**
- multiple experimentally manipulated cues: **PASS**
- multiple behavioral stages: **PASS**
- outcome-contingent cue acquisition: **NO**
- fixed-versus-contingent access contrast: **NO**
- relational target-map contrast: **NO**

### Claim ceiling

Use as ecological precedent for stage-dependent multimodal cue relevance, not
as a routeability test.

---

## Re-audit 2026-10-02 — Bombus public data can support a componentwise empirical test

The earlier binary decision "direct validation or precedent only" was too
coarse. A stronger and more useful distinction is:

1. **full theorem validation** — one experiment directly identifies the matched
   physical cue environment, alternate action maps, multiple branch-specific
   cue resources, acquisition order, costs and fixed/adaptive access;
2. **componentwise operational validation** — public experiments directly test
   distinct necessary consequences of the framework.

No single located dataset yet satisfies (1). Several *Bombus* datasets now make
(2) unusually strong.

### A. Yuan et al. 2026 — costly adaptive information acquisition, raw public trials

Immutable public source family:
- repository: \`Cuixiaojian21/bee_metacognition\`;
- active-seeking file:
  \`data/4_active_information_seeking_trials.csv\`;
- 192 bees × 100 trials = 19,200 trial records.

Fields include:
- Bee_ID;
- Trial_Number;
- Difficulty;
- Trial_Type (Regular / Random_Free_Cue);
- Info_Requested;
- Actually_Landed_On_Platform;
- Post_Request_Accuracy / correctness;
- Non_Request_Accuracy / correctness.

An independent raw-file aggregation gives, for **Regular** trials:

| Difficulty | trials | costly information request | accuracy after request | accuracy without request |
|---|---:|---:|---:|---:|
| Easy | 6,140 | 0.096 | 0.939 | 0.750 |
| Hard | 6,108 | 0.469 | 0.929 | 0.494 |
| Impossible | 3,112 | 0.716 | 0.930 | 0.207 |

Thus the probability of paying for information rises as unaided performance
collapses, while post-acquisition accuracy remains near 0.93–0.94.

The Random_Free_Cue trials additionally manipulate whether the predictive cue
is supplied independently of the bee's platform action. The source repository
contains a preregistered-style GLMM of

\[
\text{platform landing}
\sim
\text{Difficulty}\times\text{Trial Type}
+(1|\text{Bee ID}).
\]

This is a direct public test of **state-dependent costly acquisition**, not just
a published anecdote.

Claim ceiling:
- DIRECT evidence that bumblebees selectively acquire costly information;
- DIRECT evidence that the acquisition rate changes with the current
  informational state and that acquisition restores decision accuracy;
- NOT direct evidence of \(C_A<C_F\) in the deterministic worst-case model,
  because only one optional predictive information source is provided and the
  task does not select among different branch-specific next cues.

A prospective check of whether the immediately preceding trial outcome predicts
the next Regular-trial request after conditioning on current difficulty showed
little additional signal (request rates differed by only a few percentage
points). The useful conditioning variable here is therefore current evidence
quality/difficulty rather than one-step reward history.

### B. MaBouDi et al. 2025 — active sequential sensing with public trajectories

The *Bombus terrestris* active-vision study provides public high-speed
trajectory data and analysis code (Figshare DOI
10.15131/shef.data.14185865.v1).

Bees discriminate plus and multiplication patterns by sequentially inspecting
only a restricted region of each stimulus before accepting or rejecting it.
The inspected regions differ between the two physical patterns. Importantly,
the published analysis reports that pattern-specific scanning remains similar
when reward valence is reversed.

This supplies two useful tests:

1. **positive component** — information acquisition is physically sequential
   and selective rather than parallel access to the whole stimulus;
2. **negative control** — a pure binary relabeling of reward/action that leaves
   the underlying target partition unchanged does not by itself force a new
   scanning architecture.

The second point is compatible with the routeability theorem's distinction
between an arbitrary label swap and a genuine change in decision topology.

Claim ceiling:
- DIRECT evidence for selective sequential sensory acquisition;
- useful invariance control;
- NOT a positive same-environment topology-change test, because the reciprocal
  reward mapping is only a label complement.

### C. Spaethe et al. 2026 — cue allocation tracks information content, public source data

Science Advances DOI: 10.1126/sciadv.adw9320.

All source data for the behavioral experiments are public on Figshare and the
analysis code is archived at
\`stoeckl-lab/Spaethe_et_al_2024_beeDecisions\` / Zenodo
10.5281/zenodo.15911965.

Bees were trained on combined colour + pattern/shape stimuli. Conflict tests
then separated the attributes. When colour pairs were perceptually distant,
bees relied almost exclusively on colour and did not learn the simultaneous
pattern/shape cue; when colour discrimination was difficult, they learned and
used both attributes.

This directly validates the prediction that **the same nominal cue vocabulary
does not imply the same acquired information burden**: secondary cues are
allocated when the primary cue is insufficiently discriminating.

Claim ceiling:
- DIRECT evidence for information-content-dependent cue allocation;
- not a within-encounter branch-specific next-cue policy, because cue
  attributes are simultaneously available and the easy/hard colour values
  change the physical task.

### D. Smolla et al. 2016 — sequential public choices and uncertainty-dependent social cue use

Dryad DOI: 10.5061/dryad.3jb68.

The public \`beeLandings.csv\` records individual landing sequences, cue
positions, rewarding flowers and first/last landing times. The experiment shows
that bees rely more strongly on social information when resource rewards are
highly variable.

This is useful for a prospective history/state-dependent cue-use reanalysis,
but it concerns cue use rather than explicit acquisition of one of several
alternative next cues.

### E. Essenberg et al. 2015 — closest biological topology example, but no public raw table located

Two artificial flower types had unique colour/scent identities. Flower size was
reward-informative in one type and uninformative in the other. The same bees
learned to respond to size only in the branch where size predicted reward.

This is almost a textbook biological example of conditional cue relevance:

\[
\text{flower type A}\Rightarrow\text{size relevant},
\qquad
\text{flower type B}\Rightarrow\text{size irrelevant}.
\]

It is conceptually closer to conditional decision topology than the datasets
above, but the present audit did not locate a reusable trial-level public raw
dataset.

### F. Historical contextual-learning experiments establish biological feasibility

Dale et al. (2005) trained bumblebees so that an earlier priming cue changed
which later visual target was correct. Lotto & Chittka (2005) similarly showed
that illumination context could reverse the correct target colour.

These are strong biological precedents for context-conditioned action maps, but
modern public raw trial data were not located.

---

## Revised evidence decision

The public-data conclusion is now:

\[
\boxed{
\text{No single public dataset validates the full relational theorem,}
}
\]

but also

\[
\boxed{
\text{Bombus public data directly validate three operational components:}
}
\]

1. **costly state-dependent information acquisition** — Yuan et al. 2026;
2. **selective sequential sensory sampling** — MaBouDi et al. 2025;
3. **information-content-dependent cue allocation** — Spaethe et al. 2026.

Smolla et al. adds uncertainty-dependent information-source use, while
Essenberg and the older contextual-learning experiments show that
branch/context-dependent cue relevance is biologically realizable.

This is strong enough for a compact **empirical convergence / biological
grounding section** in the theory paper, provided it is not called a direct
test of the exact \(C_A,C_F\) theorem.

The missing positive experiment remains very specific:

> on one unchanged physical cue matrix, manipulate a focal action mapping so
> that different early outcomes make different later cues relevant, and measure
> whether bees condition costly acquisition accordingly within a finite budget.

That experiment is now a narrow final step rather than an unsupported leap.

---

## Decision

No single public dataset located in this audit satisfies the full
same-environment/action-map routeability theorem. However, the deeper Bombus
audit finds sufficient public raw evidence for a **componentwise empirical
validation program**, with Yuan et al. (2026), MaBouDi et al. (2025) and
Spaethe et al. (2026) covering costly acquisition, sequential sampling and
information-dependent cue allocation, respectively.

Therefore:

\[
\boxed{
\text{public empirical validation is not a prerequisite for the theory paper}.
}
\]

The flagship manuscript should be completed theory-first.

Public data can be added only under one of two roles:

### Role A — prospective empirical concordance

A dataset passes a predeclared analysis and shows a stage-dependent cue effect
that was not selected after looking at the result.

Label:
**empirical signature consistent with routeability**.

### Role B — ecological precedent

Use published results to show that natural decisions are staged and cue
relevance can differ across stages.

Label:
**natural-history motivation / external scope**.

Neither role licenses:
- \(C_A<C_F\) in the natural system;
- a measured routeability advantage;
- validation of the exact balanced theorem;
- validation of the relational same-environment/action-map theorem.

---

## Recommended program

### Paper 1 — theory

Close:
1. fixed cost as a static subset-information optimization;
2. complete static-information-profile non-sufficiency for adaptive cost;
3. outcome-resolved Bellman geometry for \(C_A\);
4. PID and active-feature-acquisition prior-art boundaries;
5. exact-balanced relational theorem and ecological budget consequence.

Submit without waiting for a public-data effect.

### Paper 2 — empirical routeability

Design an experiment that directly manipulates:
- one common physical cue environment;
- focal target/action mapping;
- contingent versus fixed access;
- a finite budget.

The strongest prediction remains a budget-localized interaction rather than a
generic main effect.

---

## Sources audited

- Wilmsen et al. 2017, DOI 10.1002/ece3.2768.
- Kawaguchi et al. 2026, Dryad DOI 10.5061/dryad.qfttdz0qv.
- Brzozowski et al. 2020, DOI 10.1111/1365-2664.13689; Dryad DOI
  10.5061/dryad.69p8cz8zg.
- Yuan et al. 2026, bioRxiv DOI 10.64898/2026.09.15.751944.
- Chapman et al. 2023, DOI 10.1002/ece3.10687; Dryad DOI
  10.5061/dryad.jsxksn0h5.
