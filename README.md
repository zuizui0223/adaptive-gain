# adaptive-gain

A small theory repository for **when outcome-contingent measurement choice is strictly better than a fixed measurement bundle**.

This repository was extracted from a cross-repository comparison of:

- [`zuizui0223/mrod`](https://github.com/zuizui0223/mrod) — a first observation can route the next assay even when it carries zero direct target information;
- [`zuizui0223/payoff`](https://github.com/zuizui0223/payoff) — a first payoff contrast can route the next architecture distance and reduce worst-path acquisition cost;
- [`zuizui0223/balance`](https://github.com/zuizui0223/balance) — under the current Cartesian threshold-span objective, branch labels change interval location but not the sufficient future-value state, so extra direction adaptivity has zero gain.

The source repositories retain ownership of their scientific models. `adaptive-gain` abstracts only the **decision structure** and has no runtime dependency on those repositories.

## Core finite problem

Let

- `W` be a finite represented hidden-world set;
- `T: W -> labels` be the declared target;
- each query `q` have a positive integer acquisition cost;
- each query have one deterministic outcome in every represented world.

A **fixed design** chooses one bundle before seeing outcomes. An **adaptive design** chooses the next query from the outcomes already observed.

Define

```text
C_adapt = minimum worst-path cost of guaranteed target resolution,
C_fixed = minimum cost of a fixed resolving bundle.
```

Every fixed bundle can be executed as an adaptive policy that simply ignores its observations until the bundle is complete. Therefore

```text
C_adapt <= C_fixed.
```

Strict adaptive gain in guaranteed resolution exists exactly when

```text
C_adapt < C_fixed.
```

For integer acquisition budget `B`, the **adaptive-only resolution window** is exactly

```text
C_adapt <= B < C_fixed.
```

When both costs are finite, this window is contiguous. It may be empty.

## New structural decomposition from validation

Let `pi*` be the selected optimal adaptive tree and let

```text
U = total cost of every distinct query appearing anywhere in pi*.
```

Flattening the full query union into one fixed bundle always resolves the target, so

```text
C_adapt <= C_fixed <= U.
```

This gives the exact decomposition

```text
U - C_adapt
=
(C_fixed - C_adapt)
+
(U - C_fixed).
```

The three terms are named

```text
branch-exclusive overhead = U - C_adapt
realized adaptive gain     = C_fixed - C_adapt
fixed bypass discount      = U - C_fixed.
```

Hence

```text
branch-exclusive overhead
=
realized adaptive gain
+
fixed bypass discount.
```

This sharpens the earlier intuition. Branch-dependent continuation can create query overhead for a fixed plan, but **another fixed bundle may bypass the routing query entirely**. Positive branch-exclusive overhead is therefore necessary but not sufficient for strict adaptive gain.

Implementation: `adaptive_gain/decomposition.py`.

### Registered positive witnesses

For both MROD-style and PAYOFF-style routing:

```text
C_adapt = 2
C_fixed = 3
U       = 3

overhead = 1
gain     = 1
bypass   = 0.
```

The branch-exclusive overhead is fully converted into realized adaptive gain.

### Bypass counterexample

A four-world control has

```text
targets = (0,0,1,1)

q_left  = (0,0,0,1)
q_route = (0,1,0,1)
q_right = (0,1,1,0).
```

`q_route` has zero direct target information under uniform worlds and its two outcomes require different next queries. Yet the fixed bundle `(q_left,q_right)` already resolves the target without buying `q_route`.

Therefore

```text
C_adapt = 2
C_fixed = 2
U       = 3

overhead = 1
gain     = 0
bypass   = 1.
```

So

```text
zero direct target information
+
branch-dependent continuation
```

does **not** imply strict adaptive gain.

## Routing certificate

A strong sufficient certificate for adaptive-only resolution at budget `B` is:

```text
1. choose an affordable root query q;
2. every q-outcome branch has a resolving adaptive continuation within B-cost(q);
3. no fixed bundle of total cost <= B resolves the root task.
```

The library returns the branch-specific continuation query, continuation cost, and whether the next action actually differs across branches.

This is deliberately stronger than merely saying "the branches differ".

## Local no-routing certificate

Suppose a model declares a sufficient future-value state `sigma`. If every outcome of a query maps to the same future signature,

```text
sigma(after q, outcome y) = sigma_prime  for every reachable y,
```

then a continuation value that depends only on that signature cannot gain from conditioning the **next action** on the branch label at that step.

The library can audit equality of declared signatures. It cannot prove that the caller's signature is scientifically sufficient.

This is the structure used by the BALANCE negative control.

## Minimality and exhaustive validation

Strict worst-path adaptive cost gain in this deterministic finite problem requires at least

```text
4 represented worlds
3 query identities.
```

With fewer than four worlds there cannot be two disjoint unresolved outcome branches, each containing different target values. With fewer than three queries there cannot be one routing query plus distinct branch-exclusive continuations.

An independent brute-force oracle was added to the test suite. For three labeled unit-cost binary queries:

| Fixed target assignment | Labeled query triples | Strict-gain tasks |
|---|---:|---:|
| 2 worlds, split 1+1 | 64 | 0 |
| 3 worlds, split 2+1 | 512 | 0 |
| 4 worlds, split 3+1 | 4096 | 0 |
| 4 worlds, split 2+2 | 4096 | **192** |

For the balanced four-world universe the exact cost classification is:

| `(C_adapt,C_fixed)` | Count |
|---|---:|
| unresolved | 1688 |
| `(1,1)` | 1352 |
| `(2,2)` | 864 |
| `(2,3)` | **192** |

Every strict-gain case in this deliberately tiny balanced universe has `C_adapt=2,C_fixed=3`, and every optimal root has zero direct target information under uniform world weights.

That last zero-information property is **not a general theorem**. A separate five-world control has `C_adapt=2,C_fixed=3` while its optimal routing root has positive direct target information. Thus

```text
I(T; root) = 0
```

is neither necessary nor sufficient for adaptive gain in general.

See `theory/STRUCTURAL_DECOMPOSITION_AND_MINIMALITY.md`.

## Registered source-repository witnesses

| Witness | Root direct target info | `C_adapt` | `C_fixed` | Adaptive-only budget |
|---|---:|---:|---:|---:|
| MROD-style context routing | 0 bit | 2 | 3 | 2 |
| PAYOFF-style response routing | 0 bit | 2 | 3 | 2 |
| Direct-resolution control | >0 | 1 | 1 | none |

For the two positive witnesses under uniform represented worlds:

```text
root direct target information = 0 bit
selected adaptive-policy target information = 1 bit
best fixed information with budget 2 = 0.5 bit
next-action entropy at the root = 1 bit
```

So

```text
zero direct target information
!=
zero decision relevance.
```

The first observation can be useful because it tells the policy **which experiment should come next** — but the bypass counterexample shows that routing structure alone does not guarantee a class-level gain.

### MROD-style witness

The deterministic hidden world is `(context, target, nuisance0, nuisance1)`.

```text
context 0 -> assay0 reveals target, assay1 reveals nuisance
context 1 -> assay1 reveals target, assay0 reveals nuisance
```

`context` itself is independent of the target in the uniform witness. The adaptive policy measures context, then the context-appropriate assay.

### PAYOFF-style witness

Four categorical worlds preserve the exact separation pattern of the existing finite quadratic/triangular PAYOFF routing example:

```text
first intrinsic contrast
  low branch  -> interaction distance 0.2
  high branch -> interaction distance 0.1
```

The abstraction preserves the finite target-separation structure; it does not copy or replace PAYOFF's continuous payoff model.

### BALANCE-style negative control

For a threshold span `w` and bounded command error `e`, the current BALANCE midpoint-reset model updates the span by

```text
a(w,e) = min(w, w/2 + e)
```

under either supported state outcome. The posterior interval **location** differs, but the declared sufficient future-value signature based on spans, remaining budget, errors, and directional costs is unchanged by the branch label.

The no-routing certificate therefore fires.

## Package

```text
adaptive_gain/
  core.py           exact fixed/adaptive resolution solvers
  certificates.py  routing and no-routing certificates
  decomposition.py exact union/gain/bypass cost identity
  exhaustive.py    finite binary-universe classification helper
  information.py   direct/continuation information diagnostics
  witnesses.py     source-derived witnesses plus adverse controls

theory/
  ADAPTIVE_GAIN_THEOREM.md
  STRUCTURAL_DECOMPOSITION_AND_MINIMALITY.md
  PROVENANCE.md
  OPEN_PROBLEMS.md
```

Quick example:

```python
from adaptive_gain import adaptive_gain_receipt, optimal_policy_cost_decomposition
from adaptive_gain.witnesses import mrod_routing_task

task = mrod_routing_task()

print(adaptive_gain_receipt(task))
print(optimal_policy_cost_decomposition(task))
```

## Scope boundary

This repository does **not** claim:

- a new general theory of adaptive experimental design;
- that PAYOFF, MROD, and BALANCE are the same scientific model;
- that branch dependence alone is sufficient for adaptive gain;
- that zero direct target information is necessary or sufficient for gain;
- that adaptive gain persists at all budgets;
- that counts in a tiny labeled task universe are empirical prevalence estimates;
- that a finite synthetic witness is empirical evidence;
- that target resolution licenses a biological report;
- that the registered positive examples are common in natural systems.

The narrower contribution is a reusable, tested abstraction of the exact structural distinction exposed by the three repository-specific results.

## Run

```bash
python -m pip install -e .
python -m pytest -q
```
