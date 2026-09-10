# Paper theorem spine: information structure and evolutionary timescale

## Paper-level question

Do not frame the paper as asking whether rapid short-term evolution can coexist with long-term stasis. That phenomenon is prior art.

The narrower question is:

> **When individual information use generates state-dependent selection, how does finite information structure constrain both the amplitude and the temporal fate of evolutionary change?**

The paper should treat the finite sensing theory as an upstream generator of selection structure, not as a detachable combinatorial appendix.

---

# Result hierarchy

The paper does **not** contain four equal headline theorems. The results have different jobs:

1. **Principal reachability theorem** — a required dynamical regime implies a minimum or Pareto-minimal finite information structure. This is the main biological/combinatorial result.
2. **Supporting extremal theorem** — finite structural range and recurrence impose a sharp structural-temporal envelope on long-run fluctuation. This is an extremal ceiling, not a predictor of realized variance.
3. **Diagnostic theorem** — within the generalized local model, a complex eigenpair excludes every zero-feedback decomposition and therefore forces feedback existence, while leaving magnitude unidentified.
4. **Mechanistic proposition** — neutral cancellation stasis and attractive restoring stasis are dynamically distinct. The distinction matters biologically, but the underlying identity-map versus contraction algebra is standard and should not carry an independent novelty claim.

This hierarchy should be visible in the Abstract, Results ordering, Discussion, figures, Supplement, and PR description.

---

# Main-text result sequence

## Principal theorem — Dynamical requirements imply minimum information complexity

### Binary exact form

If a downstream dynamical regime requires integer structural gap `q>=1`, define

\[
h_2^*(q)
=
\min\{h\ge1:2^h-1-h\ge q\}.
\]

Then the componentwise first binary unit-cost information corner is

\[
\boxed{
(n^*,m^*,E^*)
=
(h_2^*+q+1,\ h_2^*+q,\ h_2^*+q),
}
\]

where `E=|H_min|` is the minimal productive-frontier obligation count.

Moreover,

\[
h_2^*(q)=\log_2q+O(1).
\]

Hence fixed-mandatory information obligations grow essentially linearly with the required gap, while adaptive routing depth grows only logarithmically.

### Bounded-arity generalization

For maximum query arity `b>=2`, define

\[
h_b^*(q)
=
\min\left\{h\ge1:\frac{b^h-1}{b-1}-h\ge q\right\}.
\]

Then

\[
\boxed{
m_{\min}=E_{\min}=q+h_b^*(q),}
\]

whereas the minimum world count is arity-independent,

\[
\boxed{n_{\min}=q+h_2^*(q)+1.}
\]

The exact joint requirement is generally a Pareto frontier

\[
\mathcal P_b(q),
\]

not one componentwise minimum. Binary sensing is the special case in which the frontier collapses to one exact corner.

For `q=3,b=4`, the two nondominated information requirements

\[
(8,5,5)
\qquad\text{and}\qquad
(7,6,6)
\]

make the biological tradeoff explicit: increasing cue outcome richness can reduce query/frontier burden without erasing the lower bound on how many ecological alternatives must be represented.

### Dynamic composition

For generalized structural feedback

\[
G=a\Delta g,
\]

the local response supplies the first oscillatory integer gap `q_osc`. Therefore the main reachability map is

\[
\boxed{
(\alpha,\phi,a,b)
\longrightarrow
q_{\rm osc}
\longrightarrow
\mathcal P_b(q_{\rm osc}).
}
\]

If the integer gap ladder jumps directly beyond the upper stability threshold, the stable-oscillation Pareto set is empty.

### Why this is the principal theorem

This is the strongest direct use of the repository's static extremal mathematics. A requested dynamical behavior imposes a lower bound on individual-information complexity. The result runs **backward from dynamics to required natural-history structure**, so the finite sensing theory carries a biological conclusion rather than serving only as a descriptive encoding.

---

## Supporting theorem — Structural-temporal extremal envelope

### Statement

For recurrent community states with structural gaps

\[
0\le g_i\le g_{\max},
\]

continuous lift

\[
s_i=\lambda g_i-\kappa,
\]

and a finite ergodic reversible community chain with largest nontrivial algebraic eigenvalue `r_max<1`,

\[
\boxed{
\sigma_{\rm eff}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}}.
}
\]

Equality is attained by a symmetric two-state chain with endpoint structural rewards.

### Sharpness and tightness discipline

The bound is **sharp in the extremal sense** because an equality witness exists. Do not describe it as a prediction of realized long-run variance in a generic multi-state community.

Let

\[
f(r)=\frac{1+r}{1-r},
\qquad
B=\frac{(\lambda g_{\max})^2}{4}f(r_{\max}),
\]

and, when `Var_pi(s)>0`, define normalized spectral reward weights

\[
\widetilde w_j=\frac{w_j}{\operatorname{Var}_\pi(s)}.
\]

Then the slack has the exact factorization

\[
\boxed{
\frac{\sigma_{\rm eff}^2}{B}
=
\underbrace{
\frac{4\operatorname{Var}_\pi(s)}{(\lambda g_{\max})^2}
}_{\text{range/variance saturation}}
\times
\underbrace{
\frac{\sum_j\widetilde w_j f(r_j)}{f(r_{\max})}
}_{\text{reward--slow-mode alignment}}
\le1.
}
\]

Thus equality requires both maximal endpoint variance and complete loading of that variance onto the slowest algebraic mode. In larger state spaces either factor can be far below one. This is the correct interpretation of the ceiling's looseness.

### Corollary

For nonzero stationary mean-selection magnitude `|mu|`, the asymptotic mean-versus-fluctuation crossover proxy obeys

\[
H_{\times}^{\rm asy}
\le
\frac{(\lambda g_{\max})^2}{4\mu^2}
\frac{1+r_{\max}}{1-r_{\max}}.
\]

Keep this as a corollary, not a headline result, because it is not a finite-time hitting-time statement.

### Role in the paper

This theorem supplies the structural envelope around the principal reachability result. Static information structure bounds the available reward range and community persistence can amplify that range through time, but the realized fluctuation still depends on reward variance and modal alignment.

---

## Diagnostic theorem — Oscillation forces feedback existence within the generalized model

The local generalized response has invariants

\[
T=\alpha+\phi,
\qquad
D=\alpha\phi+(1-\phi)G.
\]

For every candidate `phi<1`,

\[
G(\phi)
=
\frac{\phi^2-T\phi+D}{1-\phi}.
\]

The numerator is the characteristic polynomial evaluated at `phi`.

### Real nonnegative modes

If the two local eigenvalues satisfy

\[
0\le r_1,r_2<1,
\]

then taking `phi=r_1` and `alpha=r_2` gives

\[
\boxed{G=0.}
\]

Thus stable monotone return does not establish feedback existence within this model class.

The parent generalized model itself allows `alpha=1` while requiring `phi<1`. Therefore a neutral boundary case with one eigenvalue exactly one can also admit `G=0` when the other eigenvalue can serve as `phi`; this is model-feasible but is outside the asymptotically stable monotone-return corollary.

### Complex modes

If the local eigenvalues are a non-real conjugate pair, the characteristic polynomial is strictly positive for every real `phi`. Hence every admissible `phi<1` gives

\[
\boxed{G(\phi)>0.}
\]

Thus oscillatory local dynamics force feedback existence, although the feedback magnitude remains unidentified.

### Role in the paper

This is a **diagnostic boundary**, not the principal reachability theorem. It says what a local transient can establish about mechanism inside the declared generalized model: oscillation can rule out `G=0`, but it cannot identify `G`, `alpha`, or `phi` separately.

---

## Mechanistic proposition — Two origins of stasis are dynamically distinct

### Cancellation stasis

For additive periodic weak selection

\[
z_{t+1}=z_t+E\beta_t,
\]

if one period satisfies

\[
\sum_{t=0}^{P-1}\beta_t=0,
\]

then the one-period map is

\[
\boxed{F_P(z)=z}
\]

with multiplier exactly one.

Thus arbitrarily large within-cycle evolutionary activity can coexist with zero retained period drift, but perturbations are **not** restored. This is neutral cancellation.

### Restoring stasis

For the endogenous eco-evolutionary system, an interior equilibrium with

\[
\rho(J)<1
\]

is locally attractive. Small perturbations decay. Real eigenvalues give monotone restoring dynamics; complex eigenvalues give oscillatory restoring dynamics.

### Main distinction

\[
\boxed{
\begin{aligned}
\text{cancellation stasis}
&=\text{zero period drift + neutral return map},\\
\text{restoring stasis}
&=\text{zero equilibrium drift + attractive map}.
\end{aligned}
}
\]

### Claim discipline

Keep this distinction in the main text because it prevents biologically different processes from being collapsed into one category of "stasis." Do **not** present the identity-map versus contraction algebra as an independent mathematical novelty claim.

---

# Supporting propositions / main-text lemmas

## Proposition A — Reward-mode alignment

For finite reversible community dynamics,

\[
\sigma_{\rm eff}^2
=\sum_r w_r\frac{1+\lambda_r}{1-\lambda_r}.
\]

Slow community modes matter evolutionarily only to the extent that the structurally generated reward vector projects onto them. This supplies the second factor in the structural-envelope slack decomposition.

## Proposition B — Time-interpretation nonidentifiability

The pair `(T,D)` does not jointly identify `(alpha,phi,G)`. Retain this as a limitation on interpreting evolutionary time, not as an observation-design program.

## Proposition C — Productive-frontier edge cap

A cap on `|H_min|` bounds `C_F` and therefore the structural gap. A rank cap does not: sharp witnesses already have frontier rank one. This is useful in proving the principal reachability theorem and should not become its own ecological headline.

---

# Supplementary / proof-support layer

Keep the following out of the main narrative unless needed in proof sketches:

- continuation bisimulation construction;
- residual fixed-side kernels and proof DAGs;
- LP/fractional/integer certificate ladders;
- exhaustive 4-world / 5-world enumeration receipts;
- exact bounded-arity recurrence implementation details;
- private-pair forest colouring proof details;
- critical-slowing asymptotics at both local stability boundaries;
- exact transient-period ceilings;
- AR(2) inversion algebra;
- solver-cap implementation details.

They support the result hierarchy but should not compete with it.

---

# Figures implied by the result hierarchy

## Figure 1 — One structural state space, two outputs

```text
community state i
       |
       +--> finite information structure --> g_i --> selection amplitude
       |
       +--> transition operator P ---------> temporal recurrence
```

Show that amplitude and time are generated on the same state space.

## Figure 2 — Principal reachability map

Show

```text
required G
 -> required integer gap q
 -> binary exact corner / bounded-arity Pareto frontier
```

Use `q=3,b=4` and the two nondominated points `(8,5,5)` and `(7,6,6)` as the main visual example.

## Figure 3 — Structural-temporal envelope and its slack

Show the extremal ceiling together with the two multiplicative slack factors:

```text
range/variance saturation  x  reward--slow-mode alignment
                         |
                         v
             realized sigma_eff^2 / extremal bound
```

Include the symmetric two-state equality witness, but visually distinguish "sharp" from "typically tight."

## Figure 4 — Mechanistic long-time outcomes and diagnostic status

Side-by-side trajectories:

1. directional trend;
2. neutral cancellation stasis;
3. attractive monotone restoration;
4. attractive oscillatory restoration.

Mark that the stasis comparison is a mechanistic proposition and that only the complex local subcase forces feedback existence within the generalized model.

---

# Claims not to headline

Do not claim novelty for:

- rapid short-term evolution coexisting with long-term stasis;
- temporal autocorrelation affecting evolution;
- generic eco-evolutionary feedback;
- oscillations from two-dimensional feedback systems;
- Popoviciu variance bounds;
- reversible Markov spectral formulas;
- Jury stability criteria;
- full binary / b-ary tree counting;
- hitting-set duality;
- generic Pareto optimization;
- identity maps versus contractions;
- AR(2) inversion or generic nonidentifiability.

The candidate novelty is their exact composition around one biological statement:

\[
\boxed{
\text{finite individual information structure constrains
which evolutionary amplitudes, timescales, and feedback phases are reachable.}
}
\]

The strongest form of that statement is the reverse reachability map from a required dynamical regime to a required finite information structure. The structural-temporal ceiling and oscillation diagnostic support that claim; the stasis proposition prevents mechanistic overinterpretation.
