# Target-prevalence constraints restore cue-arity dependence in expected value

Status: supporting theory / empirical realism gate, not a fourth flagship theorem. Requires deterministic exact target resolution, unit query costs, a single universal fixed-bundle comparator, two target labels, and freely chosen strictly positive world frequencies conditional on a declared target prevalence.

## 1. Why RF7's arity independence needs a prior qualification

RF7 shows that without constraints on encounter frequencies the finite-scope expected-value supremum is independent of cue arity. It concentrates almost all encounters on one easy world and hides all fixed-bundle obligations in very rare worlds.

Ecological encounters need not allow arbitrary concentration. A modest restriction is to hold the frequency of the *required target decisions* fixed, while allowing within-target world frequencies to vary.

Let target labels be 0 and 1, with

\[
\Pr(\mathrm{target}=0)=p,\qquad
\Pr(\mathrm{target}=1)=1-p,\quad 0<p<1.
\]

Let \(U(c)\) be finite, nonincreasing and bounded below, with \(U_\infty=\lim_{c\to\infty}U(c)\). Let \(R_{\rm expected}(\pi)=\sum_xp_xU(T_\pi(x))-U(C_F)\).

## 2. Theorem TP1 — binary versus ternary global capacities at fixed target prevalence

For arbitrary finite nontrivial tasks with strict positive frequencies and unbounded finite n/m budgets:

**Binary outcomes (b=2):**

\[
\boxed{
\sup R_{\rm expected}^{(b=2)}
=
qU(1)+(1-q)U(2)-U_\infty,\quad q=\max(p,1-p).
}
\]

**At least three outcomes (b>=3):**

\[
\boxed{
\sup R_{\rm expected}^{(b\ge3)}
=
U(1)-U_\infty.
}
\]

### Binary upper bound

If \(C_F=1\), fixed resolution is complete after one query and there is no positive advantage over the optimal fixed benchmark.

If \(C_F\ge2\), then a binary first query cannot make *both* outcomes target-pure: otherwise that single query would be a fixed resolver. Consequently at most one first-query outcome may terminate immediately, and every world in that pure outcome has the same target.

Its encounter mass is therefore at most \(q\). Writing \(p_1=\Pr[T_\pi=1]\le q\), every other path takes at least two queries. Hence

\[
E[U(T_\pi)]
\le p_1U(1)+(1-p_1)U(2)
\le qU(1)+(1-q)U(2).
\]

Subtracting \(U(C_F)\ge U_\infty\) proves the binary upper bound.

### Binary matching construction

Take a binary root with a target-pure depth-one leaf of the more frequent target. Its other branch has a depth-two pure leaf of the opposite target, plus a rare subtree containing both targets and an arbitrarily large private-pair fixed burden.

Let the total rare probability tend to zero, partitioned between its two targets so that target prevalence remains exactly \(p,1-p\). The depth-one and depth-two leaves then asymptotically carry probabilities \(q,1-q\); \(C_F\to\infty\). Every represented world retains positive probability for each finite task. This attains the stated supremum in the limit.

### Ternary upper bound and matching construction

All nontrivial policies have \(T_\pi(x)\ge1\), so \(R_{\rm expected}\le U(1)-U_\infty\).

A three-outcome root can send target 0 to a pure depth-one leaf, target 1 to a second pure depth-one leaf, and a rare mixed subset of both targets to a third outcome. Below the mixed branch place an arbitrarily large binary private-pair tree.

Let the rare mixed mass tend to zero while preserving target prevalence \(p,1-p\). Then expected adaptive value tends to \(U(1)\) while \(C_F\to\infty\). This construction uses at most three outcomes per query, so it is admissible for every b>=3.

## 3. Balanced target frequencies give a strict capacity separation

For \(p=1/2\),

\[
\boxed{
\sup R_{\rm expected}^{(2)}
=
\frac{U(1)+U(2)}2-U_\infty,
}
\]

whereas

\[
\boxed{
\sup R_{\rm expected}^{(\ge3)}
=
U(1)-U_\infty.
}
\]

The extra expected-value capacity available to ternary sensing is exactly

\[
\boxed{
\frac{U(1)-U(2)}2.
}
\]

With exponential opportunity value \(U(c)=ve^{-\mu c}\), it equals \(v(e^{-\mu}-e^{-2\mu})/2\).

For \(\mu=0.3,v=1\), global ceilings are approximately 0.644815 (binary) and 0.740818 (ternary). Thus an additive control cost \(K=0.68\) is globally impossible to repay with binary cues under balanced target prevalence but repayable with a ternary cue under a sufficiently large finite task and sufficiently rare difficult worlds.

This is a **prevalence-constrained expected** no-go. It does not contradict RF7, which optimizes over target prevalence too.

## 4. Same finite world and query budgets: one fully explicit counterexample

Fix **exactly ten worlds**, **at most nine available queries**, target prevalence exactly 50:50, \(U(c)=e^{-0.3c}\), and maintenance cost \(K=0.62\).

For any binary task in the scope, \(C_F\le M=\min(10-1,9)=9\), and the binary target-balance argument gives

\[
R_{\rm expected}^{(2)}
\le
\tfrac12[e^{-0.3}+e^{-0.6}]-e^{-2.7}
\approx0.577610<K.
\]

So **no binary task** in this finite scope can repay \(K\) in expectation while respecting target prevalence.

Construct a ternary-root task with:
- one target-0 pure leaf at depth 1;
- one target-1 pure leaf at depth 1;
- one rare mixed third branch comprising a full depth-3 binary private-pair subtree (eight rare worlds).

The task has exactly ten worlds, eight productive unit-cost queries (below the budget of nine), and at most three outcomes per query. Every productive query has a unique opposite-target private pair, so \(C_F=8\). Both common target leaves finish after one query; all rare worlds finish by depth 4.

Give each common target leaf probability 0.49 and distribute a total probability of 0.01 across the rare target-0 worlds and 0.01 across the rare target-1 worlds (each world strictly positive). This preserves target prevalence exactly 50:50.

The declared tree has expected advantage

\[
R_{\rm expected}^{(3)}
=
0.98e^{-0.3}+0.02e^{-1.2}-e^{-2.4}
\approx0.6413>K=0.62.
\]

Thus in the same finite \(n=10,m=9\) structural scope, **binary is impossible but ternary is constructively possible** once target prevalence is fixed to 50:50.

This does not mean biological ternary sensory channels have the same constitutive cost as binary ones. K and query unit cost are declared comparison assumptions.

## 5. Biological reading

What matters is not only whether cue outcomes branch, but whether one early observation can dispose of *both target classes* while preserving a rare branch for difficult cases.

- With two outcomes, keeping a mixed difficult branch means one target class must usually wait for a second query.
- With three outcomes, both common target classes can be resolved in one step while difficult states retain their own branch.

Target prevalence therefore interacts with cue arity to determine what fraction of ecologically valuable encounters can terminate early.

This is a model-specific constructive limit, not a new general theory of categorical sensing or a claim about receptor number. It offers a stricter empirical target than the frequency-free RF7 maximum.

## 6. Relation to the manuscript

This result belongs as a caveat or supplementary extension to RF7. The manuscript should retain the defensible wording:

> Expected-value ceilings are arity-independent **when encounter frequencies are unrestricted**; ecologically motivated restrictions on target prevalence can restore arity dependence.

A natural empirical test would jointly measure target-category frequencies and branch-specific completion curves, rather than calling cue arity biologically irrelevant based on the unrestricted envelope.
