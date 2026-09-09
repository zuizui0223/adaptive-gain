# Paper theorem spine: information structure and evolutionary timescale

## Paper-level question

Do not frame the paper as asking whether rapid short-term evolution can coexist with long-term stasis.  That phenomenon is prior art.

The narrower question is:

> **When individual information use generates state-dependent selection, how does finite information structure constrain both the amplitude and the temporal fate of evolutionary change?**

The paper should treat the finite sensing theory as an upstream generator of selection structure, not as a detachable combinatorial appendix.

---

# Main-text theorem sequence

## Theorem 1 — Structural-temporal joint ceiling

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

### Why it belongs in the main text

This is the cleanest quantitative realization of the paper's central premise.  Static information structure bounds the instantaneous reward range; community persistence amplifies that range through time.  Neither appears as an independent phenomenological parameter once the structural layer is declared.

### Corollary

For nonzero stationary mean-selection magnitude `|mu|`, the asymptotic mean-versus-fluctuation crossover proxy obeys

\[
H_{\times}^{\rm asy}
\le
\frac{(\lambda g_{\max})^2}{4\mu^2}
\frac{1+r_{\max}}{1-r_{\max}}.
\]

Keep this as a corollary, not a headline theorem, because it is not a finite-time hitting-time statement.

---

## Theorem 2 — Dynamical requirements imply minimum information complexity

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

not one componentwise minimum.  Binary sensing is the special case in which the frontier collapses to one exact corner.

### Dynamic composition

For generalized structural feedback

\[
G=a\Delta g,
\]

the local response supplies the first oscillatory integer gap `q_osc`.  Therefore the main reachability map is

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

### Why it belongs in the main text

This is the strongest direct use of the repository's static extremal mathematics.  A requested dynamical behavior imposes a lower bound on individual-information complexity.  Productive frontier survives as a real downstream coordinate rather than an internal representation artifact.

---

## Theorem 3 — Two mechanisms of stasis are dynamically distinct

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

Thus arbitrarily large within-cycle evolutionary activity can coexist with zero retained period drift, but perturbations are **not** restored.  This is neutral cancellation.

### Restoring stasis

For the endogenous eco-evolutionary system, an interior equilibrium with

\[
\rho(J)<1
\]

is locally attractive.  Small perturbations decay.  Real eigenvalues give monotone restoring dynamics; complex eigenvalues give oscillatory restoring dynamics.

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

### Why it belongs in the main text

Both mechanisms can produce little long-term net change, but their causal structures are different.  Treating them as one category would erase the feedback mechanism that the paper is trying to expose.

---

## Theorem 4 — Oscillation forces feedback existence within the generalized model

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

### Complex modes

If the local eigenvalues are a non-real conjugate pair, the characteristic polynomial is strictly positive for every real `phi`.  Hence every admissible `phi<1` gives

\[
\boxed{G(\phi)>0.}
\]

Thus oscillatory local dynamics force feedback existence, although the feedback magnitude remains unidentified.

### Why it belongs in the main text

This is the qualitative bridge between dynamical phase and mechanism.  It is also the reason the structural reachability theorem for the complex-eigenvalue regime has biological meaning beyond classifying mathematical phases.

---

# Supporting propositions / main-text lemmas

## Proposition A — Reward-mode alignment

For finite reversible community dynamics,

\[
\sigma_{\rm eff}^2
=
\sum_r w_r\frac{1+\lambda_r}{1-\lambda_r}.
\]

Slow community modes matter evolutionarily only to the extent that the structurally generated reward vector projects onto them.

Use this as the mechanistic explanation beneath Theorem 1 rather than as a separate headline theorem.

## Proposition B — Time-interpretation nonidentifiability

The pair `(T,D)` does not jointly identify `(alpha,phi,G)`.  Retain this as a limitation on interpreting evolutionary time, not as an observation-design program.

## Proposition C — Productive-frontier edge cap

A cap on `|H_min|` bounds `C_F` and therefore the structural gap.  A rank cap does not: sharp witnesses already have frontier rank one.  This is useful in proving Theorem 2 and should not become its own ecological headline.

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

They support the theorem spine but should not compete with it.

---

# Figures implied by the theorem spine

## Figure 1 — One structural state space, two outputs

```text
community state i
       |
       +--> finite information structure --> g_i --> selection amplitude
       |
       +--> transition operator P ---------> temporal recurrence
```

Show that amplitude and time are generated on the same state space.

## Figure 2 — Structural-temporal ceiling

Plot or diagram the two multiplicative ceilings:

```text
finite structural range       community persistence
(lambda*g_max)^2 / 4      x   (1+r_max)/(1-r_max)
                    |
                    v
               sigma_eff^2
```

## Figure 3 — Dynamical gain to information complexity

Show

```text
required G
 -> required integer gap q
 -> binary exact corner / bounded-arity Pareto frontier
```

Include the `q=3,b=4` two-point example to make the Pareto generalization visually obvious.

## Figure 4 — Three long-time phenotypes of short-time evolution

Side-by-side trajectories:

1. directional trend;
2. neutral cancellation stasis;
3. attractive restoring stasis, with monotone and oscillatory subcases.

Mark that only the complex local subcase forces feedback existence within the generalized model.

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
- AR(2) inversion or generic nonidentifiability.

The candidate novelty is their exact composition around one biological statement:

\[
\boxed{
\text{finite individual information structure constrains
which evolutionary amplitudes, timescales, and feedback phases are reachable.}
}
\]
