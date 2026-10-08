# Target-prevalence constraints restore cue-arity dependence in expected adaptive value

Status: side theorem on the opportunity-fitness branch. This concerns fixed target-class prevalence, not fixed world probabilities and not the frequency-free robust frontier.

## The ecological question

RF7 proves that when world probabilities are free to concentrate arbitrarily, the sharp expected-value supremum at fixed finite (n,m) is independent of cue arity b >= 2.

That does not imply cue arity is irrelevant after biologically meaningful constraints are placed on the distribution of decisions.

Here the target has exactly two categories, and their *aggregate prevalence* is fixed.

This captures, for example, environments with a fixed proportion of acceptable and unacceptable opportunities, while allowing within-class differences in rarity or ambiguity.

## Theorem TP1 — binary versus ternary information capacity at fixed target prevalence

Let the target Y be binary with

\[
\Pr(Y=0)=\alpha,\qquad
\Pr(Y=1)=1-\alpha,
\quad 0<\alpha<1.
\]

Set

\[
a=\max\{\alpha,1-\alpha\},
\quad
1-a=\min\{\alpha,1-\alpha\}.
\]

Assume a finite, nonincreasing, bounded-below completion-value function U(c), with finite

\[
U_\infty=\lim_{c\to\infty}U(c).
\]

Consider all nontrivial finite deterministic unit-cost exact-target-resolution tasks, all guaranteed-resolving contingent policies, all strictly positive world-frequency distributions satisfying the target prevalence, and a universal precommitted fixed resolver as comparator.

For cue arity bounded by b, define expected performance advantage

\[
R_{\rm expected}
=
\sum_xp_x U(T_\pi(x))-U(C_F).
\]

Then for binary cues (b=2),

\[
\boxed{
\sup R_{\rm expected}^{(2)}
=
aU(1)+(1-a)U(2)-U_\infty.
}
\]

For any b >= 3,

\[
\boxed{
\sup R_{\rm expected}^{(b)}
=
U(1)-U_\infty.
}
\]

These are suprema over scalable finite tasks, not assertions that one finite task attains the bound.

### Binary upper bound

If C_F=1, every correct policy requires at least one query and has no positive completion-value advantage.

If C_F>=2, the first binary query must leave at least one target-mixed outcome; otherwise it would itself be a fixed resolver.

Consequently at most one of the two root outcomes is target-pure and resolves in a single query.

That pure outcome can contain only one target class, so its total encounter probability p_1 is bounded by the more prevalent target:

\[
p_1\le a.
\]

Every remaining world requires at least two queries, so

\[
E[U(T_\pi)]
\le p_1U(1)+(1-p_1)U(2)
\le aU(1)+(1-a)U(2).
\]

The fixed completion value satisfies U(C_F)>=U_infinity. Subtracting it proves the bound.

### Binary sharpness

Use a binary root with a pure leaf of the more prevalent target and a mixed second branch.

The second query creates a pure leaf of the less prevalent target and a rare mixed branch. Put an increasingly large private-pair subtree inside that rare branch.

Give the depth-one leaf probability approaching a, the depth-two leaf probability approaching 1-a, and distribute an arbitrarily small positive remainder across both target classes in the rare subtree, preserving target prevalence *exactly*.

As the rare subtree grows, C_F tends to infinity; as rare mass tends to zero, expected adaptive value tends to

\[
aU(1)+(1-a)U(2).
\]

This attains the upper bound in the supremal sense.

### Ternary upper bound and sharpness

Every nontrivial policy requires at least one query in every state, so expected value cannot exceed U(1). Subtracting U(C_F)>=U_infinity gives the universal bound.

For ternary queries, use one root with three outcomes:

1. a target-0-pure leaf;
2. a target-1-pure leaf;
3. a rare mixed branch containing a large binary private-pair subtree.

Allocate nearly all of the prescribed prevalence of each target class to its corresponding one-step leaf. Allocate a small positive mass from *both* classes to the rare branch.

Both common target classes then terminate after one query, but the rare branch forces the universal fixed resolver to acquire an unbounded number of branch-specific queries.

Hence the ternary construction approaches U(1)-U_infinity and is admissible at any arity bound b>=3.

## Corollary TP1.1 — exact expected-evolvability arity threshold at fixed binary-target prevalence

Let K>=0 be the additive constitutive control cost, and define

\[
K_2
=
aU(1)+(1-a)U(2)-U_\infty,
\]

\[
K_3=U(1)-U_\infty.
\]

When K_2<K_3, the minimum cue arity for positive expected net value in *some* finite task with the prescribed target-class prevalence is

\[
\boxed{
b_{\min}^{\rm expected}
=
\begin{cases}
2,& K<K_2,\\
3,& K_2\le K<K_3,\\
\infty,&K\ge K_3.
\end{cases}
}
\]

Thus the arity-independence in RF7 is a consequence of permitting arbitrary target prevalence as well as arbitrary within-class frequencies. Fixing both target classes to occur with positive prevalence can reinstate an exact global cue-arity no-go in expectation.

The theorem does not require a uniform distribution over individual worlds.

## Corollary TP1.2 — exact 50/50 target balance

Set alpha=1/2 and U(c)=v exp(-mu c).

Then

\[
\boxed{
K_2
=
\frac{v}{2}
\left(e^{-\mu}+e^{-2\mu}\right)
}
\]

and

\[
\boxed{
K_3=ve^{-\mu}.
}
\]

The gap is

\[
\boxed{
K_3-K_2
=
\frac{v}{2}
\left(e^{-\mu}-e^{-2\mu}\right)>0.
}
\]

At mu=0.3, v=1,

\[
K_2\approx0.644815,
\qquad
K_3\approx0.740818.
\]

Thus K=0.68 lies in a regime where no finite binary-cue task can have positive expected net value with balanced target prevalence, while a finite ternary-cue task can.

A concrete ternary root plus rare binary depth-four subtree suffices; take 49.5% encounters in each of two pure one-step target leaves and 1% distributed positively across both targets in the rare branch.

Its fixed mandatory-query burden is 16 and its expected exponential completion-value advantage exceeds 0.68.

## Why this matters biologically

The result identifies a specific compensation mechanism:

- under unconstrained target prevalence, a binary query can concentrate almost all encounters in one easy pure branch, making higher cue arity unnecessary for the expected-value supremum;
- when two target classes both remain common, a binary query cannot identify both classes *and* leave an ambiguity branch at the first observation;
- a ternary cue can simultaneously dedicate one root outcome to each common target class and reserve a third for rare ambiguous states.

So cue arity and ecological prevalence interact; neither alone determines expected sensing value.

The mathematical result is about declared query outcome counts, not receptor numbers, neurological complexity, or experimentally measured sensory fidelity.

## Relation to RF7 and RF7.4

RF7: free world frequencies -> arity-independent expected supremum.

RF7.4: a lower bound on every world probability yields a general, usually nonsharp expected-value upper bound.

TP1: fixed prevalence of the *two target categories* yields sharp, constructive and qualitatively different binary-versus-ternary expected-value ceilings, even while allowing highly skewed within-class world frequencies.

The results have different probability constraints and are not contradictory.

## Scope and novelty boundary

The ingredients (decision-tree arity, pure outcomes, class prevalence, adaptive value) have substantial precedents in classification and decision theory.

The candidate programme-specific contribution is the exact composition of private-pair fixed-query necessity, ecological completion value and constrained target prevalence, yielding sharp evolutionary control-cost ceilings.

This is not an empirical prediction until the target categories, cue outcomes, opportunity-value function, competitor architecture and control costs are measured.

Do not headline a generic claim that three-outcome sensors are biologically superior to binary sensors.
