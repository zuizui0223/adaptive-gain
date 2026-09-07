# Sharp query-count minima for internal and external bypass

Let `S` be the set of distinct physical query resources used anywhere in one
selected optimal adaptive resolving policy.  Write

```text
C_A = adaptive worst-path optimum
C_F = global fixed optimum
C_U = fixed optimum restricted to S
U   = c(S)
```

with positive query acquisition costs.  The standard containment is

\[
C_A\le C_F\le C_U\le U.
\]

## Lemma: a two-resource selected union has no bypass

If `|S|=1`, the selected policy uses that one query and `C_A=U`.

If `|S|=2`, one resource is the root.  If the second resource is genuinely part
of the selected union, it occurs below the root on at least one branch.  That
root-to-leaf path therefore pays both resource costs, so its cost is exactly
`U`.  No path can cost more than the union cost, hence again

\[
\boxed{C_A=U.}
\]

Combining with

\[
C_A\le C_F\le C_U\le U
\]

forces

\[
\boxed{C_A=C_F=C_U=U.}
\]

Therefore a selected policy union with at most two distinct queries has neither
internal union redundancy nor external shortcut discount.

## Internal bypass needs at least three declared queries

Positive internal redundancy means

\[
U-C_U>0.
\]

By the lemma this requires `|S|>=3`, hence at least three declared query
resources.  The registered `routing_bypass_control()` uses exactly three unit-cost
queries and has

\[
(C_A,C_F,C_U,U)=(2,2,2,3),
\]

so

\[
\boxed{\min |Q|\text{ for positive internal bypass}=3.}
\]

The bound is sharp and does not depend on unit costs; unit costs are used only by
the witness.

## External bypass needs at least four declared queries

Positive external shortcut discount means

\[
C_U-C_F>0.
\]

Again `|S|>=3` is necessary.  If the complete declared vocabulary has only three
queries, `|S|=3` leaves no outside resource at all, so an external shortcut is
impossible.  Hence at least four declared queries are necessary.

The registered `external_shortcut_control()` has exactly four unit-cost queries
and

\[
(C_A,C_F,C_U,U)=(2,2,3,3),
\]

so

\[
\boxed{\min |Q|\text{ for positive external bypass}=4.}
\]

## Relation to the productive frontier

The minimal-transversal theorem gives the same result structurally:

- internal redundancy requires the selected union `S` not to be an
  inclusion-minimal productive-frontier transversal;
- external discount requires a cheaper minimal transversal using at least one
  resource outside `S`.

The two-resource lemma shows that neither geometry can arise while the selected
adaptive union contains at most two resources.

## Validation

Executable checks include:

- all `15^2 x 2^2 = 900` two-query arbitrary-partition tasks on four balanced
  worlds with query costs in `{1,2}`: every resolved task has zero internal and
  external bypass;
- all `16^3 = 4096` balanced four-world / three-binary-unit-cost tasks: all
  `2408` resolved tasks have zero external shortcut;
- the three-query internal witness and four-query external witness attain the two
  lower bounds exactly.

The finite enumerations validate implementation behavior.  The lower bounds
follow from the containment argument above and are not inferred from the finite
counts.

## Claim boundary

The theorem concerns finite deterministic guaranteed target resolution with
positive acquisition costs and the query union of a selected optimal adaptive
policy.  It does not identify the minimum number of worlds needed for bypass,
nor does it extend automatically to stochastic observations, repeated sampling,
calibration-changing resources, or scientific report licensing.
