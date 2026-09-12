# Causal attribution is selected by diffusion assumptions, not the trait series alone

## Status

This note refines the exact evoTS moving-optimum congruence result. The earlier construction is correct, but it changes both the drift coupling and the process-innovation covariance. That is not a technical nuisance: it identifies the precise assumption on which one-way mechanistic interpretation rests.

## 1. Source model

Write the evoTS moving-optimum model as

\[
dZ_t=-A_0Z_t\,dt+S_0dW_t,
\qquad
A_0=\begin{pmatrix}\alpha&-\alpha\\0&0\end{pmatrix},
\qquad
Q_0=S_0S_0^\top=
\begin{pmatrix}v_x&0\\0&v_\theta\end{pmatrix},
\]

with \(v_x>0\). Only the first coordinate \(X\) is observed.

Biologically, the zero below-diagonal element says the optimum drives the trait but the trait does not feed back on the optimum. The zero off-diagonal element of \(Q_0\) says the instantaneous trait innovation and optimum innovation have no common stochastic component.

These are different assumptions.

## 2. Output-preserving hidden-coordinate gauge

Every invertible transformation

\[
T=\begin{pmatrix}1&0\\t&u\end{pmatrix},\qquad u\ne0,
\]

leaves the observed coordinate exactly unchanged. Under \(Z'=TZ\),

\[
A'=TA_0T^{-1}
=
\begin{pmatrix}
\alpha(t+u)/u&-\alpha/u\\
\alpha t(t+u)/u&-\alpha t/u
\end{pmatrix},
\]

and

\[
Q'=TQ_0T^\top
=
\begin{pmatrix}
v_x&t v_x\\
t v_x&t^2v_x+u^2v_\theta
\end{pmatrix}.
\]

Because \(X'=X\) pathwise, every such pair \((A',Q')\) has exactly the same observed trait likelihood as the source model.

For generic \(t\ne0,-u\), both drift cross-couplings are non-zero, so the transformed system contains reciprocal feedback. But then

\[
\boxed{Q'_{12}=t v_x\ne0.}
\]

Thus reciprocal feedback can be hidden inside the same trait law, but in this exact two-state gauge it arrives together with a shared instantaneous innovation.

## 3. No-common-shock theorem

The converse is sharper and does not rely only on the specific similarity parameterization.

Consider any two-state zero-mode linear diffusion with

\[
\operatorname{tr}A=\alpha,
\qquad
\det A=0,
\]

diagonal process covariance

\[
Q=\operatorname{diag}(q_x,q_y),
\]

and observed first coordinate. By Cayley-Hamilton,

\[
e^{-At}=I-k(t)A,
\qquad
k(t)=\frac{1-e^{-\alpha t}}{\alpha}.
\]

For

\[
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},
\]

the first-row covariance-kernel inner product is

\[
K_A(r,s)
=q_x(1-a k_r)(1-a k_s)+q_y b^2k_rk_s.
\]

For evoTS OUBM it is

\[
K_E(r,s)
=v_x(1-\alpha k_r)(1-\alpha k_s)
+v_\theta\alpha^2 k_rk_s.
\]

If the complete observed finite-time covariance laws are equal for all \(r,s\), coefficient matching gives

\[
q_x=v_x,
\qquad
q_xa=v_x\alpha.
\]

Since \(v_x>0\),

\[
\boxed{a=\alpha.}
\]

Trace equality then gives \(d=0\), and determinant zero gives

\[
\boxed{bc=0.}
\]

If the hidden state genuinely drives the trait, \(b\ne0\), then necessarily

\[
\boxed{c=0.}
\]

Therefore:

> **Within the two-state zero-mode class, an evoTS OUBM trait law with non-zero trait process variance cannot have an exactly congruent reciprocal-feedback realization if the observed and hidden state innovations are required to be instantaneously independent.**

This is the assumption gate.

## 4. Interpretation

The trait series alone does not select between

1. one-way moving optimum + independent innovations; and
2. reciprocal latent feedback + shared innovation.

The one-way causal reading becomes unique only after imposing the additional biological restriction

\[
Q_{12}=0.
\]

Because the second coordinate is unobserved in the trait-only application, that restriction is not itself tested by the observed trait series.

The correct statement is therefore not that the moving-optimum likelihood can never support directionality. It is:

\[
\boxed{
\text{causal direction is conditional on a hidden innovation-structure assumption.}
}
\]

## 5. Relation to Reitan-type layered SDEs

Reitan, Schweder & Henderiks (2012) explicitly obtain a layered causal structure by fixing drift sparsity and restricting the diffusion matrix to a blocked structure. Their concrete layered model uses independent Wiener processes across the causal layers. Under those restrictions, they show that the top-layer covariance of a two-layer model differs from the one-layer OU covariance and can therefore be statistically detected.

That is compatible with the theorem above rather than contradicted by it. The detectability result is conditional on the diffusion restriction. Once instantaneous common innovations across the measured and hidden layers are admitted, drift direction can move along an exactly observation-equivalent gauge.

This distinction must be explicit in any paper. Do not claim that the earlier layered-SDE literature ignored identifiability. It discussed pull-label identifiability and deliberately imposed causal/diffusion structure. The new question is whether biological claims are robust to relaxing the unobserved no-common-shock assumption.

## 6. Revised candidate contribution

The strongest candidate contribution is now:

> **In partially observed evolutionary linear-Gaussian models, mechanistic attribution can be carried by untestable sparsity assumptions on latent innovation covariance. We give an exact causal gauge showing how reciprocal feedback and common shocks trade against one-way adaptive tracking while preserving the complete observed trait law, and identify the extra measurements or interventions needed to break that gauge.**

This has a better claim boundary than generic OU non-identifiability, but its impact depends on demonstrating that published biological conclusions are sensitive to this hidden assumption.

## 7. Empirical audit required

For each target paper or software workflow, record separately:

- which state variables are observed;
- which drift edges are allowed or forbidden;
- which process-noise covariances are allowed or fixed to zero;
- which of those restrictions are empirically testable from the available observations;
- whether the headline biological interpretation changes when an observationally equivalent shared-innovation/feedback realization is admitted.

A Nature-family claim is justified only if this audit shows that a widespread mechanistic conclusion is routinely attributed to data when it is actually selected by an unverified latent-noise restriction.
