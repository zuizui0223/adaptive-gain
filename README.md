# adaptive-gain

A small theory repository for **when outcome-contingent measurement choice is strictly better than a fixed measurement bundle**.

It was extracted from a cross-repository comparison of:

- [`zuizui0223/mrod`](https://github.com/zuizui0223/mrod) — an initial observation can route the next assay;
- [`zuizui0223/payoff`](https://github.com/zuizui0223/payoff) — an initial payoff contrast can route the next architecture distance;
- [`zuizui0223/balance`](https://github.com/zuizui0223/balance) — under the current threshold-span objective, branch labels change interval location but not the sufficient future-value state, giving a no-routing control.

The source repositories retain ownership of their scientific models. `adaptive-gain` abstracts only the finite **decision structure** and has no runtime dependency on those repositories.

## Core finite problem

Let `W` be a finite represented hidden-world set, `T: W -> labels` the declared target, and each query have a positive integer acquisition cost plus one deterministic outcome in every represented world.

A **fixed design** chooses one bundle before seeing outcomes. An **adaptive design** chooses the next query from outcomes already observed.

Define

```text
C_A = minimum worst-path cost of guaranteed target resolution by an adaptive tree
C_F = minimum cost of a fixed resolving bundle
```

Every fixed bundle is an adaptive policy that ignores intermediate outcomes, so

\[
\boxed{C_A\le C_F}.
\]

Strict adaptive gain exists exactly when

\[
\boxed{C_A<C_F}.
\]

For integer acquisition budget `B`, the exact adaptive-only resolution window is

\[
\boxed{C_A\le B<C_F}.
\]

## Refined cost decomposition: where potential gain goes

Let `pi*` be the selected optimal adaptive tree and define

```text
U   = cost of every distinct query appearing anywhere in pi*
C_U = cheapest fixed resolving subset restricted to that selected tree union
```

Flattening the tree union is a valid fixed resolver and restricting the fixed vocabulary cannot improve its global optimum. Therefore

\[
\boxed{C_A\le C_F\le C_U\le U}.
\]

This yields the exact four-term identity

\[
\boxed{
U-C_A
=(C_F-C_A)+(C_U-C_F)+(U-C_U)
}
\]

with

```text
branch-exclusive overhead = U - C_A
realized adaptive gain     = C_F - C_A
external shortcut discount = C_U - C_F
internal union redundancy  = U - C_U
```

and the older aggregate fixed bypass

```text
fixed bypass discount = U - C_F
                      = internal redundancy + external shortcut.
```

So branch specialization creates **potential** overhead, but a fixed design can recover some of it in two distinct ways:

1. **internal redundancy** — a cheaper fixed subset already exists inside the adaptive tree's query union;
2. **external shortcut** — the union is internally irreducible, but another query outside that union creates a cheaper fixed route.

Bypass is a discount, not a binary veto. Six-world controls show

```text
C_A=3, C_F=4, U=5
```

with either one unit of internal redundancy or one unit of external shortcut. In both cases one unit of overhead is consumed by bypass and one unit survives as genuine adaptive gain.

Implementation: `adaptive_gain/decomposition.py`.

## Fixed resolution as a target-pair cover

Only pairs of represented worlds with different target values need to be separated:

\[
P_T=\{\{w_i,w_j\}:T(w_i)\ne T(w_j)\}.
\]

Each query covers the cross-target pairs on which its outcomes differ. A fixed resolving bundle is therefore a weighted **target-pair cover**.

This connects the fixed side to established Test Cover / Set Cover structure. The repository does **not** claim invention of those covering methods; it uses them to build checkable lower-bound certificates against the exact adaptive optimum.

## Certificate ladder for strict adaptive gain

The current repository contains four increasingly strong fixed-side proof layers.

### 1. Private-pair certificate

If a query is the **only** declared separator of some cross-target pair, every fixed resolver must buy it.

If every query in the selected adaptive union has such a globally private pair and `U>C_A`, then

\[
\boxed{C_F=U>C_A}
\]

without globally optimizing the fixed class.

The registered MROD-style and PAYOFF-style routing witnesses satisfy this strong certificate.

### 2. Integral pair packing

Choose cross-target pairs `P*` such that each query separates at most `cost(q)` chosen pairs:

\[
|\{p\in P^*:q\text{ separates }p\}|\le c(q).
\]

Then every fixed resolver obeys

\[
\boxed{C_F\ge |P^*|}.
\]

Thus a packing of size at least `C_A+1` certifies strict gain. This can succeed when no single private pair proves every needed query mandatory.

### 3. Fractional pair-cover dual

Allow rational pair weights `y_p>=0` with

\[
\sum_{p:q\text{ separates }p}y_p\le c(q).
\]

Then

\[
C_F\ge\sum_p y_p.
\]

Since fixed acquisition costs are integer,

\[
\boxed{C_F\ge\left\lceil\sum_p y_p\right\rceil}.
\]

A five-world control has

```text
C_A=2, C_F=3
integral packing maximum = 2
fractional optimum       = 5/2
```

so only the fractional layer proves `C_F>=3` without solving the integer fixed cover.

### 4. Exact integer fixed cover

The hierarchy is still incomplete before exact integer optimization. Another five-world control has

```text
C_A = 2
fractional fixed lower bound = 2
C_F = 3
```

so the LP relaxation has an explicit integrality gap. Strict gain is real, but private-pair, integral-packing, and fractional-packing certificates are all insufficient.

Therefore the verified hierarchy is

```text
private pair
  -> integral pair packing
  -> fractional pair packing
  -> exact integer fixed cover
```

and each additional layer can matter.

See:

- `theory/FIXED_BYPASS_PAIR_COVER.md`
- `theory/PAIR_PACKING_LOWER_BOUND.md`
- `theory/FRACTIONAL_PAIR_COVER_BOUND.md`

## Registered source-derived witnesses

For both MROD-style and PAYOFF-style routing:

```text
C_A = 2
C_F = C_U = U = 3

overhead = 1
gain     = 1
internal = 0
external = 0
```

Under uniform represented worlds, the first routing observation has zero direct target information, while the selected adaptive policy identifies the target completely. The best fixed information at budget 2 is 0.5 bit in both registered abstractions.

This demonstrates

```text
zero direct target information
!=
zero decision relevance
```

but zero direct information is neither necessary nor sufficient for adaptive gain in general.

### MROD-style routing

The deterministic hidden world expands `(context, target)` with nuisance bits:

```text
context 0 -> assay0 reveals target, assay1 reveals nuisance
context 1 -> assay1 reveals target, assay0 reveals nuisance
```

The routing observation chooses which assay should come next.

### PAYOFF-style routing

Four categorical worlds preserve the finite separation pattern of the source PAYOFF quadratic/triangular example:

```text
first intrinsic contrast
  low branch  -> interaction distance 0.2
  high branch -> interaction distance 0.1
```

This abstraction does not replace PAYOFF's continuous payoff model or bounded-error phase certificate.

### BALANCE-style no-routing control

For the source BALANCE midpoint reset rule,

```text
a(w,e)=min(w,w/2+e)
```

both supported state outcomes leave the same future span. Branch labels change interval location but not the declared sufficient future-value signature. A local branch-invariance certificate therefore reports no extra routing value at that step.

## Minimality and exhaustive validation

Strict worst-path adaptive cost gain requires at least

```text
4 represented worlds
3 query identities.
```

For three labeled unit-cost binary queries the complete small-universe classification is:

| Target assignment | Labeled tasks | Strict-gain tasks |
|---|---:|---:|
| 2 worlds, 1+1 | 64 | 0 |
| 3 worlds, 2+1 | 512 | 0 |
| 4 worlds, 3+1 | 4096 | 0 |
| 4 worlds, 2+2 | 4096 | **192** |

For the balanced four-world universe:

| `(C_A,C_F)` | Count |
|---|---:|
| unresolved | 1688 |
| `(1,1)` | 1352 |
| `(2,2)` | 864 |
| `(2,3)` | **192** |

All 192 strict-gain tasks are also caught by the strong selected-policy private-pair certificate. That finite completeness is not general: larger controls require integral or fractional pair-packing certificates, and some still require the exact integer cover.

See `theory/STRUCTURAL_DECOMPOSITION_AND_MINIMALITY.md`.

## Executable certificate audit

```bash
python examples/audit_witnesses.py
python examples/audit_certificate_ladder.py
```

The second script prints, for source-derived and adverse controls, which certificate layer succeeds together with `C_A`, `C_F`, `C_U`, `U`, internal redundancy, and external shortcut discounts. CI runs both scripts on Python 3.10, 3.11, and 3.12.

## Package

```text
adaptive_gain/
  core.py                 exact fixed/adaptive resolution solvers
  certificates.py         routing and branch-invariance certificates
  decomposition.py        C_A <= C_F <= C_U <= U decomposition
  exhaustive.py           complete tiny binary-universe validation
  information.py          target-information diagnostics
  pair_cover.py           target-pair cover + private-pair certificates
  pair_packing.py         exact integral pair-packing lower bounds
  fractional_packing.py   exact rational small-task LP-dual bounds
  witnesses.py            source-derived and adverse structural controls

theory/
  ADAPTIVE_GAIN_THEOREM.md
  STRUCTURAL_DECOMPOSITION_AND_MINIMALITY.md
  FIXED_BYPASS_PAIR_COVER.md
  PAIR_PACKING_LOWER_BOUND.md
  FRACTIONAL_PAIR_COVER_BOUND.md
  PROVENANCE.md
  OPEN_PROBLEMS.md
```

## Scope boundary

This repository does **not** claim:

- a new general theory of adaptive experimental design or Set/Test Cover;
- that PAYOFF, MROD, and BALANCE are the same scientific model;
- that branch dependence alone is sufficient for adaptive gain;
- that zero direct target information is necessary or sufficient for gain;
- that bypass must eliminate gain;
- that a failed lower-bound certificate means no gain exists;
- that adaptive gain persists at all budgets;
- that tiny-universe task counts are empirical prevalence estimates;
- that a finite synthetic witness is empirical evidence;
- that target resolution licenses a biological report.

The narrower contribution is a tested bridge between exact adaptive-tree costs and increasingly strong, checkable fixed-resolution lower bounds exposed by the three repository-specific results.

## Run

```bash
python -m pip install -e .
python -m pytest -q
```
