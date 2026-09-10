# Manuscript shortening plan v1

## Goal

Reduce repetition without weakening theorem qualifiers, the ecological framing, the information-theory boundary, or the result hierarchy. No new theorem should be introduced during this pass.

## Repeated ideas that should appear only once in full

### 1. `Short-term rapid evolution can coexist with long-term stasis is prior art`

Keep the full statement in the first Introduction paragraph.

Elsewhere shorten to phrases such as:

- `Rather than re-explaining temporal cancellation...`
- `The distinction here is structural reachability...`

Do not repeat the full prior-art disclaimer in every section.

### 2. `C_F-C_A is not itself fitness`

Keep the explicit warning in Model 2.3.

In Introduction say only that the gap is linked to selection under an explicit lift.

In Discussion do not restate the full warning unless needed for limitations.

### 3. `Same state space generates amplitude and recurrence`

State this fully in Introduction and Figure 1.

In Model define it formally.

In Discussion refer to `the common state-space construction` rather than repeating the whole argument.

### 4. Information-theory / novelty boundary

Keep the complete novelty boundary in Discussion `Relation to existing theory` and one compact contrast in the Introduction.

The following must remain prior art even after shortening:

- fitness value of environmental information;
- minimum mutual-information requirements for target growth or selection (Moffett & Eckford 2022);
- evolutionary information thresholds;
- evolved sensing/information-processing architecture;
- classical separating systems and adaptive/multiway decision trees.

Do not list every reference repeatedly, but never shorten the principal result to an unqualified `minimum information` novelty claim. Prefer `minimum finite decision/separation structure` or explicit `(n,m,E)` language.

### 5. Result hierarchy

State the hierarchy once in the Introduction roadmap:

- principal reachability theorem;
- supporting structural-temporal extremal theorem;
- diagnostic feedback-existence theorem;
- mechanistic stasis proposition.

Do not repeatedly call these `four results` in a way that makes them sound equal in novelty or evidential weight.

## Section-specific cuts

### Abstract

Aim for approximately 180–230 words. Preserve:

- the principal reverse map from required dynamics to required **finite decision/separation structure**;
- the structural-temporal result as an **extremal envelope**, not a generic realized-variance prediction;
- the oscillation result as a **diagnostic** theorem, conditional on model compatibility;
- the stasis distinction as a **mechanistic proposition** rather than an independent novelty claim.

Do not introduce Shannon bits, mutual information, or rate-distortion notation into the Abstract; the distinction can be made by naming the manuscript's object precisely.

Keep `within the declared model class` only where mathematically necessary.

### Introduction

Target structure:

1. known short/long-timescale problem;
2. information constraints and information-fitness theory are known;
3. finite decision-tree/test-cover machinery is known;
4. exact gap: local feedback phase -> adaptive/fixed gap -> discrete finite structural requirement;
5. hierarchical roadmap with the principal reachability theorem first.

Moffett & Eckford (2022) should remain visible because it is the closest reverse-direction mathematical precursor. The manuscript distinction is the object being minimized and the target: discrete `(n,m,E)` decision/separation architecture for a local feedback phase rather than mutual-information rate for target growth/selection.

Avoid a second mini-Discussion in the Introduction.

### Model

This section should be the most explicit section in the paper.

Keep:

- biological translations of world/query/arity/distinction;
- `C_A`, `C_F`, `g_i`;
- declared lift;
- common state space with `P`;
- generalized local response;
- `0<=alpha<=1`, `0<=phi<1`;
- consequent trace-compatibility domain `0<=T<2`;
- one supporting finite decision/separation-structure inequality.

Move to Supplement or theorem notes:

- detailed provenance of test theory;
- proof logic for `F_b`;
- long explanation of productive-frontier terminology.

### Results

Order results by argumentative weight, not historical development:

1. principal reachability theorem;
2. supporting structural-temporal envelope;
3. diagnostic oscillation/feedback theorem;
4. mechanistic stasis proposition.

For the principal theorem, retain the `q=3,b=4` Pareto example because it carries the biological tradeoff. Call the result a finite decision/separation-structure requirement, not a generic information lower bound.

For the structural-temporal envelope, retain only enough of the slack decomposition to make `extremally sharp != generically tight` unambiguous. The two factors are:

- range/variance saturation;
- reward--slow-mode alignment.

For the diagnostic theorem, one sentence must preserve the gate: a complex eigenpair forces feedback only after `0<=T<2` establishes that the generalized persistence domain is nonempty. Outside that trace range, say `model incompatible`, not `feedback forced`.

Do not re-derive definitions already introduced in Model.

### Discussion

Each subsection should answer `what changes biologically?` rather than restating the result.

Lead with the reverse reachability interpretation, immediately distinguishing it from Moffett & Eckford's reverse mutual-information requirement. Discuss the fluctuation theorem second as an extremal envelope. Keep the oscillation theorem explicitly diagnostic and conditional on model compatibility, and the stasis result explicitly mechanistic.

Cut repeated equations unless they are essential to those interpretations.

## Phrases to use sparingly

- `within the declared model class` — necessary for strong feedback-existence claims; otherwise avoid repetition.
- `exact ecological composition` — use in Introduction novelty paragraph and final Discussion only.
- `finite information structure` — acceptable as the broad paper-level term, but when stating novelty or a minimum requirement prefer `finite decision/separation structure` so it cannot be confused with Shannon/mutual information.
- `structurally generated selection` — define once, then use `state-dependent structural reward` where shorter.
- `sharp` — when applied to the structural-temporal ceiling, pair with `extremal` or explicitly distinguish it from realized tightness.

## Terminology consistency

Use consistently:

- `represented ecological alternatives` at first use, then `worlds` only in formal/proof contexts;
- `declared cues` at first use, then `queries` only where needed for the theorem;
- `query arity` = number of possible outcomes of one cue;
- `productive-frontier obligation count E` rather than switching among edge count / mandatory pair count / frontier size without warning;
- `structural gap g` for a state and `Delta g` for a contrast between states;
- `finite decision/separation structure` for the principal structural object;
- `(n,m,E)` when the minimum/Pareto result is being contrasted with scalar mutual-information rates;
- `feedback gain G` for the generalized local system;
- `extremal envelope` for the structural-temporal upper bound;
- `diagnostic theorem` for the oscillation/feedback-existence result;
- `model-compatible` for a transient whose trace satisfies `0<=T<2` before feedback inference.

## What must not be shortened away

Retain visibly:

- the structural lift is an assumption;
- reversibility is required for the structural-temporal ceiling;
- the ceiling is extremally sharp but not claimed to predict realized multi-state variance;
- unit costs / deterministic finite sensing are required for the sharp finite decision/separation-structure results;
- the principal theorem is not a mutual-information lower bound and does not claim novelty for minimum informational requirements for fitness/selection;
- feedback-existence statement is conditional on the generalized local model;
- `alpha=1` is allowed while `phi<1`, so model feasibility and asymptotically stable monotone return are not identical domains;
- the trace gate `0<=T<2` must be checked before a complex eigenpair is interpreted as forcing feedback;
- bounded arity generally gives a Pareto frontier, not one universal minimum;
- nonidentifiability remains a time-interpretation limit.

## Desired endpoint

The submission draft should feel like one ecological argument centered on a principal reverse **discrete structural reachability** theorem, with an extremal envelope and a diagnostic theorem supporting it and a mechanistic stasis proposition preventing overinterpretation. It should not read like four independent mathematical notes stitched together, and it should not imply that reverse minimum-information reasoning for fitness or selection is new.
