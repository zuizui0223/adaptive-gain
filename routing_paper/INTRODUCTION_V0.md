# Introduction v1

Natural selection ranks genotypes by fitness, but stationary evolutionary occupancy depends on more than the rank of individual states. A high-fitness phenotype may be realized by few genotypes while slightly inferior phenotypes are represented by many more. This distinction is established in weak-mutation and genotype–phenotype theory: reversible stationary laws combine selection with a neutral mutation measure, and sequence multiplicity can enter equilibrium statistics directly. Riedel et al. (2015), for example, parameterized the relative number of sequence variants representing alternative states and combined that multiplicity with selection in low-mutation equilibrium inference. Neutral-network, free-fitness, and survival-of-the-flattest literatures provide related abundance–selection effects. Our starting point is therefore not the general claim that multiplicity can oppose selection.

A second established ingredient is limiting-component or weakest-link fitness. Many systems require several components to function, so total performance can be controlled by the least adequate component. Recent population-genetic work explicitly analyzes weakest-link epistasis with organismal fitness set by the minimum component (Labourel, Bansept & McCandlish 2026, bioRxiv preprint), while limiting-factor arguments are much older. We therefore do not introduce a `min` phenotype map or claim novelty for its generic mutation–selection consequences.

Here we ask a narrower finite-architecture question. Suppose a routing phenotype is encoded by `k` branch coordinates, each taking integer values from `0` to `q`, with overall gain set by the weakest branch:

`X={0,...,q}^k`,

`g(x)=min_i x_i`.

The full-gain class contains the single genotype `(q,...,q)`, whereas lower gain classes can contain many genotypes. The representation therefore creates a discrete multiplicity profile before population-genetic dynamics are specified. We ask two distinct occupancy questions. First, how large must the selective tilt be before the full-gain class becomes the **largest aggregate gain class**? Second, how much stronger must selection be before full gain contains **at least half of stationary probability**? Separating these estimands prevents “dominance” from conflating a mode with a majority.

We first derive the exact number of genotypes at gain `r`,

`D_r=(q-r+1)^k-(q-r)^k`.

Writing `s=q-r` for distance below full gain gives

`A_s=(s+1)^k-s^k`.

The adjacent layer therefore has multiplicity `A_1=2^k-1`. We then show that this one number controls every more distant layer:

`A_s <= (2^k-1)^s`,

with strict inequality for `k>=2` and `s>=2`. A finite combinatorial certificate maps states in the `s`-below-full layer to nested sequences of nonempty subsets of branch labels; dropping nesting gives `(2^k-1)^s` arbitrary subset sequences. Thus comparison with all lower layers collapses to one adjacent-layer obstruction.

Combining this routing-specific multiplicity result with the standard reversible weak-mutation stationary law yields the first exact occupancy threshold. If each gain step contributes stationary tilt `theta`, aggregate gain-layer weight is

`W_r=D_r theta^r`.

Let `T_k=2^k-1`. For `k>=2`, if `theta<T_k` the full-gain layer is nonmodal; at `theta=T_k`, exactly the full and adjacent layers tie for maximal aggregate weight; and if `theta>T_k`, full gain is uniquely aggregate-modal. This is not a switch in the most probable individual genotype: for `theta>1`, the unique full-gain genotype already has greater per-genotype weight than any lower-gain genotype. `T_k` appears only after summing over genotype multiplicity within gain classes.

Aggregate modality does not imply majority. The stationary full-gain mass is

`P_full(theta)=1/[1+sum_{s=1}^q A_s theta^{-s}]`.

It crosses one half at a unique positive `theta_1/2(q,k)`. For `q=1`, this majority threshold equals `T_k`; for every `q>=2`, the same global layer bound gives the strict bracket

`T_k < theta_1/2(q,k) < 2T_k`.

Thus finite routing architecture creates two ordered transitions: full gain first becomes the largest gain class and only later becomes a stationary majority.

Under the standard haploid Moran origin-fixation parameterization with multiplicative fitness step `a`, established theory gives `theta=a^(N-1)`. The routing theorems therefore translate directly into population-size corollaries without introducing new population-genetic machinery. In the canonical construction `k=q+1` with `a=2`, full gain becomes uniquely aggregate-modal at `N=q+2`. For every `q>=2`, it becomes a stationary majority exactly one population-size step later, at `N=q+3`.

These thresholds are exact because the representation is explicit, not because they are universal. We make that limitation part of the main argument. Holding gain levels and phenotype-level fitness fixed but replacing the branch-product representation by a compressed chain changes the modal threshold from `2^(q+1)-1` to `1`. Likewise, even on a fixed mutation-support graph, changing a reversible neutral mutation measure can generate arbitrarily different positive stationary occupancies. Representation and mutation bias are therefore causal inputs to occupancy, not quantities identified by the gain coordinate alone.

Our contribution is consequently a finite representation result rather than a new theory of mutation–selection balance. A declared branch-product routing architecture induces an exactly countable hierarchy of genotype layers; a nested-chain bound reduces all lower-layer competition to the adjacent layer; and standard selection weighting then yields exact thresholds for two distinct forms of stationary occupancy. The accompanying representation and mutation-measure controls show precisely when those conclusions cease to be identified.

## Citation anchors for the next prose pass

- Sella & Hirsh 2005 — reversible weak-mutation / statistical-physics stationary weighting.
- McCandlish et al. 2018 — long-term weak-mutation evolution on complex landscapes.
- Riedel, Khatri, Lässig & Berg 2015 — explicit sequence-multiplicity parameter combined with selection in low-mutation equilibrium inference.
- Wilke et al. 2001 — survival of the flattest as prior art for abundance–selection competition.
- Rosenheim, Alon & Shinar 2010 — evolutionary balancing of fitness-limiting factors.
- Labourel, Bansept & McCandlish 2026 — weakest-link epistasis and genetic load; bioRxiv preprint, version 2 posted January 27, 2026.

Final citation formatting and priority wording remain blocked on the dedicated scholarly novelty pass.