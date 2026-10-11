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


## 5b. Theorem FP2 — ecological urgency can switch the optimal cue order

The previous witness changes world frequencies. A second exact witness holds world frequencies fixed and changes only the ecological value of speed.

Use four equiprobable worlds with targets

\[
(0,0,1,1)
\]

and unit-cost binary queries

\[
q_0=(0,0,0,1),
\]

\[
q_1=(0,1,0,0),
\]

\[
q_2=(0,1,0,1),
\]

\[
q_3=(0,1,1,0).
\]

Consider two policy classes already realizable in this one fixed task.

### Balanced policy

A balanced root partitions the worlds into two target-mixed pairs, each resolvable with one additional query.

Its path vector is

\[
\boxed{
(2,2,2,2).
}
\]

Under

\[
V(t)=e^{-\mu t},
\]

its expected performance is

\[
\boxed{
J_{\rm balanced}=e^{-2\mu}.
}
\]

### Prioritized policy

A different root immediately resolves one world, resolves another in two steps, and leaves two worlds at depth three.

Its path multiset is

\[
\boxed{
\{1,2,3,3\}.
}
\]

With equal world frequencies,

\[
\boxed{
J_{\rm priority}
=
\frac{
e^{-\mu}
+
e^{-2\mu}
+
2e^{-3\mu}
}{4}.
}
\]

Let

\[
x=e^{-\mu}\in(0,1).
\]

Then

\[
J_{\rm priority}-J_{\rm balanced}
=
\frac{x}{4}
(2x-1)(x-1).
\]

Because \(x-1<0\),

\[
J_{\rm balanced}>J_{\rm priority}
\quad\Longleftrightarrow\quad
x>\frac12,
\]

or equivalently

\[
\boxed{
\mu<\log2.
}
\]

Likewise,

\[
\boxed{
\mu>\log2
\quad\Longrightarrow\quad
J_{\rm priority}>J_{\rm balanced}.
}
\]

At

\[
\boxed{
\mu^*=\log2
}
\]

the two policies tie exactly.

Therefore the same organisms, same state frequencies, same cue vocabulary, same cue costs and same target can change their fitness-optimal cue order solely because the ecological value of delay changes.

### Biological interpretation

Weak time pressure favors the balanced tree:

\[
(2,2,2,2).
\]

Strong time pressure favors a more prioritized tree:

\[
\{1,2,3,3\},
\]

which creates one immediate success at the cost of making two other states slower.

This is a decision-policy analogue of specialization under urgency:

> as delay becomes more costly, selection can favor early resolution of a subset of ecological states rather than uniformly good performance across all states.

The word "specialization" here refers only to decision-path allocation. It does not by itself imply narrower dietary, habitat or taxonomic niche breadth.

## Corollary FP2.1 — time pressure can rewire sensing without environmental turnover

No represented ecological state changes across the threshold.

Only the value-of-time parameter changes.

Thus:

\[
\boxed{
\text{ecological time pressure}
\to
\text{optimal decision-tree rewiring}
}
\]

can occur without:

- species turnover;
- cue turnover;
- target turnover;
- altered state frequencies.

This is a cleaner process prediction than treating routeability as a fixed property of an environment.

Routeability defines a feasible policy space. Natural history selects where within that space the organism should operate.


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
