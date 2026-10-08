# Exact uniform-encounter envelope for binary information architectures

Status: side theory supporting RF7 and its ecological interpretation. The
principal prior unrestricted-frequency result is not changed.

## 1. Why this question

RF7 proves an exact expected-value supremum

\[
U(1)-U(\min\{m,n-1\})
\]

when an investigator may choose arbitrarily skewed encounter frequencies.

Its sharp witness concentrates encounters on one target-pure one-query branch.
That does not predict selection when each represented ecological world is
encountered at the same frequency.

RF7.4 introduced a frequency-floor upper bound but did not prove its
attainability. This note closes the equal-world-frequency case exactly for
binary cues under the declared resource condition \(m\ge n-1\).

## 2. Model and envelope

Fix \(n\ge2\) equiprobable represented worlds, at least \(n-1\) declared
unit-cost binary queries, and a finite nonincreasing completion-value function
\(U(c)\).

The target must be resolved exactly. The fixed comparator pays the cost of one
universal precommitted resolving bundle.

For a finite full binary decision tree \(T\), let:

- \(j(T)\) be its number of internal-node occurrences;
- \(L(T)\) be its terminal leaves, so \(|L(T)|=j(T)+1\);
- \(d_\ell\) be the depth of leaf \(\ell\);
- \(d_{\min}(T)=\min_\ell d_\ell\).

Write the following score:

\[
\boxed{
A_n(T;U)
=
\frac{
\sum_{\ell\in L(T)}U(d_\ell)
+
[n-|L(T)|]\,U(d_{\min}(T))
}{n}
-
U(j(T)).
}
\]

The second term inside the numerator allocates the surplus represented worlds
to a shallowest target-pure terminal leaf. These worlds can be exact
cue/target-equivalent copies; the resulting encounter distribution remains
uniform over the *represented worlds*, not necessarily over the *terminal
decision classes*.

## Theorem UE1 — exact uniform-encounter expected envelope

Let \(\mathcal B_{\le n}\) denote all full binary trees with between two and
\(n\) terminal leaves. Then

\[
\boxed{
\sup_{\substack{|W|=n,\ |Q|\ge n-1,\ b=2\\
p_x=1/n}}
\left[
\max_\pi\sum_xp_xU(T_\pi(x))-U(C_F)
\right]
=
\max_{T\in\mathcal B_{\le n}}A_n(T;U).
}
\]

The right-hand side is a maximum over a finite collection of depth profiles,
and is constructively attained by the private-pair finite task associated with
a maximizing binary tree.

### Upper bound

Take any finite task and any guaranteed-resolving productive adaptive policy
\(\pi\). Its binary decision tree has \(n_\ell\le n\) target-pure terminal cells
and \(j=n_\ell-1\) internal nodes.

Flattening its queries gives a fixed resolver of cost at most \(j\), so

\[
C_F\le j.
\]

Monotonicity of \(U\) implies

\[
-U(C_F)\le-U(j).
\]

Let \(k_\ell\ge1\) count represented worlds in terminal cell \(\ell\), with
\(\sum_\ell k_\ell=n\). Uniform encounter frequencies give

\[
E[U(T_\pi)]
=
\frac1n\sum_\ell k_\ell U(d_\ell).
\]

At fixed tree shape the maximum over such integer multiplicities places all
\(n-n_\ell\) surplus worlds at a shallowest leaf:

\[
\sum_\ell k_\ell U(d_\ell)
\le
\sum_\ell U(d_\ell)
+
(n-n_\ell)U(d_{\min}).
\]

Therefore

\[
R_{\rm expected}(\pi)\le A_n(T;U).
\]

Taking the maximum over trees proves the upper bound.

### Attainment

For every full binary tree \(T\) with \(j\le n-1\) internal nodes, create one
physical query per internal node and apply the repository's private
opposite-target-pair construction.

Each internal query is fixed-mandatory, hence

\[
C_F=j.
\]

Place one world at each leaf and duplicate the shallowest leaf until exactly
\(n\) represented worlds exist. The adaptive policy follows \(T\), so every
world has the declared completion depth.

Because \(m\ge n-1\ge j\), this construction stays within the declared query
budget; any unused query slots are padded by constant queries.

It attains \(A_n(T;U)\), and hence the displayed upper bound. QED.

## 3. Exact canonical comparison

Take

\[
n=10,\quad m=9,\quad b=2,\qquad U(c)=e^{-0.3c}.
\]

Enumerating all distinct full-binary leaf-depth multisets (115 profiles across
two to ten leaves) gives

\[
\boxed{R_{\rm uniform,max}=0.3328200168.}
\]

The maximizing architecture has:

\[
\boxed{C_F=6}
\]

and base leaf-depth multiset

\[
\boxed{\{1,3,3,4,4,4,4\}.}
\]

It has seven terminal cells; the three remaining represented worlds are
target/cue-equivalent to the one-query leaf. Thus four of ten equiprobable
worlds reach a correct target decision in one query.

The existing RF7.4 probability-floor bound is only

\[
R_{\rm uniform}\le0.5008067818.
\]

The unrestricted-frequency RF7 supremum is

\[
R_{\rm free\ prior}=U(1)-U(9)=0.6736127079.
\]

The sharp uniform value is only about half of the free-prior supremum.

In particular, the claimed \(K=0.60\) expected rescue **cannot** occur with
uniform world encounter frequencies in this structural scope.

## 4. How natural history re-ranks trees under uniform encounters

Keeping \(n=10,m=9,b=2\), the exact maximizing structures include:

| Exponential closure \(\mu\) | Optimal fixed burden | Base terminal depths | Surplus easy worlds | Sharp uniform value |
| ---: | ---: | --- | ---: | ---: |
| 0.1 | 9 | six 3s, four 4s | 0 | 0.3060493 |
| 0.2 | 9 | six 3s, four 4s | 0 | 0.3437197 |
| 0.3 | 6 | 1,3,3,4,4,4,4 | 3 | 0.3328200 |
| 0.5 | 4 | 1,3,3,3,3 | 5 | 0.3178352 |
| 1.0 | 3 | 1,2,3,3 | 6 | 0.2312195 |

Thus, even under equal frequencies for the represented worlds, the
ecologically best available *task geometry* changes from mostly balanced and
resource-rich to strongly prioritized and resource-light as the value of time
becomes steeper.

This is a comparison across **possible task structures**, not a claim that
one existing organism can evolve between those structures costlessly or that
an already-given task changes its hidden worlds as urgency changes.

## 5. Role of decision-equivalent world multiplicity

The full model permits different represented ecological worlds to have the
same query outcomes and target. These worlds can be encountered equally often,
yet together make their terminal decision class frequent.

To separate this from tree shape, impose the stronger restriction that each
represented world occupies its own terminal leaf:

\[
|L(T)|=n.
\]

The sharp restricted envelope is then

\[
\boxed{
\max_{T:\,|L(T)|=n}
\left[
\frac1n\sum_\ell U(d_\ell)-U(n-1)
\right].
}
\]

At \(\mu=0.3,n=10\), its maximum is

\[
\boxed{0.2972139679,}
\]

with six leaves at depth three and four at depth four.

The difference

\[
0.3328200168-0.2972139679
=
\boxed{0.0356060489}
\]

is the additional maximum value available when decision-equivalent
multiplicity is permitted at equal represented-world frequencies.

The distinction is important biologically: an equal-frequency distribution
over species or named environments is not necessarily an equal-frequency
distribution over *decisions that still need to be distinguished*.

## 5b. Equal target prevalence does not erase the effect

The exact unrestricted uniform-world optimum does not constrain the
prevalence of target labels. To check whether its advantage depends on a
majority target class, construct a different private-pair witness with:

- ten equally probable represented worlds;
- exactly five target-0 and five target-1 worlds;
- seven fixed-mandatory binary query resources;
- one early terminal world of target 0, duplicated twice as
  cue/target-equivalent represented worlds.

Its eight distinct terminal leaf depths are

\[
\{1,3,3,4,4,4,5,5\}.
\]

The private-pair tree has base target counts \(3:5\); two copies of the
one-step target-0 leaf make the represented target counts \(5:5\).

Under \(U(c)=e^{-0.3c}\), the declared tree has expected-value advantage

\[
\boxed{R_{\rm balanced\ target}\ge0.3160872655.}
\]

The inequality is a *constructive lower bound*. A different adaptive policy
for this same task could potentially have higher expected value; the global
sharp optimum subject to balanced target prevalence has **not** been
established.

It nevertheless rules out the explanation that a strongly unequal target
base rate is necessary for a large fraction of the uniform-world advantage.
Decision-equivalent world multiplicity can generate highly uneven decision
completion opportunities even when both the world frequencies and the binary
target prevalences are exactly balanced.


## 6. Relation to RF7 and PAYOFF

RF7's arity-free envelope assumes encounter frequencies may be chosen
arbitrarily. UE1 closes a different, much more restrictive data-generating
regime: exactly uniform encounter probabilities on represented worlds.

PAYOFF receives the model-specific recoverable benefit:

\[
R_{\rm uniform,max},
\]

and can apply the comparison

\[
R-K.
\]

For the canonical example, no binary architecture within the declared scope
can repay additive control cost

\[
K\ge0.3328200168
\]

in expectation under uniform represented-world encounters, whereas the
free-prior envelope would allow costs up to about \(0.673613\).

This is an exact maximum over *admissible task constructions* under the stated
uniform prior. It is not a fitness estimate for any observed population.

## 7. Prior-art and claim boundary

Expected decision-tree cost, prefix-code length distributions, and
utility-sensitive binary tree optimization are established subjects.

Do not claim novelty for enumeration of binary tree shapes or for the fact
that decision-tree topology changes with a time-value function.

The repository-specific purpose is to compose:

1. the exact fixed mandatory-query/private-pair construction;
2. an explicitly constrained ecological encounter distribution;
3. an attained expected-value envelope, rather than an arbitrary-prior
   envelope or a nonsharp probability-floor upper bound.

The result demonstrates why claims about natural selection require empirical
state-frequency semantics, not just theoretical cue counts or maximal
structural adaptive ratios.
