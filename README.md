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

The main result is now a hierarchy of **what information may be forgotten for which objective**.

## 1. Full target-pair incidence preserves both costs

For each query and each cross-target world pair, record whether the query separates that pair. The full identity-indexed incidence plus target labels and query costs determines both exact optima:

\[
\boxed{
\text{full target-pair incidence}\Longrightarrow(C_A,C_F).
}
\]

See `theory/TARGET_PAIR_INCIDENCE_SUFFICIENCY.md`.

## 2. Adaptive-only continuation structure preserves `C_A`

`continuation_bisimulation.py` recursively keeps only action costs and mixed-child continuation classes. Query identity, outcome labels, pure branches, and repeated action types may disappear.

\[
\boxed{
\operatorname{Type}(s)=\operatorname{Type}(t)
\Longrightarrow V_A(s)=V_A(t).
}
\]

This quotient is not sufficient for `C_F`; registered tasks share the same adaptive continuation type and `C_A=2` while having fixed costs `3` and `2`.

## 3. Reachable state-resource incidence is sufficient for `C_F`

For every reachable mixed state `s`, define

```text
U_s = queries already consumed on the history to s
P_s = still-available queries productive on s
```

Then a fixed bundle `B` fails exactly when

\[
\boxed{
\exists s:\ U_s\subseteq B,\qquad P_s\cap B=\varnothing.
}
\]

Therefore query costs plus the unique reachable `(U_s,P_s)` rows determine the exact fixed optimum:

\[
\boxed{
\{(U_s,P_s)\}+\text{costs}\Longrightarrow C_F.
}
\]

A row `(U_1,P_1)` makes `(U_2,P_2)` redundant when

\[
U_1\subseteq U_2,\qquad P_1\subseteq P_2.
\]

Implementation: `adaptive_gain/state_resource_incidence.py`.

See `theory/STATE_RESOURCE_INCIDENCE_SUFFICIENCY.md`.

## 4. Joint scalar-cost sufficiency without child wiring

Combining the previous two results gives

\[
\boxed{
\text{cost-only continuation structure}
+
\text{state-resource }(U,P)\text{ incidence}
\Longrightarrow
(C_A,C_F).
}
\]

This is weaker than retaining the entire resource-labelled child-transition system when only the two scalar optima are needed.

`resource_continuation.py` and `resource_transition_isomorphism.py` remain useful for named resource transitions, policy lifting, child wiring, and explicit global resource-renaming certificates.

## 5. Weaker resource summaries really fail

Two negative layers are registered:

```text
continuation type + resource-orbit capacities    -> not enough for C_F
continuation type + per-resource role profiles  -> not enough for C_F
```

In the balanced four-world binary scope, the first per-resource-role ambiguity appears with four queries: one signature contains `2,304` tasks, split into `1,536` with `(C_A,C_F)=(2,2)` and `768` with `(2,3)`.

State-resource co-location repairs that entire finite ambiguity, and the theorem above explains why the simpler `(U,P)` projection already suffices for `C_F` generally under the deterministic contract.

See `theory/RESOURCE_OVERLAP_HIERARCHY.md`.

---

# Adaptive and fixed kernels

Adaptive-only exact reductions include:

- state-local query continuation equality;
- target-relevant query refinement dominance;
- dynamic same-target world twins;
- the adaptive two-sided kernel.

Fixed-side exact machinery includes:

```text
private-pair necessity
-> integral pair packing
-> fractional pair-cover dual
-> integer budget-infeasibility proof
-> two-sided residual kernel
-> proof DAG / isomorphism / symmetry compression
```

A separate joint-safe global kernel iterates same-target world twins and global query refinement dominance before either objective is solved.

---

# Finite normal-form ladder

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

The repository does **not** claim a new general theory of adaptive experimental design, Set Cover, bisimulation, or graph isomorphism; polynomial-time exact optimization; natural prevalence from finite labeled-task counts; field empirical validation; or that target resolution licenses a biological report.

Current results concern finite deterministic guaranteed target resolution with positive acquisition costs.

## Run

```bash
python -m pip install -e .
python -m pytest -q
python examples/audit_witnesses.py
python examples/audit_certificate_ladder.py
```
