# Required-gap scaling under local routing mutations

Status: side theory on `theory/local-routing-mutation-accessibility`. This note is not part of the frozen Theoretical Ecology submission.

## 1. Question

`LOCAL_ROUTING_MUTATION_ACCESSIBILITY.md` proves that, inside the fixed `k`-branch extremal sensing task, realized policy gain `r` requires exactly `k r` one-branch pruning mutations from the zero-saving full routing program.

The stronger question is whether this local accessibility cost can be composed with the **required structural gap `q`** used by the current flagship reachability theorem.

It can, for an exact query-minimal depth-two family.

## Theorem LRM2 — a query-minimal static gap can require quadratic local rewiring distance

Fix an integer required gap

```text
q>=1.
```

Set

```text
k=q+1
```

and allow maximum cue arity

```text
b=k=q+1.
```

Use the existing `k`-branch extremal star-routing task.

Then the task realizes the exact structural coordinates

```text
(worlds, queries, productive-frontier edges, adaptive depth)
=
(2q+2, q+2, q+2, 2),
```

which form a nondominated point on the exact bounded-arity gap-`q` Pareto frontier.

At the same time, under the declared one-branch-at-a-time pruning mutation syntax, the exact shortest mutation distance from the zero-saving full routing program to realized gain `q` is

```text
boxed: q(q+1).
```

The first positive worst-case gain cannot occur before `q+1` pruning mutations, so the first `q` local edits are necessarily neutral under the declared worst-path structural reward.

### Static proof

For maximum arity `b=q+1`, depth one cannot create a positive adaptive/fixed gap. At depth two, a full `b`-ary productive tree has

```text
1+b=q+2
```

internal-node occurrences, so its maximum fixed/adaptive difference is

```text
(q+2)-2=q.
```

Therefore

```text
h_b*(q)=2
```

and the exact minimum query/frontier burden is

```text
m_min=E_min=q+2.
```

To realize `q+2` productive internal-node occurrences at depth two, the root must have `q+1` target-mixed internal children. Every such child requires at least two represented worlds, giving

```text
n>=2(q+1)=2q+2.
```

The `k=q+1` star-routing task attains these bounds with exactly two worlds per branch. Hence

```text
(2q+2,q+2,q+2,2)
```

is the query/frontier-minimal depth-two Pareto point.

### Accessibility proof

The same task has

```text
C_A=2,
C_F=q+2,
g*=q.
```

Theorem LRM1 gives exact local pruning distance

```text
k r
```

to realized policy gain `r`. Setting

```text
k=q+1,
r=q
```

gives

```text
q(q+1).
```

QED.

## 2. Static size and local distance scale differently

Along this family:

```text
world count       = 2q+2          = Theta(q),
query count       = q+2           = Theta(q),
frontier burden   = q+2           = Theta(q),
adaptive depth    = 2             = constant,
local edit distance to full gain = q(q+1) = Theta(q^2).
```

So the smallest static task on this depth-two/query-minimal branch of the Pareto frontier need not be locally close, under the declared mutation operator, to an efficient heritable routing program.

This is not a universal statement about all genotype-policy encodings. It is an exact separation for one explicitly declared encoding and local mutation graph.

## 3. Strict-improvement accessibility barrier

At the zero-saving program

```text
ell_full=(k,...,k),
```

every one-edit neighbor has exactly the same realized gain `0`.

Therefore a local evolutionary/search dynamics that accepts only **strictly gain-increasing** one-edit mutants cannot leave the initial state at all, despite the existence of a policy with optimal gain `k-1`.

A dynamics that permits neutral moves can cross the plateau, with exact shortest distance `k` to the first positive gain and `k r` to gain `r`.

The generic role of neutral mutations, introns, redundant representations and fitness plateaus is established prior art. The repository-specific point is their exact composition with the finite sensing gap and the eco-evolutionary required-gap coordinate.

## 4. Exact plateau geometry

The pruning state space contains

```text
k^k
```

branch-length vectors.

For required realized gain `r`,

```text
g(ell)>=r
iff
ell_i<=k-r for every branch i.
```

Hence the number of states with gain at least `r` is

```text
N_>=r=(k-r)^k.
```

The number with gain exactly `r` is

```text
N_r=(k-r)^k-(k-r-1)^k
```

for `r<k-1`, with `N_{k-1}=1`.

At minimum distance `k r`, every branch must have been pruned exactly `r` times. Therefore the number of shortest branch-choice sequences from the full program to gain `r` is

```text
(k r)! / (r!)^k.
```

These are elementary combinatorial consequences of the declared product-state representation; they are not independent novelty claims.

## 5. Reverse eco-evolutionary chain under the side model

If a future extension explicitly lifts **realized policy gain** into feedback, rather than using the optimal task gap directly, the chain becomes

```text
required local feedback phase
-> required integer gap q
-> exact Pareto-minimal depth-two task
   (2q+2,q+2,q+2,2)
-> local routing mutation distance q(q+1)
   from the declared zero-saving program.
```

This is the cleanest direct connection yet between the earlier small-jump/accessibility idea and the current finite structural reachability theorem because both thresholds now live inside the same sensing-task state space.

It still remains a **side model**. The frozen manuscript does not claim that real sensory architectures mutate by deleting one redundant branch acquisition at a time.

## 6. Canonical q=2 example

For `q=2`:

```text
k=b=3,
(worlds,queries,E,depth)=(6,4,4,2),
minimum local pruning distance=6,
neutral prefix before first gain=2.
```

Thus the canonical structural task capable of the manuscript's first stable oscillatory gap is already present, yet the declared zero-saving routing genotype is six local edits from realizing the full gap.

## 7. Claim discipline

Do not advertise LRM2 as:

- the first theory of neutral evolution;
- a new theory of genetic-programming introns;
- a general decision-tree mutation lower bound;
- a universal biological sensory-evolution law;
- evidence that real organisms require `q(q+1)` mutations.

The safe statement is:

> For one explicit heritable routing encoding of the exact star-routing sensing family, a required structural gap `q` has a query-minimal depth-two task of linear size while the shortest branch-local pruning path from a zero-saving program to the full realized gap is `q(q+1)`.

See `LOCAL_ROUTING_MUTATION_PRIOR_ART.md` for the novelty ceiling.
