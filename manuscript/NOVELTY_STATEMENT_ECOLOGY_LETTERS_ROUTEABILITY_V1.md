# Ecology Letters novelty statement — routeability v3

A long-standing question in behavioural ecology is why some broad choice sets
impose large information-processing costs while others can be handled by
sequential decisions. Existing work establishes information-processing limits,
hierarchical foraging, sequential cue use and behavioural specialization. What
has been missing is an exact distinction between **how many alternatives
exist** and **how many distinctions must actually be resolved together**.

We formalize that distinction with fixed and contingent resolution costs. For
deterministic ecological choices,

\[
C_F=\min_{S:I(T;Q_S)=H(T)}c(S)
\]

is determined by the complete static subset-information function. Yet two
tasks on the same physical cue matrix can have the same complete Shannon
entropy vector and the same \(C_F=4\), while their optimal adaptive costs are
\(C_A=4\) and 3. Cartesian products preserve entropic equivalence while making
this adaptive-cost difference arbitrarily large. Thus resource richness, cue
richness and even complete static Shannon information do not determine
effective sequential decision complexity.

The biological novelty is not that animals make sequential decisions. The new
claim is that the **structure of the ecological choice problem itself** has an
operational dimension not identified by option count or static information
content. A finite natural-history budget exposes this dimension when
\(C_A\le B<C_F\). Exact target-relevant compression further shows that raw
state and cue diversity can contain decision-irrelevant redundancy.

A minimal temporal extension makes the same distinction dynamic. An early cue
with zero direct target information can have positive value when it predicts
which later cue will be useful. In the symmetric two-step model,

\[
G_{\rm time}=\frac{|2\rho-1|}{4},
\]

so routing value vanishes exactly at temporal independence; with symmetric
cue noise the gain factorizes as

\[
G_{\rm noisy}
=
\frac{|2\rho-1|(2a-1)(2b-1)}{4}.
\]

Biological examples are deliberately cross-system rather than centered on one
model organism. Bumblebee flower choice, parasitoid host finding, multi-stage
predator avoidance and patch foraging illustrate staged information use in
different ecological settings. None is treated as a direct validation of the
exact theorem.

The paper therefore contributes a theory of **when ecological diversity
becomes decision complexity**, an exact non-identification theorem separating
static information from adaptive accessibility, and a temporal prediction for
when context-dependent cue routing has value. It does not claim novelty for
sequential choice, decision trees, PID, active feature acquisition, value of
information, or the generic fact that entropy can miss other operational
quantities.
