# Topology-to-sensing bridge target

Status: conditional side theorem target. This is **not** part of the frozen Theoretical Ecology submission. It isolates the exact additional object needed to compose PAYOFF topology accessibility with adaptive-gain structural reachability.

## 1. Why topology is the cleaner bridge coordinate

PAYOFF already contains a discrete architecture state space under vertex/topology selection. With binary retained-versus-released coupling edges, architectures are nodes of a hypercube and single-edge architectural mutations connect Hamming-neighbor topologies.

This is cleaner than forcing the continuous recovery coordinate `r` directly into adaptive-gain because both sides can then be finite/discrete:

```text
PAYOFF topology T
-> biological sensing task S(T)
-> adaptive/fixed gap g(T)
-> downstream feedback capability.
```

The missing scientific object is the map

```text
psi: T -> S(T).
```

It must be defined from natural-history / mechanism semantics, not fitted after seeing the desired adaptive-gain result.

## 2. Source-side PAYOFF structure

Let the finite topology graph be

```text
G_top=(V,E),
```

where `T,T' in V` are adjacent when one declared architectural edge changes state.

PAYOFF supplies for each topology an intrinsic optimized payoff

```text
b_T,
```

and for source `S` and target `G` the single-edge intrinsic valley depth

```text
B(S->G)
=max[0, b_S - m*(S,G)],
```

where `m*(S,G)` is the best bottleneck payoff among all single-edge paths.

PAYOFF's TRM4 states:

```text
B(S->G)=0
```

iff there exists a single-edge path from `S` to `G` whose every visited topology has payoff at least `b_S`.

This is an accessibility statement, not a fixation-time theorem.

## 3. Sensing-side adaptive-gain structure

For a declared task `S(T)=psi(T)`, define

```text
g(T)=C_F(S(T))-C_A(S(T)).
```

Suppose a requested local eco-evolutionary regime requires structural gap at least

```text
q>=1.
```

The current adaptive-gain reachability theorem then constrains which finite sensing structures can realize `g>=q`.

Define the regime-capable topology set

```text
V_q={T in V : g(T)>=q}.
```

This set is meaningful only after `psi` has been declared and the tasks have been solved exactly or certified.

## 4. Structural-regime distance

Define

```text
d_q(S)
=min{ d_H(S,G) : G in V_q },
```

with `d_q(S)=infinity` when `V_q` is empty.

Here `d_H` is Hamming distance on binary topology states, equivalently the minimum number of single-edge changes ignoring selection/fixation.

### Proposition TS1 — mutation-step lower bound

If mutations change at most one topology edge per substitution, every route from `S` to a topology capable of the target regime requires at least

```text
d_q(S)
```

substitutions.

This is a graph-distance identity, not a novelty claim.

## 5. Structural-regime valley depth

Define the minimum intrinsic valley depth to the regime-capable set:

```text
B_q(S)
=min{ B(S->G) : G in V_q },
```

with `B_q(S)=infinity` if `V_q` is empty.

### Proposition TS2 — exact zero-valley characterization

Assume `V_q` is nonempty. Then

```text
B_q(S)=0
```

iff there exists at least one regime-capable topology `G in V_q` and a single-edge path from `S` to `G` such that every visited topology `T_i` satisfies

```text
b_{T_i} >= b_S.
```

### Proof

If `B_q(S)=0`, some `G in V_q` attains `B(S->G)=0`; PAYOFF TRM4 gives the required path. Conversely, any such path implies `B(S->G)=0` for that target and therefore `B_q(S)=0`. QED.

This proposition is a set-valued corollary of PAYOFF TRM4 after the adaptive-gain structural target set `V_q` is declared. It should not be presented as an independent mathematical priority claim.

### Proposition TS3 — positive joint barrier

If

```text
0 < B_q(S) < infinity,
```

then every single-edge path from `S` to **every** topology capable of the target regime must pass through at least one topology whose intrinsic payoff lies below the source by at least `B_q(S)`.

This is the exact sense in which a target feedback regime can be structurally realizable somewhere in the architecture family yet inaccessible by an all-above-source single-edge route from the current topology.

## 6. Three distinct failure modes

The topology bridge separates three exclusions that should never be collapsed:

### Structural-family exclusion

```text
V_q = empty.
```

No topology in the declared family carries enough finite sensing gap for the target regime. Mutation dynamics are irrelevant because there is nowhere structurally capable to go.

### Mutation-distance burden

```text
V_q != empty,
d_q(S) > 0.
```

At least `d_q(S)` single-edge changes are required before any regime-capable topology can be reached, even before fitness valleys are considered.

### Fitness-valley barrier

```text
V_q != empty,
B_q(S) > 0.
```

Regime-capable topologies exist, but every single-edge route to all of them crosses an intrinsic-payoff valley below the source.

Actual fixation or first-passage probability additionally depends on mutation rates, population size, selection strength, topology-distance feedback and other process details. `B_q` is not itself a waiting time.

## 7. Relation to the continuous small-jump bridge

The earlier continuous proposal

```text
psi: r -> S(r)
```

and structural jump modulus

```text
J_g(delta)
```

remain valid as a more general target. But the topology route has two practical advantages:

1. PAYOFF already supplies an exact discrete mutation graph and exact valley-depth theorem;
2. adaptive-gain already operates on finite tasks, so no continuous-to-discrete limiting argument is required once `psi(T)` is biologically specified.

Therefore the recommended development order is:

```text
first:  topology T -> finite sensing task S(T)
then:   compute g(T), V_q, d_q, B_q
later:  ask whether these converge to / embed in a continuous r-based bridge.
```

## 8. What remains genuinely hard

None of TS1-TS3 solves the biological mapping problem. The hard step is to justify that changing one PAYOFF architecture edge changes the organism's feasible cue-routing problem in a specific, reproducible way.

A valid `psi(T)` should specify, for every topology:

- represented ecological alternatives;
- available cues / outcomes;
- target distinctions relevant to fitness;
- acquisition costs;
- which cue dependencies are physically available under that topology.

The map must be declared before evaluating `g(T)`.

## 9. Candidate empirical / source-derived construction strategy

The most defensible first construction is not to invent arbitrary tasks. Start from a small PAYOFF network family where topology has a direct mechanistic meaning (retained versus released coupling among functions) and define sensing resources from those functions or their measurable state contrasts.

Then require:

1. the same natural-history rule generates `S(T)` for every topology;
2. no topology is hand-assigned a target gap;
3. `C_A` and `C_F` are solved by the existing adaptive-gain machinery;
4. the target phase threshold `q` is fixed before inspecting `g(T)`;
5. `V_q`, `d_q`, and `B_q` are computed prospectively.

A successful example in which `V_q` is nonempty but `B_q>0` would be the first nontrivial joint witness: the regime is structurally available in the architecture family but separated from the resident by an evolutionary accessibility barrier.

## 10. Novelty ceiling

Do not claim TS1-TS3 as deep new graph theory. They are exact compositions of an existing PAYOFF accessibility theorem with a new finite sensing target set.

Possible future novelty would have to come from one or more of:

- a biologically nontrivial `psi(T)` whose finite sensing gaps can be characterized analytically;
- an exact relation between topology distance / valley depth and adaptive-gain Pareto structure;
- a theorem showing when architecture mutation cannot change `g` fast enough to reach a requested feedback phase;
- an empirically testable prediction that separates structurally capable but evolutionarily inaccessible regimes from genuinely structurally impossible regimes.
