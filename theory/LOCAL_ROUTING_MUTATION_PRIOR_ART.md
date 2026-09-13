# Local routing-mutation prior-art audit

Status: conservative side-theory audit for `LOCAL_ROUTING_MUTATION_ACCESSIBILITY.md`, `LOCAL_ROUTING_MUTATION_SCALING.md`, and `LOCAL_ROUTING_MUTATION_RADIUS.md`. This is not part of the frozen Theoretical Ecology submission.

## 1. Neutrality and redundant program structure are established prior art

The generic observation that genotype/program changes can be fitness-neutral is deeply established in evolutionary computation and genetic programming.

Relevant neighboring concepts include:

- redundant genotype-phenotype representations;
- neutral networks connected by single mutations;
- genetic-programming introns / noneffective instructions;
- neutral drift across plateaus;
- code bloat and protective redundancy.

Representative anchors:

- Rothlauf & Goldberg (2003), *Redundant representations in evolutionary computation*, Evolutionary Computation 11:381-415, DOI `10.1162/106365603322519288`;
- Galvan-Lopez et al. (2011), *Neutrality in Evolutionary Algorithms... What do we know?*, Evolving Systems 2:145-163, DOI `10.1007/s12530-011-9030-5`;
- Nordin, Francone & Banzhaf (1996), *Explicitly Defined Introns and Destructive Crossover in Genetic Programming*, in Advances in Genetic Programming II;
- the later linear-GP lineage on noneffective instructions, including *An Analysis of the Influence of Noneffective Instructions in Linear Genetic Programming*, Evolutionary Computation 30:51-74, DOI `10.1162/evco_a_00296`.

Therefore the local-routing side line must not claim novelty for neutral mutations, neutral plateaus, redundant code, or neutral drift.

## 2. Program/tree pruning is established prior art

Removing redundant nodes or subtrees from evolved programs and decision structures is also established.

Rockett (2020), *Pruning of genetic programming trees using permutation tests*, Evolutionary Intelligence 13:649-661, DOI `10.1007/s12065-020-00379-8`, explicitly reviews earlier work on introns, dormant nodes, algebraic simplification and local subtree pruning.

Other evolutionary-programming work uses insertion/deletion mutation, cleaning operators, and removal of ineffective instructions.

Therefore the side line must not claim novelty for:

- deleting one program instruction at a time;
- pruning target-irrelevant/redundant operations;
- obtaining a smaller program with unchanged input-output behavior;
- evolutionary search over tree/program structure.

## 3. Representation locality is established prior art

Evolutionary-computation theory already emphasizes that accessibility depends jointly on:

```text
representation + mutation operator + fitness landscape.
```

Rothlauf's representation theory treats locality, redundancy and bias as central properties governing evolutionary search. Work on neutral networks similarly studies how mutational neighborhoods change reachability and evolvability.

Thus the generic slogan

```text
an optimum exists != it is locally accessible under a chosen representation
```

is not a novelty claim.

## 4. Evolvable sensory and decision architectures are also established prior art

A wider targeted search also rules out a broad claim that it is novel to let sensing or decision architecture itself evolve.

Important neighboring examples include:

- Eliassen, Andersen, Jorgensen & Giske (2016), *From sensing to emergent adaptations: Modelling the proximate architecture for decision-making*, Ecological Modelling 326:90-100, DOI `10.1016/j.ecolmodel.2015.09.001`. Their individual-based proximate sensing/information-processing/behaviour-control architecture is embedded in a genetic algorithm to find evolutionary adaptations.
- Watson (2005), *The Elementary Nature of Purposive Behavior: Evolving Minimal Neural Structures that Display Intrinsic Intentionality*, Evolutionary Psychology 3, DOI `10.1177/147470490500300103`. The model permits sensory, hidden and memory nodes to be added or eliminated by mutation.
- the broader evolutionary-network and evolutionary-robotics literature contains architecture mutations that add/remove connections, nodes, sensors, or controller structure.

Therefore do not claim novelty for:

- heritable sensory architecture;
- mutation of sensor number or decision-network structure;
- genetic-algorithm evolution of proximate information-processing architecture;
- active sensing as a biological or computational concept.

The local-routing line must earn any novelty from the **exact finite structural composition**, not from saying that sensing architecture evolves.

## 5. Why LRM1 alone is not a strong priority claim

LRM1 states that, in the declared product routing state

```text
ell=(ell_1,...,ell_k),
```

with gain

```text
g(ell)=k-max_i ell_i,
```

and one-coordinate decrement mutations, gain `r` is exactly `k r` edits from the full state.

The proof is elementary coordinate counting. The mandatory neutral prefix follows immediately from the `max` objective. This is useful exact bookkeeping for the biological composition, but mathematical priority should not be placed on the bare `k r` identity.

Likewise the plateau cardinalities

```text
(k-r)^k-(k-r-1)^k
```

and shortest-path multinomial counts are elementary consequences of the product representation.

LRM3's edit-radius thresholds `rho_first=k` and `rho_direct=k r` are the same geometry viewed as one-event mutation radii; they are not independent mathematical priority claims.

## 6. Stronger candidate composition after narrowing

The more defensible candidate is the chain that combines the already-established finite structural reachability theorem with the declared local routing mutation graph.

For required structural gap `q`, choose the exact depth-two/query-minimal star family with

```text
k=b=q+1.
```

Then the static task occupies the exact bounded-arity Pareto point

```text
(n,m,E,h)=(2q+2,q+2,q+2,2),
```

while the declared zero-saving routing program is exactly

```text
q(q+1)
```

one-branch pruning edits from realizing the full gap `q`.

The corresponding coordinated mutation-radius thresholds are

```text
rho_first=q+1,
rho_direct=q(q+1).
```

This yields the side-model composition

```text
required eco-evolutionary phase
-> required structural gap q
-> exact finite Pareto task
-> exact local routing accessibility distance / jump-radius threshold.
```

A targeted search located substantial prior art for every generic ingredient separately — neutral evolution, redundant representations, introns, tree pruning, mutation of program structure, evolvable sensing/decision architectures, and fitness plateaus — but did not locate an exact predecessor for this complete eco-evolutionary structural composition.

That search outcome is **not proof of priority**.

## 7. Important limitation: the quadratic distance is representation-dependent

The `q(q+1)` distance is not intrinsic to the sensing task itself.

It depends on the declared genotype/policy representation:

- branch programs are represented separately;
- one elementary mutation changes one branch only;
- only deletion of an irrelevant acquisition is allowed;
- coordinated deletions require an explicitly larger edit radius;
- rewiring, duplication, sensor invention and other mutation classes are excluded.

A different genotype-phenotype map can make the same optimal policy much closer or farther away. This is exactly why the representation literature is relevant.

The biologically meaningful question is therefore not whether `q(q+1)` is universal, but whether a real sensory-development mechanism justifies a mutation operator with comparable locality.

## 8. Strict-improvement trap is also not generic novelty

The full program has no strictly gain-improving one-edit neighbor, so a dynamics that accepts only strict improvements is trapped, while neutral-permitting dynamics can cross the plateau.

Neutral drift as an escape mechanism from plateaus is established in evolutionary computation. Do not claim this mechanism as new.

Its value here is diagnostic: it shows exactly which additional evolutionary-process assumption is needed after the static sensing optimum has been proven to exist.

## 9. Safe companion-paper novelty sentence

If this line is developed further, a defensible provisional sentence is:

> We compose an exact finite sensing-architecture requirement for a target eco-evolutionary feedback phase with an explicitly declared local mutation graph on heritable routing programs, thereby separating structural capability from mutational accessibility and deriving exact accessibility distances and mutation-radius thresholds for a Pareto-minimal sensing family.

This remains a candidate composition, not a priority statement.

Avoid:

- `first mutational theory of sensing`;
- `first neutral plateau for decision trees`;
- `first evolutionary pruning model`;
- `first evolution of sensory architecture`;
- `universal q(q+1) mutation law`;
- any suggestion that the deletion-only encoding is empirically established biology.

## 10. Current verdict

LRM1-LRM3 are mathematically correct side results and create a cleaner small-jump connection than reinterpreting PAYOFF topology. Their standalone combinatorics are too elementary and too close to established neutrality/pruning/representation ideas to carry a paper by themselves.

The possible publication value is in the **composition**:

```text
finite ecological sensing requirement
+
explicit genotype-policy locality
+
mutation accessibility to the required feedback phase.
```

The next substantive step is not another pruning identity. It is either:

1. justify a biologically meaningful mutation representation for sensory routing; or
2. add a population process (neutral drift / mutation-selection) on the exact routing state graph and derive a result that depends on the ecological required-gap coordinate rather than on generic plateau theory alone.
