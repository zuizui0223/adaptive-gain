# Routing second paper — claim ledger v1

## Purpose

Freeze what the second paper may claim, where each claim belongs, and which stacked results must remain scope controls or supplement material.

This ledger is subordinate to two frozen theorem/governance surfaces:

- `freeze/routing-second-paper-novelty-boundary-v1`;
- `freeze/routing-stationary-majority-threshold-v1`.

The latter inherits the sharp aggregate-modality theorem from `freeze/routing-sharp-modal-corollaries-v1` and adds the stationary-majority result.

## Claim classes

| ID | Claim | Status | Manuscript role |
|---|---|---|---|
| C1 | For `X={0,...,q}^k`, `g=min_i x_i`, gain-layer multiplicity is `D_r=(q-r+1)^k-(q-r)^k`. | candidate routing-specific novelty | Main Theorem 1 |
| C2 | With `A_s=(s+1)^k-s^k` and `T_k=2^k-1`, `A_s<=T_k^s`; for `k>=2`, equality occurs only at `s=1`. | candidate novelty | Main Theorem 2 |
| C3 | Under symmetric per-gain tilt, `theta<T_k`, `theta=T_k`, `theta>T_k` give nonmodal / exact `{q-1,q}` tie / uniquely modal full-gain layer. | strongest closed-form candidate novelty | Main Theorem 3 |
| C4 | Full-gain stationary mass is `P_full(theta)=1/(1+sum_{s=1}^q A_s theta^{-s})`; its unique half-mass boundary satisfies `theta^q=sum A_s theta^(q-s)`, with `T_k<theta_1/2<2T_k` for `q>=2`. | candidate routing-specific occupancy consequence | Main Theorem 4 |
| C5 | Under Moran tilt `theta=a^(N-1)`, aggregate modality and majority translate into exact population-size thresholds. | corollary using prior-art population genetics | Main Corollary |
| C6 | In canonical routing `k=q+1`, `a=2`, first unique mode is `N=q+2`; first stationary majority is `N=q+3` for every `q>=2` (`q=1` is the boundary exception). | exact canonical corollary | Main example / corollary |
| C7 | Same gain phenotypes and fitness schedule can yield opposite aggregate stationary conclusions under branch-product versus compressed representations. | exact boundary result; generic representation dependence is prior art | Main scope proposition |
| C8 | With fixed support graph and fixed fitness tilt, reversible mutation bias can generate arbitrary positive stationary occupancy. | exact identifiability boundary; generic mutation bias is prior art | Main scope proposition |
| C9 | Local routing representation can inflate mutational distance by factor `q+1` relative to compressed gain chain. | useful but secondary | Supplement / optional representation paragraph |
| C10 | Neutral plateau waiting times, mesoscopic full-target dynamics, absolute rate scaling, downstream population nonidentifiability. | valid side theory but not part of paper center | Exclude from main text |

## Established prior art — never phrase as contribution

The following statements may be used only as lemmas, setup, or citations:

- Moran fixation probability and fixation-ratio identity;
- Sella–Hirsh / reversible weak-mutation stationary weighting;
- `pi(x) proportional to mu(x) fitness(x)^(N-1)` under the relevant assumptions;
- minimum / weakest-link fitness maps;
- state multiplicity, sequence entropy, neutral networks, free-fitness style competition;
- explicit equilibrium competition between selection and sequence multiplicity, including Riedel et al. (2015);
- survival-of-the-flattest type abundance–selection tradeoffs;
- generic genotype–phenotype representation dependence;
- mutation bias affecting stationary distributions.

## Precision rules

### P1 — mode, majority, and per-genotype mode are different estimands

When discussing `2^k-1`, “mode” means the **aggregate gain-layer mode**:

`W_r = sum_{x:g(x)=r} pi_unnormalized(x)`.

For `theta>1`, the unique full-gain genotype already has the greatest per-genotype weight. The theorem at `2^k-1` does not describe an individual-genotype mode switch.

“Stationary majority” means

`P_full >= 1/2`.

Do not use “dominant” without specifying which of these objects is meant.

### P2 — modality threshold equality is a tie

For `k>=2`, at

`theta=2^k-1`,

exactly the adjacent and full layers tie. Unique aggregate modality requires strict inequality.

### P3 — majority is strictly later than modality for `q>=2`

For `q>=2`,

`T_k < theta_1/2(q,k) < 2T_k`.

Thus the full-gain class can be the largest gain class while still holding less than half of stationary mass. In the canonical `a=2` family this produces the exact one-step population-size gap `q+2` versus `q+3`.

### P4 — neither threshold is universal

Both results are conditional on:

1. the branch-product routing representation;
2. weakest-branch gain `g=min`;
3. symmetric neutral measure at the genotype level;
4. stationary tilt depending only on gain.

A different representation or reversible neutral measure can change or destroy the thresholds.

### P5 — do not biologize the representation by analogy

A neural, regulatory, developmental, or behavioral system is not evidence for the branch-product genotype map merely because it performs state-dependent routing.

Biological use requires independent qualification of heritable representation and mutation coordinates.

## Wording allowed in Abstract

Allowed:

- “For a finite branch-product routing representation, we derive exact genotype multiplicities for every gain layer.”
- “A nested-subset-chain bound reduces comparison with all lower-gain layers to the adjacent layer.”
- “The full-gain class becomes aggregate-modal at the sharp threshold `theta=2^k-1`; at equality exactly two gain layers tie.”
- “Stationary majority occurs at a distinct unique threshold, lying strictly between `T_k` and `2T_k` when `q>=2`.”
- “The thresholds change when the genotype-policy representation or neutral mutation measure changes.”

Not allowed:

- “We introduce weakest-link epistasis.”
- “We derive the mutation-selection stationary law.”
- “We discover that degeneracy can overcome selection.”
- “Selection must exceed `2^k-1` in biological routing systems.”
- “The phenotype gap determines evolutionary accessibility or occupancy.”
- “The full-gain genotype undergoes a mode switch at `2^k-1`.”
- “The mode threshold is the point at which the optimum occupies most of the population.”

## Result promotion rules

A result enters the main text only if it does one of four jobs:

1. establishes the exact multiplicity hierarchy;
2. establishes or interprets the mode/majority occupancy thresholds;
3. proves why those thresholds are representation-specific;
4. states the mutation-measure claim ceiling.

Everything else must justify its presence against this rule.

## Current main-text set

**Keep**

- general `(q,k)` layer multiplicity;
- nested-chain global bound;
- exact aggregate modality trichotomy;
- exact stationary-majority boundary and `T_k < theta_1/2 < 2T_k` bracket;
- Moran population-size corollaries, including canonical `q+2` versus `q+3`;
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

Before submission, rerun a focused literature review on four exact objects only:

1. `(s+1)^k-s^k` used as finite weakest-branch genotype-layer multiplicity;
2. the nested-subset-chain inequality `A_s<=(2^k-1)^s` with strictness for `s>=2`;
3. the exact aggregate-mode trichotomy at `theta=2^k-1`;
4. the paired mode/majority structure, especially `T_k<theta_1/2<2T_k` and the canonical `a=2` population-size separation.

Do not broaden the search into generic weakest-link, robustness, neutral-network, or mutation-selection literature unless a direct collision is found.