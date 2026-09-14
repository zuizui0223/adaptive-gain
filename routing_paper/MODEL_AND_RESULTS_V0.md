# Model and Results v1

## 1. Finite routing representation and occupancy estimands

Let `q>=1` be the maximum routing-gain level and `k>=1` the number of routing branches. The finite genotype-policy representation is

`X_{q,k}={0,1,...,q}^k`,

with state `x=(x_1,...,x_k)` and weakest-branch gain

`g(x)=min_i x_i`.

The full-gain class `g=q` contains only `x*=(q,...,q)`.

For a stationary distribution `pi`, define aggregate gain-layer mass

`Pi_r=sum_{x:g(x)=r} pi(x)`.

We distinguish two population-level summaries:

- **aggregate modality:** `Pi_q=max_r Pi_r`;
- **stationary majority:** `Pi_q>=1/2`.

These are different estimands. The main results characterize both.

## 2. Established origin-fixation weighting

Let genotype fitness depend on gain through `F(x)=a^{g(x)}`, with `a>=1`. For a haploid Moran process of population size `N>=2`, the standard reciprocal fixation ratio is

`rho(R)/rho(1/R)=R^(N-1)`.

Under a reversible neutral mutation process with stationary measure `mu(x)`, established weak-mutation theory gives

`pi(x) proportional to mu(x) a^((N-1)g(x))`.

Define

`theta=a^(N-1)`.

Then

`pi(x) proportional to mu(x) theta^{g(x)}`.

The main routing theorems assume the symmetric genotype-level neutral measure, so each genotype in layer `r` has unnormalized weight `theta^r`. If `D_r` is the number of genotypes at gain `r`, aggregate layer weight is

`W_r=D_r theta^r`.

The fixation identity, reversible stationary law, and neutral-measure factor are prior art. The routing-specific work begins with `D_r`.

---

# Result 1 — exact routing-layer multiplicity

## Theorem 1

For `r=0,...,q`,

`D_r=(q-r+1)^k-(q-r)^k`.

Equivalently, for `s=q-r`,

`A_s:=D_{q-s}=(s+1)^k-s^k`.

### Proof

`g(x)>=r` iff every coordinate lies in `{r,...,q}`, giving `(q-r+1)^k` states. Likewise `g(x)>=r+1` gives `(q-r)^k`. Their difference is the exact gain-`r` count. QED.

The full-gain layer has `A_0=1`; the adjacent layer has

`A_1=2^k-1`.

For `q=2,k=3`,

`(D_0,D_1,D_2)=(19,7,1)`.

---

# Result 2 — one adjacent obstruction controls every lower layer

Define

`T_k=2^k-1`.

## Theorem 2

For every `s>=1`,

`A_s<=T_k^s`.

If `k>=2`, equality occurs only at `s=1`; for every `s>=2`,

`A_s<T_k^s`.

### Proof

For `x in {0,...,s}^k` with `min_i x_i=0`, define

`S_j={i:x_i<j}`, `j=1,...,s`.

The `S_j` are nonempty and nested:

`S_1 subseteq ... subseteq S_s`.

This gives a bijection between states counted by `A_s` and nested length-`s` sequences of nonempty subsets of the `k` branch labels. There are `T_k=2^k-1` nonempty subsets. Dropping nesting yields `T_k^s` arbitrary sequences, proving the bound. At `s=1` nesting imposes no restriction. For `k>=2,s>=2`, nonnested sequences such as `{1},{2}` exist, giving strict inequality. QED.

Theorem 2 is the combinatorial engine: comparison with all lower gain layers reduces to the adjacent-layer constant `T_k`.

---

# Result 3 — exact aggregate-mode transition

Under symmetric tilt,

`W_{q-s}/W_q=A_s/theta^s`.

## Theorem 3

Assume `k>=2`.

- If `theta<T_k`, then `W_{q-1}/W_q=T_k/theta>1`; full gain is not aggregate-modal.
- If `theta=T_k`, then `W_{q-1}=W_q`, while every `s>=2` layer is strictly lighter by Theorem 2. Exactly `{q-1,q}` tie for maximal aggregate weight.
- If `theta>T_k`, then for every `s>=1`,

  `W_{q-s}/W_q <= (T_k/theta)^s < 1`,

  so full gain is uniquely aggregate-modal.

Thus

`theta<T_k` -> full nonmodal,

`theta=T_k` -> exact two-layer tie,

`theta>T_k` -> full uniquely modal.

### Individual genotype versus gain-layer mode

For every `theta>1`, the unique full-gain genotype already has greater **per-genotype** weight than every lower-gain genotype. `T_k` is therefore an aggregate-layer threshold created by multiplicity, not an individual-genotype mode switch.

---

# Result 4 — exact stationary-majority boundary

Aggregate modality does not imply that full gain contains most stationary probability.

Using the distance-layer counts,

`P_full(theta)=1/[1+sum_{s=1}^q A_s theta^{-s}]`.

Define

`H_{q,k}(theta)=sum_{s=1}^q A_s theta^{-s}`.

`H_{q,k}` is continuous and strictly decreasing on `theta>0`, with limits `infinity` at zero and `0` at infinity. Hence there is a unique positive `theta_1/2(q,k)` such that

`P_full(theta_1/2)=1/2`.

Equivalently, `theta_1/2` is the unique positive root of

`theta^q=sum_{s=1}^q A_s theta^(q-s)`.

## Theorem 4

For `q=1`,

`theta_1/2=T_k`.

For every `q>=2`,

`T_k < theta_1/2 < 2T_k`.

### Proof

At `theta=T_k`, the adjacent layer alone has the same weight as full gain, and at least one additional lower layer contributes positive mass when `q>=2`; therefore `P_full(T_k)<1/2` and `theta_1/2>T_k`.

At `theta=2T_k`, Theorem 2 gives

`H_{q,k}(2T_k) <= sum_{s=1}^q 2^{-s}=1-2^{-q}<1`.

Hence `P_full(2T_k)>1/2` and `theta_1/2<2T_k`. QED.

For `q>=2`, the stationary ordering therefore has three biologically distinct regions:

1. `theta<T_k`: full gain is not the largest gain class;
2. `T_k<=theta<theta_1/2`: full gain is aggregate-modal at or beyond the mode boundary but still has less than half of stationary mass;
3. `theta>=theta_1/2`: full gain is a stationary majority.

## Running example

For `q=2,k=3`, `A_1=7`, `A_2=19`. The majority boundary is the positive root of

`theta^2-7theta-19=0`,

namely

`theta_1/2=(7+5 sqrt(5))/2`,

between 9 and 10. Exact evaluations give

`P_full(9)=81/163<1/2`,

`P_full(10)=100/189>1/2`.

The aggregate-mode threshold is only `T_3=7`, so the two occupancy transitions are visibly separated.

---

# Population-size corollaries under the Moran bridge

With multiplicative fitness step `a>1`,

`theta=a^(N-1)`.

Therefore full gain is aggregate-modal iff

`a^(N-1)>=2^k-1`,

and uniquely aggregate-modal iff the inequality is strict.

It is a stationary majority iff

`a^(N-1)>=theta_1/2(q,k)`.

## Canonical routing with `a=2`

Set `k=q+1`.

The mode theorem gives

`N_modal=N_unique_mode=q+2`.

For `q=1`, majority also occurs at `N=3=q+2`.

For every `q>=2`, majority occurs exactly one population-size step later:

`N_majority=q+3`.

To see necessity, at `N=q+2` the tilt is `theta=2^k=T_k+1`. The adjacent-layer ratio is `1-2^{-k}`. The `s=2` ratio is `(3^k-2^k)/4^k`, which exceeds `2^{-k}` for `k>=3` because `3^k>2^(k+1)`. Thus those two lower layers alone outweigh full gain. Sufficiency follows from Theorem 4 because

`theta_1/2<2T_k<2^(k+1)`,

the tilt reached at `N=q+3`.

This exact one-step separation is the canonical distinction between becoming the largest class and becoming a majority of stationary occupancy.

---

# Scope Result 1 — occupancy thresholds depend on representation

Hold fixed the gain set `{0,...,q}` and phenotype-level fitness schedule.

For the canonical branch-product representation

`X_prod={0,...,q}^{q+1}`,

the aggregate-mode threshold is `2^(q+1)-1` and the majority threshold is larger for `q>=2`.

For a compressed representation

`X_chain={0,...,q}`

with one genotype per gain, aggregate weights are `1,theta,...,theta^q`. The full layer is uniquely modal for every `theta>1`, and its majority boundary is the positive solution of

`theta^q=sum_{r=0}^{q-1} theta^r`.

At `q=2,theta=2`:

- compressed weights `(1,2,4)`, `P_full=4/7>1/2`;
- branch-product weights `(19,14,4)`, `P_full=4/37` and full gain is nonmodal.

The phenotype levels and fitness schedule are identical. Representation changes both mode and majority conclusions.

---

# Scope Result 2 — fixed mutation support is still insufficient

Under a general reversible neutral mutation measure `mu`,

`pi(x) proportional to mu(x) theta^{g(x)}`.

On a fixed gain path `0<->1<->...<->q`, fix any `theta>0` and any strictly positive target stationary distribution `p`. Taking

`mu_r proportional to p_r theta^{-r}`

and constructing a connected reversible nearest-neighbor kernel with stationary measure `mu` yields selected stationary law `pi=p`.

Thus gain levels, phenotype fitness, and local mutation support do not identify stationary occupancy without neutral mutation weights. For the frozen `q=2,theta=2` witness, the same path support admits selected stationary distributions

`(1/10,1/10,4/5)`

and

`(9/20,9/20,1/10)`.

This is the claim ceiling for both the modal and majority thresholds.

---

# Final result hierarchy

- **Theorem 1:** exact routing-layer multiplicity.
- **Theorem 2:** global nested-chain degeneracy bound.
- **Theorem 3:** exact aggregate-mode trichotomy.
- **Theorem 4:** unique stationary-majority boundary and `T_k < theta_1/2 < 2T_k` for `q>=2`.
- **Corollary:** Moran population thresholds, including canonical `N_unique_mode=q+2` versus `N_majority=q+3` for `q>=2`.
- **Scope controls:** representation dependence and reversible mutation-measure nonidentifiability.

Do not append neutral-plateau waiting times, mesoscopic acquisition, absolute-rate scaling, or downstream population-process results. They are not needed for the stationary occupancy story.