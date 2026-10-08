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


## Theorem TP2 — a minimal finite four-world counterexample

The class-balance constraint already restores an arity gap at the smallest
nontrivial finite corner with a mixed continuation.

Fix:

\[
n=4,\qquad m=2,
\]

two target classes each having exactly one-half of encounter probability, and
finite nonincreasing U.

Then, over deterministic unit-cost tasks and strictly positive world
probabilities respecting this target balance,

\[
\boxed{
\sup R_{\rm expected}^{(b=2)}
=
\frac12[U(1)-U(2)],
}
\]

whereas

\[
\boxed{
\sup R_{\rm expected}^{(b\ge3)}
=
U(1)-U(2).
}
\]

### Proof for binary cues

A strict gain requires fixed cost \(C_F=2\). The first binary query must then
leave a target-mixed outcome; otherwise one query would already resolve the
target universally.

At most one root outcome is target-pure, and target balance limits its encounter
mass to one-half.

With only two available queries, all remaining states resolve no sooner than
after the second query. Thus

\[
\mathbb E[U(T)]-U(C_F)
\le
\frac12U(1)+\frac12U(2)-U(2).
\]

A binary root-pure leaf plus a mixed second branch attains this in the limit as
the rare opposite-target world inside the mixed branch gets arbitrarily small
positive mass. Four-world padding can preserve the exact 50/50 target
prevalence.

### Proof for ternary cues

A ternary root has:

- one target-0-pure outcome;
- one target-1-pure outcome;
- one mixed outcome resolved by the second binary query.

The two queries are fixed-mandatory by separate opposite-target private pairs.
Both target classes can have almost all of their probability on their respective
one-step pure outcomes while a positive rare mass is reserved for the mixed
branch.

Thus expected completion value approaches \(U(1)\), and the fixed comparator
cost is two. The upper bound \(U(1)-U(2)\) is therefore sharp as a supremum.

### Finite numerical witness without extreme rare-state concentration

Take

\[
U(c)=e^{-0.3c}.
\]

The sharp binary ceiling is

\[
\frac12(e^{-0.3}-e^{-0.6})
\approx0.0960033.
\]

Use the four-world ternary witness with probabilities

\[
(0.45,\ 0.45,\ 0.05,\ 0.05)
\]

on the two pure one-step worlds and the two rare mixed worlds, respectively.

Both target classes have total probability exactly 0.50.

The explicit routing tree has expected completion-value advantage

\[
0.9 e^{-0.3}+0.1 e^{-0.6}-e^{-0.6}
=
0.9(e^{-0.3}-e^{-0.6})
\approx0.172806.
\]

Hence a constitutive architecture cost

\[
\boxed{K=0.14}
\]

is impossible to repay by any binary two-query task with this target balance,
but is repaid by the explicit ternary two-query task.

This is an exact finite construction, not a biological experiment.


## Independent finite enumeration of TP2

To avoid relying on the private-pair witness factory or the general exact
solver, we independently enumerated every binary target labeling on four
worlds and every unordered pair of two deterministic unit-cost queries.

We retained only configurations in which neither query resolves the target
alone but the pair does, so the minimum universal fixed bundle contains both.

| Query arity | Fixed-cost-two configurations | One-step pure outcomes from both target classes | Supremal one-step encounter mass at 50/50 target prevalence |
| --- | ---: | ---: | ---: |
| Binary | 264 | 0 | 0.5 |
| Ternary | 9,720 | 3,888 | 1.0 |

The enumeration covers target labelings with one or more worlds in each
class; strictly positive individual world probabilities can realize exactly
50/50 aggregate target prevalence. The one-step mass values are suprema
because within-class world probabilities may become arbitrarily small.

A separate three-world check finds no fixed-cost-two ternary pair whose
root offers both target-pure classes and still retains a mixed branch.
This verifies that four represented worlds are the first finite corner at
which the ternary separation can occur.

The independent regression is
`tests/test_target_prevalence_independent_exhaustive.py`.

The result does not turn TP2 into an independent main theorem: it audits the
exact finite mechanism behind the target-prevalence caveat to RF7.

### Predicted prevalence boundary (supporting inversion)

For any cost (K) between the binary balanced-target and the ternary
ceilings, the binary threshold depends on
(a=\max\{\alpha,1-\alpha\}\):

\[
a>a_{\rm crit}
=
\frac{K+U_\infty-U(2)}{U(1)-U(2)}.
\]

At (U(c)=e^{-0.3c}\) and (K=0.68\),
(a_{\rm crit}\approx0.6833\). Binary cues can repay the cost in some
scalable task if the target prevalence is sufficiently skewed past this
boundary; otherwise at least ternary query outcomes are needed.
This is a task-class existence condition, not a predicted evolutionary
response for a measured natural population.


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
