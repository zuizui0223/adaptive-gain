# Structural decomposition, bypass channels, and minimality

Status: exact finite deterministic target-resolution theory. Registered source-repository witnesses remain synthetic/conditional abstractions.

## 1. Union-flattening theorem

Let `pi` be any deterministic adaptive tree that resolves the target on every represented world. Let

```text
Q(pi) = set of distinct query identities appearing anywhere in the tree
U(pi) = sum of their positive acquisition costs
d(pi) = worst root-to-leaf path cost.
```

Then `Q(pi)` is itself a resolving fixed bundle.

Proof: take any two represented worlds with different target values. If every query appearing in the tree gave the same outcome in the two worlds, they would follow the same branch at every node and reach the same terminal leaf, contradicting target resolution. Therefore some query in the union separates every cross-target pair.

For a selected optimal adaptive tree `pi*`, write

```text
C_A = d(pi*)
U   = U(pi*)
C_F = global minimum fixed resolving-bundle cost
C_U = minimum fixed resolving cost restricted to Q(pi*)
```

Then

\[
\boxed{C_A\le C_F\le C_U\le U}.
\]

The first inequality is class containment; the second follows because restricting the fixed vocabulary cannot improve the optimum; the third follows because the whole union is feasible.

## 2. Refined exact decomposition

Define

```text
branch-exclusive overhead = U - C_A
realized adaptive gain     = C_F - C_A
external shortcut discount = C_U - C_F
internal union redundancy  = U - C_U.
```

All four quantities are nonnegative and

\[
\boxed{
U-C_A
=(C_F-C_A)+(C_U-C_F)+(U-C_U)
}.
\]

The older aggregate fixed bypass is

\[
U-C_F=(C_U-C_F)+(U-C_U).
\]

Interpretation:

- `U-C_A`: extra burden of flattening mutually exclusive branches into one query union;
- `U-C_U`: part removable by deleting redundant queries from that union while remaining fixed;
- `C_U-C_F`: further discount available only by changing to a fixed bundle that can use queries outside the selected adaptive union;
- `C_F-C_A`: overhead that survives both discounts and is therefore genuine adaptive gain.

So bypass is not a yes/no property. It is an additive discount and can consume none, some, or all of the branch-exclusive overhead.

Implementation: `adaptive_gain/decomposition.py`.

## 3. Source-derived positive witnesses

For both the MROD-style and PAYOFF-style routing witnesses,

```text
C_A = 2
C_F = 3
C_U = 3
U   = 3.
```

Hence

```text
overhead = 1
internal = 0
external = 0
gain     = 1.
```

Every unit of branch-exclusive overhead survives as adaptive gain.

## 4. Two complete-bypass controls

### Internal redundancy control

A four-world routing task has a genuinely branch-dependent adaptive tree but

```text
C_A = 2
C_F = 2
C_U = 2
U   = 3.
```

Thus

```text
overhead = 1
internal = 1
external = 0
gain     = 0.
```

The selected adaptive union itself contains a cheaper fixed resolving subset.

### External shortcut control

A separate four-query task has

```text
C_A = 2
C_F = 2
C_U = 3
U   = 3.
```

Thus

```text
overhead = 1
internal = 0
external = 1
gain     = 0.
```

The selected adaptive union is internally irreducible, but a query outside that union creates a cheaper global fixed route.

These controls falsify the naive sufficient condition

```text
zero direct target information
+
branch-dependent continuation
=> strict adaptive gain.
```

## 5. Partial bypass does not kill gain

Larger controls show that bypass can consume only part of the overhead.

### Partial internal bypass

```text
C_A = 3
C_F = 4
C_U = 4
U   = 5
```

so

```text
overhead = 2
internal = 1
external = 0
gain     = 1.
```

### Partial external bypass

```text
C_A = 3
C_F = 4
C_U = 5
U   = 5
```

so

```text
overhead = 2
internal = 0
external = 1
gain     = 1.
```

Therefore neither of these is valid in general:

```text
bypass exists -> no gain
no bypass is necessary -> gain.
```

Only the additive decomposition is exact.

## 6. Minimality theorem

Strict worst-path adaptive cost gain requires at least:

```text
4 represented worlds
3 query identities.
```

### Fewer than four worlds

Strict gain requires positive branch-exclusive overhead. That requires some adaptive node with at least two unresolved child supports. Every unresolved child contains at least two represented worlds with different targets, and child supports are disjoint. Hence at least four worlds are required.

### Fewer than three queries

With at most two query identities there cannot be one routing query plus distinct branch-exclusive continuations. Any resolving adaptive tree can be flattened without increasing beyond the worst-path cost, so strict gain is impossible.

These are structural lower bounds for deterministic guaranteed resolution, not statements about stochastic expected-cost experiments.

## 7. Complete tiny-universe classification

`adaptive_gain.exhaustive.enumerate_binary_universe` enumerates every labeled binary outcome map for a fixed target assignment and three labeled unit-cost queries. Isomorphic relabelings are intentionally counted separately.

| Universe | Labeled query triples | Strict gain |
|---|---:|---:|
| 2 worlds, target 1+1 | 64 | 0 |
| 3 worlds, target 2+1 | 512 | 0 |
| 4 worlds, target 3+1 | 4096 | 0 |
| 4 worlds, target 2+2 | 4096 | **192** |

For the balanced four-world universe:

| `(C_A,C_F)` | Count |
|---|---:|
| unresolved | 1688 |
| `(1,1)` | 1352 |
| `(2,2)` | 864 |
| `(2,3)` | **192** |

Thus every strict task in that deliberately tiny universe has

```text
C_A=2
C_F=3.
```

The selected-policy private-pair certificate happens to identify exactly the same 192 strict tasks there with zero false positives. This finite completeness is not general.

## 8. Zero direct root information is not a general condition

In the balanced four-world / three-query universe, every optimal first query in the 192 strict-gain tasks has zero direct target information under uniform world weights.

But a five-world control has

```text
C_A=2
C_F=3
```

while an optimal root has positive direct target information. Conversely, a four-world bypass control has zero root information and branch-dependent continuation but no strict gain.

Therefore

\[
I(T;Q_{root})=0
\]

is neither necessary nor sufficient for adaptive gain.

## 9. Fixed-side certificate hierarchy

The decomposition identifies `C_F-C_A` as the quantity that must be proved positive. The repository now supplies increasingly strong lower-bound routes for `C_F`:

```text
private cross-target pair
-> integral pair packing
-> exact fractional pair-cover dual
-> exact integer fixed cover.
```

Each layer can matter on explicit controls:

- source-derived MROD/PAYOFF: private pairs already prove `C_F=U`;
- a five-world task: private pairs fail but integral packing proves strict gain;
- another five-world task: integral packing reaches only 2 but fractional optimum `5/2` proves integer `C_F>=3`;
- an LP-integrality-gap task: fractional optimum remains 2 while exact integer `C_F=3`.

See:

```text
theory/FIXED_BYPASS_PAIR_COVER.md
theory/PAIR_PACKING_LOWER_BOUND.md
theory/FRACTIONAL_PAIR_COVER_BOUND.md
```

## 10. Revised structural picture

The original heuristic can now be sharpened:

```text
branch specialization creates potential overhead;
internal fixed simplification removes part of it;
external fixed shortcuts can remove more;
only the residual becomes realized adaptive gain.
```

Equivalently,

\[
\boxed{
\text{gain}
=
\text{overhead}
-
\text{internal redundancy}
-
\text{external shortcut}
}.
\]

This is an exact cost identity for the selected optimal deterministic tree and finite guaranteed target resolution. Information-valued, stochastic, continuous-state, calibration-learning, and randomized-policy problems remain separate extensions.

## Reproduce

```bash
python -m pytest -q tests/test_structural_validation.py tests/test_pair_cover.py tests/test_pair_packing.py tests/test_fractional_packing.py
python examples/audit_certificate_ladder.py
```
