# Manuscript shortening plan v1

## Goal

Reduce repetition without weakening theorem qualifiers, the ecological framing, or the result hierarchy. No new theorem should be introduced during this pass.

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

### 4. Novelty disclaimer

Keep the complete novelty boundary in Discussion `Relation to existing theory`.

In Introduction use one compact paragraph.

Do not list all prior-art component areas twice.

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

- the principal reverse map from required dynamics to required information structure;
- the structural-temporal result as an **extremal envelope**, not a generic realized-variance prediction;
- the oscillation result as a **diagnostic** theorem, conditional on model compatibility;
- the stasis distinction as a **mechanistic proposition** rather than an independent novelty claim.

Keep `within the declared model class` only where mathematically necessary.

### Introduction

Target structure:

1. known short/long-timescale problem;
2. information constraints are known;
3. decision-tree/test-cover machinery is known;
4. exact gap: ecological reachability composition;
5. hierarchical roadmap with the principal reachability theorem first.

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
- one supporting information-complexity inequality.

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

For the principal theorem, retain the `q=3,b=4` Pareto example because it carries the biological tradeoff.

For the structural-temporal envelope, retain only enough of the slack decomposition to make `extremally sharp != generically tight` unambiguous. The two factors are:

- range/variance saturation;
- reward--slow-mode alignment.

For the diagnostic theorem, one sentence must preserve the gate: a complex eigenpair forces feedback only after `0<=T<2` establishes that the generalized persistence domain is nonempty. Outside that trace range, say `model incompatible`, not `feedback forced`.

Do not re-derive definitions already introduced in Model.

### Discussion

Each subsection should answer `what changes biologically?` rather than restating the result.

Lead with the reverse reachability interpretation. Discuss the fluctuation theorem second as an extremal envelope. Keep the oscillation theorem explicitly diagnostic and conditional on model compatibility, and the stasis result explicitly mechanistic.

Cut repeated equations unless they are essential to those interpretations.

## Phrases to use sparingly

- `within the declared model class` — necessary for strong feedback-existence claims; otherwise avoid repetition.
- `exact ecological composition` — use in Introduction novelty paragraph and final Discussion only.
- `finite information structure` — unavoidable central term, but alternate with `finite sensing structure` only when meaning is identical.
- `structurally generated selection` — define once, then use `state-dependent structural reward` where shorter.
- `sharp` — when applied to the structural-temporal ceiling, pair with `extremal` or explicitly distinguish it from realized tightness.

## Terminology consistency

Use consistently:

- `represented ecological alternatives` at first use, then `worlds` only in formal/proof contexts;
- `declared cues` at first use, then `queries` only where needed for the theorem;
- `query arity` = number of possible outcomes of one cue;
- `productive-frontier obligation count E` rather than switching among edge count / mandatory pair count / frontier size without warning;
- `structural gap g` for a state and `Delta g` for a contrast between states;
- `feedback gain G` for the generalized local system;
- `extremal envelope` for the structural-temporal upper bound;
- `diagnostic theorem` for the oscillation/feedback-existence result;
- `model-compatible` for a transient whose trace satisfies `0<=T<2` before feedback inference.

## What must not be shortened away

Retain visibly:

- the structural lift is an assumption;
- reversibility is required for the structural-temporal ceiling;
- the ceiling is extremally sharp but not claimed to predict realized multi-state variance;
- unit costs / deterministic finite sensing are required for the sharp information-complexity results;
- feedback-existence statement is conditional on the generalized local model;
- `alpha=1` is allowed while `phi<1`, so model feasibility and asymptotically stable monotone return are not identical domains;
- the trace gate `0<=T<2` must be checked before a complex eigenpair is interpreted as forcing feedback;
- bounded arity generally gives a Pareto frontier, not one universal minimum;
- nonidentifiability remains a time-interpretation limit.

## Desired endpoint

The submission draft should feel like one ecological argument centered on a principal reverse reachability theorem, with an extremal envelope and a diagnostic theorem supporting it and a mechanistic stasis proposition preventing overinterpretation. It should not read like four independent mathematical notes stitched together.
