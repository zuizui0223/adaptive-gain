# adaptive-gain

A finite structural theory of **when outcome-contingent measurement choice is strictly better than a fixed measurement bundle**.

The repository was extracted from a cross-repository comparison of `mrod`, `payoff`, and `balance`. Those repositories retain ownership of their scientific models; this repository abstracts only the finite decision structure.

## Core theorem

For a finite hidden-world set, declared target map, positive query costs, and deterministic query outcomes,

```text
C_A = minimum worst-path cost of guaranteed target resolution by an adaptive tree
C_F = minimum cost of a fixed resolving query bundle
```

Every fixed bundle is an adaptive policy that ignores intermediate outcomes, so

\[
\boxed{C_A\le C_F}.
\]

Strict adaptive gain exists exactly when

\[
\boxed{C_A<C_F},
\]

and for integer budget `B` the adaptive-only window is

\[
\boxed{C_A\le B<C_F}.
\]

For one selected optimal adaptive tree, with union cost `U` and cheapest fixed resolver inside that union `C_U`,

\[
\boxed{
U-C_A=(C_F-C_A)+(C_U-C_F)+(U-C_U).
}
\]

So realized adaptive gain is branch-exclusive overhead minus external shortcut discount and internal union redundancy.

---

# Representation hierarchy

The main result is a hierarchy of **what information may be forgotten for which objective**.

## 1. Adaptive continuation structure determines `C_A`

`continuation_bisimulation.py` recursively keeps only action costs and mixed-child continuation classes. Query identity, outcome labels, pure branches, and repeated action types may disappear.

\[
\boxed{
\operatorname{Type}(s)=\operatorname{Type}(t)
\Longrightarrow V_A(s)=V_A(t).
}
\]

This quotient is deliberately adaptive-only: registered tasks share one continuation type and `C_A=2` while having fixed costs `3` and `2`.

## 2. Productive frontier determines `C_F`

For every reachable target-mixed state `s`, let

\[
P_s=\{q:q\text{ is productive/nonconstant on }s\}.
\]

A query already consumed on the path to `s` is constant on the chosen outcome cell and remains constant on every descendant. Therefore a fixed bundle `B` resolves exactly when

\[
\boxed{
B\cap P_s\ne\varnothing
\quad\text{for every reachable mixed }s.
}
\]

So `C_F` is exactly the minimum-weight hitting set of the reachable productive-set hypergraph. Only inclusion-minimal productive sets matter:

\[
\boxed{
\mathcal H_{\min}=\min_{\subseteq}\{P_s:s\text{ mixed}\}
\Longrightarrow C_F.
}
\]

This **productive frontier** is equivalent, for fixed resolution, to the inclusion-minimal cross-target pair-separator hypergraph, and its size obeys the usual Sperner bound

\[
|\mathcal H_{\min}|\le {m\choose\lfloor m/2\rfloor}
\]

for `m` declared query resources.

Implementation: `adaptive_gain/productive_frontier.py`.

See `theory/PRODUCTIVE_FRONTIER_HITTING_SET.md` and `theory/PRODUCTIVE_FRONTIER_PAIR_EQUIVALENCE.md`.

## 3. Joint scalar-cost sufficiency

Combining the two sufficient statistics gives

\[
\boxed{
\text{cost-only adaptive continuation}
+
\text{productive frontier}
\Longrightarrow
(C_A,C_F).
}
\]

No fixed-side child wiring, world-pair identities, or consumed-query history is required once these two objects are known.

`state_resource_incidence.py` is a richer intermediate representation. `resource_continuation.py` and `resource_transition_isomorphism.py` remain useful when named resources, child wiring, policy lifting, or explicit resource-renaming certificates are required.

## 4. Weaker resource summaries really fail

Registered negative layers include

```text
continuation type + resource-orbit capacities    -> not enough for C_F
continuation type + per-resource role profiles  -> not enough for C_F
```

In the balanced four-world binary scope, the first per-resource-role ambiguity appears with four queries: one signature contains `2,304` tasks, split into `1,536` with `(C_A,C_F)=(2,2)` and `768` with `(2,3)`.

The productive-frontier theorem explains exactly what fixed-side information those weaker projections lost.

---

# Productive-frontier form of the gain decomposition

Let `S` be the distinct query resources used anywhere in one selected optimal adaptive tree and let `c(S)` be their total cost. If `tau_c(H)` is minimum weighted hitting-set cost of the productive frontier and `tau_c(H;S)` is the same optimum restricted to resources in `S`, then

\[
\boxed{
c(S)-C_A
=
[\tau_c(\mathcal H)-C_A]
+
[\tau_c(\mathcal H;S)-\tau_c(\mathcal H)]
+
[c(S)-\tau_c(\mathcal H;S)].
}
\]

These are respectively

```text
branch-exclusive overhead
= realized adaptive gain
+ external shortcut discount
+ internal union redundancy.
```

`frontier_decomposition.py` reproduces the original decomposition exactly from the frontier. Regression includes internal/external bypass controls and all `4,096` minimal labeled tasks.

See `theory/PRODUCTIVE_FRONTIER_DECOMPOSITION.md`.

---

# Adaptive and fixed kernels

Adaptive-only exact reductions include:

- state-local query continuation equality;
- target-relevant query refinement dominance;
- dynamic same-target world twins;
- the adaptive two-sided kernel.

Fixed-side exact machinery includes:

```text
productive-frontier hitting set
private-pair necessity
-> integral pair packing
-> fractional pair-cover dual
-> integer budget-infeasibility proof
-> residual kernel / proof DAG / isomorphism / symmetry compression
```

A separate joint-safe global kernel iterates same-target world twins and global query refinement dominance before either objective is solved.

---

# Finite normal forms and an extremal family

### 4 worlds / 3 binary queries

All `16^3=4,096` labeled tasks were classified exactly. The 192 strict tasks all have `(C_A,C_F)=(2,3)` and form one symmetry orbit with canonical signature

\[
\boxed{(3,5,9)}.
\]

### 4 worlds / 4 binary queries

All `16^4=65,536` tasks were enumerated. The 3,840 strict cases are only one-query extensions of the unique three-query core; no new irreducible mechanism appears.

### 5 worlds / 3 binary queries

All `32^3=32,768` tasks were classified. There are 2,016 strict tasks; exactly 288 are one-world-deletion-minimal and form one new orbit with signature

\[
\boxed{(7,28,42)}.
\]

Its standard representative has `C_A=2<C_F=3` and an optimal root with positive direct target information under uniform represented-world weights.

## Unbounded unit-cost adaptive advantage

The minimal four-world mechanism extends to an explicit `k`-branch family. There are `2k` worlds, one unit-cost `k`-ary router, and `k` unit-cost branch-terminal queries. The router identifies the branch; one terminal then resolves the target.

The terminal outcome codes are chained so that every terminal and the router is individually mandatory for fixed resolution. Therefore

\[
\boxed{C_A=2,\qquad C_F=k+1}
\]

and

\[
\boxed{
C_F-C_A=k-1,
\qquad
\frac{C_F}{C_A}=\frac{k+1}{2}.
}
\]

Thus both additive adaptive gain and the fixed/adaptive ratio are unbounded even with **unit acquisition cost**. The growing router is multi-valued.

The `k=3` member has six worlds, four queries, and ratio `2`. It is componentwise minimal in world count and query count for a **unit-cost** finite deterministic task with ratio strictly above `3/2`; every task with at most five represented worlds has ratio at most `3/2`.

See `theory/UNBOUNDED_UNIT_COST_ADAPTIVE_GAIN.md`.

---

# Source-derived witnesses

For the registered MROD-style and PAYOFF-style abstractions:

```text
C_A = 2
C_F = C_U = U = 3
```

The first routing observation has zero direct target information under uniform represented worlds, but the adaptive policy resolves the target. BALANCE supplies a no-routing control under its current deterministic threshold-span objective.

These are synthetic/conditional structural witnesses, not field empirical validation.

---

# Scope

The repository does **not** claim a new general theory of adaptive experimental design, Set Cover, hitting set, bisimulation, or graph isomorphism; polynomial-time exact optimization; natural prevalence from finite labeled-task counts; field empirical validation; or that target resolution licenses a biological report.

Current results concern finite deterministic guaranteed target resolution with positive acquisition costs. The six-world minimality and unbounded-family statements above are explicitly **unit-cost** statements; unequal costs can change minimal finite scopes.

## Run

```bash
python -m pip install -e .
python -m pytest -q
python examples/audit_witnesses.py
python examples/audit_certificate_ladder.py
```
