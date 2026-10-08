# Fitness-process prior-art boundary

Status: novelty audit for the opportunity-fitness branch. This file is intentionally conservative.

## Established ingredients that must not be claimed as new

### Speed, accuracy, effort and decision time affect biological performance

Behavioral ecology and decision science already treat information acquisition as time- and effort-limited.

Relevant anchors include:

- Chittka, Skorupski & Raine 2009, Trends in Ecology & Evolution, DOI 10.1016/j.tree.2009.02.010;
- de Froment, Rubenstein & Levin 2014, PLOS Computational Biology, DOI 10.1371/journal.pcbi.1003937;
- Dall et al. 2005, Trends in Ecology & Evolution, DOI 10.1016/j.tree.2005.01.010.

Therefore the present programme must not claim that delayed decisions can reduce fitness, that information has value, or that speed and accuracy trade off.

### Response-time distributions can matter beyond their means

Psychology and visual-search research explicitly argues that mean response time can miss process structure and uses response-time distributions and hazard functions.

A relevant example is Panis et al. 2020, Attention, Perception, & Psychophysics, DOI 10.3758/s13414-019-01897-z.

Therefore the statement "mean decision time is insufficient" is not a standalone novelty claim.

### First-order stochastic dominance is standard

The equivalence between:

- one completion-time distribution being preferred under every monotone value-of-time function; and
- first-order stochastic dominance

is standard expected-utility / stochastic-order mathematics.

The opportunity-fitness branch uses this result to locate the correct process object. It does not claim the stochastic-order theorem itself.

### Worst-case and expected-cost decision trees are established distinct objectives

Optimal decision-tree theory has long distinguished expected and worst testing costs.

Relevant anchors include:

- Hyafil & Rivest 1976, Information Processing Letters, DOI 10.1016/0020-0190(76)90095-8;
- Saettler, Laber & Cicalese, "Trading off Worst and Expected Cost in Decision Tree Problems", ISAAC 2015 / later Algorithmica treatment.

The literature explicitly notes that a worst-case-optimal tree can behave poorly in expectation and vice versa.

Therefore FP1, the four-world minimax-versus-fitness witness, is an explanatory bridge for this repository rather than a priority claim for the generic distinction.

### Deadlines and time-dependent costs in decision trees are not new

Real-time diagnosis, cost-sensitive decision trees and planning have incorporated deadlines, late penalties, action utility and completion-time requirements.

Examples include:

- real-time diagnostic decision trees with deadline-contingent action utility;
- Kao, Tang & Tang, cost-sensitive decision trees with completion-time requirements;
- general decision-theoretic and risk-sensitive tree / MDP literature.

Therefore an adaptive tree with a deadline objective is not novel by itself.

### Ecological optimal stopping and time-dependent reward are established

Foraging and movement theory already combine time-dependent reward, opportunity costs, search costs and stopping rules.

Examples include foraging drift-diffusion models and stopping-theory treatments of settlement/search.

Therefore the present programme must not claim a general new theory of ecological time costs or optimal stopping.


### Time pressure can change cue use in animals

Time-pressure-dependent cue selection is not only a human or algorithmic result.

Toader et al. (2019, Journal of Comparative Psychology, DOI
10.1037/com0000168) tested rhesus macaques on a four-cue probabilistic
decision task. Under time pressure, cue use decreased; one animal showed a
satisficing strategy that ignored the least informative cue dimension.

Therefore the present programme must not claim that:

- animals can change cue use under time pressure;
- urgency can favor dropping information;
- cue weighting/order can be context dependent.

The narrower question is whether a **declared finite ecological routing
topology** plus a measured ecological value-of-time predicts which contingent
policy is favored and where policy switches occur.

### Label-dependent deadlines already alter decision-tree design

Kao & Tang (2014, INFORMS Journal on Computing, DOI
10.1287/ijoc.2013.0560) explicitly formulate cost-sensitive decision-tree
induction with label-dependent late constraints and optimize trees under
completion-time requirements.

Thus deadline-sensitive tree topology is established operations-research
theory. The ecological programme cannot claim novelty for adding deadlines to
trees.

The biologically distinctive layer must come from identifying the deadline or
value-of-time process from natural history and composing it with an
interaction-specific cue topology, encounter process and architecture cost.



### Sequential value of information is long established

Miller (1975, Management Science, DOI 10.1287/mnsc.22.1.1) explicitly showed
that the value of information changes when observables can be acquired
sequentially, because early observations affect whether later observations are
worth purchasing.

Therefore the present programme must not claim that conditional acquisition
creates a distinct value of information in principle.

### Real-time decision trees already optimize utility before deadlines

Real-time diagnosis and cost-sensitive tree literatures already allow action
utility to depend on how far through a decision tree the agent has progressed
when a deadline arrives. Decision-tree theory also distinguishes worst-case and
expected testing cost and provides approximation/trade-off results.

Therefore neither a deadline-weighted tree objective nor the distinction
between worst and expected cost is a novelty claim here.

### Consequence for the sharp envelope claim

The defensible candidate is narrower.

The repository already owns an exact finite extremal theorem for the attainable
adaptive/fixed cost frontier under fixed world count, query count and query
arity.

The opportunity-fitness branch composes that **sharp structural frontier** with
a natural-history time-value function and proves that the resulting ecological
envelope is itself sharp and constructively attained:

[
R_{max}
=
vmax_h[S(h)-S(I_h)].
]

The novelty candidate is therefore not "sequential information has value" but:

> a finite ecological information architecture admits an exact sharp ceiling on
> the **worst-state / frequency-free** value adaptivity can guarantee, and
> natural history can select a different extremal architecture than the one
> maximizing the structural adaptive/fixed ratio.

A targeted prior-art search found decision-tree work on value-dependent test
costs, worst/expected cost trade-offs, sequential information value and
deadline-contingent action utility, but not this particular sharp ecological
composition with the bounded-arity extremal frontier.

This absence is not a proof of priority; it is the current claim boundary.



### Deadline-distribution weighting of performance profiles is established

Ash & Hayes-Roth (1996, *Artificial Intelligence* 88:317-347, DOI
10.1016/S0004-3702(96)00024-0) developed action-based hierarchies for
real-time diagnosis in which performance through the diagnostic process is
weighted by a deadline distribution. Their formulation explicitly integrates
time-varying action utility against the probability distribution of deadlines.

Therefore the present programme must not claim novelty for the generic kernel

\[
\int P(t)m(t)\,dt
\]

or for weighting a decision process by a deadline distribution.

This directly demotes the general value-of-time overlap identity from a novelty
claim to an interface/result-organizing device.

The remaining candidate is the **sharp composition with this repository's
finite structural frontier**:

\[
I_h=\min\{m,F_b(n,h)\}
\]

and

\[
R_{\max}
=
v\max_h[S(h)-S(I_h)].
\]

The distinction is that the finite ecological information architecture gives an
exact attainable frontier before deadline weighting, and the same constructive
witnesses attain the deadline-weighted ecological envelope.



### Adaptivity-gap theory already compares adaptive and nonadaptive expected value

A large algorithms literature studies the **adaptivity gap**: the ratio or
difference between the expected value/cost of optimal adaptive and nonadaptive
policies.

Examples include stochastic probing, stochastic packing, stochastic Boolean
function evaluation, adaptive submodular optimization, and recent exact/sharp
adaptivity-gap results in specialized models.

Therefore the present programme must not claim novelty for:

- defining a value gap between adaptive and nonadaptive policies;
- showing that adaptivity can have a large expected-value advantage;
- optimizing expected reward over adaptive trees;
- calling that advantage an "adaptivity gap."

The current claim is narrower and structurally stronger in a different
direction:

1. the hidden-world/query model has an exact attainable frontier
   \((h,I_h)\) at fixed world count, query count and query arity;
2. **every** finite nonincreasing completion-value function \(U\) lifts that
   frontier sharply as a **robust worst-state margin**:
   \[
   \max[U(C_A)-U(C_F)]
   =
   \max_h[U(h)-U(I_h)];
   \]
3. the same constructive witnesses attain the lifted robust envelope;
4. the envelope yields an exact architecture-cost threshold for positive net
   value in every represented world.

This robust envelope is not an upper bound on expected adaptive value under a
specific world-frequency distribution. Expected-value adaptivity gaps remain a
separate, established class of problems and require branch probabilities and
completion-time profiles.

A targeted search found broad adaptivity-gap and deadline-utility literatures,
but not this particular fixed-\((n,m,b)\), guaranteed-resolution, arbitrary
monotone-completion-value envelope.

That absence is not a priority proof. It defines the current defensible novelty
boundary.



### Log-depth adaptive versus near-linear nonadaptive burden is not new by itself

Adaptivity-gap results for stochastic Boolean function evaluation already
contain address-function and formula families in which adaptive evaluation uses
a short routing sequence while nonadaptive evaluation pays a much larger
testing burden. Hellerstein et al. study gaps reaching order \(n/\log n\) in
general formula settings.

Therefore RF4 must not be sold as the discovery that routing can replace a
large simultaneous burden by logarithmic adaptive depth.

The narrower ecological statement is:

- exponential opportunity value introduces an external natural-history
  timescale \(1/\mu\);
- retaining any fixed fraction \(1-\varepsilon\) of the full timely-resolution
  value forces
  \[
  C_A=\Theta(\log(1/\mu)),
  \qquad
  C_F,n,m=\Theta(1/\mu);
  \]
- these orders are derived from the same exact finite routing frontier and are
  both necessary and constructively sufficient.

So the candidate contribution is a **natural-history-dependent complexity
requirement**, not the generic existence of logarithmic adaptive routing.



### Sensory-system cost/fidelity tradeoffs and strategy switching are established

Sensory ecology and theoretical biology already contain explicit models in which:

- sensory fidelity has a biological cost;
- environmental noise changes the optimal measurement strategy;
- more sophisticated sensing is favored only when its performance benefit
  exceeds energetic or implementation cost;
- sensory systems and decision policies can coevolve.

Relevant anchors include work on the evolution of sensory fidelity and recent
signal-detection models of joint sensory/decision-system evolution.

Therefore the present programme must not claim novelty for:

- costly sensory complexity;
- an optimal sensory resolution;
- sensory strategies changing with environmental uncertainty;
- cognition/sensing being favored only when information is valuable enough.

The narrower RF2.3a claim is a finite-routing **global no-go**:

> after cue arity \(b\) is fixed, there is an exact robust cost ceiling
> \(K_{\rm crit,robust}^{(b)}\) that cannot be overcome by adding arbitrarily
> many worlds or query resources.

The inverse threshold

\[
b_{\min}(K;U)
\]

is meaningful only in this model-specific sense. Cue arity is the number of
distinguishable outcomes of one declared query, not receptor count, neural
dimensionality, or sensory fidelity in general.



### Adaptive-tree flattening into all possible queries is established

The generic simulation

\[
\text{adaptive depth }h
\Longrightarrow
\text{nonadaptive query all internal nodes}
\]

is not novel.

For binary-outcome query algorithms, recent query-complexity literature
explicitly uses the bound

\[
1+2+\cdots+2^{h-1}
=
2^h-1
\]

to convert an adaptive \(h\)-query computation tree into a nonadaptive query
set. For example, *Adaptive Query Algorithms for Relational Structures Based
on Homomorphism Counts* (MFCS 2025) uses exactly this flattening argument.

Therefore the programme must not claim novelty for:

- the existence of adaptive-to-nonadaptive flattening;
- the crude \(b\)-ary internal-node ceiling
  \[
  J_b(h)=\frac{b^h-1}{b-1};
  \]
- exponential adaptive/nonadaptive separations in query complexity by
  themselves.

The narrower candidate is the **fixed-resource sharpness** inside the present
target-resolution model:

- the exact frontier
  \[
  (C_A,C_F)=(h,\min\{m,F_b(n,h)\})
  \]
  is attained at every feasible depth;
- represented-world count \(n\), query count \(m\), and query arity \(b\) are
  simultaneously controlled;
- private opposite-target pairs certify fixed necessity;
- natural-history value then lifts that attainable frontier exactly.

So the biological paper should treat flattening as a known upper-bound idea and
place any novelty on the sharp finite frontier plus its evolutionary
interpretation.



### Distribution-dependent expected tree depth is established

Decision-tree theory has long treated expected cost under a prior distribution
as distinct from worst-case depth. High-probability states being placed in
shallow leaves is therefore not a novelty claim.

Recent and classical decision-tree work explicitly writes expected depth/cost as

\[
\sum_\ell p_\ell d_\ell
\]

and studies trade-offs between worst and expected performance.

Therefore MAIN 4 must not be sold as:

- skewed encounter frequencies favoring shallow branches;
- priors changing expected decision cost;
- expected value exceeding worst-state value.

The narrower finite-routing result is the exact ceiling:

\[
\boxed{
\sup R_{\rm expected}(n,m,b)
=
U(1)-U(\min\{m,n-1\})
}
\]

for every \(b\ge2\), with a binary private-pair construction attaining the
supremum.

The model-specific consequence is that cue arity remains important for robust
statewise evolvability but disappears from the exact finite-scope expected
ceiling once encounter frequencies may be arbitrarily skewed.

That arity contrast, rather than skewed priors themselves, is the defensible
claim.



### The fixed resolver is a test-collection problem, not a new object

The fixed side of the model is closely related to the classical minimum test
collection / minimum test set / minimum test cover literature.

In the classical Test Collection Problem, one selects a minimum subset of
binary tests whose joint outcomes distinguish the relevant entities. The
Generalized Test Collection Problem (Douek-Pinkovich, Ben-Gal & Raviv 2021,
*TOP* 29:372–386, DOI 10.1007/s11750-020-00554-1) extends this to categorical
test outputs, multiple readings per state/class and heterogeneous test costs.

That literature is especially close to the present fixed resolver because a
fixed query set must jointly separate every represented pair that carries a
different focal target.

Therefore V6 must not claim novelty for:

- selecting a minimum fixed resolving set of tests;
- categorical test outcomes;
- multiple environmental readings mapping to one target class;
- fixed test-selection cost minimization.

The candidate mathematical contribution is the **joint adaptive/fixed
frontier** in one target-resolution model:

\[
\boxed{
(C_A,C_F)
=
\left(
h,\min\{m,F_b(n,h)\}
\right)
}
\]

attained for every feasible adaptive depth \(h\), with world count \(n\),
available query count \(m\), and query arity \(b\) simultaneously controlled.

So the novelty boundary is not:

> fixed test collections exist,

nor:

> adaptive trees can be flatter than fixed tests,

but rather:

> the two established viewpoints can be closed into one exact finite attainable
> frontier, which can then be lifted and inverted by biological completion
> value.

A targeted search across test-collection, separating-system and decision-tree
literatures did not identify this exact fixed-\((n,m,b)\), all-depth joint
frontier. That absence is not a priority proof and should not be written as
such in the manuscript.



### Three-way positive/negative/uncertain triage is established

A first-stage decision that returns positive, negative, or uncertain and
continues testing only uncertain cases is established sequential diagnosis
practice and decision-tree design.

For example, the serial risk-score approach in clinical classification
(*A Serial Risk Score Approach to Disease Classification that Accounts for
Accuracy and Cost*, PMC4790436) explicitly divides subjects into positive,
negative and neutral/undecided categories and sends undecided subjects for
additional testing. Sequential diagnostic testing with inconclusive outcomes
is likewise discussed in the statistical testing literature (DOI
10.1002/sim.4358).

Therefore the target-prevalence extension must not claim that a three-outcome
cue with two pure decisions plus an ambiguous continuation is a new behavioral
or diagnostic architecture.

The narrower candidate result is the *sharp capacity contrast* for the
declared finite hidden-world/query comparator:

- fixing the prevalence of the two target classes at alpha and 1-alpha;
- allowing arbitrarily many finite worlds and queries, but requiring all world
  probabilities to be positive;
- comparing to one universal fixed resolving bundle;
- proving the exact binary supremum
  \[
  aU(1)+(1-a)U(2)-U_\infty
  \]
  against the ternary-or-higher supremum
  \[
  U(1)-U_\infty,
  \]
  where a=max(alpha,1-alpha);
- obtaining an exact cue-arity feasibility threshold from the difference.

This does not establish a new general theory of triage, nor does it identify
real sensory receptor number from mathematical cue arity.


## What remains repository-specific

The defensible contribution is the composition of layers that the existing finite theory already makes exact upstream.

### 1. Exact finite conditional-routing structure as the source object

The repository begins with a declared hidden-world / target / query system and exact objects such as:

[
C_A,
qquad
C_F,
]

cost-only continuation structure, and the productive frontier.

The ecological timing layer is downstream of these exact finite objects rather than replacing them with a generic reaction-time model.

### 2. Explicit claim ceiling for C_A

The opportunity-fitness branch establishes that:

[
C_A
]

is a minimax guaranteed-resolution estimand.

It is not:

- fitness;
- expected decision time;
- the uniquely predicted evolved policy;
- a sufficient summary of pathwise ecological performance.

This claim-boundary correction is important because earlier adaptive-gain manuscript versions risked reading C_A too biologically.

### 3. Exact interface from feasible decision topology to ecological policy selection

The finite task defines which contingent trees are feasible.

Natural history then supplies:

- world frequencies (p_x);
- time-dependent ecological value (V(t));
- architecture costs;
- comparator semantics.

The selected tree solves a biological objective over the finite feasible-policy space.

The contribution is therefore not the existence of expected-cost trees, but the explicit interface:

[
oxed{
	ext{finite routeable topology}
	o
	ext{feasible policy set}
	o
	ext{completion-time profiles}
	o
	ext{ecological value of time}
	o
	ext{selection}.
}
]

### 4. Ecological opportunity shape as a microfoundation for architecture-payoff curvature

PAYOFF already owns the generic convex-recovery architecture barrier.

The opportunity-fitness branch instead derives the shape of recovery from a measurable natural-history time process.

For a general opportunity survival function, the branch derives

[
R''(r)
=
q(c)
left[
h(c)^2(1-q(c))-h'(c)
ight].
]

This identifies how the ecological hazard shape can generate:

- increasing returns;
- decreasing returns;
- mixed curvature.

The novelty candidate is therefore a microfoundation of the recovery geometry, not the convex tangent/secant theorem itself.

### 5. Same finite sensing task, ecology-induced policy rewiring

The FP2 witness holds fixed:

- worlds;
- target;
- cue vocabulary;
- cue costs;
- world frequencies.

Changing only the ecological value-of-delay parameter changes the fitness-optimal tree at the exact threshold

[
mu=log2.
]

Time-pressure effects on planning depth and strategy are known in cognitive science, so the generic idea is not new.

The narrower claim is that a fixed ecological cue topology can support a sharp switch between balanced and prioritized **information-acquisition trees** solely because natural history changes the marginal value of early completion.

Whether that is publishably novel requires a targeted search in time-sensitive decision-tree induction, ecological sensory decision models and state-dependent cue-order evolution.

## Current novelty hierarchy

Strongest current candidate:

> Exact finite information constraints determine a sharp **frequency-free robust-value frontier**; natural history re-ranks that frontier, while encounter frequencies separately determine any additional expected-fitness value.

Supporting results:

1. C_A is guaranteed complexity, not fitness.
2. Fitness depends on the overlap between completion profiles and ecological value of time.
3. Comparator architecture can reverse the sign of selection.
4. Opportunity hazard shape determines the curvature of time-saving payoff.
5. Ecological urgency can change the optimal cue order without changing the available cues or state frequencies.

## Claims to avoid

Do not headline:

- routeability is useful;
- sequential cues save effort;
- faster decisions can be fitter;
- response-time distributions matter;
- worst-case and expected-cost trees differ;
- stochastic dominance orders policies;
- deadlines change optimal decisions;
- convex recovery can create a local/global gap.

All are established or too close to established general results.

The paper must earn novelty from the **cross-layer ecological mechanism and exact finite structural constraints**, not from rebranding generic decision theory.
