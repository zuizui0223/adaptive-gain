# Topology-to-sensing bridge target

Status: side-theory target. This is **not** part of the frozen Theoretical Ecology submission.

## 1. The original bridge problem

PAYOFF already supplies a discrete architecture state space under retained-versus-released coupling topologies. Single-edge architectural mutations connect neighboring topologies, while PAYOFF can attach intrinsic optimized payoff and valley/accessibility quantities to those states.

adaptive-gain supplies finite sensing tasks and exact adaptive/fixed structural gaps.

A joint theory therefore needs a declared biological map

```text
psi: topology T -> finite sensing task S(T).
```

For a declared task define

```text
g(T)=C_F(S(T))-C_A(S(T)).
```

and for a target local eco-evolutionary regime requiring gap `q`,

```text
V_q={T:g(T)>=q}.
```

The map must be defined before inspecting `g(T)`, `V_q`, or any desired downstream phase result.

---

## 2. Topology alone is not enough

`TOPOLOGY_ONLY_BRIDGE_NONIDENTIFIABILITY.md` establishes an exact repository witness that bare PAYOFF topology semantics do not identify `g(T)`. The missing ingredients include represented worlds, target distinctions, cue resources, outcome maps, costs, and physical dependency/availability rules.

This means the bridge cannot be recovered by relabelling a topology edge as a cue edge after the fact.

`TOPOLOGY_SENSING_SUFFICIENT_KERNEL.md` gives the constructive replacement. A future bridge does not need to reconstruct every detail of a full finite task; it is enough to generate

```text
K_A(T)      = adaptive continuation information sufficient for C_A,
H_min(T)    = minimal productive frontier sufficient for C_F,
resource costs.
```

Call such a prospective generative rule

```text
Gamma_K(T).
```

Then

```text
Gamma_K(T)
-> g(T)
-> V_q
-> mutation / payoff accessibility.
```

---

## 3. Conditional topology-regime reachability after g(T) is supplied

Let the topology mutation graph have one node per architecture state and one edge per allowed single-edge architectural mutation.

For source `S`, define

```text
d_q(S)=minimum mutation-graph distance from S to V_q.
```

With PAYOFF intrinsic topology payoff `b_T`, define the best bottleneck payoff from source `S` to target `G` and PAYOFF valley depth

```text
B(S->G)=max[0,b_S-m*(S,G)].
```

Then define

```text
B_q(S)=min_{G in V_q} B(S->G).
```

The executable side module `topology_sensing_reachability.py` computes the corresponding finite-graph quantities after exact topology-specific gaps have been supplied.

### Exact interpretation

- `V_q=empty`: no topology in the declared family is structurally capable of the target phase;
- `V_q!=empty` but no capable topology lies in the source mutation component: structural capability exists somewhere but is mutation-disconnected;
- finite `d_q>0`: at least that many topology substitutions are required before any capable state can be reached, ignoring selection/fixation;
- `B_q=0`: some capable topology is reachable along a single-edge path whose every visited topology has intrinsic payoff at least the source payoff;
- `B_q>0`: every route to every capable topology crosses an intrinsic-payoff valley below the source.

These are graph/accessibility compositions, not independent novelty claims.

---

## 4. Source-derived bridge remains unresolved

The current PAYOFF source does **not** license `psi` automatically.

PAYOFF topology edges represent developmental/genetic/structural integration among fitness-relevant functions. Its adaptive finite-panel queries are researcher-side phase-identification measurements. There is no source rule saying

```text
released coupling edge = new organismal cue
```

or

```text
topology state = contingent sensory policy.
```

Therefore a **source-derived** `psi(T)` has not yet been recovered from PAYOFF as currently written.

This remains the hard stop for any empirical/source claim.

---

## 5. Prospective bridge now available: Gamma_comp

A separate prospective model is developed in

```text
theory/COMPONENT_ROUTING_BRIDGE.md
adaptive_gain/component_routing_bridge.py
```

The component-addressability axiom declares:

```text
one connected topology component
= one jointly controlled functional module;

different connected components
= independently addressable modules;

coarse context cue
-> relevant module;

module-specific terminal cue
-> local target.
```

This is an **added biological axiom**, not a fact inferred from PAYOFF topology alone.

Under this rule, if `c(T)` is the number of connected components,

```text
Gamma_comp(T)
-> exact finite routing task
-> induced joint structural kernel
-> g(T)=c(T)-1.
```

The implementation verifies both sides of the sufficient kernel: the continuation quotient recovers the exact adaptive cost and the productive frontier recovers the exact fixed cost.

Thus the side theory now contains its first explicit prospective `Gamma_K(T)` realization, while preserving the topology-only nonidentifiability result for the unaugmented source semantics.

---

## 6. New mutation-accessibility theorem under Gamma_comp

If architectural mutation flips one retained/released edge at a time, a target gap `q` requires at least

```text
q+1 connected components.
```

The exact minimum number of topology edge mutations needed to reach `g>=q` from a topology `T` is

```text
min |F|
such that
F subset E(T)
and
components(T-F)>=q+1.
```

This is the classical unweighted minimum `(q+1)`-cut objective applied to the bridge model.

The graph-theoretic object is established prior art; the side-theory role is the biological composition

```text
required feedback phase
-> required structural gap q
-> required independently addressable modules q+1
-> topology mutation burden via k-cut.
```

### Important consequence

`q-g(T)` is only a lower bound on mutation distance.

Cycles can make early edge deletions structurally neutral. Therefore two topologies with the same current gap can have different accessibility to the same target gap.

Example:

```text
3-node path:     g=0, one deletion reaches g=1;
3-node triangle: g=0, two deletions are required;
K4:              g=0, three deletions are required to obtain the first extra component.
```

For a connected source and target `q=1`, the mutation burden is ordinary edge connectivity.

This distinction between current capability and accessibility is the main new mathematical consequence of the prospective bridge.

---

## 7. Two bridge tracks must remain distinct

### Track A — source-derived / empirical bridge

Still unresolved. A valid completion must show that real or source-model architecture variables actually determine the sensing/control kernel without an added post hoc mapping.

### Track B — prospective component-addressability bridge

Mathematically explicit and executable. It can support a companion theoretical model if natural-history assumptions justify the component-addressability axiom.

Do not use Track B as evidence that PAYOFF already contained organismal sensory modules.

---

## 8. Completion criteria for a stronger bridge

For a source-derived or empirically grounded companion result:

1. choose a heritable architecture family with explicit topology semantics;
2. predeclare the rule generating `K_A(T)`, `H_min(T)`, and resource costs;
3. show that the rule is biologically motivated rather than selected to manufacture a desired gap pattern;
4. compute exact `C_A(T), C_F(T), g(T)`;
5. fix the downstream phase threshold `q` before inspecting topology gaps;
6. compute `V_q`, mutation distance, and PAYOFF valley/accessibility quantities prospectively;
7. seek a nontrivial witness such as `V_q!=empty` but positive topology/payoff barrier from the resident;
8. keep identification/reportability gates separate from mutation accessibility;
9. perform a fresh prior-art audit before any companion novelty claim.

---

## 9. Novelty ceiling

Do not claim novelty for:

- small mutations or adaptive dynamics;
- Hegselmann-Krause/bounded confidence;
- replicator-mutator / mesoscopic trait distributions;
- topology mutation graphs or valley crossing;
- modular neural/sensory networks;
- minimum `k`-cut or edge connectivity;
- decision trees or generic adaptivity gaps;
- generic possible-versus-accessible distinctions.

The current frozen flagship novelty candidate remains

```text
required local feedback phase
-> required adaptive/fixed structural gap
-> exact minimum/Pareto finite (n,m,E) sensing structure.
```

A future companion novelty would require an exact, biologically defensible architecture-to-sensing generative rule that makes mutation accessibility and finite sensing phase reachability jointly testable in the same state space. `Gamma_comp` is now one mathematically complete prospective candidate, but its biological axiom still requires independent justification.
