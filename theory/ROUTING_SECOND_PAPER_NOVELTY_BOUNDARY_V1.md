# Routing second-paper novelty boundary v1

## Status

Novelty-governance note only. This document does not alter any theorem, implementation, or claim in the frozen flagship. It records the current boundary after a targeted literature audit of the stacked routing population theory through PR #26.

The correct stance is conservative: the candidate-new result is the **routing-specific finite combinatorics and its sharp modal threshold**, not the population-genetic machinery used to weight states.

## 1. Established prior art — do not claim novelty

### Weak-mutation origin-fixation stationary laws

Moran fixation probabilities, the fixation-ratio identity, detailed balance, and the stationary weighting of fixed genotypes by fitness under symmetric/reversible mutation are established prior art. Sella & Hirsh (2005) and subsequent work give the statistical-physics / Boltzmann form; later formulations explicitly include the mutation-only stationary measure as a degeneracy/neutral-measure factor.

Therefore do **not** claim novelty for:

- `rho(R) / rho(1/R) = R^(N-1)` in the haploid Moran case;
- reversibility of the origin-fixation chain under reversible mutation;
- `pi(x) ∝ mu(x) * fitness(x)^(N-1)` or its log-fitness equivalent;
- the fact that multiplicity / sequence entropy / neutral measure can oppose selection;
- generic mutation-bias dependence of stationary occupancy.

Relevant anchors include Sella & Hirsh (2005), McCandlish et al. (2018), and the broader free-fitness / sequence-entropy literature.

### Minimum / weakest-link fitness maps

The biological and mathematical use of a minimum across limiting components is also prior art. Liebig-style limiting-factor models predate this repository, and recent population-genetic work makes the connection especially direct.

Labourel, Bansept & McCandlish (bioRxiv v2, 2026; DOI `10.64898/2025.12.08.693057`) explicitly define weakest-link epistasis as

`f_WLE(F) = min_d F_d`

and study its mutation-selection-drift consequences. Under continuous i.i.d. component distributions they derive the distribution of the minimum and the resulting stationary fitness distribution / genetic load. They also invoke the standard reversible weak-mutation stationary weighting.

Therefore do **not** claim:

- first use of a `min` fitness/phenotype map;
- first population-genetic analysis of weakest-link/minimum epistasis;
- first demonstration that minimum structure creates many neutral or masked mutations;
- first demonstration that state multiplicity can alter mutation-selection balance.

Older limiting-factor work and survival-of-the-flattest / neutral-network theory make any broader version of those claims even less defensible.

### Survival of the flattest / robustness transitions

The general idea that a lower-fitness but more numerous or more mutationally robust region can dominate an equilibrium distribution is established. Error-threshold, neutral-network, sequence-entropy, and survival-of-the-flattest literatures all contain versions of this selection-versus-degeneracy competition.

Therefore the phrase “selection must overcome degeneracy” is explanatory framing, not the novelty claim.

## 2. Candidate novel core

The candidate contribution begins only after fixing the **finite routing-policy representation** used in the stacked theory.

Let the branch-product routing genotype be a vector in `{0, ..., q}^k` and let routing gain be the weakest branch:

`g(x) = min_i x_i`.

For the canonical routing construction `k = q + 1`, but the combinatorics below are naturally stated for general positive `q, k`.

### Result A — exact routing-layer degeneracy

The number of routing genotypes at gain layer `r` is exactly

`D_r = (q-r+1)^k - (q-r)^k`.

Equivalently, writing distance from the full-gain layer as `s = q-r`,

`A_s = (s+1)^k - s^k`.

This is not being presented as a new formula for order statistics in the abstract. The candidate novelty is that this exact layer count is the genotype multiplicity induced by the declared finite routing-policy representation, and therefore enters the routing origin-fixation stationary law without approximation.

### Result B — global degeneracy-chain bound

For every integer `s >= 1`,

`A_s <= (2^k - 1)^s`,

with equality at `s = 1`.

The repository's combinatorial certificate maps a routing genotype in the distance-`s` layer to a nested chain of nonempty subsets. Dropping the nesting condition yields `(2^k-1)^s` possible subset strings; at `s=1` there is no nesting loss, so the bound is sharp.

The scientific value is not merely bounding a polynomial difference. It collapses **all lower routing layers simultaneously** to the adjacent-layer obstruction.

### Result C — sharp mode-switch threshold

Under the symmetric origin-fixation stationary law

`P(layer q-s) ∝ A_s * theta^(q-s)`,

where `theta` is the per-gain stationary tilt (`theta = a^(N-1)` in the declared Moran fitness-step parameterization), the full-gain layer has maximal aggregate stationary mass among gain layers if and only if

`theta >= 2^k - 1`.

Equivalently,

`(N-1) log a >= log(2^k - 1)`.

Necessity comes from the adjacent layer `s=1`, whose multiplicity is exactly `2^k-1`; sufficiency for every `s>=1` follows from the global degeneracy-chain bound above. Thus the threshold is exact and sharp, not a local or asymptotic criterion.

Important distinction: this is a threshold for the **aggregated stationary mass of gain layers**, not for the most-probable individual genotype. Under the symmetric tilt with `theta > 1`, the unique full-gain genotype already has higher per-genotype probability than any lower-gain genotype; `2^k-1` appears only after summing over the multiplicity of every genotype within a gain layer.

This exact reduction from an exponentially degenerate finite policy space to one sharp threshold is the strongest current candidate for the second paper's theorem-level novelty.

## 3. What distinguishes this from the nearest contemporary WLE work

Labourel et al. analyze a continuous weakest-link phenotype/fitness space and derive distributions of fitness and genetic load from the order statistics of continuous component distributions. Their central scaling is an effective maladaptive bias and mean stationary load.

The routing result addresses a different object:

1. an explicitly finite, mechanistically declared routing-policy genotype space;
2. integer phenotype-layer multiplicities generated by the routing representation;
3. exact comparison of every discrete gain layer under origin-fixation weighting;
4. a sharp condition for when the full-gain layer becomes the stationary **modal gain layer by aggregate mass** despite the combinatorial mass of lower-gain genotypes.

The current audit did not locate the formulas

- `(s+1)^k - s^k`, in this routing-policy population-genetic role;
- `A_s <= (2^k-1)^s` with the nested-subset-chain certificate;
- the exact modal criterion `theta >= 2^k-1`

in the nearest WLE, Sella-Hirsh, free-fitness, survival-of-the-flattest, or neutral-network sources inspected.

This is evidence for a **candidate novelty boundary**, not proof of literature-wide novelty. A submission should still use careful wording such as “for this finite routing representation, we derive...” rather than “for the first time...”.

## 4. Second-paper architecture implied by this boundary

A compact theory paper should center on the following logical spine:

1. **Routing representation** — define the finite branch-product policy genotype and `g=min_i x_i`.
2. **Exact degeneracy theorem** — derive `D_r` / `A_s`.
3. **Origin-fixation projection** — invoke established reversible stationary weighting as a lemma/prior-art bridge, not a contribution.
4. **Sharp modal theorem** — prove the all-layer bound and `theta_c=2^k-1` iff criterion.
5. **Representation dependence** — show that the threshold is a property of the declared genotype-policy representation, not of the phenotypic gain value alone.
6. **Mutation-bias boundary** — under general reversible neutral measure `mu`, occupancy becomes `mu(x) theta^g`; therefore the symmetric threshold is not mutation-representation invariant.
7. **Interpretation** — exact finite architecture can create an entropy-like load opposing directional selection even when the phenotype optimum is unique.

The nonidentifiability results should serve as **scope controls** around the theorem, not as coequal main results.

## 5. Claim ledger

| Claim | Status |
|---|---|
| Moran fixation ratio identity | established prior art |
| Sella-Hirsh stationary weighting | established prior art |
| Reversible neutral-measure factor | established prior art |
| Min / weakest-link fitness map | established prior art |
| Selection-versus-degeneracy competition | established prior art |
| Exact routing layer counts `D_r`, `A_s` | candidate routing-specific novelty |
| Nested-subset-chain global bound | candidate novelty |
| Sharp iff modal threshold `theta_c=2^k-1` | strongest candidate novelty |
| Threshold depends on genotype-policy representation | useful boundary/generalization |
| Mutation bias can alter stationary occupancy at fixed gain map | boundary / identifiability result, not generic mutation-theory novelty |

## 6. Hard stops for manuscript wording

Do not write:

- “we introduce weakest-link epistasis”;
- “we derive the stationary mutation-selection distribution” as a novelty claim;
- “we show for the first time that degeneracy can overcome fitness”;
- “the threshold `2^k-1` is universal” without the finite branch-product representation and symmetric-neutral-measure assumptions;
- “the phenotype gap identifies evolutionary accessibility/occupancy/waiting time.”

Prefer:

- “Within a finite routing-policy representation, the minimum structure induces an exactly countable hierarchy of neutral genotype layers.”
- “Combining those routing-specific multiplicities with the standard origin-fixation stationary law yields an exact, sharp mode-switch criterion.”
- “The criterion is representation-specific; reversible mutation bias replaces raw multiplicity by a neutral-measure weighting.”

## Literature anchors

- Sella G, Hirsh AE. 2005. The application of statistical physics to evolutionary biology. PNAS.
- McCandlish DM et al. 2018. Long-term evolution on complex fitness landscapes when mutation is weak.
- Labourel FJF, Bansept F, McCandlish DM. 2026. Weakest link epistasis and the geometry of genetic load. bioRxiv v2. DOI `10.64898/2025.12.08.693057`.
- Rosenheim JA, Alon U, Shinar G. 2010. Evolutionary balancing of fitness-limiting factors. American Naturalist. DOI `10.1086/652468`.
- Wilke CO et al. 2001. Evolution of digital organisms at high mutation rates leads to survival of the flattest. Nature. DOI `10.1038/35085569`.
- Relevant free-fitness / multiplicity literature cited by Sella-Hirsh and subsequent molecular-evolution work.

## Current verdict

**Do not sell the second paper as new population-genetic machinery.**

Its strongest defensible center is:

> A finite routing architecture with weakest-branch gain has an exact combinatorial entropy profile, and under standard origin-fixation selection the full-gain class becomes the stationary modal gain layer by aggregate mass exactly when selection tilt crosses the sharp architecture-dependent threshold `2^k - 1`.

That is narrower than the original population-genetic framing, but substantially cleaner and more defensible.