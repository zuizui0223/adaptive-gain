# Exact occupancy thresholds in finite routing representations

## Abstract

Phenotype-level fitness does not by itself determine stationary phenotype occupancy when different phenotypes are represented by different numbers of genotypes. This selection–multiplicity tension and representation-dependent evolutionary thresholds are established ideas. Here we derive two exact occupancy transitions for a finite routing representation. Genotype-policy states are `x in {0,...,q}^k`, with gain set by the weakest branch, `g(x)=min_i x_i`. The gain-`r` class contains `D_r=(q-r+1)^k-(q-r)^k` genotypes. Writing `A_s=(s+1)^k-s^k` for the class `s` steps below full gain, the routing hierarchy satisfies `A_s <= (2^k-1)^s`, with equality only for the adjacent class when `k>=2`. Under a symmetric stationary tilt `theta` per gain step, this yields an exact aggregate-mode threshold `T_k=2^k-1`: below `T_k` full gain is nonmodal, at `T_k` it ties only with the adjacent class, and above `T_k` it is uniquely modal. A stronger stationary-majority threshold `theta_1/2(q,k)` satisfies `T_k < theta_1/2 < 2T_k` for `q>=2`. Under the standard Moran origin-fixation tilt `theta=a^(N-1)`, canonical routing `k=q+1` with `a=2` becomes uniquely modal at `N=q+2` but a stationary majority only at `N=q+3`. Representation and reversible mutation-measure counterexamples delimit the result: the thresholds are exact consequences of the declared genotype-policy map, not representation-free biological laws.

**Keywords:** population genetics; genotype–phenotype map; mutation–selection balance; stationary distribution; weakest-link epistasis; genotype multiplicity

## 1. Introduction

Natural selection ranks genotypes by fitness, but stationary occupancy can also depend on how many genotypes realize each phenotype and on the neutral mutation measure over those genotypes. This distinction is explicit in weak-mutation population genetics: reversible mutation–selection stationary distributions combine selective weighting with a neutral measure (Sella & Hirsh 2005), and sequence multiplicity can enter equilibrium inference directly (Riedel et al. 2015). Related effects occur in neutral-network and quasispecies models, where genotype–phenotype redundancy can shift evolutionary thresholds (Bull et al. 2005; Takeuchi et al. 2005). We therefore do not claim novelty for the broad principles that multiplicity can oppose selection or that representation can move a threshold.

A second established ingredient is weakest-link fitness. When performance requires several components, the least adequate component can limit the whole system; recent population-genetic work treats such minimum-type fitness maps explicitly (Labourel et al. 2026). Our use of a minimum across routing branches is likewise not a novelty claim.

We instead ask a finite representation-specific question. Consider `k` heritable routing coordinates, each taking values `0,...,q`, with overall gain determined by the weakest coordinate. The fully adapted phenotype is represented by one genotype-policy state, whereas lower-gain phenotypes can be represented by many. Under a standard weak-mutation stationary tilt, when does the full-gain class become the **largest aggregate class**, and when does it carry **at least half of stationary probability**? These are distinct population-level questions: the most probable individual genotype, the largest aggregate phenotype class, and a stationary majority need not coincide.

The routing representation is tractable enough to answer both questions exactly. Its layer multiplicities obey a global bound controlled by the adjacent suboptimal layer. That bound yields an exact aggregate-mode threshold and a distinct stationary-majority threshold, which translate into adjacent population-size transitions in a canonical Moran family (Figs. 1–2). We then show that changing either the genotype-policy representation or the reversible neutral mutation measure changes the stationary conclusion (Fig. 3). The resulting theorem is therefore conditional by construction: exactness comes from specifying representation and mutation measure, not from a universal selection threshold.

## 2. Model and population-genetic bridge

Let `q>=1` be the maximum gain level and `k>=1` the number of routing branches. The genotype-policy space is

`X_{q,k}={0,1,...,q}^k`,

with state `x=(x_1,...,x_k)` and routing gain

`g(x)=min_i x_i`.

Thus `g(x)` lies in `{0,...,q}`, and the full-gain class contains only `x*=(q,...,q)`. For a stationary distribution `pi`, let

`Pi_r=sum_{x:g(x)=r} pi(x)`

be the aggregate stationary mass of gain layer `r`. A layer is **aggregate-modal** when its mass is maximal among gain layers; full gain is a **stationary majority** when `Pi_q>=1/2`.

We use an established origin-fixation bridge rather than introducing a new population process. Let fitness be `F(x)=a^{g(x)}` with `a>=1`. For a haploid Moran process of population size `N>=2`, reciprocal fixation probabilities imply the standard reversible stationary weighting (Sella & Hirsh 2005)

`pi(x) proportional to mu(x) a^((N-1)g(x))`,

where `mu(x)` is the stationary measure of the neutral mutation process. Write

`theta=a^(N-1)`.

Under the symmetric genotype-level neutral measure used in the main theorems, every genotype at gain `r` has unnormalized weight `theta^r`; hence aggregate layer weight is

`W_r=D_r theta^r`,

where `D_r` is the number of states at gain `r`. Moran fixation probabilities and this reversible stationary law are prior art; the routing-specific argument begins with `D_r`.

## 3. Exact routing-layer multiplicity

### Theorem 1. Routing-layer multiplicity

For `r=0,...,q`,

`D_r=(q-r+1)^k-(q-r)^k`.

Equivalently, if `s=q-r` is distance below full gain,

`A_s=D_{q-s}=(s+1)^k-s^k`.

**Proof.** A state has `g(x)>=r` exactly when every coordinate lies in `{r,...,q}`, giving `(q-r+1)^k` states. Subtracting the `(q-r)^k` states with `g(x)>=r+1` gives the result. `□`

The full-gain layer has `A_0=1`; the adjacent layer has `A_1=2^k-1`. For `q=2,k=3`, the layer multiplicities are `(D_0,D_1,D_2)=(19,7,1)` (Fig. 1).

## 4. One adjacent obstruction controls all lower layers

Define

`T_k=2^k-1`.

### Theorem 2. Global degeneracy bound

For every integer `s>=1`,

`A_s <= T_k^s`.

If `k>=2`, equality occurs only for `s=1`.

**Proof.** A state counted by `A_s` is a vector in `{0,...,s}^k` with minimum coordinate zero. For `j=1,...,s`, define `S_j={i:x_i<j}`. These sets are nonempty and nested, `S_1 subseteq ... subseteq S_s`, and the nested sequence uniquely reconstructs `x`. Thus `A_s` counts nested length-`s` sequences of nonempty subsets of `k` branch labels. There are `T_k` nonempty subsets; dropping the nesting constraint gives `T_k^s` sequences. Equality holds at `s=1`; for `k>=2,s>=2`, nonnested sequences exist, so the inequality is strict. `□`

The key consequence is global: the multiplicity of the adjacent suboptimal class bounds every more distant class strongly enough to determine the first occupancy transition.

## 5. Two stationary occupancy transitions

For the layer `s` steps below full gain,

`W_{q-s}/W_q=A_s/theta^s`.

### Theorem 3. Sharp aggregate-mode transition

Assume `k>=2`.

- If `theta<T_k`, full gain is not aggregate-modal.
- If `theta=T_k`, exactly the full and adjacent layers tie for maximal aggregate weight.
- If `theta>T_k`, full gain is uniquely aggregate-modal.

**Proof.** For `s=1`, the weight ratio is `T_k/theta`, giving the lower-bound obstruction and equality at `theta=T_k`. At equality, Theorem 2 gives `A_s/T_k^s<1` for every `s>=2`; above the threshold, `A_s/theta^s <= (T_k/theta)^s<1` for all `s>=1`. `□`

This is an aggregate-class transition, not a per-genotype mode switch. For `theta>1`, the full-gain genotype already has greater individual weight than every lower-gain genotype.

The normalized full-gain mass is

`P_full(theta)=1/[1+sum_{s=1}^q A_s theta^{-s}]`.

### Theorem 4. Stationary-majority boundary

There is a unique positive threshold `theta_1/2(q,k)` at which `P_full=1/2`, equivalently

`theta^q=sum_{s=1}^q A_s theta^(q-s)`.

For `q=1`, `theta_1/2=T_k`. For every `q>=2`,

`T_k < theta_1/2(q,k) < 2T_k`.

**Proof.** The lower/full mass ratio `sum_s A_s theta^{-s}` decreases strictly from infinity to zero. At `theta=T_k`, its adjacent term alone equals one, and for `q>=2` additional positive terms make `P_full<1/2`. At `theta=2T_k`, Theorem 2 gives a lower/full ratio at most `sum_{s=1}^q 2^{-s}<1`, so `P_full>1/2`. `□`

Theorems 3 and 4 therefore define two ordered stationary transitions (Fig. 2). For `q=2,k=3`, `T_3=7`. At `theta=7`, weights are `(19,49,49)` and `P_full=49/117≈0.419`: full gain ties for the aggregate mode but remains a minority. The half-mass equation is `theta^2=7theta+19`, with positive root

`theta_1/2=(7+5sqrt(5))/2≈9.09`.

Under the Moran bridge `theta=a^(N-1)`, canonical routing `k=q+1` with `a=2` gives a particularly simple population-size separation. Because `2^q<T_k<2^(q+1)`, unique aggregate modality first occurs at

`N=q+2`.

For every `q>=2`, the majority bound gives the exact next-step result

`N_majority=q+3`.

Thus becoming the largest aggregate class and carrying most stationary probability are distinct finite-population events.

## 6. Scope controls: representation and mutation measure

The thresholds above are properties of the declared branch-product representation, not of gain values alone. Compare canonical branch-product routing `X_prod={0,...,q}^{q+1}` with a compressed representation `X_chain={0,...,q}` containing one genotype per gain level. Give both representations the same gain values and phenotype-level fitness schedule. At `q=2,theta=2`, the compressed representation has weights `(1,2,4)` and `P_full=4/7>1/2`, whereas branch-product routing has multiplicities `(19,7,1)`, weights `(19,14,4)`, and `P_full=4/37`. Full gain is therefore a unique mode and majority in one representation but nonmodal and far from majority in the other (Fig. 3).

The main theorems also assume a symmetric genotype-level neutral measure. Under a general reversible neutral measure,

`pi(x) proportional to mu(x) theta^{g(x)}`,

so raw genotype counts need not equal the relevant abundance factor. Even fixing mutation support does not identify occupancy. On the path `0<->1<->...<->q`, fix any positive `theta` and any strictly positive target distribution `p`. Choosing `mu_r proportional to p_r theta^{-r}` and a connected reversible nearest-neighbor proposal kernel with stationary measure `mu` gives selected stationary law `pi_r proportional to p_r`. At `q=2,theta=2`, the same support can therefore yield, for example, `(1/10,1/10,4/5)` or `(9/20,9/20,1/10)` (Fig. 3).

These controls are part of the result rather than generic limitations. The exact thresholds require both the branch-product representation and the symmetric neutral measure. A biological application must independently justify those ingredients rather than infer them from phenotype-level gain or fitness values.

## 7. Discussion

The broad evolutionary lesson that genotype abundance can oppose selection is established (Riedel et al. 2015), as are representation-dependent thresholds in quasispecies and phenotype-level models (Bull et al. 2005; Takeuchi et al. 2005) and minimum-type fitness maps (Labourel et al. 2026). The contribution here is the exact composition of these ingredients for one finite routing representation.

The representation creates a multiplicity hierarchy in which the adjacent suboptimal class controls every lower class. This turns a qualitative selection–multiplicity tradeoff into two different stationary statements. At `T_k=2^k-1`, full gain becomes the largest aggregate class; only at the larger `theta_1/2` does it contain most stationary probability. The distinction matters because per-genotype fitness ranking, aggregate modality, and stationary majority answer different population-level questions. In the canonical Moran family, their separation is visible as the exact `N=q+2` versus `N=q+3` transition.

The scope controls show why this result should not be generalized into a representation-free law. Compressing the genotype-policy map removes the multiplicity burden, while changing a reversible neutral mutation measure can reverse occupancy even on fixed mutation support. The relevant abundance factor under mutation bias is neutral layer mass, not raw genotype count. Explicit genotype–phenotype representation and mutation structure are therefore causal inputs to stationary prediction.

For biological routing systems, that requirement is substantial. A regulatory, neural, developmental, or behavioral system may perform state-dependent routing without possessing the discrete branch-product genotype space, coordinate-local mutational structure, or symmetric neutral measure assumed here. The model is consequently a conditional population-genetic representation whose biological use requires independent qualification.

The practical conclusion is narrow: phenotype-level selection coefficients do not determine stationary phenotype occupancy without a representation and mutation model. When those ingredients are explicit, their multiplicity structure may sometimes be solved exactly. In the present routing representation, one adjacent-layer obstruction determines the transition to aggregate modality and tightly brackets the later transition to stationary majority. Exactness comes from specifying the representation, not from discovering a universal threshold.

## References

Bull JJ, Meyers LA, Lachmann M. 2005. Quasispecies Made Simple. *PLoS Computational Biology* 1(6):e61. DOI `10.1371/journal.pcbi.0010061`.

Labourel FJF, Bansept F, McCandlish DM. 2026. *Weakest link epistasis and the geometry of genetic load*. bioRxiv v2. DOI `10.64898/2025.12.08.693057`.

Riedel N, Khatri BS, Lässig M, Berg J. 2015. Multiple-Line Inference of Selection on Quantitative Traits. *Genetics* 201:305–322. DOI `10.1534/genetics.115.178988`.

Sella G, Hirsh AE. 2005. The application of statistical physics to evolutionary biology. *Proceedings of the National Academy of Sciences USA* 102(27):9541–9546. DOI `10.1073/pnas.0501865102`.

Takeuchi N, Poorthuis PH, Hogeweg P. 2005. Phenotypic error threshold; additivity and epistasis in RNA evolution. *BMC Evolutionary Biology* 5:9. DOI `10.1186/1471-2148-5-9`.
