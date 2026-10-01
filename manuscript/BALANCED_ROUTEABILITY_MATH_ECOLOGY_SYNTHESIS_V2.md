# Balanced routeability synthesis v2 — amount versus decision topology

Status: post-freeze synthesis. This file does not modify the frozen Evolution Letters V5 initial-submission surface.

## Core claim

The mathematical and ecological programs meet at a distinction between two different kinds of object.

### Amount / distribution

Examples:
- number of ecological states;
- species richness;
- environmental variance;
- cue frequencies;
- cue entropy;
- pairwise association;
- full available target information;
- temporal frequency or persistence.

### Conditional decision topology

The structure of which distinctions remain necessary **after a particular earlier observation outcome**.

The second is not generic temporal order. It is an outcome-contingent dependency structure over ecological distinctions.

The combined claim is:

\[
\boxed{
\text{amount/distribution does not identify conditional decision topology}.
}
\]

---

## 1. Exact orthogonality witness

For every routing depth \(d\ge2\), let \(k=2^d\).

Take the existing exact-balanced routeable task and a matched control obtained by changing only the target/action labels.

The two tasks have identical:
- \(n=2k+2\) worlds;
- \(m=d+k\) query resources;
- world identities;
- binary query outcome matrix;
- unit query costs;
- exact 50/50 marginal balance of every query;
- every cue-cue joint distribution;
- full cue-only joint distribution;
- target multiplicities \((k+2,k)\);
- target entropy \(H(T)\).

In both tasks the full cue vocabulary resolves the target, so under a uniform world distribution,

\[
I(T;Q_{\mathrm{all}})=H(T)
\]

is equal as well.

Only the target/action map differs.

### Routeable mapping

\[
C_F\ge2^d,\qquad C_A\le d+1.
\]

### Matched control mapping

Let the target be equality versus inequality of the first two routing bits.

Then

\[
\boxed{C_A=C_F=2.}
\]

Therefore

\[
\boxed{
\frac{C_F^R}{C_A^R}
-
\frac{C_F^K}{C_A^K}
\ge
\frac{2^d}{d+1}-1
\to\infty.
}
\]

This is stronger than saying that the same marginal statistics can hide different architectures.

The **entire physical cue environment is the same**.

What changes is only how that environment maps to the focal ecological action.

---

## 2. Consequence for the V5 general principle

The V5 statement can be sharpened from

> diversity is not complexity

to

> **the amount of environmental variation and the topology of decision-relevant distinctions are independent coordinates.**

An even more precise version is:

> **Two ecological tasks can contain the same alternatives, the same physical cues, the same cue distribution and the same total available information, yet impose radically different costs because the action map induces different conditional decision topology.**

This is the conceptual role of routeability.

It is not a universal scalar measure of complexity.

It is an additional relational coordinate.

---

## 3. Relation to existing ecological heterogeneity theory

The synthesis must not caricature existing ecology as purely scalar.

Levins and later niche-breadth theory already distinguish:
- amount of heterogeneity;
- spatial versus temporal variation;
- coarse versus fine grain;
- environmental pattern relative to organismal timescale.

Community ecology also studies network topology rather than only species counts.

The new distinction is narrower:

> those structures need not specify **which later cue becomes relevant conditional on an earlier cue outcome for a focal action**.

Routeability therefore adds conditional decision topology rather than generic pattern or generic order.

---

## 4. The ecological currency is the budget

The combinatorial objects \(C_A\) and \(C_F\) do not themselves specify fitness.

Ecology enters through a real constraint \(B\).

Examples:
- host departure time;
- floral handling opportunity;
- predator-exposure window;
- attention limit;
- energetic sampling budget.

The exact bridge is

\[
\boxed{
C_A\le B<C_F.
}
\]

This is the regime in which topology becomes performance-relevant.

So the integration factorizes cleanly:

\[
\text{conditional topology}
\longrightarrow
(C_A,C_F)
\]

and

\[
\text{ecological natural history}
\longrightarrow
B.
\]

Their intersection determines whether routeability has a realized consequence.

---

## 5. Blindness test for ecological summaries

For a proposed ecological predictor \(S\):

1. freeze \(S\);
2. freeze the physical environmental distribution as far as possible;
3. vary only the cue-to-action conditional topology;
4. ask whether the performance or feasibility prediction changes under finite \(B\).

If it does, \(S\) is not false. It is **not sufficient for a routeability-sensitive claim**.

### Heterogeneity → niche breadth

Freeze:
- resource number;
- resource frequencies;
- physical cue distribution.

Vary:
- decision topology.

Test:
does broad use incur different information burden under the same conventional heterogeneity?

### Information amount → performance

Freeze:
- target entropy;
- full cue distribution;
- \(I(T;Q_{\mathrm{all}})\).

Vary:
- sequential accessibility.

Test:
does a finite acquisition budget separate two systems with the same total available information?

### Specialist/generalist axis

Freeze:
- number and frequency of exploitable resources.

Vary:
- branch structure of discrimination.

Test:
can two equally broad nominal niches have different realized sampling cost?

### Community interaction complexity

Freeze:
- species richness;
- morphology/phenology/encounter-compatible link set.

Vary:
- conditional decision topology.

Test:
does the behaviorally accessible subset differ?

---

## 6. Nonidentifiability is the deeper bridge

The quantity/topology contrast implies an identification statement.

If two latent ecological tasks can produce the same observed summary \(S\) but different \((C_A,C_F)\), then

\[
S
\not\Rightarrow
\text{routeability}.
\]

This creates a general distinction:

### Descriptive ecological summary

What is observed:
- richness;
- marginals;
- entropy;
- pairwise association;
- endpoint interaction network.

### Mechanistic decision object

What must be identified:
- action map;
- conditional cue relevance;
- branch-specific unresolved alternatives;
- acquisition costs/order.

This parallels the Villavicencio lesson without being the same theorem.

There, observed link turnover failed to identify latent ecological rewiring because detection and state were confounded.

Here, aggregate environmental information can fail to identify decision topology because multiple action/branch structures share the same environmental summary.

The common meta-principle is:

> **an ecological summary is mechanistically interpretable only if the latent structures relevant to the claim are identifiable from that summary.**

---

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

## 7. What the current V5 should claim

The present V5 does not need stochastic expected-loss theory.

It needs only establish:

1. conditional decision topology is a well-defined structural axis;
2. it is not determined by common marginal measures of heterogeneity/information;
3. it can change exact finite decision cost;
4. it becomes ecologically consequential in the budget window \(C_A\le B<C_F\);
5. it yields falsifiable predictions for direct experiments.

This is enough for the current paper.

---

## 8. What belongs to the next theory paper

The deterministic theory asks for guaranteed exact resolution.

Natural systems require a risk-sensitive extension.

A next-generation objective can take the form

\[
J(\pi)
=
\mathbb E_\pi[C]
+
\lambda\,\mathbb E_\pi[L(A,T)],
\]

with:
- stochastic cue likelihoods;
- classification error;
- state priors;
- expected acquisition cost;
- satisficing or utility-based actions.

Then define adaptive and fixed risk optima:

\[
C_A^{\mathrm{risk}},\qquad
C_F^{\mathrm{risk}}.
\]

The key future theorem is not merely to solve this model.

It is:

> **Does quantity/topology orthogonality survive under noisy cues and expected loss?**

If yes, the current qualitative ecological synthesis becomes quantitative.

That is a separate paper and should not delay V5.

---

## 9. Experimental consequence

The existing four-state experiment is the minimal causal version.

The new exact-balanced matched pair is the stronger stress test.

### Minimal experiment

Matches physical cue support and low-order information structure.

Tests:

\[
\Delta_{B=1}=0,\quad
\Delta_{B=2}>0,\quad
\Delta_{B=3}=0.
\]

### Balanced stress test

Matches:
- full physical cue matrix;
- exact cue marginals;
- target prevalence;
- target entropy;
- total full-vocabulary target information.

Only the target/action mapping changes.

This is the direct experimental implementation of the orthogonality theorem.

---

## 10. Paper portfolio

### V5 — ecology theory

Claim:
conditional decision topology is an ecological axis orthogonal to common amount-based summaries.

### Mathematical companion

Claim:
exact-balanced query systems have rigid finite extremal geometry but unbounded asymptotic adaptivity.

### Direct experiment

Claim:
holding the physical cue environment fixed, changing only cue-to-action topology changes behavior specifically in the predicted budget window.

### Expected-loss theory

Claim:
to be determined; this is the stochastic quantitative extension.

---

## One-line synthesis

\[
\boxed{
\text{Amount describes what information is present; topology describes what must be acquired together before action.}
}
\]
