# Results v1

## Result 1. Finite information structure and community persistence jointly bound long-run evolutionary fluctuation

We first asked whether finite information structure can constrain long-run evolutionary fluctuation even when community states recur over time. Let `g_i` denote the structural gap associated with recurrent community state `i`, and assume

\[
0\le g_i\le g_{\max}.
\]

Under the declared linear lift

\[
s_i=\lambda g_i-\kappa,
\]

the constant maintenance term `kappa` shifts the mean selection but does not change the centered reward geometry. The state-dependent selection range is therefore bounded by `lambda*g_max`.

Let the recurrent community dynamics be a finite ergodic reversible Markov chain with stationary distribution `pi` and largest nontrivial algebraic eigenvalue `r_max<1`. The long-run fluctuation strength of the centered selection process can be written spectrally as

\[
\sigma_{\rm eff}^2
=
\sum_r w_r\frac{1+r_r}{1-r_r},
\]

where `w_r` is the squared projection of the centered structural reward onto community relaxation mode `r`. Because the structural reward is confined to an interval of width `lambda*g_max`, its stationary variance is at most `(lambda*g_max)^2/4`. Since every nontrivial spectral multiplier is at most `(1+r_max)/(1-r_max)`, we obtain

\[
\boxed{
\sigma_{\rm eff}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}}.
}
\]

The bound is sharp. A symmetric two-state community chain with structural rewards at the two endpoints of the allowed interval places all centered reward variance on the single nontrivial community mode and attains equality.

This result separates two sources of long-run evolutionary variability. Finite information structure bounds the amplitude of the state-dependent selection that can be generated, while community persistence determines how strongly that amplitude is retained through time. Slow community modes do not automatically create slow evolutionary modes: they matter only when the structural reward projects onto them.

For nonzero stationary mean-selection magnitude `|mu|`, the same bound yields the asymptotic crossover proxy

\[
\boxed{
H_{\times}^{\rm asy}
\le
\frac{(\lambda g_{\max})^2}{4\mu^2}
\frac{1+r_{\max}}{1-r_{\max}}.
}
\]

This quantity describes the asymptotic scale at which persistent directional mean selection dominates centered fluctuation. It is not a finite-time hitting-time bound.

## Result 2. Required evolutionary dynamics imply minimum or Pareto-minimal information complexity

We next reversed the problem. Suppose a downstream evolutionary regime requires an integer structural gap

\[
q\ge1.
\]

How large must the finite sensing problem be before such a gap is reachable?

### Binary sensing

For binary unit-cost queries, define

\[
h_2^*(q)
=
\min\{h\ge1:2^h-1-h\ge q\}.
\]

The quantity `h_2*(q)` is the smallest adaptive depth at which a productive binary tree can contain enough fixed-mandatory query occurrences to support gap `q`. The exact componentwise first information corner is

\[
\boxed{
(n^*,m^*,E^*)
=
(h_2^*+q+1,\ h_2^*+q,\ h_2^*+q),
}
\]

where `n` is the number of represented worlds, `m` the number of declared query resources, and `E=|H_min|` the number of minimal productive-frontier obligations.

The adaptive depth grows only logarithmically:

\[
h_2^*(q)=\log_2 q+O(1),
\]

whereas the fixed-mandatory information obligations grow essentially linearly:

\[
m^*=E^*=q+\log_2 q+O(1).
\]

Thus increasing the required downstream gain primarily increases the number of mandatory distinctions that a fixed strategy must carry, while the additional adaptive routing depth grows much more slowly.

### Bounded query arity

For maximum query arity `b>=2`, define

\[
h_b^*(q)
=
\min\left\{h\ge1:\frac{b^h-1}{b-1}-h\ge q\right\}.
\]

Higher arity reduces the minimum query/frontier burden,

\[
\boxed{
m_{\min}=E_{\min}=q+h_b^*(q),}
\]

but does not reduce the minimum number of represented ecological alternatives,

\[
\boxed{n_{\min}=q+h_2^*(q)+1.}
\]

These componentwise minima need not be jointly attainable. The exact bounded-arity requirement is therefore generally a Pareto frontier

\[
\mathcal P_b(q)
\]

rather than a single minimum point. Binary sensing is the special case in which the frontier collapses to one exact corner.

For example, when `q=3` and `b=4`, the exact nondominated information structures include

\[
(8,5,5)
\quad\text{and}\quad
(7,6,6).
\]

The first minimizes query/frontier complexity, while the second minimizes the number of represented worlds. Increasing cue arity therefore does not simply make every dimension of the problem easier; it can expose a tradeoff between ecological-state complexity and information-channel complexity.

### Composition with local feedback dynamics

For the generalized local response, let structural feedback satisfy

\[
G=a\Delta g.
\]

The dynamical system determines the smallest integer gap `q_osc` that enters the stable oscillatory regime. The resulting reachability map is

\[
\boxed{
(\alpha,\phi,a,b)
\longrightarrow
q_{\rm osc}
\longrightarrow
\mathcal P_b(q_{\rm osc}).
}
\]

If the integer gap ladder jumps directly from non-oscillatory stability beyond the upper stability boundary, the stable-oscillation Pareto set is empty.

A canonical binary example illustrates the composition. For

\[
\alpha=1,\qquad
\phi=\frac12,\qquad
a=\frac18,
\]

the first stable oscillatory gap is `q_osc=2`, giving

\[
\boxed{(n,m,E)=(6,5,5).}
\]

The registered sharp witness has adaptive cost `C_A=3`, fixed cost `C_F=5`, and five singleton productive-frontier obligations.

## Result 3. Long-term stasis has two dynamically distinct origins

We next compared two mechanisms that both produce little or no net long-term change.

### Neutral cancellation stasis

Consider additive periodic weak selection,

\[
z_{t+1}=z_t+E\beta_t.
\]

If one complete period satisfies

\[
\sum_{t=0}^{P-1}\beta_t=0,
\]

then the full-period map is

\[
\boxed{F_P(z)=z}
\]

with derivative exactly one. Within-cycle evolutionary activity can be arbitrarily large, but the period leaves every perturbation unchanged. The stasis is therefore neutral: selection cancels through time, but there is no restoring force.

### Attractive restoring stasis

By contrast, consider an endogenous eco-evolutionary equilibrium with Jacobian `J`. If

\[
\rho(J)<1,
\]

then small perturbations decay. Real eigenvalues produce monotone restoring dynamics, whereas complex eigenvalues produce damped oscillatory restoration. In both cases the equilibrium is attractive.

Thus the two mechanisms are formally distinct:

\[
\boxed{
\begin{aligned}
\text{cancellation stasis}
&=\text{zero period drift + neutral return},\\
\text{restoring stasis}
&=\text{zero equilibrium drift + attraction}.
\end{aligned}
}
\]

The distinction persists even when both systems exhibit almost no long-term net phenotypic change. In the cancellation case, perturbations survive; in the restoring case, perturbations are erased.

## Result 4. Oscillatory local dynamics force feedback existence within the generalized model

Finally, we asked whether local evolutionary trajectories can establish that eco-evolutionary feedback is present.

The generalized local response has invariants

\[
T=\alpha+\phi,
\qquad
D=\alpha\phi+(1-\phi)G,
\]

where `alpha` denotes intrinsic evolutionary persistence, `phi` community persistence, and `G` feedback gain. For any candidate `phi<1`, the compatible feedback gain is

\[
G(\phi)
=
\frac{\phi^2-T\phi+D}{1-\phi}.
\]

The numerator is the characteristic polynomial evaluated at `phi`.

### Stable monotone modes do not establish feedback

If the two local eigenvalues are real and satisfy

\[
0\le r_1,r_2<1,
\]

choosing

\[
\phi=r_1,
\qquad
\alpha=r_2
\]

gives

\[
\boxed{G=0.}
\]

Thus a stable monotone return can always remain compatible with a zero-feedback decomposition within this model class. Its apparent timescale can be attributed to intrinsic evolutionary persistence and community persistence alone.

### Complex modes exclude zero feedback

If the local eigenvalues are a non-real conjugate pair, the characteristic polynomial has negative discriminant and is strictly positive for every real `phi`. Since `1-phi>0` for every admissible `phi<1`, every compatible decomposition satisfies

\[
\boxed{G(\phi)>0.}
\]

A complex local eigenpair therefore forces feedback existence within the generalized model, although the magnitude of feedback remains unidentified.

This result gives oscillatory restoration a qualitatively different mechanistic status from monotone restoration. Oscillation is not merely a different transient shape: within the declared local model it removes the zero-feedback explanation altogether.

## Summary of the four results

Together, the results establish a reachability hierarchy:

```text
finite sensing structure
    -> structural reward / gap ceiling
    -> selection or feedback ceiling
    -> community temporal filtering
    -> reachable fluctuation, stasis, and oscillatory regimes
```

The hierarchy also works in reverse at the level of dynamical requirements:

```text
required feedback phase
    -> required gain
    -> required integer structural gap
    -> minimum / Pareto-minimal information complexity
```

The component decision-tree, separating-system, and dynamical-systems results are standard or independently re-derived machinery. Their ecological composition is what turns finite information structure into a constraint on evolutionary time and feedback reachability.
