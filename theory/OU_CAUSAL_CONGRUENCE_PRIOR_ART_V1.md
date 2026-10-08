# Prior-art ceiling v2: causal congruence of partially observed OU systems

## Status

Targeted prior-art search updated 2026-09-13. This note defines what the second paper may and may not claim. A failure to locate an exact predecessor is a search result, not a priority proof.

## Established prior art that must be conceded

### 1. Partial observation can destroy parameter identifiability in OU/diffusion models

Anders Christian Jensen's 2014 PhD thesis, *Statistical Inference for Partially Observed Diffusion Processes*, treats identifiability in a two-dimensional OU process when one coordinate is completely unobserved. Therefore neither "partially observed OU parameters may be non-identifiable" nor "a hidden OU coordinate complicates inference" is available as a novelty claim.

Browning, Chappell, Rahkooy, Loman & Baker, *Exact identifiability analysis for a class of partially observed near-linear stochastic differential equation models* (arXiv:2503.19241; first posted 2025-03-25), develop exact structural-identifiability machinery for linear and near-linear partially observed SDEs, including identifiable parameter combinations and dependence on initial conditions.

Generic claims such as

- `hidden linear SDE mechanisms are not uniquely identified`,
- `only parameter combinations may be identifiable`, or
- `initial conditions affect identifiability`

are prior art.

### 2. State-space realization non-uniqueness and OU law comparison are prior art

Similarity transformations, changes of latent coordinates, and multiple state-space realizations for the same observed process are standard control/state-space ideas.

Recent probability theory further strengthens this ceiling. Kania (2026), *Law Equivalence for Ornstein–Uhlenbeck Dynamics Driven by Lévy Noise*, studies conditions under which changing the OU drift operator preserves absolute continuity or equivalence of path laws. That result is not the same as the present exact scalar observation-law equality, but it removes any plausible novelty claim of the form "different OU drift mechanisms can never share an observational law."

The reciprocal evoTS construction is therefore not novel merely because two drift/state representations are observationally indistinguishable.

### 3. Reciprocal OU adaptation is already explicit in evolutionary methodology

Bartoszek et al. (2012), *A phylogenetic comparative method for studying multivariate adaptation*, already allow multiple traits to evolve in response to one another and to fixed or randomly evolving predictors.

Voje (2023), *Fitting and evaluating univariate and multivariate models of within-lineage evolution*, explicitly describes **reciprocal adaptation** in multivariate OU models, with non-zero off-diagonal drift terms and either correlated or uncorrelated stochastic changes. Reitan (2019, `layeranalyzer`) and Hannisdal & Liow (2018) likewise place linear SDEs/OU systems inside a Granger-causal framework for biological and palaeontological time series.

Ringen (2026), *Trait coevolution and causal inference using generalized dynamic phylogenetic models*, explicitly contrasts one-way and reciprocal evolutionary effects and emphasizes that observational directional/Granger interpretations require causal assumptions.

Therefore none of the following is novel:

- putting reciprocal feedback into an OU evolutionary model;
- allowing correlated innovations;
- using continuous-time OU/SDE models for directed or reciprocal evolutionary association;
- warning that observational directional effects require causal assumptions.

### 4. Causal interpretation of OU drift matrices is an active mathematical literature

Work on interventions in OU SDEs, graphical OU processes, and causal interpretation of Lévy-driven OU systems already supplies causal semantics for drift matrices under declared assumptions. Adams' 2024 thesis, including work with Recke & Hansen on non-Gaussian graphical precision models, studies conditions under which causal conclusions can be obtained from stationary OU observational distributions.

The present branch must therefore avoid suggesting that it invents causal reading of an OU drift matrix or that causality is generally impossible in continuous-time OU systems.

### 5. Moving-optimum OU models and adaptation half-life are established evolutionary theory

Hansen, Pienaar & Orzack (2008) and the broader adaptation-inertia literature already supply the evolutionary interpretation of OU pull rates, moving adaptive landscapes, optimal/evolutionary regressions, and half-life. Phylogenetic and time-series papers routinely define `log(2)/alpha` as a time/rate of adaptation under their model assumptions.

No novelty is claimed for the model, the half-life transformation, or the biological usefulness of these quantities when the relevant causal structure is externally justified.

## What the present branch can still add

The defensible candidate contribution is the **exact composition at a specific, active empirical likelihood**:

1. reproduce the exact mean/covariance convention of the implemented `evoTS::logL.joint.OU.BM` nonstationary OUBM likelihood, including its Brownian zero mode, sampling-error convention and initial-state convention;
2. show that, when only the trait coordinate is observed, the same complete trait law admits both the published exogenous Brownian-optimum representation and a continuum of reciprocal latent-state representations;
3. make the causal consequence quantitative: the same fitted observed relaxation `alpha` decomposes as `alpha=a+d`, yielding `H_direct=H_OU/q` with no finite upper endpoint when the hidden shared-innovation structure is unconstrained;
4. identify a concrete assumption gate: the declared no-common-shock restriction collapses this particular reciprocal gauge, while an external bound on common shocks gives a finite sensitivity interval;
5. attach the theorem to an actual published OUBM inference and prospectively audit how often this exact statistical fit is promoted to a uniquely attributed adaptation-speed / exogenous-moving-landscape mechanism.

The candidate novelty is therefore not **OU non-identifiability**, **feedback**, **causal SDEs**, or **law equivalence**. It is an exact **likelihood-specific causal identified set and replacement analysis** for a published evolutionary moving-optimum workflow.

## Why the exact theorem is narrower than adjacent work

The branch claims equality of the complete finite-dimensional Gaussian law of the **observed trait coordinate** for arbitrary observation times after a coupled transformation of latent drift, latent initial condition and innovation covariance. This is stronger than demonstrating practical flatness on one dataset, but narrower than a general theorem for arbitrary partially observed OU systems.

It also differs from:

- multivariate reciprocal-adaptation models where both interacting traits/environmental variables are observed;
- phylogenetic OU likelihoods on trees;
- general path-law absolute-continuity/equivalence results, which need not give identical likelihoods pointwise for the same finite observation vector;
- non-Gaussian graphical OU identifiability results that use higher-order information unavailable in a Gaussian trait-only likelihood.

These distinctions must remain explicit.

## Targeted exact-predecessor search result

The 2026-09-13 search explicitly combined terms for:

- partially observed OU/SDE identifiability;
- moving / randomly evolving Brownian optimum;
- reciprocal versus exogenous OU feedback;
- correlated/common innovations;
- causal OU law equivalence;
- Hansen-Pienaar-Orzack / evoTS OUBM;
- fossil time-series Granger/linear-SDE causality.

It located the adjacent literatures above but **did not locate an exact predecessor that simultaneously**:

1. targets the implemented `evoTS::logL.joint.OU.BM` nonstationary observation law;
2. gives an exogenous-optimum versus reciprocal-hidden-state equality for the observed trait law;
3. derives the resulting `H_direct in [H_OU, infinity)` mechanistic half-life identified set; and
4. supplies the common-shock sensitivity replacement.

This is a bounded search outcome, not evidence of priority. The literature gate remains reopenable if a closer predecessor is found.

## Sharp wording boundary

Allowed working language:

> For the trait-only evoTS moving-optimum likelihood, the observed trait law does not by itself distinguish the published exogenous stochastic-optimum representation from a reciprocal latent-state realization in the proven congruence class. Consequently the conventional OUBM half-life is model-conditional rather than a uniquely identified direct adaptation speed unless additional innovation/cross-coupling restrictions are justified.

Avoid:

- `OU models are non-identifiable`;
- `reciprocal OU adaptation is new`;
- `OU alpha has never been identifiable`;
- `this is the first proof that hidden stochastic models are non-identifiable`;
- `published half-lives are wrong`;
- `moving optima do not exist`;
- `all phylogenetic OU inference is invalid`;
- `Granger causality cannot be inferred from OU models`.

## Current impact ceiling

The mathematical gate is now sharp enough that adding more generic OU algebra has low value. Impact depends on practice and empirical scope:

- exact theorem + one published-summary witness: real conceptual target, but still a case study;
- independent reproduction of the Voje et al. fit: strong conceptual/methods case;
- recurrent direct-target usage under the frozen audit protocol + multiple reproduced fits + usable sensitivity replacement: broad ecology/evolution scope becomes plausible;
- Nature Ecology & Evolution should be reconsidered only if the audit shows that this exact inferential move materially affects a nontrivial body of published evolutionary inference.
