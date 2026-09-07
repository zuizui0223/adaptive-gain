# adaptive-gain

A finite theory repository for **when outcome-contingent measurement choice is strictly better than a fixed measurement bundle**.

It was extracted from a cross-repository comparison of:

- [`zuizui0223/mrod`](https://github.com/zuizui0223/mrod) — an initial observation can route the next assay;
- [`zuizui0223/payoff`](https://github.com/zuizui0223/payoff) — an initial payoff contrast can route the next architecture distance;
- [`zuizui0223/balance`](https://github.com/zuizui0223/balance) — under the current threshold-span objective, branch labels change interval location but not the sufficient future-value state, giving a no-routing control.

The source repositories retain ownership of their scientific models. `adaptive-gain` abstracts only the finite **decision structure** and has no runtime dependency on those repositories.

## Core finite problem

Let `W` be a finite represented hidden-world set, `T: W -> labels` the declared target, and each query have a positive integer acquisition cost plus one deterministic outcome in every represented world.

A fixed design chooses one bundle before seeing outcomes. An adaptive design chooses the next query from outcomes already observed.

Define

```text
C_A = minimum worst-path cost of guaranteed target resolution by an adaptive tree
C_F = minimum cost of a fixed resolving bundle
```

Every fixed bundle is an adaptive policy that ignores intermediate outcomes, so

\[
\boxed{C_A\le C_F}.
\]

Strict adaptive gain exists exactly when

\[
\boxed{C_A<C_F}.
\]

For integer acquisition budget `B`, the exact adaptive-only resolution window is

\[
\boxed{C_A\le B<C_F}.
\]

## Where potential gain goes

Let `pi*` be the selected optimal adaptive tree. Define

```text
U   = total cost of every distinct query appearing anywhere in pi*
C_U = cheapest fixed resolving subset restricted to that tree union
```

Then

\[
\boxed{C_A\le C_F\le C_U\le U}
\]

and

\[
\boxed{
U-C_A
=(C_F-C_A)+(C_U-C_F)+(U-C_U)
}.
\]

Interpret the terms as

```text
branch-exclusive overhead = U - C_A
realized adaptive gain     = C_F - C_A
external shortcut discount = C_U - C_F
internal union redundancy  = U - C_U
```

so

\[
\boxed{
\text{adaptive gain}
=
\text{branch-exclusive overhead}
-
\text{internal redundancy}
-
\text{external shortcut}
}.
\]

Bypass is therefore a discount, not a binary veto. Registered six-world controls show that one unit of internal or external bypass can coexist with one remaining unit of strict gain.

Implementation: `adaptive_gain/decomposition.py`.

## Fixed resolution is a target-pair cover

Only world pairs with different target values need to be separated:

\[
P_T=\{\{w_i,w_j\}:T(w_i)\ne T(w_j)\}.
\]

Each query covers the cross-target pairs on which its outcomes differ. A fixed resolving bundle is therefore a weighted target-pair cover.

This connects the fixed side to established Test Cover / Set Cover structure. The repository does **not** claim invention of those general covering methods; it uses them to build checkable fixed-side comparators for the adaptive problem.

## Certificate ladder

Strict gain can often be certified without first computing the exact numerical `C_F`.

```text
private-pair necessity
  -> integral pair packing
  -> fractional pair-cover dual
  -> exact integer budget-infeasibility proof at B=C_A
  -> exact fixed optimum, only when its value is needed
```

The layers are genuinely distinct:

- source-derived MROD/PAYOFF controls are already certified by private pairs;
- a larger control needs integral packing;
- another has integral packing 2 but fractional optimum `5/2`, so only the fractional layer proves `C_F>=3`;
- an LP-integrality-gap control has `C_A=2`, fractional lower bound 2, and `C_F=3`, so only the exact integer budget proof closes the strict-gain claim.

The integer proof emits a checkable infeasibility tree. `verify_fixed_budget_decision_certificate()` reconstructs the target-pair system and independently verifies every branch, budget update, and separator obligation.

See:

- `theory/FIXED_BYPASS_PAIR_COVER.md`
- `theory/PAIR_PACKING_LOWER_BOUND.md`
- `theory/FRACTIONAL_PAIR_COVER_BOUND.md`
- `theory/INTEGER_FIXED_COVER_PROOF.md`

## Proof compression stack

The exact integer comparison now has several semantics-preserving compression layers.

### 1. Two-sided residual kernel

Before branching, `cover_kernel.py` repeatedly applies exact reductions:

```text
inactive/unaffordable query deletion
pair-obligation dominance
unique-separator forcing
query dominance
```

A seeded eight-world strict-gain control has `C_A=3,C_F=4`; the unkernelized integer proof visits 13 states, while the kernel closes the fixed-budget impossibility in one kernel call with zero genuine branch states.

After pair dominance, nonempty separator signatures form an inclusion antichain over the remaining queries. Therefore, for `m` remaining queries,

\[
\boxed{|P_K|\le {m\choose\lfloor m/2\rfloor}}
\]

by Sperner's theorem. The unique minimal strict-gain normal form below saturates this bound at `m=3`.

### 2. Exact-state proof DAG

Different branch histories can reach the literal same residual `(uncovered pairs, available queries, budget)` state. `proof_dag.py` stores that subproof once and references it by node ID. A registered control compresses 19 expanded tree nodes to 14 DAG nodes.

### 3. Weighted-incidence isomorphism quotient

Label-different residual states can still be the same continuation problem. `isomorphism_quotient.py` forgets pair order and query names while preserving:

```text
remaining budget
query acquisition costs
pair-query incidence
```

A six-world / six-query strict-gain control has

```text
C_A = 2
C_F = 3
4 label-specific residual states
2 weighted-incidence isomorphism classes
```

so this quotient gives compression beyond exact-state DAG sharing. The first merge exports an explicit query-bijection witness that is independently checked by `verify_residual_pair_cover_isomorphism()`.

### 4. Bipartite color refinement before exact canonicalization

`color_refinement.py` propagates isomorphism-invariant colors between obligation rows and query columns before exact query-permutation enumeration.

A registered eight-query residual benchmark has

```text
initial query permutation family = 720
stable refined family            = 12
```

so the exact canonicalization search is reduced by a factor of 60. All 4096 minimal tasks preserve the exact canonical isomorphism classes.

Color refinement is deliberately not treated as an isomorphism test. A connected bipartite 8-cycle and two disjoint 4-cycles remain color-indistinguishable but have different exact canonical forms.

### 5. Exact individualization-refinement

`individualization_refinement.py` handles higher-order color collisions by choosing a non-singleton query color class, individualizing one query, refining again, and recursively exploring every required branch.

For each of the two regular color-collision controls,

```text
stable exact permutations = 24
IR canonical leaves       = 8.
```

The IR encoding need not be byte-identical to the older brute-force canonical encoding; exactness is checked by equality of induced isomorphism classes. Over all 4096 minimal tasks, the old exact canonicalizer and IR canonicalizer give a one-to-one correspondence between equivalence classes.

### 6. Exact automorphism audit and stabilizer-orbit pruning

`automorphism.py` enumerates the complete small-task query automorphism group after stable refinement, verifies a generator set, and reports query orbits. If the stable color classes leave

\[
N_{\rm color}=\prod_i |C_i|!
\]

labelings and the exact residual automorphism group is `G`, then

\[
\boxed{N_{\rm distinct}=N_{\rm color}/|G|}.
\]

`orbit_pruning.py` uses the subgroup fixing the already individualized queries pointwise. Only one representative per stabilizer orbit must be individualized.

Registered controls give:

| Residual structure | Stable permutations | IR leaves | `|Aut|` | Orbit-pruned leaves |
|---|---:|---:|---:|---:|
| Minimal strict-gain normal form | 6 | 6 | 6 | **1** |
| Connected bipartite 8-cycle | 24 | 8 | 8 | **1** |
| Two disjoint 4-cycles | 24 | 8 | 8 | **1** |
| 720->12 refinement benchmark | 12 | 12 | 12 | **1** |

The current automorphism audit itself still enumerates the stable-color-preserving permutation family up to a hard cap. Orbit pruning therefore removes downstream canonical-leaf redundancy, but does not yet avoid the full exact group-certification cost.

### 7. Explicit isomorphism transports in proof DAG edges

`isomorphism_proof_dag.py` exports the isomorphism reuse itself as a proof object. Every shared child edge stores an explicit query bijection from the reconstructed source child instance to its representative DAG node.

The verifier does **not** trust canonical-signature equality. It reconstructs each child from the parent query and directly verifies the supplied cost/incidence-preserving transport before reusing the representative subproof. A tampered transport is rejected by regression tests.

### 8. Parent-automorphism branch pruning

`adaptive_gain/symmetry_pruned_proof_dag.py` now compresses the sibling branch set itself. If an exact parent residual automorphism maps query `q` to query `r`, then

\[
\boxed{I\setminus q\cong I\setminus r}.
\]

Thus, among the affordable separators of one proof obligation, one recursive child proof per exact query-automorphism orbit is sufficient. Every skipped branch carries an explicit child-to-orbit-representative transport.

For a proof node `v`, write

\[
b(v)=\text{raw affordable branch count},\qquad
o(v)=\text{orbit-representative count}.
\]

Then the exact local branch saving is

\[
\boxed{s(v)=b(v)-o(v)}
\]

and the local compression factor obeys

\[
\boxed{1\le \frac{b(v)}{o(v)}\le |\operatorname{Aut}(I_v)|}.
\]

`proof_size_bounds.py` recomputes these metrics from the stored proof object rather than trusting execution counters.

The reusable four-query C4 control gives

```text
raw affordable branches = 2
orbit representatives    = 1
local saving             = 1
local factor             = 2
parent automorphism size = 8
```

while still providing an explicit transport for the skipped branch. All 4096 minimal tasks retain the exact strict/no-gain classification.

The exact compression/canonicalization chain is now

\[
\boxed{
\text{raw proof tree}
\to
\text{two-sided kernel}
\to
\text{exact-state DAG}
\to
\text{weighted-incidence quotient}
\to
\text{color refinement}
\to
\text{individualization-refinement}
\to
\text{certified automorphism-orbit pruning}
\to
\text{transported proof DAG}
\to
\text{automorphism-orbit-pruned proof branches}
}.
\]

See:

- `theory/FIXED_COVER_KERNELIZATION.md`
- `theory/PROOF_DAG_COMPRESSION.md`
- `theory/RESIDUAL_ISOMORPHISM_QUOTIENT.md`
- `theory/BIPARTITE_COLOR_REFINEMENT.md`
- `theory/SYMMETRY_REFINEMENT_AND_AUTOMORPHISMS.md`
- `theory/SYMMETRY_PRUNED_PROOF_DAG.md`

## Unique minimal strict-gain normal form

Strict worst-path adaptive cost gain requires at least

```text
4 represented worlds
3 query identities
```

For the complete balanced minimal universe

```text
4 worlds
T = (0,0,1,1)
3 labeled binary unit-cost queries
```

there are `16^3=4096` declared query triples. Exact classification is:

| `(C_A,C_F)` | Count |
|---|---:|
| unresolved | 1688 |
| `(1,1)` | 1352 |
| `(2,2)` | 864 |
| `(2,3)` | **192** |

The 192 strict-gain tasks are not 192 structural types. Quotienting target-preserving world permutations, query permutations, and independent binary outcome flips collapses all 192 into **one symmetry orbit**.

A canonical standard form is

\[
q_0=(0,0,1,0),\qquad
q_1=(0,1,1,0),\qquad
q_2=(0,1,1,1),
\]

with canonical cross-target separator signature

\[
\boxed{(3,5,9)}.
\]

Over all 4096 tasks in this declared scope,

\[
\boxed{
C_A<C_F
\iff
\text{canonical signature}=(3,5,9)
}
\]

with zero false positives and zero false negatives against the exact solver.

The raw multiplicity is explained by the declared symmetry orbit:

\[
4\times 3!\times2^3=192.
\]

At the residual fixed-cover level the standard form has full query automorphism group

\[
\boxed{\mathrm{Aut}\cong S_3,\qquad |\mathrm{Aut}|=6,}
\]

so its six query relabelings are genuine self-symmetry, not unresolved color-refinement ambiguity.

See `theory/MINIMAL_STRICT_GAIN_NORMAL_FORM.md`.

## Source-derived witnesses

For both registered MROD-style and PAYOFF-style routing abstractions:

```text
C_A = 2
C_F = C_U = U = 3
```

Under uniform represented worlds, the first routing observation has zero direct target information, while the selected adaptive policy identifies the target completely. The best fixed information at budget 2 is 0.5 bit in both abstractions.

This demonstrates

```text
zero direct target information != zero decision relevance
```

but zero direct information is neither necessary nor sufficient for adaptive gain in general.

BALANCE supplies the negative control: under the current midpoint-reset span objective, supported branch labels change interval location but not the declared sufficient future-value state, so extra direction adaptivity has no gain at that step.

## Validation

The test suite includes:

- independent exact-oracle checks;
- the complete 4096-task minimal universe;
- bypass controls;
- integral/fractional/integer certificate gaps;
- tampered proof rejection;
- two-sided kernel equivalence;
- exact-state DAG verification;
- residual isomorphism witnesses and quotient regression;
- color-refinement exact-class regression and adverse regular controls;
- individualization-refinement class-equivalence regression;
- exact automorphism group and generator verification;
- stabilizer-orbit-pruned versus unpruned IR regression;
- explicit isomorphism-transport proof DAG verification;
- parent-automorphism branch pruning with skipped-branch transport verification;
- branch-orbit proof-size accounting and metadata-tamper detection;
- the unique minimal normal-form iff classifier.

CI runs the suite on Python 3.10, 3.11, and 3.12, plus the executable witness and certificate-ladder audits.

## Package

```text
adaptive_gain/
  core.py
  certificates.py
  decomposition.py
  pair_cover.py
  pair_packing.py
  fractional_packing.py
  integer_cover_proof.py
  cover_kernel.py
  kernel_bounds.py
  proof_dag.py
  isomorphism_quotient.py
  color_refinement.py
  individualization_refinement.py
  automorphism.py
  orbit_pruning.py
  isomorphism_proof_dag.py
  symmetry_pruned_proof_dag.py
  proof_size_bounds.py
  symmetry_witnesses.py
  minimal_normal_form.py
  exhaustive.py
  information.py
  witnesses.py

theory/
  ADAPTIVE_GAIN_THEOREM.md
  STRUCTURAL_DECOMPOSITION_AND_MINIMALITY.md
  FIXED_BYPASS_PAIR_COVER.md
  PAIR_PACKING_LOWER_BOUND.md
  FRACTIONAL_PAIR_COVER_BOUND.md
  INTEGER_FIXED_COVER_PROOF.md
  FIXED_COVER_KERNELIZATION.md
  PROOF_DAG_COMPRESSION.md
  RESIDUAL_ISOMORPHISM_QUOTIENT.md
  BIPARTITE_COLOR_REFINEMENT.md
  SYMMETRY_REFINEMENT_AND_AUTOMORPHISMS.md
  SYMMETRY_PRUNED_PROOF_DAG.md
  MINIMAL_STRICT_GAIN_NORMAL_FORM.md
  PROVENANCE.md
  OPEN_PROBLEMS.md
```

## Scope boundary

This repository does **not** claim:

- a new general theory of adaptive experimental design, Set Cover, Test Cover, graph isomorphism, color refinement, or group algorithms;
- that PAYOFF, MROD, and BALANCE are the same scientific model;
- that branch dependence alone is sufficient for adaptive gain;
- that zero direct target information is necessary or sufficient for gain;
- that bypass must eliminate gain;
- that failed lower-bound or quotient certificates imply no gain;
- polynomial-time exact integer cover or general graph canonicalization;
- that finite synthetic controls are empirical evidence;
- that target resolution licenses a biological report.

The contribution is a tested bridge between exact adaptive-tree costs and increasingly strong, checkable fixed-side certificates, together with exact proof compression, certified symmetry handling, and finite structural classification exposed by the three source repositories.

## Run

```bash
python -m pip install -e .
python -m pytest -q
python examples/audit_witnesses.py
python examples/audit_certificate_ladder.py
```
