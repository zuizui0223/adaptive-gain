# Mathematical–ecological synthesis v1 — balanced routeability

Status: post-freeze synthesis / follow-up design. This document does **not** modify the frozen Evolution Letters V5 submission surface.

## Central synthesis

The mathematical and ecological results are different expressions of one principle:

\[
\boxed{
\text{marginal cue statistics}
\neq
\text{decision architecture}
}
\]

and therefore

\[
\boxed{
\text{environmental diversity or cue entropy}
\neq
\text{decision-relevant ecological complexity}.
}
\]

The mathematical exact-balanced results show that every available binary cue can be globally 50/50 balanced and yet adaptive versus fixed resolution can differ without bound.

The ecological routeability contrast shows something complementary and experimentally stronger: two tasks can share the same physical cue vectors, cue frequencies, pairwise information signatures, and full cue-only joint distribution, while differing in \(C_A\), \(C_F\), and the value of contingent access because the cue surface maps differently onto the focal action.

Together they identify routeability as a **higher-order relational property of ecological alternatives, cues, and actions**, rather than a property of richness, one-cue informativeness, marginal entropy, or cue covariance alone.

---

## 1. Translation dictionary

| Mathematical object | Ecological interpretation |
| --- | --- |
| represented world \(w\) | resource, host, partner, habitat state, predator context, or other ecological alternative |
| target \(T(w)\) | focal action: accept/reject, attack/avoid, exploit/leave, mate/reject, etc. |
| query \(q\) | observable cue channel or sampling action |
| query outcome | physical/sensory state of that cue |
| \(n\) | number of represented ecological alternatives |
| \(m\) | number of available cue channels |
| \(C_A\) | minimum worst-case cue cost when the next observation may depend on previous outcomes |
| \(C_F\) | minimum cue burden when a fixed cue bundle must be provisioned without contingent routing |
| \(g=C_F-C_A\) | routeability advantage |
| adaptive depth \(h\) | maximum sequential observation budget per encounter |
| private cross-target pair | an irreducible ecological distinction that only one cue can resolve within the declared vocabulary |
| decision-equivalence class | ecological states that require the same focal action and continuation distinctions |
| \(D_h(n)\) | maximum fixed-side burden compatible with ecological navigation using at most \(h\) contingent observations |

---

## 2. Why exact 50/50 balance has ecological meaning

Under a uniform distribution over represented alternatives, an exactly balanced binary cue has maximal marginal entropy:

\[
H(q)=1\text{ bit}.
\]

Therefore an exact-balanced theorem removes a natural low-order explanation for adaptive advantage.

If every cue is 50/50:
- no cue is globally rare;
- no cue is globally almost constant;
- every cue has the same marginal entropy;
- adaptive advantage cannot be attributed simply to one strongly skewed routing cue.

Yet the repository constructs families with

\[
\frac{C_F}{C_A}\to\infty.
\]

Ecological interpretation:

> even when every available cue is maximally variable across environmental alternatives, the information burden of interaction can depend arbitrarily strongly on **which distinctions become relevant after which earlier observations**.

Thus marginal cue diversity or entropy is not enough to quantify effective ecological complexity.

---

## 3. The direct experiment is the causal counterpart

The existing four-state routeability experiment uses the same physical cue-vector support in routeable and bypass architectures:

\[
000,\ 001,\ 011,\ 111.
\]

The two treatments share:
- four states;
- identical physical cue combinations;
- identical cue frequencies;
- identical target balance;
- identical canonical pairwise information signatures;
- identical cue-only joint distribution.

Only the mapping from cue combination to focal target/action differs.

Exact costs:

\[
\text{routeable}: (C_A,C_F)=(2,3),
\]

\[
\text{bypass}: (C_A,C_F)=(2,2).
\]

Therefore the experiment isolates the **relational mapping between environmental cue structure and ecological action**, rather than physical cue diversity.

This is more than a demonstration that animals can learn sequential cues.

It tests:

> can the same physical environmental cue surface impose different behavioral costs solely because its distinctions are organized differently relative to the focal action?

That is the direct experimental form of the V5 claim.

---

## 4. Nested hierarchy of controls

The theory and experiment provide progressively stronger controls.

### Level A — same richness

Hold \(n\) fixed.

This removes raw number of alternatives as the explanation.

### Level B — same cue marginals

Match per-cue outcome frequencies.

This removes simple cue prevalence as the explanation.

### Level C — exact global balance

Require every binary cue to be 50/50.

This removes marginal cue entropy differences.

### Level D — same pairwise information surface

Match all target–cue and cue–cue pairwise information signatures.

This removes ordinary pairwise association strength.

### Level E — same full cue-only joint distribution

Use exactly the same physical cue vectors with the same frequencies.

This removes environmental cue-distribution differences altogether.

At Level E, what remains different is the relationship:

\[
\boxed{
\text{cue state}
\longrightarrow
\text{ecological action}.
}
\]

This is routeability in its cleanest form.

---

## 5. A general ecological principle

The combined theory suggests:

> **Ecological complexity is the geometry of distinctions that must remain jointly unresolved, not the amount of environmental variation considered marginally.**

This yields several equivalent contrasts:

\[
\text{biodiversity}
\neq
\text{decision complexity},
\]

\[
\text{cue entropy}
\neq
\text{decision complexity},
\]

\[
\text{pairwise cue information}
\neq
\text{decision complexity},
\]

\[
\text{environmental turnover}
\neq
\text{decision turnover}.
\]

A change matters through this mechanism only when it changes the target-relevant conditional geometry.

---

## 6. Ecological interpretation of the balanced fixed-side theorem

For exact-balanced binary environments with even \(n\ge6\),

\[
\max C_F=n-3.
\]

The unrestricted fixed-side cap is \(n-1\).

Ecological interpretation:

> requiring every cue to divide ecological alternatives evenly limits how many cue channels can all be independently indispensable for a fixed discrimination strategy.

This is a finite structural constraint on environmental decision architecture.

It should **not** be interpreted as a universal natural-law ceiling on animal cognition. It is conditional on:
- deterministic cues;
- exact target resolution;
- unit cue costs;
- uniform represented-state balance;
- the declared cue vocabulary.

The value is comparative: it identifies what perfect marginal balance does and does not constrain.

---

## 7. Ecological interpretation of star--edge--star equality

At the fixed cap, the minimum resolver has a rigid private-pair normal form:

\[
(n/2-1,\ 2,\ n/2-1)
\]

with two stars and one edge.

A cautious ecological interpretation is:

> maximum fixed irredundance under perfect cue balance requires a highly organized modular pattern of unique discriminations.

The star--edge--star motif should not be claimed as a naturally universal community motif.

Its best biological uses are:
1. a controlled stimulus architecture;
2. a null/extremal reference for comparing natural systems;
3. a constructive explanation for why high fixed burden requires many branch-exclusive distinctions.

---

## 8. Ecological meaning of \(D_h(n)\)

Define

\[
D_h(n)=\max\{C_F:C_A\le h\}.
\]

Ecologically, \(h\) can represent a hard per-encounter observation budget:
- limited handling time;
- host departure;
- predator exposure;
- flower residence time;
- energetic sampling capacity;
- finite attention before action.

Then \(D_h(n)\) asks:

> how much latent fixed discrimination burden can an environment contain while still being navigable with at most \(h\) contingent observations?

This is a direct bridge from extremal combinatorics to ecology.

The ecological meaning is not the exact integer value in every natural system. The important result is the existence of a **feasibility frontier** between:
- environmental decision architecture;
- sequential observation budget;
- guaranteed action resolution.

Finite compatibility defects such as \(D_3(10)=6\) show that richness, cue balance and observation budget do not combine through a simple monotone scalar formula.

---

## 9. Budget-window prediction

For any ecological task,

\[
C_A\le B<C_F
\]

is the routeability-sensitive budget window.

This connects the exact math directly to the existing experiment.

### Below the window

\[
B<C_A.
\]

Even contingent routing is insufficient.

### Inside the window

\[
C_A\le B<C_F.
\]

Contingent access can succeed while fixed access cannot guarantee resolution.

### Above the window

\[
B\ge C_F.
\]

Routeability loses its unique performance advantage because the whole fixed bundle fits.

The current experiment already implements this as

\[
B=1,\ 2,\ 3
\]

with a predicted architecture × access interaction only at \(B=2\).

Thus the ecological experiment is not merely inspired by the theorem; it manipulates the exact mathematical phase boundary.

---

## 10. Strongest empirical theorem-to-experiment chain

The clean synthesis is:

\[
\boxed{
\begin{aligned}
&\text{same physical environmental cue surface}\\
&\downarrow\\
&\text{different cue-to-action conditional geometry}\\
&\downarrow\\
&\text{different }(C_A,C_F)\\
&\downarrow\\
&\text{different performance only in }C_A\le B<C_F\\
&\downarrow\\
&\text{testable architecture}\times\text{access}\times\text{budget interaction}.
\end{aligned}
}
\]

This is a genuine mathematics-to-ecology-to-experiment chain.

---

## 11. Two complementary experimental tiers

### Tier 1 — minimal causal routeability experiment

Keep the current four-state / three-cue design.

Advantages:
- smallest strict-gain architecture;
- same physical cue vectors across treatments;
- same pairwise information surface;
- simple \(B=1,2,3\) ladder;
- practical for animal learning.

This should remain the first biological experiment.

### Tier 2 — exact-balanced stress test

A later experiment can instantiate an exact-balanced finite witness, for example the eight-world / five-query balanced task with

\[
(C_A,C_F)=(3,5).
\]

All five cues split the eight states 4:4.

This tests the stronger proposition:

> routeability matters even when every individual cue has identical maximal marginal entropy.

A matched balanced control should preserve:
- eight physical states;
- five 4:4 cue marginals;
- target balance;
- cue costs;
- exposure schedule;

while reducing or eliminating the adaptive-fixed gap.

This is scientifically attractive but operationally more demanding, so it should not replace the minimal four-state first experiment.

---

## 12. Natural-system prediction

For natural ecological data, do not attempt to estimate routeability from species counts alone.

Instead measure or infer:
1. the focal action classes;
2. candidate environmental states;
3. available cue channels;
4. cue-state incidence;
5. cue costs or observation order;
6. target-relevant decision-equivalence classes.

Then estimate:
- \(C_A\);
- \(C_F\);
- \(g=C_F-C_A\);
- whether the natural observation budget lies in the routeability-sensitive window.

Predictions:

### P1 — richness decoupling
Species-rich systems can have small \(C_A\) if many alternatives fall into shared conditional branches or decision-equivalence classes.

### P2 — marginal-information failure
Cue entropy or pairwise cue–target association will not necessarily predict \(g\).

### P3 — interaction accessibility
Among morphology/phenology/encounter-compatible interactions, links requiring expensive non-routeable discrimination should be less behaviorally accessible under finite budgets.

### P4 — turnover asymmetry
Turnover within a decision-equivalence class can be decision-silent, whereas small compositional changes crossing a decision boundary can alter \(C_A\), \(C_F\), or both.

These are empirical hypotheses, not consequences guaranteed by the finite theorem alone.

---

## 13. Paper architecture

The mathematics and ecology should be connected across papers without forcing every result into one manuscript.

### Paper 1 — V5 initial theory

Headline:
environmental routeability separates raw heterogeneity from effective ecological complexity.

Use the balanced theorem as a strong structural counterexample / supporting proof.

Do not delay submission to add experiments.

### Paper 2 — balanced finite-search mathematics

Headline:
exact-balanced query systems have rigid finite extremal geometry, finite compatibility defects, and unbounded asymptotic adaptive advantage.

Pure mathematical contribution.

### Paper 3 — direct ecological experiment

Headline:
holding the physical cue environment fixed, changing only cue-to-action architecture changes the value of contingent information in the predicted budget window.

This is the causal ecological validation.

The three papers share one conceptual backbone but own different claims.

---

## 14. One-sentence synthesis

> **Environmental routeability is the ecological manifestation of a finite combinatorial fact: globally similar or even perfectly balanced cues can impose radically different decision costs because contingent value is determined by conditional separation geometry rather than marginal information.**

## Claim boundary

The exact finite theorems concern deterministic target resolution under declared query constraints.

The ecological translations are hypotheses about biological decision-making unless directly tested.

The direct artificial-flower experiment can establish a causal behavioral consequence of routeability in that task, but does not by itself establish natural-network rewiring, niche-breadth evolution, or ecosystem-level effects.

## Stop rule

Do not reopen frozen V5 to absorb this synthesis.

Use this document to:
- sharpen interpretation of the existing V5 mathematics;
- guide the direct experiment;
- motivate a later exact-balanced experimental stress test.
