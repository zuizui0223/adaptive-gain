# Sharp aggregate-layer modality corollaries v1

## Scope

This note sharpens the routing-specific theorem package while leaving the standard origin-fixation machinery as prior art.

Consider the finite product space

`X = {0,...,q}^k`,

with `q>=1`, `k>=1`, and weakest-branch gain

`g(x)=min_i x_i`.

Under a symmetric stationary tilt `theta>0`, each genotype at gain `r` has weight proportional to `theta^r`, so the **aggregate** stationary weight of gain layer `r` is

`W_r = D_r theta^r`.

Nothing below concerns a switch in the most-probable individual genotype. For `theta>1`, the unique full-gain genotype already has the greatest per-genotype weight. The theorem concerns aggregation over the combinatorial multiplicity within each gain class.

## Theorem 1 — exact layer multiplicity

For `r=0,...,q`,

`D_r = (q-r+1)^k - (q-r)^k`.

Writing `s=q-r`, define

`A_s=(s+1)^k-s^k`.

Then the ratio of the layer `s` steps below full gain to the full-gain layer is

`W_{q-s}/W_q = A_s / theta^s`.

## Theorem 2 — strict global degeneracy bound

Let

`T_k = 2^k - 1 = A_1`.

For every `s>=1`,

`A_s <= T_k^s`.

For `k>=2`, equality occurs only at `s=1`; for every `s>=2`,

`A_s < T_k^s`.

### Combinatorial certificate

Represent a vector in `{0,...,s}^k` with minimum zero by

`S_j={i : x_i < j}`,  `j=1,...,s`.

Each `S_j` is nonempty and the sequence is nested:

`S_1 subseteq S_2 subseteq ... subseteq S_s`.

This gives the `A_s` admissible nested sequences. If nesting is dropped, there are exactly

`(2^k-1)^s`

arbitrary sequences of nonempty subsets. For `s=1`, no nesting restriction remains, giving equality. If `k>=2` and `s>=2`, nonnested sequences exist (for example `{1},{2},...`), so the inequality is strict.

## Theorem 3 — exact modality trichotomy

Assume `k>=2`. Then:

### Below threshold

If

`theta < T_k`,

the adjacent layer beats the full layer because

`W_{q-1}/W_q = T_k/theta > 1`.

Hence the full-gain layer is not aggregate-modal.

### At threshold

If

`theta = T_k`,

then

`W_{q-1}=W_q`,

while for every `s>=2`,

`W_{q-s}/W_q = A_s/T_k^s < 1`.

Therefore **exactly two layers tie for maximal aggregate mass**:

`{q-1, q}`.

### Above threshold

If

`theta > T_k`,

then for every `s>=1`,

`W_{q-s}/W_q <= (T_k/theta)^s < 1`.

Therefore the full-gain layer `q` is the **unique** aggregate-modal layer.

Thus the transition is sharper than a simple iff statement:

- `theta<T_k`: full layer is not modal;
- `theta=T_k`: full and adjacent layers tie, and no others tie;
- `theta>T_k`: full layer is uniquely modal.

The special case `k=1` is degenerate: `T_1=1`, every layer has multiplicity one, and all gain layers tie at `theta=1`.

## Corollary 1 — origin-fixation population threshold

Under the declared Moran step model,

`theta = a^(N-1)`,

with `a>=1` the multiplicative fitness step and `N>=2` population size.

For `a>1` and `k>=2`, the full-gain layer is aggregate-modal iff

`a^(N-1) >= T_k`.

It is uniquely aggregate-modal iff

`a^(N-1) > T_k`.

In real-valued boundary notation,

`N_modal = 1 + ceil(log(T_k)/log(a))`,

where equality is allowed, while the smallest integer population size guaranteeing uniqueness is

`N_unique = 2 + floor(log(T_k)/log(a))`.

The implementation uses exact rational powers rather than floating logarithms so exact-threshold cases cannot be misclassified numerically.

## Corollary 2 — canonical routing architecture

For the canonical routing construction,

`k=q+1`,

so

`T(q)=2^(q+1)-1`.

Hence the exact aggregate-layer transition is

`a^(N-1) ? 2^(q+1)-1`.

For `a=2`,

`2^q < 2^(q+1)-1 < 2^(q+1)`,

so both the first modal and first uniquely modal population sizes equal

`N=q+2`.

This recovers the existing canonical computational result as a direct corollary of the general `(q,k)` theorem.

## Why this strengthening matters

The main novelty candidate is not that degeneracy competes with selection. That is established. The sharper result is that, for this finite routing representation:

1. every gain layer has an exact multiplicity;
2. all lower layers are simultaneously controlled by one adjacent-layer constant `T_k`;
3. the exact threshold has a complete three-regime structure;
4. threshold equality has a precise two-layer tie for `k>=2`;
5. the population-size consequence follows without asymptotics.

This makes the theorem a finite architecture result rather than a generic weakest-link or mutation-selection statement.

## Claim boundary

Do not call `T_k` universal. It depends on the branch-product representation and the symmetric neutral measure. Under a nonuniform reversible neutral measure, raw multiplicity is replaced by layerwise neutral mass and the simple threshold need not survive.
