# Structural phase-exclusion bounds from finite sensing constraints

## Status

This note does **not** prove a new finite-task extremal theorem. It reuses the
repository's existing bounded-arity tree-union bound and productive-frontier edge
bound to obtain rigorous impossibility certificates for the endogenous
feedback model.

The key idea is simple:

> if the finite sensing structure cannot generate enough adaptive/fixed gap, then
> no amount of dynamical interpretation can place the closed loop in a phase that
> requires a larger structural loop gain.

---

## 1. Existing finite-task bound

For a unit-cost deterministic task with

- `n` represented worlds;
- `m` declared queries;
- maximum query arity `b`;
- adaptive optimum

\[
C_A=h,
\]

the existing bounded-arity theorem gives

\[
\boxed{
C_F\le \min\{m,F_b(n,h)\}.
}
\]

Here `F_b(n,h)` is the exact maximum number of internal-node occurrences in a
productive bounded-arity decision tree with at most `n` nonempty leaves and
height at most `h`.

Therefore

\[
\boxed{
C_F-C_A
\le
\min\{m,F_b(n,h)\}-h.
}
\]

Let

\[
D_b(n,m,h)
=
\min\{m,F_b(n,h)\}-h.
\]

This is an upper bound on the high-state structural gap when adaptive cost is
fixed to `h`.

---

## 2. Lift to endogenous loop gain

Suppose the low community state is a gap-zero control and the high state lies in
the finite sensing scope above.

Under the continuous structural lift,

\[
\Delta s
=\lambda\Delta g,
\]

with

\[
\Delta g\le D_b(n,m,h).
\]

For restoring negative feedback

\[
\eta<0
\]

and interior equilibrium frequency `p*`, the loop gain is

\[
L
=-\eta\Delta s\,p^*(1-p^*).
\]

Hence

\[
\boxed{
L
\le
L_{\max}
:=
(-\eta)\lambda p^*(1-p^*)
D_b(n,m,h).
}
\]

This statement is one-sided. It does not assert that every value below
`L_max` is attainable. It is useful because values above `L_max` are rigorously
impossible under the declared finite structural scope.

---

## 3. Excluding damped oscillation

The exact local feedback phase diagram gives damped oscillation only when

\[
L>\frac{1-\phi}{4}.
\]

Therefore, if

\[
\boxed{
L_{\max}
\le
\frac{1-\phi}{4},
}
\]

then no task with the declared `(n,m,b,h)` scope can generate the stable damped
phase against a gap-zero control under the stated feedback parameters.

This is a **structural no-oscillation certificate**.

It is stronger than observing no oscillation in one simulation: it excludes the
phase for the entire finite task class covered by the bound.

---

## 4. Excluding strong-feedback instability

The strong negative-feedback instability boundary is

\[
L=1.
\]

Thus, if

\[
\boxed{
L_{\max}<1,
}
\]

then the entire declared finite sensing scope is incapable of reaching the
strong-feedback unit-circle instability through structural gap amplification.

Again, this is an impossibility result, not a claim that `L_max>=1` guarantees an
unstable witness.

---

## 5. Productive-frontier edge cap strengthens the certificate

Under unit costs,

\[
C_F
=\tau(\mathcal H_{\min})
\le
|\mathcal H_{\min}|.
\]

If the inclusion-minimal productive frontier has edge-count cap

\[
|\mathcal H_{\min}|\le E,
\]

then

\[
\boxed{
C_F
\le
\min\{m,E,F_b(n,h)\}.
}
\]

So the structural gap bound becomes

\[
\boxed{
D_{b,E}(n,m,h)
=
\min\{m,E,F_b(n,h)\}-h.
}
\]

and

\[
L_{\max,E}
=
(-\eta)\lambda p^*(1-p^*)D_{b,E}(n,m,h).
\]

This makes productive-frontier edge count a direct dynamical control parameter.

Reducing the number of irreducible productive obligations can make oscillatory
or unstable eco-evolutionary feedback structurally impossible.

---

## 6. Frontier rank does not provide the same protection

The parent repository proves a negative extremal result:

> every positive cap on productive-frontier rank leaves the sharp
> adaptive/fixed ratio unchanged.

Rank-one singleton obligations can already attain the worst adaptive/fixed
separation.

Therefore a rank cap alone is **not** promoted here as a general phase-exclusion
mechanism.

This gives a useful ecological distinction:

```text
number of irreducible cue obligations
    can bound feedback amplification

size of each individual obligation
    need not bound worst-case amplification
```

The structure of obligation multiplicity matters more than merely limiting how
many cues occur inside one obligation.

---

## 7. Minimal repo-native boundary witness

For `payoff_routing_task()`:

\[
(n,m,b,h)=(4,3,2,2).
\]

The existing theorem gives

\[
F_2(4,2)=3,
\]

so

\[
D_2(4,3,2)=3-2=1.
\]

The task itself has

\[
C_A=2,
\qquad
C_F=3,
\]

so it **attains** this gap bound.

Against `routing_bypass_control()` with gap zero, take

\[
\lambda=1,
\qquad
\eta=-\frac12,
\qquad
p^*=\frac12.
\]

Then

\[
L_{\max}
=
\frac12\cdot1\cdot\frac14\cdot1
=
\frac18.
\]

At

\[
\phi=\frac12,
\]

the damped-oscillation threshold is also

\[
\frac{1-\phi}{4}=\frac18.
\]

Because damped oscillation requires a **strict** inequality,

\[
L>\frac18,
\]

the entire `(4,3,2,2)` scope is certified nonoscillatory under these feedback
parameters.

The registered task sits exactly on that structural boundary.

---

## 8. Larger binary scope can permit oscillation but still exclude instability

For

\[
(n,m,b,h)=(12,12,2,3),
\]

the existing recurrence gives

\[
F_2(12,3)=7.
\]

Hence

\[
D_2=7-3=4.
\]

With

\[
\lambda=1,
\quad
\eta=-\frac12,
\quad
p^*=\frac12,
\quad
\phi=\frac12,
\]

we obtain

\[
L_{\max}
=\frac12.
\]

Thus

\[
L_{\max}>\frac18,
\]

so damped oscillation is no longer structurally excluded, while

\[
L_{\max}<1,
\]

so strong-feedback instability is still rigorously excluded.

This illustrates why the two phase boundaries carry distinct information.

---

## 9. Edge-count cap can remove all adaptive amplification

Keep

\[
(n,m,b,h)=(12,12,2,3)
\]

but impose

\[
E=3.
\]

Then

\[
C_F\le3=h,
\]

so

\[
D_{b,E}=0.
\]

Consequently

\[
\boxed{L_{\max,E}=0}
\]

for every negative feedback magnitude and every nonnegative `lambda` in this
fixed-`h` scope.

The structural class cannot amplify feedback through adaptive/fixed separation at
all.

---

## 10. Biological reading

The bound separates two reasons a natural system might lack complex
eco-evolutionary dynamics.

### Weak ecological feedback

Even large structural gaps may not matter if

\[
|\eta|
\]

is small.

### Structural inability to generate a large reward contrast

Even strong ecological feedback may remain dynamically simple when the cue system
has too few worlds, too few physical cues, insufficient decision-tree branching,
or too few irreducible productive obligations to produce a large `C_F-C_A` gap.

This is important empirically because it creates a falsifiable alternative to
"the feedback slope is weak".

A system may fail to oscillate because its natural-history sensing structure does
not permit enough closed-loop gain in the first place.

---

## 11. Scope boundary

The certificates apply to

- finite deterministic target-resolution tasks;
- unit query costs;
- declared world count, query count, maximum query arity, and adaptive cost;
- optional productive-frontier edge-count cap;
- a gap-zero low-state comparator;
- the continuous structural fitness lift;
- local endogenous feedback as defined in the dependent feedback branch.

A `possible=True` result from the executable helper means only that the existing
upper bound does not exclude the phase. It is **not** an existence theorem.

A `possible=False` result is the strong conclusion: the phase is structurally
unreachable under the declared assumptions.
