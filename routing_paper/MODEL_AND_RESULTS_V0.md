# Model and Results v0

## 1. Finite routing representation

Let `q>=1` be the maximum routing-gain level and `k>=1` the number of routing branches. We define the finite genotype-policy representation

`X_{q,k}={0,1,...,q}^k`.

A genotype-policy state is

`x=(x_1,...,x_k)`.

Overall routing gain is determined by the weakest branch,

`g(x)=min_i x_i`.

Thus `g(x)` takes values in `{0,...,q}`. The full-gain class `g=q` contains only

`x*=(q,...,q)`.

The central population-level object in this paper is not the probability of this individual genotype but the **aggregate stationary mass of a gain layer**.

For any stationary distribution `pi` on `X_{q,k}`, define

`Pi_r = sum_{x:g(x)=r} pi(x)`.

A gain layer is aggregate-modal if its `Pi_r` is maximal among `r=0,...,q`.

## 2. Established origin-fixation weighting

We use a standard weak-mutation origin-fixation bridge rather than introducing a new population-genetic process.

Let genotype fitness depend only on routing gain through a multiplicative step

`F(x)=a^{g(x)}`,

with `a>=1`. For a haploid Moran process of population size `N>=2`, the fixation-probability ratio for reciprocal fitness changes is

`rho(R)/rho(1/R)=R^(N-1)`.

Therefore, under a reversible neutral mutation process with stationary measure `mu(x)`, the selected origin-fixation stationary law has the standard form

`pi(x) proportional to mu(x) a^((N-1)g(x))`.

Define the per-gain stationary tilt

`theta=a^(N-1)`.

Then

`pi(x) proportional to mu(x) theta^{g(x)}`.

The main theorems assume the symmetric genotype-level neutral measure, so `mu(x)` is constant over `X_{q,k}`. In that case each genotype in gain layer `r` has the same unnormalized weight `theta^r`, and aggregate layer weight is

`W_r = D_r theta^r`,

where `D_r` is the number of genotypes with gain `r`.

The Moran fixation identity, reversibility argument, and neutral-measure weighting are established prior art. The new work begins with the exact routing-specific multiplicities `D_r`.

---

# Result 1 — exact routing-layer multiplicity

## Theorem 1

For `r=0,...,q`, the number of genotypes with routing gain exactly `r` is

`D_r=(q-r+1)^k-(q-r)^k`.

Equivalently, if

`s=q-r`

is the distance in gain levels below full gain, then

`A_s := D_{q-s} = (s+1)^k-s^k`.

### Proof

A genotype has `g(x)>=r` exactly when every coordinate lies in

`{r,r+1,...,q}`,

which contains `q-r+1` values. Hence

`#{x:g(x)>=r}=(q-r+1)^k`.

Similarly,

`#{x:g(x)>=r+1}=(q-r)^k`.

Subtracting gives

`D_r=(q-r+1)^k-(q-r)^k`.

Replacing `q-r` by `s` gives the equivalent expression for `A_s`. QED.

## Immediate consequences

The full-gain layer has

`A_0=1`.

The adjacent layer has

`A_1=2^k-1`.

For the running example `q=2,k=3`,

`(D_0,D_1,D_2)=(19,7,1)`.

Thus the representation contains a unique maximally adapted genotype but seven genotypes one gain step below it.

---

# Result 2 — a global bound from nested subset chains

The adjacent-layer multiplicity will turn out to control every lower layer.

Define

`T_k=2^k-1`.

## Theorem 2

For every integer `s>=1`,

`A_s <= T_k^s`.

If `k>=2`, equality occurs only at `s=1`. Thus for every `s>=2`,

`A_s < T_k^s`.

### Proof

Consider a vector

`x in {0,...,s}^k`

with minimum coordinate zero. Such vectors are counted by

`A_s=(s+1)^k-s^k`.

For each level `j=1,...,s`, define

`S_j={i:x_i<j}`.

Because at least one coordinate equals zero, every `S_j` is nonempty. Moreover,

`S_1 subseteq S_2 subseteq ... subseteq S_s`.

Conversely, a nested sequence of nonempty subsets uniquely reconstructs `x`: coordinate `i` is the number of initial levels for which `i` is absent before it enters the nested sequence, equivalently its threshold of membership. Hence the vectors counted by `A_s` are in bijection with nested length-`s` sequences of nonempty subsets of `{1,...,k}`.

There are `2^k-1=T_k` nonempty subsets of `{1,...,k}`. If the nesting condition is dropped, there are exactly

`T_k^s`

arbitrary length-`s` sequences. Therefore

`A_s<=T_k^s`.

At `s=1`, there is no between-level nesting restriction, so equality holds. If `k>=2` and `s>=2`, nonnested sequences exist, for example a sequence beginning with `{1},{2}`. Therefore the nested sequences form a strict subset of all sequences and

`A_s<T_k^s`.

QED.

## Interpretation

This theorem is stronger than an adjacent-layer comparison. It states that once the adjacent multiplicity `T_k` is known, every layer `s` gain steps below the optimum is bounded by the `s`th power of the same constant. That reduction is what makes the stationary transition exact.

---

# Result 3 — sharp aggregate-layer modality transition

Under the symmetric stationary tilt, layer `r` has unnormalized aggregate weight

`W_r=D_r theta^r`.

Relative to the full-gain layer,

`W_{q-s}/W_q = A_s/theta^s`.

## Theorem 3

Assume `k>=2`.

### Below threshold

If

`theta<T_k`,

then

`W_{q-1}/W_q=T_k/theta>1`.

Hence the full-gain layer is not aggregate-modal.

### At threshold

If

`theta=T_k`,

then

`W_{q-1}=W_q`.

For every `s>=2`, Theorem 2 gives

`W_{q-s}/W_q=A_s/T_k^s<1`.

Therefore exactly two layers attain maximal aggregate weight:

`{q-1,q}`.

### Above threshold

If

`theta>T_k`,

then for every `s>=1`,

`W_{q-s}/W_q = A_s/theta^s <= (T_k/theta)^s < 1`.

Therefore the full-gain layer is uniquely aggregate-modal.

Combining the three cases gives the exact trichotomy

`theta<T_k`  -> full layer nonmodal,

`theta=T_k`  -> exact `{q-1,q}` tie,

`theta>T_k`  -> full layer uniquely modal,

with

`T_k=2^k-1`.

QED.

## Individual-genotype versus aggregate-layer modality

The threshold above does not describe when the individual genotype `(q,...,q)` becomes the most probable genotype. Under the symmetric tilt, every genotype at gain `r` has per-genotype weight `theta^r`. Thus for every `theta>1`, the full-gain genotype already has strictly greater per-genotype weight than every lower-gain genotype.

The factor `2^k-1` appears only because the stationary weights of all genotypes in each gain layer are summed before comparing layers.

---

# Corollary — population-size threshold under the Moran bridge

Under the multiplicative fitness step `a>1`,

`theta=a^(N-1)`.

Therefore, for `k>=2`, the full-gain layer is aggregate-modal if and only if

`a^(N-1)>=2^k-1`.

It is uniquely aggregate-modal if and only if

`a^(N-1)>2^k-1`.

The smallest population size satisfying the weak inequality and the smallest population size satisfying the strict inequality need not coincide when `2^k-1` is an exact power of `a`.

For the canonical routing architecture

`k=q+1`,

and `a=2`,

`2^q < 2^(q+1)-1 < 2^(q+1)`.

Hence both the first modal and first uniquely modal population sizes are

`N=q+2`.

This corollary translates the finite representation theorem into one familiar population parameter; it does not make the underlying Moran machinery a contribution of the paper.

---

# Scope Result 1 — the threshold depends on representation

The gain coordinate and fitness schedule do not identify the aggregate-mode threshold.

Consider the canonical branch-product representation

`X_prod={0,...,q}^{q+1}`,

with the same gain map `g=min` and tilt `theta`. Its full-layer threshold is

`theta_prod=2^(q+1)-1`.

Now consider a compressed representation

`X_chain={0,...,q}`,

with one genotype per gain level and the same phenotype-level fitness schedule. Its aggregate layer weights are simply

`1, theta, ..., theta^q`.

Thus the full-gain layer is aggregate-modal for `theta>=1` and uniquely modal for `theta>1`.

For every

`1<theta<2^(q+1)-1`,

the full-gain layer is uniquely modal under the compressed representation but nonmodal under the branch-product representation.

## Canonical contradiction witness

At `q=2,theta=2`:

compressed representation:

`weights=(1,2,4)`, `P(full)=4/7`;

branch-product representation:

`D=(19,7,1)`, `weights=(19,14,4)`, `P(full)=4/37`.

The gain phenotypes and fitness schedule are identical. The stationary conclusion changes because the genotype-policy representation changes.

This result is used as a claim boundary, not as a claim to have discovered representation-dependent evolvability in general.

---

# Scope Result 2 — fixed mutation support is still insufficient

The main theorem assumes a symmetric genotype-level neutral measure. Under a general reversible neutral mutation measure `mu`,

`pi(x) proportional to mu(x) theta^{g(x)}`.

Consequently raw genotype counts need not determine layer mass.

A stronger nonidentifiability holds even after mutation support is fixed. Consider the gain path

`0 <-> 1 <-> ... <-> q`

and fix any `theta>0`. For any strictly positive target selected stationary distribution

`p=(p_0,...,p_q)`,

choose

`mu_r proportional to p_r theta^(-r)`.

A connected reversible nearest-neighbor proposal kernel can be constructed with stationary measure `mu`; under selection, its stationary distribution then satisfies

`pi_r proportional to mu_r theta^r proportional to p_r`.

Thus the same gain levels, the same fitness schedule, and the same local support graph can support arbitrarily different positive stationary occupancies if the reversible mutation probabilities are changed.

For `q=2,theta=2`, the frozen exact witnesses include selected stationary distributions

`(1/10,1/10,4/5)`

and

`(9/20,9/20,1/10)`

on the same path support.

This scope result explains precisely why `theta_c=2^k-1` must be stated as a symmetric branch-product theorem rather than a universal mutation-selection law.

---

# Result hierarchy for the final paper

Theorems 1–3 are the mathematical contribution.

The Moran population-size statement is a corollary through established theory.

The representation comparison and mutation-measure construction are scope controls. They prevent overgeneralization but should not compete with the central theorem sequence in title, abstract, or figure allocation.

## Hard stop

Do not append neutral-plateau waiting-time, mesoscopic acquisition, absolute-rate-scale, or downstream population-process results to this section. None is needed to prove or interpret the sharp aggregate-layer threshold.