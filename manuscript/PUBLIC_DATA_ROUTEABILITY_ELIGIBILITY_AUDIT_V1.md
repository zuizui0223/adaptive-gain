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

## Decision

No public dataset located in this audit satisfies the full strong-validation
target.

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
