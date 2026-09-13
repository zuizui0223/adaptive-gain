# Routing second paper — provenance contract v1

## Purpose

Keep the second-paper manuscript surface reproducible without merging unrelated frozen surfaces or modifying the flagship manuscript.

## Base theorem surface

This manuscript PR is now based on

`freeze/routing-stationary-majority-threshold-v1`

at canonical head

`c49876d53ab0684b01ac0d264bc843b7aa6a37fd`.

That surface inherits:

- the exact-rational review fix from PR #53;
- the general `(q,k)` routing-layer modality theorem from PR #55;
- the exact stationary-majority theorem from PR #58.

The inherited theorem sequence is therefore:

`exact layer multiplicity -> global degeneracy bound -> aggregate-mode trichotomy -> stationary-majority boundary`.

## Independent novelty-governance dependency

The claim boundary remains frozen separately at

`freeze/routing-second-paper-novelty-boundary-v1`

with canonical head

`5de3acff8f9982d3726fc30cdd081700c61abfe8`.

That branch is a governance dependency, not a merged code dependency. The manuscript reproduces its conservative claim discipline and extends it only to account for the majority theorem.

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
- `theory/ROUTING_SHARP_MODAL_COROLLARIES_V1.md`
- `theory/ROUTING_STATIONARY_MAJORITY_THRESHOLD_V1.md`
- `adaptive_gain/routing_origin_fixation.py`
- `tests/test_routing_origin_fixation.py`

## Frozen CI receipts

Sharp modality surface:

- head `9a70ad3afa00eb0f92980c7d9c12cdccf3750992`;
- CI run `34731638014`;
- Python 3.10 / 3.11 / 3.12 all green.

Majority surface:

- head `c49876d53ab0684b01ac0d264bc843b7aa6a37fd`;
- CI run `34740236273`;
- Python 3.10 / 3.11 / 3.12 all green;
- every job passed full pytest, `examples/audit_witnesses.py`, and `examples/audit_certificate_ladder.py`.

## Deliberately excluded from manuscript dependency

The second paper does not require the following side-theory stack as main-text dependencies:

- local routing mutation-radius results;
- neutral plateau first-gain dynamics;
- mesoscopic full-target routing dynamics;
- absolute proposal-rate-scale nonidentifiability;
- downstream population-process nonidentifiability ceiling.

They remain valid repository results but are not needed to prove the paper's stationary occupancy results.

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

## Authoring status

The original authoring gate is complete:

- Introduction draft exists;
- Model/Results draft contains the full mode-plus-majority theorem sequence;
- Discussion draft respects the claim boundary;
- focused novelty audit exists;
- figure plan explicitly separates mode from majority.

Therefore **new abstract routing theory is no longer the default next step**. Remaining work is literature collision testing, manuscript compression/integration, figure production, and journal fit.