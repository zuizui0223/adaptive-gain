# Continuous-time OU congruence gate

## Status

Working note for the proposed second paper. This is deliberately separated from the current finite-architecture manuscript.

## Starting point

For a centered two-state linear Gaussian diffusion

\[
dZ_t=-A Z_t\,dt+S\,dW_t,
\qquad
A=\begin{pmatrix}a&b\\c&d\end{pmatrix},
\qquad
S=\begin{pmatrix}p&0\\r&s\end{pmatrix},
\]

only the first coordinate \(x_t\) is observed. Define

\[
\tau=a+d,\qquad \Delta=ad-bc,\qquad
\kappa=(dp-br)^2+b^2s^2.
\]

For a stable stationary system, the exact scalar spectral density of the observed coordinate is

\[
\boxed{
S_x(\omega)=
\frac{p^2\omega^2+\kappa}
{(\Delta-\omega^2)^2+\tau^2\omega^2}.
}
\]

This follows directly from the first row of \((A+i\omega I)^{-1}S\). Consequently the complete stationary Gaussian observation law of \(x_t\) depends on the drift matrix only through \((\tau,\Delta)\), and on the diffusion through \((p,\kappa)\), in addition to the observed stationary mean. This is consistent with Browning et al. (2025/2026), who identify the same combinations for a partially observed two-state OU process.

## Proposition 1 — exact no-feedback congruent realization for real modes

Assume

\[
\tau>0,\qquad \Delta>0,\qquad \tau^2-4\Delta\ge0,
\]

so the two drift eigenvalues

\[
\lambda_{1,2}=\frac{\tau\mp\sqrt{\tau^2-4\Delta}}2
\]

are real and positive. For every admissible observed law \((\tau,\Delta,p,\kappa)\), choose any \(b_0\ne0\) and define

\[
A_0=\begin{pmatrix}\lambda_1&b_0\\0&\lambda_2\end{pmatrix}.
\]

Then \(\operatorname{tr}A_0=\tau\), \(\det A_0=\Delta\), and the reciprocal feedback product is exactly

\[
\boxed{b_0c_0=0.}
\]

The diffusion can always be chosen to preserve the observed law. One explicit (possibly rank-deficient) choice is

\[
s_0=0,\qquad
r_0=\frac{\lambda_2p-\sqrt{\kappa}}{b_0},
\]

which gives

\[
(\lambda_2p-b_0r_0)^2+b_0^2s_0^2=\kappa.
\]

If \(\kappa>0\), a non-degenerate latent noise can instead be chosen with any
\(0<|s_0|<\sqrt{\kappa}/|b_0|\), followed by a matching \(r_0\).

Therefore every stable stationary scalar OU observation law with real drift modes has an exactly observation-equivalent realization with no reciprocal feedback loop.

## Proposition 2 — complex modes force reciprocal restoring feedback

For any two-state drift matrix,

\[
\tau^2-4\Delta=(a-d)^2+4bc.
\]

Hence if

\[
\boxed{\tau^2-4\Delta<0,}
\]

then necessarily

\[
\boxed{bc<0.}
\]

In particular, no realization with \(bc=0\) can generate the same observed scalar law. Thus a stable complex mode pair identifies the *existence and sign class* of reciprocal feedback, while its magnitude and factorization remain unidentified.

This is the continuous-time analogue of the repository's discrete diagnostic theorem: real monotone modes admit a zero-feedback decomposition; model-compatible oscillatory modes force feedback existence.

## Corollary — a sharp mechanistic-attribution boundary

For a partially observed two-state linear Gaussian evolutionary system observed at stationarity:

- real positive modes: the scalar trait record cannot establish reciprocal eco-evolutionary feedback, because an exact no-feedback realization exists;
- complex stable modes: reciprocal negative loop product is forced, although individual couplings remain non-identifiable.

The statement is distributional, not an asymptotic or finite-sample approximation: congruent parameterizations generate the same finite-dimensional Gaussian distributions for the observed trait and therefore the same exact likelihood for observations at arbitrary time points.

## Novelty discipline

The general structural-identifiability result is not new. Browning et al. already show that a partially observed two-state OU process identifies only the drift trace and determinant together with specific diffusion combinations. The candidate new contribution is biological and inferential:

1. classify the congruence class by reciprocal-feedback existence;
2. prove the real-mode / complex-mode sharp boundary;
3. translate that boundary into claims currently made about adaptive landscapes and eco-evolutionary mechanism;
4. test whether published evolutionary time-series interpretations change across exactly congruent realizations.

If these steps do not overturn or sharply qualify a real empirical inference practice, this line should not be marketed as a Nature-family result.

## Next gate: evoTS / moving-optimum models

The highest-value empirical target is not generic OU usage but models in which an unobserved moving optimum is given a mechanistic interpretation from a trait series alone. The next derivation must establish whether the evoTS moving-optimum OU likelihood belongs to an observation-law congruence class containing both:

- an exogenous moving-optimum realization; and
- an endogenous reciprocal-feedback realization.

This is a stricter and more consequential claim than the stationary proposition above, because common moving-optimum implementations include a Brownian (zero-eigenvalue) latent coordinate and are therefore non-stationary. The stationary proof must not be reused without separately proving the non-stationary observation law and initial-condition conditions.