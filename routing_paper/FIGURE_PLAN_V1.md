# Routing second paper — figure plan v2

## Design principle

Three main figures remain sufficient. The key change from v1 is that Figure 2 now distinguishes **largest aggregate gain class** from **stationary majority**, eliminating the impression that the closed-form mode threshold was chosen as a proxy for all occupancy notions.

## Figure 1 — Finite routing representation creates an exact multiplicity profile

### Panel A — genotype-policy representation

Show `X={0,...,q}^k` with weakest-branch gain `g(x)=min_i x_i`. Use `q=2,k=3` as the running example.

### Panel B — exact layer counts

For `q=2,k=3`:

- gain 0: `D_0=19`
- gain 1: `D_1=7`
- gain 2: `D_2=1`

Display

`D_r=(q-r+1)^k-(q-r)^k`.

### Panel C — distance below full gain

Show

`A_s=(s+1)^k-s^k`,

with `A_1=2^k-1` highlighted.

### Message

The unique full-gain genotype can sit above a much more numerous adjacent gain class. Figure 1 is representation/combinatorics, not yet a population-genetic conclusion.

---

## Figure 2 — One layer hierarchy generates two ordered occupancy thresholds

This is the central figure.

### Panel A — nested-subset-chain certificate

For `k=3,s=2`, depict

`x -> (S_1 subseteq S_2)`

with nonempty branch-label subsets. Contrast nested admissible chains with unrestricted nonempty-subset strings.

Display

`A_s <= (2^k-1)^s`,

strict for `k>=2,s>=2`.

### Panel B — exact aggregate-mode transition

For `q=2,k=3`, aggregate layer weights are

`W_r=D_r theta^r`.

Show three exact mode regimes:

- `theta=2`: `(19,14,4)` — full nonmodal;
- `theta=7`: `(19,49,49)` — exact gain-1/gain-2 tie;
- `theta=8`: `(19,56,64)` — full uniquely modal.

Mark

`T_3=7`.

Use the label **largest aggregate gain class**, not “dominant genotype.”

### Panel C — stationary-majority transition

Plot or annotate

`P_full(theta)=1/[1+7/theta+19/theta^2]`.

Mark:

- mode threshold `theta=7`, where `P_full=49/117≈0.419`;
- majority threshold `theta_1/2=(7+5 sqrt(5))/2≈9.09`;
- `theta=9`: `P_full=81/163<1/2`;
- `theta=10`: `P_full=100/189>1/2`.

The plot should visually expose the interval in which full gain is already the largest gain class but still not a stationary majority.

### Panel D — general theorem strip

For `q>=2` show the ordered regions

`theta < T_k`

`T_k <= theta < theta_1/2`

`theta >= theta_1/2`

with labels

`full nonmodal`

`full modal but <1/2`

`full stationary majority`.

Above the strip write

`T_k=2^k-1 < theta_1/2 < 2T_k`.

At exactly `theta=T_k`, note the `{q-1,q}` tie for `k>=2`.

### Panel E — canonical Moran staircase

Map `theta=a^(N-1)`. For canonical `k=q+1,a=2` and `q>=2`, show

`N_unique_mode=q+2`

and

`N_majority=q+3`.

This one-step separation is the cleanest population-level consequence of having defined both estimands.

### Message

The adjacent layer controls the full lower-layer hierarchy, but “largest class” and “majority occupancy” are distinct thresholds. The same global combinatorial bound controls both.

---

## Figure 3 — Occupancy thresholds are conditional on representation and mutation measure

### Panel A — representation contrast

At the same `q=2,theta=2` and the same phenotype-level fitness schedule:

**Compressed chain**

`weights=(1,2,4)`, `P(full)=4/7>1/2` — full is uniquely modal and a majority.

**Branch-product routing**

`D=(19,7,1)`, `weights=(19,14,4)`, `P(full)=4/37` — full is nonmodal and far below majority.

Label:

**same phenotype fitness schedule, opposite occupancy conclusions**.

### Panel B — reversible mutation-measure boundary

On the same gain path and at the same `theta=2`, show the frozen exact selected occupancies:

- `(1/10,1/10,4/5)`;
- `(9/20,9/20,1/10)`.

Label:

**fixed support is insufficient; the neutral mutation measure remains causal**.

### Panel C — dependency diagram

`gain map + genotype-policy representation + neutral mutation measure + selection tilt`

`                              -> stationary gain occupancy`

Annotate that both `T_k` and `theta_1/2` are properties of the symmetric branch-product specification, not universal biological constants.

---

# Supplement only if needed

Possible supplementary figures:

- `theta_1/2/T_k` across `(q,k)` to show the majority threshold remains within the factor-two theorem bracket;
- population-size staircases for rational `a` values;
- accessibility-distance contrast between branch-product and compressed encodings;
- additional fixed-support mutation-bias witnesses.

Do not add figures for neutral-plateau waiting times, mesoscopic target dynamics, absolute-rate nonidentifiability, or downstream population-process ceilings.

# Figure-to-claim map

| Figure | Main claim |
|---|---|
| Fig. 1 | exact routing-layer multiplicity |
| Fig. 2 | global bound + modal transition + majority transition |
| Fig. 3 | representation and mutation-measure claim ceilings |

A fourth main figure is a warning that the paper is becoming too broad.