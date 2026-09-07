# Resource-labelled continuation quotient

The cost-only continuation quotient preserves deterministic worst-path adaptive
resolution cost `C_A`, but it deliberately forgets which branch-specific action
is the same physical query.  That omission is harmless for the local Bellman
minimum and can be fatal for the fixed comparator `C_F`.

This note adds the missing resource identity.

## 1. Task-local query tokens

For one declared finite task, every query has a persistent task-local token
`q`.  At a mixed state `s`, retain every productive available query as

\[
(q,\;c(q),\;\{\operatorname{Class}(u):u\in M(s,q)\}),
\]

where `M(s,q)` is the set of target-mixed outcome children.  Pure children are
already resolved and have continuation value zero.  Repeated occurrences of one
child class do not change guaranteed worst-path resolution, but **distinct query
tokens are never merged**.

Two states are placed in one class only when this entire token-labelled recursive
descriptor is identical.

This quotient is task-local.  It does not claim that a query named `left` in one
scientific task is the same resource as a query named `left` in another task.
Cross-task resource alignment would require an explicit externally justified
bijection.

## 2. Adaptive-cost preservation

Let `V_A(K)` be the minimum guaranteed worst-path adaptive cost of resource class
`K`.  Then

\[
V_A(0)=0
\]

for the resolved class and

\[
V_A(K)=\min_{q\in A(K)}
\left[c(q)+\max_{L\in Ch(K,q)}V_A(L)\right],
\]

with infinity when no productive action resolves the state.

Because equal resource classes have the same query tokens, costs, and recursive
mixed-child classes, the equation is identical in every member state.  Hence

\[
\boxed{
K(s)=K(t)\Longrightarrow V_A(s)=V_A(t).
}
\]

This is the labelled analogue of the existing cost-only continuation theorem.

## 3. Fixed bundles on the same quotient

Let `B` be a fixed set of physical query tokens.  A bundle resolves resource
class `K` recursively as follows.

1. `K=0` is resolved.
2. If `B` is empty and `K!=0`, resolution fails.
3. Take one query token `q` from `B`.
4. If `q` has no productive transition in `K`, then it is constant on this
   state (or already absent along this concrete history), so remove it from `B`
   without changing the state.
5. Otherwise apply the **same token `q`** to every branch and require every
   target-mixed child class to resolve under `B\{q}`.

Deterministic noninvasive query application commutes at the level of the final
joint outcome partition, so this replay tests the same fixed bundle that would be
applied to the original worlds.

Therefore bundle resolvability depends only on the resource-labelled quotient and
its persistent query tokens.  Minimizing bundle cost gives

\[
\boxed{
C_F^{\rm resource}=C_F^{\rm original}.
}
\]

Together with the adaptive theorem,

\[
\boxed{
\text{resource-labelled continuation quotient}
\Longrightarrow (C_A,C_F).
}
\]

## 4. Why resource identity is necessary for the joint comparator

The registered collision has four worlds with targets `(0,0,1,1)`.

Strict task:

```text
left  = (0,0,0,1)
right = (0,1,0,0)
route = (0,1,1,0)
```

Bypass task:

```text
left   = (0,0,0,1)
bypass = (0,1,0,1)
route  = (0,1,1,0)
```

The existing **cost-only** recursive quotient gives the two roots the same
continuation class and therefore the same adaptive value `C_A=2`.

But the fixed costs differ:

\[
(C_A,C_F)_{\rm strict}=(2,3),\qquad
(C_A,C_F)_{\rm bypass}=(2,2).
\]

In the strict task, different branches require different physical terminal
queries and all three query identities are necessary for a fixed resolver.  In
the bypass task, the same `bypass` token can be reused as part of one two-query
fixed bundle.

Thus erasing query identity loses information required for `C_F`:

\[
\boxed{
\text{cost-labelled continuation type alone}
\not\Rightarrow C_F.
}
\]

The new quotient retains precisely this branch-crossing resource identity.

## 5. Independent verification

`verify_resource_continuation_quotient()` does not trust the builder's hash
matches.  It reconstructs every reachable state and checks:

- the declared query token and cost on every action;
- availability of each query token;
- every target-mixed child membership;
- exact child-class sets;
- class descriptor uniqueness;
- topological child references;
- complete reachability from the root; and
- the original query-name and query-cost registry.

Changing an action's query token or cost causes rejection.

## 6. Exhaustive validation

The regression suite requires exact agreement with the direct adaptive/fixed
solvers on:

```text
4 worlds, 2+2 targets, 3 binary unit-cost queries
16^3 = 4,096 tasks
```

and

```text
4 worlds, 2+2 targets, 3 arbitrary deterministic partition queries
15^3 = 3,375 tasks.
```

The strict-gain counts must remain respectively `192` and `24`.

These counts are complete finite-universe checks, not empirical prevalence
estimates.

## 7. Scope boundary

The quotient preserves finite deterministic guaranteed target resolution with
positive additive query costs.  It does not establish sufficiency for:

- noisy likelihood observations;
- expected-loss or information-valued objectives;
- randomized policies;
- calibration actions that modify later observation laws;
- continuous unenumerated world sets; or
- scientific report licensing.

It is also not claimed to be the coarsest representation preserving both
`C_A` and `C_F`.  The next question is how far query tokens can themselves be
quotiented or dominated while preserving **global bundle reuse** as well as local
adaptive continuation value.
