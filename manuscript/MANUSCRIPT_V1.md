# Finite information structure constrains evolutionary timescales and feedback phases

## Abstract

Rapid evolutionary change over short intervals can coexist with weak long-term divergence, but fluctuating- and stabilizing-selection theory already explain why short-term activity need not accumulate. We ask a different question: when state-dependent selection is generated through finite information use, which evolutionary amplitudes, timescales, and feedback phases are structurally reachable? For each recurrent community state, we represent information use as a finite sensing task with an optimal adaptive cost and a corresponding fixed separating-test cost. Their structural difference is linked, under an explicit ecological lift, to state-dependent selection or feedback, while transitions among the same states determine temporal recurrence. The principal result runs backward from dynamics to information structure: a required feedback regime implies a required structural gap and therefore a minimum, or under bounded query arity a Pareto-minimal, finite information structure. Two theorem-level results support that reachability statement. Finite structural reward range and community persistence impose a sharp extremal ceiling on long-run evolutionary fluctuation, and a model-compatible complex local eigenpair forces feedback existence within the generalized model even though its magnitude remains unidentified. A mechanistic proposition separately distinguishes neutral cancellation stasis from attractive restoration. The contribution is the ecological composition of these levels: finite information structure restricts which evolutionary fluctuations and local feedback regimes are reachable within the declared model class.

## 1. Introduction

Rapid evolutionary change can occur on ecological timescales, yet strong short-term activity need not accumulate into comparably large long-term divergence. Ecological and evolutionary dynamics can overlap in time, selection can fluctuate strongly, and stabilizing or temporally reversing selection can reconcile rapid local change with long periods of apparent stasis (Hairston et al. 2005; Estes & Arnold 2007; Bell 2010; Uyeda et al. 2011; Messer et al. 2016; Cotto & Chevin 2020). The question here is therefore not why short-term evolution can cancel or be restored, but what constrains the amplitudes and temporal regimes that are reachable upstream.

Information use provides one such upstream constraint. Organisms acquire and combine finite cues under limits of sampling, attention, memory, and reliability; evolutionary ecology already treats this as an adaptive decision problem, and prior theory explicitly treats information-processing and sensing architectures as evolutionarily shaped mechanisms (Dall et al. 2005; Dukas 2004; Schmidt et al. 2010; Trimmer & Houston 2014; Eliassen et al. 2016; Wright et al. 2022). Separately, separating systems and optimal binary or multiway decision trees characterize fixed and sequential finite-state identification (Katona 1966; Hyafil & Rivest 1976; Chakaravarthy et al. 2009). We use that machinery only as a structural coordinate and make no novelty claim for information use, test cover, decision trees, bounded outcome arity, or generic adaptive advantage.

For recurrent community state `i`, let `C_A(i)` be the least guaranteed adaptive cost of resolving the declared sensing task and `C_F(i)` the corresponding fixed information requirement. Their difference

\[
g_i=C_F(i)-C_A(i)
\]

is linked, through an explicit ecological lift, to state-dependent selection or feedback. The same recurrent state space determines how those rewards reappear through time via a community transition operator. This creates a reachability problem: how large can structurally generated evolutionary fluctuations become, and what finite information complexity is required before a specified feedback regime becomes possible?

The paper is organized around one principal reachability theorem rather than four equal claims. A required dynamical regime imposes a required structural gap and therefore a minimum or Pareto-minimal information structure. A structural-temporal extremal theorem bounds long-run fluctuation from above; a diagnostic theorem determines when a model-compatible local oscillation rules out zero feedback; and a mechanistic proposition keeps neutral cancellation stasis distinct from attractive restoration.

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

Let ecological states evolve as a finite ergodic Markov chain with transition matrix `P` and stationary distribution `pi`. Temporal autocorrelation and fluctuating selection are established evolutionary mechanisms; here the Markov representation is used only to connect recurrence of the same state-indexed structural rewards to long-run filtering (Bell 2010; Cotto & Chevin 2020). For centered reward vector `c=s-\bar s 1`, define

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

Let `alpha` denote intrinsic evolutionary persistence, `phi` ecological/community persistence, and `G` net feedback gain. Reciprocal eco-evolutionary feedback itself is established theory (Post & Palkovacs 2009; Schoener 2011); the role here is to ask how much finite sensing structure is required to reach particular local regimes. The local invariants are

\[
\boxed{T=\alpha+\phi,}\qquad
\boxed{D=\alpha\phi+(1-\phi)G.}
\]

A mechanistic factorization is `G=-beta Delta s e`. Under `Delta s=lambda Delta g`,

\[
\boxed{G=a\Delta g,}\qquad a=(-\beta e)\lambda>0
\]

for restoring negative ecological feedback. The generalized persistence domain is

\[
0\le\alpha\le1,
\qquad
0\le\phi<1,
\]

so an observed trace admits at least one persistence split exactly when

\[
\boxed{0\le T<2.}
\]

Within this domain, local stability requires

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

Hence gap `q=C_F-C_A` requires `min{m,E,F_b(n,h)}>=h+q`. Binary sensing yields one exact first corner; higher arity generally yields a Pareto frontier over `(n,m,E)`. The separating-system and multiway decision-tree literatures are used as prior-art anchors for this imported combinatorial setting, not as equivalence claims for the repository's exact arity restriction (Katona 1966; Hyafil & Rivest 1976; Chakaravarthy et al. 2009; Crowston et al. 2016).

## 3. Results

### 3.1 Principal result: required dynamics imply minimum or Pareto-minimal information complexity

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

These minima need not be jointly attainable; the exact bounded-arity object is generally a Pareto frontier `P_b(q)`. For `q=3,b=4`, `(8,5,5)` and `(7,6,6)` are both nondominated. Richer cue outcomes can therefore reduce query/frontier burden without eliminating the lower bound on how many ecological alternatives must be represented.

With local feedback `G=a Delta g`,

\[
\boxed{(\alpha,\phi,a,b)\longrightarrow q_{\rm osc}\longrightarrow\mathcal P_b(q_{\rm osc}).}
\]

Under `alpha=1`, `phi=1/2`, `a=1/8`, the first stable oscillatory gap is `q_osc=2`, giving `(n,m,E)=(6,5,5)`. More generally, if the integer gap ladder jumps directly beyond the upper stability boundary, the stable-oscillation Pareto set is empty.

This reverse map is the principal result: a requested dynamical phase imposes a lower bound on the finite natural-history information structure capable of supporting it.

### 3.2 Supporting result: structural and temporal constraints impose an extremal fluctuation envelope

If `0<=g_i<=g_max`, the state-dependent selection range is at most `lambda*g_max`. For a reversible community chain with largest nontrivial algebraic eigenvalue `r_max<1`,

\[
\boxed{\sigma_{\rm eff}^2\le\frac{(\lambda g_{\max})^2}{4}\frac{1+r_{\max}}{1-r_{\max}}.}
\]

The bound is sharp in the extremal sense, attained by a symmetric two-state chain with endpoint structural rewards. It is not a generic prediction of realized variance in a multi-state community.

To make that distinction explicit, let

\[
f(r)=\frac{1+r}{1-r},
\qquad
B=\frac{(\lambda g_{\max})^2}{4}f(r_{\max}),
\]

and, for nonzero stationary reward variance, define `tilde w_j=w_j/Var_pi(s)`. Then

\[
\boxed{
\frac{\sigma_{\rm eff}^2}{B}
=
\frac{4\operatorname{Var}_\pi(s)}{(\lambda g_{\max})^2}
\frac{\sum_j\widetilde w_j f(r_j)}{f(r_{\max})}
\le1.
}
\]

The first factor measures range/variance saturation and the second reward alignment with the slowest mode. Equality requires both. This explains why the extremal ceiling can be loose even when it is mathematically sharp.

For nonzero stationary mean-selection magnitude `|mu|`,

\[
H_{\times}^{\rm asy}\le\frac{(\lambda g_{\max})^2}{4\mu^2}\frac{1+r_{\max}}{1-r_{\max}},
\]

an asymptotic crossover proxy rather than a finite-time hitting-time bound.

### 3.3 Diagnostic result: model-compatible oscillation forces feedback existence

For every candidate `phi<1`,

\[
G(\phi)=\frac{\phi^2-T\phi+D}{1-\phi}.
\]

If the local eigenvalues are real and satisfy `0<=r_1,r_2<1`, taking `phi=r_1`, `alpha=r_2` gives `G=0`. Stable monotone return therefore remains compatible with zero feedback.

The generalized model permits the neutral boundary `alpha=1` while requiring `phi<1`. Thus a real mode exactly at one can still participate in a model-feasible zero-feedback decomposition if the other eigenvalue can serve as `phi`, but that boundary case is not asymptotically stable monotone return.

If the eigenvalues are a non-real conjugate pair **and `0<=T<2`**, the characteristic polynomial is strictly positive for every real `phi`, while the persistence domain contains at least one feasible split. Every model-feasible decomposition therefore satisfies

\[
\boxed{G(\phi)>0.}
\]

Model-compatible oscillatory local dynamics force feedback existence within the generalized model, although feedback magnitude remains unidentified. If `T<0` or `T>=2`, the observed transient lies outside the declared persistence domain; the conclusion is model incompatibility rather than feedback existence.

### 3.4 Mechanistic proposition: stasis has two dynamically distinct origins

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

This distinction is retained because the two mechanisms have different biological interpretations, not because identity maps and contractions constitute a new dynamical-systems theorem.

## 4. Discussion

### 4.1 Required dynamics imply required information complexity

The reverse map gives the static combinatorics a direct ecological role. A required feedback phase implies a required gain, that gain implies a structural gap, and the gap imposes lower bounds on finite sensing structure. Higher cue arity can reduce query/frontier burden without reducing the minimum number of represented alternatives, exposing a Pareto tradeoff between ecological-state complexity and information-channel complexity. This is the paper's main reachability claim.

### 4.2 The structural-temporal theorem is an envelope, not a realized-variance predictor

Phenomenological models can vary selection amplitude and temporal autocorrelation independently. Here both are tied to recurrent ecological states: finite sensing structure constrains state-specific reward, while transitions among those states determine recurrence. The resulting ceiling is extremally sharp, but realized fluctuation can sit far below it when reward variance does not saturate the available range or when reward does not project strongly onto the slowest community mode. Community persistence is therefore not itself an evolutionary timescale.

### 4.3 Oscillation has a diagnostic status

Within the generalized local model, stable monotone return can remain compatible with zero feedback, whereas a model-compatible complex local mode cannot. The trace condition `0<=T<2` must be checked before making that mechanistic inference; outside it, no allowed persistence split exists and the observation instead rejects the declared local model. Conditional on compatibility, oscillation excludes the zero-feedback decomposition but does not identify feedback magnitude, separate evolutionary from ecological persistence, or prove that finite sensing structure caused the feedback. The result is a diagnostic boundary on mechanistic interpretation rather than the principal theorem.

### 4.4 Stasis is not one mechanism

Little long-term net change can arise from neutral temporal cancellation or active restoration. Under cancellation, perturbations survive; under restoring stasis, perturbations decay. The algebraic distinction is elementary, but retaining it prevents the main reachability argument from conflating two biologically different routes to small net long-term change.

### 4.5 Natural history specifies feasible information structure

Finite sensing tasks should be grounded in natural history: the application defines relevant alternatives, available cues, and required distinctions before the evolutionary model is evaluated. This does not require a separate observation-design theory. Natural history specifies feasible information structure and ecological feedback, not a measurement protocol.

### 4.6 Relation to existing theory

Information use, limited attention, evolved sensing architecture, sampling costs, memory, cue reliability, separating systems, optimal and multiway decision trees, adaptivity gaps, fluctuating selection, temporal autocorrelation, and generic eco-evolutionary feedback are prior art. The closest conceptual precursors located in the final targeted search explicitly evolve or analyze information-processing and sensing architectures (Trimmer & Houston 2014; Eliassen et al. 2016), but the search did not locate the exact reverse lower-bound map developed here. No novelty claim is made for the bounded-arity tree extremal formulas used internally, for the reversible-chain variance formula, or for identity-map versus contraction algebra. The contribution is their ecological composition, with the strongest claim being the exact reverse map from a required dynamical regime to a required finite information structure.

## 5. Scope and limitations

The sensing theory is finite, deterministic, and guaranteed-resolution, with unit acquisition costs in the sharp information-complexity results. Structural gaps are connected to selection or feedback through declared lifts rather than physiological derivation. The structural-temporal ceiling assumes a finite ergodic reversible community chain and is sharp only in the extremal sense; no claim is made that it predicts realized variance in a generic multi-state system. The local feedback results concern deterministic linearization around an equilibrium and are not a global bifurcation theory. Feedback-existence inference additionally requires that the observed trace be compatible with the declared persistence domain, `0<=T<2`. The framework does not include mutation, migration, drift, demographic stochasticity, multivariate quantitative genetics, noisy cue likelihoods, or continuous compatible sets.

The pair `(T,D)` does not uniquely identify `(alpha,phi,G)`, so an observed local timescale cannot generally be decomposed uniquely into evolutionary persistence, community persistence, and feedback. We retain this only as a limit on interpreting evolutionary time; no observation-design program is developed here.

## 6. Conclusion

Finite information structure constrains which evolutionary dynamics are available to an ecological system. Most directly, a required local feedback regime implies a required structural gap and therefore a minimum or Pareto-minimal information structure. Around that principal reachability result, community recurrence supplies an extremal envelope on long-run fluctuation and model-compatible local oscillation supplies a diagnostic for feedback existence. Within the declared model class, evolutionary time is therefore constrained upstream by finite individual information structure without requiring every supporting algebraic component to be novel.

## References cited in the current draft

- Bell, G. 2010. Fluctuating selection: the perpetual renewal of adaptation in variable environments. *Philosophical Transactions of the Royal Society B: Biological Sciences* 365(1537):87–97. https://doi.org/10.1098/rstb.2009.0150.
- Chakaravarthy, V. T., Pandit, V., Roy, S. & Sabharwal, Y. 2009. Approximating decision trees with multiway branches. In *Automata, Languages and Programming (ICALP 2009)*. https://doi.org/10.1007/978-3-642-02927-1_19.
- Cotto, O. & Chevin, L.-M. 2020. Fluctuations in lifetime selection in an autocorrelated environment. *Theoretical Population Biology* 134:119–128. https://doi.org/10.1016/j.tpb.2020.03.002.
- Crowston, R., Gutin, G., Jones, M., Muciaccia, G. & Yeo, A. 2016. Parameterizations of Test Cover with bounded test sizes. *Algorithmica* 74(1):367–384. https://doi.org/10.1007/s00453-014-9948-7.
- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. 2005. Information and its use by animals in evolutionary ecology. *Trends in Ecology & Evolution* 20(4):187–193. https://doi.org/10.1016/j.tree.2005.01.010.
- Dukas, R. 2004. Causes and consequences of limited attention. *Brain, Behavior and Evolution* 63(4):197–210. https://doi.org/10.1159/000076781.
- Eliassen, S., Andersen, B. S., Jørgensen, C. & Giske, J. 2016. From sensing to emergent adaptations: Modelling the proximate architecture for decision-making. *Ecological Modelling* 326:90–100. https://doi.org/10.1016/j.ecolmodel.2015.09.001.
- Estes, S. & Arnold, S. J. 2007. Resolving the paradox of stasis: models with stabilizing selection explain evolutionary divergence on all timescales. *The American Naturalist* 169(2):227–244. https://doi.org/10.1086/510633.
- Hairston, N. G. Jr., Ellner, S. P., Geber, M. A., Yoshida, T. & Fox, J. A. 2005. Rapid evolution and the convergence of ecological and evolutionary time. *Ecology Letters* 8(10):1114–1127. https://doi.org/10.1111/j.1461-0248.2005.00812.x.
- Hyafil, L. & Rivest, R. L. 1976. Constructing optimal binary decision trees is NP-complete. *Information Processing Letters* 5(1):15–17. https://doi.org/10.1016/0020-0190(76)90095-8.
- Katona, G. O. H. 1966. On separating systems of a finite set. *Journal of Combinatorial Theory* 1(2):174–194. https://doi.org/10.1016/S0021-9800(66)80024-8.
- Messer, P. W., Ellner, S. P. & Hairston, N. G. Jr. 2016. Can population genetics adapt to rapid evolution? *Trends in Genetics* 32(7):408–418. https://doi.org/10.1016/j.tig.2016.04.005.
- Post, D. M. & Palkovacs, E. P. 2009. Eco-evolutionary feedbacks in community and ecosystem ecology: interactions between the ecological theatre and the evolutionary play. *Philosophical Transactions of the Royal Society B: Biological Sciences* 364(1523):1629–1640. https://doi.org/10.1098/rstb.2009.0012.
- Schmidt, K. A., Dall, S. R. X. & Van Gils, J. A. 2010. The ecology of information: an overview on the ecological significance of making informed decisions. *Oikos* 119(2):304–316. https://doi.org/10.1111/j.1600-0706.2009.17573.x.
- Schoener, T. W. 2011. The newest synthesis: understanding the interplay of evolutionary and ecological dynamics. *Science* 331(6016):426–429. https://doi.org/10.1126/science.1193954.
- Trimmer, P. C. & Houston, A. I. 2014. An evolutionary perspective on information processing. *Topics in Cognitive Science* 6(2):312–330. https://doi.org/10.1111/tops.12085.
- Uyeda, J. C., Hansen, T. F., Arnold, S. J. & Pienaar, J. 2011. The million-year wait for macroevolutionary bursts. *Proceedings of the National Academy of Sciences of the USA* 108(38):15908–15913. https://doi.org/10.1073/pnas.1014503108.
- Wright, J., Haaland, T. R., Dingemanse, N. J. & Westneat, D. F. 2022. A reaction norm framework for the evolution of learning: how cumulative experience shapes phenotypic plasticity. *Biological Reviews* 97(5):1999–2021. https://doi.org/10.1111/brv.12879.

## Supplement map

Proofs and implementation details remain outside the main narrative, including continuation quotients, residual fixed-side kernels, certificate ladders, exhaustive small-world enumeration, bounded-arity recurrence proofs, private-pair constructions, critical-slowing asymptotics, exact transient-period ceilings, AR(2) inversion algebra, and solver-cap details.
