# Relational routeability theorem spine v1

Status: canonical post-freeze math–ecology integration spine. This file does not modify the frozen Evolution Letters V5 initial-submission surface.

## Paper-level question

> Can two ecological decision problems contain the same physical cue environment and the same conventional information quantities, yet differ sharply in how costly they are to resolve because the focal action induces a different conditional decision topology?

Answer: yes.

---

## Theorem 1 — relational routeability

For every integer \(d\ge2\), there exists one finite physical cue environment

\[
\mathcal E_d=(W_d,Q_d,c)
\]

and two target/action maps

\[
T_R,\qquad T_K
\]

defined on that same environment such that the two tasks share:

- the same represented worlds;
- the same query identities;
- the same query costs;
- the same complete query-outcome matrix;
- exact 50/50 balance for every binary query;
- every cue-only marginal and joint distribution of every order;
- the same target multiplicities \((2^d+2,2^d)\);
- the same target entropy;
- the same full-vocabulary target information
  \[
  I(T;Q_{\mathrm{all}})=H(T).
  \]

Yet the routeable task satisfies

\[
C_F(T_R)\ge2^d,
\qquad
C_A(T_R)\le d+1,
\]

while the matched control satisfies exactly

\[
\boxed{
C_A(T_K)=C_F(T_K)=2.
}
\]

Therefore

\[
\boxed{
\frac{C_F(T_R)}{C_A(T_R)}
-
\frac{C_F(T_K)}{C_A(T_K)}
\ge
\frac{2^d}{d+1}-1
\to\infty.
}
\]

### Interpretation

Routeability is not an intrinsic scalar property of the physical environment.

It is relational:

\[
\boxed{
\text{environment}
+
\text{available cues}
+
\text{cue costs}
+
\text{focal action}
\longrightarrow
\text{decision topology}.
}
\]

---

## Corollary 1 — exact ecological budget interaction

Set one shared hard observation budget

\[
B=d+1.
\]

Since \(2^d>d+1\) for \(d\ge2\),

\[
C_A(T_R)\le B<C_F(T_R).
\]

Thus the routeable task is guaranteed resolvable adaptively but not by any fixed bundle of cost at most \(B\).

For the matched control,

\[
C_A(T_K)=C_F(T_K)=2\le B,
\]

so both adaptive and fixed resolution are guaranteed.

Using guaranteed-success indicators:

\[
(S_{R,A},S_{R,F},S_{K,A},S_{K,F})
=
(1,0,1,1).
\]

Therefore

\[
\boxed{
(S_{R,A}-S_{R,F})
-
(S_{K,A}-S_{K,F})
=
1.
}
\]

This is the exact mathematics-to-ecology bridge.

---

## Proposition 2 — finite pairwise-information stress controls

At routing depths 2 and 3, registered matched controls additionally preserve:

- the same physical cue matrix;
- the same target multiplicities;
- the same **multiset** of canonical target–cue \(2\times2\) contingency profiles.

Thus the multiset of pairwise target–cue information strengths is matched.

### Depth 2

\[
C_A=C_F=2.
\]

### Depth 3

\[
C_A=C_F=3.
\]

These are finite controls only.

No asymptotic name-by-name pairwise match is claimed.

---

## Proposition 3 — summary sufficiency hierarchy

The current deterministic theory supplies explicit examples showing that the following summaries need not identify routeability:

1. state count;
2. query count;
3. all one-cue marginals;
4. the full cue-only joint distribution;
5. target prevalence;
6. target entropy;
7. total full-vocabulary target information;
8. at finite registered scopes, the multiset of pairwise target–cue information-strength profiles.

By contrast, the complete action-conditioned table

\[
(w,T(w),q_1(w),\ldots,q_m(w))
\]

together with cue costs specifies the deterministic finite routeability problem.

### Interpretation

The theory is not a claim that topology is fundamentally unobservable.

It is a theorem about the insufficiency of rich summaries that omit the action-conditioned arrangement.

---

## Corollary 4 — measurement rule

A natural system is routeability-evaluable only if one can defensibly specify:

- focal action;
- represented alternatives;
- cue identities;
- cue outcomes across alternatives;
- cue costs or timing constraints.

Then compute:

\[
C_A,\quad C_F,\quad g=C_F-C_A,
\]

and compare with a biological budget \(B\).

Observed animal behavior should be kept separate from the structural optimum.

This yields the rule:

\[
\boxed{
\text{measure the action-conditioned cue table first; summarize it second}.
}
\]

---

## Experimental realization A — minimal causal test

Four states, three cues.

Purpose:
- demonstrate behavioral use of contingent routeability;
- localize the effect to the exact budget window.

Primary pattern:

\[
\Delta_{B=1}=0,\qquad
\Delta_{B=2}>0,\qquad
\Delta_{B=3}=0.
\]

This remains the first biological experiment.

---

## Experimental realization B — exact-balanced stress test

Ten states, six cues, every cue exactly 5/5 balanced.

Routeable:

\[
(C_A,C_F)=(3,4).
\]

Matched control:

\[
(C_A,C_F)=(2,2).
\]

At \(B=3\):

- routeable contingent ceiling = 1;
- routeable best fixed ceiling = \(4/5\);
- control contingent ceiling = 1;
- control best fixed ceiling = 1.

Therefore

\[
\boxed{
(1-4/5)-(1-1)=1/5.
}
\]

This is the stronger second experiment.

---

## Ecological consequence hierarchy

### Directly supported

- environmental amount/distribution does not determine exact decision cost;
- total available target information does not determine acquisition architecture;
- nominal niche breadth does not determine information-processing burden;
- potential interaction richness need not equal behaviorally accessible interaction richness.

### Supported only as modifiers

- heterogeneity → evolved niche breadth;
- specialist/generalist evolutionary outcomes.

These require a fitness/evolutionary lift.

### Not yet supported

- diversity–stability;
- community resilience;
- ecosystem-function stability.

These require explicit population/community dynamics.

---

## Prior-art boundary

Treat as prior art:

- adaptive feature acquisition;
- costly sequential information acquisition;
- value of information;
- uniform separating systems;
- generic adaptivity gaps;
- the general fact that entropy need not be a complete operational invariant.

The present contribution is the exact ecological composition:

\[
\boxed{
\text{same cue environment}
+
\text{different action-conditioned topology}
+
\text{same budget}
\Rightarrow
\text{different feasible access regime}.
}
\]

---

## V5 ceiling

The frozen V5 needs only the qualitative theorem:

> conditional decision topology is a relational ecological axis not determined by strong distributional summaries of heterogeneity or information, and finite ecological budgets expose its consequences.

Do not reopen V5 for:
- stochastic expected-loss theory;
- diversity–stability dynamics;
- exact-balanced stress-test data;
- additional theorem families.

---

## Next theory paper

Replace guaranteed exact resolution by stochastic expected loss:

\[
J(\pi)
=
\mathbb E[C_\pi]
+
\lambda \mathbb E[L(A,T)].
\]

Main future question:

> Does the quantity/topology separation survive when cues are noisy, errors are allowed, and policies minimize expected loss rather than worst-case exact-resolution cost?

This is a separate paper.

## Stop rule

No new theorem family is needed for the deterministic program.

Next work is limited to:
- manuscript synthesis;
- prior-art tightening;
- experimental implementation;
- stochastic expected-loss theory as a separate project.
