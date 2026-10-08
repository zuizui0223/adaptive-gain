# Natural history re-ranks adaptive information architectures

## Teaser

Adaptive sensing can have an arbitrarily large structural advantage without
having a large fitness effect. Exact finite routing theory shows why: natural
history selects among an attainable frontier of information architectures, and
encounter frequencies can rescue architectures that are impossible to favor
robustly across all states.

## Abstract

Environmental heterogeneity is often expected to favor behavioral flexibility,
yet a structural advantage in information acquisition is not itself a fitness
advantage. We link an exact finite theory of contingent sensing to ecological
value. Let \(C_A\) be the minimum worst-case cost of contingent target
resolution and \(C_F\) the minimum cost of a precommitted resolving query set.
For fixed world count \(n\), query count \(m\) and maximum query arity \(b\),
every feasible adaptive depth \(h\) lies on an exact attainable frontier
\[
(C_A,C_F)=
\left(h,\min\{m,F_b(n,h)\}\right).
\]
For any nonincreasing biological value of completion \(U(c)\), this frontier
lifts sharply:
\[
\max[U\(C_A\)-U\(C_F\)]
=
\max_h[U(h)-U(I_h)].
\]
Natural history therefore re-ranks information architectures rather than merely
scaling one adaptive-gain score. Inverting the frontier gives exact
evolutionary requirements: for bounded cue arity, some control costs cannot be
repaid robustly by any finite task, regardless of how many states or query
resources are added. As a biological consequence, encounter frequencies can
still raise expected value above this robust floor by concentrating common
states on shallow branches; we use this distinction to prevent robust no-go
results from being over-read as universal selection impossibility. Public
mosquito data provide complementary temporal anchors: individual probing
profiles can differ strongly in early-tail and censoring structure, while an
infrared host-seeking effect is strongly nonuniform through time. Structural
adaptive gain is evolutionary potential; natural history determines which
parts of the exact frontier are robustly evolvable, and encounter frequencies
determine the additional expected-value premium.

Keywords: adaptive sensing; ecological information; decision trees;
behavioral flexibility; environmental heterogeneity; natural history;
evolutionary constraints; value of information

## Introduction

Organisms rarely acquire all potentially relevant information before acting.
Predators narrow prey alternatives, herbivores evaluate hosts sequentially,
pollinators combine sensory channels, and animals often stop gathering
information once a sufficient ecological distinction has been resolved.
Conditional information use is therefore a natural feature of ecological
decision making (Dall et al. 2005; Schmidt et al. 2010; Trimmer & Houston
2014).

The evolutionary interpretation is less straightforward. Information can have
a measurable fitness value, but that value depends on the ecological decision
problem rather than information amount alone (Donaldson-Matasci et al. 2010;
Rivoire & Leibler 2011; Moffett & Eckford 2022). A sensing architecture can be
structurally efficient without being selectively valuable.
Saving five observations may matter greatly if it moves an action inside an
ecological opportunity window, or hardly at all if both the fixed and
contingent decisions are already early enough, or already too late. Likewise,
the same sensing tree can have very different expected value when common
environmental states occupy shallow branches rather than deep ones.

These distinctions matter because theoretical treatments often collapse
information architecture into one scalar advantage. In our earlier finite
routing theory, the structural benefit of contingent sensing is summarized by
the difference or ratio between the minimum contingent worst-case cost
\(C_A\) and the minimum precommitted resolving cost \(C_F\). This structure is
mathematically informative: \(C_A\le C_F\), and finite environments can
generate large or even unbounded fixed-to-contingent ratios. But neither
\(C_F-C_A\) nor \(C_F/C_A\) is intrinsically fitness. Both ignore where the
saved information cost occurs relative to ecological time, and both ignore the
frequency with which different decision branches are encountered.

Here we ask a reverse evolutionary question:

> Which finite information architectures can generate enough ecological value
> for contingent sensing to be supported by selection?

We answer this with three main results and one biological extension.

First, we close the finite structural problem at fixed world count, query count
and query arity. Rather than retaining only the single architecture that
maximizes \(C_F/C_A\), we identify an exact attainable frontier of
\((C_A,C_F)\) pairs.

Second, we compose this frontier with an arbitrary nonincreasing biological
value of completion \(U(c)\). This yields a sharp cross-layer result:
natural history selects among structural architectures and can rank them
differently from any purely structural adaptive-gain metric.

Third, we invert the result. Given an architecture cost, we derive the minimum
fixed burden—and therefore the minimum world, query and cue-arity structure—
needed for positive contingent value. This produces model-wide no-go regions:
for a fixed maximum query arity, some control costs cannot be repaid by any
finite environment in the declared class.

Finally, as an interpretive extension rather than a separate novelty theorem,
we separate robust statewise value from expected evolutionary value. Expected
selection additionally uses state frequencies and early termination, so a
robust no-go need not imply negative expected selection. This distinction is
used as a biological claim firewall and to quantify the extra value contributed
by common shallow branches.

The resulting picture differs from the common intuition that more
heterogeneity or larger adaptive gain should monotonically favor flexible
information use. Structural routeability defines evolutionary opportunity.
Natural history and encounter frequencies determine whether that opportunity
is worth anything.

## Model

### Finite ecological decision tasks

A task contains a finite set of represented worlds \(W\), a focal target
\(T(w)\), and a finite set of queries. A query has deterministic outcomes and
positive acquisition cost. The target is intentionally narrower than the full
environmental state: two worlds can be ecologically distinct yet equivalent
for the focal action.

A fixed resolver chooses one query set in advance. Its minimum total cost is
\(C_F\).

A contingent resolver can choose later queries from earlier outcomes. Its
minimum worst-path cost is \(C_A\).

Any fixed strategy is a special contingent strategy, so
\[
C_A\le C_F.
\]

Throughout the principal exact results we use unit query costs and bound the
number of possible outcomes of any query by \(b\).

### Biological value of completion

We deliberately separate information structure from biological value.

Let
\[
U(c)
\]
be the biological value of guaranteed correct completion at total acquisition
cost (c). We require only that (U) is finite and nonincreasing over the
relevant finite costs.

Examples include a linear time penalty,
\[
U(c)=-\lambda c,
\]
or an ecological opportunity model,
\[
U(c)=vS(c),
\]
where (S(c)) is the probability that a feeding, mating or other opportunity
remains available through cost (c).

The robust value of contingent over fixed resolution is
\[
R_{\rm robust}
=
U\(C_A\)-U\(C_F\).
\]

This is a frequency-free worst-state quantity. It is not the expected fitness
value of a decision tree.

### Expected value

For a contingent policy \(\pi\), let \(T_\pi(w)\) be its realized completion
cost in world (w), and let \(p_w\) be the encounter probability of that world.

Then
\[
R_{\rm expected}\(\pi\)
=
\sum_w p_w U[T_pi(w)]
-
U\(C_F\).
\]

For a minimax tree,
\[
R_{\rm expected}\ge R_{\rm robust},
\]
because every realized path is no longer than the worst path.

The difference is the early-termination premium generated by the distribution
of ecological encounters across tree branches.

## Results

### 1. Finite information constraints define an exact attainable frontier

Let \(F_b(n,h)\) be the exact maximum number of productive internal-node
occurrences in a rooted decision tree with at most \(n\) nonempty leaves,
worst-path depth at most \(h\), and at most \(b\) nonempty children at each
internal node.

For a task with \(n\) represented worlds, \(m\) query resources and
\(C_A=h\),
\[
C_F
\le
I_h
=
\min\{m,F_b(n,h)\}.
\]

The key strengthening is sharpness at every feasible depth.

For each \(h\), we construct a productive tree with a protected deepest spine
and one physical query per internal node. A private opposite-target pair is
assigned to every internal query so that this query is the pair's unique
separator. Private pairs make all internal queries fixed-mandatory. Along the
protected spine, one realized world belongs to a private pair at every depth,
forcing every adaptive resolver on that world to acquire all \(h\) spine
queries.

Thus
\[
\boxed{
(C_A,C_F)
=
(h,I_h)
}
\]
is exactly attainable at every feasible \(h\).

The structural problem is therefore not represented by one optimum ratio. It
is represented by an exact frontier.

### 2. Natural history re-ranks the structural frontier

For any finite nonincreasing (U), the maximum robust biological value over
the declared structural scope is
\[
\boxed{
R_{\rm robust,max}
=
\max_h
[U\(h\)-U(I_h)].
}
\]

The same frontier constructions attain the bound.

This result identifies when a structural gap is biologically sufficient. If
\[
U(c)=-\lambda c,
\]
then
\[
U\(C_A\)-U\(C_F\)
=
\lambda\(C_F-C_A\).
\]
A linear adaptive-gain-to-fitness map is therefore equivalent to assuming
constant marginal biological penalty per unit completion cost.

For nonlinear natural history, absolute completion times matter. Equal
structural gaps at different positions on the time axis need not have equal
value.

Consider binary tasks with
\[
n=10,\qquad m=9.
\]
Relevant exact frontier points are
\[
(2,3),\qquad(3,7),\qquad(4,9).
\]
The fixed-to-contingent ratio is largest at \(h=3\).

Now let
\[
U(c)=e^{-\mu c}.
\]
The robust biological values are
\[
e^{-2\mu}-e^{-3\mu},
\]
\[
e^{-3\mu}-e^{-7\mu},
\]
and
\[
e^{-4\mu}-e^{-9\mu}.
\]
As \(\mu\) increases, the maximizing depth switches
\[
4\to3\to2.
\]
The structural ratio optimum therefore agrees with the biological optimum only
over an intermediate range.

An even sharper counterexample comes from the exact binary extremal family
\[
C_A=d+1,\qquad C_F=2^d.
\]
Its structural ratio diverges:
\[
\frac{2^d}{d+1}\to\infty.
\]
But for every fixed \(\mu>0\),
\[
e^{-\mu(d+1)}-e^{-\mu2^d}\to0.
\]
A sequence can therefore become structurally more adaptive while becoming
biologically worthless.

### 3. Architecture cost can be inverted into minimum information structure

Let the contingent architecture pay constitutive cost \(K\).

At adaptive depth \(h\), define
\[
J_K\(h\)
=
\min\{j\ge h:U\(h\)-U(j)>K\}.
\]
Then positive robust architecture value at depth \(h\) is possible exactly when
\[
I_h\ge J_K\(h\).
\]

The forward value theorem therefore has an exact inverse: natural history and
architecture cost specify the amount of information structure required for
evolvability.

This becomes especially informative when world and query counts are allowed to
grow but cue arity remains bounded.

A full \(b\)-ary adaptive tree of depth \(h\) has at most
\[
J_b\(h\)
=
\frac{b^h-1}{b-1}
\]
internal nodes. The private-pair construction attains
\[
(C_A,C_F)
=
(h,J_b\(h\)).
\]

For bounded-below (U), define
\[
\boxed{
K_{\rm crit,robust}^{(b)}
=
\max_{h\ge2}
[U\(h\)-U(J_b\(h\))].
}
\]

If
\[
K>K_{\rm crit,robust}^{(b)},
\]
no finite task with cue arity at most \(b\) can guarantee positive net
contingent value in every represented world. More environmental states and
more query resources cannot help.

This gives an exact minimum robust cue arity
\[
b_{min}^{\rm robust}
=
\min{b\ge2:K<K_{\rm crit,robust}^{(b)}}.
\]

For
\[
U(c)=e^{-0.3c},
\qquad K=0.30,
\]
the binary global ceiling is approximately (0.290085), whereas the ternary
ceiling is approximately (0.386328). Thus
\[
b_{min}^{\rm robust}=3.
\]

The interpretation is specific to the finite query model. Query arity is the
number of distinguishable outcomes of one declared information source, not a
generic measure of receptor number or nervous-system complexity.

### Biological consequence: encounter frequencies can rescue expected value

The robust frontier is intentionally distribution free. Expected selection is
not. The following exact ceiling is a model-specific corollary used to separate
those claims; prior-weighted expected decision-tree cost itself is established
theory.

Fix finite world and query budgets (n,m) and define
\[
M=\min\{m,n-1\}.
\]

Across all legal tasks, guaranteed-resolving policies and strictly positive
world-frequency distributions,
\[
\boxed{
\sup R_{\rm expected}(n,m,b)
=
U(1)-U(M)
}
\]
for every
\[
b\ge2.
\]

The upper bound follows because no nontrivial decision can finish before one
query and because any fixed resolver costs at most \(M\).

Sharpness requires only binary queries. We construct a private-pair tree with
exactly \(M\) fixed-mandatory internal queries and one target-pure leaf directly
below the root. As encounter probability concentrates on that leaf, adaptive
expected value approaches \(U(1)\), whereas fixed value remains \(U(M)\).

This creates a qualitative split.

Cue arity matters for robust statewise evolvability:
\[
K_{\rm crit,robust}^{(b)}
\]
depends on \(b\).

But cue arity disappears from the exact finite-scope expected ceiling once
encounter frequencies can be skewed.

This is a supremum over freely varying encounter distributions, not a
prediction that arity has no effect at a measured distribution. The limiting
construction concentrates almost all encounters on a one-query branch; if
rare-state probabilities cannot approach zero, the branch completion-time
profile and cue arity may still affect expected performance.

In the unrestricted finite-size limit,
\[
\sup R_{\rm robust}
=
U(2)-U_\infty,
\]
whereas
\[
\sup R_{\rm expected}
=
U(1)-U_\infty.
\]

Therefore
\[
U(2)-U_\infty
\le K
<
U(1)-U_\infty
\]
defines a frequency-assisted evolvability band: no finite architecture can be
positive in every state, yet expected positive value remains possible.

For exponential opportunity value,
\[
U(c)=ve^{-\mu c},
\]
the robust and expected global ceilings are
\[
ve^{-2\mu}
\]
and
\[
ve^{-\mu}.
\]

At
\[
\mu=0.3,\qquad v=1,\qquad K=0.60,
\]
the control cost exceeds the absolute robust ceiling
\[
e^{-0.6}\approx0.5488,
\]
but remains below the expected ceiling
\[
e^{-0.3}\approx0.7408.
\]

Thus encounter-frequency structure can support a contingent architecture that
no finite information architecture can make robustly favorable.

## Empirical process anchors: temporal effect shape and individual completion profiles

The theory separates two temporal objects: when a behavioral effect is expressed
and how individuals are distributed across completion times. Current public
mosquito data illustrate both objects without yet closing the fitness chain.

First, Chandel et al. (2024) measured *Aedes aegypti* host-seeking activity with
and without infrared cues during a 300-s assay containing transient CO2 pulses.
Reanalysis of the public Figure 3a source data shows that the post-pulse
infrared advantage is strongly late weighted. Half of the first post-pulse
signed advantage accumulates only after approximately 46.2 s, and half of the
second only after approximately 46.5 s. The same aggregate cue effect would
therefore be valued differently by short versus long ecological opportunity
windows.

Second, Uehara et al. (2026) provide individual one-minute Probe percentages
for six mosquito species. Restricting the secondary analysis to individuals
with zero probing in the -1 to 0 min pre-stimulus bin gives a one-minute
interval-censored first post-stimulus probing profile. *Aedes albopictus* is
especially delayed: only 10 of 38 individuals (26.3%) show probing in the first
minute, the discrete cumulative probability reaches 0.50 only by minute 4, and
15 of 38 remain without observed probing through 8 min. By contrast, first-
minute probing occurs in 18/28 *Ae. aegypti* (64.3%), 12/14 *Anopheles
gambiae* (85.7%) and 15/18 *An. stephensi* (83.3%). The two *Anopheles*
profiles also cross: *An. gambiae* remains higher through minute 3
(85.7% versus 83.3%), whereas *An. stephensi* reaches 88.9% by minute 4 and
overtakes *An. gambiae*. Thus real individual temporal profiles can differ in
early-tail mass, right-censoring and even deadline-dependent ordering, not
merely in a single mean.

These are process anchors, not fitness validations. The Chandel data do not
identify individual completion times, and the Uehara source data are
one-minute interval-censored rather than frame-resolved. Neither dataset
identifies the natural opportunity-value function, constitutive control cost or
an adaptive-versus-fixed architecture.

## Discussion

### Structural adaptive gain is evolutionary potential, not fitness

The central result is a separation.

Finite information architecture determines which contingent and fixed
completion-cost combinations are possible. Natural history determines their
value.

This prevents two opposite errors.

The first is to equate a large structural adaptive gap with a large biological
effect. The exact extremal family shows that the structural ratio can diverge
while ecological value tends to zero.

The second is to conclude that weak robust value makes adaptivity irrelevant.
Encounter frequencies can concentrate ecological weight on shallow branches,
creating positive expected value even when robust repayment is impossible in
every state.

### Natural history selects a point on a frontier

The usual question asks how much adaptivity a system has.

The finite theory suggests a different object: an exact frontier of
architectures. A deep contingent architecture can support a large simultaneous
fixed burden but itself completes late. A shallower architecture finishes
earlier but supports less branch-exclusive structure.

Natural history selects among these alternatives.

This is why a structural ratio, an additive structural gap and an expected
fitness advantage can rank the same architectures differently.

### Sensory branching and encounter frequency are different evolutionary resources

Cue arity and encounter frequencies enter the theory differently.

Higher cue arity enlarges the robust structural frontier by allowing more
branching to be compressed into a fixed adaptive depth.

Encounter-frequency skew does not change that robust frontier. Instead it
places more ecological value on selected shallow branches.

The resulting distinction is sharp: robust cost ceilings depend on cue arity,
whereas the exact expected-value ceiling at fixed (n,m) does not.

This provides a precise sense in which ecological frequency structure can
substitute for information branching capacity in expected, but not robust,
evolvability.

### Relation to PAYOFF

The present framework supplies the upstream recoverable benefit.

At the robust level,
\[
R_{\rm robust,max}
=
\max_h[U(h)-U(I_h)].
\]

PAYOFF then asks whether
\[
R-K>0
\]
and transports architecture value into invasion, fixation and occupancy.

The two theories therefore answer different parts of one chain:

finite routing structure
-> recoverable ecological value
-> architecture cost
-> selection and population dynamics.

The generic (R-K) architecture landscape remains PAYOFF's domain. The
contribution here is to derive sharp information-structural limits on (R).

### What the theory does not claim

Sequential value of information (Miller 1975), prior-weighted and
worst-versus-expected decision trees (Hyafil & Rivest 1976; Saettler et al.
2017), deadline-sensitive action utility (Ash & Hayes-Roth 1996),
adaptive-versus-nonadaptive expected-value gaps (Hellerstein et al. 2022), and
minimum/generalized test-collection problems (Douek-Pinkovich et al. 2021) all
have substantial prior literatures. These are boundary conditions for the
present contribution, not claims of novelty. In particular, the fixed resolver
is closely related to a test collection: V6's mathematical claim is the exact
joint frontier with contingent worst-case depth under simultaneous finite
world, query and query-arity constraints, not the fixed test-set problem by
itself.

The proposed contribution is narrower:

1. an exact fixed-((n,m,b)) target-resolution frontier attained at every
   feasible depth;
2. a sharp lift of that frontier by arbitrary monotone biological completion
   value;
3. exact inverse robust thresholds, including global cue-arity no-go regions;
4. an exact finite expected-value ceiling that separates sensory branching
   capacity from encounter-frequency effects.

These claims remain inside finite deterministic guaranteed target resolution.
No claim is made for noisy sensing, continuous belief states or endogenous
learning without further extensions.

## Current empirical requirements

A direct biological test needs four empirical objects:

1. the focal target and available cue topology;
2. branch-specific completion-time distributions;
3. the ecological value of completion through time;
4. architecture or control costs.

Expected-value tests additionally require encounter frequencies.

A positive \(C_F-C_A\) measurement alone is therefore a structural receipt,
not a selection estimate.

## Conclusion

Adaptive information architecture does not carry a fixed evolutionary value.
Finite ecological information constraints define an exact structural frontier.
Natural history re-ranks that frontier, architecture cost determines which
points are evolvable, and encounter frequencies can create expected-value
regimes unavailable to any robust statewise architecture.

Structural adaptive gain is potential. Evolution depends on where that
potential lies in time and how often each branch of the environment is
encountered.


## References

Ash, D. & Hayes-Roth, B. 1996. Using action-based hierarchies for real-time
diagnosis. *Artificial Intelligence* 88:317–347.
https://doi.org/10.1016/S0004-3702(96)00024-0.

Chandel, A., DeBeaubien, N. A., Ganguly, A. et al. 2024. Thermal infrared
directs host-seeking behaviour in *Aedes aegypti* mosquitoes. *Nature*
633:615–623. https://doi.org/10.1038/s41586-024-07848-5.

Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens,
D. W. 2005. Information and its use by animals in evolutionary ecology.
*Trends in Ecology & Evolution* 20:187–193.
https://doi.org/10.1016/j.tree.2005.01.010.

Donaldson-Matasci, M. C., Bergstrom, C. T. & Lachmann, M. 2010. The fitness
value of information. *Oikos* 119:219–230.
https://doi.org/10.1111/j.1600-0706.2009.17781.x.

Douek-Pinkovich, Y., Ben-Gal, I. & Raviv, T. 2021. The generalized test collection problem. *TOP* 29:372–386.
https://doi.org/10.1007/s11750-020-00554-1.


Hellerstein, L., Kletenik, D., Liu, N. & Witter, R. T. 2022. Adaptivity gaps
for the stochastic Boolean function evaluation problem. In *Approximation and
Online Algorithms*, Lecture Notes in Computer Science, 190–210.
https://doi.org/10.1007/978-3-031-18367-6_10.

Hyafil, L. & Rivest, R. L. 1976. Constructing optimal binary decision trees is
NP-complete. *Information Processing Letters* 5:15–17.
https://doi.org/10.1016/0020-0190(76)90095-8.

Miller, A. C. 1975. The value of sequential information. *Management Science*
22:1–11. https://doi.org/10.1287/mnsc.22.1.1.

Moffett, A. S. & Eckford, A. W. 2022. Minimal informational requirements for
fitness. *Physical Review E* 105:014403.
https://doi.org/10.1103/PhysRevE.105.014403.

Rivoire, O. & Leibler, S. 2011. The value of information for populations in
varying environments. *Journal of Statistical Physics* 142:1124–1166.
https://doi.org/10.1007/s10955-011-0166-2.

Saettler, A., Laber, E. & Cicalese, F. 2017. Trading off worst and expected
cost in decision tree problems. *Algorithmica* 79:886–908.
https://doi.org/10.1007/s00453-016-0211-2.

Schmidt, K. A., Dall, S. R. X. & Van Gils, J. A. 2010. The ecology of
information: an overview on the ecological significance of making informed
decisions. *Oikos* 119:304–316.
https://doi.org/10.1111/j.1600-0706.2009.17573.x.


Uehara, T., Dong, L. & Duvall, L. B. 2026. Behavioral heterogeneity in host
seeking and post-feeding suppression among disease vector mosquitoes.
*Communications Biology* 9:757.
https://doi.org/10.1038/s42003-026-09987-z.

Trimmer, P. C. & Houston, A. I. 2014. An evolutionary perspective on
information processing. *Topics in Cognitive Science* 6:312–330.
https://doi.org/10.1111/tops.12085.
