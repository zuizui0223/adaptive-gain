# Finite information structure constrains evolutionary timescales and feedback phases

## Abstract

Rapid evolutionary change over short intervals can coexist with weak long-term divergence, but fluctuating- and stabilizing-selection theory already explain why short-term activity need not accumulate. We ask a different question: when state-dependent selection is generated through finite information use, which evolutionary amplitudes, timescales, and feedback phases are structurally reachable? For each recurrent community state, we represent information use as a finite sensing task with an optimal adaptive cost and a corresponding fixed separating-test cost. Their structural difference is linked, under an explicit ecological lift, to state-dependent selection or feedback, while transitions among the same states determine temporal recurrence. We derive four results. First, finite structural reward range and community persistence jointly impose a sharp ceiling on long-run evolutionary fluctuation. Second, a required feedback regime implies a required structural gap and therefore a minimum, or under bounded query arity a Pareto-minimal, finite information structure. Third, long-term stasis has two dynamically distinct origins: neutral cancellation and attractive restoration. Fourth, within a generalized local model, monotone return can admit a zero-feedback decomposition whereas a complex eigenpair forces positive feedback existence even though its magnitude remains unidentified. The contribution is the ecological composition of these levels: finite information structure restricts which evolutionary fluctuations and local feedback regimes are reachable within the declared model class.

## 1. Introduction

Rapid evolutionary change can occur on ecological timescales, yet strong short-term activity need not accumulate into comparably large long-term divergence. Ecological and evolutionary dynamics can overlap in time, selection can fluctuate strongly, and stabilizing or temporally reversing selection can reconcile rapid local change with long periods of apparent stasis (Hairston et al. 2005; Estes & Arnold 2007; Bell 2010; Uyeda et al. 2011; Messer et al. 2016). The question here is therefore not why short-term evolution can cancel or be restored, but what constrains the amplitudes and temporal regimes that are reachable upstream.

Information use provides one such upstream constraint. Organisms acquire and combine finite cues under limits of sampling, attention, memory, and reliability; evolutionary ecology already treats this as an adaptive decision problem (Dall et al. 2005; Dukas 2004; Schmidt et al. 2010; Wright 2022). Separately, minimum test sets, separating systems, and adaptive decision trees characterize fixed and sequential finite-state identification. We use that machinery only as a structural coordinate and make no novelty claim for information use, test cover, decision trees, bounded outcome arity, or generic adaptive advantage.

For recurrent community state `i`, let `C_A(i)` be the least guaranteed adaptive cost of resolving the declared sensing task and `C_F(i)` the corresponding fixed information requirement. Their difference

\[
g_i=C_F(i)-C_A(i)
\]

is linked, through an explicit ecological lift, to state-dependent selection or feedback. The same recurrent state space determines how those rewards reappear through time via a community transition operator. This creates a reachability problem: how large can structurally generated evolutionary fluctuations become, and what finite information complexity is required before a specified feedback regime becomes possible?

We derive four results: a sharp structural-temporal ceiling on long-run fluctuation; a map from dynamical requirements to minimum or Pareto-minimal information complexity; a distinction between neutral cancellation and attractive restoring stasis; and a feedback-existence result separating monotone from oscillatory local return.

## 2. Model

### 2.1 Recurrent ecological states and finite sensing tasks

We consider recurrent ecological or community states `i=1,...,K`. Each state defines a finite sensing task: **represented alternatives** (worlds), **declared cues** (queries), an outcome-arity cap `b`, and the **required distinctions** needed to guarantee the declared state-contingent action. The biological application declares these alternatives and cues. The present theory assumes deterministic outcomes and guaranteed resolution; noisy likelihoods and probabilistic stopping lie outside scope.

### 2.2 Adaptive and fixed information costs

Let `C_A(i)` be the minimum worst-case number of unit-cost cue acquisitions required adaptively in state `i`, and `C_F(i)` the minimum fixed cue set required for the same resolution. Define

\[
\boxed{g_i=C_F(i)-C_A(i).}
\]

For the fixed problem, let `H_min` denote the retained family of irreducible productive obligations and

\[
E_i=|H_{\min}(i)|.
\]

`Productive frontier` is repository terminology for this obligation family; only its edge count enters the main ecological argument.

### 2.3 Structural lift to selection

We declare

\[
\boxed{s_i=\lambda g_i-\kappa,}
\]

where `lambda>0` converts structural gap into a state-dependent selection contribution and `kappa` is state-independent maintenance cost. This is a modelling assumption: the structural gap is not intrinsically fitness. If `pi` is the stationary distribution and `bar s=sum_i pi_i s_i`, then

\[
s_i-\bar s=\lambda(g_i-\bar g).
\]

### 2.4 Community recurrence

Let ecological states evolve as a finite ergodic Markov chain with transition matrix `P` and stationary distribution `pi`. For centered reward vector `c=s-\bar s 1`, define

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

Let `alpha` denote intrinsic evolutionary persistence, `phi` ecological/community persistence, and `G` net feedback gain. The local invariants are

\[
\boxed{T=\alpha+\phi,}\qquad
\boxed{D=\alpha\phi+(1-\phi)G.}
\]

A mechanistic factorization is `G=-beta Delta s e`. Under `Delta s=lambda Delta g`,

\[
\boxed{G=a\Delta g,}\qquad a=(-\beta e)\lambda>0
\]

for restoring negative ecological feedback. For `0<=alpha<=1` and `0<=phi<1`, local stability requires

\[
\alpha-1<G<\frac{1-\alpha\phi}{1-\phi},
\]

and the real-to-complex threshold is

\[
\boxed{G_{\rm osc}=\frac{(\alpha-\phi)^2}{4(1-\phi)}.}
\]

### 2.6 Information-complexity support

For unit-cost sensing with at most `b` outcomes per query, let `F_b(n,h)` denote the supporting rooted-tree extremal count. A task with adaptive optimum `C_A=h` obeys

\[
\boxed{C_F\le\min\{m,E,F_b(n,h)\}.}
\]

Hence gap `q=C_F-C_A` requires `min{m,E,F_b(n,h)}>=h+q`. Binary sensing yields one exact first corner; higher arity generally yields a Pareto frontier over `(n,m,E)`.

## 3. Results

### 3.1 Structural and temporal constraints jointly bound long-run fluctuation

If `0<=g_i<=g_max`, the state-dependent selection range is at most `lambda*g_max`. For a reversible community chain with largest nontrivial algebraic eigenvalue `r_max<1`,

\[
\boxed{\sigma_{\rm eff}^2\le\frac{(\lambda g_{\max})^2}{4}\frac{1+r_{\max}}{1-r_{\max}}.}
\]

The bound is sharp, attained by a symmetric two-state chain with endpoint structural rewards. Finite information structure caps selection amplitude; community persistence controls retention, but slow modes matter only when rewards project onto them.

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

with multiplier one. Within-cycle activity can be arbitrarily large, but perturbations persist: neutral cancellation stasis.

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

### 4.1 Finite information couples evolutionary amplitude to temporal fate

Phenomenological models can vary selection amplitude and temporal autocorrelation independently. Here both are tied to recurrent ecological states: finite sensing structure constrains state-specific reward, while transitions among those states determine recurrence. Community persistence is therefore not itself an evolutionary timescale; slow modes matter only when reward projects onto them.

### 4.2 Required dynamics imply required information complexity

The reverse map gives the static combinatorics a direct ecological role. A required feedback phase implies a required gain, that gain implies a structural gap, and the gap imposes lower bounds on finite sensing structure. Higher cue arity can reduce query/frontier burden without reducing the minimum number of represented alternatives, exposing a Pareto tradeoff between ecological-state complexity and information-channel complexity.

### 4.3 Stasis and oscillation separate mechanisms

Little long-term net change can arise from neutral temporal cancellation or active restoration. Under cancellation, perturbations survive; under restoring stasis, feedback erases them. Within the generalized local model, monotone return can remain compatible with zero feedback, whereas a complex local mode cannot. Oscillation therefore has a distinct mechanistic status, although it does not identify feedback magnitude or prove that finite sensing structure caused the feedback.

### 4.4 Natural history specifies feasible information structure

Finite sensing tasks should be grounded in natural history: the application defines relevant alternatives, available cues, and required distinctions before the evolutionary model is evaluated. This does not require a separate observation-design theory. Natural history specifies feasible information structure and ecological feedback, not a measurement protocol.

### 4.5 Relation to existing theory

Information use, limited attention, sampling costs, memory, cue reliability, separating systems, optimal and multiway decision trees, adaptivity gaps, fluctuating selection, temporal autocorrelation, and generic eco-evolutionary feedback are prior art. No novelty claim is made for the bounded-arity tree extremal formulas used internally. The contribution is their ecological composition: finite information complexity bounds structurally generated selection, recurrence filters those rewards through time, and downstream dynamical requirements translate back into minimum or Pareto-minimal information structures.

## 5. Scope and limitations

The sensing theory is finite, deterministic, and guaranteed-resolution, with unit acquisition costs in the sharp information-complexity results. Structural gaps are connected to selection or feedback through declared lifts rather than physiological derivation. The sharp structural-temporal ceiling assumes a finite ergodic reversible community chain. The local feedback results concern deterministic linearization around an equilibrium and are not a global bifurcation theory. The framework does not include mutation, migration, drift, demographic stochasticity, multivariate quantitative genetics, noisy cue likelihoods, or continuous compatible sets.

The pair `(T,D)` does not uniquely identify `(alpha,phi,G)`, so an observed local timescale cannot generally be decomposed uniquely into evolutionary persistence, community persistence, and feedback. We retain this only as a limit on interpreting evolutionary time; no observation-design program is developed here.

## 6. Conclusion

Finite information structure constrains which evolutionary dynamics are available to an ecological system: it limits structurally generated selection amplitude, community recurrence filters that amplitude through time, and feedback requirements impose minimum information complexity before particular local phases become reachable. Within the declared model class, evolutionary time is therefore constrained upstream by finite individual information structure.

## References cited in the current draft

- Bell, G. 2010. Fluctuating selection: the perpetual renewal of adaptation in variable environments. Philosophical Transactions of the Royal Society B 365:87–97.
- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. 2005. Information and its use by animals in evolutionary ecology. Trends in Ecology & Evolution 20:187–193.
- Dukas, R. 2004. Causes and consequences of limited attention. Brain, Behavior and Evolution 63:197–210.
- Estes, S. & Arnold, S. J. 2007. Resolving the paradox of stasis: models with stabilizing selection explain evolutionary divergence on all timescales. The American Naturalist 169:227–244.
- Hairston, N. G. Jr., Ellner, S. P., Geber, M. A., Yoshida, T. & Fox, J. A. 2005. Rapid evolution and the convergence of ecological and evolutionary time. Ecology Letters 8:1114–1127.
- Messer, P. W., Ellner, S. P. & Hairston, N. G. Jr. 2016. Can population genetics adapt to rapid evolution? Trends in Genetics 32:408–418.
- Schmidt, K. A., Dall, S. R. X. & van Gils, J. A. 2010. The ecology of information: an overview on the ecological significance of making informed decisions. Oikos 119:304–316.
- Uyeda, J. C., Hansen, T. F., Arnold, S. J. & Pienaar, J. 2011. The million-year wait for macroevolutionary bursts. PNAS 108:15908–15913.
- Wright, J. 2022. A reaction norm framework for the evolution of learning: how cumulative experience shapes phenotypic plasticity. Biological Reviews 97:1999–2021.

## Supplement map

Proofs and implementation details remain outside the main narrative, including continuation quotients, residual fixed-side kernels, certificate ladders, exhaustive small-world enumeration, bounded-arity recurrence proofs, private-pair constructions, critical-slowing asymptotics, exact transient-period ceilings, AR(2) inversion algebra, and solver-cap details.