# Local replacement certificate for zero external shortcut

Let `H` be the productive-frontier hypergraph and let `S` be the query union of
one selected optimal adaptive policy.  The exact external shortcut discount is

\[
C_U-C_F,
\]

where `C_U` is minimum hitting-set cost restricted to `S` and `C_F` is the global
minimum hitting-set cost.

Exact minimal-transversal enumeration decides this quantity, but a shorter
sufficient certificate is possible.

## Set-valued replacement theorem

For every outside resource

\[
q\in Q\setminus S,
\]

suppose there exists an inside replacement set

\[
R_q\subseteq S
\]

such that

\[
c(R_q)\le c(q)
\]

and every productive-frontier edge hit by `q` is also hit by `R_q`:

\[
q\in E\in H
\Longrightarrow
R_q\cap E\ne\varnothing.
\]

Then

\[
\boxed{C_F=C_U.}
\]

### Proof

Take any global hitting set `B`.  For every outside `q in B`, replace `q` by
`R_q`.  Edge coverage is preserved: any edge whose coverage relied on `q` is hit
by `R_q`, while edges hit by other members remain hit.  Cost does not increase
because `c(R_q)<=c(q)`.  Repeating this for all outside resources yields a hitting
set contained in `S` with cost no greater than `c(B)`.

Applying the transformation to a global optimum gives

\[
C_U\le C_F.
\]

The reverse inequality `C_F<=C_U` is automatic because the restricted class is a
subset of the global fixed class.  Hence equality holds. QED.

## Why this is stronger than pairwise dominance

`R_q` may contain several inside resources.  For example, with frontier edges

```text
{a,x}
{b,x}
```

and costs

```text
c(a)=1, c(b)=1, c(x)=2,
```

neither `a` nor `b` alone replaces outside resource `x`, but `{a,b}` does at equal
cost.  Thus the theorem strictly extends one-query coverage dominance.

## Executable certificate

`adaptive_gain/frontier_bypass_certificates.py` provides:

- `frontier_replacement_certificate(...)` for a declared frontier and policy
  union;
- `selected_policy_no_external_shortcut_certificate(...)` for a finite task;
- `verify_frontier_replacement_certificate(...)` for direct independent checking
  of every stored replacement against frontier incidence and costs.

The search is exact over subsets of the selected union and fail-closed behind a
hard subset cap.

Regression includes the registered internal/external bypass controls and the
complete balanced four-world / three-binary-query universe.  A successful
certificate must never coexist with positive external shortcut discount.

## Claim boundary

This is a sufficient certificate, not a necessary characterization.  Failure to
find a replacement means only `certificate_not_obtained`; it does not imply that
an external shortcut exists.  Exact presence/absence remains characterized by
the minimal-transversal theorem.
