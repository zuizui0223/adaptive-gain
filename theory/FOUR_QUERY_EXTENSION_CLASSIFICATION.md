# Complete four-query extension classification

Status: exact finite exhaustive theorem for the declared deterministic scope

```text
4 represented worlds
binary target multiplicity 2+2
4 labeled binary-or-constant unit-cost queries
```

This is a structural classification result. The raw task counts are not empirical
prevalence estimates.

## 1. Question

The three-query balanced universe has a unique strict-gain normal form. The next
question is whether adding a fourth query creates a genuinely new irreducible
adaptive-gain mechanism.

It does not, in this declared scope.

## 2. Complete cost classification

There are

\[
16^4=65{,}536
\]

labeled four-query outcome maps. Exhaustive exact adaptive/fixed optimization
returns:

| `(C_A,C_F)` | Count |
|---|---:|
| unresolved | 14,896 |
| `(1,1)` | 27,120 |
| `(2,2)` | 19,680 |
| `(2,3)` | **3,840** |

There are no cases with `C_F=4`, no strict cases with `C_A>2`, and therefore

\[
\boxed{\max_{\rm strict} C_F/C_A=3/2}.
\]

The extra query increases the number of labeled strict tasks but does not increase
the attainable strict cost ratio.

## 3. Exact iff signatures

Quotient target-equivalence-preserving world permutations and query order, and
represent each query by its four-bit cross-target separator mask. Strict gain
occurs iff the canonical four-query separator signature is one of exactly three
values:

\[
\boxed{
\begin{aligned}
(0,3,5,9) &\quad\text{null-query extension},\\
(3,3,5,9) &\quad\text{duplicate-terminal extension},\\
(3,5,9,9) &\quad\text{duplicate-routing extension}.
\end{aligned}}
\]

Across all 65,536 tasks, this three-signature classifier has zero disagreement
with the exact `C_A<C_F` optimizer.

## 4. Why these are extensions of the minimal normal form

The unique three-query strict-gain separator signature is

\[
(3,5,9).
\]

Each four-query strict signature is obtained by adding exactly one redundant
query type:

1. `0`: a constant/null query that separates no cross-target pair;
2. a duplicate of a terminal-resolution query (`3` or its world-symmetric mate
   `5`); or
3. a duplicate of the routing query (`9`).

Thus every strict four-query task has a deletion minor equal to the unique
three-query strict-gain normal form.

More strongly, exhaustive deletion auditing gives:

| Strict extension class | Labeled tasks | Strict 3-query deletions |
|---|---:|---:|
| null query | 1,536 | 1 each |
| duplicate terminal | 1,536 | 2 each |
| duplicate routing | 768 | 2 each |

Overall,

```text
1 strict deletion: 1,536 tasks
2 strict deletions: 2,304 tasks
```

and zero strict four-query tasks have no strict three-query deletion.

Therefore

\[
\boxed{
\text{every strict 4-query task is reducible to the unique strict 3-query core}
}
\]

within this finite scope.

## 5. Terminal duplication and routing duplication are not the same task orbit

At the fixed pair-cover level the minimal three-query normal form has full query
`S_3` automorphism. But the full adaptive world/query decision structure
distinguishes the routing query from the two terminal queries:

- the routing query creates the mixed branches that determine which terminal
  query is useful next;
- a terminal query resolves only one routed branch directly.

Consequently duplicating a terminal query and duplicating the routing query are
separate four-query task orbits, even though the three queries are symmetric in
the flattened fixed pair-cover incidence.

This is another reminder that

\[
\boxed{
\text{fixed-cover automorphism}\neq\text{full adaptive-task automorphism}
}
\]

in general.

## 6. Raw strict counts by extension class

The complete strict set has

\[
3{,}840=1{,}536+1{,}536+768
\]

labeled tasks:

```text
null_query_extension          1536
duplicate_terminal_extension  1536
duplicate_routing_extension    768
```

These are finite labeled counts under the declared query/world conventions, not
empirical probabilities.

## 7. Consequence for the next search frontier

No new irreducible mechanism appears merely by moving from three to four binary
queries while keeping four balanced worlds and unit costs. A genuinely new
normal form therefore requires changing at least one structural dimension, for
example:

- more represented worlds;
- unequal query costs;
- more than two query outcomes;
- more target labels; or
- a larger query vocabulary whose strict task has no strict three-query deletion.

The repository should search those dimensions rather than treating four-query
raw strict counts as evidence of a new mechanism.

## 8. Implementation

`adaptive_gain/four_query_normal_form.py` provides:

- `canonical_four_query_separator_signature()`;
- `four_query_normal_form_receipt()`;
- `enumerate_balanced_four_query_universe()`; and
- the three exact registered strict-extension signatures.

The exhaustive scan compares the three-signature classifier against the exact
adaptive/fixed solver on every one of the 65,536 labeled tasks and records any
classification disagreement explicitly.

## Reproduce

```bash
python -m pytest -q tests/test_four_query_normal_form.py
```
