# Fitness-process claim spine for adaptive-gain

Status: synthesis note for PR #67. This is a proposed biological spine, not a frozen manuscript replacement.

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

This is the process-level core of the proposed paper.

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

> Environmental heterogeneity selects particular sensing policies through the interaction of feasible decision topology, encounter frequencies, the ecological value of decision time, and the alternative architectures available to evolution.

A shorter version:

> The fitness value of routeability is the overlap between where a decision architecture changes completion probability through time and where ecology assigns value to being faster.

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
