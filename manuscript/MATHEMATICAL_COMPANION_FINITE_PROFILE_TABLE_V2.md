# Mathematical companion finite-profile table v2

Date: 2026-10-01
Status: corrected synthesis after the depth-five upper-bound audit. No new theorem is introduced here.

All rows assume finite deterministic target resolution with binary unit-cost queries that are globally exactly 50/50 balanced.

## 1. Sharp fixed-m ratio profiles

| worlds n | sharp maximum C_F/C_A by declared query count m | status |
|---:|---|---|
| 4 | 1 for all m | complete symmetry-reduced classification |
| 6 | 3/2 maximum | complete symmetry-reduced classification |
| 8 | m=1,2: 1; m=3,4: 3/2; m>=5: 5/3 | closed |
| 10 | m=1,2: 1; m=3,4: 3/2; m=5: 5/3; m>=6: 2 | closed |
| 12 | m=1,2: 1; m=3,4: 3/2; m=5: 5/3; m=6: 2; m>=7: 7/3 | closed |

The smallest exact-balanced binary scope with ratio strictly above 3/2 is

n=8, m=5, (C_A,C_F)=(3,5).

This differs from the unrestricted binary class, where the same ratio 5/3 is already possible at six worlds and five queries.

---

## 2. Balanced fixed-side cap

For even n:

max C_F =
- 1 at n=2;
- 2 at n=4;
- n-3 for every n>=6.

The sharp n>=6 witnesses use a private-pair forest with component sizes

(n/2-1, 2, n/2-1).

At equality, the two large components are stars.

---

## 3. Adaptive-depth-three envelope

Define

D_3(n)=max{C_F : C_A<=3}.

The exact values are:

| n | D_3(n) | status / feature |
|---:|---:|---|
| 6 | 3 | sharp |
| 8 | 5 | sharp; first exact-balanced ratio >3/2 |
| 10 | 6 | sharp; unique defect below min{7,n-3} |
| every even n>=12 | 7 | sharp; 12-world (3,7) witness pads upward |

Thus

D_3(n)=min{7,n-3}

for every even n>=6 except n=10.

---

## 4. Adaptive-depth-four envelope

Define

D_4(n)=max{C_F : C_A<=4}.

Closed near-ceiling values:

| n | D_4(n) | proof status |
|---:|---:|---|
| 12 | 8 | sharp |
| 14 | 10 | sharp |
| 16 | 12 | sharp |
| 18 | 13 | sharp |
| every even n>=20 | 15 | sharp; universal depth-four ceiling attained |

The 20-world witness has

(C_A,C_F)=(4,15)

with all fifteen queries exactly 10/10 balanced and all fifteen fixed-mandatory by query-unique cross-target private pairs.

---

## 5. Adaptive-depth-five rows

Define

D_5(n)=max{C_F : C_A<=5}.

The repository currently closes the following rows:

| n | D_5(n) | comparison with D_4 |
|---:|---:|---|
| 16 | 12 | no gain from the fifth adaptive level |
| 18 | 14 | one-unit recovery beyond D_4(18)=13 |
| 22 | 17 | sharp; C_F=19 and C_F=18 both excluded |

### n=16

The exact-balanced fixed cap is 13. Every cap-13 task is normalized to the star--edge--star minimum resolver plus at most three identity-safe external cuts. Mandatory-pair Bellman DP requires depth 7 in all eight safe-cut subsets, so C_F=13 is impossible at C_A<=5. The existing (4,12) witness gives

D_5(16)=12.

### n=18

The fixed cap is 15. Cap-15 plus any subset of the three identity-safe external balanced cuts requires depth 8 for the forced mandatory pairs, so C_F=15 is impossible at depth five. An explicit (5,14) task exists, hence

D_5(18)=14.

### n=22

The fixed cap is 19.

The upper audit:
- excludes C_F=19 using the normalized cap bundle and its three identity-safe external cuts;
- classifies all minimum 18-query private-pair forests into 60 non-isomorphic forms and 4,742 normalized matrices;
- excludes all 4,725 identifying matrices by fixed-safe external-query/basis-exchange analysis;
- reduces the 17 one-collision matrices to two isomorphism classes;
- exhausts safe-query automorphism orbits and 25,512 maximal pairwise-safe cliques in the hard collision class;
- finds zero depth-five survivors.

An explicit (5,17) witness exists. Therefore

D_5(22)=17.

The next recorded open finite row is D_5(24).

---

## 6. Asymptotic exact-balanced family

For routing depth d there are exact-balanced tasks with

C_F >= 2^d,
C_A <= d+1,

hence

C_F/C_A >= 2^d/(d+1) -> infinity.

This resolves an important apparent tension:

- exact balance imposes strong finite restrictions;
- exact balance does not produce a uniform adaptivity bound.

---

## 7. Paper-use classification

### Main text
Use:
- fixed cap n-3;
- star--edge--star equality structure;
- full D_3(n);
- compact D_4 frontier;
- asymptotic unbounded family.

### Supplement
Put:
- full n=4,6,8,10,12 fixed-m profiles;
- D_5(16), D_5(18), D_5(22) computational exclusion details;
- normalized search counts and certificate receipts.

### Do not claim
- a complete general D_h(n) formula;
- a complete exact-balanced fixed-(n,m) formula beyond the closed rows;
- that D_5(20) or D_5(24) is known unless separately proved;
- that uniform separating systems or adaptive search themselves are new.

## Source map

- theory/EXACT_BALANCED_BINARY_FIXED_COST_CAP.md
- theory/EXACT_BALANCED_BINARY_CAP_SATURATION_DEPTH.md
- theory/EXACT_BALANCED_BINARY_FINITE_THRESHOLD.md
- theory/EXACT_BALANCED_BINARY_EIGHT_WORLD_PROFILE.md
- theory/EXACT_BALANCED_BINARY_TEN_WORLD_PROFILE.md
- theory/EXACT_BALANCED_BINARY_TWELVE_WORLD_PROFILE.md
- theory/EXACT_BALANCED_BINARY_DEPTH_THREE_CAP.md
- theory/EXACT_BALANCED_BINARY_DEPTH_FOUR_CEILING.md
- theory/EXACT_BALANCED_BINARY_SIXTEEN_WORLD_DEPTH_FIVE_SHARP.md
- theory/EXACT_BALANCED_BINARY_EIGHTEEN_WORLD_DEPTH_FIVE_SHARP.md
- theory/EXACT_BALANCED_BINARY_TWENTY_TWO_WORLD_DEPTH_FIVE_UPPER.md
- theory/BALANCED_BINARY_UNBOUNDED_ADAPTIVE_GAIN.md

## Claim boundary

Analytic fixed-cap/equality results, closed finite envelopes, and constructive asymptotic results must remain separately labeled.

Computationally closed finite rows are exact only within their stated finite scopes. Non-discovery of a literature collision is not a proof of priority.
