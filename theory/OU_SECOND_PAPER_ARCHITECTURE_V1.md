# Second-paper architecture v1: what a trait-only OU likelihood identifies

## Working scope

This document freezes the conceptual spine of the causal-identifiability follow-on so the project does not expand by accumulating loosely related OU cautions.

The paper is about a separation between **observable relaxation** and **causal attribution** in evolutionary OU time-series likelihoods.

## Core claim hierarchy

### Claim 1 — exact observation-law congruence for the moving-optimum evoTS likelihood

For the implemented `evoTS::logL.joint.OU.BM` likelihood, the usual exogenous Brownian optimum and a continuum of reciprocal latent-state systems generate the same observed trait process at arbitrary observation times.

This is the strongest causal-direction result: the trait likelihood alone does not distinguish exogenous landscape motion from reciprocal trait-latent feedback in the proven class.

### Claim 2 — adaptation half-life is an identified set for the direct coupling

The fitted relaxation rate satisfies

`alpha = a + d`,

while the direct trait response is `a=q alpha`. Consequently

`H_direct = H_OU/q`.

Without an additional innovation/cross-coupling restriction, the conventional OUBM half-life is the lower endpoint of the direct-coupling half-life set. A bound on hidden common shocks gives a finite sensitivity envelope.

### Claim 3 — the standard paleoTS fixed-optimum joint OU is an exact boundary corollary

Setting optimum innovation variance to zero recovers the fixed-optimum joint likelihood. The identical reciprocal construction therefore applies.

Here the interpretation must be narrower: `log(2)/alpha` remains the model-conditional observed relaxation half-life. What trait data alone do not uniquely identify is that the entire rate `alpha` is a one-way direct attraction or stabilizing-selection coefficient. Congruent reciprocal systems have `alpha=a+d`.

### Claim 4 — published evolutionary practice crosses this distinction

Direct empirical anchors already exist in both strata:

- moving optimum: Voje, Saito-Kato & Spanbauer (2024), fossil diatom time series;
- fixed optimum: Hunt, Bell & Travis (2008), fossil stickleback;
- fixed optimum: Lo Cascio Saetre et al. (2017), reed-warblers in Nature Communications.

The practice audit must distinguish cases where OU parameters are used only descriptively from cases where they are promoted to adaptation speed, restraining force, stabilizing selection or adaptive-landscape mechanism.

## What is explicitly not new

The paper must concede:

- generic OU and state-space non-identifiability;
- realization non-uniqueness;
- reciprocal/multivariate OU adaptation;
- Granger/causal linear-SDE methods;
- general warnings against biological overinterpretation of OU alpha;
- phylogenetic OU half-life theory and its identifiability literature.

The candidate increment is implementation-matched and inferential: exact causal congruence for two evolutionary time-series likelihoods, sharp separation of observed relaxation from direct causal coupling, and a usable assumption-sensitivity replacement tied to real published interpretations.

## Main-text shape

### Figure 1 — same trait law, different causal diagrams
Show the exogenous moving-optimum representation and one reciprocal realization, with the same observed X trajectory/law highlighted. The equality should be represented at the likelihood level, not by a single simulated look-alike trajectory.

### Figure 2 — what alpha means under congruence
Separate `alpha` as observed decay eigenvalue from `a` as direct trait attraction and `d` as reciprocal latent response. Show `alpha=a+d` and the direct half-life identified set / common-shock sensitivity envelope.

### Figure 3 — fixed versus moving optimum consequences
Two columns:
- moving optimum: causal direction and direct half-life both non-unique;
- fixed optimum: observable halfway time retained, one-way mechanistic attribution non-unique.

### Figure 4 — empirical-practice audit
Prospectively coded direct applications by stratum and interpretation code, with independently reproduced fits distinguished from literature-only anchors.

## Empirical reproduction priority

1. reproduce Voje 2024 from the archived Dryad workflow;
2. reproduce Lo Cascio Saetre 2017 if data/code can be recovered cleanly;
3. reproduce at least one Hunt 2008 trait fit from archived/package data or published data;
4. attach exact reciprocal witnesses to the empirical observation times and fitted parameter values;
5. never substitute a published summary calculation for an independent refit in the reproduction count.

## Impact gate

Current status supports a strong conceptual/methodological paper because exact theorems and direct empirical anchors exist in both moving and fixed strata.

Nature Ecology & Evolution remains conditional. Promotion requires:

- a denominator-defensible practice audit showing recurrent mechanistic attribution rather than isolated examples;
- independent empirical reproductions in both strata;
- a clear replacement workflow useful to practitioners;
- evidence that the result changes interpretation rather than merely restating generic OU caution.

If the fixed-OU audit remains small or the majority of empirical studies already supply independent identifying evidence/caution, target a specialist evolutionary methods/concept journal instead. That outcome should be decided by the audit, not by desired prestige.

## Hard boundary

Do not extend to phylogenetic/tree OU, nonlinear adaptive landscapes or higher-dimensional hidden systems merely to increase apparent scope. Each would require a separate observation-law theorem and a new prior-art audit.
