# Structural loop gain and the eco-evolutionary phase diagram

## Status and claim boundary

This note closes the local deterministic phase diagram for the minimal endogenous
community-feedback model in `ENDOGENOUS_COMMUNITY_FEEDBACK.md`.

The discrete-time Jacobian, Jury stability conditions, damped-oscillation
boundary, and feedback-gain algebra are standard dynamical-systems results.  The
repository does **not** claim those mathematical tools as new.

The repository-specific result is the upstream identification

\[
\boxed{
\text{exact adaptive/fixed structural gap contrast}
\longrightarrow
\text{closed-loop eco-evolutionary gain}.
}
\]

Because the gap contrast is already constrained by the repository's sharp
finite-task theorems, those combinatorial results now imply exact dynamical phase
crossings in the feedback model.

---

## 1. Closed feedback model

Let

\[
p_t\in[0,1]
\]

be the frequency of the contingent sensing architecture and

\[
q_t\in[0,1]
\]

be the occupancy of a high-opportunity community state.

Community occupancy relaxes toward a phenotype-dependent target

\[
q_{\rm target}(p)
=q_0+\eta\left(p-\frac12\right),
\]

with memory

\[
0\le\phi<1:
\]

\[
q_{t+1}
=
\phi q_t
+(1-\phi)q_{\rm target}(p_t).
\]

State-specific log-fitness rewards are

\[
s_-<s_+,
\qquad
\Delta s=s_+-s_->0.
\]

The exact haploid log-odds update is

\[
\operatorname{logit}(p_{t+1})
=
\operatorname{logit}(p_t)
+s_-+\Delta s\,q_t.
\]

At an interior equilibrium,

\[
q^*=-\frac{s_-}{\Delta s}
\]

and

\[
q_{\rm target}(p^*)=q^*.
\]

---

## 2. Exact Jacobian

Use local coordinates

\[
z=\operatorname{logit}(p),
\qquad q.
\]

Because

\[
\frac{dp}{dz}=p(1-p),
\]

the interior Jacobian is

\[
\boxed{
J=
\begin{pmatrix}
1 & \Delta s\\
(1-\phi)\eta p^*(1-p^*) & \phi
\end{pmatrix}.
}
\]

Let

\[
r=p^*(1-p^*)>0.
\]

Then

\[
\operatorname{tr}J=1+\phi
\]

and

\[
\det J
=\phi-(1-\phi)\eta\Delta s\,r.
\]

---

## 3. Dimensionless loop gain

Define

\[
\boxed{
L=-\eta\Delta s\,r.
}
\]

For the biologically restoring case

\[
\eta<0,
\qquad \Delta s>0,
\]

we have

\[
L>0.
\]

The determinant becomes

\[
\boxed{
\det J=\phi+(1-\phi)L.
}
\]

The entire local feedback problem is therefore compressed to two dimensionless
numbers:

```text
L    closed-loop structural feedback gain
phi  community memory
```

`L` combines

- ecological feedback sensitivity `eta`;
- state-specific selection contrast `Delta s`;
- local evolutionary responsiveness `p*(1-p*)`.

---

## 4. Exact stability interval

For a second-order discrete system with characteristic polynomial

\[
\lambda^2-T\lambda+D,
\]

the Jury conditions are

\[
1-T+D>0,
\]

\[
1+T+D>0,
\]

\[
1-D>0.
\]

Substituting

\[
T=1+\phi,
\qquad
D=\phi+(1-\phi)L
\]

gives

\[
1-T+D=(1-\phi)L,
\]

\[
1+T+D=2+2\phi+(1-\phi)L,
\]

\[
1-D=(1-\phi)(1-L).
\]

For

\[
0\le\phi<1,
\]

the middle inequality is automatic whenever `L>0`.  Hence

\[
\boxed{
\text{local asymptotic stability}
\iff
0<L<1.
}
\]

Equivalently,

\[
\boxed{
-\frac{1}{\Delta s\,p^*(1-p^*)}
<\eta<0.
}
\]

This has three immediate biological regimes.

### Positive or non-restoring feedback

\[
L\le0
\]

fails to restore an interior polymorphism.

### Moderate negative feedback

\[
0<L<1
\]

stabilizes the interior state.

### Excessive negative feedback

\[
L\ge1
\]

overshoots in discrete time and destabilizes the interior state again.

Thus stronger negative ecological feedback is not monotonically stabilizing.

---

## 5. Monotone versus damped-oscillatory return

The characteristic discriminant is

\[
\Delta_J
=(1+\phi)^2
-4[\phi+(1-\phi)L].
\]

It factorizes exactly as

\[
\boxed{
\Delta_J
=(1-\phi)[(1-\phi)-4L].
}
\]

For a stable equilibrium,

\[
0<L<1,
\]

the eigenvalues are a complex conjugate pair exactly when

\[
\boxed{
L>\frac{1-\phi}{4}.
}
\]

Therefore the complete local phase diagram is

```text
L <= 0
    unstable non-restoring / positive feedback

0 < L <= (1-phi)/4
    stable nonoscillatory return

(1-phi)/4 < L < 1
    stable damped eco-evolutionary oscillation

L >= 1
    unstable negative-feedback overshoot
```

Community memory changes the transient boundary but not the basic stability
interval.

As

\[
\phi\uparrow1,
\]

the oscillation threshold

\[
\frac{1-\phi}{4}
\]

approaches zero.  Hence even weak restoring feedback can produce long damped
cycles when community states have long memory.

---

## 6. Structural gap enters the loop literally

Under the continuous structural lift,

\[
s_i
=\lambda g_i-\kappa,
\qquad
\g_i=C_F(i)-C_A(i).
\]

The common maintenance cost cancels from the state contrast:

\[
\Delta s
=\lambda\Delta g,
\]

where

\[
\Delta g=g_+-g_-.
\]

Hence

\[
\boxed{
L
=-\eta\lambda\Delta g\,p^*(1-p^*).
}
\]

This is the key connection to the original repository mathematics.

The same exact quantity that measures how much more fixed sensing must pay in one
community state now acts as a dynamical feedback amplifier when evolution feeds
back onto community occupancy.

At the centered equilibrium

\[
p^*=\frac12,
\]

we get

\[
\boxed{
L
=-\frac{\eta\lambda\Delta g}{4}.
}
\]

---

## 7. Repo-native minimal witness

Use existing tasks

- `routing_bypass_control()` with gap `0`;
- `payoff_routing_task()` with gap `1`.

With

\[
\lambda=1,
\qquad
\kappa=\frac12,
\]

the rewards are

\[
s_-=-\frac12,
\qquad
s_+=+\frac12.
\]

For

\[
q_0=p^*=q^*=\frac12,
\qquad
\eta=-\frac12,
\]

we obtain

\[
L=\frac18.
\]

If

\[
\phi=0.2,
\]

the oscillation threshold is

\[
\frac{1-\phi}{4}=0.2,
\]

so the return is stable and nonoscillatory.

If instead

\[
\phi=0.8,
\]

the threshold is

\[
0.05,
\]

so exactly the same structural feedback gain produces a stable damped
oscillation.

Thus community memory can change the visible eco-evolutionary transient without
changing either the structural gap contrast or local stability itself.

---

## 8. k-branch extremal family becomes a dynamical phase sequence

The repository's unit-cost `k`-branch family has

\[
C_A=2,
\qquad
C_F=k+1,
\]

hence structural gap

\[
g_k=k-1.
\]

Against a gap-zero control, at the centered equilibrium

\[
\boxed{
L_k
=-\frac{\eta\lambda(k-1)}{4}.
}
\]

Take

\[
\eta=-\frac12,
\qquad
\lambda=1,
\qquad
\phi=\frac12.
\]

Then

\[
L_k=\frac{k-1}{8}
\]

and the oscillation threshold is

\[
\frac18.
\]

Therefore

```text
k = 2
    L=1/8
    stable nonoscillatory boundary

k = 3,...,8
    1/8 < L < 1
    stable damped oscillation

k >= 9
    L >= 1
    overshoot instability
```

This is an exact dynamical interpretation of the repository's linear extremal
gap family.

Increasing branch structure does not simply produce a stronger adaptive
advantage.  Once the evolving architecture feeds back on the community, the
same increase can drive the closed loop through qualitative dynamical phases.

---

## 9. Binary extremal family crosses phases faster

For the repository's binary routing family,

\[
C_A=d+1,
\qquad
C_F=2^d,
\]

so

\[
\Delta g_d
=2^d-(d+1).
\]

At the centered equilibrium,

\[
\boxed{
L_d
=-\frac{\eta\lambda}{4}
[2^d-(d+1)].
}
\]

Again take

\[
\eta=-\frac12,
\qquad
\lambda=1,
\qquad
\phi=\frac12.
\]

Then

\[
L_2=\frac18,
\]

\[
L_3=\frac12,
\]

\[
L_4=\frac{11}{8}>1.
\]

Thus

```text
depth 2 -> stable nonoscillatory boundary
depth 3 -> stable damped oscillation
depth 4 -> overshoot instability
```

The exponential structural gap family therefore reaches the instability phase
much faster than the linear `k`-branch family.

---

## 10. General family thresholds

At a centered equilibrium with

\[
a=-\eta\lambda>0,
\]

the `k`-branch family has

\[
L_k=\frac{a(k-1)}4.
\]

### Oscillation onset

Damped oscillation begins when

\[
\frac{a(k-1)}4
>
\frac{1-\phi}{4},
\]

i.e.

\[
\boxed{
k-1>\frac{1-\phi}{a}.}
\]

### Stability loss

Overshoot begins when

\[
\frac{a(k-1)}4\ge1,
\]

i.e.

\[
\boxed{
k-1\ge\frac4a.}
\]

So the width of the stable-oscillatory family region is controlled by both
community memory and the product of ecological feedback strength and structural
fitness scaling.

For the binary family the same phase criteria apply after replacing `k-1` by

\[
2^d-(d+1).
\]

---

## 11. Damping time and oscillation period

Inside the damped-oscillatory phase the conjugate eigenvalue modulus is

\[
\rho=\sqrt{\det J}
=\sqrt{\phi+(1-\phi)L}.
\]

The local e-folding damping time is

\[
\boxed{
\tau_{\rm damp}
=-\frac{1}{\log\rho}.
}
\]

As either

\[
L\uparrow1
\]

or

\[
\phi\uparrow1,
\]

we have

\[
\rho\uparrow1,
\]

so damping becomes arbitrarily slow.

The complex eigenvalue phase determines the local oscillation period.  Thus two
stable systems can have identical equilibrium positions while differing greatly
in how many generations of oscillation remain visible after a perturbation.

---

## 12. Biological interpretation

The loop-gain form separates four ingredients.

### Structural contrast

\[
\Delta g
\]

comes from exact continuation/productive-frontier structure.

### Fitness conversion

\[
\lambda
\]

maps saved sensing burden into state-specific log-fitness contrast in the
continuous lift.

### Ecological feedback sensitivity

\[
-\eta
\]

measures how strongly increasing contingent-architecture frequency suppresses
or restores the high-opportunity community state under negative feedback.

### Evolutionary responsiveness

\[
p^*(1-p^*)
\]

is largest at an intermediate phenotype frequency and vanishes near fixation.

Their product is the dynamical gain.

This means a system can have a large static adaptive advantage but weak feedback
if ecological state is insensitive to phenotype frequency.  Conversely, a
moderate structural contrast can generate pronounced cycles when ecological
feedback and community memory are strong.

---

## 13. What this does and does not establish

The exact result in this branch is local and deterministic.

It establishes that, in the stated two-community-state feedback model,
repository-derived structural gap contrasts map directly to the local feedback
gain and therefore to exact monotone / damped / overshoot phase boundaries.

It does **not** yet establish

- demographic stochasticity;
- mutation, migration, or drift;
- multiple evolving species;
- stochastic sensory observations;
- nonlinear or history-dependent community feedback beyond the affine target;
- global bifurcation structure outside the local interior analysis;
- empirical realization in a natural system.

The next natural-history application should estimate or constrain all four
pieces of `L`: structural gap contrast, fitness scaling, ecological feedback
slope, and equilibrium phenotype responsiveness.
