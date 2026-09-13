# Routing second paper — claim ledger v1

## Purpose

Freeze what the second paper may claim, where each claim belongs, and which stacked results must remain scope controls or supplement material.

This ledger is subordinate to the frozen novelty boundary at

`freeze/routing-second-paper-novelty-boundary-v1`

and the frozen theorem implementation at

`freeze/routing-sharp-modal-corollaries-v1`.

## Claim classes

| ID | Claim | Status | Manuscript role |
|---|---|---|---|
| C1 | For `X={0,...,q}^k`, `g=min_i x_i`, gain-layer multiplicity is `D_r=(q-r+1)^k-(q-r)^k`. | candidate routing-specific novelty | Main Theorem 1 |
| C2 | With `A_s=(s+1)^k-s^k` and `T_k=2^k-1`, `A_s<=T_k^s`; for `k>=2`, equality occurs only at `s=1`. | candidate novelty | Main Theorem 2 |
| C3 | Under symmetric per-gain tilt, `theta<T_k`, `theta=T_k`, `theta>T_k` give nonmodal / exact `{q-1,q}` tie / uniquely modal full-gain layer. | strongest candidate novelty | Main Theorem 3 |
| C4 | Under Moran tilt `theta=a^(N-1)`, aggregate modality is equivalent to `a^(N-1)>=T_k`, uniqueness to strict `>`. | corollary using prior-art population genetics | Main Corollary |
| C5 | In canonical routing `k=q+1`, `a=2`, first modal and first uniquely modal population sizes are `N=q+2`. | exact canonical corollary | Main example / corollary |
| C6 | Same gain phenotypes and fitness schedule can yield opposite aggregate stationary conclusions under branch-product versus compressed representations. | exact boundary result; generic representation dependence is prior art | Main scope proposition |
| C7 | With fixed support graph and fixed fitness tilt, reversible mutation bias can generate arbitrary positive stationary occupancy. | exact identifiability boundary; generic mutation bias is prior art | Main scope proposition or short subsection |
| C8 | Local routing representation can inflate mutational distance by factor `q+1` relative to compressed gain chain. | useful but secondary | Supplement / optional representation paragraph |
| C9 | Neutral plateau waiting times, mesoscopic full-target dynamics, absolute rate scaling, downstream population nonidentifiability. | valid side theory but not part of paper center | Exclude from main text |

## Established prior art — never phrase as contribution

The following statements may be used only as lemmas, setup, or citations:

- Moran fixation probability and fixation-ratio identity;
- Sella–Hirsh / reversible weak-mutation stationary weighting;
- `pi(x) proportional to mu(x) fitness(x)^(N-1)` under the relevant assumptions;
- minimum / weakest-link fitness maps;
- state multiplicity, sequence entropy, neutral networks, free-fitness style competition;
- survival-of-the-flattest type abundance–selection tradeoffs;
- generic genotype–phenotype representation dependence;
- mutation bias affecting stationary distributions.

## Precision rules

### P1 — “mode” always means aggregate gain-layer mode when discussing `2^k-1`

Never write that `2^k-1` is the threshold at which the full-gain **genotype** becomes the most probable genotype.

For `theta>1`, the unique full-gain genotype already has the greatest per-genotype weight. The theorem concerns

`W_r = sum_{x:g(x)=r} pi_unnormalized(x)`.

### P2 — threshold equality is a tie, not unique dominance

For `k>=2`, at

`theta=2^k-1`,

exactly the adjacent and full layers tie. Unique aggregate dominance requires strict inequality.

### P3 — `2^k-1` is not universal

It is conditional on:

1. the branch-product routing representation;
2. weakest-branch gain `g=min`;
3. symmetric neutral measure at the genotype level;
4. stationary tilt depending only on gain.

A different representation or reversible neutral measure can change or destroy the threshold.

### P4 — do not biologize the representation by analogy

A neural, regulatory, developmental, or behavioral system is not evidence for the branch-product genotype map merely because it performs state-dependent routing.

Biological use requires independent qualification of heritable representation and mutation coordinates.

## Wording allowed in Abstract

Allowed:

- “For a finite branch-product routing representation, we derive exact genotype multiplicities for every gain layer.”
- “A nested-subset-chain bound reduces comparison with all lower-gain layers to the adjacent layer.”
- “The full-gain class becomes aggregate-modal at the sharp threshold `theta=2^k-1`; at equality exactly two gain layers tie.”
- “The threshold changes when the genotype-policy representation or neutral mutation measure changes.”

Not allowed:

- “We introduce weakest-link epistasis.”
- “We derive the mutation-selection stationary law.”
- “We discover that degeneracy can overcome selection.”
- “Selection must exceed `2^k-1` in biological routing systems.”
- “The phenotype gap determines evolutionary accessibility or occupancy.”
- “The full-gain genotype undergoes a mode switch at `2^k-1`.”

## Result promotion rules

A result enters the main text only if it does one of three jobs:

1. establishes the exact threshold;
2. proves why the threshold is representation-specific;
3. states the mutation-measure claim ceiling.

Everything else must justify its presence against this rule.

## Current main-text set

**Keep**

- general `(q,k)` layer multiplicity;
- nested-chain global bound;
- exact aggregate modality trichotomy;
- Moran population-size corollary;
- compressed-chain representation contrast;
- reversible neutral-measure boundary.

**Do not promote**

- coupon-collector / first-gain timing;
- mesoscopic target-acquisition dynamics;
- arbitrary representation-distance constructions beyond the clean comparator;
- stationary occupancy nonidentifiability as a separate flagship theorem once mutation-measure boundary is stated;
- absolute proposal-rate scaling;
- downstream population-process nonidentifiability.

## Novelty review trigger

Before turning this spine into a submission-ready manuscript, rerun a focused literature review on three exact objects only:

1. `(s+1)^k-s^k` used as finite weakest-branch genotype-layer multiplicity;
2. the nested-subset-chain inequality `A_s<=(2^k-1)^s` with strictness for `s>=2`;
3. the exact aggregate-mode trichotomy at `theta=2^k-1`.

Do not broaden the search into generic weakest-link, robustness, neutral-network, or mutation-selection literature unless a direct collision is found.