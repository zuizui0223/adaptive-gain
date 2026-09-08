# Sharp exact-balanced fixed-cost envelope through adaptive depth three

Let

\[
D_3(n)
=
\max C_F
\]

where the maximum ranges over finite deterministic unit-cost tasks with exactly
`n` represented worlds, every query binary and globally exact 50/50 balanced,
and adaptive optimum

\[
C_A\le3.
\]

For even `n>=6`, the envelope is completely determined.

## Theorem

\[
\boxed{
D_3(n)
=
\begin{cases}
3, & n=6,\\
5, & n=8,\\
6, & n=10,\\
7, & n\ge12\text{ even}.
\end{cases}
}
\]

Equivalently,

\[
\boxed{
D_3(n)=\min\{7,n-3\}
}
\]

for every even `n>=6` **except `n=10`**, where the right-hand side equals seven
but the sharp value is six.

## Upper bounds

Two general theorems give

\[
C_F\le7
\]

whenever `C_A<=3`, because a binary depth-three tree has at most seven internal
query occurrences, and

\[
C_F\le n-3
\]

for every exact-balanced binary task on even `n>=6` worlds.

Hence

\[
D_3(n)\le\min\{7,n-3\}.
\]

This already closes `n=6` and `n=8` once witnesses are supplied, and caps every
`n>=12` at seven.

The sole unresolved intersection is `n=10`, where both generic bounds equal
seven.  The ten-world complete-depth-three compatibility theorem rules out
`(C_A,C_F)=(3,7)`: exact 5/5 balance on the six non-root queries is incompatible
with the private-edge conditions forced by fixed minimality.  Since `C_A<=2`
would itself imply `C_F<=3`, ten worlds obey

\[
D_3(10)\le6.
\]

## Sharp witnesses

The repository registers exact-balanced witnesses with cost pairs

\[
(2,3)\quad(n=6),
\]

\[
(3,5)\quad(n=8),
\]

\[
(3,6)\quad(n=10),
\]

and

\[
(3,7)\quad(n=12).
\]

The twelve-world witness pads by complementary all-zero/all-one world pairs to
every larger even world count, preserving both exact balance and the seven
original private cross-target pairs.  Thus `D_3(n)=7` for all even `n>=12`.

## Interpretation

At adaptive depth three, exact marginal balance creates exactly one finite
compatibility defect after `n=6`:

```text
n      6   8   10  12  14  16  ...
D3(n)  3   5    6   7   7   7  ...
```

The ten-world defect is therefore not evidence of an asymptotic reduction in
adaptive advantage.  It is the unique small-size failure of the two otherwise
sharp generic caps to be simultaneously saturable.

Consequently, the next unresolved balanced-binary compatibility layer begins at
**adaptive depth four**.  Depth three is closed.

## Reproducibility

Implementation:

- `adaptive_gain/balanced_binary_depth_three_cap.py`
- `tests/test_balanced_binary_depth_three_cap.py`
- `validation/balanced_binary_depth_three_cap.json`

The theorem reuses the independently registered six-, eight-, ten-, and
twelve-world witnesses, the sharp global exact-balanced fixed-cost cap, and the
ten-world exhaustive half-state obstruction.
