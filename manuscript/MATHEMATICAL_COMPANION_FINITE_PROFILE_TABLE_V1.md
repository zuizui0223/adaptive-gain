# Mathematical companion finite-profile table v1

Date: 2026-10-01  
Status: synthesis of existing exact-balanced binary validation results for the mathematical companion. No new theorem is introduced here.

## A. Closed sharp fixed-m profiles for small even world counts

All rows below assume:
- finite deterministic target resolution;
- binary unit-cost queries;
- every declared query exactly 50/50 balanced over represented worlds.

| worlds n | sharp maximum ratio by declared query count m | strongest registered witness / cap | proof status |
|---:|---|---|---|
| 4 | maximum ratio = 1 | complete symmetry-reduced scan | closed by exhaustive classification |
| 6 | maximum ratio = 3/2 | (C_A,C_F)=(2,3) | closed by exhaustive classification |
| 8 | m=1,2: 1; m=3,4: 3/2; m>=5: 5/3 | (3,5); global C_F<=5 | closed; 1,623,160 six-cut families checked for irredundancy cap |
| 10 | m=1,2: 1; m=3,4: 3/2; m=5: 5/3; m>=6: 2 | (3,6); (3,7) impossible | closed; exhaustive canonical depth-three compatibility obstruction |
| 12 | m=1,2: 1; m=3,4: 3/2; m=5: 5/3; m=6: 2; m>=7: 7/3 | (3,7) | closed; exact solver + sharp fixed-cost cap |

### Immediate finite threshold

The smallest exactly-balanced binary scope with ratio strictly above 3/2 is:

\[
\boxed{n=8,\quad m=5,\quad (C_A,C_F)=(3,5).}
\]

For comparison, the unrestricted binary class reaches ratio 5/3 already at six worlds and five queries.

---

## B. Sharp fixed-cost envelope at adaptive depth at most three

Define

\[
D_3(n)=\max\{C_F:C_A\le3\}
\]

inside the exactly-balanced binary subclass.

For even \(n\ge6\),

\[
\boxed{
D_3(n)=
\begin{cases}
3,&n=6,\\
5,&n=8,\\
6,&n=10,\\
7,&n\ge12.
\end{cases}}
\]

Equivalently,

\[
D_3(n)=\min\{7,n-3\}
\]

except at \(n=10\), where the generic upper bounds both equal 7 but the sharp value is 6.

| n | sharp D3(n) | witness | special feature |
|---:|---:|---|---|
| 6 | 3 | (2,3) | depth-two witness already sharp |
| 8 | 5 | (3,5) | first balanced ratio >3/2 |
| 10 | 6 | (3,6) | unique small-size compatibility defect: (3,7) impossible |
| 12 | 7 | (3,7) | full binary depth-three flattening ceiling becomes attainable |
| every even n>=12 | 7 | padded 12-world witness | complementary all-zero/all-one padding preserves balance |

This is the cleanest finite-size story in the balanced subclass.

---

## C. Sharp depth-four envelope near saturation

Define

\[
D_4(n)=\max\{C_F:C_A\le4\}.
\]

A depth-four binary tree gives the universal flattening ceiling

\[
D_4(n)\le15.
\]

The existing exact-balanced results close the near-ceiling frontier:

| n | sharp D4(n) | status |
|---:|---:|---|
| 12 | 8 | closed |
| 14 | 10 | closed |
| 16 | 12 | closed |
| 18 | 13 | closed; C_F=14 ruled out |
| every even n>=20 | 15 | closed; explicit 20-world (4,15) witness plus balance-preserving padding |

At 20 worlds the full complete-depth-four flattening ceiling is attained:

\[
\boxed{(C_A,C_F)=(4,15).}
\]

The 20-world witness uses all fifteen labels exactly once in a complete depth-four policy and has a query-unique cross-target private pair for each fixed-mandatory query.

---

## D. First registered depth-five lower layer

At 22 worlds there is an exactly-balanced binary witness with

\[
\boxed{(C_A,C_F)=(5,17).}
\]

Thus, for

\[
D_5(n)=\max\{C_F:C_A\le5\},
\]

the repository currently certifies

\[
D_5(22)\ge17
\]

and the same lower bound for every even \(n\ge22\) by complementary padding.

This is currently a **lower-bound construction**, not a claimed sharp depth-five envelope.

---

## E. Asymptotic balanced family

Independently of the finite sharp profiles, for routing depth d the repository constructs exactly-balanced binary tasks satisfying

\[
C_F\ge2^d,
\qquad
C_A\le d+1,
\]

hence

\[
\boxed{
\frac{C_F}{C_A}
\ge
\frac{2^d}{d+1}
\to\infty.
}
\]

The finite-profile results therefore describe a real small-size penalty from exact balance, while the asymptotic theorem shows that the penalty cannot uniformly bound adaptivity.

---

## F. How this table should appear in the companion

Main text:
- only the n=4,6,8,10,12 ratio rows;
- the compact D3 sequence;
- the 20-world (4,15) saturation as one later illustration if space permits.

Supplement:
- D4 details;
- 22-world depth-five lower construction;
- full witness signatures and certificate receipts.

The paper should not advertise every finite row as an independent theorem. Their role is to demonstrate that:
1. the exact general bounds are attained in identifiable regimes;
2. exact balance creates genuine finite compatibility effects;
3. those effects disappear asymptotically.

## Source map

- `theory/EXACT_BALANCED_BINARY_FINITE_THRESHOLD.md`
- `theory/EXACT_BALANCED_BINARY_EIGHT_WORLD_PROFILE.md`
- `theory/EXACT_BALANCED_BINARY_TEN_WORLD_PROFILE.md`
- `theory/EXACT_BALANCED_BINARY_TWELVE_WORLD_PROFILE.md`
- `theory/EXACT_BALANCED_BINARY_DEPTH_THREE_CAP.md`
- `theory/EXACT_BALANCED_BINARY_DEPTH_FOUR_CEILING.md`
- `validation/balanced_binary_small_scope.json`
- `validation/balanced_binary_eight_world_profile.json`
- `validation/balanced_binary_eighteen_world_depth_four_lower.json`
- `validation/balanced_binary_twenty_two_world_depth_five.json`

## Claim boundary

Closed finite rows are exact within their declared scope. The asymptotic family is an existence/unboundedness result. The depth-five 22-world result is currently only a lower bound. Do not interpolate an unproved general exact-balanced fixed-(n,m) formula from these rows.
