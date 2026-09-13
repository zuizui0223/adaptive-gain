# Stationary-majority threshold for finite routing layers v1

## Scope

This note repairs a manuscript-level weakness in the sharp aggregate-mode theorem: becoming the largest gain layer is not the same as containing a majority of stationary mass.

No new population-genetic machinery is introduced. The result stays inside the same finite routing representation

`X={0,...,q}^k`, `g(x)=min_i x_i`,

with symmetric per-gain stationary tilt `theta>0`.

Let

`A_s=(s+1)^k-s^k`

be the multiplicity of the layer `s` steps below full gain and

`T_k=2^k-1=A_1`.

The full-gain layer has unnormalized weight `theta^q`, while all lower layers together have weight

`sum_{s=1}^q A_s theta^(q-s)`.

## Theorem M1 — unique stationary-majority boundary

The normalized stationary mass of the full-gain layer is

`P_full(theta)=1 / (1 + sum_{s=1}^q A_s theta^(-s))`.

Define

`H_{q,k}(theta)=sum_{s=1}^q A_s theta^(-s)`.

For `theta>0`, every term is positive and strictly decreasing in `theta`, so `H_{q,k}` is continuous and strictly decreasing, with

`H_{q,k}(theta) -> infinity` as `theta -> 0+`

and

`H_{q,k}(theta) -> 0` as `theta -> infinity`.

Therefore there is a unique positive value

`theta_1/2(q,k)`

such that

`P_full(theta_1/2)=1/2`.

Equivalently, `theta_1/2` is the unique positive root of

`theta^q = sum_{s=1}^q A_s theta^(q-s)`,

or

`theta^q - A_1 theta^(q-1) - ... - A_q = 0`.

The full-gain layer has stationary majority exactly when

`theta >= theta_1/2(q,k)`.

This is an occupancy threshold, not a modal threshold.

## Theorem M2 — exact relation to the modal threshold

For `q=1`,

`theta_1/2(1,k)=T_k`.

For every `q>=2`,

`T_k < theta_1/2(q,k) < 2 T_k`.

### Lower bound

At `theta=T_k`, the adjacent layer alone has the same weight as the full layer:

`A_1/T_k=1`.

If `q>=2`, at least one additional lower layer contributes positive mass, so

`H_{q,k}(T_k)>1`.

Hence

`P_full(T_k)<1/2`

and therefore

`theta_1/2>T_k`.

Thus the aggregate-mode transition necessarily occurs before stationary majority once at least three gain levels exist.

### Upper bound

The sharp layer theorem gives

`A_s <= T_k^s`.

At `theta=2T_k`,

`H_{q,k}(2T_k)
 <= sum_{s=1}^q (1/2)^s
 = 1-2^(-q)
 < 1`.

Therefore

`P_full(2T_k)>1/2`

and

`theta_1/2<2T_k`.

The factor-of-two interval is a theorem-level consequence of the same global layer bound that produced the exact modal threshold.

## Corollary M2.1 — mode and majority are distinct estimands

For `q>=2`, the three relevant regions are now

1. `theta<T_k`: full layer is not aggregate-modal and is not a majority;
2. `T_k<=theta<theta_1/2`: full layer is aggregate-modal at or above the modal boundary but still contains less than half of stationary mass;
3. `theta>=theta_1/2`: full layer contains at least half of stationary mass.

At `theta=T_k` and `k>=2`, the full and adjacent layers tie for the aggregate mode, while full mass is strictly below one half whenever `q>=2`.

This distinction removes the ambiguity of using “dominance” for two different stationary summaries.

## Canonical q=2 witness

For `q=2,k=3`,

`(A_1,A_2)=(7,19)`.

The majority boundary is the positive root of

`theta^2-7 theta-19=0`,

namely

`theta_1/2=(7+5 sqrt(5))/2`.

This lies between 9 and 10. Exact rational evaluations give

`P_full(9)=81/163 < 1/2`,

`P_full(10)=100/189 > 1/2`.

By contrast, the aggregate-mode threshold is only

`T_3=7`.

Thus the running example has a genuine interval in which full gain is the largest individual gain class but not a stationary majority.

## Corollary M3 — canonical twofold-fitness population gap

Now specialize to the canonical routing construction

`k=q+1`

and a twofold multiplicative fitness step

`a=2`.

The Moran tilt is

`theta=2^(N-1)`.

The modal theorem already gives

`N_modal=N_unique_mode=q+2`.

For `q=1`, the majority boundary is `T_2=3`, so `N_majority=3=q+2`.

For every `q>=2`, let `k=q+1>=3`. At the first dyadic tilt above the modal threshold,

`theta=2^k=T_k+1`.

The adjacent-layer ratio is

`T_k/2^k = 1-2^(-k)`.

The `s=2` layer contributes

`A_2/2^(2k) = (3^k-2^k)/4^k`.

For `k>=3`,

`3^k > 2^(k+1)`,

so

`A_2/2^(2k) > 2^(-k)`.

Hence the first two lower-layer terms already satisfy

`A_1/2^k + A_2/2^(2k) > 1`.

Therefore the full-gain layer is still below one half at

`N=q+2`.

On the other hand, Theorem M2 gives

`theta_1/2 < 2T_k < 2^(k+1)`.

Thus the next dyadic tilt,

`theta=2^(k+1)`,

is sufficient. Consequently, for every `q>=2`,

`boxed: N_majority=q+3`.

So under this canonical parameterization there is exactly one population-size step between the first unique aggregate mode and the first stationary majority:

`N_unique_mode=q+2`,

`N_majority=q+3`,  for `q>=2`.

This is a cleaner biological occupancy consequence than the mode threshold alone.

## Claim boundary

Do not describe `theta_1/2` or the factor-of-two bracket as universal mutation-selection results. They depend on the same branch-product representation and symmetric neutral measure as the modal theorem.

Under a nonuniform reversible neutral measure, raw `A_s` is replaced by layerwise neutral mass. Under a compressed representation, both the modal and majority boundaries change.

## Manuscript role

The majority result should be a **secondary theorem/corollary immediately after the sharp mode theorem**.

It has one job: show that the exact modal transition is not being used as a convenient proxy for all notions of stationary dominance. The paper can now report both:

- an exact closed-form aggregate-mode threshold;
- an exact implicit majority threshold with a sharp factor-of-two bracket and a simple canonical population-size consequence.

No waiting-time, mesoscopic, absolute-rate, or downstream-process theory is needed to complete this occupancy story.