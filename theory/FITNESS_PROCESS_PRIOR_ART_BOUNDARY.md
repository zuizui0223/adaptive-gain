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
