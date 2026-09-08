# Structural loop gain and the eco-evolutionary phase diagram

## Status and claim boundary

This note closes the local deterministic phase diagram for the minimal endogenous
community-feedback model in `ENDOGENOUS_COMMUNITY_FEEDBACK.md`.

The discrete-time Jacobian, Jury stability conditions, damped-oscillation
boundary, unit-circle crossing, and feedback-gain algebra are standard
dynamical-systems results. The repository does **not** claim those tools as new.

The repository-specific result is the upstream identification

\[
\boxed{
\text{exact adaptive/fixed structural gap contrast}
\longrightarrow
\text{closed-loop eco-evolutionary gain}.
}
\]

Because the gap contrast is constrained by the repository's finite sensing
theorems, those combinatorial results now imply dynamical phase crossings and
phase exclusions in the feedback model.

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

Community occupancy relaxes toward

\[
q_{\rm target}(p)
=q_0+\eta\left(p-\frac12\right)
\]

with memory

\[
0\le\phi<1:
\]

\[
q_{t+1}
=\phi q_t
+(1-\phi)q_{\rm target}(p_t).
\]

State-specific log-fitness rewards are

\[
s_-<s_+,
\qquad
\Delta s=s_+-s_->0.
\]

Evolution follows the exact haploid log-odds update

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

Since

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

For restoring negative feedback

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

The local feedback problem is therefore compressed to

```text
L    closed-loop structural feedback gain
phi  community memory
```

`L` combines

- ecological feedback sensitivity `eta`;
- state-specific selection contrast `Delta s`;
- evolutionary responsiveness `p*(1-p*)`.

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

the middle inequality is automatic whenever `L>0`. Hence

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

Thus positive feedback is non-restoring, moderate negative feedback stabilizes
the interior state, and sufficiently strong negative feedback destabilizes it
again in discrete time.

---

## 5. Nonoscillatory versus damped return

The characteristic discriminant is

\[
\Delta_J
=(1+\phi)^2
-4[\phi+(1-\phi)L]
\]

and factorizes exactly as

\[
\boxed{
\Delta_J
=(1-\phi)[(1-\phi)-4L].
}
\]

Within the stable interval

\[
0<L<1,
\]

the eigenvalues are complex exactly when

\[
\boxed{
L>\frac{1-\phi}{4}.
}
\]

Hence

```text
L <= 0
    unstable non-restoring / positive feedback

0 < L <= (1-phi)/4
    stable nonoscillatory return

(1-phi)/4 < L < 1
    stable damped eco-evolutionary oscillation

L >= 1
    strong-negative-feedback oscillatory instability
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

approaches zero. Even weak restoring feedback can therefore generate long
damped cycles when community states have strong memory.

---

## 6. The `L=1` boundary is an oscillatory unit-circle crossing

At

\[
L=1,
\]

we have

\[
\det J=1
\]

and

\[
\operatorname{tr}J=1+\phi.
\]

For every

\[
0\le\phi<1,
\]

the two eigenvalues form a nonreal conjugate pair on the unit circle:

\[
\lambda_{\pm}=e^{\pm i\theta_c}.
\]

Their angle satisfies

\[
\boxed{
\cos\theta_c
=\frac{1+\phi}{2}.
}
\]

Thus the critical local oscillation period is

\[
\boxed{
T_c
=\frac{2\pi}{\theta_c}
=\frac{2\pi}{\arccos[(1+\phi)/2]}.
}
\]

For example,

```text
phi = 0      -> T_c = 6 generations
phi = 0.2    -> T_c ~= 6.78
phi = 0.5    -> T_c ~= 8.69
phi = 0.8    -> T_c ~= 13.93
phi = 0.95   -> T_c ~= 28.04
```

and

\[
T_c\to\infty
\quad\text{as}\quad
\phi\uparrow1.
\]

So the strong-feedback boundary is not a flip through eigenvalue `-1`; it is an
oscillatory unit-circle crossing. The repository does not claim the generic
bifurcation algebra as novel, but the boundary becomes biologically relevant
once `L` is tied to structural adaptive gain.

---

## 7. Structural gap enters the loop literally

Under the continuous structural lift,

\[
s_i
=\lambda g_i-\kappa,
\qquad
g_i=C_F(i)-C_A(i).
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

## 8. Repo-native minimal witness

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

the oscillation threshold is `0.2`, so return is stable and nonoscillatory.

If

\[
\phi=0.8,
\]

the threshold is `0.05`, so the same structural feedback gain produces a stable
damped oscillation.

Community memory can therefore alter the visible eco-evolutionary transient
without changing either structural gap contrast or local stability.

---

## 9. `k`-branch extremal family becomes a dynamical phase sequence

The repository's unit-cost `k`-branch family has

\[
C_A=2,
\qquad
C_F=k+1,
\]

so

\[
g_k=k-1.
\]

Against a gap-zero control at the centered equilibrium,

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

and the oscillation threshold is `1/8`.

Therefore

```text
k = 2
    L=1/8
    stable nonoscillatory boundary

k = 3,...,8
    1/8 < L < 1
    stable damped oscillation

k = 9
    L=1
    oscillatory unit-circle boundary

k > 9
    L>1
    oscillatory instability
```

Increasing branch structure does not simply produce a stronger static adaptive
advantage. Once the evolving architecture feeds back on community state, the
same increase drives the closed loop through qualitative dynamical phases.

---

## 10. Binary extremal family crosses phases faster

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

With the same parameters,

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
depth 4 -> oscillatory instability
```

The exponential structural-gap family reaches the instability phase much faster
than the linear `k`-branch family.

---

## 11. General family thresholds

At a centered equilibrium define

\[
a=-\eta\lambda>0.
\]

For the `k`-branch family,

\[
L_k=\frac{a(k-1)}{4}.
\]

Damped oscillation begins when

\[
\boxed{
k-1>\frac{1-\phi}{a}.}
\]

The unit-circle instability boundary is reached when

\[
\boxed{
k-1\ge\frac{4}{a}.}
\]

For the binary family the same criteria apply after replacing `k-1` by

\[
2^d-(d+1).
\]

---

## 12. Damping time and oscillation period

Inside the damped-oscillatory phase the conjugate eigenvalue modulus is

\[
\rho
=\sqrt{\det J}
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

The complex eigenvalue phase determines the local oscillation period. Two stable
systems can therefore have identical equilibrium positions while differing
greatly in how many generations of oscillation remain visible after a
perturbation.

---

## 13. Biological interpretation

The loop gain separates four ingredients.

### Structural contrast

\[
\Delta g
\]

comes from exact continuation/productive-frontier structure.

### Fitness conversion

\[
\lambda
\]

maps saved sensing burden into state-specific log-fitness contrast.

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

is largest at intermediate phenotype frequency and vanishes near fixation.

Their product is the dynamical gain.

A system can therefore have a large static adaptive advantage but weak feedback
if ecological state is insensitive to phenotype frequency. Conversely, a
moderate structural contrast can generate pronounced cycles when ecological
feedback and community memory are strong.

---

## 14. Relation to structural phase-exclusion bounds

`STRUCTURAL_PHASE_EXCLUSION_BOUNDS.md` adds the complementary one-sided result.
The parent bounded-arity theorem gives an upper bound on the largest possible
`C_F-C_A` gap in a finite sensing scope, and therefore an upper bound on `L`.

This can certify that a damped or unstable phase is impossible for **every** task
in that scope under the declared feedback parameters.

So the two notes play different roles:

```text
STRUCTURAL_LOOP_GAIN_PHASE_DIAGRAM
    given L, which dynamical phase follows?

STRUCTURAL_PHASE_EXCLUSION_BOUNDS
    can the finite sensing structure generate enough L to reach that phase at all?
```

---

## 15. Scope boundary

The exact result here is local and deterministic.

It establishes that, in the stated two-community-state feedback model,
repository-derived structural gap contrasts map directly to loop gain and hence
to exact nonoscillatory / damped / unit-circle phase boundaries.

It does **not** yet establish

- demographic stochasticity;
- mutation, migration, or drift;
- multiple evolving species;
- stochastic sensory observations;
- nonlinear or history-dependent community feedback beyond the affine target;
- global bifurcation structure outside the local interior analysis;
- empirical realization in a natural system.

A natural-history application must estimate or constrain the four components of
`L`: structural gap contrast, fitness scaling, ecological feedback slope, and
equilibrium phenotype responsiveness.
