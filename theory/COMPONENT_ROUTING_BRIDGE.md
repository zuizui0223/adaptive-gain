# Prospective component-routing bridge

Status: side-theory development on `theory/reachability-admissibility-synthesis`.

This note introduces an explicit **new bridge axiom** between a heritable coupling topology and a finite sensing task. It is not read back into PAYOFF as if it had already been present there, and it is not part of the frozen Theoretical Ecology submission.

## 1. Why a new bridge axiom is needed

`TOPOLOGY_ONLY_BRIDGE_NONIDENTIFIABILITY.md` proves the negative result that a bare PAYOFF topology does not determine the adaptive/fixed sensing gap. The missing information includes represented worlds, target distinctions, cue resources, cue outcomes, costs, and physical availability/dependency rules.

`TOPOLOGY_SENSING_SUFFICIENT_KERNEL.md` then shows that a full finite task is more than is needed. It is enough for a biological bridge to generate both:

```text
K_A(T)      = an adaptive continuation object sufficient for C_A(T),
H_min(T)    = a minimal productive frontier sufficient for C_F(T),
resource costs.
```

The correct next move is therefore not to pretend that topology alone already encodes sensing. It is to declare one biologically interpretable generative rule and ask what exact joint kernel it induces.

---

## 2. Component-addressability axiom

Let a candidate heritable architecture be an undirected coupling topology

```text
T=(V,E).
```

Declare:

1. each node is a fitness-relevant functional unit;
2. nodes in one connected component share one jointly controlled functional module;
3. different connected components are independently addressable modules;
4. a coarse ecological context cue identifies which module is currently relevant;
5. once the relevant module is known, one module-specific terminal cue resolves the local binary target;
6. all cue acquisitions have unit cost.

Call this prospective generative rule

```text
Gamma_comp(T).
```

It is an **additional model assumption**, not source-derived PAYOFF semantics. The axiom is biologically appropriate only when integration really does impose shared control and modular release really does permit independently gated cue processing.

Let

```text
c(T)=number of connected components of T.
```

---

## Theorem CR1 — exact topology-to-gap map under component addressability

For one connected component, only one terminal cue is required:

```text
C_A=C_F=1.
```

For `c(T)>=2`, `Gamma_comp` maps the topology to the existing `c(T)`-branch extremal routing family. The coarse router identifies the active module; the adaptive policy then acquires only that module's terminal cue. The fixed architecture must carry the router and every module-terminal obligation.

Therefore

```text
C_A=2,
C_F=c(T)+1,
```

and in all cases

```text
g(T)=C_F-C_A=c(T)-1.
```

### Proof

For `c=1`, the one declared terminal cue resolves the binary target for both adaptive and fixed strategies.

For `c>=2`, `adaptive_gain.extremal_routing_task(c)` already has the exact executable theorem

```text
C_A=2,
C_F=c+1.
```

`Gamma_comp` identifies its `c` branches with the `c` independently addressable topology components. Subtracting gives `g=c-1`. QED.

### Relation to the sufficient-kernel result

This does not contradict topology-only nonidentifiability. Bare `T` remains insufficient under the original source semantics. The new axiom supplies extra biological semantics and thereby defines a concrete generative rule

```text
T
-> Gamma_comp(T)
-> full routing task
-> (K_A(T), H_min(T), costs)
-> g(T).
```

The test suite reconstructs both halves of the sufficient kernel from the generated task. For `c=3`, the continuation quotient recovers `C_A=2`, while the productive frontier contains four singleton fixed-mandatory obligations (one router plus three module terminals) and recovers `C_F=4`.

Thus `Gamma_comp` is the first explicit prospective bridge in this side line that realizes the previously derived joint structural sufficiency condition.

---

## Theorem CR2 — one coupling mutation changes the structural gap by at most one

If two topology states differ by one undirected edge flip, then

```text
|g(T')-g(T)| <= 1.
```

More precisely:

```text
delete a graph bridge
-> c increases by 1
-> g increases by 1;

delete a redundant/non-bridge edge
-> c unchanged
-> g unchanged;

add an edge joining two components
-> c decreases by 1
-> g decreases by 1;

add an edge inside one component
-> c unchanged
-> g unchanged.
```

This is standard graph connectivity composed with CR1; no graph-theoretic novelty is claimed.

---

## 3. Why `q-g` is only a lower bound on mutation distance

A tempting but false step is:

```text
required gap increase = q-g(T)
therefore exactly q-g(T) edge mutations are enough.
```

Cycles break that equivalence. Deleting one edge from a cycle need not create a new component, so several topology mutations can be structurally neutral before the sensing gap changes.

Example with three function nodes:

```text
path A-B-C:
current c=1, g=0;
one bridge deletion -> c=2, g=1.

triangle A-B-C-A:
current c=1, g=0;
one deletion -> still connected, g=0;
two deletions -> c=2, g=1.
```

Thus two architectures can have the same current sensing gap but different evolutionary accessibility to the same required gap.

---

## Theorem CR3 — required sensing gap becomes a minimum k-cut problem

Suppose architectural mutation flips one retained/released coupling edge at a time and every currently retained edge is individually mutable.

For a target regime requiring structural gap `q`, CR1 requires

```text
c(T_target) >= q+1.
```

Let

```text
d_q(T)
=
minimum number of single-edge topology mutations needed to reach any topology
with g>=q.
```

Any edge addition can only preserve or reduce the number of connected components. Hence a shortest path to `g>=q` can be replaced by one that uses only deletions of edges already present in `T`.

Therefore

```text
d_q(T)
=
min |F|
such that
F subset E(T)
and
c(T-F)>=q+1.
```

This is exactly the unweighted minimum `(q+1)`-cut objective, generalized to a starting graph that may already be disconnected.

### Proof

Any successful edge-flip path has some set `F` of deleted initial edges and some set of added edges. Removing the additions from the final topology cannot decrease its component count, so deleting `F` alone is also sufficient to reach at least `q+1` components. Hence every successful path uses at least as many deletions as the minimum cut expression above.

Conversely, deleting a minimum feasible set `F` one edge at a time gives a path of exactly `|F|` mutations to a topology with `g>=q`. QED.

### Prior-art boundary

Minimum `k`-cut is a classical graph-optimization problem. No novelty is claimed for the cut problem, its complexity, or its algorithms. The contribution of this bridge model is only the translation

```text
required eco-evolutionary gap q
-> required number of independently addressable modules q+1
-> topology mutation distance given by a k-cut objective.
```

---

## Corollary CR3.1 — forest topologies attain the gap-change lower bound

If every connected component of `T` is a tree, every retained edge is a bridge. Therefore, whenever `q<=|V|-1`,

```text
d_q(T)=max(0,q-g(T)).
```

There is no coupling-redundancy overhead.

---

## Corollary CR3.2 — cycles protect the integrated state against gap release

Define

```text
R_q(T)
=d_q(T)-max(0,q-g(T))
```

when the target is feasible.

Then

```text
R_q(T)>=0.
```

`R_q` is the extra number of edge mutations needed because some deletions are structurally neutral before component count increases. It is a bridge-specific accessibility diagnostic, not a new graph invariant.

For the first positive gap (`q=1`) from a connected topology,

```text
d_1(T)
```

is the ordinary global edge connectivity of `T`.

Examples:

```text
3-node path:     d_1=1
3-node triangle: d_1=2
K4:              d_1=3
```

So coupling redundancy can delay the emergence of any contingent sensing advantage even when the required final gap is only one.

This gives a clean distinction:

```text
current structural capability g(T)
!=
mutation accessibility of a larger gap.
```

---

## 4. Composition with the existing eco-evolutionary threshold

The frozen flagship supplies a required integer structural gap, for example

```text
q_osc
```

for a stable oscillatory local regime.

Under `Gamma_comp`, the reverse reachability chain becomes

```text
required local feedback phase
-> required gap q
-> required component count q+1
-> minimum topology mutations d_q(T)
   = minimum (q+1)-cut cardinality.
```

The frozen flagship asks what finite sensing structure is required. The prospective bridge asks a new accessibility question: how many heritable coupling mutations are needed before that structural capability can emerge under this particular topology-to-control model?

Do not merge this extension into the frozen manuscript without a fresh novelty and biological-assumption audit.

---

## 5. PAYOFF payoff overlay

PAYOFF can assign intrinsic optimized payoff `b_T` to topology states and can define a single-edge mutation graph plus valley depth.

Once a topology family is evaluated under `Gamma_comp`, compute

```text
g(T)=c(T)-1,
V_q={T:g(T)>=q}.
```

Then `topology_sensing_reachability.py` separates:

```text
V_q empty
-> no topology in the declared family is structurally capable;

V_q nonempty but mutation-disconnected
-> structurally possible somewhere but graph-inaccessible;

B_q>0
-> every route to every capable topology crosses an intrinsic-payoff valley;

B_q=0
-> some capable topology is reachable without dropping below source payoff.
```

A canonical audit fixture illustrates both kinds of barrier:

```text
triangle -> path -> split topology

gaps:     0       0       1
payoffs:  10       9      12
```

The target `q=1` is globally present at `split`, but one redundant edge deletion is needed before the gap changes, and the only route crosses an intrinsic payoff valley of depth one.

So three objects remain distinct even after the bridge is declared:

```text
structural capability,
topological mutation distance,
intrinsic payoff valley depth.
```

---

## 6. Novelty discipline after targeted literature check

Neighboring prior art is substantial:

- classical minimum `k`-cut and edge-connectivity theory;
- modular biological and neural networks;
- connection-cost-driven evolution of modularity;
- modular sensory/decision processing architectures;
- evolutionary models of proximate sensing and behavioural-control architecture;
- adaptive/fixed decision trees and information-use theory.

Representative neighboring work includes Clune, Mouret & Lipson (2013) on evolutionary origins of modularity, Ellefsen, Mouret & Clune (2015) on modular neural architectures and selective learning, Eliassen et al. (2016) on proximate sensing/decision architecture, and the classical `k`-cut literature.

Therefore do **not** claim novelty for:

- modularity improving information processing;
- disconnected modules having separate functions;
- graph cuts or edge connectivity;
- adaptive routing as a generic idea;
- small mutation or valley crossing.

The possible companion contribution is narrower:

> under a predeclared biological map from heritable coupling topology to independently addressable sensing modules, a required eco-evolutionary feedback phase induces an exact topology mutation-accessibility problem; structural capability is determined by the generated adaptive/fixed kernel, coupling redundancy controls the number of edge mutations needed to create enough independent modules, and PAYOFF payoff valleys provide a separate accessibility barrier.

This remains a **candidate novelty statement**, not a priority claim.

---

## 7. Biological hard stop

`Gamma_comp` is not licensed by PAYOFF automatically.

Before using this bridge for a real biological system, establish that:

1. the declared function nodes correspond to units whose coupling topology is heritable/evolvable;
2. connected coupling imposes shared control at the relevant sensing scale;
3. separation into components permits independently gated cue acquisition;
4. the coarse context router and module-specific cues correspond to biologically plausible sensory operations;
5. topology mutations do not simultaneously change target semantics in a way that invalidates comparison of `g(T)` across states.

Without those conditions, CR1-CR3 are valid mathematics for the prospective bridge model but not an empirical mechanism claim.
