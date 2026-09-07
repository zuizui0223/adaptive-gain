# adaptive-gain

A finite theory repository for **when outcome-contingent measurement choice is strictly better than a fixed measurement bundle**.

It was extracted from a cross-repository comparison of:

- [`zuizui0223/mrod`](https://github.com/zuizui0223/mrod) — an initial observation can route the next assay;
- [`zuizui0223/payoff`](https://github.com/zuizui0223/payoff) — an initial payoff contrast can route the next architecture distance;
- [`zuizui0223/balance`](https://github.com/zuizui0223/balance) — under the current threshold-span objective, branch labels change interval location but not the sufficient future-value state, giving a no-routing control.

The source repositories retain ownership of their scientific models. `adaptive-gain` abstracts only the finite **decision structure** and has no runtime dependency on those repositories.

## Core finite problem

Let `W` be a finite represented hidden-world set, `T: W -> labels` the declared target, and each query have a positive integer acquisition cost plus one deterministic outcome in every represented world.

A **fixed design** chooses one bundle before seeing outcomes. An **adaptive design** chooses the next query from outcomes already observed.

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

For integer acquisition budget `B`, the adaptive-only guaranteed-resolution window is

\[
\boxed{C_A\le B<C_F}.
\]

## Where potential gain goes

For a selected optimal adaptive tree `pi*`, let

```text
U   = cost of every distinct query used anywhere in pi*
C_U = cheapest fixed resolver restricted to that tree union
```

Then

\[
\boxed{C_A\le C_F\le C_U\le U}
\]

and exactly

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

Bypass is a discount, not a binary veto: registered six-world controls retain one unit of strict gain despite one unit of internal or external bypass.

Implementation: `adaptive_gain/decomposition.py`.

## Fixed resolution as target-pair cover

Only world pairs with different target values require separation:

\[
P_T=\{\{w_i,w_j\}:T(w_i)\ne T(w_j)\}.
\]

Each query covers the cross-target pairs on which its outcomes differ. A fixed resolving bundle is therefore a weighted target-pair cover.

This connects the fixed side to established Set/Test Cover structure; the repository does **not** claim invention of those general covering methods.

### Certificate ladder

Strict gain can often be certified without first computing the exact numerical `C_F`:

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
- an LP-integrality-gap control has `C_A=2`, fractional lower bound 2, and `C_F=3`, so only the exact integer budget proof closes strict gain.

The integer proof is independently rechecked by `verify_fixed_budget_decision_certificate()`.

See:

- `theory/FIXED_BYPASS_PAIR_COVER.md`
- `theory/PAIR_PACKING_LOWER_BOUND.md`
- `theory/FRACTIONAL_PAIR_COVER_BOUND.md`
- `theory/INTEGER_FIXED_COVER_PROOF.md`

## Exact proof compression stack

The fixed-side proof now has semantics-preserving compression at several levels.

### Two-sided residual kernel

`cover_kernel.py` repeatedly applies exact reductions:

```text
inactive/unaffordable query deletion
pair-obligation dominance
unique-separator forcing
query dominance
```

After pair dominance, distinct nonempty separator signatures form an inclusion antichain over `m` queries, so Sperner's theorem gives

\[
\boxed{|P_K|\le {m\choose\lfloor m/2\rfloor}}.
\]

### Exact-state and isomorphism DAGs

`proof_dag.py` shares literal repeated residual states. `isomorphism_quotient.py` further forgets pair order and query names while preserving remaining budget, query costs, and pair-query incidence.

A six-world / six-query strict-gain control compresses

```text
4 label-specific residual states -> 2 weighted-incidence isomorphism classes.
```

`isomorphism_proof_dag.py` exports every shared edge with an explicit child-to-representative query bijection. Its verifier reconstructs each child and checks the transport directly rather than trusting a canonical-signature match.

### Certified symmetry handling

The current exact stack is

\[
\boxed{
\text{color refinement}
\to
\text{individualization-refinement}
\to
\text{exact automorphism audit}
\to
\text{stabilizer-orbit pruning}
}.
\]

A registered eight-query residual benchmark shrinks exact permutation enumeration from `720` candidates to `12` after color refinement. Regular adverse controls show why refinement alone is not an isomorphism test.

For a proof node `v`, `symmetry_pruned_proof_dag.py` keeps one recursive child per exact parent query-automorphism orbit. If

\[
g(q)=r,\qquad g\in\operatorname{Aut}(I_v),
\]

then

\[
\boxed{I_v\setminus q\cong I_v\setminus r}.
\]

Writing

\[
b(v)=\text{raw affordable branches},\qquad
o(v)=\text{orbit representatives},
\]

we get exact local saving

\[
\boxed{s(v)=b(v)-o(v)}
\]

and

\[
\boxed{1\le b(v)/o(v)\le |\operatorname{Aut}(I_v)|}.
\]

The C4 branch-symmetry control gives `2 -> 1` recursive branches with an explicit transport for the skipped branch.

See:

- `theory/FIXED_COVER_KERNELIZATION.md`
- `theory/PROOF_DAG_COMPRESSION.md`
- `theory/RESIDUAL_ISOMORPHISM_QUOTIENT.md`
- `theory/BIPARTITE_COLOR_REFINEMENT.md`
- `theory/SYMMETRY_REFINEMENT_AND_AUTOMORPHISMS.md`
- `theory/SYMMETRY_PRUNED_PROOF_DAG.md`

## Finite normal-form ladder

### 1. Unique minimal 4-world / 3-query core

Strict worst-path adaptive cost gain requires at least

```text
4 represented worlds
3 query identities
```

For

```text
4 worlds
T=(0,0,1,1)
3 labeled binary unit-cost queries
```

all `16^3 = 4,096` tasks are classified exactly:

| `(C_A,C_F)` | labeled tasks |
|---|---:|
| unresolved | 1,688 |
| `(1,1)` | 1,352 |
| `(2,2)` | 864 |
| **`(2,3)`** | **192** |

All 192 strict tasks collapse to one symmetry orbit with canonical separator signature

\[
\boxed{(3,5,9)}.
\]

Thus, in this declared scope,

\[
\boxed{C_A<C_F\iff \sigma=(3,5,9)}.
\]

The standard residual fixed-cover automorphism group is the full `S3`.

See `theory/MINIMAL_STRICT_GAIN_NORMAL_FORM.md`.

### 2. Adding a fourth query creates no new irreducible mechanism

For

```text
4 worlds
2+2 target multiplicity
4 binary unit-cost queries
```

all `16^4 = 65,536` labeled tasks were enumerated. There are 3,840 strict tasks, all with

\[
(C_A,C_F)=(2,3).
\]

Every strict task contains the unique three-query core after deleting at least one query. The only strict canonical signatures are

```text
(0,3,5,9)   null-query extension
(3,3,5,9)   duplicate-terminal extension
(3,5,9,9)   duplicate-routing extension
```

so increasing the query vocabulary from three to four does not create a new irreducible gain mechanism in this scope.

See `theory/FOUR_QUERY_EXTENSION_CLASSIFICATION.md`.

### 3. Five worlds create the first new deletion-minimal core

For

```text
5 worlds
2+3 target multiplicity
3 binary unit-cost queries
```

all `32^3 = 32,768` labeled tasks are classified exactly:

| `(C_A,C_F)` | labeled tasks |
|---|---:|
| unresolved | 17,928 |
| `(1,1)` | 5,768 |
| `(2,2)` | 6,336 |
| `(3,3)` | 720 |
| **`(2,3)`** | **2,016** |

The strict set has exactly five canonical separator signatures:

```text
(7,9,49)    288 tasks
(7,14,54)   288 tasks
(7,27,42)   576 tasks
(14,21,45)  576 tasks
(7,28,42)   288 tasks
```

Exactly 288 tasks lose strict gain after **every** one-world deletion. They all form one symmetry orbit with unique irreducible signature

\[
\boxed{(7,28,42)}.
\]

A standard representative is

\[
T=(0,0,1,1,1),
\]

\[
q_0=(0,1,1,1,1),\quad
q_1=(0,1,0,0,1),\quad
q_2=(0,1,0,1,0).
\]

An optimal adaptive policy uses two queries on every path, while singleton fixed-cover obligations force all three queries:

\[
\boxed{C_A=2<C_F=3}.
\]

Deleting any world removes strict gain; deleting any query leaves only two query identities and also removes strict gain. This is the first world/query deletion-minimal core after the four-world normal form.

Under uniform world weights an optimal root has **positive** direct target information,

\[
I(T;Q_{\rm root})\approx0.0199730940\text{ bits},
\]

so zero root information is not necessary even for deletion-minimal gain.

Most importantly, the four-world and five-world cores have different raw pair systems but the **same inclusion-minimal fixed kernel**:

\[
\boxed{(1,2,4)}.
\]

Therefore

\[
\boxed{
\text{same minimal fixed obstruction}
\not\Rightarrow
\text{same adaptive routing geometry}.
}
\]

This makes a complete adaptive-side invariant beyond target-pair cover a new central problem.

See `theory/FIVE_WORLD_IRREDUCIBLE_NORMAL_FORM.md`.

## Source-derived witnesses

For both registered MROD-style and PAYOFF-style routing abstractions:

```text
C_A = 2
C_F = C_U = U = 3
```

Under uniform represented worlds, the first routing observation has zero direct target information while the selected adaptive policy identifies the target completely. The best fixed information at budget 2 is 0.5 bit in both abstractions.

This demonstrates

```text
zero direct target information != zero decision relevance
```

but zero direct information is neither necessary nor sufficient for adaptive gain.

BALANCE supplies the negative control: under the current midpoint-reset span objective, supported branch labels change interval location but not the declared sufficient future-value state, so extra direction adaptivity has no gain at that step.

## Validation

The suite now includes:

- independent exact-oracle checks;
- the complete 4,096-task minimal universe;
- the complete 65,536-task four-query extension universe;
- the complete 32,768-task five-world universe;
- exact strict-signature and irreducibility iff classifiers;
- bypass controls and certificate gaps;
- tampered proof and transport rejection;
- two-sided kernel equivalence;
- exact-state and isomorphism DAG verification;
- color-refinement adverse controls;
- individualization-refinement class-equivalence regression;
- exact automorphism group and generator verification;
- stabilizer-orbit pruning;
- parent-automorphism branch pruning and proof-size accounting;
- fixed-kernel equality between the four- and five-world irreducible cores.

CI runs on Python 3.10, 3.11, and 3.12 plus executable witness and certificate-ladder audits.

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
  four_query_normal_form.py
  five_world_normal_form.py
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
  FOUR_QUERY_EXTENSION_CLASSIFICATION.md
  FIVE_WORLD_IRREDUCIBLE_NORMAL_FORM.md
  PROVENANCE.md
  OPEN_PROBLEMS.md
```

## Scope boundary

This repository does **not** claim:

- a new general theory of adaptive experimental design, Set Cover, Test Cover, graph isomorphism, color refinement, or group algorithms;
- that PAYOFF, MROD, and BALANCE are the same scientific model;
- that branch dependence alone is sufficient for adaptive gain;
- that zero direct target information is necessary or sufficient for gain;
- that failed lower-bound or quotient certificates imply no gain;
- polynomial-time exact integer cover or general graph canonicalization;
- that finite labeled-task counts are empirical prevalence estimates;
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
