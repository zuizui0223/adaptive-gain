# Higher-order cue structure can reverse hard-budget selection

## Status

This note combines two **existing repository results** with the budget-gated evolutionary lift:

1. the registered `resource_role_profile_collision()`;
2. the exact adaptive-only budget window `C_A <= B < C_F`.

The point is to remove the linear cost-to-fitness assumption from the higher-order community-structure counterexample.

---

## 1. Existing collision

The two registered finite tasks have

- the same adaptive continuation root type;
- the same multiset of complete per-resource abstract role profiles;
- the same adaptive cost `C_A=2`;
- different fixed costs.

Call them `X_0` and `X_1`, with

\[
(C_A,C_F)(X_0)=(2,2)
\]

and

\[
(C_A,C_F)(X_1)=(2,3).
\]

Therefore the structural difference is entirely on the fixed/productive-frontier side:

\[
\Delta C_A=0,
\qquad
\Delta C_F=1.
\]

The earlier linear lift showed that this can reverse selection at an intermediate maintenance cost.

---

## 2. Put both states under the same hard ecological budget

Choose

\[
\boxed{B=2.}
\]

In `X_0`,

\[
C_A=C_F=2,
\]

so both architectures complete target resolution before the budget expires.

In `X_1`,

\[
C_A=2<C_F=3,
\]

so

\[
\boxed{C_A\le B<C_F}
\]

and only the contingent architecture completes resolution.

Thus the same external budget moves from

```text
both architectures feasible
```

to

```text
adaptive-only feasible
```

without changing `C_A`.

---

## 3. Positive threshold fitness model

Use

\[
W_A=e^{-\kappa}[w_0+vS_A],
\]

\[
W_F=w_0+vS_F,
\]

with

\[
w_0=v=1.
\]

Then in `X_0`, both succeed, so

\[
s_0=\log(W_A/W_F)=-\kappa.
\]

In `X_1`, only adaptive succeeds, so

\[
s_1=\log2-\kappa.
\]

Choose

\[
\boxed{\kappa=\frac12\log2.}
\]

Then

\[
\boxed{s_0=-\frac12\log2,}
\]

and

\[
\boxed{s_1=+\frac12\log2.}
\]

Therefore

\[
\boxed{
\text{the registered higher-order resource collision reverses selection under a hard shared budget, without any linear mapping from cost savings to fitness.}
}
\]

---

## 4. What information stays unchanged

Across the two tasks, the following weaker summaries are unchanged:

- adaptive continuation root type;
- adaptive cost `C_A`;
- multiset of complete per-resource role profiles.

Yet the hard-budget evolutionary outcome switches from selection against contingent control to selection for it.

Therefore these summaries are insufficient not only for recovering `C_F`, but also for predicting the sign of selection in this explicit budget-gated evolutionary model.

The missing information is higher-order co-location structure that changes the fixed resolving burden.

---

## 5. Exact burst–stasis cycle

Alternate community states

\[
X_1,X_0,X_1,X_0,\ldots
\]

under the same budget and maintenance cost.

Then

\[
s_t=+s,-s,+s,-s,\ldots
\]

with

\[
s=\frac12\log2.
\]

For haploid viability selection,

\[
\operatorname{logit}(p_{t+1})
=
\operatorname{logit}(p_t)+s_t.
\]

Hence every odd generation moves,

\[
p_{2n+1}\ne p_{2n}
\]

for interior frequencies, but

\[
\boxed{p_{2n}=p_0.}
\]

Thus higher-order cue-structure switching alone is sufficient, in this explicit conditional model, to generate

\[
\boxed{
\text{rapid reversible short-term evolution}
+
\text{zero retained two-cycle displacement}.
}
\]

---

## 6. Ecological reading

The mathematical collision should not be confused with an already-demonstrated natural mechanism.

Its ecological interpretation is a hypothesis about community organization:

> two community states may present similar marginal cue roles and the same individual adaptive decision complexity, while differing in which cue obligations are co-located across ecological situations. That higher-order rearrangement can create or destroy a fixed shortcut and move a hard ecological deadline into or out of the adaptive-only budget window.

Potential natural-history sources include

- different partner-species combinations;
- stage-specific cue co-occurrence;
- changes in which signals are jointly available after approach/contact;
- appearance of a broadly diagnostic external cue;
- disappearance of a fixed bypass when community composition changes.

The empirical target is therefore not only cue frequency but the **state-conditioned joint arrangement of cue usefulness**.

---

## 7. Why this strengthens the branch

The branch now has two independent structural-selection lifts.

### Linear cost-value witness

\[
s=\lambda(C_F-C_A)-\kappa.
\]

The collision reverses selection because the exact gap changes from 0 to 1.

### Hard-budget witness

\[
S_A-S_F=\mathbf1\{C_A\le B<C_F\}.
\]

The same collision reverses selection because `B=2` lies outside the adaptive-only window in one state and inside it in the other.

The qualitative conclusion therefore does not depend on a single linear conversion of sensing cost to fitness.

Executable regression: `tests/test_budget_gated_structural_collision.py`.
