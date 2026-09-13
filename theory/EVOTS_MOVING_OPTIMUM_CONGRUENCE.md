# Exact congruence of the evoTS moving-optimum OU model with reciprocal feedback

## Status

The hard non-stationary gate is **passed algebraically** for the actual covariance and mean used by `evoTS::logL.joint.OU.BM` at commit `84c201258e35776b7e1ad87fd5563f0c68fceed1`.

This note does not claim that state-space realization non-uniqueness is new mathematics. Its purpose is to identify exactly what the published trait-only likelihood can and cannot support mechanistically.

## 1. The likelihood actually used by evoTS

`logL.joint.OU.BM` fits an OU trait whose unobserved optimum follows an unbiased random walk. In continuous-time notation the process is

\[
\begin{aligned}
dX_t &= \alpha(\Theta_t-X_t)\,dt+\sqrt{v_s}\,dW_{1t},\\
d\Theta_t &= \sqrt{v_o}\,dW_{2t},
\end{aligned}
\]

with independent Brownian motions, deterministic initial values
\(X_0=x_0\) and \(\Theta_0=\theta_0\), and \(\alpha>0\).

The expected observed trait is

\[
\boxed{
E[X_t]=\theta_0+(x_0-\theta_0)e^{-\alpha t}.
}
\]

For \(m=\min(s,t)\) and \(h=|t-s|\), the latent-process covariance is

\[
\begin{aligned}
C_X(s,t)
={}&\frac{v_s}{2\alpha}
\left[e^{-\alpha h}-e^{-\alpha(h+2m)}\right]\\
&+v_o\left[
 m-\frac{(1+e^{-\alpha h})(1-e^{-\alpha m})}{\alpha}
 +\frac{e^{-\alpha h}-e^{-\alpha(h+2m)}}{2\alpha}
\right].
\end{aligned}
\]

This is algebraically identical to the covariance matrix constructed in `logL.joint.OU.BM`. evoTS then adds the known sampling variance `vv/nn` to each diagonal entry and evaluates a multivariate-normal likelihood.

## 2. A continuum of reciprocal-feedback realizations

Choose any

\[
0<q<1,
\qquad
a=q\alpha,
\qquad
d=(1-q)\alpha.
\]

Define a second two-state system

\[
\boxed{
\begin{aligned}
dX_t &= a(Y_t-X_t)\,dt+\sqrt{v_s}\,dW_{1t},\\
dY_t &= d(X_t-Y_t)\,dt
-\frac{d}{a}\sqrt{v_s}\,dW_{1t}
+\frac{\alpha}{a}\sqrt{v_o}\,dW_{2t}.
\end{aligned}
}
\]

Its drift matrix in `dZ=-AZdt+SdW` form is

\[
A_q=
\begin{pmatrix}
a&-a\\
-d&d
\end{pmatrix}.
\]

Both cross-couplings are non-zero for every interior \(q\), and

\[
\operatorname{tr}A_q=a+d=\alpha,
\qquad
\det A_q=0,
\qquad
(A_q)_{12}(A_q)_{21}=ad>0.
\]

Thus the exogenous moving-optimum model (`dTheta` independent of `X`) and a continuum of two-way coupled models occupy the same candidate observation class.

## 3. Match the deterministic mean exactly

Because

\[
A_q^2=\alpha A_q,
\]

we have

\[
e^{-A_qt}
=I-\frac{1-e^{-\alpha t}}{\alpha}A_q.
\]

Set

\[
X_0=x_0,
\qquad
\boxed{
Y_0=\frac{\alpha\theta_0-dx_0}{a}.
}
\]

Then the first coordinate satisfies

\[
E[X_t]
=\theta_0+(x_0-\theta_0)e^{-\alpha t},
\]

exactly matching evoTS for all \(t\ge0\).

## 4. Match the entire stochastic convolution kernel

The reciprocal model has diffusion matrix

\[
S_q=
\begin{pmatrix}
\sqrt{v_s}&0\\
-\frac{d}{a}\sqrt{v_s}&\frac{\alpha}{a}\sqrt{v_o}
\end{pmatrix}.
\]

The first row of \(e^{-A_qt}S_q\) simplifies exactly to

\[
\boxed{
\left(
\sqrt{v_s}e^{-\alpha t},
\sqrt{v_o}(1-e^{-\alpha t})
\right).
}
\]

But this is also the observed convolution kernel of the evoTS exogenous moving-optimum system. Therefore, using the same two Brownian drivers, the observed stochastic part of \(X_t\) is pathwise identical under the two realizations.

Consequently the mean and covariance agree for every collection of observation times, not merely asymptotically or approximately.

## 5. Exact likelihood consequence

Let

\[
\mathbf X=(X_{t_1},\ldots,X_{t_n})^\top.
\]

Both systems generate the same multivariate Gaussian law

\[
\mathbf X\sim N(\mu,\Sigma)
\]

for arbitrary irregular times \(t_1,\ldots,t_n\). Adding the same fossil sampling-error variances to `diag(Sigma)` preserves equality. Hence

\[
\boxed{
\ell_{\rm evoTS}
(\text{trait data}\mid\text{exogenous moving optimum})
=
\ell
(\text{same data}\mid\text{reciprocal coupled state})
}
\]

**exactly for every possible observed trait data vector**, provided the reciprocal realization is parameterized as above.

This is stronger than a flat profile likelihood on one empirical data set. It is an equality of the complete observation law.

## 6. What is and is not identified

The evoTS apparent adaptation rate \(\alpha\) need not be a uniquely attributable one-way trait-to-optimum relaxation rate. Within the reciprocal family,

\[
\boxed{
\alpha=a+d,
}
\]

where

- \(a\) is direct trait response toward the latent state;
- \(d\) is reciprocal response of the latent state toward the trait.

Every partition \(a=q\alpha\), \(d=(1-q)\alpha\) with \(0<q<1\) gives the same trait likelihood after the corresponding hidden initial state and process-noise covariance are transformed.

Thus a trait-only fit can identify the observed relaxation scale \(\alpha\) in the fitted statistical model while failing to identify the mechanistic attribution of that scale.

## 7. A concrete symmetric witness

Taking \(q=1/2\),

\[
A=
\frac{\alpha}{2}
\begin{pmatrix}
1&-1\\
-1&1
\end{pmatrix},
\]

so deterministically

\[
\dot X=\frac{\alpha}{2}(Y-X),
\qquad
\dot Y=\frac{\alpha}{2}(X-Y).
\]

The two states reciprocally track one another and collapse their difference, while noise drives the neutral common mode. The observed trait process is nevertheless exactly the same as under the model in which an exogenous optimum executes a Brownian random walk and the trait alone follows it.

## 8. Why this is not just the stationary Browning result

Browning et al. analyse the stable stationary two-state OU case and identify drift trace/determinant plus diffusion combinations under partial observation. The evoTS OUBM model sits on the zero-eigenvalue boundary because its latent optimum is Brownian. The construction above therefore required a separate non-stationary derivation with the exact initial-state convention and the exact evoTS covariance.

The resulting equality is also transparent as a state-space realization transformation: the hidden coordinate is not empirically anchored by the observed trait series. That observation is standard in control/state-space theory and must be acknowledged rather than presented as new mathematics.

## 9. Candidate biological claim

The defensible candidate claim is narrower than `OU models are invalid`:

> A trait-only moving-optimum OU likelihood can support the existence of a slow stochastic component in the observed trait trajectory, but it does not by itself identify that component as an exogenously moving adaptive optimum. Exactly the same trait law can arise from a reciprocally coupled latent state.

Whether this is a high-impact result now depends on empirical practice, not additional algebra: how often published papers convert support for OUBM into claims about the dynamics or causal origin of the adaptive landscape without an independently observed latent driver.

## 10. Remaining hard gates

1. **Prior-art gate:** search state-space, evolutionary, quantitative-genetic, and hidden-environment literature for this exact exogenous-vs-reciprocal realization ambiguity.
2. **Semantic gate:** decide which mechanistic statements in published papers genuinely distinguish exogenous peak movement from endogenous feedback, rather than merely describing an unobserved stochastic optimum phenomenologically.
3. **Empirical audit:** reproduce at least one published evoTS OUBM fit and attach a reciprocal member of the exact congruence class with identical log-likelihood.
4. **Scope gate:** quantify how widespread the affected inference is. A single example supports a methods/concept paper; a field-level audit is required before Nature-family framing.
5. **Replacement gate:** state what extra observation or intervention breaks the equivalence (e.g. an independently measured environmental/fitness optimum, a perturbation that fixes one coordinate, or direct cross-lag response measurements).
