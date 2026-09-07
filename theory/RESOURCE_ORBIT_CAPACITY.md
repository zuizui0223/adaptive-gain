# Resource automorphism does not license resource collapse

Exact query automorphisms are useful for canonicalization and proof-branch
pruning, but a symmetry orbit is **not** automatically one interchangeable
physical resource.

The unique minimal four-world strict-gain normal form is the smallest control.
Its fixed pair-cover incidence has full query automorphism group

\[
\operatorname{Aut}\cong S_3,
\qquad |\operatorname{Aut}|=6,
\]

and all three declared queries lie in one automorphism orbit.

Nevertheless every one of those three queries has a private cross-target pair for
which it is the only separator.  Therefore every fixed resolving bundle must buy
all three physical resources:

\[
\boxed{C_F=3.}
\]

The adaptive optimum is

\[
C_A=2.
\]

Thus

\[
\boxed{
q_1,q_2,q_3\text{ in one resource-symmetry orbit}
\not\Rightarrow
\text{one physical query token is sufficient}.
}
\]

## What symmetry does license

A certified automorphism may justify:

- canonical relabeling;
- exploring one representative of symmetric proof branches;
- reusing an isomorphic proof after supplying an explicit transport; and
- describing resources by orbit plus an exact transport structure.

It does **not** justify deleting orbit multiplicity when the fixed comparator may
need several orbit members simultaneously.

Any joint adaptive/fixed resource quotient using symmetry must therefore retain
at least enough information to represent **capacity / multiplicity of distinct
physical tokens** inside an orbit.

The regression test `test_resource_orbit_capacity.py` checks the complete `S3`
query orbit, exact private-pair essentiality of all three tokens, and `(C_A,C_F)=(2,3)`.

This result also sharpens the open problem for resource-labelled continuation:
we seek a quotient by resource symmetry **with capacity**, not a collapse of a
query orbit to one reusable action.
