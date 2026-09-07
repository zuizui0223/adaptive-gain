# Open problems

The finite deterministic guaranteed-resolution layer now has several closed components:

```text
exact adaptive optimum C_A
fixed-cost certificate ladder
  private pair
  -> integral pair packing
  -> fractional pair-cover dual
  -> exact integer budget-infeasibility proof at B=C_A
exact bypass decomposition C_A <= C_F <= C_U <= U
two-sided residual kernelization
exact shared-state proof DAG quotient
exact weighted-incidence residual isomorphism quotient
bipartite color refinement
exact individualization-refinement canonicalization
exact small-task query automorphism audit
stabilizer-orbit pruning of individualization branches
explicit isomorphism-transport proof DAG edges
parent-automorphism orbit pruning of proof branches
branch-orbit proof-size accounting
unique minimal 4-world / 3-query strict-gain normal form
complete 4-world / 4-query one-query-extension classification
unique deletion-minimal 5-world / 2+3-target / 3-query strict-gain normal form
full identity-indexed target-pair incidence sufficiency for deterministic C_A and C_F
pair-side Sperner kernel bound
```

The next problems concern cheaper symmetry certification, **adaptive-safe compression of the full target-pair incidence**, stronger bounds, larger normal-form classifications, and extensions beyond finite deterministic target resolution.

## 1. Certify automorphism generators without enumerating the full stable-color permutation family

The earlier factorial-canonicalization and proof-reuse questions are substantially closed for small residual states.

`color_refinement.py` can reduce exact query permutations before canonicalization; one registered benchmark goes from `720` candidates to `12`. `individualization_refinement.py` breaks higher-order color collisions. `automorphism.py` distinguishes unresolved search ambiguity from genuine query symmetry, and `orbit_pruning.py` keeps one individualization representative per exact stabilizer orbit.

`isomorphism_proof_dag.py` stores explicit query transports on shared subproof edges. `symmetry_pruned_proof_dag.py` goes further: when several affordable proof branches lie in one exact parent query-automorphism orbit, it recursively proves one representative child and stores explicit child-isomorphism transports for the skipped branches.

For a proof node `v`, with `b(v)` raw affordable branches and `o(v)` orbit representatives,

\[
s(v)=b(v)-o(v)
\]

is an exact executable branch-saving quantity, with local bound

\[
1\le b(v)/o(v)\le |\operatorname{Aut}(I_v)|.
\]

However the current automorphism audit still obtains a complete group by enumerating every stable-color-preserving query permutation up to a hard cap. Downstream orbit pruning is exact only after paying that group-certification cost.

Open questions:

- Can a small generator set and its **completeness** be certified without enumerating the whole candidate permutation family?
- Can a stabilizer chain be built incrementally during individualization and reused by the proof DAG?
- Can graph-canonicalization traces provide a compact proof that skipped branches are in the same automorphism orbit?
- Can the branch-orbit bound be sharpened using stabilizer sizes of the chosen obligation or already selected proof path?
- Can a global proof-size bound be expressed in certified orbit counts without first materializing every residual automorphism group?

The fail-closed rule remains: exceeding a symmetry/group-certification cap means `quotient_incomplete`, never `non_isomorphic` or `strict_gain`.

## 2. Tight kernel-size bounds beyond the pair-side Sperner bound

After pair-obligation dominance, distinct nonempty separator signatures form an inclusion antichain over `m` remaining queries, hence

\[
|U_K|\le {m\choose\lfloor m/2\rfloor}.
\]

Both the four-world minimal core and the new five-world deletion-minimal core reduce to the same minimal fixed-side signatures

\[
\boxed{(1,2,4)}
\]

at `m=3`, saturating the three-element Sperner bound.

Open questions:

- What joint bounds follow when query dominance is imposed simultaneously?
- For unit query costs, both row and column signatures are antichains; what incidence matrices can satisfy both conditions?
- Can branch-exclusive overhead or residual budget sharpen the middle-binomial bound?
- Is there a kernel-size bound parameterized by `C_A`, `C_F-C_A`, or selected adaptive-tree union size rather than raw query count?
- After exact automorphism quotienting, can the number of distinct residual kernels be bounded by orbit counts rather than raw row/column counts?

A useful result would bound the size or number of exact proof instances after safe preprocessing, not merely one side of the incidence matrix.

## 3. Find the coarsest adaptive-safe compression of full target-pair incidence

The five-world classification initially looked like a failure of pair incidence on the adaptive side, but the precise result is sharper.

For every query and every pair of worlds with different targets, retain the **identity-indexed** separation bit

\[
S_q(u,v)=\mathbf 1[q(u)\ne q(v)].
\]

Together with world identities, target labels, query identities, and query costs, this full incidence determines both exact fixed resolution and exact adaptive worst-path target-resolution cost. `target_pair_incidence.py` reconstructs each target-mixed query outcome cell as a connected component of the graph of cross-target **nonseparation** edges and then runs the Bellman recursion. The theorem is documented in `FULL_PAIR_INCIDENCE_SUFFICIENCY.md`.

Regression tests include all `15^3=3,375` triples of arbitrary deterministic set partitions on four worlds, not only binary outcomes.

What fails is the more aggressive fixed-side compression. The four-world core has raw pair rows `(1,2,4,7)` and the five-world deletion-minimal core has `(1,2,3,4,5,6)`, but pair-obligation dominance reduces both to `(1,2,4)`. A same-five-world no-gain control also has that minimal kernel while changing the exact costs from `(2,3)` to `(3,3)`.

Thus

\[
\boxed{
\text{full identity-indexed pair incidence is adaptive-safe,}
}
\]

but

\[
\boxed{
\text{the inclusion-minimal fixed-cover kernel is not.}
}
\]

The new open problem is therefore not to replace pair incidence wholesale, but to characterize **which reductions of the full incidence preserve `C_A`**.

Questions:

- Which pair-obligation deletions are safe for adaptive Bellman values, and which are safe only for fixed cover?
- Is the state-local collection of target-mixed outcome components a minimal sufficient representation for `C_A`?
- Can worlds of one target be quotient-ed by a target-resolution bisimulation without changing any future Bellman value?
- Can a polynomial-time refinement compute the coarsest such quotient?
- Can an adaptive-safe kernel be strictly smaller than full identity-indexed incidence while still preserving all reachable residual states?
- Which parts of the sufficiency theorem survive stochastic observation kernels or information-valued objectives?

This distinction between **full incidence** and **fixed-minimal kernel** should remain explicit in all subsequent claims.

## 4. Classify the next finite normal forms

Two nearby scopes are closed.

### Four worlds, four queries

For

```text
4 worlds
2+2 target multiplicity
4 binary unit-cost queries
```

all `16^4 = 65,536` labeled tasks were enumerated. There are 3,840 strict tasks, all with `(C_A,C_F)=(2,3)`, and every one contains the unique three-query strict core after deleting at least one query. The only strict canonical signatures are

```text
(0,3,5,9)   null-query extension
(3,3,5,9)   duplicated terminal-query extension
(3,5,9,9)   duplicated routing-query extension
```

so no new irreducible mechanism appears merely by adding one query identity.

### Five worlds, three queries

For

```text
5 worlds
2+3 target multiplicity
3 binary unit-cost queries
```

all `32^3 = 32,768` labeled tasks were enumerated. There are 2,016 strict tasks in five canonical signature classes. Exactly 288 are world/query deletion-minimal and all belong to one new orbit with signature

\[
\boxed{(7,28,42)}.
\]

This is the first new irreducible normal form after the four-world core, and an optimal root has positive direct target information under uniform represented-world weights.

Next questions:

- What new irreducible forms first appear with five worlds **and four queries**?
- What is the next deletion-minimal form at six worlds?
- At what smallest scope can `C_F/C_A` exceed `3/2`?
- What is the smallest scope with strict gain and nonzero internal or external bypass **inside a deletion-minimal core**?
- What is the smallest integral-packing or fractional integrality gap after quotienting the new adaptive normal forms?
- How many normal forms remain after simultaneous world, query, outcome, and certified automorphism quotienting?

Counts should continue to be reported both raw-labeled and modulo declared exact symmetries.

## 5. Characterize external fixed bypass locally

The exact decomposition is

\[
U-C_A=(C_F-C_A)+(C_U-C_F)+(U-C_U),
\]

where `C_U-C_F` is the external shortcut discount.

Internal redundancy is visible inside the adaptive tree union. External shortcutting depends on the larger measurement vocabulary and remains more global.

Open questions:

- Can an outside query be certified irrelevant using only its incidence on private/minimal pair obligations?
- Is there a cut-style certificate that every external shortcut must cross?
- What query-vocabulary operations monotonically create or destroy external bypass?
- Can external shortcut discount be bounded without solving the full fixed cover?

## 6. Information-valued adaptive gain

For MROD-like tasks the utility need not be binary target resolution:

\[
G(B)=\max_{\pi:c(\pi)\le B}I(T;H_\pi)-\max_{F:c(F)\le B}I(T;Q_F).
\]

The cost theory shows why routing entropy alone is insufficient: the optimized fixed class can bypass an adaptive route. The five-world deletion-minimal core additionally shows that a genuinely irreducible routing root may carry positive direct target information.

Questions:

- What are the information analogues of internal redundancy and external shortcut discount?
- Can the class-oracle information gap have multiple disconnected positive budget windows?
- Under what assumptions is the information objective submodular or adaptively submodular?
- What certificate replaces cross-target pair separation when partial information rather than exact resolution is the target?
- Is there an information-valued analogue of branch-orbit proof compression for equivalent continuation experiments?
- What representation replaces deterministic pair incidence when observations are noisy likelihoods?

## 7. Continuous compatible sets

PAYOFF's scientific uncertainty is continuous. A desired extension has

\[
\Theta_{t+1}=\Theta_t\cap C(q_t,y_t)
\]

and target map `T(theta)` without discretizing `Theta` into an unjustified finite panel.

A continuous counterpart of pair cover must certify separation of every parameter pair with different target values. This becomes an uncountable separation problem.

Potential directions include convex/semi-algebraic certificates, interval branch-and-bound, and finite witness reductions whose completeness is proved rather than assumed.

## 8. Calibration actions versus target actions

MROD, PAYOFF, and BALANCE all expose the resource tradeoff

```text
measure the scientific target
vs
improve the measurement model itself.
```

A calibration action can change the future query structure, so a static cover model is insufficient. The state must carry both scientific uncertainty and calibration uncertainty.

## 9. Stochastic branch-invariance and scenario robustness

BALANCE's current no-routing theorem is deterministic/minimax. Under stochastic errors, equal span need not imply equal continuation distributions.

The probabilistic analogue likely requires equality of continuation-value kernels rather than raw state summaries. Randomized policies under multiple calibration scenarios are another separate objective and should not be imported into deterministic guaranteed resolution by default.

## 10. Empirical identification of routing value

A natural-data routing claim needs more than low direct information of the first observation. The finite controls establish that:

- zero direct root information is neither necessary nor sufficient;
- deletion-minimal strict gain can have a positive-information root;
- fixed bypass may be internal or external;
- bypass may remove all or only part of potential gain;
- lower-bound relaxations may miss integer fixed-cost gaps;
- label-different residual states can be the same continuation problem after exact weighted-incidence quotienting;
- residual symmetry can be local-color ambiguity, higher-order ambiguity, or a genuine automorphism, and those cases should not be conflated;
- symmetric proof branches may be mathematically redundant even though the underlying measurements remain distinct named actions;
- identical inclusion-minimal fixed kernels do not imply identical adaptive routing geometries;
- full deterministic identity-indexed pair incidence is sufficient for guaranteed target-resolution cost, but that does not establish the same sufficiency for noisy or information-valued objectives.

An empirical claim therefore needs evidence that the first result changes the useful continuation, the branch-specific plan has a real resource advantage, plausible fixed bypasses are bounded, and the measurement/calibration relationships transport to deployment.

The source repositories currently provide synthetic/conditional witnesses, not that natural-data demonstration.
