# Internal reviewer gate v0

## Verdict

**Major conceptual repair and manuscript synchronization complete; the paper is ready for focused collision review and journal-fit evaluation, not more abstract theorem expansion.**

The previous largest vulnerability was that the headline `2^k-1` result concerned the **modal aggregate gain layer**, while the manuscript risked letting “mode” carry an implicit majority interpretation. PR #58 closed that mathematical gap, and the manuscript surface has now been synchronized to the resulting two-threshold structure.

## Closed concern 1 — aggregate mode versus stationary majority

The manuscript treats two occupancy estimands explicitly.

### Aggregate mode

With `T_k=2^k-1`, the full-gain layer is:

- nonmodal for `theta<T_k`;
- tied exactly with the adjacent layer at `theta=T_k`;
- uniquely modal for `theta>T_k`.

### Stationary majority

The normalized full-gain mass is

`P_full(theta)=1/(1+sum_{s=1}^q A_s theta^{-s})`.

Its unique half-mass threshold `theta_1/2(q,k)` satisfies

`theta^q=sum_{s=1}^q A_s theta^(q-s)`.

For `q>=2`,

`T_k < theta_1/2 < 2T_k`.

Thus the manuscript no longer treats “largest single gain class” as synonymous with “most stationary probability.”

### Canonical consequence

For `k=q+1`, Moran step `a=2` and `q>=2`:

- first unique aggregate mode: `N=q+2`;
- first stationary majority: `N=q+3`.

The one-step separation is exact. For `q=2`, the majority threshold is `(7+5sqrt(5))/2`, between 9 and 10.

**Status: CLOSED.**

## Closed concern 2 — manuscript surfaces disagreed about the majority result

The following files now all encode the same mode-versus-majority distinction:

- `ABSTRACT_V0.md`;
- `INTRODUCTION_V0.md`;
- `MODEL_AND_RESULTS_V0.md`;
- `DISCUSSION_V0.md`;
- `MANUSCRIPT_SPINE_V1.md`;
- `CLAIM_LEDGER_V1.md`;
- `FIGURE_PLAN_V1.md`;
- `PROVENANCE_V1.md`;
- `NOVELTY_AUDIT_V0.md`;
- this review gate.

Figure 2 explicitly marks both thresholds and the interval in which full gain is already the largest class but remains below one-half stationary mass.

**Status: CLOSED.**

## Remaining major concern 1 — theorem-level novelty is a composition, not difficult isolated mathematics

Each isolated ingredient is elementary or established:

- difference-of-powers layer counts are elementary;
- the nested-chain inequality has a short proof;
- origin-fixation stationary weighting is prior art;
- selection versus multiplicity is prior art;
- a monotone half-mass root is not a novel object by itself.

The defensible contribution is the exact **composition** for the declared finite routing representation:

`routing representation -> exact multiplicity hierarchy -> one adjacent obstruction -> paired mode/majority occupancy thresholds -> explicit representation/mutation-measure claim ceiling`.

### Reviewer criterion

If a direct prior source already contains this same finite-class composition or an algebraically identical theorem under a different name, the paper must be reframed. If only the components are prior art, the current conditional theorem story remains defensible.

## Remaining major concern 2 — biological interpretation is conditional

No empirical system currently qualifies the branch-product genotype-policy map, local mutation coordinates, and neutral measure strongly enough to present either threshold as a measured biological law.

### Consequence

This is acceptable for a compact theory paper, but the manuscript must maintain the explicit conditional language:

> for this finite routing representation

rather than

> biological routing systems require...

The representation counterexample and mutation-measure counterexample must remain in the main text because they are part of the claim, not boilerplate limitations.

## Remaining major concern 3 — journal scope depends on what is claimed as the contribution

The paper should not be pitched as:

- a new mutation-selection framework;
- a new weakest-link epistasis theory;
- a universal entropy threshold;
- a broad empirical eco-evolutionary result.

It should be pitched as a compact mathematical-biology result on how an explicit finite genotype-policy representation converts phenotype-level selection into two exact stationary occupancy transitions.

Without empirical representation qualification, the natural target class is a strong theoretical/mathematical biology journal rather than a top general ecology journal.

## Essential scope controls

### Representation contrast

Keep the compressed-chain contrast in the main paper. It demonstrates that the thresholds are not identified by gain values and fitness schedule alone.

### Neutral mutation measure

Keep the fixed-support mutation-bias construction in the main paper or concise main-text proposition. It demonstrates that raw genotype multiplicity is only the relevant abundance measure under the symmetric neutral measure.

Removing either control would make the threshold look more universal than it is.

## Terminology rules

Use:

- “per-genotype mode” for the most probable individual genotype;
- “aggregate-modal gain layer” for the largest gain class;
- “stationary majority” for full-gain mass `>=1/2`.

Avoid unqualified “dominant,” “takes over,” or “wins.”

## Title guidance

Preferred current title:

**Exact occupancy thresholds in finite routing representations**

This is safer than a generic “selection–multiplicity threshold” title because it tells the reader that the result is conditional on a representation and that more than one occupancy threshold is studied.

## Next action gate

Do **not** add another theorem.

The next work is now:

1. pass clean three-version CI on the synchronized manuscript surface;
2. perform one deeper scholarly collision search on the exact four objects in `NOVELTY_AUDIT_V0.md`;
3. assess journal fit using the completed mode-plus-majority manuscript;
4. only then decide whether figures and submission formatting are worth building.

## Current impact assessment

The mode-only version risked reading as an elegant note built around a conveniently selected statistic. The mode-plus-majority version is substantially stronger: the same representation-specific combinatorics now explains two distinct stationary occupancy transitions, and the canonical family gives an exact separation between becoming the largest class and becoming most of the stationary distribution.

This is now a coherent theorem paper. Its remaining risk is **priority/scope**, not an internal mathematical gap.