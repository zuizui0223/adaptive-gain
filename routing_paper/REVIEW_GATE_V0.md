# Internal reviewer gate v0

## Verdict

**Promising theorem paper, not yet submission-ready.**

The current manuscript has a clean mathematical spine and a disciplined novelty boundary, but one conceptual vulnerability is large enough that it should be repaired before journal targeting: the headline threshold is currently a threshold for the **modal aggregate gain layer**, not for stationary majority or another clearly population-dominance quantity.

## Major concern 1 — why is aggregate mode the biologically relevant estimand?

The sharp theorem at

`theta_c=2^k-1`

is mathematically exact, but “modal layer” can look chosen because it produces a closed-form threshold.

For the canonical running example `q=2,k=3`, at `theta=7` the layer weights are

`(19,49,49)`.

The full-gain layer is tied for the mode, yet its stationary mass is only

`49/117 < 1/2`.

A reviewer can therefore ask:

> Why should becoming the largest single gain class count as evolutionary dominance if most stationary probability still lies outside the full-gain class?

This is the strongest current threat to the paper’s conceptual importance.

### Recommended repair

Add a **stationary-majority threshold** within the same finite routing model, not a new unrelated theory branch.

For symmetric tilt,

`P_full(theta) = 1 / (1 + sum_{s=1}^q A_s theta^{-s})`.

Therefore the half-mass boundary is the unique positive solution of

`sum_{s=1}^q A_s theta^{-s}=1`,

or equivalently

`theta^q = sum_{s=1}^q A_s theta^{q-s}`.

The same global bound immediately gives a sharp universal bracket:

- for `q=1`, the half-mass threshold equals `T_k=2^k-1`;
- for `q>=2`, `T_k < theta_1/2 < 2 T_k`.

The lower inequality follows because the adjacent term alone equals one at `theta=T_k` and additional lower layers contribute positive mass. The upper inequality follows from

`A_s <= T_k^s`

and

`sum_{s=1}^q (1/2)^s < 1`.

This would let the paper distinguish two biologically interpretable transitions:

1. **mode threshold** — full gain becomes the largest gain class;
2. **majority threshold** — full gain contains at least half of stationary mass.

The mode theorem remains the exact closed-form centerpiece; majority becomes a natural occupancy corollary rather than a competing theory.

## Major concern 2 — theorem-level novelty is a composition, not difficult isolated mathematics

Each isolated ingredient is elementary or established:

- difference-of-powers layer counts are elementary;
- the nested-chain inequality has a short proof;
- origin-fixation stationary weighting is prior art;
- selection versus multiplicity is prior art.

The defensible contribution is their exact composition for the declared finite routing representation.

### Consequence

The paper must earn importance through **interpretation and boundary control**, not by implying pure-mathematical depth. Figure 2 and the Discussion should emphasize that one adjacent-layer obstruction controls the complete lower-layer hierarchy and that the threshold changes under alternative representations.

## Major concern 3 — biological interpretation remains conditional

No empirical system currently qualifies the branch-product genotype-policy map, local mutation coordinates, and neutral measure strongly enough to present `2^k-1` as a measured biological threshold.

### Consequence

This is acceptable for a theory paper, but it limits how high the journal target can be without either:

- a persuasive biological case study that independently qualifies the representation; or
- a broader class theorem showing the routing result captures a meaningful family rather than one chosen encoding.

The present manuscript should not fake the former or add the latter merely for breadth.

## Major concern 4 — representation counterexample is essential, not optional

Without the compressed-chain contrast, the main theorem can be read as a property of weakest-link fitness itself. The exact `q=2,theta=2` contradiction makes clear that the result is about **representation-induced multiplicity**.

### Consequence

Keep representation dependence in the main text and Figure 3 even though generic representation dependence is prior art.

## Minor concern 1 — “dominant” is ambiguous

Use precise terms:

- “aggregate-modal gain layer” for the largest single gain class;
- “stationary majority” for mass at least `1/2`;
- “per-genotype mode” only when explicitly discussing individual states.

Avoid “dominant” without qualification.

## Minor concern 2 — title may overpromise a generic principle

Current working title:

**Finite routing representations create sharp selection–multiplicity thresholds**

is usable, but “selection–multiplicity thresholds” could sound more general than the theorem.

Safer alternatives after majority analysis:

- **Exact occupancy thresholds in finite routing representations**
- **Finite routing architecture sets exact thresholds for stationary gain occupancy**
- **Representation-induced multiplicity sets sharp stationary thresholds in finite routing models**

Do not freeze title yet.

## Minor concern 3 — prior art should include explicit multiplicity-selection equilibrium work

Riedel et al. (2015) use multiplicity parameters based on the number of sequence variants representing states and combine them with selection in low-mutation equilibrium statistics.

This is stronger prior art than citing only generic neutral networks or survival of the flattest.

### Consequence

Add Riedel et al. explicitly in the Introduction’s prior-art paragraph in the next prose pass.

## Recommended next action

**Do one mathematical repair only: stationary-majority threshold characterization.**

Do not reopen coupon-collector, mesoscopic, rate-scale, or downstream-process theory.

After majority is frozen:

1. revise Abstract/Introduction to distinguish mode and majority;
2. update Figure 2 to show both thresholds;
3. rerun novelty audit;
4. then choose journal target.

## Current impact assessment

Without the majority repair or empirical representation qualification, the paper is mathematically clean but risks being judged as an elegant note around an elementary count plus standard stationary weighting.

With mode + majority occupancy transitions, representation counterexample, and mutation-measure claim ceiling all in one compact story, it becomes a substantially more complete theoretical result while remaining disciplined.