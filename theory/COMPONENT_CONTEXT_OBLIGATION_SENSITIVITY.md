# Context-obligation sensitivity in the component bridge

Status: side-theory refinement. This is **not** part of the frozen Theoretical Ecology submission.

## 1. Why connected-component count is not yet the whole bridge

`COMPONENT_ROUTING_BRIDGE.md` introduced a prospective component-addressability rule in which disconnected coupling components become independently addressable functional modules.

That rule still leaves one biologically meaningful choice open:

> Is the coarse context cue itself indispensable to a fixed sensory architecture, or can a fixed architecture bypass it by carrying all module-specific terminal cues simultaneously?

This distinction changes the productive frontier while leaving the same topology and the same broad adaptive route available.

It therefore provides a concrete bridge-level illustration of the earlier sufficient-kernel result:

```text
adaptive continuation alone is not enough;
fixed-side productive obligations matter independently.
```

---

## 2. Two prospective semantics on the same topology

Let

```text
c=c(T)
```

be the number of independently addressable topology components.

### Semantics M — context mandatory

This is the original `Gamma_comp` construction. Module-terminal cue codes are globally ambiguous without the coarse context router.

For `c>=2`:

```text
C_A=2,
C_F=c+1,
g_M=c-1.
```

The minimal productive frontier consists of `c+1` singleton obligations:

```text
{router},
{terminal_1},...{terminal_c}.
```

For `c=1`, `C_A=C_F=1` and `g_M=0`.

### Semantics B — context bypassable

The same coarse router is available to the adaptive policy, but each module terminal is globally interpretable. Collecting all module terminals simultaneously therefore resolves the target without measuring context.

Use worlds

```text
(a_i,target=0),
(b_i,target=1)
```

for each module `i`. The router reports only module identity. Terminal `i` is one only on `b_i` and zero everywhere else.

For `c>=2`:

```text
C_A=2,
C_F=c,
g_B=c-2.
```

The fixed productive frontier contains only the `c` terminal singleton obligations; the router singleton disappears.

For `c=1`, again `C_A=C_F=1` and `g_B=0`.

---

## Proposition COS1 — one context-obligation bit changes the exact gap by one

For every topology with `c>=2` components,

```text
g_M-g_B=1.
```

Equivalently, if

```text
chi=1  when context is fixed-mandatory,
chi=0  when context is fixed-bypassable,
```

then for `c>=2`

```text
g(T;chi)=c-2+chi.
```

### Proof

Both semantics have the same exact adaptive minimum `C_A=2`: observe context, then the active module terminal.

Under Semantics M the router and all `c` module terminals are fixed-mandatory, so `C_F=c+1`.

Under Semantics B, all `c` terminals together resolve the target and every terminal is individually necessary for its private pair `(a_i,b_i)`, so `C_F=c`. Subtraction gives the result. QED.

### Interpretation

The component partition alone does not determine the sensing gap, even inside the prospective component-addressability family. One additional piece of physical semantics — whether context can be bypassed in the fixed architecture — changes the exact fixed-side burden.

This is not a contradiction of `Gamma_comp`; it identifies which biological assumption made its router fixed-mandatory.

---

## Proposition COS2 — the two semantics have different productive frontiers

For `c>=2`, index the router as query zero and module terminals as queries `1,...,c`.

Then:

```text
Semantics M:
H_min = {{router},{terminal_1},...,{terminal_c}};

Semantics B:
H_min = {{terminal_1},...,{terminal_c}}.
```

The adaptive minimum remains two in both cases.

Thus the topology-semantic difference is localized exactly to the fixed-side sufficient object.

For `c=3`, the executable bitmask receipts are

```text
M: (1,2,4,8),
B: (2,4,8).
```

and

```text
(C_A,C_F,g)_M=(2,4,2),
(C_A,C_F,g)_B=(2,3,1).
```

This gives a concrete biological interpretation to the abstract statement in `TOPOLOGY_SENSING_SUFFICIENT_KERNEL.md` that both continuation structure and productive frontier are independently needed.

---

## 3. Required phase -> different component threshold

Let a downstream feedback phase require structural gap

```text
q>=1.
```

Then:

```text
Semantics M:
g_M>=q
iff
c>=q+1;

Semantics B:
g_B>=q
iff
c>=q+2.
```

So the same dynamical target demands one additional independently addressable module when the fixed architecture can bypass context.

This sounds backwards only if `C_F` is interpreted as generic complexity. The gap measures **the advantage of contingent routing relative to the best fixed comparator**. Making context bypassable improves the fixed comparator and therefore raises the amount of modular release needed before a given adaptive/fixed gap appears.

---

## Proposition COS3 — context semantics shift the topology cut problem

Under one-edge coupling mutations, define

```text
lambda_k(T)
=
minimum number of retained edges that must be deleted so that T has at least k components.
```

This is the standard unweighted minimum `k`-cut cardinality for the declared starting graph.

Then, for `q>=1`:

```text
d_q^M(T)=lambda_{q+1}(T),

d_q^B(T)=lambda_{q+2}(T),
```

provided the required number of components does not exceed the number of function nodes.

Hence

```text
d_q^B(T)>=d_q^M(T)
```

whenever both are feasible.

Again, no novelty is claimed for the graph cut objects. The result is about how a biological fixed-side interpretation changes which cut order is induced by the same eco-evolutionary target gap.

---

## 4. Canonical mutation-distance contrasts

For target `q=1`:

### Three-node path

```text
Semantics M:
need 2 components -> delete 1 bridge edge.

Semantics B:
need 3 components -> delete both edges.
```

So

```text
d_1^M=1,
d_1^B=2.
```

### Three-node triangle

```text
Semantics M:
need 2 components -> minimum 2 edge deletions.

Semantics B:
need 3 components -> all 3 edges must be deleted.
```

Thus

```text
d_1^M=2,
d_1^B=3.
```

### Complete graph K4

```text
Semantics M:
need 2 components -> edge connectivity = 3.

Semantics B:
need 3 components -> minimum 3-cut = 5.
```

Thus

```text
d_1^M=3,
d_1^B=5.
```

The same final dynamical requirement can therefore induce materially different evolutionary architecture distances under two biologically distinct fixed-side interpretations.

---

## 5. Declared-family pipeline consequence

Consider the topology sequence

```text
triangle -> path -> split -> isolated
```

on three function nodes, where each arrow is one edge deletion.

The component counts are

```text
1,1,2,3.
```

Therefore the two gap landscapes are

```text
Semantics M:
0,0,1,2;

Semantics B:
0,0,0,1.
```

For target `q=1`, the regime-capable sets differ:

```text
V_q^M={split, isolated};
V_q^B={isolated}.
```

Starting from the triangle, the graph-distance burden is therefore two versus three topology substitutions.

If PAYOFF intrinsic payoffs are attached to the same topology states, `declared_topology_sensing_family.py` and `topology_sensing_reachability.py` can compute the payoff-valley overlay without changing those payoffs. This keeps structural eligibility and evolutionary payoff accessibility as separate objects.

---

## 6. Relation to topology-only nonidentifiability

The context-sensitivity result strengthens, rather than weakens, the earlier negative theorem.

`TOPOLOGY_ONLY_BRIDGE_NONIDENTIFIABILITY.md` says bare topology does not identify `g` under current source semantics.

Here even after adding a strong component-addressability assumption, one still must specify whether the context resource is globally indispensable or fixed-bypassable. That choice changes the productive frontier and hence `g`.

So a future biological bridge must determine at least:

```text
which modules are independently addressable,
which context variables gate their use,
whether terminal cues are interpretable without context,
which resources remain globally indispensable to a fixed architecture.
```

This is a much sharper completion criterion than simply mapping topology to module count.

---

## 7. Novelty discipline

Do not claim novelty for:

- bypasses in decision trees or test covers;
- private-pair lower bounds;
- productive-frontier/hitting-set algebra as general graph theory;
- minimum k-cut;
- modular sensory architecture;
- context-dependent cue use.

The possible companion contribution is the **ecological composition** if a real biological system determines these context-obligation semantics prospectively:

```text
heritable coupling topology
+ physical cue interpretability
-> exact adaptive/fixed sensing kernel
-> required gap/phase eligibility
-> topology mutation distance
+ independent PAYOFF valley barrier.
```

Until that biological bridge is justified, COS1-COS3 are exact results for two prospective bridge models, not empirical mechanism claims.
