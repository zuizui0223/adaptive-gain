# Fixed bypass as a target-pair cover problem

Status: exact finite deterministic theorem for the `adaptive-gain` abstraction. It does not replace source-repository scientific models.

## 1. Fixed resolution is a cross-target pair cover

For represented worlds `W` and target map `T`, define the cross-target pair set

\[
P_T=\{\{w_i,w_j\}:T(w_i)\ne T(w_j)\}.
\]

Each query `q` covers the pair when it separates the two declared outcomes:

\[
S_q=\{\{w_i,w_j\}\in P_T:o_q(w_i)\ne o_q(w_j)\}.
\]

A fixed query bundle resolves the target iff its separator sets cover every pair in `P_T`.

This is a target-specific pair-cover formulation. It is closely related to the classical Test Cover problem, where a smallest collection of tests is chosen to separate all relevant item pairs. The term `globally essential` below follows the same structural idea as an essential test: one test is the unique separator of at least one pair.

Prior-art boundary: Test Cover and essential-test algorithms are established. See de Bontridder, Lageweg, Lenstra, Orlin & Stougie (2002), *Branch-and-Bound Algorithms for the Test Cover Problem*, ESA 2002, LNCS 2461, 223–233, DOI `10.1007/3-540-45749-6_23`; and Crowston, Gutin, Jones, Saurabh & Yeo (2012), *Parameterized Study of the Test Cover Problem*, MFCS 2012, LNCS 7464, 283–295, DOI `10.1007/978-3-642-32589-2_27`.

`adaptive-gain` uses only cross-**target** pairs, not necessarily every pair of distinct represented worlds.

## 2. Refined bypass decomposition

Let

```text
C_A = minimum adaptive worst-path resolution cost,
C_F = global minimum fixed resolving cost,
U   = total cost of all distinct query identities used anywhere in the selected optimal adaptive tree,
C_U = minimum fixed resolving cost using only queries in that selected tree union.
```

Flattening the selected tree union is a valid fixed resolver, and restricting the fixed vocabulary cannot improve the global optimum. Therefore

\[
\boxed{C_A\le C_F\le C_U\le U}.
\]

Hence

\[
\boxed{
U-C_A
=(C_F-C_A)+(C_U-C_F)+(U-C_U)
}
\]

with nonnegative terms

```text
branch-exclusive overhead = U - C_A
realized adaptive gain     = C_F - C_A
external shortcut discount = C_U - C_F
internal union redundancy  = U - C_U.
```

The older aggregate bypass is

\[
U-C_F=(U-C_U)+(C_U-C_F).
\]

So an adaptive tree can lose potential gain in two different ways:

1. **internal redundancy**: a cheaper fixed subset already exists inside the tree's union;
2. **external shortcut**: the union is internally irreducible, but a cheaper fixed bundle uses at least one query outside that union.

This distinction matters experimentally. The first says the adaptive plan itself contains measurements that need not all be bought by a fixed design. The second says an entirely different measurement route bypasses the adaptive tree's branch-specific vocabulary.

Crucially, bypass is a **discount**, not a binary veto. It may consume all branch-exclusive overhead and eliminate strict gain, or only part of the overhead and leave a positive residual gain.

## 3. Private-pair no-bypass theorem

A query `q` has a globally private cross-target pair if there exists

\[
p\in P_T
\]

such that `q` separates `p` and no other declared query separates `p`.

Then every fixed resolving bundle must include `q`.

Let `Q_pi` be the selected adaptive tree's query union. If

1. `Q_pi` resolves the target when flattened; and
2. every query in `Q_pi` has a globally private cross-target pair,

then every fixed resolver must contain every query in `Q_pi`. Since `Q_pi` itself resolves,

\[
\boxed{C_F=U}.
\]

If additionally the adaptive tree has branch-exclusive overhead,

\[
U>C_A,
\]

then

\[
\boxed{C_A<C_F=U}
\]

without solving the global fixed optimization.

This is implemented by `selected_policy_private_pair_gain_certificate()`.

### Important asymmetry

The private-pair condition is **sufficient, not necessary**.

A fixed optimum can require the full selected union because of a combinatorial set-cover lower bound even when one union query has no pair for which it is individually the unique separator. The repository includes a five-world strict-gain control with exactly that behavior.

Therefore

```text
private-pair certificate fails
!=
fixed bypass exists.
```

## 4. Registered source-derived positive witnesses

For both the MROD-style and PAYOFF-style registered routing tasks,

```text
C_A = 2
C_F = 3
C_U = 3
U   = 3.
```

Thus

```text
internal redundancy = 0
external shortcut    = 0
realized gain        = 1.
```

Every query in the selected adaptive union has a globally private cross-target pair. The private-pair certificate therefore proves the no-bypass result directly.

For PAYOFF-style routing the private pairs can be read transparently:

```text
intrinsic_r_0.5   is uniquely needed for one low/high cross-phase pair,
interaction_d_0.2 is uniquely needed for one low-alpha cross-phase pair,
interaction_d_0.1 is uniquely needed for one high-alpha cross-phase pair.
```

The MROD deterministic nuisance-expanded witness has analogous private pairs for `context`, `assay0`, and `assay1`.

## 5. Two distinct no-gain bypass controls

### Internal redundancy

A branch-dependent routing control has

```text
C_A = 2
C_F = 2
C_U = 2
U   = 3.
```

So

```text
internal redundancy = 1
external shortcut    = 0
gain                 = 0.
```

The adaptive union itself contains a cheaper fixed resolving subset.

### External shortcut

A separate four-query control has

```text
C_A = 2
C_F = 2
C_U = 3
U   = 3.
```

So

```text
internal redundancy = 0
external shortcut    = 1
gain                 = 0.
```

Here the selected adaptive union is internally irreducible, but a fixed bundle using a query outside that union resolves at lower cost.

These two controls show that the old single quantity `fixed_bypass_discount` hides scientifically different failure modes.

## 6. Partial bypass can coexist with strict gain

The refined identity predicts a third possibility: bypass can remove only part of the overhead.

Two six-world unit-cost structural controls verify each channel separately.

### Partial internal discount

```text
C_A = 3
C_F = 4
C_U = 4
U   = 5
```

so

```text
overhead            = 2
internal redundancy = 1
external shortcut    = 0
realized gain        = 1.
```

The selected adaptive union contains one unit of fixed redundancy, yet the fixed optimum still costs one unit more than the adaptive worst path.

### Partial external discount

```text
C_A = 3
C_F = 4
C_U = 5
U   = 5
```

so

```text
overhead            = 2
internal redundancy = 0
external shortcut    = 1
realized gain        = 1.
```

The adaptive union is internally irreducible, but an outside query lets the global fixed class recover one unit. The remaining unit is still genuine adaptive gain.

Therefore neither statement is valid in general:

```text
bypass exists -> no adaptive gain
no bypass      -> necessary for adaptive gain.
```

The exact statement is only the additive decomposition.

## 7. Minimal-universe validation

For the exhaustively enumerated balanced universe

```text
4 worlds
binary target split 2+2
3 labeled binary unit-cost queries
```

there are 4096 labeled tasks and exactly 192 strict-gain tasks.

For this deliberately tiny universe, the selected-policy private-pair certificate identifies exactly those same 192 tasks and produces no false positives.

That finite completeness is **not** a general theorem. In larger vocabularies/world sets, strict gain can occur while the private-pair certificate is incomplete, and partial bypass can coexist with strict gain as above.

## 8. What remains open

The private-pair certificate is a cheap structural lower bound on fixed cost. The next stronger problem is to certify `C_F>=K` without exhaustively solving the weighted target-pair cover.

Possible routes include:

- packing lower bounds over cross-target pairs;
- weighted set-cover dual certificates;
- branch-generated cuts tied to an adaptive tree;
- continuous analogues where the cross-target set is an uncountable compatible parameter region.

These are not implemented or claimed here.
