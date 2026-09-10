# Finite information structure constrains evolutionary timescales and feedback phases

## Abstract

Rapid evolutionary change over short intervals can coexist with weak long-term divergence, but fluctuating-selection and stabilizing-selection theory already explain why short-term activity need not accumulate. We ask a different question: when state-dependent selection is generated through finite information use, which evolutionary amplitudes, timescales, and feedback phases are structurally reachable? For each recurrent community state, we represent information use as a finite sensing task with an optimal adaptive cost and a corresponding fixed separating-test cost. Their structural difference is linked, under an explicit ecological lift, to state-dependent selection or feedback, while transitions among the same community states determine temporal recurrence. This common state space couples structural amplitude to temporal filtering. We derive four results. First, finite structural reward range and community persistence jointly impose a sharp ceiling on long-run evolutionary fluctuation. Second, a required feedback regime implies a required structural gap and therefore a minimum, or under bounded query arity a Pareto-minimal, finite information structure. Third, long-term stasis has two dynamically distinct origins: neutral cancellation under temporally opposing selection and attractive restoration under endogenous feedback. Fourth, within a generalized local model, monotone return can admit a zero-feedback decomposition whereas a complex eigenpair forces positive feedback existence even though its magnitude remains unidentified. Existing theory already covers information use, cognitive constraints, separating systems, decision trees, fluctuating selection, and eco-evolutionary feedback. The contribution here is their exact ecological composition: finite information structure restricts which evolutionary fluctuations and local feedback regimes are reachable within the declared model class.

## 1. Introduction

Rapid evolutionary change can occur on ecological timescales, yet strong short-term evolutionary activity need not accumulate into comparably large long-term divergence. This mismatch is not itself a theoretical puzzle without precedent. Ecological and evolutionary dynamics can overlap in time, selection can fluctuate strongly in direction and magnitude, and stabilizing or temporally reversing selection can reconcile rapid local change with long periods of apparent stasis (Hairston et al. 2005; Estes & Arnold 2007; Bell 2010; Uyeda et al. 2011; Messer et al. 2016). The relevant question for the present paper is therefore not why short-term evolution can cancel or be restored. It is what determines which amplitudes and temporal regimes are reachable before those downstream evolutionary dynamics are specified.

Information use is a natural place to look for such upstream constraints. Organisms do not respond to ecological states through unconstrained access to all relevant variables. They acquire, combine, and act on finite cues, often under costs of sampling, attention, memory, or processing. Evolutionary ecology already treats information acquisition as an adaptive decision problem, and limited attention, cue reliability, sampling effort, and memory are established constraints on behaviour and plasticity (Dall et al. 2005; Dukas 2004; Schmidt et al. 2010; Wright 2022). Richer or more reliable cue combinations can improve adaptive responses, whereas costly or unreliable information can limit them. We therefore do not claim novelty for the idea that information constrains adaptation, nor for sequential cue use, learning, or state-dependent decision making.

A separate mathematical literature asks how finite states can be distinguished by tests. In the non-adaptive formulation, minimum test sets, separating systems, and test covers seek the smallest collection of attributes that distinguishes all relevant entities. In the adaptive formulation, decision trees choose later tests conditionally on earlier outcomes. Binary and multiway decision trees, optimal decision-tree depth, and adaptive-versus-non-adaptive advantages are classical topics. Our use of this machinery is deliberately instrumental. We treat finite information complexity as an ecological structural variable and ask what it permits downstream. No novelty claim is attached to minimum test cover, decision trees, bounded outcome arity, generic adaptivity gaps, or the rooted-tree extremal formulas used internally.

Consider a recurrent community state `i`. The state defines a finite sensing task: a set of ecologically relevant alternatives, a repertoire of possible cues, and the distinctions that must be resolved before a state-contingent action can be taken. Let `C_A(i)` denote the least guaranteed cost of resolving that task adaptively and `C_F(i)` the corresponding fixed information requirement. Their difference

\[
g_i=C_F(i)-C_A(i)
\]

is not assumed to be fitness by itself. Under an explicit ecological lift, however, it bounds or generates a state-dependent selection or feedback contribution. The same recurrent state space also determines how those rewards reappear through time via a community transition operator. Selection amplitude and temporal recurrence are therefore indexed by the same ecological states and constrained upstream by the same finite information structure.

This construction leads to a reachability problem. Given a finite cue repertoire, a bound on query outcomes, and a recurrent community process, how large can structurally generated selection fluctuations become? Conversely, if a particular local evolutionary regime requires a minimum feedback gain, how complex must the underlying finite information structure be before that regime is possible? We derive four results: a sharp structural-temporal ceiling on long-run fluctuation; a map from dynamical requirements to minimum or Pareto-minimal information complexity; a distinction between neutral cancellation and attractive restoring stasis; and a feedback-existence result separating monotone from oscillatory local return.

## 2. Model

### 2.1 Recurrent ecological states and finite sensing tasks

We consider a finite set of recurrent ecological or community states indexed by `i=1,...,K`. A state summarizes the ecological context relevant to an organism's decision problem at a given time: for example a resource assemblage, predator regime, pollinator context, host community, or another finite configuration that changes which distinctions must be resolved before a state-contingent action can be taken.

Within state `i`, the organism faces a finite sensing task described by four ingredients. **Represented alternatives**, or worlds, are the ecological alternatives that remain behaviorally distinct before sensing. **Declared cues**, or queries, are available deterministic information sources. Asking a query partitions the alternatives according to possible outcomes. **Outcome arity** `b` is the maximum number of outcomes available from one cue. Finally, the **required distinctions** specify which alternatives must be distinguished to guarantee the declared state-contingent action.

This abstraction represents finite natural-history structure rather than a universal model of perception. The relevant alternatives and cues are declared by the biological application. The present theory assumes deterministic outcomes and guaranteed resolution; noisy likelihoods and probabilistic stopping rules lie outside the current scope.

### 2.2 Adaptive and fixed information costs

Let `C_A(i)` be the minimum worst-case number of unit-cost cue acquisitions required to resolve the declared target adaptively in state `i`. An adaptive policy can choose later cues conditionally on previous outcomes and is represented by a decision tree. Let `C_F(i)` be the minimum number of cue resources that must be acquired as a fixed set to guarantee the same resolution. The structural adaptive gap is

\[
\boxed{g_i=C_F(i)-C_A(i).}
\]

The gap measures how much fixed information burden can be avoided when cue acquisition branches conditionally. It is a structural property of the declared sensing task and is not itself fitness.

For the fixed problem, only irreducible required distinctions contribute to the minimal fixed burden. We denote the retained family of minimal productive obligations by `H_min` and its size by

\[
E_i=|H_{\min}(i)|.
\]

`Productive frontier` is repository terminology for this retained obligation family. We use its edge count only where it constrains downstream fixed cost and structural gap; the quotient and proof machinery are supplementary.

### 2.3 Structural lift to selection

To connect information structure to evolution, we declare

\[
\boxed{s_i=\lambda g_i-\kappa,}
\]

where `lambda>0` converts one unit of structural gap into a state-dependent selection contribution and `kappa` is a state-independent maintenance cost. This is an explicit modelling assumption; `C_F-C_A` is not intrinsically fitness.

If `pi` is the stationary distribution and `bar s=sum_i pi_i s_i`, then

\[
s_i-\bar s=\lambda(g_i-\bar g).
\]

Thus state-independent maintenance cost shifts mean selection but not centered temporal geometry.

### 2.4 Community recurrence

Let ecological states evolve as a finite ergodic Markov chain with transition matrix `P` and stationary distribution `pi`. The same state index carries two roles: its finite sensing task generates structural reward `g_i`, while `P` determines when that reward recurs.

For centered reward vector `c=s-\bar s 1`, define

\[
\gamma(k)=\sum_i\pi_i c_i[P^k c]_i.
\]

For cumulative centered selection over horizon `H`,

\[
\operatorname{Var}(S_H)=H\gamma(0)+2\sum_{k=1}^{H-1}(H-k)\gamma(k).
\]

When `P` is reversible,

\[
\boxed{\sigma_{\rm eff}^2=\sum_r w_r\frac{1+r_r}{1-r_r},}
\]

where `r_r` is a nontrivial community eigenvalue and `w_r` the squared reward projection onto that mode.

### 2.5 Local endogenous feedback

Let `alpha` denote intrinsic persistence of the evolutionary coordinate, `phi` persistence of the ecological/community coordinate, and `G` net feedback gain. The local invariants are

\[
\boxed{T=\alpha+\phi,}\qquad
\boxed{D=\alpha\phi+(1-\phi)G.}
\]

A mechanistic factorization is `G=-beta Delta s e`. Under `Delta s=lambda Delta g`,

\[
\boxed{G=a\Delta g,}\qquad a=(-\beta e)\lambda>0
\]

for restoring negative ecological feedback.

For `0<=alpha<=1` and `0<=phi<1`, local stability requires

\[
\alpha-1<G<\frac{1-\alpha\phi}{1-\phi},
\]

and the real-to-complex threshold is

\[
\boxed{G_{\rm osc}=\frac{(\alpha-\phi)^2}{4(1-\phi)}.}
\]

### 2.6 Information-complexity support

For unit-cost sensing with at most `b` outcomes per query, let `F_b(n,h)` denote the supporting rooted-tree extremal count under world, depth, and arity constraints. A task with adaptive optimum `C_A=h` obeys

\[
\boxed{C_F\le\min\{m,E,F_b(n,h)\}.}
\]

Hence gap `q=C_F-C_A` requires `min{m,E,F_b(n,h)}>=h+q`. For binary sensing this yields one exact first corner; for higher arity the exact joint requirement is generally a Pareto frontier over `(n,m,E)`.

## 3. Results

### 3.1 Structural and temporal constraints jointly bound long-run fluctuation

If `0<=g_i<=g_max`, the state-dependent selection range is at most `lambda*g_max` and its stationary variance is at most `(lambda*g_max)^2/4`. For a reversible community chain with largest nontrivial algebraic eigenvalue `r_max<1`,

\[
\boxed{\sigma_{\rm eff}^2\le\frac{(\lambda g_{\max})^2}{4}\frac{1+r_{\max}}{1-r_{\max}}.}
\]

The bound is sharp, attained by a symmetric two-state chain with endpoint structural rewards. Finite information structure caps selection amplitude; community persistence controls temporal retention. Slow ecological modes matter only when structural rewards project onto them.

For nonzero stationary mean-selection magnitude `|mu|`,

\[
H_{\times}^{\rm asy}\le\frac{(\lambda g_{\max})^2}{4\mu^2}\frac{1+r_{\max}}{1-r_{\max}},
\]

an asymptotic crossover proxy rather than a finite-time hitting-time bound.

### 3.2 Required dynamics imply minimum or Pareto-minimal information complexity

For binary unit-cost sensing and required integer gap `q>=1`, define

\[
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\}.
\]

The exact componentwise first corner is

\[
\boxed{(n^*,m^*,E^*)=(h_2^*+q+1,\ h_2^*+q,\ h_2^*+q).}
\]

Moreover `h_2^*(q)=log_2 q+O(1)`.

For maximum query arity `b>=2`,

\[
h_b^*(q)=\min\left\{h\ge1:\frac{b^h-1}{b-1}-h\ge q\right\},
\]

with

\[
\boxed{m_{\min}=E_{\min}=q+h_b^*(q),}
\qquad
\boxed{n_{\min}=q+h_2^*(q)+1.}
\]

These minima need not be jointly attainable; the exact bounded-arity object is generally a Pareto frontier `P_b(q)`. For `q=3,b=4`, `(8,5,5)` and `(7,6,6)` are both nondominated.

With local feedback `G=a Delta g`,

\[
\boxed{(\alpha,\phi,a,b)\longrightarrow q_{\rm osc}\longrightarrow\mathcal P_b(q_{\rm osc}).}
\]

Under `alpha=1`, `phi=1/2`, `a=1/8`, the first stable oscillatory gap is `q_osc=2`, giving `(n,m,E)=(6,5,5)`.

### 3.3 Stasis has two dynamically distinct origins

For additive periodic weak selection `z_{t+1}=z_t+E beta_t`, if one period satisfies `sum beta_t=0`, the full-period map is

\[
\boxed{F_P(z)=z}
\]

with multiplier one. Within-cycle activity can be arbitrarily large, but perturbations persist. This is neutral cancellation stasis.

By contrast, an endogenous equilibrium with `rho(J)<1` is attractive: perturbations decay. Thus

\[
\boxed{\text{cancellation stasis}=\text{zero period drift + neutral return},}
\]

\[
\boxed{\text{restoring stasis}=\text{zero equilibrium drift + attraction}.}
\]

### 3.4 Oscillation forces feedback existence within the generalized model

For every candidate `phi<1`,

\[
G(\phi)=\frac{\phi^2-T\phi+D}{1-\phi}.
\]

If the local eigenvalues are real and satisfy `0<=r_1,r_2<1`, taking `phi=r_1`, `alpha=r_2` gives `G=0`. Stable monotone return therefore remains compatible with zero feedback.

If the eigenvalues are a non-real conjugate pair, the characteristic polynomial is strictly positive for every real `phi`, so every admissible decomposition satisfies

\[
\boxed{G(\phi)>0.}
\]

Oscillatory local dynamics therefore force feedback existence within the generalized model, although feedback magnitude remains unidentified.

## 4. Discussion

The central result is not that rapid short-term evolution can coexist with long-term stasis. The new claim is narrower: when state-dependent selection is generated through a finite information structure, the range of evolutionary dynamics available to the system is constrained upstream.

### 4.1 Finite information couples evolutionary amplitude to temporal fate

Phenomenological models of fluctuating selection can vary amplitude and temporal autocorrelation independently. Here both are tied to the same recurrent ecological states. Finite sensing structure constrains the structural reward available at each state, while transitions among those states determine temporal recurrence. Community persistence is therefore not itself an evolutionary timescale: slow modes matter only when reward projects onto them.

### 4.2 Required dynamics imply required information complexity

The reverse map gives the static combinatorics a direct ecological role. A required feedback phase implies a required gain, that gain implies a structural gap, and the gap imposes lower bounds on finite sensing structure. Higher cue arity can reduce query/frontier burden without reducing the minimum number of ecological alternatives represented, exposing a Pareto tradeoff between ecological-state complexity and information-channel complexity.

The productive frontier is retained only where it carries downstream weight. Its edge count records irreducible separation obligations; capping those obligations caps fixed information burden and hence reachable feedback gain.

### 4.3 Stasis does not identify one mechanism

Little long-term net change can arise from neutral temporal cancellation or from active restoration. Under cancellation, strong short-term changes cancel and perturbations survive. Under restoring stasis, feedback erases perturbations. The two mechanisms are dynamically distinct even when both produce negligible long-term net divergence.

### 4.4 Oscillation has a different mechanistic status from monotone return

Within the generalized local model, monotone return may be explained without feedback by reallocating persistence between evolutionary and ecological coordinates. A complex local mode cannot. Oscillation therefore excludes the zero-feedback decomposition inside the declared model class, although it does not identify feedback magnitude or prove that finite sensing structure caused the feedback.

### 4.5 Natural history enters upstream

Finite sensing tasks should be grounded in natural history: the application defines relevant alternatives, available cues, and required distinctions before the evolutionary model is evaluated. This does not require a separate observation-design theory. Natural history specifies feasible information structure and ecological feedback, not a measurement protocol.

### 4.6 Relation to existing theory

Information use, limited attention, sampling costs, memory, cue reliability, separating systems, optimal and multiway decision trees, adaptivity gaps, fluctuating selection, temporal autocorrelation, and generic eco-evolutionary feedback are prior art. We also make no novelty claim for the bounded-arity tree extremal formulas used internally.

The contribution is their exact ecological composition: finite information complexity bounds structurally generated selection; recurrence of the same community states determines temporal filtering; and downstream dynamical requirements translate back into minimum or Pareto-minimal information structures.

## 5. Scope and limitations

The sensing theory is finite, deterministic, and guaranteed-resolution, with unit acquisition costs in the sharp information-complexity results. Structural gaps are connected to selection or feedback through declared lifts rather than a physiological derivation. The sharp structural-temporal ceiling assumes a finite ergodic reversible community chain. The local feedback results concern deterministic linearization around an equilibrium and are not a global bifurcation theory. The framework does not include mutation, migration, drift, demographic stochasticity, multivariate quantitative genetics, noisy cue likelihoods, or continuous compatible sets.

The pair `(T,D)` does not uniquely identify `(alpha,phi,G)`, so an observed local timescale cannot generally be decomposed uniquely into evolutionary persistence, community persistence, and feedback. We retain this only as a limit on interpreting evolutionary time; no observation-design program is developed here.

## 6. Conclusion

Evolutionary time is often described in terms of how quickly traits change or how long those changes persist. The present results suggest an upstream structural question: what selection contrasts can an organism's finite information system generate at all? Finite information structure limits the amplitude that can be produced, community recurrence limits how that amplitude persists through time, and feedback requirements impose minimum information complexity before particular local phases become reachable. Within the declared model class, individual information structure is therefore a constraint on the evolutionary dynamics available to the ecological system.

## References cited in the current draft

- Bell, G. 2010. Fluctuating selection: the perpetual renewal of adaptation in variable environments. Philosophical Transactions of the Royal Society B 365:87–97.
- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. 2005. Information and its use by animals in evolutionary ecology. Trends in Ecology & Evolution 20:187–193.
- Dukas, R. 2004. Causes and consequences of limited attention. Brain, Behavior and Evolution 63:197–210.
- Estes, S. & Arnold, S. J. 2007. Resolving the paradox of stasis: models with stabilizing selection explain evolutionary divergence on all timescales. The American Naturalist 169:227–244.
- Hairston, N. G. Jr., Ellner, S. P., Geber, M. A., Yoshida, T. & Fox, J. A. 2005. Rapid evolution and the convergence of ecological and evolutionary time. Ecology Letters.
- Messer, P. W., Ellner, S. P. & Hairston, N. G. Jr. 2016. Can population genetics adapt to rapid evolution? Trends in Genetics 32:408–418.
- Schmidt, K. A., Dall, S. R. X. & van Gils, J. A. 2010. The ecology of information: an overview on the ecological significance of making informed decisions. Oikos.
- Uyeda, J. C., Hansen, T. F., Arnold, S. J. & Pienaar, J. 2011. The million-year wait for macroevolutionary bursts. PNAS 108:15908–15913.
- Wright, J. 2022. A reaction norm framework for the evolution of learning: how cumulative experience shapes phenotypic plasticity. Biological Reviews.

## Supplement map

Proofs and implementation details remain outside the main narrative, including continuation quotients, residual fixed-side kernels, certificate ladders, exhaustive small-world enumeration, bounded-arity recurrence proofs, private-pair constructions, critical-slowing asymptotics, exact transient-period ceilings, AR(2) inversion algebra, and solver-cap details.
