# Structural decomposition, bypass controls, and minimality

Status: exact finite deterministic target-resolution theory. The registered source-repository witnesses remain synthetic/conditional abstractions.

## 1. Union-flattening theorem

Let `pi` be any deterministic adaptive tree that resolves the target on every represented world. Let

```text
U(pi) = set of distinct query identities appearing anywhere in the tree,
u(pi) = sum of their positive acquisition costs,
d(pi) = worst root-to-leaf path cost.
```

Then `U(pi)` is itself a resolving fixed bundle.

Proof: take any two represented worlds with different targets. If every query in `U(pi)` gave the same outcome in the two worlds, the worlds would follow exactly the same branch at every node of `pi` and reach the same terminal leaf. That leaf would then contain two target values, contradicting target resolution. Therefore some query in the union separates every opposite-target pair.

For an optimal adaptive tree `pi*`, write

```text
C_A = d(pi*)
C_F = minimum fixed resolving-bundle cost
U   = u(pi*).
```

The class-containment and union-flattening inequalities are

```text
C_A <= C_F <= U.
```

## 2. Exact cost decomposition

Define

```text
branch-exclusive overhead = U - C_A
realized adaptive gain     = C_F - C_A
fixed bypass discount      = U - C_F.
```

All three are nonnegative and satisfy the exact identity

```text
U - C_A = (C_F - C_A) + (U - C_F).
```

or

\[
\boxed{
\text{branch-exclusive overhead}
=
\text{realized adaptive gain}
+
\text{fixed bypass discount}
}
\]

Interpretation:

- `U-C_A` is the extra acquisition burden of flattening all mutually exclusive adaptive branches into one union bundle;
- `C_F-C_A` is the part of that burden that actually survives after optimizing the fixed class;
- `U-C_F` is the amount the fixed class recovers by using some cheaper resolving bundle, possibly one that omits the adaptive tree's routing query entirely.

Therefore positive branch-exclusive overhead is **necessary but not sufficient** for strict adaptive gain.

Implementation: `adaptive_gain/decomposition.py`.

## 3. Registered positive witnesses saturate the bound

For both the MROD-style and PAYOFF-style routing witnesses,

```text
C_A = 2
C_F = 3
U   = 3.
```

Hence

```text
overhead = 1
gain     = 1
bypass   = 0.
```

Every unit of branch-exclusive overhead becomes realized adaptive gain.

## 4. Bypass counterexample

A four-world binary-target control uses three unit-cost queries:

```text
targets = (0,0,1,1)

q_left  = (0,0,0,1)
q_route = (0,1,0,1)
q_right = (0,1,1,0).
```

`q_route` has zero direct target information under uniform worlds and splits the task into two unresolved branches:

```text
q_route=0 -> q_right resolves
q_route=1 -> q_left resolves.
```

Thus an adaptive tree has worst-path cost 2 and genuinely branch-dependent next actions. Its query union is all three queries, so `U=3`.

However the fixed bundle `(q_left,q_right)` already resolves the target at cost 2 without buying `q_route`.

Therefore

```text
C_A = 2
C_F = 2
U   = 3

overhead = 1
gain     = 0
bypass   = 1.
```

This falsifies the naive sufficient condition

```text
zero direct target information
+
branch-dependent continuation
=> strict adaptive gain.
```

The missing condition is that the optimized fixed class must NOT have a cheaper bypass bundle.

## 5. Minimality theorem

Strict worst-path adaptive cost gain requires at least:

```text
4 represented worlds,
3 query identities.
```

### Fewer than four worlds

Suppose every internal node has at most one child whose compatible set contains more than one target value. Then all nonterminal queries lie on one unresolved spine. The union of all queries used by the tree is exactly the set of queries on that spine, so

```text
U = d(pi).
```

The decomposition gives zero possible strict gain.

Therefore positive branch-exclusive overhead requires some node with at least two unresolved children. Each unresolved child contains at least two worlds with different targets, and the child supports are disjoint. At least four represented worlds are required.

### Fewer than three queries

With at most two query identities, a resolving tree cannot have one routing query plus two distinct branch-exclusive continuations. Any resolving union has the same cost as some worst path, hence `U=C_A` for an optimal tree and strict gain is impossible.

These are structural lower bounds for this deterministic guaranteed-resolution problem, not claims about stochastic expected-cost design.

## 6. Exhaustive small-universe classification

`adaptive_gain.exhaustive.enumerate_binary_universe` enumerates every labeled binary outcome map for a fixed target assignment and three labeled unit-cost queries. Isomorphic relabelings are intentionally counted separately.

### Two worlds, target split 1+1

There are

```text
4^3 = 64
```

labeled query triples. Strict gain count: `0`.

### Three worlds, target split 2+1

There are

```text
8^3 = 512
```

labeled query triples. Strict gain count: `0`.

### Four worlds, target split 3+1

There are

```text
16^3 = 4096
```

labeled query triples. Strict gain count: `0`.

### Four worlds, balanced target split 2+2

There are `4096` labeled query triples. Exact classification:

| `(C_A,C_F)` | Count |
|---|---:|
| unresolved | 1688 |
| `(1,1)` | 1352 |
| `(2,2)` | 864 |
| `(2,3)` | **192** |

Thus exactly

\[
\boxed{192/4096}
\]

of this deliberately tiny labeled universe has strict gain, and every strict case has

```text
C_A=2, C_F=3.
```

For this specific balanced four-world universe, every optimal first query in all 192 strict-gain tasks has zero direct target information under uniform world weights.

That zero-information pattern is a **finite-universe classification result**, not a general theorem.

## 7. Zero direct root information is not necessary

A five-world binary-target witness uses

```text
targets = (0,0,1,1,1)

q_left  = (0,0,0,0,1)
q_right = (0,1,0,0,0)
q_route = (0,1,1,1,0).
```

The optimal root `q_route` has positive direct target information under uniform world weights, yet

```text
C_A=2,
C_F=3.
```

So

```text
I(T;q_root)=0
```

is neither a necessary condition for adaptive gain nor part of the general cost theorem. It is a useful diagnostic feature of the registered MROD/PAYOFF routing examples and of the minimal balanced four-world classification only.

## 8. Revised structural picture

The earlier heuristic can now be sharpened.

Strict adaptive gain requires:

1. **branch-exclusive future work** — otherwise `U=C_A`;
2. **resource scarcity** — otherwise the fixed class can simply buy enough measurements;
3. **no equally cheap fixed bypass** — otherwise `C_F=C_A` despite branch-dependent routing.

The exact decomposition shows where the heuristic fails:

```text
branch specialization creates overhead,
fixed bypass consumes some or all of that overhead,
only the remainder appears as realized adaptive gain.
```

This is a statement about acquisition cost for finite deterministic guaranteed target resolution. Information-valued, stochastic, continuous-state, and calibration-learning problems remain separate extensions.

## Reproduce

```bash
python -m pytest -q tests/test_structural_validation.py
```

The test suite includes an independent brute-force oracle for the small universes, rather than relying only on the production dynamic program.
