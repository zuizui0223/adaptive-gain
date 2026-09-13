# Nonlinear sensing-to-feedback no-go theorem v2

## Purpose

This revision separates two structural quantities that must not be collapsed:

1. the adaptive-versus-fixed sensing gap **within** ecological state `i`,
   \[
   g_i=C_F(i)-C_A(i)\ge0;
   \]
2. the ordered structural contrast **between** two ecological states,
   \[
   \Delta g=g_2-g_1\ge0.
   \]

The local feedback bridge acts on the state-to-state selection contrast and therefore on `Delta g`, not on one `g_i` in isolation.

The theorem remains intentionally one-sided. It proves when the available structural contrast is too small to reach a requested local dynamical regime. It does not claim that every system above the bound realizes that regime.

---

## 1. State-specific sensing gaps

In ecological state `i`, let

\[
C_A(i)
\]

be the minimum worst-case cue-acquisition cost under adaptive outcome-contingent sensing and

\[
C_F(i)
\]

be the minimum cost of a fixed resolving bundle for the same declared target. Define

\[
\boxed{g_i=C_F(i)-C_A(i)\ge0.}
\]

`g_i` is a structural property of the state-specific finite sensing task. It is not intrinsically fitness.

Under additive cue-acquisition cost `c>0`, a minimal state-specific selection lift is

\[
s_i=cg_i-\kappa,
\]

where `kappa` is a state-independent maintenance debit. Hence, for two states with `g_2>=g_1`,

\[
\Delta s=c(g_2-g_1)=c\Delta g.
\]

This is the constructive linear special case.

---

## 2. Nonlinear lift class

Let the state-specific selection contribution be

\[
s_i=f(g_i)-\kappa,
\]

where `f` is nondecreasing and has bounded marginal effect on the relevant gap domain:

\[
0\le f(g_2)-f(g_1)\le L(g_2-g_1)
=L\Delta g
\]

for finite `L>0`.

This class allows linear, saturating, diminishing-return and piecewise-linear sensing-to-selection maps and does not require differentiability.

Let

\[
B=-\beta e>0
\]

be the local feedback-per-selection scale. Then

\[
G=B\Delta s
\]

obeys

\[
\boxed{0\le G\le BL\Delta g.}
\]

---

## 3. Theorem — nonlinear lower bound on between-state structural contrast

For local evolutionary persistence `alpha` and ecological persistence `phi`, the complex-eigenpair boundary is

\[
G_{\rm osc}
=\frac{(\alpha-\phi)^2}{4(1-\phi)}.
\]

A stable oscillatory response requires the strict inequality

\[
G>G_{\rm osc}
\]

while remaining below the upper stability boundary.

Because every admissible lift satisfies

\[
G\le BL\Delta g,
\]

oscillation is possible only if

\[
\boxed{
\Delta g>
\frac{G_{\rm osc}}{BL}.
}
\]

For integer state gaps, the minimum necessary ordered contrast is

\[
\boxed{
q_{\rm osc}^{\rm nec}
=
\left\lfloor
\frac{G_{\rm osc}}{BL}
\right\rfloor+1.
}
\]

This is a necessary condition only.

---

## 4. Architecture-class no-go corollary

Suppose a declared class of state-specific sensing tasks satisfies

\[
0\le g_i\le q_{\max}
\qquad\text{for every admissible ecological state }i.
\]

Then any ordered state pair satisfies

\[
\Delta g\le q_{\max}.
\]

Therefore

\[
\boxed{
BLq_{\max}\le G_{\rm osc}
\Longrightarrow
\text{oscillatory feedback is unreachable for the entire class.}
}
\]

This is the headline no-go orientation:

```text
state-specific architecture class
-> ceiling on every g_i
-> ceiling on between-state Delta g
-> ceiling on feedback G
-> requested regime impossible
```

---

## 5. From required contrast back to one state-specific architecture

If a regime requires

\[
\Delta g\ge q
\]

and state gaps are nonnegative, then

\[
g_2=g_1+\Delta g\ge q.
\]

Thus at least one ecological state must contain a finite sensing task capable of gap at least `q`. The sharp single-task finite architecture theorem may therefore be applied to that high-gap state.

For binary unit-cost sensing, the exact first componentwise corner is

\[
(n^*,m^*,E^*)
=
(h_2^*(q)+q+1,\ h_2^*(q)+q,\ h_2^*(q)+q),
\]

with

\[
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\}.
\]

For bounded arity greater than two, the required high-gap state generally lies on a Pareto frontier over represented alternatives, cue resources and irreducible fixed-side obligations.

---

## 6. Canonical binary no-go

Take

\[
\alpha=1,
\qquad
\phi=\tfrac12,
\qquad
B=\tfrac12,
\qquad
L=\tfrac14.
\]

Then

\[
G_{\rm osc}=\tfrac18,
\qquad
BL=\tfrac18,
\]

so

\[
q_{\rm osc}^{\rm nec}=2.
\]

Existing binary extremal results give state-specific gap ceiling one for every task with any one of:

- at most five represented worlds;
- at most four declared binary cues;
- at most four minimal productive-frontier obligations.

Because all state gaps in any such class lie in `[0,1]`, every between-state contrast satisfies

\[
|\Delta g|\le1.
\]

Hence all three classes are ruled out without exact linearity.

The constructive linear special case pairs a zero-gap state with the known six-world/five-query state having `g=2`. Their structural contrast is two, meeting the necessary finite threshold when the marginal ceiling is attained. This construction does not upgrade the nonlinear necessary condition to sufficiency.

---

## Claim ceiling

The theorem licenses:

- a necessary lower bound on between-state structural contrast;
- a class-level impossibility result when all state-specific gaps are too small;
- transport of that contrast requirement into a minimum or Pareto-minimal architecture for at least one high-gap state;
- recovery of the additive linear model as a constructive special case.

It does **not** license:

- interpreting one state gap `C_F-C_A` as feedback by itself;
- claiming that crossing the contrast threshold guarantees oscillation;
- an empirical estimate of `B`, `L`, `alpha` or `phi`;
- noisy-sensing, stochastic-demographic or global-bifurcation extensions;
- a universal natural threshold.
