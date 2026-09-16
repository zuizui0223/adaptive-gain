# Paper theorem spine V3: finite sensing architecture and eco-evolutionary possibility

Status: canonical theorem hierarchy for `manuscript/MANUSCRIPT_EVOLUTION_LETTERS_V3.md`. The frozen V2 spine and submission package remain available as fallback; this file does not rewrite their provenance.

## Paper-level question

> **How does a declared finite sensing architecture constrain which ecological decisions are feasible under hard budgets, which state-dependent selection contrasts can be generated, and which local eco-evolutionary regimes can therefore be reached?**

The paper treats finite decision structure as an upstream generator of ecological performance and selection structure. `Information` is used here in the biological/decision-architectural sense; no generic Shannon or mutual-information minimum is claimed.

## One headline, not many

The V3 mathematical assets serve one headline:

\[
\boxed{
\text{finite sensing architecture defines a constrained eco-evolutionary possibility space.}
}
\]

The result hierarchy is causal rather than a ranking of mathematical elegance:

1. **Foundation:** exact adaptive/fixed resolution geometry.
2. **Exposure:** a hard ecological budget can expose the adaptive-only interval.
3. **Extremal structure:** sharp/Pareto finite bounds determine how large a structural advantage is possible.
4. **Reachability:** state-dependent structural contrast bounds local eco-evolutionary feedback.
5. **Temporal expression:** ecological recurrence filters generated selection through time.
6. **Diagnostic boundary:** compatible oscillation can diagnose feedback existence but not magnitude or sensing causality.

Target-relevant kernels support Step 1 by defining the exact decision-relevant state/query representation. Balanced-query counterexamples support Step 3 by showing which intuitive summaries do not control adaptive value.

---

## Theorem A — Exact adaptive/fixed containment

For any resolvable finite deterministic target-resolution task with positive additive query costs,

\[
\boxed{C_A\le C_F.}
\]

This is a class-containment theorem. A fixed resolving bundle is a feasible adaptive policy that ignores intermediate observations.

### Corollary A1 — Exact adaptive-only ecological budget window

For a hard budget `B` on the same acquisition-cost scale,

\[
\boxed{
\text{adaptive-only guaranteed resolution}
\iff
C_A\le B<C_F.
}
\]

Thus the budget axis has three exact regions: both fail, adaptive only, both succeed.

### Evolutionary lift A2 — Threshold selection

With

\[
S_A=1\{C_A\le B\},\qquad
S_F=1\{C_F\le B\},
\]

\[
W_A=e^{-\kappa}(w_0+vS_A),\qquad
W_F=w_0+vS_F,
\]

selection

\[
s_B=\log(W_A/W_F)
\]

is positive relative to maintenance cost only in the adaptive-only interval when

\[
\kappa<\log\frac{w_0+v}{w_0}.
\]

The biological budget may be time, energy, exposure, handling opportunity or another justified hard ceiling; the theorem does not choose it for a focal system.

---

## Theorem B — Exact target-relevant reduction

At a Bellman state, same-target world twins can be quotient-collapsed and a query `r` can be removed when another query `q` satisfies

\[
S_A(q)\supseteq S_A(r),
\qquad
c(q)\le c(r).
\]

Recursive composition preserves the exact adaptive optimum:

\[
\boxed{C_A^{\rm kernel}=C_A^{\rm direct}.}
\]

### Role in the Letter

This theorem is not a second ecological headline. It licenses a precise statement about natural-history representation: descriptive differences that preserve target-relevant continuation geometry need not be counted as distinct decision complexity for the declared objective.

### Scope

Deterministic exact target resolution, positive additive query costs and worst-path optimization. No claim is made for noisy likelihoods, expected loss or calibration-changing observations.

---

## Theorem C — Sharp finite architecture for required structural gap

For binary unit-cost sensing and required integer gap `q>=1`, define

\[
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\}.
\]

Then the first componentwise gap-capable corner is

\[
\boxed{
(n^*,m^*,E^*)
=(h_2^*+q+1,\;h_2^*+q,\;h_2^*+q).
}
\]

It is componentwise sharp, and

\[
h_2^*(q)=\log_2q+O(1).
\]

Thus adaptive routing overhead grows logarithmically while fixed-mandatory structural burden grows essentially linearly in the required gap.

### Theorem C2 — Bounded-arity Pareto requirement

For maximum cue arity `b>=2`, define

\[
h_b^*(q)
=\min\left\{h\ge1:\frac{b^h-1}{b-1}-h\ge q\right\}.
\]

Separate minima are

\[
m_{\min}=E_{\min}=q+h_b^*(q),
\qquad
n_{\min}=q+h_2^*(q)+1,
\]

but for `b>2` the exact joint requirement is generally a Pareto frontier rather than one componentwise minimum.

Canonical example:

\[
q=3,b=4:\qquad(7,6,6),\;(8,5,5)
\]

are nondominated.

---

## Theorem D — Global balance does not bound adaptive advantage

There exists a finite deterministic binary unit-cost family in which every query is exactly 50/50 balanced over represented worlds but

\[
C_F\ge2^d,
\qquad
C_A\le d+1,
\]

so

\[
\boxed{
\frac{C_F}{C_A}
\ge
\frac{2^d}{d+1}
\to\infty.
}
\]

### Interpretation

Marginal cue balance does not control contingent decision value. Branch-exclusive resource geometry can force fixed resolution to provision all terminal resources while adaptive resolution pays routing cost plus one branch-specific resource.

### Claim ceiling

Existence/unbounded-family result only. It is not the sharp maximum ratio at fixed `(n,m)` under balance constraints.

---

## Theorem E — Nonlinear structural no-go for feedback reachability

For ecological-state gaps

\[
g_i=C_F(i)-C_A(i)\ge0
\]

and ordered contrast

\[
\Delta g=g_2-g_1\ge0,
\]

let the sensing-to-selection lift be nondecreasing with bounded marginal effect

\[
0\le f(g_2)-f(g_1)\le L\Delta g.
\]

With positive feedback-per-selection scale `B_f`,

\[
0\le G\le B_fL\Delta g.
\]

If complex return requires

\[
G>G_{\rm osc},
\]

then

\[
\boxed{
\Delta g>\frac{G_{\rm osc}}{B_fL}
}
\]

is necessary. Therefore any architecture class with

\[
B_fL\Delta g_{\max}\le G_{\rm osc}
\]

cannot generate the requested oscillatory regime for any lift in the declared monotone-Lipschitz class.

### Transport to natural-history structure

If `Delta g>=q` and all `g_i>=0`, at least one ecological state has `g_i>=q`, so Theorem C/C2 supplies a necessary exact or Pareto-minimal finite architecture for that state.

### Claim ceiling

Crossing the no-go bound means only `not ruled out`. It does not guarantee oscillation or identify empirical values of the lift or feedback parameters.

---

## Theorem F — Ecological recurrence filters structural selection

For a finite ergodic reversible ecological chain and centered state-specific selection reward,

\[
\boxed{
\sigma_{\rm eff}^2
=
\sum_r w_r\frac{1+r_r}{1-r_r}.
}
\]

Slow ecological modes amplify long-run evolutionary fluctuation only when structural reward variation loads onto those modes.

In the linear acquisition-cost special case with `0<=g_i<=g_max`,

\[
\sigma_{\rm eff}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}}.
\]

The bound is extremally sharp but not a generic prediction of realized variance.

---

## Theorem G — Compatible oscillation diagnoses feedback existence, not magnitude

Within the declared persistence domain

\[
0\le\alpha\le1,
\qquad
0\le\phi<1,
\]

and model-compatible trace range `0<=T<2`, a non-real conjugate local eigenpair excludes every zero-feedback decomposition, hence

\[
G>0
\]

for every compatible decomposition.

The result does not identify `G`, `alpha`, `phi`, or the causal fraction attributable to sensing architecture.

---

## Integrated chain

The V3 paper should be read as

\[
\boxed{
\begin{aligned}
&\text{natural-history alternatives + cues}\\
&\downarrow\\
&\text{target-relevant finite decision kernel}\\
&\downarrow\\
&(C_A,C_F)\\
&\downarrow\\
&\begin{cases}
\text{hard-budget exposure }[C_A,C_F),\\
\text{state-specific structural gap }g_i
\end{cases}\\
&\downarrow\\
&\text{state-dependent selection}\\
&\downarrow\\
&\text{feedback reachability / no-go}\\
&\downarrow\\
&\text{temporal filtering by ecological recurrence.}
\end{aligned}
}
\]

The balanced-query theorem shows that this chain depends on branch/resource geometry rather than global marginal cue balance. The exact kernel theorem shows that it depends on target-relevant geometry rather than raw descriptive complexity.

## Companion boundary

Detailed kernelization, fixed-cover certificates, color refinement, automorphism reductions, balanced-binary finite profiles and solver-validation ladders belong to the mathematical companion architecture in `manuscript/MATHEMATICAL_COMPANION_OUTLINE_V1.md`. They support the Letter but should not become equal biological headlines.

## Stop rule

Do not add another theorem family to make V3 look broader. Further work must repair a demonstrated proof, scope, clarity, format, visual or prior-art defect, or complete the already defined submission surface.
