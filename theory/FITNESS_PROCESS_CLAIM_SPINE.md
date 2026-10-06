# Fitness-process claim spine for adaptive-gain

Status: synthesis note for PR #67. This is a proposed biological spine, not a frozen manuscript replacement.


## Principal theorem — sharp evolutionary frontier

Fix finite deterministic unit-cost tasks with \(n\) represented worlds, \(m\)
declared query resources, and maximum query arity \(b\).

For each feasible adaptive depth \(h\), define

\[
I_h=\min\{m,F_b(n,h)\}.
\]

The bounded-arity construction now attains the exact pair

\[
\boxed{(C_A,C_F)=(h,I_h)}
\]

for every feasible \(h\).

Therefore for any finite nonincreasing biological completion value \(U(c)\),

\[
\boxed{
\max
\left[
U(C_A)-U(C_F)
\right]
=
\max_h
\left[
U(h)-U(I_h)
\right].
}
\]

This is the current principal cross-layer theorem.

It says that natural history does not merely scale one structural
adaptive-gain score. It **re-ranks an exact finite structural frontier**.

For opportunity survival \(S(c)\) and timely-resolution value \(v\),

\[
R_{\max}
=
v\max_h[S(h)-S(I_h)].
\]

With baseline fitness \(w_0\), define

\[
\kappa_{\rm crit}^{\rm robust}
=
\max_h
\log
\frac{w_0+vS(h)}
{w_0+vS(I_h)}.
\]

Then, relative to the declared universal fixed comparator,

\[
\boxed{
\text{positive net advantage can be guaranteed in every represented world}
\iff
\kappa<\kappa_{\rm crit}^{\rm robust}.
}
\]

So the finite information constraints impose an exact ceiling on the
constitutive control cost that can be supported **without knowing encounter
frequencies**.

This is a robust statewise threshold, not a no-go for positive expected
selection.  Expected fitness can exceed the robust margin when common branches
terminate earlier than the worst path.


## Central biological question

Why does environmental heterogeneity sometimes select for contingent sensing or behavioral flexibility, but sometimes not?

The answer proposed by the current theory is not "because routeability is high."

It is:

\[
\boxed{
\text{selection for contingent sensing}
=
\text{decision-topology savings}
\times
\text{ecological value of those savings}
-
\text{architecture/comparator costs},
}
\]

with each term requiring a separate biological declaration.

## Layer 1 — structural opportunity

For a declared ecological decision task,

\[
C_A\le C_U,
\]

where C_A is the minimum worst-path cost of outcome-contingent acquisition and C_U=C_F is the minimum cost of one universal precommitted resolving bundle.

This establishes structural opportunity only.

The gap

\[
g=C_U-C_A
\]

is not intrinsically fitness.

Nor does the C_A-minimizing tree have to be the policy favored by selection. C_A solves a minimax guarantee problem:

\[
\pi_{\rm mm}
\in
\arg\min_\pi \max_x T_\pi(x).
\]

A biological policy exposed to state frequencies p_x and value-of-time V instead solves a distribution-sensitive objective such as

\[
\pi_V
\in
\arg\max_\pi
\sum_x p_x V[T_\pi(x)].
\]

The repository contains an exact four-world witness in which the minimax policy has worst path 2 but expected time-discounted performance 31/120, whereas a different policy with worst path 3 has performance 7/15.

Thus C_A is a guaranteed-complexity estimand, not a universal evolutionary policy objective.

## Layer 2 — ecological exposure of the structural opportunity

Let B be the random ecological opportunity limit and S_B(c)=P(B>=c).

The guarantee-level performance value uniquely exposed by contingent routing is

\[
\boxed{
R_{\rm opp}
=
vP(C_A\le B<C_U).
}
\]

Thus routeability matters when ecological opportunities actually terminate inside the interval saved by contingent acquisition.

The same structural gap can have very different value depending on where that interval lies relative to the natural-history distribution of opportunity limits.


## Layer 2b — general ecological value-of-time kernel

A literal opportunity deadline is only one interpretation.

Let \(V(t)\) be any nonincreasing ecological value of completing the correct action at time \(t\), after removing a time-independent baseline.

If \(V\) is differentiable, define the nonnegative marginal value-of-time kernel

\[
m(t)=-V'(t)\ge0.
\]

For architecture \(j\) with completion CDF \(F_j(t)\),

\[
E[V(T_j)]
=
V(\infty)
+
\int_0^\infty F_j(t)m(t)\,dt.
\]

Therefore the performance difference between architectures \(i\) and \(j\) is

\[
\boxed{
\Delta R_{i:j}
=
\int_0^\infty
[F_i(t)-F_j(t)]
m(t)\,dt.
}
\]

This is a useful process interface, but deadline-weighted utility profiles are established prior theory; it is no longer the novelty core of the paper.

The organism supplies the completion-time difference

\[
\Delta F(t)=F_i(t)-F_j(t),
\]

while natural history supplies the ecological value-of-time kernel

\[
m(t).
\]

Selection depends on their overlap.

The hard-deadline model, stochastic opportunity model, exposure-risk interpretation and declining-profitability interpretation are all special cases of this kernel form.


## Layer 3 — exact selection coefficient

With baseline fitness w0>0, timely-resolution value v>=0, and contingent-control log maintenance cost kappa,

\[
\boxed{
s_{\rm opp}
=
\log
\frac{w_0+vS_B(C_A)}
{w_0+vS_B(C_U)}
-\kappa.
}
\]

The old linear lift

\[
s=\lambda g-\kappa
\]

is recovered only locally:

\[
\lambda_{\rm local}
=
\frac{v}{w_0}f_B(C_A)
\]

for weak resolution value and a small structural gap.

Therefore lambda is an ecological/natural-history derivative, not a primitive universal constant.

## Robust versus expected evolutionary value

The sharp frontier theorem closes the frequency-free robust quantity

\[
R_{\rm robust}
=
U(C_A)-U(C_F).
\]

Expected evolutionary value is a different estimand:

\[
R_{\rm expected}(\pi)
=
\sum_x p_xU[T_\pi(x)]
-
U(C_F).
\]

For a minimax tree,

\[
R_{\rm expected}
\ge
R_{\rm robust},
\]

but equality need not hold.

Therefore:

- the structural frontier gives an exact **robust floor / statewise threshold**;
- encounter frequencies and branchwise completion times determine the extra
  expected-fitness value above that floor.

For any guaranteed-resolving policy \(\pi\) with worst path
\(H_\pi=\max_xT_\pi(x)\),

\[
\boxed{
R_{\rm expected}(\pi)
=
\underbrace{
U(H_\pi)-U(C_F)
}_{R_{\rm robust}(\pi)}
+
\underbrace{
\sum_xp_x\left[U(T_\pi(x))-U(H_\pi)\right]
}_{P_{\rm early}(\pi)\ge0}.
}
\]

The second term is the **early-termination premium**.  It is exactly the value
created when frequently encountered states terminate before the policy's worst
path.

This distinction is central to the biological interpretation.

### Exact expected-value rescue despite zero robust gain

The four-world witness in
`FITNESS_OPTIMAL_ROUTING_VS_MINIMAX.md` has

\[
C_A=C_F=2,
\]

so the robust adaptive value is exactly zero.

A different guaranteed policy has path costs

\[
(1,3,3,2).
\]

Let the one-step world occur with probability \(p\), and split
\(1-p\) equally among the other three worlds.

Under

\[
U(t)=e^{-\mu t},
\qquad
x=e^{-\mu},
\]

this adaptive policy beats the fixed cost-2 comparator exactly when

\[
\boxed{
p>
\frac{2x}{2x+3}.
}
\]

At

\[
\mu=\log2,
\]

the threshold is

\[
\boxed{p>1/4.}
\]

Thus robust gain can be zero while expected adaptive value is positive.

With additive architecture cost \(K\), the expected rescue remains possible
for some \(p<1\) exactly when

\[
\boxed{
K<x(1-x).
}
\]

At \(\mu=\log2\), this expected-value ceiling is \(1/4\), despite the
robust ceiling being zero for the same task.


## Absolute robust versus expected ceilings

When all finite information structure is allowed and \(U\) is bounded below,

\[
\boxed{
R_{\rm robust}^{\sup}
=
U(2)-U_\infty
}
\]

but, if positive world frequencies may be arbitrarily skewed,

\[
\boxed{
R_{\rm expected}^{\sup}
=
U(1)-U_\infty.
}
\]

Therefore encounter frequencies do more than add a small correction to a robust
margin. They open an exact **expected-only** regime:

\[
\boxed{
U(2)-U_\infty
\le K
<
U(1)-U_\infty.
}
\]

In this interval no finite architecture can repay its control cost in every
represented world, yet a finite task with a sufficiently common one-query
branch can repay it in expectation.

For exponential opportunity value,

\[
U(c)=v e^{-\mu c},
\]

the two absolute ceilings are

\[
v e^{-2\mu}
\quad\text{and}\quad
v e^{-\mu}.
\]

At \(\mu=0.3,\ v=1\), a cost \(K=0.60\) is above the absolute robust ceiling
\(0.548812\) but below the expected ceiling \(0.740818\).  The repository
contains an explicit finite binary witness with 99% mass on a one-query common
state whose expected advantage exceeds 0.60.


## Layer 4 — realized branch frequencies

Even the pair (C_A,C_U) does not identify realized expected fitness.

Worst-case costs determine a guaranteed lower bound, but actual evolutionary performance depends on branchwise completion costs T(x), encounter probabilities p_x, state values v_x, and state-specific opportunity functions S_x.

The pathwise object is

\[
\boxed{
W(\pi)
=
\sum_x p_xv_xS_x(T_\pi(x))
-
K_\pi
}
\]

in additive-fitness form, or its positive/multiplicative analogue when log selection is required.

Thus the empirical unit is not merely a decision tree. It is a decision tree embedded in an encounter process.

## Layer 5 — comparator semantics

The universal fixed comparator U is not always the biologically relevant evolutionary alternative.

A context-preindexed repertoire P can choose a branch-specific fixed program before the focal decision begins.

For the canonical two-branch task,

\[
C_P=\max(a,b),
\]

\[
C_A=r+\max(a,b),
\]

\[
C_U=r+a+b,
\]

so

\[
C_P<C_A<C_U.
\]

Hence contingent routing can beat U but lose to P at runtime.

Which architecture evolves depends on both runtime performance and constitutive architecture cost.

## Layer 6 — architecture value

For any declared pair of architectures i and j,

\[
s_{i:j}
=
\log\frac{\text{performance}_i}{\text{performance}_j}
-
(\kappa_i-\kappa_j).
\]

This is where PAYOFF logic enters:

\[
\Phi=R-K.
\]

adaptive-gain supplies a mechanistic source of R from decision topology and ecological opportunity; PAYOFF supplies the architecture-value accounting once the comparator and cost channels are declared.

## Layer 7 — downstream evolutionary response

Only after the state-specific selection signal is derived should it enter allele-frequency, quantitative-trait, eco-evolutionary feedback, fixation, or occupancy models.

The existing general response branch can then be read as downstream transport:

\`\`\`text
decision topology
-> branchwise completion costs
-> ecological opportunity process
-> architecture-specific performance
-> pairwise selection
-> evolutionary response
-> ecological feedback
\`\`\`

## Six nontrivial predictions

### P1 — intermediate ecological closure can maximize selection for contingent sensing

Under exponential opportunity closure,

\[
R_{\rm opp}(\mu)
=
v(e^{-\mu C_A}-e^{-\mu C_U})
\]

has a unique interior maximum at

\[
\mu^*
=
\frac{\log(C_U/C_A)}{C_U-C_A}.
\]

With positive architecture cost, selection can reverse twice as closure pressure increases:

\`\`\`text
fixed favored -> contingent favored -> fixed favored
\`\`\`

### P2 — equal structural gain does not imply equal selection

For fixed g=C_U-C_A under exponential closure,

\[
R_{\rm opp}
=
ve^{-\mu C_A}(1-e^{-\mu g}).
\]

Thus equal g can have different fitness value solely because absolute decision time differs.

### P3 — equal guarantee pair does not imply equal realized selection

Two tasks can share the same n, m, target counts, C_A and C_U yet differ in how often the contingent tree terminates early.

The faster path distribution has higher expected fitness under any strictly decreasing opportunity-value function.

### P4 — mean decision time is not sufficient

For stochastic completion times, fitness depends on

\[
q_j=\Pr(T_j\le B),
\]

not on \(E[T_j]\) alone.

Two architectures can have identical mean completion time while the sign of their pairwise selection reverses when the opportunity distribution changes.

This creates a direct empirical prediction: the early and late tails of the decision-time distribution can matter more than its mean.


### P5 — universal performance advantage is a stochastic-dominance claim

With stochastic completion times, one architecture has higher timely performance under every possible independent opportunity distribution if and only if its completion-time CDF lies everywhere above the comparator CDF.

Thus the exact process-level generalization of

\[
C_A\le C_F
\]

is not a comparison of mean latencies. It is first-order stochastic dominance:

\[
F_A(t)\ge F_F(t)\quad\forall t.
\]

If the curves cross, ecology can reverse the performance ordering by changing where opportunity limits fall.


### P6 — the sign of selection depends on the available comparator architecture

The same environment can give:

\[
s_{A:U}>0
\]

and

\[
s_{A:P}<0.
\]

Therefore "routeability favors adaptive sensing" is not a comparator-free statement.

## What should no longer be the headline

Do not make any of the following the central novelty claim:

- sequential cues can save sampling effort;
- heterogeneity can be routeable;
- decision time can affect fitness;
- time pressure can favor faster decisions;
- more information is not always more useful.

All have strong precedents.

## Proposed headline claim

> Natural history re-ranks an exact finite frontier of information
> architectures: the structure that maximizes adaptive efficiency need not
> maximize robust ecological value, and finite information constraints impose a
> sharp ceiling on the control cost that can be repaid in every represented
> state.

A shorter version:

> Structural adaptive gain supplies a robust floor; encounter frequencies
> convert early termination into an additional expected-fitness premium.

## Empirical measurement ladder

A biological system needs progressively stronger evidence:

1. reconstruct the focal target and cue topology;
2. estimate contingent and comparator completion-cost distributions;
3. measure the ecological value-of-time / opportunity-survival curve;
4. measure branch encounter frequencies and payoff values;
5. declare the biologically available comparator architectures;
6. estimate architecture-specific constitutive costs;
7. only then estimate selection and downstream evolutionary dynamics.

This ladder makes clear why a positive C_A<C_U receipt alone is a structural result, not an empirical fitness result.
