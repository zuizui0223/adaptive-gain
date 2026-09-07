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

## Routing certificate

A strong sufficient certificate for adaptive-only resolution at budget `B` is:

```text
1. choose an affordable root query q;
2. every q-outcome branch has a resolving adaptive continuation within B-cost(q);
3. no fixed bundle of total cost <= B resolves the root task.
```

The library returns the branch-specific continuation query, continuation cost, and whether the next action actually differs across branches.

This is deliberately stronger than merely saying "the branches differ". Branch dependence alone does not guarantee adaptive gain.

## Local no-routing certificate

Suppose a model declares a sufficient future-value state `sigma`. If every outcome of a query maps to the same future signature,

```text
sigma(after q, outcome y) = sigma_prime  for every reachable y,
```

then a continuation value that depends only on that signature cannot gain from conditioning the **next action** on the branch label at that step.

The library can audit equality of declared signatures. It cannot prove that the caller's signature is scientifically sufficient.

This is the structure used by the BALANCE negative control.

## Registered witnesses

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

The first observation can be useful because it tells the policy **which experiment should come next**.

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
  core.py          exact fixed/adaptive resolution solvers
  certificates.py routing and no-routing certificates
  information.py  direct/continuation information diagnostics
  witnesses.py    MROD/PAYOFF/BALANCE finite witnesses

theory/
  ADAPTIVE_GAIN_THEOREM.md
  PROVENANCE.md
```

Quick example:

```python
from adaptive_gain import adaptive_gain_receipt, routing_certificate
from adaptive_gain.witnesses import mrod_routing_task

task = mrod_routing_task()

print(adaptive_gain_receipt(task))
print(routing_certificate(task, "context", budget=2))
```

## Scope boundary

This repository does **not** claim:

- a new general theory of adaptive experimental design;
- that PAYOFF, MROD, and BALANCE are the same scientific model;
- that branch dependence alone is sufficient for adaptive gain;
- that adaptive gain persists at all budgets;
- that a finite synthetic witness is empirical evidence;
- that zero target information is intrinsically valuable;
- that target resolution licenses a biological report;
- that the registered positive examples are common in natural systems.

The narrower contribution is a reusable, tested abstraction of the exact structural distinction exposed by the three repository-specific results.

## Run

```bash
python -m pip install -e .
python -m pytest -q
```
