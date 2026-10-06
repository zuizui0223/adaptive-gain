# Sharp ecological value of adaptivity under finite information budgets

Status: theorem extension on branch \`theory/opportunity-fitness-process-v1\`.

This note composes two exact layers already present in the repository:

1. the sharp bounded-arity structural bound on \((C_A,C_F)\); and
2. the opportunity-fitness map from completion cost to ecological value.

The result answers a different question from the sharp ratio theorem:

> Given only the number of represented worlds, the number of query resources,
> the maximum query arity, and an ecological opportunity-survival function,
> what is the **largest guarantee-level ecological advantage** contingent
> routing can possibly have?

## 1. Structural ingredients

Fix:

- \(n\ge2\) represented worlds;
- \(m\ge1\) unit-cost query resources;
- maximum query arity \(b\ge2\).

Let

\[
F_b(n,h)
\]

be the exact maximum number of internal-node occurrences in a productive
decision tree with at most \(n\) nonempty leaves, height at most \(h\), and
query arity at most \(b\).

Define

\[
\boxed{
I_h
=
\min\{m,F_b(n,h)\}.
}
\]

For every task in this scope with

\[
C_A=h,
\]

the existing structural theorem gives

\[
\boxed{
C_F\le I_h.
}
\]

The feasible adaptive depths satisfy

\[
1\le h\le\min(n-1,m).
\]

## 2. Arbitrary-depth sharpness

The private-pair tree construction can be oriented so that one deepest
child-0 spine has length \(h\).

Let \(x_0\) be the leftmost leaf on that spine.

For every internal node \(v\) on the spine, the private-pair construction
creates an opposite-target world \(y_v\) such that:

- \(x_0\) and \(y_v\) have opposite targets;
- the query \(q_v\) at node \(v\) is their unique declared separator.

Therefore any adaptive policy when the realized world is \(x_0\) must acquire
every one of the \(h\) spine queries.

Hence

\[
C_A\ge h.
\]

The tree itself resolves in worst-path cost at most \(h\), so

\[
\boxed{
C_A=h.
}
\]

Every one of the \(I_h\) internal-node queries has its own private opposite-
target pair, so every fixed resolver must contain all of them:

\[
\boxed{
C_F=I_h.
}
\]

Thus every feasible depth \(h\), not only a ratio-maximizing depth, has an
explicit exact witness

\[
\boxed{
(C_A,C_F)=(h,I_h).
}
\]

## 3. Theorem EF1 — sharp opportunity-value envelope

Let ecological opportunity survival be any nonincreasing function

\[
S(c)=P(B\ge c)
\]

on nonnegative completion costs.

Suppose timely guaranteed resolution has value \(v\ge0\).

For one task the guarantee-level adaptive opportunity advantage is

\[
R_{\rm opp}
=
v[S(C_A)-S(C_F)].
\]

If \(C_A=h\), then

\[
C_F\le I_h.
\]

Because \(S\) is nonincreasing,

\[
S(C_F)\ge S(I_h),
\]

and therefore

\[
R_{\rm opp}
\le
v[S(h)-S(I_h)].
\]

The arbitrary-depth witness attains equality.

Hence

\[
\boxed{
\max_{\substack{|W|=n,\ |Q|=m\\
\operatorname{arity}(q)\le b}}
R_{\rm opp}
=
v
\max_{1\le h\le\min(n-1,m)}
\left[
S(h)-S(I_h)
\right].
}
\]

This is a sharp ecological envelope, not merely an upper bound.

## 4. Corollary EF1.1 — sharp log-selection envelope

Let baseline fitness be \(w_0>0\), timely-resolution value be \(v\ge0\), and
let contingent control pay a common log maintenance cost \(\kappa\ge0\)
relative to the fixed comparator.

For a task with costs \((C_A,C_F)\),

\[
s
=
\log
\frac{w_0+vS(C_A)}
{w_0+vS(C_F)}
-
\kappa.
\]

The exact maximum over the same finite structural scope is

\[
\boxed{
s_{\max}
=
\max_h
\left\{
\log
\frac{w_0+vS(h)}
{w_0+vS(I_h)}
\right\}
-
\kappa.
}
\]

Thus the finite structural theorem supplies a hard ceiling on the amount of
selection that routeability alone can generate under a declared natural-history
opportunity process.


## 4b. Theorem EF2 — sharp evolutionary feasibility ceiling

Define the zero-maintenance sharp log-performance envelope

\[
\boxed{
\kappa_{\rm crit}(n,m,b;S,w_0,v)
=
\max_h
\log
\frac{w_0+vS(h)}
{w_0+vS(I_h)}.
}
\]

Suppose contingent sensing pays an adaptive-only constitutive log maintenance
cost

\[
\kappa\ge0
\]

relative to the universal fixed comparator.

Then every task in the declared finite scope satisfies

\[
s
\le
\kappa_{\rm crit}-\kappa.
\]

Therefore:

### No-go region

If

\[
\boxed{
\kappa>\kappa_{\rm crit},
}
\]

then

\[
s<0
\]

for **every** finite deterministic unit-cost task with the declared
\((n,m,b)\) limits.

No rearrangement of worlds, targets, or legal cue outcomes inside that scope can
make contingent routing selectively favorable through this opportunity-timing
mechanism alone.

### Boundary

If

\[
\kappa=\kappa_{\rm crit},
\]

then the best attainable task is neutral and no task has positive selection.

### Existence region

If

\[
\boxed{
0\le\kappa<\kappa_{\rm crit},
}
\]

then the arbitrary-depth private-pair witness at a maximizing depth has

\[
s>0.
\]

Hence

\[
\boxed{
\text{positive selection is possible in the scope}
\iff
\kappa<\kappa_{\rm crit}.
}
\]

This is an exact necessary-and-sufficient evolutionary feasibility threshold
for the declared comparator and opportunity process.

## Corollary EF2.1 — the structural scope sets a hard ceiling on evolvable control cost

The result reverses the usual direction of the model.

Instead of choosing an architecture cost and asking what happens in one task,
one can ask:

> how expensive may contingent control be before **no ecology in this entire
> finite information scope** can pay for it?

The answer is exactly

\[
\kappa_{\rm crit}.
\]

This gives the bounded-arity extremal theorem a direct evolutionary meaning.

## Corollary EF2.2 — under exponential opportunity loss the evolvable-cost ceiling vanishes at both urgency extremes

Let

\[
S(c)=e^{-\mu c}.
\]

For any finite feasible \(h\),

\[
\log
\frac{w_0+ve^{-\mu h}}
{w_0+ve^{-\mu I_h}}
\to0
\]

as

\[
\mu\to0^+
\]

and also as

\[
\mu\to\infty.
\]

Therefore

\[
\boxed{
\kappa_{\rm crit}(\mu)\to0
}
\]

at both ecological extremes.

If the structural scope contains any strict adaptive gap, then
\(\kappa_{\rm crit}(\mu)>0\) for every finite \(\mu>0\), so it attains a positive
interior maximum.

Thus a positive-cost contingent-control architecture can be evolutionarily
feasible only over an intermediate range of ecological urgency.

The exact number of disjoint feasible urgency intervals can depend on the
upper-envelope switches among structural depths; the theorem guarantees the
global zero-at-both-extremes geometry, not universal unimodality.


## 5. Exponential opportunity closure

For

\[
S(c)=e^{-\mu c},
\]

the sharp performance envelope is

\[
\boxed{
R_{\max}(\mu)
=
v
\max_h
\left(
e^{-\mu h}
-
e^{-\mu I_h}
\right).
}
\]

Each feasible depth supplies one ecological phase candidate.

Changing only the opportunity-loss rate \(\mu\) can change which structural
depth gives the maximum possible adaptive advantage.

## 6. Exact binary example — ratio-optimal and fitness-optimal depth differ

Take

\[
n=10,\qquad m=9,\qquad b=2.
\]

The relevant exact structural pairs are

\[
h=2:\quad (C_A,C_F)=(2,3),
\]

\[
h=3:\quad (3,7),
\]

\[
h=4:\quad (4,9).
\]

Larger \(h\) cannot improve the envelope because the fixed ceiling has already
saturated at 9 while the adaptive cost continues to increase.

The structural ratios are

\[
\frac32,\qquad
\frac73,\qquad
\frac94.
\]

Therefore the sharp **ratio** theorem chooses

\[
\boxed{h_{\rm ratio}=3.}
\]

But the opportunity values are

\[
E_2(\mu)=e^{-2\mu}-e^{-3\mu},
\]

\[
E_3(\mu)=e^{-3\mu}-e^{-7\mu},
\]

\[
E_4(\mu)=e^{-4\mu}-e^{-9\mu}.
\]

Their upper envelope switches at approximately

\[
\boxed{
\mu_{4\to3}=0.1546968
}
\]

and

\[
\boxed{
\mu_{3\to2}=0.6562560.
}
\]

Hence

\[
\boxed{
h^*(\mu)=
\begin{cases}
4,&0<\mu<0.1546968,\\
3,&0.1546968<\mu<0.6562560,\\
2,&\mu>0.6562560.
\end{cases}
}
\]

So:

- weak opportunity loss favors the largest absolute structural gap;
- intermediate loss favors the ratio-optimal depth;
- strong opportunity loss favors a shallower architecture that resolves sooner,
  even though its structural adaptive ratio is smaller.

Therefore

\[
\boxed{
\text{maximal structural adaptive ratio}
\neq
\text{maximal ecological value of adaptivity}.
}
\]

This is the cleanest reason not to use \(C_F/C_A\) as a fitness proxy.

## 7. Low- and high-urgency limits

For small \(\mu\),

\[
e^{-\mu h}-e^{-\mu I_h}
=
\mu(I_h-h)+O(\mu^2).
\]

Thus weak urgency selects the depth maximizing the **additive structural gap**

\[
I_h-h.
\]

For large \(\mu\), the second term becomes negligible and the envelope is
dominated by

\[
e^{-\mu h}.
\]

Thus strong urgency selects the smallest adaptive depth that still produces a
strict gap.

The ecological optimum therefore interpolates between two different structural
objectives:

\[
\boxed{
\text{weak urgency}\to\text{maximize absolute saved cost},
}
\]

\[
\boxed{
\text{strong urgency}\to\text{minimize time to exploit any strict saving}.
}
\]

The ratio objective is generally neither limit.

## 8. Biological interpretation

The structural theorem answers:

> how much fixed acquisition can contingent routing avoid?

The ecological envelope answers:

> how much can that avoidance matter before the opportunity disappears?

The answer depends jointly on:

- state-space size \(n\);
- available query resources \(m\);
- cue arity \(b\);
- ecological opportunity survival \(S\).

Thus natural history does not simply multiply a structural adaptive-gain score.
It can select a different region of the exact structural frontier.

## 9. Relation to PAYOFF

The envelope supplies an exact upper bound on one mechanistic source of
recoverable benefit \(R\).

PAYOFF can then compare that benefit against architecture cost:

\[
\Phi=R-K.
\]

For example, if every biologically feasible task in a declared scope satisfies

\[
R_{\rm opp}\le R_{\max},
\]

then any architecture cost

\[
K>R_{\max}
\]

rules out positive net architecture value from this routeability mechanism
alone.

This is stronger than inserting an arbitrary linear conversion coefficient
between structural gap and fitness.

## 10. Prior-art boundary

Composing a constraint bound with a monotone utility function is elementary,
and ecological time discounting is not new.

The repository-specific result is the exact sharp composition:

- the finite hidden-world/query topology supplies the attainable
  \((C_A,C_F)\) frontier;
- the ecological opportunity process ranks points on that frontier;
- the same constructive witnesses attain the resulting ecological envelope.

The novelty should therefore be attached to the **sharp cross-layer envelope**
and its biological interpretation, not to exponential discounting or finite
maximization by themselves.
