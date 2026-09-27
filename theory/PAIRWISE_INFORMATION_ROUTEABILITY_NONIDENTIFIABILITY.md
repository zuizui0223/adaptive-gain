# Pairwise-information nonidentifiability of ecological routeability

Status: exact constructive side result supporting the direct routeability experiment. This does **not** modify the frozen Evolution Letters V5 submission surface.

## Proposition

There exist two four-state, three-cue binary ecological decision tasks with the same target balance, cue costs, cue marginals, named pairwise information signature, and adaptive minimum cost `C_A=2`, but different fixed minimum costs:

- routeable task: `C_F=3`;
- bypass control: `C_F=2`.

Therefore fixed-resolution cost and strict adaptive gain are not identifiable from the pairwise information surface alone.

## Pairwise information signature

For every named pair among `{target, q_left, q_route, q_right}`, form the binary 2x2 contingency counts under the uniform distribution over represented states and canonicalize over independent relabeling of the two binary outcome symbols.

The six named canonical count profiles are the pairwise information signature. Equal signatures imply equal pairwise mutual information for every target-cue and cue-cue pair.

Executable definition: `adaptive_gain.ecological_routeability_experiment.pairwise_information_signature`.

## Exact witness

The routeable task is the repository's minimal strict-gain normal form:

| state | target | q_left | q_route | q_right |
| --- | ---: | ---: | ---: | ---: |
| w0 | 0 | 0 | 0 | 0 |
| w1 | 0 | 0 | 1 | 1 |
| w2 | 1 | 1 | 1 | 1 |
| w3 | 1 | 0 | 0 | 1 |

It has `(C_A,C_F)=(2,3)`.

The matched bypass control is:

| state | target | q_left | q_route | q_right |
| --- | ---: | ---: | ---: | ---: |
| w0 | 0 | 0 | 0 | 1 |
| w1 | 0 | 0 | 1 | 1 |
| w2 | 1 | 0 | 0 | 0 |
| w3 | 1 | 1 | 1 | 1 |

It has `(C_A,C_F)=(2,2)`.

## Exact pairwise equality

For both tasks the six canonical pair signatures are identical:

| named pair | canonical counts |
| --- | --- |
| target x q_left | `(0, 2, 1, 1)` |
| target x q_route | `(1, 1, 1, 1)` |
| target x q_right | `(0, 2, 1, 1)` |
| q_left x q_route | `(0, 1, 2, 1)` |
| q_left x q_right | `(0, 1, 1, 2)` |
| q_route x q_right | `(0, 2, 1, 1)` |

Thus every pairwise mutual-information value is identical between the two architectures, while the strict adaptivity gaps are `1` and `0`.

## Why the difference survives

The distinction lies in higher-order conditional organization:

- in the routeable task, the context outcome determines which terminal cue remains target-relevant;
- in the bypass task, the two terminal cues resolve the target without needing that routing dependence.

Routeability is therefore not reducible to single-cue informativeness or the pairwise mutual-information matrix.

## Corollary — nonidentifiability

Let `Sigma_2` be the pairwise information signature and `g=C_F-C_A`. The witnesses satisfy `Sigma_2(R)=Sigma_2(B)` but `g(R)=1 != 0=g(B)`.

Hence there is no function of `Sigma_2` alone that recovers strict adaptive gain for every task in this finite binary domain.

This is a constructive nonidentifiability statement, not a claim that pairwise mutual information is generally useless.

## Relation to known higher-order information

Information theory already contains classic examples, such as XOR, in which pairwise mutual information misses higher-order dependence. No novelty is claimed for that generic fact.

The specific result here is narrower: the minimal ecological routeability task and a matched no-gain control have the same full named pairwise-information surface while differing in fixed-resolution cost and adaptive gain.

## Experimental consequence

The artificial-flower experiment therefore matches more than richness and cue frequencies. At the symbolic design level it also matches pairwise information strength among all target/cue pairs and cue/cue pairs.

A behavioral architecture-by-access interaction cannot be explained merely by one architecture having stronger pairwise cue informativeness.

Physical cue salience, timing and learned symbol meaning still require counterbalancing and manipulation checks.

## Minimality

The strict-gain member is the repository's established minimal four-world / three-query normal form. Since strict adaptive gain does not occur at a smaller binary unit-cost task size in that domain, a matched nonidentifiability witness containing a strict-gain task cannot occur on a smaller surface.

## Claim boundary

Do not claim:

- pairwise mutual information is generally useless;
- generic higher-order information or synergy is new;
- every higher-order ecological effect is routeability;
- weak pairwise association in natural data implies routeability;
- symbolic information matching automatically matches animal perceptual salience.

The exact claim is only: **pairwise information is insufficient to identify routeability, even at the minimal finite task where strict routeability first appears.**

## Reproducibility

- `adaptive_gain/ecological_routeability_experiment.py`
- `tests/test_ecological_routeability_experiment.py`
- `examples/build_routeability_experiment_stimuli.py`
