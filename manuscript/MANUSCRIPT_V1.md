# Finite sensing structure constrains eco-evolutionary feedback regimes

## Abstract

Rapid evolutionary change can coexist with little long-term divergence, but that observation does not tell us which dynamics are feasible when adaptation depends on limited sensing. We represent each recurrent ecological state as a finite deterministic sensing task. An organism may either choose later cues conditionally on earlier observations or commit to a fixed cue set; the extra cue burden of the fixed strategy defines a structural gap that is linked, under an explicit ecological lift, to state-dependent selection and feedback. The principal result runs backward from dynamics to natural-history structure: a required local feedback regime implies a required structural gap and therefore a minimum, or under bounded cue arity a Pareto-minimal, finite sensing architecture. Two supporting results show that finite structural reward range and ecological persistence impose a sharp extremal ceiling on long-run evolutionary fluctuation, and that a model-compatible complex local mode forces nonzero feedback within the generalized model while leaving its magnitude unidentified. A mechanistic proposition distinguishes neutral temporal cancellation from attractive restoration. These bounds concern worst-case finite decision structure rather than Shannon information, complementing information-theoretic results on the fitness value and minimum required amount of environmental information.

## Keywords

Adaptive information use; decision trees; evolutionary stasis; fluctuating selection; temporal autocorrelation

## 1. Introduction

Rapid evolutionary change can occur on ecological timescales, yet strong short-term activity need not accumulate into comparably large long-term divergence. Ecological and evolutionary dynamics can overlap in time, selection can fluctuate strongly, and stabilizing or temporally reversing selection can reconcile rapid local change with long periods of apparent stasis (Hairston et al. 2005; Estes & Arnold 2007; Bell 2010; Uyeda et al. 2011; Messer et al. 2016; Cotto & Chevin 2020). The unresolved question here is not why short-term evolution can cancel, but what constrains the dynamical regimes that are available upstream.

Information use provides one such constraint. Organisms acquire and combine cues under limits of sampling, attention, memory, and reliability, and evolutionary ecology already treats information-processing and sensing architectures as adaptive, evolvable mechanisms (Dall et al. 2005; Dukas 2004; Schmidt et al. 2010; Trimmer & Houston 2014; Eliassen et al. 2016; Wright et al. 2022). Information-theoretic work goes further: environmental information has an established fitness value, and rate-distortion theory can ask how much mutual information is minimally required for a target growth rate or average selection coefficient (Donaldson-Matasci et al. 2010; Rivoire & Leibler 2011; Moffett & Eckford 2022). Evolutionary information thresholds also have established meanings in coding and replication theory (de Boer & Hogeweg 2010). We therefore do not propose a new minimum-information principle in general.

Instead, we ask about a different object: the finite decision architecture by which ecological alternatives are distinguished. Separating systems and optimal binary or multiway decision trees characterize fixed and sequential finite-state identification (Katona 1966; Hyafil & Rivest 1976; Chakaravarthy et al. 2009). Here that machinery describes represented ecological alternatives, available cues, adaptive depth, irreducible fixed-side obligations, and cue outcome arity. These are worst-case structural quantities, not Shannon bits or channel rates.

For recurrent ecological state `i`, let `C_A(i)` be the least guaranteed cost when later cues can depend on earlier outcomes and `C_F(i)` the least cost of a fixed cue set that guarantees the same distinctions. Their difference

\[
g_i=C_F(i)-C_A(i)
\]

measures the avoidable fixed-information burden made available by contingent sensing. Under an explicit ecological lift, `g_i` generates state-dependent selection or feedback. The same recurrent state space determines how those rewards reappear through time. This creates the central reachability question: what finite sensing structure is required before a specified eco-evolutionary regime becomes possible?

The paper is organized around one principal reachability theorem. A required local dynamical regime imposes a required structural gap and therefore a minimum or Pareto-minimal finite sensing architecture. A supporting extremal theorem bounds long-run fluctuation, a diagnostic theorem determines when a model-compatible local oscillation rules out zero feedback, and a mechanistic proposition distinguishes neutral cancellation from attractive restoration.

## 2. Model

### 2.1 Recurrent ecological states and finite sensing tasks

We consider recurrent ecological or community states `i=1,...,K`. Each state defines a finite sensing task: **represented alternatives** (worlds), **declared cues** (queries), an outcome-arity cap `b`, and the **required distinctions** needed to guarantee the declared state-contingent action. The application specifies these alternatives and cues; the theory then asks what can be guaranteed from them. Cue outcomes are deterministic and resolution is guaranteed in the present model; noisy likelihoods and probabilistic stopping lie outside scope.

A simple natural-history interpretation is sequential habitat or resource assessment. An organism may first use a coarse cue to decide which fine-scale cue is worth sampling next. A fixed strategy must carry every cue needed across all possible branches, whereas a contingent strategy samples only the branch made relevant by the first observation. The theory abstracts this difference without prescribing how the cues must be measured empirically.

### 2.2 Adaptive and fixed cue requirements

Let `C_A(i)` be the minimum worst-case number of unit-cost cue acquisitions required adaptively in state `i`, and `C_F(i)` the minimum fixed cue set required for the same resolution. Define

\[
\boxed{g_i=C_F(i)-C_A(i).}
\]

For the fixed problem, let `H_min` denote the retained family of irreducible distinctions that any successful fixed strategy must cover, and let

\[
E_i=|H_{\min}(i)|.
\]

We call this obligation family the `productive frontier`; only its size `E_i` enters the main ecological argument.

### 2.3 Structural lift to selection

We declare

\[
\boxed{s_i=\lambda g_i-\kappa,}
\]

where `lambda>0` converts structural gap into a state-dependent selection contribution and `kappa` is state-independent maintenance cost. This is a modelling assumption: the structural gap is not intrinsically fitness. If `pi` is the stationary distribution and `bar s=sum_i pi_i s_i`, then

\[
s_i-\bar s=\lambda(g_i-\bar g).
\]

### 2.4 Ecological recurrence

Let ecological states evolve as a finite ergodic Markov chain with transition matrix `P` and stationary distribution `pi`. Temporal autocorrelation and fluctuating selection are established evolutionary mechanisms; here the Markov representation connects recurrence of the same state-indexed structural rewards to long-run filtering (Bell 2010; Cotto & Chevin 2020). For centered reward vector `c=s-\bar s 1`, define

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

Let `alpha` denote intrinsic evolutionary persistence, `phi` ecological persistence, and `G` net feedback gain. Reciprocal eco-evolutionary feedback itself is established theory (Post & Palkovacs 2009; Schoener 2011); here we ask how much finite sensing structure is required to reach particular local regimes. The local invariants are

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

### 2.6 Finite structural bounds

For unit-cost sensing with at most `b` outcomes per cue, let `F_b(n,h)` denote the supporting rooted-tree extremal count. A task with adaptive optimum `C_A=h` obeys

\[
\boxed{C_F\le\min\{m,E,F_b(n,h)\}.}
\]

Hence gap `q=C_F-C_A` requires `min{m,E,F_b(n,h)}>=h+q`. Binary sensing yields one exact first corner; higher arity generally yields a Pareto frontier over `(n,m,E)`. Separating-system and multiway decision-tree results are prior-art anchors for this imported combinatorial setting, not equivalence claims for the exact arity restriction used here (Katona 1966; Hyafil & Rivest 1976; Chakaravarthy et al. 2009; Crowston et al. 2016).

## 3. Results

### 3.1 Principal result: required dynamics imply required sensing structure

For binary unit-cost sensing and required integer gap `q>=1`, define

\[
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\}.
\]

The exact componentwise first corner is

\[
\boxed{(n^*,m^*,E^*)=(h_2^*+q+1,\ h_2^*+q,\ h_2^*+q).}
\]

Moreover `h_2^*(q)=log_2 q+O(1)`.

For maximum cue arity `b>=2`,

\[
h_b^*(q)=\min\left\{h\ge1:\frac{b^h-1}{b-1}-h\ge q\right\},
\]

with

\[
\boxed{m_{\min}=E_{\min}=q+h_b^*(q),}
\qquad
\boxed{n_{\min}=q+h_2^*(q)+1.}
\]

These minima need not be jointly attainable; the exact bounded-arity object is generally a Pareto frontier `P_b(q)`. For `q=3,b=4`, `(8,5,5)` and `(7,6,6)` are both nondominated. Richer cue outcomes can therefore reduce cue/frontier burden without eliminating the lower bound on how many ecological alternatives must be represented.

With local feedback `G=a Delta g`,

\[
\boxed{(\alpha,\phi,a,b)\longrightarrow q_{\rm osc}\longrightarrow\mathcal P_b(q_{\rm osc}).}
\]

Under `alpha=1`, `phi=1/2`, `a=1/8`, the first stable oscillatory gap is `q_osc=2`, giving `(n,m,E)=(6,5,5)`. More generally, if the integer gap ladder jumps directly beyond the upper stability boundary, the stable-oscillation Pareto set is empty.

This reverse map is the principal result: a requested local dynamical phase imposes a lower bound on the finite deterministic sensing architecture capable of supporting it. It is not a lower bound on Shannon mutual information.

### 3.2 Supporting result: a structural-temporal fluctuation envelope

If `0<=g_i<=g_max`, the state-dependent selection range is at most `lambda*g_max`. For a reversible community chain with largest nontrivial algebraic eigenvalue `r_max<1`,

\[
\boxed{\sigma_{\rm eff}^2\le\frac{(\lambda g_{\max})^2}{4}\frac{1+r_{\max}}{1-r_{\max}}.}
\]

The bound is sharp in the extremal sense, attained by a symmetric two-state chain with endpoint structural rewards. It is not a generic prediction of realized variance in a multi-state community.

Let

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

The first factor measures how fully the available reward range is used; the second measures how strongly reward variation aligns with the slowest ecological mode. Equality requires both factors to equal one. Thus the ceiling can be mathematically sharp while remaining loose for a particular multi-state system.

For nonzero stationary mean-selection magnitude `|mu|`,

\[
H_{\times}^{\rm asy}\le\frac{(\lambda g_{\max})^2}{4\mu^2}\frac{1+r_{\max}}{1-r_{\max}},
\]

an asymptotic crossover proxy rather than a finite-time hitting-time bound.

### 3.3 Diagnostic result: model-compatible oscillation requires feedback

For every candidate `phi<1`,

\[
G(\phi)=\frac{\phi^2-T\phi+D}{1-\phi}.
\]

If the local eigenvalues are real and satisfy `0<=r_1,r_2<1`, taking `phi=r_1`, `alpha=r_2` gives `G=0`. Stable monotone return therefore remains compatible with zero feedback.

The generalized model permits the neutral boundary `alpha=1` while requiring `phi<1`. A real mode exactly at one can therefore participate in a model-feasible zero-feedback decomposition if the other eigenvalue can serve as `phi`, although that boundary is not asymptotically stable return.

If the eigenvalues are a non-real conjugate pair **and `0<=T<2`**, the characteristic polynomial is strictly positive for every real `phi`, while the persistence domain contains at least one feasible split. Every model-feasible decomposition therefore satisfies

\[
\boxed{G(\phi)>0.}
\]

Thus model-compatible oscillatory local dynamics require feedback within the generalized model, although the feedback magnitude remains unidentified. If `T<0` or `T>=2`, the transient lies outside the declared persistence domain; the conclusion is model incompatibility rather than feedback existence.

### 3.4 Mechanistic proposition: two routes to little net change

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

The distinction matters because the two mechanisms respond differently to perturbation; the underlying identity-map versus contraction algebra is standard.

## 4. Discussion

### 4.1 From dynamics back to natural-history structure

The principal theorem reverses the usual direction of ecological modelling. Instead of choosing a sensing architecture and asking what dynamics it produces, we specify a local feedback regime and ask what finite architecture is required to make that regime reachable. Required feedback implies required gain, gain implies a structural gap, and the gap imposes lower bounds on represented alternatives, available cues, and irreducible fixed-side obligations. Higher cue arity can reduce cue/frontier burden without reducing the minimum number of represented alternatives, producing a genuine structural tradeoff rather than a single scalar complexity measure.

The reverse direction itself is not unprecedented in information theory. Moffett & Eckford (2022) derive minimum mutual-information requirements for target population growth and average selection coefficients using rate-distortion theory. Our result asks a different question: given a local feedback phase, what finite deterministic sensing architecture is required to generate a sufficiently large adaptive/fixed structural gap? The answer is discrete and, for bounded arity, generally Pareto-valued over `(n,m,E)` rather than a scalar information rate.

The distinction is structural rather than terminological. Once the deterministic task is declared, `C_A`, `C_F`, and the resulting `(n,m,E)` bounds are worst-case and distribution-free: they depend on which alternatives must be distinguished and which cue outcomes are available, not on a probability distribution over alternatives. Mutual-information and rate-distortion quantities require probabilistic ingredients such as a state distribution and a channel or fitness mapping. Without those ingredients, neither representation generally determines the other. The Pareto frontier here is therefore a constraint on sensing architecture, not a re-expression of information rate.

### 4.2 Ecological persistence is not itself an evolutionary timescale

Finite sensing structure constrains the range of state-dependent rewards, while transitions among the same ecological states determine how those rewards recur. Their combination gives an extremal ceiling on long-run evolutionary fluctuation. But the realized value can be much smaller if reward variation uses only part of the available range or projects weakly onto the slowest ecological mode. Thus a slowly changing community does not necessarily impose a long evolutionary timescale: the relevant ecological mode must also carry the structural selection contrast.

### 4.3 Oscillation is a diagnostic, not a magnitude estimate

Within the generalized local model, stable monotone return can remain compatible with zero feedback, whereas a model-compatible complex local mode cannot. The trace condition `0<=T<2` must be checked first; outside it, no allowed persistence split exists and the observation rejects the declared local model. Conditional on compatibility, oscillation excludes the zero-feedback decomposition but does not identify feedback magnitude, separate evolutionary from ecological persistence, or show that finite sensing structure caused the feedback.

### 4.4 Similar stasis can hide different return dynamics

Little long-term net change can arise from neutral temporal cancellation or active restoration. Under cancellation, perturbations survive; under restoring stasis, perturbations decay. The algebra is elementary, but the biological distinction matters because the two systems can look similarly static over long windows while responding differently to disturbance.

### 4.5 Natural history defines the feasible architecture

The theory does not determine which ecological alternatives or cues are biologically meaningful. Those must come from natural history. Once they are declared, however, the finite architecture imposes exact structural constraints. This division of labour is useful: natural history defines the feasible decision problem, while the theory determines what evolutionary regimes that problem can or cannot support.

### 4.6 Relation to existing theory

The component literatures are substantial. Information use, limited attention, evolved sensing architecture, sampling costs, memory, cue reliability, separating systems, optimal and multiway decision trees, adaptivity gaps, fluctuating selection, temporal autocorrelation, and generic eco-evolutionary feedback are all prior art. Information-fitness theory additionally formalizes the fitness value of environmental information (Donaldson-Matasci et al. 2010; Rivoire & Leibler 2011), and Moffett & Eckford (2022) explicitly derive minimal mutual-information requirements for target growth and selection. de Boer & Hogeweg (2010) provides a distinct evolutionary use of `information threshold` in coding structure.

Accordingly, the contribution claimed here is narrow: finite deterministic sensing architecture is linked through the adaptive/fixed structural gap to state-indexed selection and local feedback, yielding exact componentwise minima or Pareto-minimal `(n,m,E)` structures for a required local regime. Community recurrence then supplies a supporting extremal envelope. No novelty claim is made for minimum information in general, the bounded-arity tree formulas used internally, reversible-chain variance formulas, generic feedback, or the identity-map versus contraction distinction.

## 5. Scope and limitations

The sensing theory is finite, deterministic, and guaranteed-resolution, with unit acquisition costs in the sharp structural results. Structural gaps are connected to selection or feedback through declared lifts rather than physiological derivation. The structural-temporal ceiling assumes a finite ergodic reversible community chain and is sharp only in the extremal sense; it is not claimed to predict realized variance in a generic multi-state system. The feedback results concern deterministic linearization around an equilibrium and are not a global bifurcation theory. Feedback-existence inference additionally requires `0<=T<2`.

The pair `(T,D)` does not uniquely identify `(alpha,phi,G)`, so an observed local timescale cannot generally be decomposed uniquely into evolutionary persistence, ecological persistence, and feedback. The framework also excludes mutation, migration, drift, demographic stochasticity, multivariate quantitative genetics, noisy cue likelihoods, probabilistic stopping, and continuous compatible sets.

The discrete structural bounds are not substitutes for mutual-information or rate-distortion analyses. They answer a different question under a stronger deterministic finite-task representation and should not be interpreted as lower bounds in bits when noisy channels or continuous signals are essential.

## 6. Conclusion

Finite sensing architecture can restrict which eco-evolutionary dynamics are reachable. Most directly, a required local feedback regime implies a required adaptive/fixed structural gap and therefore a minimum or Pareto-minimal architecture over represented alternatives, declared cues, and irreducible obligations. Community recurrence supplies a supporting ceiling on long-run fluctuation, while model-compatible local oscillation supplies a diagnostic for feedback existence. The resulting theory connects natural-history decision structure to evolutionary dynamics without treating finite combinatorial architecture as a substitute for Shannon information.

## References cited in the current draft

- Bell, G. 2010. Fluctuating selection: the perpetual renewal of adaptation in variable environments. *Philosophical Transactions of the Royal Society B: Biological Sciences* 365(1537):87–97. https://doi.org/10.1098/rstb.2009.0150.
- Chakaravarthy, V. T., Pandit, V., Roy, S. & Sabharwal, Y. 2009. Approximating decision trees with multiway branches. In *Automata, Languages and Programming*, Part I, Lecture Notes in Computer Science 5555:210–221. https://doi.org/10.1007/978-3-642-02927-1_19.
- Cotto, O. & Chevin, L.-M. 2020. Fluctuations in lifetime selection in an autocorrelated environment. *Theoretical Population Biology* 134:119–128. https://doi.org/10.1016/j.tpb.2020.03.002.
- Crowston, R., Gutin, G., Jones, M., Muciaccia, G. & Yeo, A. 2016. Parameterizations of Test Cover with bounded test sizes. *Algorithmica* 74(1):367–384. https://doi.org/10.1007/s00453-014-9948-7.
- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. 2005. Information and its use by animals in evolutionary ecology. *Trends in Ecology & Evolution* 20(4):187–193. https://doi.org/10.1016/j.tree.2005.01.010.
- de Boer, F. K. & Hogeweg, P. 2010. Eco-evolutionary dynamics, coding structure and the information threshold. *BMC Evolutionary Biology* 10:361. https://doi.org/10.1186/1471-2148-10-361.
- Donaldson-Matasci, M. C., Bergstrom, C. T. & Lachmann, M. 2010. The fitness value of information. *Oikos* 119(2):219–230. https://doi.org/10.1111/j.1600-0706.2009.17781.x.
- Dukas, R. 2004. Causes and consequences of limited attention. *Brain, Behavior and Evolution* 63(4):197–210. https://doi.org/10.1159/000076781.
- Eliassen, S., Andersen, B. S., Jørgensen, C. & Giske, J. 2016. From sensing to emergent adaptations: Modelling the proximate architecture for decision-making. *Ecological Modelling* 326:90–100. https://doi.org/10.1016/j.ecolmodel.2015.09.001.
- Estes, S. & Arnold, S. J. 2007. Resolving the paradox of stasis: models with stabilizing selection explain evolutionary divergence on all timescales. *The American Naturalist* 169(2):227–244. https://doi.org/10.1086/510633.
- Hairston, N. G. Jr., Ellner, S. P., Geber, M. A., Yoshida, T. & Fox, J. A. 2005. Rapid evolution and the convergence of ecological and evolutionary time. *Ecology Letters* 8(10):1114–1127. https://doi.org/10.1111/j.1461-0248.2005.00812.x.
- Hyafil, L. & Rivest, R. L. 1976. Constructing optimal binary decision trees is NP-complete. *Information Processing Letters* 5(1):15–17. https://doi.org/10.1016/0020-0190(76)90095-8.
- Katona, G. O. H. 1966. On separating systems of a finite set. *Journal of Combinatorial Theory* 1(2):174–194. https://doi.org/10.1016/S0021-9800(66)80024-8.
- Messer, P. W., Ellner, S. P. & Hairston, N. G. Jr. 2016. Can population genetics adapt to rapid evolution? *Trends in Genetics* 32(7):408–418. https://doi.org/10.1016/j.tig.2016.04.005.
- Moffett, A. S. & Eckford, A. W. 2022. Minimal informational requirements for fitness. *Physical Review E* 105(1):014403. https://doi.org/10.1103/PhysRevE.105.014403.
- Post, D. M. & Palkovacs, E. P. 2009. Eco-evolutionary feedbacks in community and ecosystem ecology: interactions between the ecological theatre and the evolutionary play. *Philosophical Transactions of the Royal Society B: Biological Sciences* 364(1523):1629–1640. https://doi.org/10.1098/rstb.2009.0012.
- Rivoire, O. & Leibler, S. 2011. The Value of Information for Populations in Varying Environments. *Journal of Statistical Physics* 142(6):1124–1166. https://doi.org/10.1007/s10955-011-0166-2.
- Schmidt, K. A., Dall, S. R. X. & Van Gils, J. A. 2010. The ecology of information: an overview on the ecological significance of making informed decisions. *Oikos* 119(2):304–316. https://doi.org/10.1111/j.1600-0706.2009.17573.x.
- Schoener, T. W. 2011. The newest synthesis: understanding the interplay of evolutionary and ecological dynamics. *Science* 331(6016):426–429. https://doi.org/10.1126/science.1193954.
- Trimmer, P. C. & Houston, A. I. 2014. An evolutionary perspective on information processing. *Topics in Cognitive Science* 6(2):312–330. https://doi.org/10.1111/tops.12085.
- Uyeda, J. C., Hansen, T. F., Arnold, S. J. & Pienaar, J. 2011. The million-year wait for macroevolutionary bursts. *Proceedings of the National Academy of Sciences of the USA* 108(38):15908–15913. https://doi.org/10.1073/pnas.1014503108.
- Wright, J., Haaland, T. R., Dingemanse, N. J. & Westneat, D. F. 2022. A reaction norm framework for the evolution of learning: how cumulative experience shapes phenotypic plasticity. *Biological Reviews* 97(5):1999–2021. https://doi.org/10.1111/brv.12879.

## Supplement map

Proofs and implementation details remain outside the main narrative, including continuation quotients, residual fixed-side kernels, certificate ladders, exhaustive small-world enumeration, bounded-arity recurrence proofs, private-pair constructions, critical-slowing asymptotics, exact transient-period ceilings, AR(2) inversion algebra, and solver-cap details.
