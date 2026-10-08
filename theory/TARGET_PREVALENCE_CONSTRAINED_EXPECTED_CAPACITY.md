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

## 4b. Theorem TP2 — exact finite expected-value frontier at fixed target prevalence

The preceding example can be strengthened to a sharp result for **every**
finite world/query budget. Fix \(n\ge2\) worlds, at most \(m\ge1\) unit-cost
queries, binary target labels with probabilities \(p,1-p\) where \(0<p<1\),
and a finite nonincreasing completion value \(U\). World frequencies may vary
subject to those target probabilities, but must remain strictly positive.

Write

\[
q=\max(p,1-p),\qquad M=\min\{m,n-1\}.
\]

If \(M=1\), adaptivity offers no advantage over a fixed resolver: the supremum
is zero for every cue arity.

For \(M\ge2\), the **binary** expected-value supremum is exactly

\[
\boxed{
E_2(n,m;p,U)
=
qU(1)+(1-q)U(2)-U(M).
}
\]

For arity \(b\ge3\), define

\[
M_3=\min\{m,n-2\}.
\]

When \(n\ge4\), the exact expected-value supremum is

\[
\boxed{
E_{\ge3}(n,m;p,U)
=
\max\left\{
E_2(n,m;p,U),
\;
U(1)-U(M_3)
\right\}.
}
\]

For \(n\le3\), the second candidate is structurally unavailable and the
binary expression remains sharp for \(b\ge3\).

### Proof of upper bounds

If a task admits a single-query fixed resolver (\(C_F=1\)), there is no
positive adaptive advantage.

Otherwise consider the first query of any guaranteed-resolving policy. If
at most one target class has a pure root outcome, the probability of
completing after one query is at most \(q\). Every remaining world needs at
least two queries. Since \(C_F\le M\),

\[
R_{\rm expected}
\le
qU(1)+(1-q)U(2)-U(M).
\]

This covers every binary query and also multivalued queries lacking
target-pure root outcomes for **both** target classes.

If the root has pure outcomes for both target classes and \(C_F\ge2\), the
root must have at least one additional mixed outcome. It therefore has at
least three nonempty children. A productive decision tree with \(n\) leaves
and a root of degree at least three has at most \(n-2\) internal nodes.
Flattening its distinct queries gives a fixed resolver, so

\[
C_F\le\min\{m,n-2\}=M_3.
\]

All realized paths still require at least one query. Hence

\[
R_{\rm expected}
\le U(1)-U(M_3).
\]

Together the two cases prove the finite upper envelope.

### Constructive attainment of both branches

For \(E_2\), build a binary tree with exactly \(M\) productive internal
queries: a target-pure depth-one leaf of the more frequent target, a
target-pure depth-two leaf of the opposite target, and a chain of rare mixed
states that makes all \(M\) queries independently fixed-mandatory. Pad unused
world/query budget with duplicate worlds and constant queries. Send the rare
probability to zero while preserving the exact target prevalence. The
expected value tends to \(qU(1)+(1-q)U(2)\), with \(C_F=M\).

For the second term, use a three-outcome root: pure depth-one leaves for
target 0 and target 1, plus a rare mixed branch with a binary chain of
\(M_3-1\) productive internal nodes. The entire tree has \(M_3\)
fixed-mandatory queries and at most \(M_3+2\le n\) leaves. The two pure
leaves receive probabilities approaching \(p\) and \(1-p\). Thus expected
adaptive value approaches \(U(1)\) while \(C_F=M_3\).

All frequency distributions in the approximating sequences assign
strictly positive probability to every represented world.

### Exact finite numerical example

For \(n=10,m=9,p=1/2,U(c)=e^{-0.3c}\),

\[
M=9,\qquad M_3=8.
\]

The exact binary supremum is

\[
\boxed{
E_2
=
\frac{e^{-0.3}+e^{-0.6}}2-e^{-2.7}
\approx0.5776094.
}
\]

The exact ternary-or-higher supremum is

\[
\boxed{
E_{\ge3}
=
\max\{0.5776094,\;e^{-0.3}-e^{-2.4}\}
\approx0.6501003.
}
\]

Thus any architecture cost satisfying

\[
0.5776094\le K<0.6501003
\]

is **impossible** to repay in expectation using binary cues under the
declared target-balance and resource constraints, but **possible** with
ternary cues under some strictly positive balanced target-frequency
distribution. The \(K=0.62\) construction in Section 4 is one explicit
finite witness.

This result does not contradict RF7's arity-independent ceiling. RF7
optimizes over target prevalence and individual-world frequency, whereas
TP2 holds the target prevalence fixed. TP2 remains a supporting model-
specific theorem until its relation to constrained-prior decision-tree
literature has been audited.


## Corollary TP2.1 — exact ecological-prevalence window for a ternary-only advantage

TP2 can be inverted without increasing the number of main theorems.

For fixed \(n,m\), let

\[
M=\min(m,n-1),\qquad M_3=\min(m,n-2),
\]

and write \(q=\max(p,1-p)\) for the more prevalent target class.

The sharp binary expected-value ceiling is

\[
E_2(q)
=
U(2)-U(M)
+
q[U(1)-U(2)].
\]

The ternary architecture can use two target-pure root outcomes plus one rare
mixed continuation, giving a prevalence-independent candidate ceiling

\[
E_{\rm pure,3}=U(1)-U(M_3)
\]

when \(n\ge4\), \(m\ge2\) and both target classes remain represented.

For a declared architecture cost \(K\), a **ternary-only expected repayment
regime** exists exactly when

\[
E_2(1/2)\le K<E_{\rm pure,3}
\]

and \(U(1)>U(2)\). In that case define

\[
\boxed{
q_{\rm crit}
=
\frac{K-U(2)+U(M)}{U(1)-U(2)}.
}
\]

Then

\[
\boxed{
1-q_{\rm crit}
\le p\le
q_{\rm crit}
}
\]

is exactly the interval of target prevalences where binary queries cannot pay
\(K\) in expectation, but ternary queries can. The endpoints belong to the
interval because a binary ceiling equal to \(K\) gives neutral, not positive,
net value.

Outside this interval, some binary finite task can pay \(K\) in expectation
under the declared constraints.

### Numerical example

Fix \(n=10,m=9,U(c)=e^{-0.3c}\) and \(K=0.62\).

Then

\[
M=9,\quad M_3=8,\quad
q_{\rm crit}\approx0.7207767.
\]

The exact ternary-only interval is therefore

\[
\boxed{
0.2792233\le p\le0.7207767.
}
\]

At 50:50 target prevalence, binary expected-value capacity is approximately
0.57761, which is below \(K\), whereas ternary capacity is approximately
0.65010, which exceeds \(K\).

At 80:20 target prevalence, binary capacity increases to approximately
0.63521 and also exceeds \(K\). No change in \(n,m,U,K\) is required.

### Biological interpretation and claim ceiling

Target prevalence can substitute for cue-outcome capacity *in expectation*.
If one target category becomes sufficiently dominant, a binary first query
that recognizes that frequent target can be nearly as useful as a ternary
query that creates two pure target branches and a rare ambiguity branch.

This is a supremal task-design existence result, not a prediction that an
individual organism will evolve ternary versus binary sensory machinery.
The calculation optimizes within-target world frequencies, assumes equal
per-query acquisition costs regardless of arity, and compares against one
universal fixed bundle. It is not validated by cross-species differences in
mosquito probing. The two target categories, their encounter proportions,
actual cue outcomes, and arity-dependent acquisition/maintenance costs must
be measured before using the interval as a population prediction.

Implementation:
\`finite_ternary_only_prevalence_interval(...)\` in
\`adaptive_gain/target_prevalence_capacity.py\`, with regression tests.


## Corollary TP2.2 — extra cost can erase the class-level ternary capacity premium

The previous result asks which cue-arity class can repay a common control cost
relative to a universal fixed benchmark. Evolutionary competition among
different arities additionally requires accounting for any **extra
architecture cost** of the ternary channel.

This can be bounded without treating a class envelope as an observed
pairwise selection coefficient.

Let

\[
B_2(q)
=
U(2)-U(M)+q[U(1)-U(2)]
\]

be the sharp binary expected-value capacity at majority target prevalence
\(q=\max(p,1-p)\). Let

\[
T_3=U(1)-U(M_3)
\]

be the two-target-pure-root ternary capacity candidate.

At the level of the **best attainable task in each class**, the extra
performance capacity from permitting ternary queries is

\[
\boxed{
\Delta R_{\rm capacity}(q)
=
\max\{0,T_3-B_2(q)\}.
}
\]

If the ternary design incurs an additional constitutive cost
\(\Delta K\ge0\), the extra class-level capacity can pay that cost exactly
when

\[
\Delta R_{\rm capacity}(q)>\Delta K.
\]

When \(U(1)>U(2)\) and the maximum capacity premium at balanced prevalence
exceeds \(\Delta K\), this is equivalent to

\[
\boxed{
\max(p,1-p)
<
\frac{T_3-\Delta K-U(2)+U(M)}
{U(1)-U(2)}.
}
\]

Unlike TP2.1, the endpoints are **excluded**, because equality means no
strict positive increment after the additional cost.

### Canonical sensitivity

For \(n=10,m=9,U(c)=e^{-0.3c}\), the maximum attainable ternary capacity
premium at 50:50 target prevalence is only

\[
\boxed{
T_3-B_2(1/2)\approx0.0724909.
}
\]

If ternary control costs 0.05 extra per the same additive payoff scale, the
remaining positive premium exists only when target prevalence lies within

\[
\boxed{
0.382864<p<0.617136.
}
\]

If its extra cost reaches 0.0724909, there is no strict class-level advantage
at any target prevalence.

### Essential comparator restriction

\(\Delta R_{\rm capacity}\) subtracts **two suprema over different admissible
task designs**. It does not compare two realized genotypes, two sensing
policies, or two cue-processing systems embedded in the **same fixed
environment**.

Thus it cannot be interpreted as a selection coefficient favoring a ternary
sensory organ. A within-environment evolutionary comparison still requires
matched ecological states, actual cue outcomes, per-query acquisition costs,
architecture maintenance costs, and the same encounter distribution.

The calculation's role is to show that a theoretical arity advantage can be
biologically fragile: only a modest extra architecture cost may eliminate the
capacity premium in the stylized example.

Implementation:
\`finite_ternary_capacity_premium_prevalence_interval(...)\` in
\`adaptive_gain/target_prevalence_capacity.py\`.


## 5. Biological reading

What matters is not only whether cue outcomes branch, but whether one early observation can dispose of *both target classes* while preserving a rare branch for difficult cases.

- With two outcomes, keeping a mixed difficult branch means one target class must usually wait for a second query.
- With three outcomes, both common target classes can be resolved in one step while difficult states retain their own branch.

Target prevalence therefore interacts with cue arity to determine what fraction of ecologically valuable encounters can terminate early.

This is a model-specific constructive limit, not a new general theory of categorical sensing or a claim about receptor number. It offers a stricter empirical target than the frequency-free RF7 maximum.

## 5b. Acquisition-cost sensitivity of the finite ternary witness

The sharp TP2 bounds assume one unit per query regardless of outcome
cardinality. That is a model assumption, not a biological law.

For the explicit ten-world ternary construction in Section 4, let the root
three-outcome query take acquisition time \(a\) instead of 1, while each later
binary query retains cost 1. Keep \(\mu=0.3\), target prevalence 50:50, the
same path probabilities, and constitutive control cost \(K=0.62\).

Its declared expected benefit becomes

\[
R(a)
=
0.98e^{-0.3a}
+
0.02e^{-0.3(a+3)}
-
e^{-0.3(a+7)}
=
0.641307787\,e^{-0.3(a-1)}.
\]

Consequently that **specific witness** can repay \(K\) only if

\[
\boxed{
a<
1+\frac{\log(0.641307787/0.62)}{0.3}
\approx1.11263.
}
\]

For example, at \(a=1.10\), benefit is approximately 0.62235, but at
\(a=1.15\) it is only 0.61309.

This does **not** prove that all ternary architectures fail beyond this
threshold. It demonstrates that the finite existence example has little
margin for an additional arity-dependent acquisition delay.

The constitutive maintenance cost \(K\) and the per-encounter query time \(a\)
are distinct biological cost channels. Both must be measured before claiming
that real higher-arity sensory systems are favored.

## 5c. Prior-art boundary

Prior probabilities, expected-vs-worst diagnostic-tree objectives and
multiway/value-dependent testing are established theory, including:

- Cicalese, Laber & Saettler (2014), *Diagnosis determination: decision trees
  optimizing simultaneously worst and expected testing cost*, ICML/PMLR 32;
- Saettler, Laber & Cicalese (2015), *Approximating decision trees with value
  dependent testing costs*, *Information Processing Letters* 115:594–599,
  DOI 10.1016/j.ipl.2015.02.006.

TP2 does not claim that target prevalence affects optimal testing or that
ternary outcomes are generally superior. Its model-specific candidate
contribution is the **sharp finite envelope under simultaneous world-count,
query-count, arity and fixed binary-target-prevalence constraints**.

The novelty/priority of that precise envelope still requires a broader
literature audit; it remains supplementary rather than a fourth V6 main
result.


## 6. Relation to the manuscript

This result belongs as a caveat or supplementary extension to RF7. The manuscript should retain the defensible wording:

> Expected-value ceilings are arity-independent **when encounter frequencies are unrestricted**; ecologically motivated restrictions on target prevalence can restore arity dependence.

A natural empirical test would jointly measure target-category frequencies and branch-specific completion curves, rather than calling cue arity biologically irrelevant based on the unrestricted envelope.
