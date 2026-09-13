# Exact fixed-optimum OU corollary for `paleoTS::logL.joint.OU`

## Status

**IMPLEMENTATION-MATCHED COROLLARY.** This broadens the causal-attribution result beyond a Brownian moving optimum while preserving a critical semantic distinction: the conventional OU half-life remains the observed relaxation time; what is not uniquely identified is its attribution to a one-way direct selection/attraction coefficient.

## 1. The actual paleoTS joint likelihood

The current `paleoTS::logL.joint.OU` implementation uses four parameters

`(anc, vstep, theta, alpha)`

and mean

\[
E[X_t]=\theta+(anc-\theta)e^{-\alpha t}.
\]

Let

\[
V(t)=\frac{v}{2\alpha}(1-e^{-2\alpha t}).
\]

For observation times `s,t`, the process covariance is

\[
C_X(s,t)=e^{-\alpha|t-s|}\min\{V(s),V(t)\}.
\]

Since `V(t)` is monotone for `t>=0`, with `m=min(s,t)` and `h=|t-s|`, this is exactly

\[
\boxed{
C_X(s,t)=\frac{v}{2\alpha}
\left[e^{-\alpha h}-e^{-\alpha(h+2m)}\right].
}
\]

`paleoTS` then adds the observed sampling variance `vv/nn` to the covariance diagonal and evaluates the joint multivariate-normal likelihood.

This is precisely the `v_optimum=0` boundary of the evoTS OUBM covariance already proved in `EVOTS_MOVING_OPTIMUM_CONGRUENCE.md`.

## 2. One-way representation

The conventional fixed-optimum process can be embedded as

\[
\begin{aligned}
dX_t &= \alpha(\Theta_t-X_t)dt + \sqrt v\,dW_t,\\
d\Theta_t &= 0,
\end{aligned}
\]

with `Theta_0=theta`.

In this representation the fitted `alpha` is often described biologically as the strength of attraction, restraining force, stabilizing selection, or rate of adaptation toward a fixed adaptive peak.

## 3. Reciprocal representation with the identical observed trait law

For any

\[
0<q<1,
\qquad a=q\alpha,
\qquad d=(1-q)\alpha,
\]

define

\[
\boxed{
\begin{aligned}
dX_t &= a(Y_t-X_t)dt + \sqrt v\,dW_t,\\
dY_t &= d(X_t-Y_t)dt - \frac da\sqrt v\,dW_t.
\end{aligned}
}
\]

Choose

\[
Y_0=\frac{\alpha\theta-d\,anc}{a}.
\]

The drift matrix again has trace `alpha` and determinant zero. The first-coordinate impulse-response kernel is exactly

\[
(\sqrt v e^{-\alpha t},0),
\]

which is the conventional fixed-optimum OU kernel after embedding the constant optimum as a second zero-noise coordinate. The observed mean is also identical for every `t`.

Therefore every finite set of trait observations, with the same sampling-error variances, has exactly the same multivariate-normal likelihood under the one-way fixed-peak representation and every member of this reciprocal family.

`adaptive_gain/ou_fixed_optimum_congruence.py` regression-checks the literal paleoTS covariance against the closed form and the existing OUBM boundary. Tests independently verify the reciprocal mean and impulse-response equality for multiple `q` values.

## 4. What changes—and what does not

This corollary requires unusually careful interpretation.

### Still identified as a model-conditional observable relaxation scale

The non-zero decay eigenvalue is

\[
\alpha=a+d.
\]

Hence the observed expected trajectory still relaxes with

\[
\boxed{H_{\rm relax}=\log(2)/\alpha.}
\]

So the theorem does **not** show that the fitted trajectory takes a different amount of time to traverse half its expected displacement. Statements using half-life only as a descriptive relaxation timescale remain valid within the OU observation model.

### Not uniquely identified as a one-way mechanistic attraction coefficient

The direct coefficient in

`X <- latent state`

is only

\[
a=q\alpha.
\]

Thus a half-life associated specifically with that direct coupling is

\[
H_{\rm direct}=\frac{\log 2}{a}=\frac{H_{\rm relax}}q,
\]

which ranges from the conventional relaxation half-life toward infinity as `q` approaches zero.

Accordingly, a trait-only fixed-OU fit does not by itself establish that the whole fitted `alpha` is a one-way stabilizing-selection / attraction coefficient rather than the total decay rate of a reciprocal hidden-state system.

## 5. Published practice that makes this non-vacuous

Hunt, Bell & Travis (2008) fit the same joint Gaussian fixed-optimum OU family to fossil stickleback traits. They explicitly interpret `alpha` as the restraining force around an adaptive optimum, translate it into stabilizing-selection parameters, and report half-lives of roughly 580–853 generations as the time to traverse half the distance to the optimum.

Lo Cascio Sætre et al. (2017, *Nature Communications*) explicitly use the `PaleoTS` package on a 19-year reed-warbler body-mass series, interpret `alpha` as the restraining force around the optimum, and report a 1.76-year half-life as exceptionally rapid adaptation.

These studies do more than use `log(2)/alpha` descriptively: they connect the fitted decay parameter to an adaptive-peak mechanism. The corollary therefore targets a real inferential practice.

## 6. Prior-art ceiling

This is **not** the first warning that OU parameters can be difficult or biologically overinterpreted.

Existing work already establishes, among other things:

- parameter/intrinsic-identifiability problems in phylogenetic OU models;
- low power and model-misspecification problems;
- cautions against automatically equating positive `alpha` with stabilizing selection;
- a useful distinction between `alpha` as adaptation/selection and as phenotypic decorrelation;
- reciprocal multivariate OU adaptation and causal/Granger interpretations under declared assumptions.

The candidate contribution is narrower: an exact implementation-matched observational equivalence for the **paleoTS trait-time-series likelihood**, with an explicit decomposition `alpha=a+d` and a sharp statement of which half-life interpretation survives.

## 7. Claim boundary

Allowed:

> In the paleoTS fixed-optimum joint OU likelihood, `alpha` is identified as the observed relaxation rate within the fitted model, but trait observations alone do not uniquely identify the whole rate as a one-way direct attraction/selection coefficient. The same observed law admits reciprocal latent-state realizations with `alpha=a+d`.

Avoid:

- `the OU half-life is wrong`;
- `the time to move halfway to the fitted optimum is unidentified`;
- `fixed-optimum OU models cannot detect adaptation`;
- `Hunt et al. or Sætre et al. are falsified`;
- `positive alpha never reflects selection`.

Independent ecological, genetic, fitness, experimental, or environmental evidence can of course support an adaptive interpretation; the theorem concerns what the trait-time-series likelihood alone identifies.

## 8. Scope consequence for the second paper

The moving-optimum result remains the cleanest example where causal direction of the latent adaptive landscape itself changes across congruent realizations. The fixed-optimum corollary is broader in empirical usage and supplies a second, complementary message:

- **moving optimum:** exogenous landscape motion versus reciprocal latent feedback is not separated by the trait likelihood;
- **fixed optimum:** observed relaxation is identified, but one-way mechanistic attribution of the whole decay rate is not.

This broadens the paper from one specialized OUBM application to a likelihood family spanning both standard paleoTS fixed-OU adaptation analyses and moving-optimum evoTS analyses, without pretending the two causal consequences are identical.
