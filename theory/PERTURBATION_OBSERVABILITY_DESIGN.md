# Perturbation and observation design for two-mode eco-evolutionary transients

## Status

This note sits downstream of `SCALAR_TRANSIENT_OBSERVABILITY.md`.
That note identified the scalar visibility gate

\[
R=x_0x_2-x_1^2\ne0.
\]

The present note explains **why** that gate can fail and how experimental design enters.

No novelty is claimed for standard linear-systems observability/controllability algebra. The repository-specific use is to connect the eco-evolutionary timescale inverse to concrete natural-history perturbation and measurement choices.

---

## 1. Local linear system

Let the two-dimensional local state satisfy

\[
y_{t+1}=Jy_t,
\]

and let a scalar observable be

\[
x_t=c^\top y_t.
\]

Suppose the initial perturbation is

\[
y_0=v.
\]

Then

\[
x_t=c^\top J^t v.
\]

The scalar second-order observability gate uses

\[
R=x_0x_2-x_1^2.
\]

---

## 2. Exact factorization

Define the observation matrix

\[
\mathcal O_c=
\begin{pmatrix}
c^\top\\
c^\top J
\end{pmatrix}
\]

and the excitation matrix

\[
\mathcal C_v=
\begin{pmatrix}
v & Jv
\end{pmatrix}.
\]

Their product is the two-step Hankel matrix

\[
\mathcal O_c\mathcal C_v
=
\begin{pmatrix}
x_0 & x_1\\
x_1 & x_2
\end{pmatrix}.
\]

Therefore

\[
\boxed{
R
=\det(\mathcal O_c)\det(\mathcal C_v).
}
\]

This is the key design factorization.

The scalar mode-visibility gate closes if either side vanishes.

### Observation-side blindness

\[
\det(\mathcal O_c)=0
\]

means the measured scalar coordinate does not separate the two local dynamical directions.

### Perturbation-side blindness

\[
\det(\mathcal C_v)=0
\]

means the perturbation excites only one local dynamical direction.

Hence

\[
\boxed{
R\ne0
\iff
\det(\mathcal O_c)\ne0
\text{ and }
\det(\mathcal C_v)\ne0.
}
\]

So observing for longer cannot repair a perturbation that never excited the missing mode, and a stronger perturbation cannot repair an observable that is blind to that mode.

---

## 3. Scale-free design scores

Because rescaling `c` or `v` trivially rescales `R`, define

\[
V_O(c)=\frac{|\det(\mathcal O_c)|}{\|c\|^2},
\]

\[
V_C(v)=\frac{|\det(\mathcal C_v)|}{\|v\|^2}.
\]

Then

\[
\boxed{
V_R(c,v)
=\frac{|R|}{\|c\|^2\|v\|^2}
=V_O(c)V_C(v).
}
\]

This gives a scale-free design criterion.

It separates

- how informative the measured scalar variable is;
- how broadly the perturbation excites local modes.

---

## 4. Symmetric local system: exact optimal mixture

Suppose `J` is symmetric with orthonormal eigenvectors and eigenvalues

\[
r_1,r_2.
\]

Write a unit observation or perturbation vector in that eigenbasis as

\[
u=(u_1,u_2).
\]

Then one-side normalized visibility is

\[
\boxed{
V(u)
=|r_1-r_2|\,|u_1u_2|.
}
\]

For a non-unit vector the denominator gives

\[
V(u)
=|r_1-r_2|
\frac{|u_1u_2|}{u_1^2+u_2^2}.
\]

The maximum occurs at equal absolute modal weights,

\[
|u_1|=|u_2|,
\]

with

\[
\boxed{
V_{side}^{max}=\frac{|r_1-r_2|}{2}.
}
\]

If both perturbation and observation are designable,

\[
\boxed{
V_R^{max}=\frac{(r_1-r_2)^2}{4}.
}
\]

Thus in the orthogonal-mode case, the best local experiment is not to align with one ecological/evolutionary mode. It is to deliberately mix both modes equally in the perturbation and in the measured response.

---

## 5. Finite natural-history candidate sets: exact separability

Suppose natural history restricts the design to a finite set of admissible scalar observations

\[
\mathcal C=\{c_1,\ldots,c_k\}
\]

and admissible perturbations

\[
\mathcal V=\{v_1,\ldots,v_\ell\}.
\]

Assume every observation can be paired with every perturbation, so the feasible design set is the Cartesian product

\[
\mathcal C\times\mathcal V.
\]

Because

\[
V_R(c,v)=V_O(c)V_C(v),
\]

we obtain the exact design separation

\[
\boxed{
\max_{c\in\mathcal C,\,v\in\mathcal V}V_R(c,v)
=
\left(\max_{c\in\mathcal C}V_O(c)\right)
\left(\max_{v\in\mathcal V}V_C(v)\right).
}
\]

Therefore the best admissible observation and the best admissible perturbation can be chosen independently:

\[
\boxed{
(c^*,v^*)
\in
\arg\max_c V_O(c)
\times
\arg\max_v V_C(v).
}
\]

This matters for field design because one does not need to evaluate every intervention-measurement pair when feasibility is independent.

The result stops applying when feasibility is joint, for example if a particular perturbation destroys or prevents a particular measurement. In that case pairwise constraints must be retained and the Cartesian-product reduction is invalid.

---

## 6. Natural-history interpretation

The factorization gives natural history two distinct experimental roles.

### Which perturbation excites both clocks?

Examples could include

- changing a resource state strongly enough to affect both phenotype frequency and community occupancy;
- altering interaction opportunity rather than only phenotype frequency;
- perturbing both focal-organism state and biotic context;
- using reciprocal/transplant or resource-addition/removal manipulations that move the system off a single invariant direction.

The question is

\[
\boxed{
\det[v,Jv]\ne0?
}
\]

### Which observable sees both clocks?

A single phenotype score may be nearly blind to one mode, while another observable or combination of observables may project onto both.

Examples could include measuring

- phenotype frequency plus a derived scalar strongly coupled to community occupancy;
- visitation/interaction rate rather than morphology alone;
- a behavioral state that responds to both selection and ecological feedback.

The scalar question is

\[
\boxed{
\det[c^\top;c^\top J]\ne0?
}
\]

The correct natural-history experiment therefore asks not only **what changes after perturbation**, but whether the chosen perturbation and observable expose the coupled evolutionary and ecological modes needed for identification.

---

## 7. Relation to the identifiability hierarchy

The inverse ladder is now

```text
choose perturbation v
    |
    v
perturbation-side visibility det[v,Jv]
    |
choose observation c
    |
    v
observation-side visibility det[c^T;c^T J]
    |
    v
R != 0
    |
    v
recover T,D
    |
    v
independent alpha or phi
    |
    v
recover generalized gain G
    |
    v
factor ecological/selection response
    |
    v
compare with finite sensing gap Delta_g
```

This makes experimental design logically prior to biological parameter identification.

---

## 8. Claim boundary

This note does **not** yet provide

- optimal design under observation noise;
- optimal design under process noise;
- multivariate sensor selection;
- constrained perturbation optimization under field costs;
- nonlinear global perturbation design;
- empirical evidence that a particular real system is two-dimensional near equilibrium.

The result is an exact local deterministic design decomposition for the two-dimensional linearization already used by the feedback theory.
