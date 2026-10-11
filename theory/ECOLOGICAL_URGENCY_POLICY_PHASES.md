# Finite urgency phase diagram for contingent sensing policies

Status: process extension on branch theory/opportunity-fitness-process-v1.

This note generalizes the exact \(\mu=\log 2\) switching witness in
\`FITNESS_OPTIMAL_ROUTING_VS_MINIMAX.md\`.

The mathematical ingredients are elementary finite-policy and polynomial facts.
The ecological contribution is to make explicit how a fixed finite cue topology
can support a finite sequence of optimal sensing-policy rewiring events as the
ecological value of delay changes.

## 1. Fixed finite task, fixed world frequencies

Fix:

- a finite hidden-world set \(X\);
- a finite positive-cost query vocabulary;
- a target relation;
- world probabilities \(p_x\);
- the set \(\Pi\) of deterministic guaranteed-resolving contingent policies.

For \(\pi\in\Pi\), let

\[
T_\pi(x)
\]

be the realized completion cost in world \(x\).

Assume integer query costs for the polynomial form below.

Under exponential value of completion time,

\[
V_\mu(t)=e^{-\mu t},
\qquad
\mu>0,
\]

the ecological performance of policy \(\pi\) is

\[
J_\pi(\mu)
=
\sum_x p_x e^{-\mu T_\pi(x)}.
\]

## 2. Depth-mass representation

Let

\[
a_{\pi,d}
=
\sum_{x:T_\pi(x)=d}p_x.
\]

Then

\[
a_{\pi,d}\ge0,
\qquad
\sum_d a_{\pi,d}=1.
\]

Write

\[
z=e^{-\mu}\in(0,1).
\]

Then

\[
\boxed{
J_\pi(z)
=
\sum_{d=0}^{D_\pi}a_{\pi,d}z^d.
}
\]

Thus every policy is represented by a probability-generating polynomial of its
completion-cost distribution.

Two different decision trees that induce the same weighted completion-cost
distribution are fitness-equivalent under every exponential urgency level.

## Theorem UP1 — urgency-driven policy rewiring has finitely many critical points

Take two policies \(\pi,\rho\) with distinct depth-mass profiles.

Their value difference is

\[
J_\pi(z)-J_\rho(z)
=
\sum_{d=0}^{D}
(a_{\pi,d}-a_{\rho,d})z^d,
\]

a nonzero polynomial of degree at most

\[
D=\max(D_\pi,D_\rho).
\]

Therefore the two policies can tie at at most \(D\) values of
\(z\in(0,1)\), and hence at at most \(D\) positive urgency values

\[
\mu=-\log z.
\]

Because the finite task admits only finitely many deterministic policies, the
fitness-optimal policy can change only finitely many times as \(\mu\) varies.

Hence

\[
\boxed{
\text{a fixed finite decision topology has a finite urgency phase diagram.}
}
\]

The optimal sensing policy is piecewise constant in \(\mu\), apart from ties at
a finite set of critical urgency values.

This does not claim that the number of distinct trees is small. It claims only
that finite decision structure prevents an infinite accumulation of policy
switches over a finite positive urgency domain.

## 3. Low-urgency limit

Expand

\[
e^{-\mu T}
=
1-\mu T+\frac{\mu^2T^2}{2}-\cdots.
\]

Then

\[
\boxed{
J_\pi(\mu)
=
1
-\mu E_\pi[T]
+\frac{\mu^2}{2}E_\pi[T^2]
+O(\mu^3).
}
\]

Therefore, among policies with unequal mean completion cost, sufficiently weak
urgency selects the policy with lower

\[
E_\pi[T].
\]

So the low-urgency evolutionary objective approaches expected completion cost,
not worst-case completion cost.

If policies tie in mean completion cost, higher moments determine the local
ordering. In particular, with equal means the positive second-order term can
favor a more dispersed completion-time profile because exponential value
rewards an early tail.

This is exactly why equal mean decision time is not a sufficient evolutionary
summary.

## 4. High-urgency limit

Let

\[
d_{\min}(\pi)
=
\min\{d:a_{\pi,d}>0\}.
\]

As

\[
\mu\to\infty
\quad\Longleftrightarrow\quad
z\to0,
\]

the leading term is

\[
J_\pi(z)
\sim
a_{\pi,d_{\min}}z^{d_{\min}}.
\]

Therefore sufficiently strong urgency first favors the policy with the smallest
possible earliest completion depth.

Among policies tied in earliest depth, it favors the one with the largest
probability mass resolved at that depth.

If that coefficient also ties, the next depth coefficient decides, and so on.

Thus high urgency induces a lexicographic preference for the left tail of the
completion-time distribution:

\[
\boxed{
(d_{\min},
-a_{d_{\min}},
-a_{d_{\min}+1},
\ldots).
}
\]

Biologically, severe time pressure can favor sacrificing difficult or rare
states in order to create more very-early successful decisions, even while
guaranteed resolution of all states is retained eventually.

## 5. Exact recovery of the registered \(\mu=\log2\) witness

The balanced policy has profile

\[
a_2=1,
\]

so

\[
J_B(z)=z^2.
\]

The prioritized policy with path multiset

\[
\{1,2,3,3\}
\]

under equal world frequencies has

\[
J_P(z)
=
\frac14z
+
\frac14z^2
+
\frac12z^3.
\]

Their difference factorizes:

\[
J_P-J_B
=
\frac{z}{4}(2z-1)(z-1).
\]

The unique interior switch is

\[
z=\frac12,
\]

hence

\[
\boxed{
\mu^*=\log2.
}
\]

The low-urgency side favors the balanced tree. The high-urgency side favors the
prioritized tree, exactly as predicted by Sections 3-4.

## 6. Structural versus ecological policy objects

The finite task determines the feasible policy set

\[
\Pi.
\]

The core adaptive-gain quantity

\[
C_A
=
\min_{\pi\in\Pi}\max_xT_\pi(x)
\]

selects minimax trees.

The ecological urgency family instead selects

\[
\pi^*(\mu)
\in
\arg\max_{\pi\in\Pi}J_\pi(\mu).
\]

Thus routeability should be interpreted as a **feasible policy geometry**, not
as one fixed evolved tree.

Natural history can move the lineage among distinct optimal policies without
changing:

- the species present;
- the hidden worlds;
- the target;
- the cue vocabulary;
- query costs;
- world frequencies.

Only the ecological value of delay must change.

## 7. Empirical prediction

If a focal species experiences populations or seasons differing in opportunity
duration but sharing the same sensory vocabulary, the theory predicts
piecewise changes in cue ordering rather than necessarily a smooth change in
the amount of cue use.

A useful empirical analysis should therefore test:

1. whether completion-time profiles of candidate cue orders cross;
2. whether estimated value-of-time differs among ecological contexts;
3. whether observed cue order changes near predicted policy-crossing regions.

This is stronger than asking whether decisions become faster under time
pressure.

## 8. Prior-art boundary

Do not claim novelty for:

- polynomial expected utility of finite completion-time distributions;
- finite roots of polynomial differences;
- expected-cost versus worst-cost tree optimization;
- response-time urgency effects;
- satisficing or cue dropping under time pressure.

Time-sensitive decision trees already optimize late penalties and completion
constraints (for example Kao & Tang 2014, DOI 10.1287/ijoc.2013.0560), and
behavioral experiments show altered cue use under time pressure.

The repository-specific use is narrower:

> an exact ecological hidden-world/query topology defines the finite feasible
> routing set, and the ecological value-of-delay induces a finite phase diagram
> over those contingent sensing policies.

The ecological manuscript should rely on this cross-layer composition rather
than claim the polynomial-envelope fact itself as new.
