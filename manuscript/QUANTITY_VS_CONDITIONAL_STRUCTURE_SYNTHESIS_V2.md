# Quantity versus conditional structure — ecological synthesis v2

Status: post-freeze conceptual synthesis. This document does **not** modify the frozen Evolution Letters V5 submission surface.

## Core revision

The useful contrast is not literally

\[
\text{quantity versus temporal order}.
\]

It is

\[
\boxed{
\text{permutation-invariant / marginal summaries}
\quad\text{versus}\quad
\text{conditional decision structure}.
}
\]

"Order" is a good intuition because adaptive policies observe one cue and then choose the next cue conditionally. But the mathematical object is richer than a fixed temporal ordering. It is a **decision topology**: which distinctions remain relevant after each possible observation.

This framing is both stronger and safer.

Ecology already contains structural theories:
- coarse- versus fine-grained environmental variation;
- interaction-sign and network structure;
- trophic coherence;
- state-dependent behavior;
- adaptive foraging.

The gap is narrower:

> many widely used ecological summaries are invariant to changes in conditional decision topology that can strongly alter the cost of ecological action.

---

## 1. Three classes of ecological description

### Class Q — quantity summaries

Examples:

- species richness;
- environmental variance;
- connectance;
- interaction-strength variance;
- cue entropy;
- marginal cue frequencies;
- pairwise mutual information.

These summarize **how much** heterogeneity, interaction or information is present.

Many are permutation-invariant: rearranging which states are conditionally linked to which future distinctions can leave the summary unchanged.

### Class S — structural summaries

Examples already present in ecology:

- spatial versus temporal grain;
- interaction sign structure;
- nestedness or trophic organization;
- covariance structure;
- network motifs;
- temporal autocorrelation.

These recognize that arrangement matters.

### Class D — conditional decision structure

The routeability framework introduces a more specific object:

\[
\text{observation history}
\longrightarrow
\text{which distinction/query is relevant next}.
\]

This is not captured by a scalar richness, variance or entropy alone, and need not be captured by ordinary static network structure.

It is task-dependent because the target action matters.

---

## 2. What the balanced theorem actually proves

The exact-balanced family proves:

- every available binary query can have the same maximal marginal entropy;
- every query can be exactly 50/50 balanced;
- yet the adaptive/fixed cost ratio can grow without bound as problem size grows.

Therefore:

\[
\boxed{
\text{marginal cue balance does not uniformly bound routeability advantage}.
}
\]

Important scope correction:

The asymptotic construction does **not** hold every conceivable ecological quantity fixed across family size. The number of represented worlds and available queries grows with the construction.

So the safe statement is:

> even perfect marginal balance of every cue is insufficient to control adaptive advantage uniformly.

Do **not** say:

> all quantities are fixed while the ratio becomes arbitrarily large.

The stronger fixed-size statement comes from matched task pairs, not from the asymptotic balanced family.

---

## 3. The stronger fixed-size result comes from the direct experiment

The existing four-state routeable versus bypass pair holds fixed:

- world count \(n=4\);
- query count \(m=3\);
- target balance;
- physical cue-vector support;
- cue frequencies;
- pairwise information signatures;
- full cue-only joint distribution.

Only the mapping from cue combinations to the focal target changes.

Yet:

\[
\text{routeable}: (C_A,C_F)=(2,3),
\]

\[
\text{bypass}: (C_A,C_F)=(2,2).
\]

Thus:

\[
\boxed{
P(Q_1,Q_2,Q_3)
\text{ does not identify }
(C_A,C_F)
\text{ without the target/action map }T.
}
\]

This is a sharper ecological statement than marginal insufficiency.

The environmental cue distribution can be identical while effective decision complexity differs.

---

## 4. Information quantity versus functional relevance

Donaldson-Matasci, Bergstrom & Lachmann (2010) explicitly note that mutual information is blind to function: it quantifies uncertainty reduction but not whether the information matters for the organism's response. Their fitness-value framework then connects information quantity to growth under particular optimization conditions.

The routeability distinction is complementary.

It asks not only:

> how much information does a cue contain about the environment or target?

but:

> after this cue outcome, which other information remains necessary for the action?

Thus two tasks can have matched low-order information summaries but different sequential acquisition requirements.

The correct novelty boundary is therefore not:

> information theory measures quantity; routeability discovers structure.

Decision theory already contains structural and order-based comparisons of information, including Blackwell-style informativeness relations.

The narrower ecological contribution is:

> environmental heterogeneity theory rarely treats **conditional acquisition architecture under finite ecological budgets** as an explicit property of the environment–organism–task relation.

---

## 5. Budget \(B\) is the true ecological coupling variable

The finite costs \(C_A\) and \(C_F\) are structural quantities.

They become ecological only when compared with a real resource constraint \(B\):

\[
\boxed{C_A\le B<C_F.}
\]

This is the genuine coupling point.

Possible biological meanings of \(B\):

- time before a flower closes or reward is lost;
- host residence / departure time;
- predator-exposure window;
- handling opportunity;
- energetic sampling budget;
- developmental decision window;
- attentional or working-memory constraint, if justified empirically.

The ecological environment enters the theory through two logically distinct channels:

1. **decision topology** — determines \(C_A,C_F\);
2. **ecological budget** — determines whether the structural difference matters in realized performance.

This separation is powerful because it prevents vague "information matters" interpretations.

---

## 6. A stronger general principle

The synthesis can be stated as:

> **Ecological consequences depend not only on the amount and distribution of heterogeneity, but on whether that heterogeneity changes the set of distinctions that must remain jointly unresolved under the organism's decision budget.**

Or more compactly:

\[
\boxed{
\text{amount of variation}
\neq
\text{conditional burden of resolution}.
}
\]

This is stronger than "diversity is not complexity" because it states what replaces raw diversity.

---

## 7. Stress-testing quantity-based ecological principles

The next theoretical program should not be "find another routeability example."

It should be:

> hold the established quantity-side predictor fixed as far as possible, vary conditional decision topology, and ask whether the classical prediction remains invariant.

### Program A — heterogeneity and niche breadth

Classical quantity-side predictor:
amount of environmental variation / heterogeneity.

Kassen's synthesis already recognizes that grain and other constraints matter, so the target is not to refute "heterogeneity matters."

The sharper question is:

> among environments matched in state richness, frequencies and relevant marginal variation, does routeability alter the information cost of generalism?

Design:
- same resource count;
- same resource frequencies;
- same cue marginals;
- matched reward distribution;
- different target-relevant routing architecture.

Prediction:
generalism should be cheaper only in the routeable environment when the ecological budget intersects the adaptive-only window.

### Program B — diversity / complexity and stability

Classical quantity-side summaries:
species richness \(S\), connectance \(C\), interaction-strength dispersion \(\sigma\).

Existing theory already shows that network organization can alter May-style stability, so routeability should not be sold as the first structural correction.

The routeability-specific question is:

> can two communities matched in ordinary complexity summaries generate different *behaviorally accessible* interaction matrices because decision topology differs?

The downstream stability effect would then be mediated by an endogenous accessibility filter.

This is a two-stage hypothesis:

\[
\text{decision topology}
\to
\text{accessible network}
\to
\text{community dynamics}.
\]

Only the first arrow is currently covered by routeability theory.

### Program C — fitness value of information

Classical quantity:
mutual information / entropy reduction / fitness value.

Stress test:
construct matched cue distributions and matched low-order information summaries but different adaptive acquisition costs.

The four-state routeable/bypass pair already provides the finite prototype.

The new question is:

> which scalar information quantities remain invariant while sequential cost or expected loss changes?

This is the cleanest bridge to information theory.

### Program D — specialist–generalist axis

Classical summary:
niche width / number or diversity of resources used.

Stress test:
fix niche breadth but vary hierarchical navigability of the resource set.

Prediction:
the same nominal generalist breadth can imply different sensing costs and therefore different feasibility under finite encounter budgets.

---

## 8. Nonidentifiability is the deeper unifying theme

The routeability program now contains several distinct nonidentifiability results.

### Environmental-summary nonidentifiability

The cue-only environmental distribution does not identify routeability without a target/action map.

The four-state matched experiment is an exact witness.

### Marginal-information insufficiency

Exact 50/50 cue marginals do not bound adaptive advantage.

The balanced family is an asymptotic witness.

### Network-response nonidentifiability

Observed binary interaction turnover does not identify latent ecological rewiring under unknown detection.

The Villavicencio interior witness is an exact observation-model counterexample.

These should not be collapsed into one theorem, but they share a methodological message:

> observed summaries identify only what their measurement map preserves.

This provides a bridge from finite decision theory to ecological inference.

---

## 9. "Reality claim" versus "model claim"

A useful taxonomy for ecological principles is:

### Reality claim

A statement about the biological system itself, e.g.

> environmental heterogeneity increases the realized cost of generalism.

To support this, the measurement must identify the relevant mechanism or outcome.

### Model claim

A statement conditional on a representation, e.g.

> under a state representation summarized by variance \(V\), predicted niche breadth increases with \(V\).

If different hidden decision topologies share the same \(V\) but imply different feasible behavior, then the scalar principle is not false; it is incomplete with respect to that hidden axis.

The role of routeability is therefore often **diagnostic**, not destructive:

> it identifies when an ecological scalar is insufficient for the mechanism being claimed.

This is a stronger and more defensible use of nonidentifiability than saying existing ecological laws are wrong.

---

## 10. Why the current deterministic theory is enough for V5

Current assumptions:

- finite states;
- deterministic cues;
- additive costs;
- worst-case objective;
- guaranteed exact resolution.

These assumptions define an idealized limit.

Within that limit the present paper can establish:

1. conditional decision topology is a distinct structural axis;
2. marginal balance does not control its value;
3. identical cue distributions need not identify decision complexity;
4. a hard ecological budget exposes when the structural axis affects performance.

That is already a complete qualitative theory.

It is not necessary to solve noisy, expected-loss ecology before submitting V5.

---

## 11. The next quantitative theory

The natural extension replaces exact resolution by stochastic decision loss.

A generic future object would be

\[
C_A^\epsilon
=
\min_\pi
\left\{
\mathbb E[\text{acquisition cost}]
:
\Pr(\text{error under }\pi)\le\epsilon
\right\},
\]

or, more generally,

\[
V_A
=
\inf_\pi
\mathbb E[
L(T,\hat T)
+
\lambda\,\text{acquisition cost}
].
\]

Compare with a fixed-acquisition analogue \(V_F\).

New questions:

- Does a stochastic routeability gap remain?
- Which deterministic theorems survive under small error?
- Can marginal mutual information still fail to identify optimal sequential cost?
- What replaces the hard budget window?
- Can Blackwell order / rate-distortion / sequential experiment design provide the right prior-art language?

This is a separate paper.

Do not import it into V5 merely to make the present theory look more realistic.

---

## 12. Recommended V5-level statement

The strongest safe conceptual claim is:

> **Many ecological summaries quantify the amount or marginal distribution of heterogeneity. Routeability captures a different property: the conditional structure of the distinctions an organism must resolve. These axes are not interchangeable. Even perfectly balanced cues can support arbitrarily large adaptive advantages, and identical physical cue distributions can define tasks with different decision costs once the action map changes. Ecological consequences arise when those structural differences intersect a finite biological decision budget.**

## Stop rule

For V5:
- do not derive a stochastic extension;
- do not reopen the manuscript to challenge four literatures at once;
- use quantity-versus-conditional-structure as the conceptual interpretation of the existing theorem stack.

For follow-up theory:
- develop expected-loss / noisy-cue routeability;
- connect explicitly to Blackwell ordering, rate-distortion and sequential information acquisition;
- test quantity-based ecological principles by matched-summary / altered-topology constructions.
