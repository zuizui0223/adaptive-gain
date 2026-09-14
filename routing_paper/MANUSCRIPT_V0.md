# Exact occupancy thresholds in finite routing representations

## Abstract

A phenotype can be optimal at the level of individual genotypes yet remain rare after stationary probability is aggregated over all genotypes that realize each phenotype. This general tension between selection and genotype multiplicity is well established, as is the fact that genotype–phenotype redundancy can alter evolutionary thresholds. Here we derive an exact version for a finite routing representation. We consider genotype-policy states `x in {0,...,q}^k` with routing gain set by the weakest branch, `g(x)=min_i x_i`. The number of genotypes at gain `r` is

`D_r=(q-r+1)^k-(q-r)^k`.

Writing `A_s=(s+1)^k-s^k` for the layer `s` steps below full gain, we show that

`A_s <= (2^k-1)^s`,

with equality only for the adjacent layer when `k>=2`. Under a symmetric stationary tilt `theta` per gain step, aggregate layer weight is `D_r theta^r`. The bound yields an exact trichotomy: below `T_k=2^k-1` the full-gain layer is nonmodal, at `T_k` it ties exactly with the adjacent layer, and above `T_k` it is uniquely modal. Aggregate modality is weaker than stationary majority. The full-gain mass has a unique half-mass threshold `theta_1/2(q,k)` satisfying, for `q>=2`,

`T_k < theta_1/2(q,k) < 2T_k`.

Under the standard Moran origin-fixation tilt `theta=a^(N-1)`, canonical routing `k=q+1` with `a=2` becomes uniquely modal at `N=q+2` but a stationary majority only at `N=q+3` for `q>=2`. Representation and reversible mutation-measure counterexamples show that these thresholds are conditional on the declared genotype-policy map. Thus an explicit finite representation converts a qualitative selection–multiplicity tradeoff into two exact, assumption-explicit stationary occupancy transitions.

## 1. Introduction

Natural selection orders genotypes by fitness, but population-level occupancy is not determined by that ordering alone. A high-fitness phenotype may be realized by few genotypes, whereas a slightly lower-fitness phenotype may be represented by many more. In weak-mutation settings, this distinction appears through the neutral mutation measure that multiplies selective weighting in the stationary distribution. Sequence multiplicity can therefore enter equilibrium population-genetic statistics explicitly. Riedel et al. (2015), for example, parameterized the relative number of sequence variants representing alternative trait states and combined that multiplicity with selection in low-mutation inference. Related abundance–selection effects arise in free-fitness formulations, neutral-network theory, and survival-of-the-flattest phenomena.

Representation-dependent thresholds are also not new in general. Quasispecies theory shows that the breadth and connectivity of neutral networks can change the competitiveness of phenotypes and shift error thresholds. Phenotypic error-threshold theory similarly aggregates redundant genotypes into phenotype classes before asking whether the focal phenotype persists. These models operate in a different mutation regime from the weak-mutation origin-fixation process used below, but they establish the broad principle that genotype–phenotype redundancy can alter evolutionary thresholds. We therefore do not claim novelty for the ideas that multiplicity can oppose selection or that representation can move a threshold.

A second established ingredient is limiting-component or weakest-link fitness. Many systems require several components to function, so total performance can be controlled by the least adequate component. Limiting-factor models are longstanding, and recent population-genetic work formalizes weakest-link epistasis with organismal fitness determined by the minimum of component fitnesses. Our use of a minimum across routing branches is consequently not itself a novelty claim.

The question here is narrower. We study a finite routing representation in which a genotype-policy state has `k` branch coordinates, each taking integer values from `0` to `q`, and overall gain is determined by the weakest branch:

`X_{q,k}={0,...,q}^k`,

`g(x)=min_i x_i`.

The full-gain class contains only the genotype `(q,...,q)`, whereas lower gain classes may contain many genotypes. This representation generates a discrete multiplicity hierarchy before population-genetic dynamics are specified. Once a standard stationary selection tilt is applied, that hierarchy raises two distinct questions. First, how large must the selective tilt be before the full-gain class becomes the **largest aggregate gain class**? Second, how much stronger must selection be before full gain contains **at least half of stationary probability**? These questions distinguish three objects that are often blurred by informal language: the most probable individual genotype, the largest phenotype or gain class, and a stationary majority.

We obtain exact answers because the routing representation has a particularly tractable layer structure. The number of genotypes at gain `r` is

`D_r=(q-r+1)^k-(q-r)^k`.

If `s=q-r` is distance below full gain, the corresponding multiplicity is

`A_s=(s+1)^k-s^k`.

The adjacent layer has `A_1=2^k-1` genotypes. More importantly, that adjacent-layer multiplicity controls every lower layer: for all `s>=1`,

`A_s <= (2^k-1)^s`,

with strict inequality when `k>=2` and `s>=2`. The proof identifies layer states with nested sequences of nonempty subsets of branch labels and then drops the nesting constraint. This reduction makes it possible to compare the full-gain layer with every suboptimal layer simultaneously.

Combining these routing-specific multiplicities with an established reversible weak-mutation stationary law yields the first occupancy threshold. Let `theta` denote the stationary tilt per gain step. Aggregate layer weight is then proportional to

`W_r=D_r theta^r`.

With `T_k=2^k-1`, the full-gain layer is nonmodal for `theta<T_k`; at `theta=T_k`, exactly the full and adjacent layers tie; and for `theta>T_k`, full gain is uniquely aggregate-modal. This threshold is not a change in the most probable individual genotype. Under symmetric weighting, the full-gain genotype already has greater per-genotype weight than every lower-gain genotype whenever `theta>1`. The factor `2^k-1` appears only after genotype probabilities are aggregated within gain classes.

The second threshold is stronger. Full-gain stationary mass is

`P_full(theta)=1/[1+sum_{s=1}^q A_s theta^{-s}]`.

It crosses one half at a unique positive value `theta_1/2(q,k)`. For `q=1`, this majority threshold equals `T_k`; for every `q>=2`,

`T_k < theta_1/2(q,k) < 2T_k`.

Thus a finite interval exists in which full gain is already the largest gain class but most stationary probability still lies outside it.

To connect the representation theorem to a familiar population parameter, we use the standard haploid Moran origin-fixation result. If a gain step multiplies fitness by `a`, then the stationary tilt is `theta=a^(N-1)` for population size `N`. In the canonical routing construction `k=q+1`, taking `a=2` yields an especially simple separation: full gain first becomes the unique aggregate mode at `N=q+2`, but for every `q>=2` it first becomes a stationary majority at `N=q+3`.

These thresholds are exact because the representation and mutation measure are explicit, not because the results are universal. We therefore include two scope controls in the main argument. First, keeping the same gain levels and phenotype-level fitness while replacing the branch-product representation with a compressed chain changes the stationary conclusion. Second, even after mutation support is fixed, changing a reversible neutral mutation measure can generate arbitrarily different positive stationary occupancies. Representation and mutation measure are therefore causal model inputs rather than quantities identified by gain values alone.

The contribution is consequently an exact finite-representation result. The isolated counting identity, weakest-link map, and stationary population-genetic weighting are not new. What the routing construction supplies is a specific multiplicity hierarchy in which one adjacent-layer obstruction controls all suboptimal layers and, through that control, yields linked exact statements about aggregate modality and stationary majority.

## 2. Model and established population-genetic bridge

### 2.1 Finite routing genotype-policy space

Let `q>=1` be the maximum gain level and `k>=1` the number of routing branches. Define

`X_{q,k}={0,1,...,q}^k`.

A state is a vector

`x=(x_1,...,x_k)`.

Its routing gain is

`g(x)=min_i x_i`,

so `g(x)` takes values in `{0,...,q}`. The full-gain class `g=q` contains the single state

`x*=(q,...,q)`.

For a stationary distribution `pi` on `X_{q,k}`, define aggregate gain-layer mass

`Pi_r=sum_{x:g(x)=r} pi(x)`.

We call layer `r` aggregate-modal when its mass is maximal among the gain layers. We call full gain a stationary majority when `Pi_q>=1/2`.

### 2.2 Standard weak-mutation stationary weighting

We use an established origin-fixation bridge rather than introducing a new population process. Let genotype fitness depend on routing gain through

`F(x)=a^{g(x)}`,

with `a>=1`. For a haploid Moran process of population size `N>=2`, reciprocal mutant/resident fitness ratios satisfy

`rho(R)/rho(1/R)=R^(N-1)`.

Under a reversible neutral mutation process with stationary measure `mu(x)`, the selected origin-fixation stationary law therefore has the standard form

`pi(x) proportional to mu(x) a^((N-1)g(x))`.

Write

`theta=a^(N-1)`.

Then

`pi(x) proportional to mu(x) theta^{g(x)}`.

The main theorems use the symmetric genotype-level neutral measure, for which `mu(x)` is constant. Every genotype at gain `r` then has the same unnormalized weight `theta^r`, and aggregate layer weight is

`W_r=D_r theta^r`,

where `D_r` is the number of states with gain `r`.

Moran fixation probabilities, the reciprocal fixation-ratio identity, reversible stationary weighting, and the neutral-measure factor are prior art. The routing-specific results begin with the layer multiplicities.

## 3. Exact routing-layer multiplicity

### Theorem 1 — Routing-layer multiplicity

For `r=0,...,q`,

`D_r=(q-r+1)^k-(q-r)^k`.

Equivalently, if `s=q-r` denotes the number of gain levels below full gain, define

`A_s=D_{q-s}=(s+1)^k-s^k`.

#### Proof

A state has `g(x)>=r` exactly when every coordinate lies in `{r,r+1,...,q}`, a set of `q-r+1` values. Hence

`#{x:g(x)>=r}=(q-r+1)^k`.

Likewise,

`#{x:g(x)>=r+1}=(q-r)^k`.

Subtracting gives the formula for `D_r`. Replacing `q-r` by `s` gives the expression for `A_s`. `□`

The full-gain layer has `A_0=1`. The adjacent layer has

`A_1=2^k-1`.

For the running example `q=2,k=3`,

`(D_0,D_1,D_2)=(19,7,1)`.

Thus a unique fully adapted state is adjacent, in phenotype space, to a gain class represented by seven states.

## 4. A global bound from nested subset chains

Define

`T_k=2^k-1`.

### Theorem 2 — Global degeneracy bound

For every integer `s>=1`,

`A_s <= T_k^s`.

If `k>=2`, equality occurs only at `s=1`; for every `s>=2`,

`A_s < T_k^s`.

#### Proof

A state counted by `A_s` can be written as a vector `x in {0,...,s}^k` with minimum coordinate zero. For each `j=1,...,s`, define

`S_j={i:x_i<j}`.

Because at least one coordinate equals zero, each `S_j` is nonempty. Moreover,

`S_1 subseteq S_2 subseteq ... subseteq S_s`.

Conversely, such a nested sequence uniquely determines the coordinate at which each branch enters the sequence, and therefore reconstructs `x`. Hence `A_s` counts nested length-`s` sequences of nonempty subsets of `{1,...,k}`.

There are `2^k-1=T_k` nonempty subsets. If nesting is removed, there are exactly `T_k^s` arbitrary sequences, proving the non-strict bound. At `s=1`, no between-level nesting restriction remains, so equality holds. If `k>=2` and `s>=2`, nonnested sequences exist, so the inequality is strict. `□`

The theorem is useful because the adjacent-layer constant controls not just the first competitor but every lower gain class simultaneously.

## 5. Two stationary occupancy transitions

### 5.1 Aggregate-layer modality

Under symmetric tilt,

`W_r=D_r theta^r`.

For the layer `s` steps below full gain,

`W_{q-s}/W_q=A_s/theta^s`.

### Theorem 3 — Sharp aggregate-mode transition

Assume `k>=2`.

- If `theta<T_k`, the full-gain layer is not aggregate-modal.
- If `theta=T_k`, exactly the layers `q-1` and `q` tie for maximal aggregate weight.
- If `theta>T_k`, the full-gain layer is uniquely aggregate-modal.

#### Proof

For `s=1`,

`W_{q-1}/W_q=T_k/theta`,

which proves nonmodality below the threshold and equality with the adjacent layer at the threshold. At `theta=T_k`, Theorem 2 gives

`W_{q-s}/W_q=A_s/T_k^s<1`

for all `s>=2`, so no additional layer ties. Above the threshold,

`W_{q-s}/W_q <= (T_k/theta)^s<1`

for every `s>=1`. `□`

The threshold concerns aggregated gain classes. It is not a per-genotype mode switch: for `theta>1`, the full-gain genotype has strictly larger individual weight than every lower-gain genotype before aggregation.

### 5.2 Stationary majority

The normalized full-gain stationary mass is

`P_full(theta)=W_q/sum_{r=0}^q W_r`

and therefore

`P_full(theta)=1/[1+sum_{s=1}^q A_s theta^{-s}]`.

This function is strictly increasing for positive `theta`.

### Theorem 4 — Stationary-majority boundary

There is a unique positive threshold `theta_1/2(q,k)` at which `P_full=1/2`. It is the unique positive solution of

`theta^q=sum_{s=1}^q A_s theta^(q-s)`.

For `q=1`,

`theta_1/2=T_k`.

For every `q>=2`,

`T_k < theta_1/2(q,k) < 2T_k`.

#### Proof

The half-mass condition is equivalent to

`sum_{s=1}^q A_s theta^{-s}=1`.

The left-hand side decreases strictly from infinity to zero as positive `theta` increases, establishing existence and uniqueness.

At `theta=T_k`, the adjacent term is exactly one:

`A_1/T_k=1`.

For `q>=2`, additional terms are positive, so the total lower/full ratio exceeds one and `P_full<1/2`. Thus `theta_1/2>T_k`.

At `theta=2T_k`, Theorem 2 gives

`sum_{s=1}^q A_s(2T_k)^{-s}`
`<=sum_{s=1}^q 2^{-s}`
`<1`.

Hence `P_full>1/2` there and `theta_1/2<2T_k`. `□`

Theorems 3 and 4 define two ordered transitions. Full gain can already be the largest aggregate class while remaining a minority of the stationary distribution.

### 5.3 Canonical running example

For `q=2,k=3`,

`D=(19,7,1)`

and `T_3=7`.

At the aggregate-mode threshold,

`theta=7`,

`W=(19,49,49)`

and

`P_full=49/117≈0.419`.

The full-gain class is tied for the aggregate mode but is not a majority.

The half-mass equation is

`theta^2=7theta+19`,

with positive solution

`theta_1/2=(7+5sqrt(5))/2≈9.09`.

Exact rational audit points give

`P_full(9)=81/163<1/2`,

`P_full(10)=100/189>1/2`.

### 5.4 Moran population-size corollary

Under the multiplicative fitness step `a>1`, the standard Moran bridge gives

`theta=a^(N-1)`.

Hence the full-gain class is aggregate-modal exactly when

`a^(N-1)>=T_k`,

uniquely aggregate-modal when the inequality is strict, and a stationary majority when

`a^(N-1)>=theta_1/2(q,k)`.

For canonical routing `k=q+1` and `a=2`,

`2^q<T_k=2^(q+1)-1<2^(q+1)`.

Therefore unique aggregate modality first occurs at

`N=q+2`.

For every `q>=2`, the majority theorem yields the exact next-step result

`N_majority=q+3`.

The case `q=1` is the boundary exception, with majority already at `N=3=q+2`.

## 6. Representation changes the stationary conclusion

The thresholds above are properties of the declared branch-product representation, not of the gain values alone.

Consider canonical branch-product routing

`X_prod={0,...,q}^{q+1}`

and a compressed representation

`X_chain={0,...,q}`

with one genotype per gain level. Assign both representations the same gain values and the same phenotype-level fitness schedule. Under the compressed representation, aggregate layer weights are simply

`1,theta,...,theta^q`.

Thus full gain is aggregate-modal for `theta>=1` and uniquely modal for `theta>1`.

At `q=2,theta=2`, the contrast is exact:

- compressed representation: weights `(1,2,4)`, `P_full=4/7>1/2`;
- branch-product representation: multiplicities `(19,7,1)`, weights `(19,14,4)`, `P_full=4/37`.

The same phenotype-level fitness schedule therefore makes full gain both uniquely modal and a stationary majority in one representation, but nonmodal and far from majority in the other.

This comparison is not offered as a discovery of representation dependence in general. Its role is to show that the routing thresholds are conditional consequences of a specified genotype-policy representation.

## 7. Neutral mutation measure is an additional occupancy input

The main theorems further assume a symmetric genotype-level neutral measure. Under a general reversible neutral mutation measure `mu`, stationary weighting is

`pi(x) proportional to mu(x) theta^{g(x)}`.

Raw genotype counts need not then equal the relevant layer abundance factor.

The limitation persists even after mutation support is fixed. Consider the path

`0 <-> 1 <-> ... <-> q`

with one state per gain. Fix any positive `theta` and any strictly positive target stationary distribution

`p=(p_0,...,p_q)`.

Choose a neutral measure satisfying

`mu_r proportional to p_r theta^{-r}`

and a connected reversible nearest-neighbor proposal kernel with that stationary measure. The selected stationary law is then

`pi_r proportional to mu_r theta^r proportional to p_r`.

Thus fixed gain values, fixed fitness tilt, and fixed mutation support still do not identify stationary occupancy without the neutral mutation measure.

For `q=2,theta=2`, exact constructions on the same gain path produce selected stationary distributions such as

`(1/10,1/10,4/5)`

and

`(9/20,9/20,1/10)`.

Accordingly, raw multiplicity is the relevant abundance factor only under the symmetric neutral-measure assumption used by Theorems 1–4.

## 8. Discussion

The main result is not that genotype abundance can oppose selection. That principle is already established across weak-mutation, neutral-network, and quasispecies theories. Nor is the novelty a minimum-type fitness map. The contribution is that one explicit finite routing representation creates a layer hierarchy simple enough to support exact population-level statements at two different occupancy levels.

The first statement is a mode transition. The adjacent suboptimal layer contains `2^k-1` states, and a nested-chain bound proves that this same number controls all more distant layers. Consequently `T_k=2^k-1` is not merely the point at which the adjacent class is overtaken; it is the exact threshold at which the full-gain class becomes an aggregate mode against the entire lower-layer hierarchy. Equality has a specific structure: for `k>=2`, only the full and adjacent layers tie.

The second statement is a majority transition. Aggregate modality is insufficient to conclude that most stationary probability lies at full gain. At `q=2,k=3`, for example, full gain reaches the mode boundary at `theta=7` with mass only `49/117`. The majority theorem identifies a distinct threshold and places it, for all `q>=2`, strictly between `T_k` and `2T_k`. Thus the same combinatorial hierarchy distinguishes becoming the largest class from containing most of the stationary distribution.

This distinction also clarifies what the Moran population-size corollary means. In canonical routing with a twofold fitness step, the fittest genotype is already individually favored whenever `theta>1`. The gain class becomes the unique aggregate mode only at `N=q+2`, and for `q>=2` becomes a stationary majority at `N=q+3`. These are not universal effective-population-size laws. They are exact translations of one genotype-policy representation through an established finite-population stationary law.

The representation contrast makes the conditionality substantive. Compressing the genotype-policy map to one genotype per gain removes the branch-product multiplicity burden and qualitatively changes occupancy at the same fitness tilt. Quasispecies and phenotype-level threshold theory already establish the broad principle that genotype–phenotype redundancy can change evolutionary thresholds. The present result differs in mutation regime and mathematical object: it gives exact stationary class thresholds for a finite branch-product representation in a reversible weak-mutation setting. That distinction should be preserved rather than inflated into a general novelty claim.

The mutation-measure result imposes a second boundary. Even a specified support graph is insufficient to recover stationary occupancy if reversible proposal weights remain unknown. Under general mutation bias, the relevant quantity is layer neutral mass rather than raw genotype count. A biological application therefore needs more than a plausible weakest-link phenotype. It needs an independently defensible heritable representation and mutation model.

This requirement is especially important for routing interpretations. A regulatory, neural, developmental, or behavioral system may perform state-dependent routing without having genotype space `{0,...,q}^k`, coordinate-local mutations, or a symmetric neutral measure. The formal branch-product representation should therefore be viewed as a model whose biological use requires qualification, not as a hidden assumption that every modular system satisfies.

Several extensions are deliberately excluded. Neutral-plateau acquisition times, mesoscopic approach to a target, absolute mutation-rate scaling, and downstream population processes address accessibility and time rather than the stationary occupancy transitions considered here. Adding them would broaden the mechanism assumptions without strengthening the central result.

The practical modeling lesson is narrow but useful. Phenotype-level selection coefficients do not by themselves determine stationary phenotype occupancy. Once a genotype-policy representation is declared, its multiplicity structure can sometimes be analyzed exactly; in the present routing model, one adjacent-layer obstruction controls both the point at which full gain becomes the largest class and a tight interval containing the point at which it becomes a majority. Equally important, explicit counterexamples show where that conclusion stops. Exactness here comes from specifying representation, not from discovering a representation-free law.

## Working references

- Labourel FJF, Bansept F, McCandlish DM. 2026. *Weakest link epistasis and the geometry of genetic load*. bioRxiv v2. DOI `10.64898/2025.12.08.693057`.
- Riedel N, Khatri BS, Lässig M, Berg J. 2015. Multiple-Line Inference of Selection on Quantitative Traits. *Genetics* 201:305–322. DOI `10.1534/genetics.115.178988`.
- Sella G, Hirsh AE. 2005. The application of statistical physics to evolutionary biology. *PNAS*.
- Takeuchi N, Poorthuis PH, Hogeweg P. 2005. Phenotypic error threshold; additivity and epistasis in RNA evolution. *BMC Evolutionary Biology* 5:9. DOI `10.1186/1471-2148-5-9`.
- Wilke CO. 2005. Quasispecies Made Simple. *PLoS Computational Biology*. DOI `10.1371/journal.pcbi.0010061`.

Reference list remains working rather than submission-final; exact bibliographic completion and citation placement belong to the final source-level review.