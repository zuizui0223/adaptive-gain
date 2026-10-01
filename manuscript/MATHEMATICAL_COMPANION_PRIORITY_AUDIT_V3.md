# Mathematical companion priority audit v3 — pivot to exact-balanced binary geometry

Date: 2026-10-01
Status: revised after deeper combinatorial-search, Boolean-function, and uniform-separating-system audit.
This file does not modify the frozen Evolution Letters V5 submission surface.

## Executive decision

The companion should **not** be organized around generic adaptive-versus-fixed search.

That comparison is classical:
- separating systems / Test Cover describe non-adaptive identification;
- combinatorial search on the same test hypergraph describes adaptive and k-round identification;
- read-once decision trees already realize the classical 2^d-1 internal-node/relevant-variable geometry.

The strongest mathematically distinctive line in this repository is instead:

> **finite adaptive target resolution when every available binary query is globally exactly balanced.**

This restriction has classical neighbors — especially uniform separating systems, where every block has size n/2 — but the targeted audit has not located a predecessor for the repository's combined extremal questions:
- maximum irredundant/fixed burden under exact balance;
- equality structure of a cap-saturating balanced family;
- interaction between that fixed burden and bounded adaptive depth;
- finite compatibility defects in D_h(n);
- unbounded adaptive/fixed ratio despite every query being exactly 50/50.

This is now the recommended companion-paper identity.

No categorical priority claim is licensed. The status remains:
**no exact predecessor located in the targeted search so far.**

---

## 1. Strong prior-art boundary

### 1.1 Adaptive versus non-adaptive combinatorial search is classical

G. Wiener, *Rounds in Combinatorial Search* (Dagstuhl Seminar Proceedings, 2009, DOI 10.4230/DagSemProc.09281.6) defines, for one separating system, k-round complexity c_k(H), with 1-round = non-adaptive and fully sequential = adaptive complexity.

P. Damaschke, *Combinatorial search in two and more rounds* (Theoretical Computer Science 780, 2019, DOI 10.1016/j.tcs.2019.02.004) studies the same general hypergraph search model and explicitly connects the one-round case with Test Cover.

Therefore:
- do not claim novelty for putting adaptive and non-adaptive costs on one finite query system;
- do not claim novelty for generic adaptivity gaps;
- do not market C_A<=C_F or flattening as new.

### 1.2 The 2^d-1 complete binary-tree geometry is classical

A depth-d read-once binary decision tree can depend on 2^d-1 distinct variables. Chiarelli, Hatami & Saks (Combinatorica 40, 2020, DOI 10.1007/s00493-019-4136-7) explicitly cite this classical lower construction.

Therefore the generic repository inequality

C_F <= 2^(C_A)-1

and threshold/read-once attainment should be treated as standard tree geometry, not as a standalone mathematical novelty claim.

This materially downgrades the generic sharp fixed-(n,m) ratio as a companion headline. Its closed form remains useful, but it is best presented as baseline geometry against which the exact-balanced subclass deviates.

### 1.3 Exact half-size blocks are classical as uniform separating systems

Ling, Li & van Rees, *Splitting systems and separating systems* (Discrete Mathematics 279, 2004, DOI 10.1016/S0012-365X(03)00280-2) define uniform separating systems using blocks of size exactly m/2.

Thus:
- the phrase "every binary query is exactly 50/50 balanced" is not by itself a new combinatorial constraint;
- the companion must connect explicitly to uniform separating-system literature.

However, the classical uniform-separating objective is typically the **minimum number of balanced blocks needed when blocks may be chosen from the full allowed class**. The repository asks a different extremal question about a declared query vocabulary and, in particular, how large an irredundant/minimum fixed burden can coexist with low adaptive depth.

### 1.4 Dedicated collision search for irredundant uniform separating families

Targeted searches for:
- irredundant uniform separating system;
- maximum irredundant balanced separating family;
- balanced cuts with private pairs;
- uniform separating systems with adaptive search;

did not locate the exact n-3 cap, star--edge--star equality classification, or the D_h(n) depth-vs-fixed-cost sequence below.

This is not a priority proof. It identifies the correct remaining audit target.

---

## 2. Headline theorem A — sharp fixed-side cap under exact balance

Repository theorem: theory/EXACT_BALANCED_BINARY_FIXED_COST_CAP.md

For even n, binary unit-cost queries with every query exactly n/2:n/2 balanced satisfy

max C_F =
- 1 for n=2;
- 2 for n=4;
- n-3 for every even n>=6.

The maximum is over arbitrary declared balanced query vocabularies and arbitrary target partitions.

### Proof mechanism

A minimum fixed resolver supplies one private cross-target pair for every mandatory query.

Selecting one such pair per query produces a graph G:
- query q crosses its own selected edge;
- it crosses no other selected edge;
- hence its edge is the unique edge of a graph cut;
- therefore every selected edge is a bridge;
- G is a forest.

Without balance this gives the ordinary n-1 forest cap.

Exact n/2:n/2 balance rules out:
- a one-component tree extremizer (n-1);
- a two-component forest extremizer (n-2);

for even n>=6, leaving C_F<=n-3.

The star--edge--star construction with component sizes

(n/2-1, 2, n/2-1)

attains equality.

### Why this is now a stronger companion candidate than the generic ratio formula

It is a genuine extremal consequence of the uniform/balanced constraint rather than generic decision-tree counting.

The theorem also supplies the structural normal form used by the later adaptive-depth results.

### Priority status

**High-priority audit target.**
No exact collision located so far.

Search next in:
- irredundant uniform separating systems;
- maximal minimal separating families;
- separating matrices with constant row weight;
- private-pair methods for uniform test systems.

---

## 3. Headline theorem B — equality forces a canonical star--edge--star spine

Repository theorem: theory/EXACT_BALANCED_BINARY_CAP_SATURATION_DEPTH.md

For n=2h>=8, if the declared exact-balanced family itself has n-3 queries and C_F=n-3, then the private-pair forest is forced, up to relabeling, to have component sizes

{2,h-1,h-1}

and the two (h-1)-components must be stars.

Thus cap saturation has a canonical

**star -- edge -- star**

private-pair geometry.

Moreover, inside that saturated bundle,

C_A >= h-1 = n/2-1,

and equality is attainable.

### Mathematical significance

This is stronger than merely giving the maximum C_F.

It classifies the equality structure and shows that **maximizing fixed irredundance under perfect balance is intrinsically adaptively difficult** if no extra queries are available.

This creates a nontrivial tension:
- cap-saturating fixed structure wants star--edge--star;
- small adaptive depth wants a richer balanced query vocabulary;
- extra queries can lower C_A only if they preserve the fixed minimum.

That tension is exactly what generates the finite compatibility defects below.

### Priority status

**Very strong audit target.**
No equivalent equality classification was found in the targeted uniform-separating searches.

---

## 4. Headline theorem family C — balanced adaptive-depth envelopes

Define

D_h(n) = max{ C_F : C_A <= h }

inside the exact-balanced binary unit-cost subclass.

This is the natural object for the companion.

It asks:

> with all questions globally balanced, how much non-adaptive/fixed burden can coexist with an adaptive worst-case depth at most h?

### Depth three — fully closed

For every even n>=6:

D_3(6)=3,
D_3(8)=5,
D_3(10)=6,
and D_3(n)=7 for all even n>=12.

Equivalently,

D_3(n)=min{7,n-3}

except for the single compatibility defect

D_3(10)=6<7.

At n=10, the ordinary tree ceiling and the exact-balanced fixed cap both permit seven, but exact balance plus the private-edge geometry makes (C_A,C_F)=(3,7) impossible.

At n=12, (3,7) becomes attainable again and pads to every larger even n.

### Depth four — near-saturation frontier closed

The repository proves:

D_4(12)=8,
D_4(14)=10,
D_4(16)=12,
D_4(18)=13,

and

D_4(n)=15 for every even n>=20.

At 20 worlds an explicit exact-balanced task attains (C_A,C_F)=(4,15), the full complete-depth-four flattening ceiling.

### Depth five — selected sharp rows

The deeper finite analysis gives:

D_5(16)=12,
D_5(18)=14,
D_5(22)=17.

The 22-world upper proof excludes both C_F=19 and C_F=18 using:
- normalized minimum-resolver forest types;
- identity-safe external cuts;
- basis-exchange constraints;
- automorphism orbits;
- exact Bellman feasibility.

The next registered open finite point is D_5(24).

### Why this family is compelling

The generic upper envelope

C_F <= min{m,n-3,2^h-1}

is simple.

The exact-balanced theory is interesting precisely because **the obvious upper bounds are sometimes jointly unattainable**.

The exceptional rows are not numerical noise: they arise from compatibility between:
- constant row weight;
- private-pair forest geometry;
- fixed minimality;
- adaptive leaf partitions.

That is a genuine finite extremal phenomenon.

---

## 5. Headline theorem D — balance suppresses finite extrema but not asymptotic adaptivity

Repository theorem: theory/BALANCED_BINARY_UNBOUNDED_ADAPTIVE_GAIN.md

There exists a family with:
- finite represented worlds;
- deterministic binary unit-cost queries;
- every query globally exactly 50/50 balanced;
- guaranteed target resolution;

yet

C_F >= 2^d,
C_A <= d+1,

so

C_F/C_A >= 2^d/(d+1) -> infinity.

### Role in the paper

This is the asymptotic capstone, not an isolated adaptivity-gap claim.

The finite theory shows that exact balance can genuinely suppress small-instance extrema.

The asymptotic theorem shows that such suppression does **not** become a uniform approximation guarantee:

> perfect global marginal balance does not bound contingent value.

Thus the paper has a clean finite-to-asymptotic arc:

uniform balance -> strong finite structural restrictions,

but

uniform balance does not imply a bounded adaptive/fixed ratio.

---

## 6. Results to demote from mathematical headline status

### Generic sharp fixed-(n,m) ratio

Keep as a baseline proposition, not the lead theorem. Its main ingredients are too close to classical complete binary-tree and read-once geometry.

Its value in the balanced paper is as the unrestricted comparison envelope.

### Prescribed-gap inverse architecture

Keep as a corollary or separate note, not the companion's headline.

It is useful for V5's ecological reverse inference, but mathematically it is largely an inversion of the same extremal tree bounds.

### Kernels and certificates

Use as proof/algorithm infrastructure only:
- target-relevant quotient;
- query dominance;
- pair-cover representation;
- private-pair / LP / integer certificates.

Do not claim generic reduction or LP novelty.

### Dynamical and spectral results

Exclude from this mathematical companion.
They belong to the ecological paper or archive.

---

## 7. Revised paper identity

Recommended title:

**Adaptive target resolution under exactly balanced binary queries**

Alternatives:

- **Exact-balanced query systems: fixed separation and adaptive depth**
- **Balanced finite search: irredundance, adaptive depth and extremal gaps**

Recommended central question:

> How does the requirement that every available binary question split the represented state space exactly in half constrain fixed separation, adaptive depth, and the gap between them?

---

## 8. Proposed theorem order

1. Balanced fixed-side cap: max C_F=n-3.
2. Equality classification: cap saturation forces star--edge--star.
3. Adaptive consequence: saturated bundle requires C_A>=n/2-1.
4. Depth-three exact envelope: full D_3(n), including the unique n=10 defect.
5. Higher-depth finite frontier: D_4 near/full saturation and selected D_5 sharp rows.
6. Asymptotic counterpoint: exact 50/50 balance still permits unbounded C_F/C_A.

This is one coherent theorem family, not six unrelated claims.

---

## 9. Remaining priority work

Before submission:

- [ ] search Katona/Aigner monographs for maximum-cardinality irredundant uniform separating families, not only minimum-size uniform separating systems;
- [ ] search constant-row-weight separating matrices for an n-3 maximal-minimal theorem;
- [ ] search equality cases for uniform separating systems for the star--edge--star normal form;
- [ ] search restricted-question Twenty Questions / combinatorial search for D_h(n)-type exact envelopes under global half-size constraints;
- [ ] search balanced decision-tree literature for finite exceptions analogous to D_3(10);
- [ ] if no collision is found, phrase novelty as an exact extremal theory for the balanced subclass, never as discovery of adaptive search or uniform separating systems.

## Stop rule

**Do not add another theorem family.**
The task is now:
1. close the prior-art boundary for the exact-balanced family;
2. correct the synthesis tables;
3. draft the companion around the balanced finite-to-asymptotic story.
