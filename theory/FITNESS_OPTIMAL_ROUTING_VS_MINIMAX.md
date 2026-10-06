# Fitness-optimal routing is not the minimax policy

Status: process extension on branch theory/opportunity-fitness-process-v1.

The core adaptive-gain quantity

\[
C_A
\]

is the minimum worst-path cost among guaranteed-resolving adaptive policies.

That is an exact and useful structural objective. It is not, in general, the policy objective maximized by natural selection.

## 1. Structural and evolutionary objectives

Let \(\pi\) be a guaranteed-resolving contingent policy.

For represented ecological world \(x\), let

\[
T_\pi(x)
\]

be its completion cost.

The core minimax policy solves

\[
\boxed{
\pi_{\rm mm}
\in
\arg\min_\pi
\max_x T_\pi(x).
}
\]

Its optimum value is \(C_A\).

Now assign world probabilities \(p_x\) and an ecological value-of-time function \(V(t)\).

A performance-optimal evolutionary policy instead solves

\[
\boxed{
\pi_V
\in
\arg\max_\pi
\sum_x p_xV[T_\pi(x)].
}
\]

Architecture cost can be added after this performance term.

There is no general reason for

\[
\pi_{\rm mm}=\pi_V.
\]

The distinction between worst-case and average/distribution-sensitive decision-tree objectives is established algorithmic decision theory. The biological point here is that the repository's finite routing structure supports both objectives, but only the latter is directly coupled to encounter frequencies and ecological value of time.

## 2. Exact four-world witness

Use four worlds with targets

\[
(0,0,1,1)
\]

and four unit-cost binary queries:

\[
q_0=(0,0,0,1),
\]

\[
q_1=(0,0,1,0),
\]

\[
q_2=(0,1,0,1),
\]

\[
q_3=(0,1,1,1).
\]

Let world \(w_0\) be common:

\[
p_0=\frac{27}{30},
\]

and each other world have probability

\[
p_1=p_2=p_3=\frac{1}{30}.
\]

Use the monotone ecological value of completion time

\[
V(t)=2^{-t}.
\]

### Minimax policy

The exact core solver gives

\[
C_A=2.
\]

With the registered query order, one selected minimax policy has path costs

\[
\boxed{
(2,2,2,1).
}
\]

Its expected performance is

\[
\frac{27}{30}\frac14
+
\frac{1}{30}\frac14
+
\frac{1}{30}\frac14
+
\frac{1}{30}\frac12
=
\boxed{
\frac{31}{120}
}
\approx0.2583.
\]

### Distribution-sensitive fitness policy

Query \(q_3\) first.

Its outcome 0 identifies the common world \(w_0\) immediately.

The other outcome retains the three rare worlds, which can still be guaranteed-resolved in at most two additional acquisitions.

A valid path-cost vector is

\[
\boxed{
(1,3,3,2)
}
\]

or the symmetric rare-world variant

\[
(1,3,2,3).
\]

Its worst path is therefore 3, strictly worse than \(C_A=2\).

But its expected ecological performance is

\[
\frac{27}{30}\frac12
+
\frac{1}{30}\frac18
+
\frac{1}{30}\frac18
+
\frac{1}{30}\frac14
=
\boxed{
\frac{7}{15}
}
\approx0.4667.
\]

Thus

\[
\boxed{
\frac{7}{15}
>
\frac{31}{120}.
}
\]

The policy with a **worse guaranteed completion cost has about 1.81 times the expected time-discounted performance** in this environment.

## 3. Theorem FP1 — minimizing C_A need not maximize ecological performance

The witness proves:

\[
\boxed{
\pi_{\rm mm}
\neq
\pi_V
}
\]

can occur even in a four-world, four-query, binary, unit-cost deterministic task.

Therefore

\[
\boxed{
C_A
\text{ identifies guaranteed adaptive complexity, not the evolutionarily optimal routing policy.}
}
\]

This is not a flaw in \(C_A\). It defines a different estimand.

## 4. Why ecology changes the preferred policy

The minimax policy protects rare difficult worlds from long decision paths.

The fitness-optimal policy can instead sacrifice performance in rare worlds to resolve a common valuable world earlier.

The preferred architecture therefore depends on:

- encounter probabilities \(p_x\);
- branch-specific completion costs;
- the ecological value-of-time function \(V(t)\);
- architecture costs.

This creates a direct ecological interpretation of route allocation:

> natural selection can favor a policy that is less robust in the worst case because it spends its early information budget on the states encountered most often or carrying the greatest time-sensitive payoff.

## 5. Exponential opportunity special case

For

\[
V(t)=e^{-\mu t},
\]

the fitness-sensitive objective is

\[
\boxed{
J_\mu(\pi)
=
\sum_x p_xe^{-\mu T_\pi(x)}.
}
\]

The executable solver in

\`adaptive_gain/policy_fitness.py\`

optimizes this quantity exactly over guaranteed-resolving adaptive policies.

As

\[
\mu\to0,
\]

the objective increasingly rewards lower expected cost.

As \(\mu\) increases, it increasingly rewards early resolution on high-probability branches.

It still differs from a pure worst-case objective.

## 6. Relation to stochastic completion-time theory

The earlier process theory treated an architecture as inducing a completion-time distribution \(T\).

This note closes the upstream link:

\[
\boxed{
\text{finite decision topology}
\to
\text{choice of routing policy}
\to
T_\pi
\to
\text{ecological value}
\to
\text{fitness}.
}
\]

Crucially, the ecological objective can feed back to **which decision tree is selected**, not merely assign fitness to one already-selected minimax tree.

## 7. Consequence for empirical work

Empirical applications should not automatically reconstruct the mathematical \(C_A\)-minimizing tree and call it the predicted biological policy.

Instead:

1. reconstruct the feasible cue/target decision structure;
2. estimate state frequencies and the value of decision time;
3. compare candidate policy path distributions;
4. ask whether observed routing resembles:
   - minimax guarantee optimization;
   - expected-time optimization;
   - opportunity-weighted fitness optimization;
   - or another objective.

This turns observed cue order into a biological hypothesis rather than assuming the organism solves the repository's minimax optimization problem.

## 8. Prior-art boundary

Do not claim novelty for:

- worst-case versus average-case decision-tree optimization;
- Bayesian decision trees;
- expected-depth optimization;
- Huffman-like coding intuitions;
- risk-sensitive control;
- exponential utility or time discounting.

The repository-specific result is narrower:

> the exact finite conditional-routing tasks already used to define adaptive gain can select a different routing architecture once the structural minimax objective is replaced by an explicit ecological value-of-time objective.

This distinction should be visible in the biological manuscript because it changes what \(C_A\) is allowed to mean.
