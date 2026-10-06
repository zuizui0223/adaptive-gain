# Fitness-process promotion ledger

Status: claim-priority ledger for PR #67. This file separates the manuscript
spine from useful but non-headline supporting theory.

## One biological question

> How does a finite ecological information structure become a fitness
> difference, and when does changing natural history select a different sensing
> architecture or routing policy?

The paper should not be sold as a new general theory of sequential decisions.

## Tier A — manuscript spine

### A0. Sharp cross-layer robust-value envelope

Promote `SHARP_OPPORTUNITY_FITNESS_ENVELOPE.md` to the first theorem result.

For fixed world count (n), query count (m), query arity (b), and ecological
opportunity survival (S), define

[
I_h=min{m,F_b(n,h)}.
]

Then the exact maximum **worst-state / frequency-free** ecological value of contingent routing is

[
oxed{
R_{\rm robust,max}
=
vmax_h[S(h)-S(I_h)].
}
]

The same constructive witnesses attain the bound at every feasible adaptive
depth.

This is stronger than maximizing (C_F/C_A): natural history re-ranks the exact
structural frontier.

In the binary (n=10,m=9) example, the structural ratio is maximized at
(h=3), while the exponential-opportunity robust-value envelope selects
(h=4	o3	o2) as ecological urgency increases.

This should be the main nontrivial theorem because it uses the repository's
distinct sharp extremal mathematics rather than generic sequential-decision
theory.


The same envelope gives an exact **robust statewise feasibility** threshold:

[
kappa_{m crit}
=
max_h
log
rac{w_0+vS(h)}
{w_0+vS(I_h)}.
]

For an adaptive-only log maintenance cost (kappa),

[
oxed{
	ext{some task in the structural scope has positive net adaptive value in every represented world}
iff
kappa<kappa_{m crit}.
}
]

This no-go/existence form should be emphasized because it converts the finite
routeability theorem into a direct statement about which control costs can be
paid **robustly without knowing encounter frequencies**.


On the additive PAYOFF scale, the same statement is even simpler:

\[
\boxed{
K_{\rm crit}
=
R_{\max}
=
\max_h[U(h)-U(I_h)].
}
\]

Positive architecture value in **every represented world** exists somewhere in
the declared finite scope exactly when

\[
K<K_{\rm crit}^{\rm robust}.
\]

This makes the repository relation explicit: adaptive-gain derives the sharp **robust recoverable-benefit** ceiling, while
PAYOFF evaluates the relevant \(R-K\).  Distribution-sensitive expected \(R\)
can exceed the robust floor and requires branch frequencies.


Also retain the interpretive correction

[
C_F/C_A	oinfty

otRightarrow
s	oinfty.
]

For bounded timely-resolution value (v),

[
s
le
log(1+v/w_0)-kappa.
]

This is important because it prevents the repository's unbounded structural
ratio theorem from being over-read as an unbounded biological effect.


### A0.5. Global arity-limited robust no-go

Promote the scalable-scope consequence from
\`EVOLUTIONARY_RESOURCE_FRONTIER.md\`.

With unlimited finite world/query counts but cue arity bounded by \(b\),

\[
K_{\rm crit,robust}^{(b)}
=
\max_{h\ge2}
[U(h)-U(J_b(h))],
\qquad
J_b(h)=\frac{b^h-1}{b-1}.
\]

No finite task of arity at most \(b\) can guarantee positive statewise net value
for a control cost above this ceiling.

For exponential opportunity value,

\[
U(c)=ve^{-\mu c},
\]

the absolute unrestricted-information ceiling is

\[
K_{\rm crit,robust}^{(\infty)}
=
ve^{-2\mu}.
\]

Hence a declared cost \(K\) induces an exact minimum cue arity

\[
b_{\min}
=
\min\{b\ge2:K<K_{\rm crit,robust}^{(b)}\},
\]

or \(b_{\min}=\infty\) when even unlimited finite information structure cannot
pay the cost.

Canonical example:

\[
\mu=0.3,\quad v=1,\quad K=0.30
\]

gives

\[
K_{\rm crit,robust}^{(2)}\approx0.290085
<
0.30
<
K_{\rm crit,robust}^{(3)}\approx0.386328,
\]

so

\[
\boxed{b_{\min}=3.}
\]

This is a global no-go over the whole finite model class, not a generic claim
that higher-fidelity sensory systems are fitter.


### A1. Exact structural source object

Retain the existing finite task and its exact feasible routing structure.

Use C_A and C_F only as guaranteed-complexity objects.

Required claim boundary:

C_A is not fitness, expected latency, or the uniquely evolved policy.


### A1.25. Absolute robust versus expected ceilings

Promote the unrestricted distinction:

\[
R_{\rm robust}^{\sup}
=
U(2)-U_\infty,
\]

while

\[
R_{\rm expected}^{\sup}
=
U(1)-U_\infty
\]

when encounter frequencies may be arbitrarily skewed.

This creates an exact expected-only cost interval

\[
U(2)-U_\infty
\le K
<
U(1)-U_\infty.
\]

Use the exponential \(\mu=0.3,\ K=0.60\) binary witness to show that a control
cost can be impossible to repay robustly under **any** finite information
architecture yet still be favored in expectation when hard states are rare.

This should be presented as the sharp consequence of adding encounter
frequencies to the structural theory, not as a generic novelty claim about
expected versus worst-case optimization.


### A1.5. Robust base plus early-termination premium

State explicitly in the main text:

\[
R_{\rm robust}
=
U(C_A)-U(C_F)
\]

is the largest value difference that can be guaranteed in the slowest adaptive
branch.

For a world distribution \(p_x\),

\[
R_{\rm expected}(\pi)
=
\sum_xp_xU[T_\pi(x)]-U(C_F)
\ge
R_{\rm robust}
\]

for a minimax tree, and the inequality can be strict.

Therefore the sharp envelope is an exact **frequency-free floor/threshold**.
It is not an upper bound on expected selection under skewed encounter
frequencies.

Promote the exact decomposition

\[
\boxed{
R_{\rm expected}(\pi)
=
R_{\rm robust}(\pi)
+
P_{\rm early}(\pi),
}
\]

where

\[
P_{\rm early}(\pi)
=
\sum_xp_x[U(T_\pi(x))-U(H_\pi)]
\ge0.
\]

This gives a direct biological interpretation to encounter frequencies:
frequencies do not change the robust structural base; they determine how much
extra value is earned by early-terminating branches.

Use the exact four-world rescue witness as the canonical example:
\(C_A=C_F=2\) but expected adaptive value becomes positive when the common
one-step state exceeds the threshold
\(p^*=2e^{-\mu}/(3+2e^{-\mu})\), equal to \(1/4\) at
\(\mu=\log2\).

This distinction must appear before any use of the word "fitness."


### A1.75. Frequency-assisted evolvability band

Retain the scalable robust-versus-expected ceiling distinction:

\[
\sup R_{\rm robust}=U(2)-U_\infty,
\]

\[
\sup R_{\rm expected}=U(1)-U_\infty.
\]

Thus architecture costs in

\[
U(2)-U_\infty
\le K
<
U(1)-U_\infty
\]

cannot be repaid robustly by any finite information architecture, but can be
repaid in expectation when ecological encounter frequencies strongly favor an
early-terminating branch.

For exponential opportunity value the band is

\[
ve^{-2\mu}
\le K
<
ve^{-\mu}.
\]

Use this to make the robust/expected distinction biologically concrete. Do not
present it as a new generic adaptivity-gap theorem.


### A2. Expected-value extension above the robust floor

Promote the general kernel form:

[
Delta R_{i:j}
=
int_0^infty
[F_i(t)-F_j(t)]m(t),dt.
]

This is the cleanest expected-value process interface, but it is established in general decision theory and is **not** the theorem-level novelty.

The biological interpretation is:

- finite topology constrains feasible completion profiles;
- organisms/policies generate (F_i(t));
- natural history generates (m(t));
- their overlap generates performance value.

Hard deadlines and stochastic opportunity survival are special cases.

### A3. Opportunity process microfounding architecture-payoff curvature

Promote the hazard-curvature identity from
OPPORTUNITY_ARCHITECTURE_LANDSCAPE:

[
R''(r)
=
q(c)
[
h(c)^2(1-q(c))-h'(c)
].
]

This is the strongest distinct bridge to PAYOFF because it derives the shape of
recoverable architecture benefit from a measurable ecological time process.

Emphasize the contrast:

- constant/decreasing hazard can generate increasing returns;
- sufficiently increasing hazard can generate diminishing returns;
- therefore natural-history opportunity shape can change the qualitative
  architecture landscape.

The generic convex tangent/secant barrier itself belongs to PAYOFF and should
not be re-claimed here.

### A4. Policy is selected within topology, not identified by C_A

Retain one compact result from FITNESS_OPTIMAL_ROUTING_VS_MINIMAX:

a minimax-optimal tree need not maximize opportunity-weighted fitness.

Use the exact witness only to prevent over-interpretation of C_A.

Do not headline worst-case versus expected-case optimization as novel.

### A5. Real-data process-shape anchor

Promote the Chandel Figure 3a aggregate result only at its valid ceiling.

Key receipt:

- +IR effect is strongly late-weighted after CO2 cessation;
- half of aggregate signed post-pulse IR advantage accumulates only after
  approximately 46 s in both post-pulse periods;
- short value-of-time kernels therefore count substantially less of the same
  observed behavioral effect than long kernels.

Use this to demonstrate why temporal effect shape and ecological value-of-time
must be measured separately.

Do not call this an adaptive-gain, individual-latency, or fitness validation.

## Tier B — supporting theory / Supplement

### B1. Exact stochastic-opportunity selection coefficient

Keep:

[
s_{opp}
=
log
rac{w_0+vS(C_A)}
{w_0+vS(C_F)}
-kappa.
]

Its main role is to show that the previous linear lift is a local approximation
rather than a primitive biological assumption.

### B2. Comparator semantics

Keep the U / A / P distinction:

universal fixed bundle,
outcome-contingent routing,
context-preindexed repertoire.

This is essential for empirical claim discipline, but it is a gate rather than
the headline theorem.

### B3. Finite urgency phase diagram

Keep ECOLOGICAL_URGENCY_POLICY_PHASES as supporting structure.

Its polynomial envelope and finite switch points are mathematically clean but
are not priority novelty; deadline-sensitive decision trees and time-pressure
cue changes have substantial prior art.

### B4. Stochastic completion-time ordering

Keep equal-mean reversals and stochastic-dominance statements as interpretation
aids.

Do not headline them; response-time distributions and stochastic orders are
established.

## Tier C — reserve / cross-repository bridge

### C1. Finite-jump architecture barrier under exponential opportunity loss

Retain as a mechanistic example only.

PAYOFF already owns the general convex-recovery local/global threshold
distinction.

adaptive-gain's contribution is the upstream ecological derivation of
curvature, not another barrier theorem.

### C2. Aedes full prospective experiment programme

Retain AEDES_OPPORTUNITY_FITNESS_BRIDGE as an empirical roadmap.

Do not let experimental planning dominate the theory manuscript until the
routing comparator and individual completion-time gates are closed.

### C3. Raw-video tracking pipeline

Keep frame_preserving_tracking and its tests as reproducibility support.

The Figure 3a raw-video mapping is currently unresolved; do not make the
manuscript depend on individual video reprocessing.

### C4. Raw-video mapping blocker

Retain the blocker receipt.

It demonstrates claim discipline and prevents inferred video assignments, but
it is not manuscript content unless data availability is discussed.

## Tier D — move outside this paper

The VHOST example/audit machinery is not part of the Aedes opportunity-fitness
spine.

It should remain a separate reserve/companion route unless it becomes the
selected empirical system.

Do not use extra biological examples merely to increase apparent generality.

## Claims explicitly demoted

Do not headline any of the following:

- routeability is useful;
- sequential cues save time;
- time pressure changes cue use;
- faster decisions can be fitter;
- mean response time is insufficient;
- worst-case and expected-cost trees differ;
- stochastic dominance orders completion-time distributions;
- deadlines can change optimal decision trees;
- convex recovery can generate a finite-jump barrier.

These are established, generic, or already owned elsewhere in the programme.

## Proposed main-result hierarchy

1. **Sharp robust frontier:** finite topology gives the exact frequency-free
   value floor and robust architecture-cost threshold.
2. **Expected-value premium:** branch frequencies add the exact
   early-termination premium above that robust floor.
3. **Policy consequence:** the biologically favored routing policy need not be
   the minimax \(C_A\) policy because a worse worst case can buy a larger
   early-termination premium.
4. **Architecture consequence:** opportunity hazard shape determines recovery
   curvature and therefore whether time-saving architecture has increasing or
   diminishing returns.
5. **Empirical anchor:** a real multisensory Aedes response has strongly
   nonuniform temporal benefit, so scalar effect magnitude cannot determine
   ecological value.

## Current strongest one-sentence claim

> Exact routing structure determines a robust value floor; encounter
> frequencies add an early-termination premium, so the architecture that
> maximizes structural adaptive gain need not maximize expected evolutionary
> value.

A process-oriented companion sentence is:

> By weighting where in time a finite decision architecture succeeds, natural
> history can change both which routing policy is favored and the curvature of
> the architecture's fitness landscape.

## Publication consequence

The current branch should remain a draft theory-development PR.

A manuscript promotion should wait until:

- full tests pass at the final theory head;
- the opportunity-hazard curvature result survives a dedicated prior-art audit;
- the Chandel aggregate result remains clearly labeled as a process-shape
  anchor;
- unrelated VHOST material is separated from the canonical reader path.
