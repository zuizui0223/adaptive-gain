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

The preprint states that raw trial data for the active-information-seeking
experiment are represented in Table S6. No stable external raw-data repository
was located in this audit.

Current status:

- active voluntary information acquisition: **PASS**
- explicit acquisition opportunity cost: **PASS**
- individual repeated trials: **PASS**
- difficulty-dependent acquisition: **PASS**
- branch-specific choice among later cues: **NO**
- fixed-versus-contingent bundle contrast: **NO**
- matched physical environment / changed action map: **NO**
- stable external raw-data repository located: **NO / UNCERTAIN**

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

## Decision

No public dataset located in this audit satisfies the full strong-validation
target. Yuan et al. (2026) comes closest to the **active acquisition and cost**
side of the theory, whereas Chapman et al. (2023) is a strong public example
of **stage-dependent cue relevance**. Neither identifies branch-specific
conditional decision topology.

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
