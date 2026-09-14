# Focused novelty audit v1 — source-level collision review

Date: 2026-09-14

## Decision

No direct collision was found for the exact finite-routing theorem composition after source-level review of the closest prior-art classes. Priority confidence remains **moderate**, not high: the isolated ingredients are established or elementary, while the candidate-new object is their routing-specific composition.

The claim boundary remains:

`finite branch-product min representation`

`-> exact layer counts D_r=(q-r+1)^k-(q-r)^k`

`-> global reduction A_s <= (2^k-1)^s`

`-> exact aggregate-mode trichotomy at T_k=2^k-1`

`-> distinct half-mass boundary T_k < theta_1/2(q,k) < 2T_k`

`-> canonical a=2 separation N_unique_mode=q+2 versus N_majority=q+3`.

## Source-level checks

### Sella & Hirsh (2005)

This is direct prior art for the finite-population stationary bridge, including a steady-state distribution of fixed genotypes under mutation, selection and drift. It closes any novelty claim on the reversible stationary law or the use of population size as a selective tilt.

**Collision verdict:** component-level only. It does not provide the routing representation, routing layer multiplicities, `2^k-1` aggregate threshold, or paired majority threshold.

### Riedel et al. (2015)

The paper explicitly introduces a multiplicity parameter from the number of sequence variants corresponding to alternative locus states and combines multiplicity with selection in the low-mutation stationary setting.

**Collision verdict:** strong conceptual collision with “selection versus multiplicity,” but not with the finite routing hierarchy or either exact routing threshold.

### Wilke (2005), Quasispecies Made Simple

This is an important boundary source. It explicitly shows that neutral-network breadth and connectivity affect phenotype competitiveness and shift error thresholds; increasing network size can favor a lower-fitness phenotype. The paper also emphasizes that these are quasispecies/high-mutation replacement-rate thresholds and notes the distinct rare-mutation regime in which populations effectively walk among fixed genotypes.

**Collision verdict:** broad representation-dependent threshold principle is prior art. The mathematical object is different: mutation-rate/eigenvalue threshold in quasispecies dynamics rather than a finite weak-mutation stationary class-mode / half-mass threshold. No algebraically identical `A_s`, `2^k-1`, equality-tie, or factor-two majority result was found.

### Takeuchi, Poorthuis & Hogeweg (2005)

This source analytically formulates a phenotype-level error threshold under genotype-phenotype redundancy / mutational neutrality and explicitly aggregates genotypes sharing a phenotype. It further notes that non-uniform genotype distributions within a phenotype change effective replication accuracy.

**Collision verdict:** closes novelty on phenotype aggregation and redundancy-dependent thresholds. It does not match the routing finite-class count, weak-mutation stationary mode, or stationary-majority theorem.

### Labourel, Bansept & McCandlish (2026 preprint)

This is direct recent prior art for weakest-link epistasis: organismal fitness is the minimum of component fitnesses, analyzed in a population-genetic setting including the rare-mutation regime and genetic load.

**Collision verdict:** the `min` map and weakest-link population-genetic interpretation are prior art. The source does not derive the branch-product routing layer hierarchy or the paper's exact aggregate occupancy thresholds.

## Exact-expression searches

Targeted searches were repeated for:

- `"(s+1)^k - s^k"` with fitness, genotype, weakest-link and selection terms;
- `"2^k-1"` with genotype multiplicity, stationary mode and weakest-link terms;
- the combined expressions `(s+1)^k-s^k` and `2^k-1`;
- stationary-majority / half-mass phenotype-class thresholds;
- finite differences of powers as possible mathematical aliases of the all-layer inequality.

No source-level hit was found that states an algebraically identical theorem or the same mode-plus-majority composition. Generic forward-difference material confirms only that the counting expressions themselves are elementary and cannot support a standalone novelty claim.

## Revised priority wording

Safe wording:

> For this finite routing representation, exact layer multiplicities and a nested-chain bound yield two distinct stationary occupancy transitions.

> Combining the routing-specific hierarchy with the established weak-mutation stationary law gives an exact aggregate-mode threshold and a separate half-mass threshold.

Unsafe wording:

- “first demonstration that multiplicity can defeat selection”;
- “new weakest-link epistasis framework”;
- “first representation-dependent evolutionary threshold”;
- “new mutation-selection equilibrium law”;
- “universal threshold `2^k-1`.”

## Submission consequence

The novelty gate is **PASS WITH CONDITIONAL WORDING**.

No additional abstract theorem is justified by this audit. The remaining scholarly work is bibliographic completion and reviewer-facing citation placement, not broadening the theorem. A later direct algebraic collision would require reframing, but none was identified in this source-level pass.
