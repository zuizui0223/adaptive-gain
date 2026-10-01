# Adaptive target resolution under exactly balanced binary queries

Draft v0.1 — mathematical companion candidate

## Abstract

Adaptive and non-adaptive finite search are classical, as are separating systems with uniform block sizes. We study their intersection under a particularly strict constraint: every available binary query must divide the represented state set exactly in half. For a finite deterministic target-resolution problem, let (C_A) be the minimum worst-case number of adaptively chosen unit-cost queries and (C_F) the minimum size of a fixed query set that guarantees the same target resolution. Exact global balance imposes strong finite restrictions on (C_F). For even (n), the largest possible fixed cost is (n-3) for every (nge6), compared with the unrestricted binary cap (n-1). The proof converts private separation obligations into a forest and uses exact balance to exclude one- and two-component extremizers. Equality is rigid: a cap-saturating family has a star--edge--star private-pair spine, and when no extra queries are available its adaptive cost is at least (n/2-1). We then study the depth-constrained envelope (D_h(n)=max{C_F:C_Ale h}). The depth-three envelope is exact for all even (nge6), with a unique finite compatibility defect at (n=10); depth-four values are closed through the transition to the universal 15-query tree ceiling, and selected depth-five rows show further non-monotone recovery of fixed burden. Despite these strong finite effects, exact balance does not uniformly control adaptivity: there are exactly-balanced binary families with (C_F/C_Age2^d/(d+1)	oinfty). Thus perfect marginal balance constrains finite separation geometry without bounding the asymptotic value of contingent querying.

## 1. Introduction

A finite search problem can be asked in two extreme ways. In the adaptive version, the next query may depend on previous answers. In the non-adaptive version, all queries must be selected before any answer is observed. This distinction is classical in combinatorial search, decision-tree theory, Test Cover and related identification problems. More generally, (k)-round search interpolates between the two extremes by allowing batches of parallel questions.

A different classical restriction concerns the sizes of the query sets themselves. Separating-system theory asks for set families that distinguish elements or prescribed subsets, and uniform separating systems constrain each block to have the same cardinality. When the ground set has even size (n), an especially symmetric case requires each binary query to split the represented states exactly (n/2:n/2).

These two themes suggest a natural finite extremal question. Suppose every available question is globally perfectly balanced. How large can the cost of a fixed resolving set be if an adaptive strategy is shallow? Does perfect balance make adaptive and non-adaptive resolution comparable, or can branch-dependent querying remain arbitrarily valuable?

We study these questions in a deterministic target-resolution model. The target need not identify the hidden world itself: several represented states may share one target action. This is useful for applications in which the aim is classification or decision rather than full identification, while identity search remains a special case.

For a declared query vocabulary, let (C_A) be the minimum worst-case cost of an adaptive target-resolving decision tree and (C_F) the minimum cardinality of a fixed resolving query set. The inequality (C_Ale C_F) is immediate and is not our contribution. Nor do we claim novelty for adaptive versus non-adaptive search, binary decision trees, Test Cover, or the use of half-size blocks. Our focus is the extremal geometry created when these ingredients are imposed simultaneously.

The first result concerns the fixed side alone. In unrestricted binary target resolution, a minimum fixed resolver can contain as many as (n-1) essential queries. Under exact global balance, the sharp maximum drops to (n-3) for every even (nge6). The proof is graph-theoretic. Every query in a minimum resolver owns a private cross-target pair. Selecting one private pair per query yields a graph in which every selected edge is the unique edge of one query cut and is therefore a bridge. The graph is a forest. Exact balance then rules out the one- and two-component forests needed to attain (n-1) or (n-2) edges.

The equality case is rigid. An (n-3)-query balanced family forces the private-pair forest to consist of two stars of size (n/2-1) and one isolated edge. This star--edge--star normal form in turn forces high adaptive depth when the declared vocabulary consists only of the saturated fixed family.

This rigidity makes bounded adaptive depth nontrivial. Define
[
D_h(n)=max{C_F:C_Ale h}
]
over exact-balanced binary unit-cost tasks on (n) represented states. The generic bounds
[
C_Fle n-3,qquad C_Fle2^h-1
]
suggest the envelope (min{n-3,2^h-1}), but the two bounds need not be simultaneously attainable. At depth three there is exactly one finite defect after (n=6): (D_3(10)=6), although both generic bounds equal seven. At twelve worlds the full seven-query depth-three tree becomes feasible and remains feasible under balance-preserving padding. Higher depths exhibit analogous compatibility structure.

Finally, the finite penalties do not accumulate into an asymptotic bound. We give an exactly-balanced binary family in which fixed resolution must provision exponentially many branch-specific resources while adaptive resolution pays logarithmic routing cost plus one branch-specific terminal query. Consequently (C_F/C_A) is unbounded even though every individual query is perfectly balanced.

The resulting picture is deliberately narrower than general adaptivity-gap theory. Exact balance is a strong marginal constraint. It changes finite irredundance and forces specific extremal geometry, but marginal balance alone does not control contingent value.

## 2. Model

Let (W) be a finite set of represented worlds with (|W|=n). Each world (win W) has a target label (T(w)) in a finite target set.

A binary query (q) is a deterministic map
[
q:W	o{0,1}.
]

Throughout the main results, all query costs are one.

A query is **exact-balanced** when (n) is even and
[
|{w:q(w)=0}|=|{w:q(w)=1}|=n/2.
]

A fixed query set (S) resolves the target if every pair (x,y) with (T(x)
e T(y)) is separated by at least one (qin S). Let
[
C_F
]
be the minimum cardinality of such a fixed resolving set within the declared query vocabulary.

An adaptive policy is a binary decision tree whose internal nodes are labeled by declared queries. At a node, the observed query outcome selects the next subtree. Every terminal leaf must be target-pure. Let
[
C_A
]
be the minimum worst-case root-to-leaf query count.

Any fixed resolving set can be queried sequentially without using intermediate outcomes, hence
[
C_Ale C_F.
]

Our concern is not this containment but the extremal relation between the two costs under exact global balance.

## 3. Exact balance reduces the maximum fixed burden

### Theorem 1 — sharp exact-balanced fixed-cost cap

For even (n), over all finite target-resolution tasks with deterministic binary unit-cost exact-balanced queries,
[
max C_F=
egin{cases}
1,&n=2,\
2,&n=4,\
n-3,&nge6.
end{cases}
]

### Proof sketch

Let (B) be a minimum fixed resolver. For each (qin B), minimality implies that (Bsetminus{q}) fails to resolve the target. Therefore some cross-target pair ((x_q,y_q)) is separated by (q) and by no other member of (B). Call it a private pair for (q).

Construct a graph (G) on (W) with one selected private-pair edge (e_q={x_q,y_q}) for every (qin B). Query (q) separates (e_q), but no other selected edge. Hence the cut of (G) induced by (q) contains exactly one graph edge. That edge must be a bridge. Every edge of (G) is therefore a bridge, so (G) is a forest and
[
C_F=|E(G)|le n-1.
]

Exact balance removes the two top forest sizes.

If (C_F=n-1), then (G) is a tree. Consider a leaf edge. Removing it gives components of sizes (1) and (n-1). Because the query corresponding to the leaf edge crosses no other selected edge, each component must lie wholly on one side of the query cut. No exact (n/2:n/2) cut is possible.

If (C_F=n-2), then (G) has two components. If both are nontrivial, an edge in the smaller component leaves the larger component intact. Its size is at least (n/2), and exact balance is incompatible with also crossing the chosen edge. The only remaining form is an isolated vertex plus an ((n-1))-vertex tree, but a leaf edge of the large tree leaves a connected block of size (n-2>n/2) for (nge6), again impossible.

Thus (C_Fle n-3).

For (n=2hge6), equality is attained by a private-pair forest with three components of sizes
[
(h-1,2,h-1),
]
using a star, an edge, and a star. Each forest edge is assigned one exact-balanced query crossing only that edge. The resulting (n-3) queries can be made jointly resolving, and each is fixed-mandatory.

The cases (n=2,4) have separate sharp constructions.

## 4. Equality is rigid

The proof of Theorem 1 leaves open many possible three-component forests. Exact balance removes that freedom.

### Theorem 2 — star--edge--star saturation

Let (n=2hge8). Suppose the entire declared query family has (n-3) exact-balanced binary queries and every one is fixed-mandatory, so (C_F=n-3). Then, up to relabeling, the selected private-pair forest has component sizes
[
{h-1,2,h-1},
]
and both ((h-1))-vertex components are stars.

Moreover the balanced query rows are forced, up to outcome complementation, by the selected private edge.

### Proof sketch

Because the private-pair forest has (n) vertices and (n-3) edges, it has three components. Let their sizes be (ale ble c).

Take a leaf edge in a nontrivial component of size (s). Removing that edge leaves a singleton, a connected block of size (s-1), and the other two components intact. A query crossing only this edge must form an (h:h) partition from those unsplittable blocks. Applying this arithmetic constraint in each nontrivial component excludes isolated components and forces the multiset of component sizes to be
[
{2,h-1,h-1}.
]

Now take any edge in one of the ((h-1))-components. If it splits that component into sizes (r) and (h-1-r), the other intact components have sizes (2) and (h-1). Exact balance is possible only when (r=1) or (h-2). Hence every edge is a leaf edge and the component is a star.

This equality classification is the fixed-side structural backbone of the adaptive results.

### Corollary 2.1 — adaptive cost of the saturated bundle

Under the assumptions of Theorem 2,
[
C_Age h-1=n/2-1.
]

The bound is attained.

The key point is that the two star arms contain many private obligations. Whichever queries are asked before the middle-edge query, one branch must retain the unqueried obligations of one large star. The optimal worst-case schedule has depth (h-1).

Thus maximal exact-balanced fixed irredundance is incompatible with shallow adaptivity when no additional query resources are available.

## 5. Adaptive-depth envelopes

We now allow additional exact-balanced queries beyond a minimum fixed resolver.

For integer (hge1), define
[
D_h(n)=max{C_F:C_Ale h}.
]

Two immediate upper bounds are
[
D_h(n)le n-3
]
from Theorem 1, and
[
D_h(n)le2^h-1
]
by flattening a depth-(h) binary decision tree. These bounds need not be jointly attainable.

### Theorem 3 — complete depth-three envelope

For every even (nge6),
[
D_3(n)=
egin{cases}
3,&n=6,\
5,&n=8,\
6,&n=10,\
7,&nge12.
end{cases}
]

Thus
[
D_3(n)=min{7,n-3}
]
except at (n=10), where
[
D_3(10)=6.
]

The ten-world row is the first clear compatibility defect. Both generic bounds permit (C_F=7), but if (C_A=3) and (C_F=7), flattening forces a complete depth-three tree with seven distinct query labels. Fixed minimality then forces private edges throughout the tree. After normalizing the complete tree, exact 5/5 balance on the six non-root coordinates has no compatible realization. An exhaustive symmetry-reduced half-state calculation certifies the obstruction.

At twelve worlds, an explicit exact-6/6 seven-query task has ((C_A,C_F)=(3,7)). Adding complementary all-zero/all-one world pairs preserves exact balance and the same cost pair for every larger even (n).

### Higher adaptive depths

Depth four produces the sharp values
[
D_4(12)=8,quad
D_4(14)=10,quad
D_4(16)=12,quad
D_4(18)=13,
]
and
[
D_4(n)=15
]
for every even (nge20).

The twenty-world extremizer attains the complete binary-tree ceiling:
[
(C_A,C_F)=(4,15).
]

At depth five, currently closed rows include
[
D_5(16)=12,qquad
D_5(18)=14,qquad
D_5(22)=17.
]

These finite exclusions use exact enumeration only after substantial structural reduction. A hypothetical near-cap minimum resolver is normalized by its private-pair forest; external exact-balanced queries are restricted by the requirement that they not lower the fixed optimum; symmetry and automorphism reductions then reduce the remaining adaptive feasibility question to exact Bellman dynamic programming.

The values show that an extra adaptive level does not necessarily improve the extremum immediately: (D_5(16)=D_4(16)). At eighteen worlds the fifth level recovers one additional unit of fixed burden.

## 6. Fixed-query profiles at small world counts

The finite behavior can also be viewed at fixed (n) as the declared query count (m) increases.

For exactly-balanced binary tasks, the closed rows are:

[
n=4:quad 1,
]

[
n=6:quad max C_F/C_A=3/2,
]

[
n=8:quad
1,1,3/2,3/2,5/3,5/3,ldots,
]

[
n=10:quad
1,1,3/2,3/2,5/3,2,2,ldots,
]

and

[
n=12:quad
1,1,3/2,3/2,5/3,2,7/3,7/3,ldots.
]

The smallest exact-balanced binary task with ratio strictly greater than (3/2) therefore has eight worlds and five queries, with
[
(C_A,C_F)=(3,5).
]

These rows show that exact balance has a genuine finite effect. The balanced subclass is not obtained by simply inserting (n-3) into the unrestricted binary tree bound: compatibility between constant row weight and private-pair geometry creates exceptional finite scopes.

## 7. Perfect balance does not bound the asymptotic adaptivity gap

The finite restrictions might suggest that exact balance regularizes adaptive advantage. It does not.

### Theorem 4 — unbounded ratio under exact 50/50 balance

For every routing depth (dge1), there exists a finite deterministic binary unit-cost target-resolution task such that every declared query is exactly 50/50 balanced and
[
C_Fge2^d,qquad C_Ale d+1.
]

Therefore
[
rac{C_F}{C_A}
ge
rac{2^d}{d+1}
longrightarrowinfty.
]

### Construction idea

Create (2^d) target-mixed branch pairs. Routing queries encode the branch index. Each branch has a terminal query that is uniquely required to separate its target-mixed pair, but the terminal row is padded across other branches so that its global outcomes remain exactly balanced.

A fixed resolver must include all branch terminals. An adaptive policy first reads the (d) routing bits and then asks only the terminal query for the realized branch.

Thus exact marginal balance does not remove branch-exclusive separation obligations.

## 8. Discussion

The results separate three notions that are easy to conflate.

First, a query can be globally perfectly balanced while participating in a highly nonuniform conditional structure. Balance describes a one-query marginal. Adaptive value depends on which separation obligations remain relevant after earlier outcomes.

Second, fixed irredundance and adaptive depth are different geometric constraints. The exact-balanced fixed extremum is rigid: cap saturation forces star--edge--star structure and therefore large adaptive depth. A shallow adaptive policy can coexist with large (C_F) only when additional balanced queries reorganize the conditional geometry without creating a cheaper fixed resolver.

Third, finite regularization need not imply asymptotic regularization. Exact balance lowers the fixed cap and creates real finite compatibility defects, yet the adaptive/fixed ratio is still unbounded.

This combination suggests that the relevant object is neither marginal split quality nor raw query count alone, but the incidence geometry of branch-specific separation obligations.

Several problems remain open. The first is the complete sharp fixed-((n,m)) ratio in the exact-balanced subclass. The second is a general description of (D_h(n)) and its exceptional finite scopes. The third is to characterize when the generic upper envelope
[
min{n-3,2^h-1}
]
is attainable. Extensions to approximately balanced queries and to equal-part multiway queries would test which parts of the private-pair geometry survive beyond the binary half-split case.

## References

- Aigner, M. 1988. *Combinatorial Search*. Wiley.
- Chiarelli, J., Hatami, P. & Saks, M. 2020. An asymptotically tight bound on the number of relevant variables in a bounded degree Boolean function. *Combinatorica* 40:237–244. DOI: 10.1007/s00493-019-4136-7.
- Damaschke, P. 2019. Combinatorial search in two and more rounds. *Theoretical Computer Science* 780:1–11. DOI: 10.1016/j.tcs.2019.02.004.
- Katona, G. O. H. 1966. On separating systems of a finite set. *Journal of Combinatorial Theory* 1:174–194.
- Ling, A. C. H., Li, P. C. & van Rees, G. H. J. 2004. Splitting systems and separating systems. *Discrete Mathematics* 279:355–368. DOI: 10.1016/S0012-365X(03)00280-2.
- Wiener, G. 2009. Rounds in Combinatorial Search. *Dagstuhl Seminar Proceedings* 09281. DOI: 10.4230/DagSemProc.09281.6.

## Claim boundary

The manuscript does not claim novelty for adaptive search, non-adaptive separating systems, uniform separating systems, complete binary-tree counting, or generic adaptivity gaps.

The candidate contribution is the exact extremal theory developed here for the intersection of:
- finite deterministic target resolution;
- globally exact-balanced binary queries;
- fixed irredundance;
- bounded adaptive depth.

Priority remains subject to the dedicated literature audit in manuscript/MATHEMATICAL_COMPANION_PRIORITY_AUDIT_V3.md.
