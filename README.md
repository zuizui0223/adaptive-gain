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

A fixed bundle resolves exactly when it intersects every reachable productive set:

\[
\boxed{
B\cap P_s\ne\varnothing
\quad\forall s\text{ mixed}.
}
\]

Therefore `C_F` is the minimum-weight hitting set of the inclusion-minimal productive sets

\[
\boxed{
\mathcal H_{\min}=\min_{\subseteq}\{P_s:s\text{ mixed}\}
\Longrightarrow C_F.
}
\]

The productive frontier is equivalent, for fixed resolution, to the inclusion-minimal cross-target pair-separator hypergraph. With `m` resources,

\[
|\mathcal H_{\min}|\le {m\choose\lfloor m/2\rfloor}.
\]

Implementation: `adaptive_gain/productive_frontier.py`.

## 3. Joint scalar-cost sufficiency

\[
\boxed{
\text{cost-only adaptive continuation}
+
\text{productive frontier}
\Longrightarrow
(C_A,C_F).
}
\]

No fixed-side child wiring, world-pair identities, or consumed-query histories are required once these two objects are known.

`state_resource_incidence.py` is a richer intermediate representation. `resource_continuation.py` and `resource_transition_isomorphism.py` remain useful when named resources, child wiring, policy lifting, or explicit resource-renaming certificates are required.

## 4. Weaker resource summaries really fail

Registered negative layers include

```text
continuation type + resource-orbit capacities    -> not enough for C_F
continuation type + per-resource role profiles  -> not enough for C_F
```

In the balanced four-world binary scope, the first per-resource-role ambiguity appears with four queries: one signature contains `2,304` tasks, split into `1,536` with `(C_A,C_F)=(2,2)` and `768` with `(2,3)`.

---

# Productive-frontier form of the gain decomposition

Let `S` be the distinct query resources used anywhere in one selected optimal adaptive tree. If `tau_c(H)` is minimum weighted hitting-set cost of the productive frontier and `tau_c(H;S)` is the same optimum restricted to resources in `S`, then

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

These are branch-exclusive overhead, realized adaptive gain, external shortcut discount, and internal union redundancy respectively.

`frontier_decomposition.py` reproduces the original decomposition exactly from the frontier. Regression includes internal/external bypass controls and all `4,096` minimal labeled tasks.

---

# Adaptive and fixed kernels

Adaptive-only exact reductions include state-local continuation equality, target-relevant refinement dominance, dynamic same-target world twins, and the adaptive two-sided kernel.

Fixed-side exact machinery includes

```text
productive-frontier hitting set
private-pair necessity
-> integral pair packing
-> fractional pair-cover dual
-> integer budget-infeasibility proof
-> residual kernel / proof DAG / isomorphism / symmetry compression
```

---

# Finite normal forms and extremal families

### 4 worlds / 3 binary queries

All `16^3=4,096` labeled tasks were classified exactly. The 192 strict tasks all have `(C_A,C_F)=(2,3)` and form one symmetry orbit with canonical signature

\[
\boxed{(3,5,9)}.
\]

### 4 worlds / 4 binary queries

All `16^4=65,536` tasks were enumerated. The 3,840 strict cases are only one-query extensions of the unique three-query core.

### 5 worlds / 3 binary queries

All `32^3=32,768` tasks were classified. There are 2,016 strict tasks; exactly 288 are one-world-deletion-minimal and form one new orbit with signature

\[
\boxed{(7,28,42)}.
\]

## Constant-depth unit-cost family

For `k>=2`, an explicit `k`-branch construction with one unit-cost `k`-ary router and `k` unit-cost terminal queries has

\[
\boxed{C_A=2,\qquad C_F=k+1}
\]

and therefore

\[
\boxed{
C_F-C_A=k-1,
\qquad
C_F/C_A=(k+1)/2.
}
\]

The ratio is unbounded. The `k=3` member uses six worlds and four queries and has ratio `2`; this is componentwise minimal in world count and query count for a **unit-cost** finite deterministic task with ratio strictly above `3/2`.

## Binary-observation unit-cost family

Unbounded advantage does not depend on a growing-arity router. With `k=2^d` mixed branches, use `d` binary routing-bit queries and one binary terminal query per branch. Then

\[
\boxed{C_A=d+1,\qquad C_F=2^d}
\]

so

\[
\boxed{
C_F/C_A=\frac{2^d}{d+1}\longrightarrow\infty.
}
\]

Thus the multiplicative adaptive advantage is unbounded even when **every observation is binary and every acquisition cost is one**.

---

# Sharp fixed-world / fixed-query extremal ratios under unit costs

The entire deterministic query-arity range is now closed.

## Unrestricted arity

For `n>=2` represented worlds and `m>=1` declared unit-cost queries,

\[
\boxed{
\max\frac{C_F}{C_A}
=
\max\!\left(
1,
\frac{\min\{m,\,1+\lfloor n/2\rfloor\}}{2}
\right).
}
\]

The exact unrestricted productive-tree internal-node bound is

\[
M(n,h)
=
n+1-
\max\!\left(
2,
\left\lceil\frac{n}{2^{h-1}}\right\rceil
\right).
\]

Depth two is globally extremal at fixed `n` when query arity is unrestricted.

## Binary arity

Let

\[
K=\min(m,n-1),
\qquad
 d=\lfloor\log_2(K+1)\rfloor.
\]

Then

\[
\boxed{
\max\frac{C_F}{C_A}
=
\max\!\left(
1,
\frac{2^d-1}{d},
\frac{K}{d+1}
\right).
}
\]

Alternating-target threshold paths attain this bound. The first binary-only fixed-`(n,m)` scope above `3/2` is six worlds and five queries with `(C_A,C_F)=(3,5)`.

## Any bounded arity `b>=2`

Let `F_b(n,h)` be the maximum number of internal-node occurrences in a productive tree with at most `n` leaves, depth at most `h`, and at most `b` children per internal node. It obeys

\[
\boxed{
F_b(n,h)
=
1+
\max_{2\le r\le\min(b,n)}
\max_{\substack{n_1+\cdots+n_r\le n\\n_i\ge1}}
\sum_i F_b(n_i,h-1)
}
\]

with `F_b(1,h)=F_b(n,0)=0`.

The exact fixed-`(n,m,b)` ratio is

\[
\boxed{
R_b(n,m)
=
\max_{1\le h\le n-1}
\frac{\min\{m,F_b(n,h)\}}{h}.
}
\]

This is sharp, not only an upper bound. Any extremal bounded-arity tree can be converted to a deterministic task in which every internal-node query has a private opposite-target pair. The private-pair graph is a forest and can be two-coloured, so all internal queries become simultaneously fixed-mandatory while the tree itself remains an adaptive resolving policy.

The theorem exactly recovers both endpoints:

- `b=2` gives the binary formula;
- `b>=n` gives the unrestricted formula.

See `theory/SHARP_BOUNDED_ARITY_UNIT_COST_RATIO.md` and `adaptive_gain/bounded_arity_extremal_bounds.py`.

## Productive-frontier edge cap

If the minimal productive frontier is constrained by

\[
|\mathcal H_{\min}|\le E,
\]

then under unit costs

\[
C_F=\tau(\mathcal H_{\min})\le E.
\]

Combining this with the bounded-arity tree bound gives the exact extremum

\[
\boxed{
R_{b,E}(n,m)
=
\max_{1\le h\le n-1}
\frac{\min\{m,E,F_b(n,h)\}}{h}.
}
\]

Sharpness again uses the private-pair forest construction, truncated to
`I=min(m,E,F_b(n,h))` internal queries. Its productive frontier is exactly the `I` singleton edges, so the cap is met with equality whenever active.

See `theory/SHARP_FRONTIER_EDGE_CAPPED_RATIO.md` and `adaptive_gain/frontier_edge_extremal_bounds.py`.

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

Current results concern finite deterministic guaranteed target resolution with positive acquisition costs. The sharp fixed-`(n,m,b)` and frontier-edge-cap theorems assume unit query costs. Unequal costs, stochastic observations, calibration-changing actions, and continuous compatible sets remain separate problems.

## Run

```bash
python -m pip install -e .
python -m pytest -q
python examples/audit_witnesses.py
python examples/audit_certificate_ladder.py
```
