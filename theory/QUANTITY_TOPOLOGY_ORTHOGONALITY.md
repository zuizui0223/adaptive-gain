# Quantity versus conditional decision topology

Status: post-freeze synthesis theorem / ecological interpretation. This file does **not** modify the frozen Evolution Letters V5 submission surface.

## 1. The distinction

Ecology already contains many kinds of structure:
- Levins-style coarse versus fine environmental grain;
- spatial and temporal heterogeneity;
- network topology;
- covariance and autocorrelation;
- interaction-strength distributions.

The missing axis proposed here is therefore not generic "order" or generic "topology".

It is more specific:

> **outcome-contingent decision topology** — whether the result of an early observation changes which later distinctions remain necessary for the focal action.

This is the structural content of routeability.

Many familiar ecological summaries are quantitative or low-order:
- number of states or species;
- variance or entropy of environmental states;
- cue frequencies;
- connectance;
- total or pairwise information;
- temporal autocorrelation.

Those summaries can be biologically important without identifying conditional decision topology.

## 2. Exact quantity-matched topology contrast

Use the existing exactly-balanced binary family with routing depth

\[
d\ge2,\qquad k=2^d.
\]

It has:
- \(2k+2\) represented worlds;
- \(d+k\) binary unit-cost queries;
- every query exactly 50/50 balanced;
- routeable target map with
  \[
  C_F\ge k,\qquad C_A\le d+1.
  \]

Now keep **the entire physical query matrix unchanged** and change only the target/action map.

Define the control target from the first two routing bits:

\[
T_{\mathrm{control}}(w)=
\begin{cases}
0,&q_0(w)=q_1(w),\\
1,&q_0(w)\ne q_1(w).
\end{cases}
\]

Then the first two routing queries form a fixed resolving set.

No single query can resolve the control target: every query has outcome classes of size \(k+1,k+1\), whereas the target classes have sizes \(k+2,k\).

Therefore exactly

\[
\boxed{
C_A^{\mathrm{control}}
=
C_F^{\mathrm{control}}
=
2.
}
\]

The routeable and control tasks have exactly the same:
- represented worlds and world count;
- query identities and query count;
- query costs;
- full query outcome matrix;
- every per-query marginal;
- every cue-cue joint distribution;
- the full cue-only joint distribution;
- target multiplicities \((k+2,k)\);
- target entropy under a uniform world distribution.

Because the full query vocabulary resolves the target in both tasks and target entropy is identical,

\[
I(T;Q_{\mathrm{all}})=H(T)
\]

is also identical in both tasks under the uniform world prior.

Yet:

\[
\frac{C_F}{C_A}
\ge
\frac{2^d}{d+1}
\]

in the routeable task, while

\[
\frac{C_F}{C_A}=1
\]

in the matched control.

Hence the matched ratio difference obeys

\[
\boxed{
\frac{C_F^{R}}{C_A^{R}}
-
\frac{C_F^{K}}{C_A^{K}}
\ge
\frac{2^d}{d+1}-1
\to\infty.
}
\]

This is a direct orthogonality witness:

> **environmental quantity and total available target information can be held fixed while conditional decision topology changes without bound in its adaptive consequence.**

The executable construction is in:

- adaptive_gain/balanced_quantity_topology_contrast.py
- tests/test_balanced_quantity_topology_contrast.py

## 3. What this does and does not say about ecological information theory

This result does **not** refute information-fitness theory.

Donaldson-Matasci et al., Rivoire & Leibler and related work ask how environmental information affects fitness under specified environmental, cue and response mappings. Those frameworks can incorporate biologically meaningful mappings and are not reducible to one scalar mutual-information number.

The narrower conclusion is:

> **the total amount of target information available in a cue set does not identify the acquisition architecture needed to obtain the relevant information sequentially.**

Two environments can satisfy

\[
I(T;Q_{\mathrm{all}})=H(T)
\]

and have the same cue-only distribution while differing strongly in:
- how many cues must be provisioned non-contingently;
- how many cues are needed along one realized path;
- whether a finite encounter budget exposes a contingent advantage.

Thus information amount and information access topology are distinct coordinates.

## 4. What this adds to heterogeneity theory

Levins and later niche-breadth theory already distinguish the amount, spatial/temporal pattern and grain of environmental variation.

The proposed addition is not a replacement for grain.

Two environments can have the same:
- state frequencies;
- cue distributions;
- state count;
- temporal schedule;
- coarse/fine grain;

yet differ in whether early observations make different later information conditionally relevant.

Therefore a useful decomposition is:

\[
\boxed{
\text{ecological heterogeneity}
=
\text{distributional structure}
+
\text{decision topology relative to a focal action}.
}
\]

The second term is relational. It cannot be defined from the environment alone without specifying:
- the focal action;
- the available cue vocabulary;
- cue costs;
- which distinctions remain relevant after each observation.

## 5. A blindness test for quantity-based ecological principles

For any proposed ecological summary \(S\), ask:

1. Can two systems be constructed with the same \(S\)?
2. Can their conditional decision topology differ?
3. If so, does the ecological prediction change once a finite observation budget is imposed?

If yes, then \(S\) is not wrong; it is **insufficient for routeability-sensitive predictions**.

This gives a disciplined way to test existing principles without pretending to invalidate them wholesale.

### Candidate A — heterogeneity and niche breadth

Hold fixed:
- number/frequency of environments or resources;
- physical cue distribution;
- target prevalence.

Vary:
- cue-to-action topology.

Question:
does the information cost of broad resource use differ at the same measured heterogeneity?

### Candidate B — information value

Hold fixed:
- target entropy;
- full available target information \(I(T;Q_{\mathrm{all}})\);
- cue-only distribution.

Vary:
- conditional acquisition topology.

Question:
does a finite sampling budget distinguish systems with the same total available information?

### Candidate C — specialist/generalist classification

Hold fixed:
- number of usable resource states;
- resource frequencies;
- reward distribution.

Vary:
- whether resources are navigable by branch-specific cues.

Question:
can the same nominal niche breadth impose different per-encounter information burdens?

### Candidate D — diversity/interaction complexity

Hold fixed:
- species/state richness;
- upstream compatibility set;
- marginal cue statistics.

Vary:
- decision-equivalence structure and conditional branching.

Question:
does the behaviorally accessible interaction set change even when conventional diversity summaries do not?

These are tests of **summary sufficiency**, not attempts to declare the established ecological principle false.

## 6. The ecological currency enters through the budget

The finite costs \(C_A\) and \(C_F\) are structural quantities.

They become ecological only after specifying a biologically meaningful budget \(B\).

The exact regime is

\[
\boxed{
C_A\le B<C_F.
}
\]

Possible currencies include:
- time before a flower/host opportunity closes;
- predator-exposure window;
- handling-time ceiling;
- energetic sampling budget;
- attention/sensory-acquisition budget.

The integration therefore has a clean factorization:

\[
\text{decision topology}
\to
(C_A,C_F)
\]

and

\[
\text{ecological constraint}
\to
B.
\]

Their intersection,

\[
C_A\le B<C_F,
\]

determines whether routeability is performance-relevant.

This keeps the combinatorics and ecology conceptually distinct while making their interaction exact.

## 7. Identification consequence

A quantity-only dataset need not identify decision topology.

For example, observing only:
- species counts;
- cue marginals;
- cue entropy;
- pairwise association;
- endpoint network links;

does not in general reveal:
- which cue was sampled first;
- which later cue became relevant after each outcome;
- which alternatives were still behaviorally confusable;
- which action map generated the classification problem.

Therefore routeability requires richer data.

### Minimum routeability data object

For each focal decision, record:

1. represented ecological alternative;
2. focal target/action;
3. available cue identities;
4. cue outcomes by alternative;
5. acquisition cost or timing;
6. observed acquisition order when relevant;
7. conditional next-cue rule or enough data to infer it.

Without the action map and conditional acquisition structure, many routeability claims are not identified.

This identification issue is distinct from the Villavicencio detection problem, but the logic is parallel:

> some ecological mechanisms cannot be recovered from a summary response surface because different latent structures map to the same observed summary.

## 8. Direct experimental hierarchy

### Experiment 1 — minimal causal test

Use the existing four-state / three-cue matched routeable versus bypass design.

It already holds fixed:
- physical cue vectors;
- cue frequencies;
- pairwise information signatures;
- full cue-only joint distribution.

It tests the budget localization:

\[
\Delta_{B=1}=0,\qquad
\Delta_{B=2}>0,\qquad
\Delta_{B=3}=0.
\]

This is the first biological test.

### Experiment 2 — exact-balanced stress test

Use a larger exact-balanced witness/control pair.

At every depth \(d\), use the same physical cue matrix in both treatments.

Only the target/action map changes.

The matched control has

\[
C_A=C_F=2,
\]

while the routeable treatment satisfies

\[
C_F/C_A\ge2^d/(d+1).
\]

This directly tests whether behavior is sensitive to conditional topology even when:
- all individual cue marginals are perfectly balanced;
- the entire cue distribution is physically identical;
- target prevalence and total available target information are matched.

This is a later experiment, not a prerequisite for V5.

## 9. Boundary to the next theory paper

The current theory is:
- deterministic;
- worst-case;
- exact-resolution;
- additive-cost.

The next quantitative ecological theory should relax those assumptions.

Natural extension:

\[
C_A^{\mathrm{risk}}
=
\inf_\pi
\mathbb E[
\text{acquisition cost}
+
\lambda\,\text{decision loss}
]
\]

versus an analogous fixed-policy optimum.

Needed ingredients:
- stochastic cue likelihoods;
- nonzero classification error;
- expected rather than worst-case cost;
- satisficing thresholds;
- heterogeneous encounter durations;
- potentially state-dependent cue costs.

The key future question is whether the quantity/topology orthogonality survives when exact resolution is replaced by expected loss.

That is a distinct paper.

## Claim precision — topology is not invisible to complete structural data

The orthogonality claim concerns aggregate, marginal, low-order, and total-information summaries that omit the complete action-conditioned cue structure.

It must **not** be stated as "no amount of measurement can recover topology."

If one observes the complete joint mapping

\[
(w,\ T(w),\ q_1(w),\ldots,q_m(w))
\]

together with cue costs, then the deterministic finite decision problem is specified and \(C_A\) and \(C_F\) can in principle be computed.

The matched constructions instead show something sharper and safer:

> even very strong quantity matching — including the entire cue-only distribution, target prevalence, target entropy and total full-vocabulary target information — does not determine sequential acquisition topology.

The missing information is precisely the higher-order **action-conditioned arrangement** of cue states.

## 10. Current-paper ceiling

The present V5 need establish only:

> **conditional decision topology is an ecological axis not determined by standard marginal summaries of heterogeneity or information.**

It does not need to claim:
- that traditional heterogeneity theory is wrong;
- that all ecological complexity measures are scalar;
- that routeability is a universal replacement metric;
- quantitative prediction in noisy natural systems.

The stronger expected-loss theory belongs downstream.

## One-line principle

\[
\boxed{
\text{Amount tells us what information exists; topology tells us what must be acquired together.}
\]
