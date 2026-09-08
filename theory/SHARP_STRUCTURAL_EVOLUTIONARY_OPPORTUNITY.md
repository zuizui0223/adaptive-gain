# Sharp structural opportunity per unit adaptive effort

## Status

This note does not introduce a new combinatorial theorem. It gives an exact
**evolutionary-timescale interpretation** of the repository's already-proved
sharp adaptive/fixed ratio results.

The purpose is to separate two questions that are often conflated:

1. **How much short-term structural opportunity can one ecological state create?**
2. **How much of state-dependent selection is retained over many generations?**

The first question is already answered exactly by the repository's finite
adaptive-gain mathematics. The second is handled by the temporal-retention layer
in `INFORMATION_MEDIATED_ECO_EVOLUTIONARY_LOOP.md`.

---

## 1. Adaptive-only opportunity without a fitness map

For a nontrivial finite deterministic unit-cost sensing task, let

\[
C_A>0
\]

be the minimum worst-path adaptive resolution cost and

\[
C_F\ge C_A
\]

be the minimum fixed resolving-bundle cost.

For integer sensing budget `B`, adaptive-only guaranteed resolution is possible
exactly on

\[
C_A\le B<C_F.
\]

The number of integer budgets in that window is therefore

\[
\boxed{W=C_F-C_A.}
\]

Normalize by the adaptive effort required to exploit the opportunity:

\[
\boxed{
\Omega
=\frac{W}{C_A}
=\frac{C_F-C_A}{C_A}
=\frac{C_F}{C_A}-1.
}
\]

`Omega` is called the **normalized adaptive-only opportunity**.

It is deliberately structural and fitness-free. It asks:

> per unit adaptive sensing effort, how broad is the budget/deadline range in
> which the contingent architecture can still resolve the relevant state but
> the best fixed architecture cannot?

A biological application may interpret the budget as a decision deadline,
energetic ceiling, predator-exposure limit, handling-time limit, or phenological
opportunity window only when natural history supports that interpretation.

---

## 2. Exact fixed-(n,m,b) maximum

Let

- `n` = represented worlds;
- `m` = declared physical query resources;
- `b` = maximum query arity.

The existing theorem defines

\[
F_b(n,h)
\]

as the exact maximum number of internal-node occurrences in a productive tree
with at most `n` leaves, depth at most `h`, and at most `b` nonempty children per
internal node.

The repository has already proved

\[
R_b(n,m)
=
\max_{1\le h\le n-1}
\frac{\min\{m,F_b(n,h)\}}{h}
=
\max\frac{C_F}{C_A}.
\]

Therefore, by the identity `Omega=C_F/C_A-1`, the exact structural-opportunity
maximum is

\[
\boxed{
\Omega_b^*(n,m)
=R_b(n,m)-1.
}
\]

This is sharp because the underlying ratio bound is sharp.

Thus the finite combinatorics supplies an exact upper envelope on short-term
adaptive-only opportunity at fixed ecological-state complexity and cue
vocabulary size.

---

## 3. Binary-cue closed form

When every observation is binary, let

\[
K=\min(m,n-1),
\qquad
d=\lfloor\log_2(K+1)\rfloor.
\]

The existing sharp ratio is

\[
R_2(n,m)
=
\max\left(
1,
\frac{2^d-1}{d},
\frac{K}{d+1}
\right).
\]

Hence

\[
\boxed{
\Omega_2^*(n,m)
=
\max\left(
1,
\frac{2^d-1}{d},
\frac{K}{d+1}
\right)-1.
}
\]

Large normalized adaptive-only opportunity therefore does not require a
high-arity 'magic cue'. It can arise from sequential binary distinctions.

---

## 4. Unrestricted-arity closed form

When query arity is unrestricted relative to the world set, the existing theorem
is

\[
R_\infty(n,m)
=
\max\left(
1,
\frac{\min\{m,1+\lfloor n/2\rfloor\}}{2}
\right).
\]

Thus

\[
\boxed{
\Omega_\infty^*(n,m)
=
\max\left(
0,
\frac{\min\{m,1+\lfloor n/2\rfloor\}-2}{2}
\right).
}
\]

Depth two is globally extremal for the corresponding ratio theorem. In this
scope, very shallow contingent sensing can therefore create the maximum
opportunity per unit adaptive effort.

---

## 5. Productive-frontier edge count is a real control parameter

Let

\[
\mathcal H_{\min}
\]

be the inclusion-minimal productive frontier and impose

\[
|\mathcal H_{\min}|\le E.
\]

The existing edge-capped theorem gives

\[
R_{b,E}(n,m)
=
\max_h
\frac{\min\{m,E,F_b(n,h)\}}{h}.
\]

Therefore

\[
\boxed{
\Omega_{b,E}^*(n,m)
=R_{b,E}(n,m)-1.
}
\]

This provides a direct structural ecological prediction:

> the number of distinct irreducible productive obligations can cap the maximum
> adaptive-only opportunity.

The wording 'obligation' is intentional. An edge of the minimal productive
frontier is not simply another available cue. It is a minimal set that a fixed
resolver must hit in order to avoid leaving some reachable target-mixed state
unresolved.

Consequently, a community state with fewer distinct irreducible cue obligations
can have a lower worst-case structural opportunity for contingent sensing even
when the raw cue vocabulary is large.

---

## 6. Frontier rank is not a control parameter in the extremal sense

Define frontier rank by

\[
\operatorname{rank}(\mathcal H_{\min})
=
\max_{E\in\mathcal H_{\min}}|E|.
\]

The repository already proves that for every positive rank cap `r>=1`,

\[
R_{b,\operatorname{rank}\le r}(n,m)=R_b(n,m).
\]

Therefore

\[
\boxed{
\Omega_{b,\operatorname{rank}\le r}^*(n,m)
=
\Omega_b^*(n,m),
\qquad r\ge1.
}
\]

Ecologically, merely bounding how many cues can coexist inside one irreducible
obligation does not control worst-case adaptive-only opportunity. Rank-one
singleton obligations already attain the sharp extremum.

This yields a useful contrast:

```text
number of irreducible obligations       -> can cap opportunity
size of the largest single obligation   -> cannot cap worst-case opportunity
```

The statement is extremal, not a claim that edge count will always dominate rank
empirically in every natural system.

---

## 7. Existing source-derived routing task already sits on the sharp boundary

The registered `payoff_routing_task()` has

\[
(C_A,C_F)=(2,3),
\]

so

\[
\Omega=\frac12.
\]

It has four represented worlds, three unit-cost binary queries, hence

\[
(n,m,b)=(4,3,2).
\]

For that scope, the sharp binary theorem gives

\[
R_2(4,3)=\frac32,
\qquad
\Omega_2^*(4,3)=\frac12.
\]

Thus this previously registered source-derived synthetic abstraction is not just
a strict-gain example: it attains the exact normalized adaptive-only opportunity
maximum in its finite `(n,m,b)` scope.

This remains a synthetic/conditional structural witness, not empirical evidence
that a natural community realizes those worlds and cues.

---

## 8. Short-term amplitude generator versus long-term retention filter

The timescale branch can now be written as two mathematically distinct layers.

### Within a community state

\[
\boxed{
\Omega(X)
=\frac{C_F(X)-C_A(X)}{C_A(X)}
}
\]

measures normalized structural opportunity.

Its maximum is controlled by the already-solved finite combinatorics:

\[
(n,m,b,|\mathcal H_{\min}|,\ldots).
\]

### Across generations

If a biological fitness map turns the current structural state into a selection
coefficient `s_t`, define

\[
A_H=\sum_{t=1}^H|s_t|
\]

and

\[
R_H=\left|\sum_{t=1}^Hs_t\right|.
\]

The retention ratio is

\[
\boxed{
\mathcal R_H=R_H/A_H
}
\]

when `A_H>0`.

Therefore the conceptual decomposition is

\[
\boxed{
\text{short-term evolutionary amplitude}
\;\leftarrow\;
\text{state-specific structural opportunity},
}
\]

while

\[
\boxed{
\text{long-term directional accumulation}
\;\leftarrow\;
\text{temporal coherence of selection}.
}
\]

A state can repeatedly create large `Omega` while long-term retained change is
small if the resulting selection direction alternates. Conversely, moderate
state-specific opportunity can accumulate strongly when selection remains
coherent over time.

This is why 'rapid short-term evolution' and 'large long-term evolution' should
not be represented by one rate parameter.

---

## 9. Natural-history interpretation

The theorem does not decide what the worlds, cues, target, or budget mean.
Natural history supplies those mappings.

Examples of possible finite cue structure include

```text
far-range -> approach -> near-range -> contact -> handling
```

or

```text
habitat -> host identity -> surface chemistry -> oviposition
```

or

```text
flower detection -> approach -> landing -> reward assessment -> revisit
```

Community state can alter

- which cues exist;
- which cues co-occur;
- which sequential continuations are feasible;
- which fixed shortcuts exist;
- how many irreducible productive obligations the individual faces.

Those changes alter the structural objects already solved by the repository.

The empirical question suggested by the edge/rank contrast is not merely

> how many cues are involved in a decision?

but more specifically

> how many distinct irreducible context-specific obligations must a noncontingent
> sensory strategy cover simultaneously?

---

## 10. Scope boundary

This note inherits all limitations of the deterministic unit-cost extremal layer.
It does not yet prove analogous sharp opportunity bounds for

- unequal cue costs;
- noisy observations;
- continuous ecological state spaces;
- explicit evolving sensory traits;
- demographic feedbacks;
- drift, mutation, migration, or diploid genetics;
- speciation or macroevolutionary lineage dynamics.

The evolutionary contribution is currently a structural bridge and a set of
exact constraints on possible state-specific opportunity, followed by a separate
temporal-retention model.
