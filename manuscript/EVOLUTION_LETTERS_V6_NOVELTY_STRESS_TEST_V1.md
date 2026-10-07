# V6 novelty stress test — reviewer view

Status: claim-risk audit for the V6 fitness-frontier candidate. This note is
deliberately stricter than the manuscript.

## Bottom line

V6 is no longer an "adaptive sensing is useful" paper.

The defensible contribution is one theorem suite:

> finite target-resolution constraints define an exact adaptive/fixed frontier;
> natural-history value ranks that frontier; the ranking can be inverted into
> robust evolutionary feasibility limits.

The three MAIN results should therefore be presented as one connected result
family, not as three unrelated breakthroughs.

The strongest biological surprise is not that conditional information saves
tests. It is:

[
oxed{
	ext{structurally larger adaptive advantage can have smaller biological value}
}
]

and, in the exact extremal family,

[
oxed{
C_F/C_A	oinfty
quad	ext{while}quad
R	o0.
}
]

That reversal is the cleanest antidote to the "obvious" objection.

## MAIN 1 — exact fixed-(n,m,b) joint frontier

### What is established prior art

Do not claim novelty for:

- adaptive decision trees;
- nonadaptive/fixed test collections;
- minimum test set / generalized test collection;
- flattening all internal nodes of an adaptive tree into a nonadaptive set;
- the full b-ary count
  [
  (b^h-1)/(b-1).
  ]

### What remains candidate-new

For the declared target-resolution model, at every feasible adaptive depth h,

[
(C_A,C_F)
=
left(
h,min{m,F_b(n,h)}
ight)
]

is not only an upper bound but is simultaneously attainable while controlling:

- represented-world count n;
- available query count m;
- query arity b;
- adaptive worst-case depth;
- fixed target-separation burden.

The private-pair construction certifies every fixed-mandatory query, while the
protected spine certifies the adaptive lower bound.

### Reviewer risk

**Moderate.**

The construction is elementary once seen. A reviewer may say that the exact
frontier is a natural sharpening of tree-node counting plus test collection.

The response should not be "the proof is hard." It should be:

> the frontier is the exact source object needed for the biological result;
> neither adaptive-tree complexity nor fixed test collection alone gives the
> joint evolvability limits.

Priority search has not found the same all-depth fixed-(n,m,b) frontier, but
absence is not proof.

## MAIN 2 — natural history re-ranks the frontier

### What is established prior art

Do not claim novelty for:

- assigning utility to completion time;
- deadline-weighted decision utility;
- sequential value of information;
- expected utility of adaptive versus nonadaptive policies.

### What is mathematically immediate once MAIN 1 is known

For nonincreasing U,

[
max[U(C_A)-U(C_F)]
=
max_h[U(h)-U(I_h)]
]

is a monotone lift of the exact frontier.

This should **not** be sold as a deep standalone mathematics theorem.

### What is biologically nontrivial

The important consequence is ordinal reversal.

Structural metrics need not preserve the biological ranking of architectures.

Canonical finite example:

- structural ratio chooses h=3;
- exponential opportunity value chooses h=4, 3 or 2 depending on urgency.

Stronger exact-family result:

[
C_F/C_A	oinfty
]

while for any fixed exponential opportunity loss

[
e^{-mu C_A}-e^{-mu C_F}	o0.
]

So increasing structural adaptive gain can eventually mean **decreasing
biological value**.

### Reviewer risk

**Low-to-moderate if framed as the reversal, high if framed as "we apply a
utility function."**

The reversal should carry the Results section, not the formal lift identity.

## MAIN 3 — inverse robust evolutionary thresholds

### What is algebraic consequence

Given U and architecture cost K, solving the sharp frontier backward for the
required fixed burden is an inversion of MAIN 2.

Do not oversell integer inversion itself.

### What is biologically useful

The inversion yields exact no-go statements.

At bounded cue arity b,

[
K_{m crit,robust}^{(b)}
=
max_{hge2}
[U(h)-U(J_b(h))].
]

Above this cost, no amount of additional finite worlds or query resources can
guarantee statewise repayment.

The inverse minimum arity

[
b_{min}^{m robust}
]

turns the theorem into a falsifiable architecture constraint.

Canonical exponential example:

[
mu=0.3,quad K=0.30
]

gives

[
K_{m crit}^{(2)}approx0.2901
<
K
<
K_{m crit}^{(3)}approx0.3863,
]

hence

[
b_{min}^{m robust}=3.
]

### Reviewer risk

**Moderate.**

The no-go is exact but cue arity is abstract. The manuscript must repeatedly
state that b is query-outcome arity, not receptor count or sensory-organ
complexity.

The biological value rises sharply if a real system can map empirical cue
channels to the declared finite query model.

## SUPPORT — expected-frequency rescue

This is biologically important but not novelty.

Prior-weighted decision trees and shallow high-probability branches are
established.

Use robust-versus-expected separation to prevent a false biological conclusion:

> failure of a frequency-free robust threshold does not imply negative expected
> selection.

The exact finite and scalable ceilings are useful accounting identities and
figure material, not a fourth main theorem.

## Empirical anchors — what they now achieve

### Chandel et al. 2024

Strength:

- high temporal resolution;
- demonstrates that cue-effect magnitude is strongly nonuniform through time.

Limit:

- aggregate activity;
- no individual completion distribution;
- no architecture comparison.

### Uehara et al. 2026

Strength:

- individual rows;
- one-minute interval-censored completion profiles;
- explicit right-censoring;
- strong cross-species early-tail differences;
- An. gambiae / An. stephensi completion profiles cross.

This is substantially better than an aggregate anchor because it demonstrates
the exact kind of temporal-profile shape that the expected-value layer needs.

Limit:

- species differences are not adaptive-versus-fixed architecture differences;
- no natural U(t);
- no architecture cost K;
- probing is not reproductive fitness.

### Empirical conclusion

The paper now has real process evidence, but not a direct test of the main
evolutionary theorem.

Do not write "validated in mosquitoes."

Write:

> public mosquito data show that the temporal objects required by the theory are
> biologically nontrivial and measurable.

## Current Evolution Letters assessment

### What is strong enough

1. Exact joint frontier under finite world/query/arity constraints.
2. A sharp biological reversal: structural adaptivity can diverge while
   ecological value vanishes.
3. Exact robust no-go / minimum-arity consequence.
4. Public individual temporal profiles showing that completion-time shape is
   not a cosmetic detail.

### What remains the central risk

The main ecological mapping is still abstract.

A skeptical reviewer can say:

> You have a clean decision-theory result, but where is the evidence that a
> biological lineage's evolved sensory architecture is actually constrained by
> these n, m, b and K quantities?

This is now the dominant weakness. Adding more combinatorial corollaries will
not solve it.

## Stop rule

Do **not** add another main theorem.

The next meaningful gains are, in order:

1. tighten priority evidence for the exact joint frontier;
2. create the three main figures from frozen receipts;
3. improve the biological mapping of n, m, b, U and K in one focal system;
4. if possible, identify a public or prospective dataset where cue topology and
   completion profiles are measured in the same individuals/system.

Anything else belongs in Supplement or a companion paper.

## Recommended one-sentence claim

> Natural history can reverse the evolutionary ranking of exact information
> architectures: the structure with the largest adaptive advantage need not be
> the one with the largest ecological value, and finite cue branching imposes
> sharp limits on the control costs that contingent sensing can robustly repay.

## Recommended teaser

> More adaptive information architecture is not necessarily more evolvable:
> exact finite routing theory shows that structural advantage can diverge while
> ecological value vanishes.
