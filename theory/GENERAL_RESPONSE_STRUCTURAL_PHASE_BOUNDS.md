# Structural phase bounds under a generalized evolutionary response

## Status

This note composes two already-established layers:

1. the repository's finite unit-cost bound on the structural gap `C_F-C_A`;
2. the generalized local evolutionary-response phase thresholds.

No new bounded-arity combinatorial theorem or generic stability theorem is claimed. The repository-specific consequence is that the same exact sensing constraints can now certify dynamical impossibility beyond the parent haploid-logit model.

---

## 1. Finite structural gap ceiling

For a high-opportunity unit-cost sensing task with

- `n` represented worlds;
- `m` declared queries;
- maximum query arity `b`;
- adaptive optimum `C_A=h`;

and a gap-zero low-state comparator, the inherited theorem gives

\[
\boxed{
\Delta g
\le
G_{gap}^{max}
:=
\min\{m,F_b(n,h)\}-h.
}
\]

With productive-frontier edge cap `E`,

\[
\boxed{
G_{gap,E}^{max}
=\min\{m,E,F_b(n,h)\}-h.
}
\]

---

## 2. Generalized gain per structural gap

Under the continuous structural lift,

\[
\Delta s=\lambda\Delta g.
\]

The generalized response has

\[
G=-\beta\Delta s\,e.
\]

For restoring ecological feedback

\[
e<0,
\]

and

\[
\beta,\lambda\ge0,
\]

define

\[
\boxed{
a_g=(-\beta e)\lambda.}
\]

Then

\[
\boxed{G=a_g\Delta g}
\]

and hence

\[
\boxed{
G\le G_{max}:=a_g G_{gap}^{max}.
}
\]

This separates

```text
structural ceiling       G_gap^max
biological conversion    a_g=(-beta e)lambda
```

before they combine into the dynamical gain ceiling.

---

## 3. Generalized response thresholds

For

\[
0\le\alpha\le1,
\qquad
0\le\phi<1,
\]

define

\[
G_- = \alpha-1,
\]

\[
G_{osc}
=\frac{(\alpha-\phi)^2}{4(1-\phi)},
\]

\[
G_+
=\frac{1-\alpha\phi}{1-\phi}.
\]

Under restoring feedback, `G>=0`, so the lower threshold does not constrain the positive structural-gain direction. The two relevant upper questions are whether finite sensing structure can reach `G_osc` and `G_+`.

---

## 4. Structural no-damped-oscillation certificate

Stable damped oscillation requires

\[
G>G_{osc}.
\]

Therefore, if

\[
\boxed{
G_{max}\le G_{osc},
}
\]

then **no task in the declared finite sensing scope** can generate a stable damped oscillation through this structural-gap mechanism under the stated generalized response parameters.

This is a class-level impossibility statement, not merely a failed simulation.

---

## 5. Structural upper-instability exclusion

The upper unit-circle boundary is

\[
G=G_+.
\]

Therefore, if

\[
\boxed{
G_{max}<G_+,
}

then strong-feedback upper instability is structurally impossible throughout the declared sensing scope.

Again, `G_max>=G_+` means only "not excluded by this bound." It is not an existence theorem for a task attaining the boundary.

---

## 6. Exact recovery of the parent structural certificate

For the parent haploid-logit coordinate,

\[
\alpha=1,
\qquad
\beta=1,
\qquad
e=\eta p^*(1-p^*).
\]

Hence

\[
G=L,
\]

\[
G_{osc}=\frac{1-\phi}{4},
\qquad
G_+=1.
\]

The generalized certificates reduce exactly to the parent PR #3 rules:

```text
L_max <= (1-phi)/4
    -> stable damped oscillation impossible

L_max < 1
    -> upper feedback instability impossible
```

So the new bound is a strict generalization, not a parallel model.

---

## 7. Same sensing scope, different response geometry

Take the minimal four-world structural scope

\[
(n,m,b,h)=(4,3,2,2).
\]

The inherited gap ceiling is

\[
G_{gap}^{max}=1.
\]

Let

\[
a_g=\frac18,
\qquad
\phi=\frac12.
\]

Then

\[
G_{max}=\frac18.
\]

### Parent response

For

\[
\alpha=1,
\]

\[
G_{osc}=\frac18.
\]

Because damped oscillation requires a strict inequality,

\[
G>G_{osc},
\]

the entire structural scope is certified nonoscillatory.

### Intrinsically damped evolutionary response

For

\[
\alpha=0.7,
\]

with the same `phi=0.5`,

\[
G_{osc}
=\frac{(0.7-0.5)^2}{4(0.5)}
=0.02.
\]

Now

\[
G_{max}=0.125>0.02.
\]

So damped oscillation is **no longer excluded** even though the sensing scope and maximum structural gap have not changed.

This is a central interpretation:

> finite sensing structure constrains the available dynamical gain, but evolutionary-response geometry determines where the dynamical phase boundaries sit.

Neither layer alone determines the phase.

---

## 8. Medium binary scope

For

\[
(n,m,b,h)=(12,12,2,3),
\]

the inherited gap upper bound is

\[
G_{gap}^{max}=4.
\]

With

\[
a_g=0.125,
\qquad
\alpha=0.8,
\qquad
\phi=0.5,
\]

we obtain

\[
G_{max}=0.5,
\]

\[
G_{osc}=0.045,
\]

\[
G_+=1.2.
\]

Thus stable damped dynamics are not structurally excluded, while upper instability remains impossible under the entire declared scope.

Increasing response conversion to

\[
a_g=0.4
\]

would instead give

\[
G_{max}=1.6>G_+,
\]

so the finite structural bound no longer excludes the upper instability phase.

---

## 9. Productive-frontier edge cap

The inherited edge-count cap enters unchanged.

For example, at

\[
(n,m,b,h)=(12,12,2,3)
\]

and

\[
E=3,
\]

we have

\[
G_{gap,E}^{max}=0.
\]

Therefore

\[
G_{max}=0
\]

for any nonnegative `beta,lambda` and any restoring `e<0`.

No structural adaptive-gap amplification is available, so neither damped nor upper-instability phases can be generated through this mechanism regardless of the generalized evolutionary-response parameters.

As in the parent theory, a frontier-rank cap is not promoted as an analogous safety certificate because rank-one obligations can already attain the extremal adaptive/fixed separation.

---

## 10. Biological reading

The phase ceiling now has two independent sources.

### Natural-history / sensing architecture

Controls

\[
G_{gap}^{max}
\]

through world count, cue count, cue arity, adaptive depth, and irreducible productive obligations.

### Evolutionary and ecological response

Controls both

\[
a_g=(-\beta e)\lambda
\]

and the phase thresholds through

\[
\alpha,\phi.
\]

Hence two systems with the same observable cue architecture can have different dynamics because their heritable response or ecological effect differs. Conversely, similar dynamics can arise from different combinations of structural gap and response coefficients.

That is why the inverse/empirical branch treats the factorization of loop gain as an identifiability problem rather than reading mechanism directly from the time series.

---

## 11. Claim boundary

`damped_oscillation_possible=True` or `upper_instability_possible=True` means only that the inherited structural upper bound does not exclude the phase. It is not an existence theorem.

A `False` value is the strong conclusion: no finite unit-cost task in the declared scope can create enough generalized structural gain to reach that phase under the stated local response parameters.

The result remains tied to

- unit-cost deterministic finite sensing tasks;
- a gap-zero low-state comparator;
- the continuous structural lift;
- restoring ecological feedback `e<0`;
- the local scalar generalized-response model.
