# Introduction v0

Natural selection ranks genotypes by fitness, but evolutionary occupancy depends on more than the rank of individual states. A phenotype that is optimal at the level of each genotype may be represented by very few genotypes, while slightly inferior phenotypes may be realized by many more. In weak-mutation models, this distinction enters explicitly through the neutral mutation measure: the stationary abundance of a state reflects both selective weighting and how mutation distributes probability across genotype space. Closely related abundance–selection tradeoffs appear in neutral-network theory, free-fitness formulations, and survival-of-the-flattest phenomena. Our starting point is therefore not the general claim that multiplicity can oppose selection. That principle is established.

A second established ingredient is limiting-component or weakest-link fitness. Many biological systems require multiple components to function, so performance can be controlled by the least adequate component. Recent work has formalized this idea as weakest-link epistasis, in which organismal fitness is determined by the least-fit phenotypic component, and has analyzed its mutation–selection–drift consequences (Labourel, Bansept & McCandlish 2026, bioRxiv preprint). More broadly, minimum-type phenotype–fitness maps and limiting-factor arguments have a long history. We therefore do not introduce weakest-link epistasis, and we do not treat the use of a minimum across components as a contribution by itself.

Here we ask a narrower finite-architecture question. Suppose a routing phenotype is encoded by `k` branch coordinates, each taking integer values from `0` to `q`, and overall routing gain is set by the weakest branch. The genotype-policy space is then

`X={0,...,q}^k`,

with

`g(x)=min_i x_i`.

The fully adapted gain class contains only the single genotype `(q,...,q)`, whereas lower gain classes can contain many genotypes. This representation creates a discrete multiplicity profile before any population-genetic dynamics are specified. The question is whether that profile permits an exact answer to a population-level problem: **how large must the selective tilt be before the full-gain class becomes the dominant stationary gain class after genotype multiplicity is aggregated?**

The answer is unusually simple. We first derive the exact number of genotypes at gain `r`,

`D_r=(q-r+1)^k-(q-r)^k`.

Writing `s=q-r` for the number of gain levels below the optimum gives

`A_s=(s+1)^k-s^k`.

The adjacent suboptimal layer therefore has multiplicity `A_1=2^k-1`. We then show that this adjacent-layer multiplicity controls every more distant layer: for all `s>=1`,

`A_s <= (2^k-1)^s`,

with strict inequality for `k>=2` and `s>=2`. The proof has a finite combinatorial interpretation. Genotypes in the `s`-below-optimum layer correspond to nested sequences of nonempty subsets of branch labels; dropping the nesting restriction yields `(2^k-1)^s` arbitrary subset sequences. Thus comparison with an exponentially large collection of lower-gain genotypes collapses to a single adjacent-layer constant.

Combining this routing-specific multiplicity theorem with the standard reversible weak-mutation stationary law gives a sharp aggregate-layer transition. If each gain step contributes stationary tilt `theta`, then the aggregate weight of gain layer `r` is proportional to

`W_r=D_r theta^r`.

For `k>=2`, the transition has three exact regimes. When `theta<2^k-1`, the adjacent suboptimal layer outweighs the full-gain layer. At `theta=2^k-1`, exactly the adjacent and full-gain layers tie for maximal aggregate stationary weight. When `theta>2^k-1`, the full-gain layer is uniquely aggregate-modal. This threshold is not a switch in the most probable individual genotype: for `theta>1`, the unique full-gain genotype already has greater per-genotype weight than any lower-gain genotype. The threshold emerges only after summing over all genotypes within each gain class.

Under the standard haploid Moran origin-fixation parameterization with multiplicative fitness step `a`, the stationary tilt is `theta=a^(N-1)`, where `N` is population size. The routing result therefore gives an exact population-size corollary without introducing new population-genetic machinery: the full-gain class is aggregate-modal exactly when

`a^(N-1) >= 2^k-1`,

and uniquely modal when the inequality is strict. In the canonical routing construction `k=q+1`, a twofold fitness step gives the particularly simple boundary `N=q+2`.

The threshold is exact because the representation is explicit, not because it is universal. We make this limitation part of the main result rather than leaving it to a generic caveat. First, we hold the gain levels and fitness schedule fixed but replace the branch-product representation by a compressed chain with one genotype per gain level. The aggregate-mode threshold then changes from `2^(q+1)-1` to `1`. Second, even with a fixed mutation-support graph, changing the reversible neutral mutation measure can change stationary gain occupancy arbitrarily. Representation and mutation bias are therefore causal inputs to the stationary conclusion, not quantities determined by the gain coordinate alone.

Our contribution is consequently a finite representation theorem rather than a new theory of mutation–selection balance. A declared branch-product routing architecture induces an exactly countable hierarchy of genotype layers; a nested-chain bound reduces all lower-layer competition to the adjacent layer; and standard selection weighting then produces an exact, architecture-dependent threshold for aggregate gain dominance. The result identifies what can be concluded once a genotype-policy representation and neutral measure are specified, while also showing precisely why the same conclusion cannot be exported to a biological system without independently validating those ingredients.

## Citation anchors for the next prose pass

- Sella & Hirsh 2005 — reversible weak-mutation / statistical-physics stationary weighting.
- McCandlish et al. 2018 — long-term weak-mutation evolution on complex landscapes / stationary formulations.
- Wilke et al. 2001 — survival of the flattest as prior art for abundance–selection competition.
- Rosenheim, Alon & Shinar 2010 — evolutionary balancing of fitness-limiting factors.
- Labourel, Bansept & McCandlish 2026 — weakest-link epistasis and genetic load; current source is a bioRxiv preprint, version 2 posted January 27, 2026.

The next revision should replace these anchors with the repository’s final reference style only after the exact novelty audit is complete.