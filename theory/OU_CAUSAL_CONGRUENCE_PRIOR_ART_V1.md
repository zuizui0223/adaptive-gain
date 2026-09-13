# Prior-art ceiling v1: causal congruence of partially observed OU systems

## Status

This audit narrows the second-paper novelty claim before any broader impact framing. It is not a claim that all adjacent literature has been exhausted.

## Established prior art that must be conceded

### 1. Partial observation can destroy parameter identifiability in OU/diffusion models

Anders Christian Jensen's 2014 PhD thesis, *Statistical Inference for Partially Observed Diffusion Processes*, treats identifiability in a two-dimensional OU process when one coordinate is completely unobserved. Therefore neither "partially observed OU parameters may be non-identifiable" nor "a hidden OU coordinate complicates inference" is available as a novelty claim.

### 2. Structural identifiability of partially observed stochastic differential equations is an active formal literature

Browning, Chappell, Rahkooy, Loman & Baker, *Exact identifiability analysis for a class of partially observed near-linear stochastic differential equation models* (arXiv:2503.19241; first posted 2025-03-25), develop exact structural-identifiability machinery for linear and near-linear partially observed SDEs and explicitly analyze identifiable parameter combinations and initial-condition dependence.

This is direct mathematical adjacent prior art. Generic statements such as

- `hidden linear SDE mechanisms are not uniquely identified`,
- `only parameter combinations may be identifiable`, or
- `initial conditions affect identifiability`

must not be advertised as new.

### 3. State-space realization non-uniqueness is classical

Similarity transformations, changes of latent coordinates, and multiple state-space realizations for the same observed process are standard control/state-space ideas. The reciprocal evoTS construction is therefore not novel merely because two latent representations share an observation law.

### 4. Moving-optimum OU models and adaptation half-life are established evolutionary theory

Hansen, Pienaar & Orzack (2008) and subsequent adaptation-inertia / moving-optimum work already supply the evolutionary interpretation of OU pull rates, moving adaptive landscapes, and half-life. No novelty is claimed for those models, quantities, or their biological usefulness under a correctly identified causal model.

## What the present branch actually adds

The defensible candidate contribution is the **composition of exact pieces at an active empirical inferential target**:

1. reproduce the exact mean/covariance convention of the implemented `evoTS::logL.joint.OU.BM` nonstationary OUBM likelihood, including its Brownian zero mode and initial-state convention;
2. exhibit a continuum of reciprocal two-state causal realizations whose observed trait process is pathwise/finite-dimensionally identical to that implemented likelihood;
3. translate the gauge into a biological identified set for direct adaptation half-life,
   `H_direct = H_OU/q`;
4. identify the hidden shared-innovation restriction that collapses the causal ambiguity and replace the binary assumption with a finite sensitivity envelope when `|Q12|` is externally bounded;
5. attach that result to published empirical practice and audit how often the fitted OUBM law is promoted from a statistical description to a uniquely attributed adaptation-speed / moving-landscape mechanism.

The novelty is therefore not "non-identifiability exists". It is an exact **practice-specific causal consequence and replacement analysis** for a published evolutionary likelihood.

## Sharp wording boundary

Allowed working language:

> The trait-only evoTS moving-optimum likelihood does not by itself distinguish an exogenous stochastic optimum from a reciprocal latent-state realization in the proven congruence class; consequently its conventional half-life is model-conditional rather than a uniquely identified direct adaptation speed unless additional innovation/cross-coupling restrictions are justified.

Avoid:

- `OU models are non-identifiable`;
- `OU alpha has never been identifiable`;
- `this is the first proof that hidden stochastic models are non-identifiable`;
- `published half-lives are wrong`;
- `moving optima do not exist`;
- `all phylogenetic OU inference is invalid`.

## Remaining prior-art gate

Before paper promotion, search specifically for all of the following combinations:

- nonstationary / integrated OU with Brownian hidden optimum under partial observation;
- reciprocal vs exogenous causal realizations with identical scalar observation law;
- identifiability of Hansen-Pienaar-Orzack moving-optimum models;
- common-noise / correlated-innovation identifiability in two-state OU/SDE systems;
- evolutionary papers explicitly warning that a trait-only moving-optimum likelihood cannot identify causal direction between trait and optimum.

If an exact predecessor already derives the same reciprocal gauge and half-life consequence for the same observation class, the mathematical novelty must be reduced further and the paper would stand or fall on the systematic empirical audit/replacement framework.

## Current impact ceiling

The theorem is mathematically sharp but impact is empirical-practice dependent.

- exact theorem alone: not a Nature-family case;
- exact theorem + one reproduced published fit: strong conceptual/methods case study;
- exact theorem + recurrent direct-target practice + multiple reproductions + usable assumption-sensitivity replacement: broad ecology/evolution scope becomes plausible;
- Nature Ecology & Evolution should be reconsidered only after the prospective practice audit establishes that the affected inference is genuinely field-relevant.
