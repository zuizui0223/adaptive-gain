# Routing second paper — provenance contract v1

## Purpose

Keep the second-paper manuscript surface reproducible without merging unrelated frozen surfaces or modifying the flagship manuscript.

## Base theorem surface

This branch is descended from

`freeze/routing-sharp-modal-corollaries-v1`

at canonical theorem head

`9a70ad3afa00eb0f92980c7d9c12cdccf3750992`.

That surface includes the exact-rational review fix inherited from PR #53 and the general `(q,k)` routing-layer modality theorem from PR #55.

## Independent novelty-governance dependency

The claim boundary is frozen separately at

`freeze/routing-second-paper-novelty-boundary-v1`

with canonical head

`5de3acff8f9982d3726fc30cdd081700c61abfe8`.

That branch is a governance dependency, not a merged code dependency. The manuscript spine reproduces its claim discipline but this branch does not merge or rewrite its history.

## Supporting side-theory dependencies

Used as scope controls:

- `theory/ROUTING_REPRESENTATION_DEPENDENCE.md`
- `theory/ROUTING_MUTATION_BIAS_NONIDENTIFIABILITY.md`
- `theory/ROUTING_REVERSIBLE_MUTATION_CERTIFICATE.md`
- `theory/ROUTING_ORIGIN_FIXATION_SELECTION.md`
- `theory/ROUTING_ORIGIN_FIXATION_PRIOR_ART.md`

Used as theorem implementation/audit:

- `adaptive_gain/routing_layer_modality.py`
- `tests/test_routing_layer_modality.py`
- `adaptive_gain/routing_origin_fixation.py`
- `tests/test_routing_origin_fixation.py`

## Deliberately excluded from manuscript dependency

The second paper does not require the following side-theory stack as main-text dependencies:

- local routing mutation-radius results;
- neutral plateau first-gain dynamics;
- mesoscopic full-target routing dynamics;
- absolute proposal-rate-scale nonidentifiability;
- downstream population-process nonidentifiability ceiling.

They remain valid repository results but are not needed to prove the paper's central threshold.

## Flagship isolation contract

The existing root directory

`manuscript/`

belongs to the frozen Theoretical Ecology flagship and is **out of scope** for this second-paper branch.

All second-paper authoring must remain under

`routing_paper/`

unless the flagship is explicitly reopened by the user.

No file under `manuscript/`, `manuscript/figures/`, or the flagship submission bundle may be modified as a side effect of routing-paper work.

## Biological qualification contract

The theorem paper does not inherit biological validation from the C. elegans or Aedes qualification branches.

Those programs may later provide examples or tests of whether a real genotype-policy map resembles the declared routing representation. Until then, the manuscript must use conditional language:

> for a declared finite routing representation

rather than

> biological routing systems have this representation.

## Next authoring gate

Before adding further abstract routing theory, complete at least:

1. one coherent Introduction draft;
2. one Model/Theory draft containing Theorems 1–3;
3. one Discussion draft respecting the claim ledger;
4. one focused novelty audit against the exact three candidate-new objects.

New side theorems do not substitute for these authoring gates.