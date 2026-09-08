# Budget-gated evolutionary selection from exact adaptive-only windows

## Status

This note gives a second evolutionary lift of the repository's deterministic mathematics.

Unlike the linear cost-to-log-fitness map

\[
s(X)=\lambda[C_F(X)-C_A(X)]-\kappa,
\]

this construction does **not** assign a linear fitness value to each unit of sensing cost.

Instead it uses one of the repository's most direct exact consequences:

\[
\boxed{
C_A\le B<C_F
}
\]

is precisely a budget range in which adaptive target resolution is feasible but fixed resolution is not.

The ecological interpretation can be a hard time, energy, exposure, or opportunity budget.

---

## 1. Exact resolution indicators

For a finite sensing task in community state `X`, define

\[
S_A(X,B)=\mathbf 1\{C_A(X)\le B\},
\]

and

\[
S_F(X,B)=\mathbf 1\{C_F(X)\le B\}.
\]

Because the repository proves

\[
C_A(X)\le C_F(X),
\]

we always have

\[
S_A(X,B)\ge S_F(X,B).
\]

Moreover,

\[
\boxed{
S_A-S_F=1
\iff
C_A(X)\le B<C_F(X).
}
\]

Thus the strict adaptive-gain budget window is exactly the adaptive-only success window.

---

## 2. Minimal positive fitness model

Let

- `w0>0` be baseline fitness;
- `v>=0` be the fitness benefit of resolving the target before the budget expires;
- `kappa>=0` be the log maintenance cost of contingent sensory control.

Define

\[
W_A
=e^{-\kappa}[w_0+vS_A(X,B)],
\]

and

\[
W_F
=w_0+vS_F(X,B).
\]

Then

\[
\boxed{
s_B(X)=\log\frac{W_A}{W_F}.}
\]

This is a threshold fitness model: saving an extra unit of sensing cost has no effect unless it moves an architecture across the hard ecological budget.

---

## 3. Three budget regions

### Both fail

If

\[
B<C_A,
\]

then

\[
S_A=S_F=0
\]

and

\[
\boxed{s_B=-\kappa.}
\]

Contingent control pays a maintenance cost but gains no resolution benefit.

### Adaptive-only window

If

\[
C_A\le B<C_F,
\]

then

\[
S_A=1,\qquad S_F=0,
\]

so

\[
\boxed{
s_B
=\log\frac{w_0+v}{w_0}-\kappa.}
\]

Adaptive sensing is favoured exactly when

\[
\boxed{
\kappa
<
\log\frac{w_0+v}{w_0}.
}
\]

### Both succeed

If

\[
B\ge C_F,
\]

then

\[
S_A=S_F=1
\]

and again

\[
\boxed{s_B=-\kappa.}
\]

Once the ecological budget is generous enough for a fixed resolver, exact deterministic resolution alone no longer repays maintenance of contingent control.

Thus selection is concentrated on the repository's exact adaptive-only budget interval.

---

## 4. Community state changes the evolutionary budget window

Community state changes can move the endpoints

\[
[C_A(X),C_F(X)).
\]

through the same two structural channels described elsewhere:

- continuation structure moves `C_A`;
- productive-frontier structure moves `C_F`.

Therefore a fixed external budget `B` can lie

- outside the window in one community;
- inside the window in another.

This creates a state-dependent selection switch even if the organism's physiological budget does not change.

---

## 5. Exact repository-native reversal witness

Use two existing tasks.

### Strict routing state

`payoff_routing_task()` has

\[
C_A=2,
\qquad
C_F=3.
\]

At

\[
B=2,
\]

this state lies in the adaptive-only window.

Hence

\[
s_+
=\log\frac{w_0+v}{w_0}-\kappa.
\]

### Fixed-bypass state

`routing_bypass_control()` has

\[
C_A=C_F=2.
\]

At the same budget

\[
B=2,
\]

both architectures resolve the target, so

\[
s_-=-\kappa.
\]

Choose

\[
w_0=v=1
\]

and

\[
\boxed{
\kappa=\frac12\log2.
}
\]

Then

\[
\boxed{
s_+=+\frac12\log2,}
\]

and

\[
\boxed{
s_-=-\frac12\log2.}
\]

Thus alternation of the two community states gives exact opposing selection without any linear cost-to-fitness assumption.

---

## 6. Rapid short-term evolution with exact long-term return

Under the exact haploid log-odds recurrence

\[
\operatorname{logit}(p_{t+1})
=
\operatorname{logit}(p_t)+s_t,
\]

an alternating sequence

\[
+s,-s,+s,-s,\ldots
\]

satisfies

\[
\boxed{p_{2n}=p_0.}
\]

Yet each odd generation has

\[
p_{2n+1}\ne p_{2n}
\]

for an interior allele frequency and `s!=0`.

So this budget-gated model reproduces the branch's central timescale phenomenon:

\[
\boxed{
\text{nonzero evolutionary movement every generation}
+
\text{zero retained change after each two-state cycle}.
}
\]

Here the reversal is caused specifically by movement into and out of an adaptive-only resolution window.

---

## 7. Why this is useful for natural history

A hard budget has several possible biological meanings, but each must be justified for the focal system.

Examples include

- time before a predator attack must be classified;
- time before a moving host, mate, prey, or pollinator is lost;
- energetic budget available for sensory sampling;
- handling-time deadline before abandoning a resource;
- a developmental or phenological window in which a decision remains useful.

Natural history determines whether such a hard constraint is plausible and which cue sequence is physically feasible before the deadline.

This creates a direct role for detailed observation:

```text
natural-history timing
-> biological budget B
-> location relative to [C_A,C_F)
-> adaptive-only success or not
-> selection on contingent architecture.
```

---

## 8. Relation to the linear structural selection model

The linear model and budget-gated model answer different questions.

### Linear cost model

\[
s=\lambda(C_F-C_A)-\kappa
\]

is useful when every unit of sensing cost plausibly contributes to fitness.

### Budget-gated model

\[
s_B
=\log\frac{w_0+v\mathbf1\{C_A\le B\}}
{w_0+v\mathbf1\{C_F\le B\}}
-\kappa
\]

is useful when ecological performance depends mainly on completing resolution before a deadline or resource ceiling.

The second model uses the repository's strict-gain budget window more directly and avoids assuming linear conversion of sensing cost into fitness.

A robust biological argument should prefer whichever mapping is justified by the natural history rather than treating either as universal.

---

## 9. Scope

This result remains conditional on deterministic exact target resolution.

It does not yet model

- graded accuracy below full resolution;
- stochastic cue errors;
- variable individual budgets;
- continuous time-to-decision distributions;
- demographic consequences beyond the stated positive fitness map.

The exact statement is:

> given a hard budget `B`, the repository's interval `C_A<=B<C_F` is exactly the region in which contingent sensing can resolve the target while every fixed resolving bundle exceeds the budget.

The evolutionary fitness consequences then follow from the explicitly stated threshold payoff model.

Executable implementation: `adaptive_gain/budget_gated_selection.py`.

Tests: `tests/test_budget_gated_selection.py`.
