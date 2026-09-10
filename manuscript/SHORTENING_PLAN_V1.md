# Manuscript shortening plan v1

## Goal

Reduce repetition without weakening theorem qualifiers or the ecological framing. No new theory should be introduced during this pass.

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

## Section-specific cuts

### Abstract

Aim for approximately 180–230 words. Current abstract is conceptually complete; likely cuts:

- compress the sentence listing already-known component literatures;
- preserve all four results but shorten their clauses;
- keep `within the declared model class` only on the feedback-existence statement or final sentence.

### Introduction

Target structure:

1. known short/long-timescale problem;
2. information constraints are known;
3. decision-tree/test-cover machinery is known;
4. exact gap: ecological reachability composition;
5. four-result roadmap.

Avoid a second mini-Discussion in the Introduction.

### Model

This section should be the most explicit section in the paper.

Keep:

- biological translations of world/query/arity/distinction;
- `C_A`, `C_F`, `g_i`;
- declared lift;
- common state space with `P`;
- generalized local response;
- one supporting information-complexity inequality.

Move to Supplement or theorem notes:

- detailed provenance of test theory;
- proof logic for `F_b`;
- long explanation of productive-frontier terminology.

### Results

Each result should follow the same template:

1. biological question;
2. theorem equation;
3. one proof idea sentence;
4. sharpness/example if needed;
5. ecological interpretation.

Do not re-derive definitions already introduced in Model.

### Discussion

Each subsection should answer `what changes biologically?` rather than restating the theorem.

Cut repeated equations unless they are essential to the interpretation.

## Phrases to use sparingly

- `within the declared model class` — necessary for strong feedback-existence claims; otherwise avoid repetition.
- `exact ecological composition` — use in Introduction novelty paragraph and final Discussion only.
- `finite information structure` — unavoidable central term, but alternate with `finite sensing structure` only when meaning is identical.
- `structurally generated selection` — define once, then use `state-dependent structural reward` where shorter.

## Terminology consistency

Use consistently:

- `represented ecological alternatives` at first use, then `worlds` only in formal/proof contexts;
- `declared cues` at first use, then `queries` only where needed for the theorem;
- `query arity` = number of possible cue outcomes;
- `productive-frontier obligation count E` rather than switching among edge count / mandatory pair count / frontier size without warning;
- `structural gap g` for a state and `Delta g` for a contrast between states;
- `feedback gain G` for the generalized local system.

## What must not be shortened away

Retain visibly:

- the structural lift is an assumption;
- reversibility is required for the sharp spectral ceiling;
- unit costs / deterministic finite sensing are required for the sharp information-complexity results;
- feedback-existence statement is conditional on the generalized local model;
- bounded arity generally gives a Pareto frontier, not one universal minimum;
- nonidentifiability remains a time-interpretation limit.

## Desired endpoint

The submission draft should feel like one ecological argument with four consequences, not four independent mathematical notes stitched together.
