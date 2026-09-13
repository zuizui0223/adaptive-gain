# Routing second paper — figure plan v1

## Design principle

Three main figures are enough. The paper should look like one theorem story with two explicit scope controls, not a catalog of the routing side-theory stack.

## Figure 1 — Finite routing representation creates an exact multiplicity profile

### Panel A — genotype-policy representation

Show

`X={0,...,q}^k`

with gain

`g(x)=min_i x_i`.

Use canonical running example

`q=2, k=3`.

A small cube/lattice schematic should make clear that gain is set by the weakest coordinate.

### Panel B — exact layer counts

For `q=2,k=3`, show

- gain 0: `D_0=19`
- gain 1: `D_1=7`
- gain 2: `D_2=1`

General formula beside the bars:

`D_r=(q-r+1)^k-(q-r)^k`.

### Panel C — distance-below-full form

Show

`A_s=(s+1)^k-s^k`

and highlight

`A_1=2^k-1`.

### Message

The maximally adapted genotype is unique, while the immediately suboptimal gain layer can be exponentially more numerous in `k`.

Do not describe this alone as a selection result; Figure 1 is representation/combinatorics.

---

## Figure 2 — All lower layers collapse to one sharp transition

This is the central figure.

### Panel A — nested-subset-chain certificate

For a small example (`k=3`, `s=2`), depict

`x -> (S_1 subseteq S_2)`

with each `S_j` a nonempty subset of branch labels.

Visually contrast:

- admissible nested chains;
- all arbitrary nonempty-subset strings.

Write

`A_s <= (2^k-1)^s`,

with strict `<` for `k>=2,s>=2`.

### Panel B — aggregate stationary layer weights

For `q=2,k=3`, plot or diagram

`W_r=D_r theta^r`.

Use three marked regimes around

`theta_c=7`:

- below: e.g. `theta=2`, weights `(19,14,4)`;
- exact: `theta=7`, weights `(19,49,49)`;
- above: e.g. `theta=8`, weights `(19,56,64)`.

The visual should explicitly label **aggregate gain-layer weight**.

### Panel C — trichotomy

Compact phase strip:

`theta < 2^k-1` | `theta = 2^k-1` | `theta > 2^k-1`

with labels

`full nonmodal` | `{q-1,q} tie` | `full uniquely modal`.

### Panel D — Moran corollary

Show mapping

`theta=a^(N-1)`

and the boundary

`a^(N-1) ? 2^k-1`.

For canonical `k=q+1,a=2`, annotate

`N*=q+2`.

### Message

The adjacent layer is not merely the first competitor: its multiplicity controls every lower-layer comparison exactly through the global bound.

---

## Figure 3 — The sharp threshold is conditional, not universal

Two scope controls in one figure.

### Panel A — representation contrast

Same gain set, same fitness tilt, two encodings.

At `q=2, theta=2`:

**Compressed chain**

`weights=(1,2,4)`

`P(full)=4/7`

full layer uniquely modal.

**Branch-product routing**

`multiplicity=(19,7,1)`

`weights=(19,14,4)`

`P(full)=4/37`

full layer nonmodal.

Label the conclusion:

**same phenotype fitness schedule, opposite stationary gain-layer conclusion**.

### Panel B — mutation-measure boundary

Keep the same gain path and the same `theta`, but show two reversible neutral measures producing contrasting selected stationary laws.

Use the frozen `q=2, theta=2` witness:

- model A selected occupancy `(1/10,1/10,4/5)`;
- model B selected occupancy `(9/20,9/20,1/10)`.

Label:

**fixed support is insufficient; neutral mutation measure remains causal**.

### Panel C — claim hierarchy

A small dependency diagram:

`gain map + representation + neutral mutation measure + selection tilt`

`                -> stationary gain-layer occupancy`

Highlight that `theta_c=2^k-1` is the symmetric branch-product special case.

### Message

The theorem is exact because assumptions are explicit. Representation and mutation measure are part of the causal specification, not nuisances to be inferred from gain alone.

---

# Supplementary figures only if needed

Possible supplement:

- broader `(q,k)` heat map of `T_k=2^k-1`;
- exact population-size staircase for several rational `a` values;
- accessibility-distance comparison between branch-product and compressed encodings;
- additional fixed-support mutation-bias constructions.

Do not make figures for neutral-plateau waiting times, mesoscopic target dynamics, absolute-rate nonidentifiability, or downstream population-process ceilings in this paper.

# Figure-to-claim map

| Figure | Main claim |
|---|---|
| Fig. 1 | exact routing-layer multiplicity |
| Fig. 2 | global bound + sharp aggregate-layer trichotomy |
| Fig. 3 | representation and mutation-measure scope controls |

If a fourth main figure becomes necessary, the manuscript is probably becoming too broad.