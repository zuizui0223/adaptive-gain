# Finite sensing architecture excludes eco-evolutionary feedback regimes

## Teaser text

When organisms must distinguish among ecological alternatives before acting, the structure of the sensing problem can limit more than decision cost. We show that finite sensing architecture can make entire local eco-evolutionary feedback regimes unreachable. A requested dynamical regime imposes a minimum adaptive-versus-fixed structural gap and therefore exact or Pareto-minimal requirements on represented alternatives, cue resources and irreducible separation obligations. This prohibition survives a broad nonlinear class of sensing-to-selection maps, while ecological recurrence determines which structurally generated selection contrasts persist through time.

## Abstract

Organisms often resolve state-dependent ecological decisions by acquiring cues conditionally on earlier observations. We ask whether the finite architecture of that sensing problem constrains which eco-evolutionary feedback regimes are dynamically reachable. For a declared set of ecological alternatives and cues, let `C_A` be the minimum worst-case adaptive acquisition cost and `C_F` the minimum fixed resolving-bundle cost. Their integer gap `Delta g=C_F-C_A` measures the structural burden avoided by outcome-contingent sensing. We show that a requested local feedback regime imposes a lower bound on `Delta g` and therefore an exact binary minimum, or under bounded cue arity a Pareto-minimal requirement, on represented alternatives, cue resources and irreducible separation obligations. The result is not specific to a linear sensing-to-selection map: for any nondecreasing lift with bounded marginal selection effect, insufficient structural complexity makes the requested oscillatory regime impossible. Ecological recurrence then determines how structurally generated selection projects onto slow community modes and therefore how strongly it persists through time. Thus finite sensing architecture does more than alter decision cost: within the declared model class, it excludes entire classes of eco-evolutionary dynamics.

**Keywords:** adaptive information use; decision architecture; eco-evolutionary feedback; finite sensing; evolutionary dynamics; environmental information; decision trees

## Introduction

Organisms rarely respond to ecological conditions with unlimited information. They sample cues, integrate observations and decide whether further information is worth acquiring. These processes are already central to evolutionary ecology: cue reliability, sampling costs, limited attention, memory and proximate decision architectures can all shape behavior and fitness (Dukas 2004; Dall et al. 2005; Schmidt et al. 2010; Trimmer & Houston 2014; Eliassen et al. 2016). Environmental information also has a formal fitness value, and information-theoretic models can ask how much mutual information is required to attain a target growth rate or average selection coefficient (Donaldson-Matasci et al. 2010; Rivoire & Leibler 2011; Moffett & Eckford 2022). We do not propose a new general principle that more information is always better, or a new lower bound on Shannon information.

Here we ask a different question. Suppose an organism must distinguish among a finite set of ecological alternatives before taking a state-contingent action. It has a declared repertoire of cues. Some cues are only useful after earlier observations have narrowed the relevant alternatives. An adaptive strategy may therefore acquire different later cues on different branches, whereas a fixed strategy must carry enough cue resources to guarantee resolution before any outcomes are known. This creates a finite **decision architecture** whose complexity is not captured by mutual information alone.

The static distinction between adaptive decision trees and fixed separating systems is classical (Katona 1966; Hyafil & Rivest 1976; Chakaravarthy et al. 2009). Our contribution is to connect that finite structure to eco-evolutionary dynamics in the reverse direction. Rather than choosing a sensing architecture and simulating its consequences, we ask: **what sensing architecture is minimally required before a specified feedback regime is even reachable?**

This reversal matters because local feedback regimes require a minimum loop gain. If sensing structure can generate only a bounded selection contrast, then some architectures are too simple to cross that dynamical threshold. The resulting statement is a no-go theorem: below a calculable structural bound, a requested eco-evolutionary regime cannot occur within the declared model class. We first derive the bound for a broad nonlinear class of sensing-to-selection maps, then use exact finite combinatorics to translate the required structural gap into minimum or Pareto-minimal natural-history architecture. A supporting result shows how ecological recurrence filters the structurally generated selection contrast through time.

## Methods

### Finite sensing architecture

Consider a recurrent ecological context in which an organism must resolve a declared target distinction among `n` represented alternatives. A **cue** is a deterministic partition of those alternatives by its possible outcomes. The maximum number of outcomes of any cue is its arity `b`. Not every pair of alternatives must be distinguished; the biological target specifies which distinctions are required before the state-contingent action is guaranteed.

Let `C_A` denote the minimum worst-case cue-acquisition cost of an adaptive decision tree. Later cues may depend on earlier outcomes. Let `C_F` denote the minimum cost of a fixed cue set that guarantees the same target resolution before any outcomes are known. Under unit costs,

\[
\Delta g=C_F-C_A\ge 0
\]

is an integer structural gap. It measures avoidable fixed information burden, not fitness itself. For the fixed problem we also retain the inclusion-minimal productive obligations, `H_min`, and write

\[
E=|H_{\min}|.
\]

The main paper uses only the consequence that `E`, cue count `m`, represented-world count `n` and arity `b` bound how large `Delta g` can be. The construction of continuation quotients, residual fixed-side kernels and proof certificates is relegated to Supplement.

### From sensing structure to selection

The simplest biological bridge follows from additive cue-acquisition cost. Suppose correct resolution of the target has the same terminal action payoff under two sensing architectures and each guaranteed cue acquisition incurs cost `c>0` on the declared selection scale. Then adaptive sensing avoids worst-case acquisition burden

\[
\Delta s=c\Delta g.
\]

This yields the linear special case `s(g)=cg-kappa`, where `kappa` is a state-independent maintenance cost.

The principal theorem does not require exact linearity. Let instead

\[
s(g)=f(g)-\kappa
\]

with `f` nondecreasing and with marginal effect bounded above on the relevant domain:

\[
0\le f(g_2)-f(g_1)\le L(g_2-g_1),\qquad g_2\ge g_1,
\]

for finite `L>0`. This class includes linear, saturating, diminishing-return and piecewise-linear mappings without requiring differentiability.

### Local eco-evolutionary feedback

Let `alpha` denote intrinsic persistence of a local evolutionary coordinate and `phi` persistence of a local ecological coordinate. Let `G` be the net restoring feedback gain. A convenient mechanistic factorization is

\[
G=-\beta\,\Delta s\,e,
\]

where `beta` is evolutionary responsiveness, `Delta s` is the selection contrast generated between ecological states and `e<0` is the effect of the evolutionary coordinate on the ecological target. Define

\[
B=-\beta e>0.
\]

For the nonlinear sensing-to-selection class,

\[
0\le G\le BL\Delta g.
\]

The local response has trace and determinant

\[
T=\alpha+\phi,
\qquad
D=\alpha\phi+(1-\phi)G,
\]

with `0<=alpha<=1` and `0<=phi<1`. The transition from real to complex eigenvalues occurs at

\[
G_{\mathrm{osc}}=\frac{(\alpha-\phi)^2}{4(1-\phi)}.
\]

A stable oscillatory response requires `G>G_osc` while remaining below the upper stability boundary

\[
G_+=\frac{1-\alpha\phi}{1-\phi}.
\]

### Finite structural bounds

For a required integer structural gap `q>=1`, define

\[
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\}.
\]

For binary unit-cost sensing the exact first componentwise corner is

\[
(n^*,m^*,E^*)=(h_2^*+q+1,\;h_2^*+q,\;h_2^*+q).
\]

For maximum cue arity `b>=2`, define

\[
h_b^*(q)=\min\left\{h\ge1:\frac{b^h-1}{b-1}-h\ge q\right\}.
\]

Then

\[
m_{\min}=E_{\min}=q+h_b^*(q),
\qquad
n_{\min}=q+h_2^*(q)+1.
\]

For `b>2` these minima need not be attained by the same task, so the exact object is generally a Pareto frontier over `(n,m,E)`. Proofs and constructive witnesses are given in the Supplement and executable repository tests.

### Ecological recurrence

To separate structural amplitude from temporal recurrence, let ecological states evolve as a finite ergodic Markov chain with stationary distribution `pi`. State `i` carries structurally generated selection `s_i`. For centered reward vector `c=s-bar{s}1`, cumulative centered selection has lag covariance determined by the ecological transition operator. For a reversible chain, the asymptotic variance rate is

\[
\sigma_{\mathrm{eff}}^2=\sum_r w_r\frac{1+r_r}{1-r_r},
\]

where `r_r` is a nontrivial ecological eigenvalue and `w_r` is the squared projection of the centered structural reward onto that mode. Slow ecological modes therefore matter only when the sensing-generated selection contrast projects onto them.

## Results

### Insufficient sensing architecture rules out oscillatory feedback

Because the nonlinear lift satisfies

\[
G\le BL\Delta g,
\]

a necessary condition for entering the complex-eigenvalue region is

\[
\Delta g>\frac{G_{\mathrm{osc}}}{BL}.
\]

Hence the minimum necessary integer gap is

\[
q_{\mathrm{osc}}^{\mathrm{nec}}
=
\left\lfloor\frac{G_{\mathrm{osc}}}{BL}\right\rfloor+1,
\]

with exact threshold equality excluded because oscillation requires the strict inequality `G>G_osc`.

This immediately gives a structural no-go criterion. If a declared architecture class has maximum possible gap `q_max` and

\[
BLq_{\max}\le G_{\mathrm{osc}},
\]

then **no sensing-to-selection map in the declared nondecreasing `L`-bounded class can generate the requested oscillatory regime**. Crossing the bound is only necessary: an admissible nonlinear map may realize less than its allowed marginal ceiling.

The result is therefore stronger than the original linear construction in one direction and deliberately weaker in the other. Exact linearity is unnecessary for excluding undersized architectures, but constructive reachability still requires specifying a lift that actually realizes enough selection contrast.

### Exact finite architecture follows from the required gap

The no-go theorem converts a dynamical requirement into an integer structural requirement; finite decision theory then converts that gap into natural-history architecture.

For binary sensing, a required gap `q` has the exact first corner

\[
(n^*,m^*,E^*)=(h_2^*+q+1,\;h_2^*+q,\;h_2^*+q).
\]

Adaptive depth grows only logarithmically in `q`, whereas fixed cue and productive-obligation requirements grow essentially linearly. Thus increasingly demanding feedback regimes require disproportionately larger fixed information architecture even when contingent sensing remains shallow.

For richer cues the answer is generally not one minimum. At `q=3` and arity `b=4`, for example, `(8,5,5)` and `(7,6,6)` are both nondominated. A richer cue outcome space can trade fewer declared cues and irreducible obligations against more represented ecological alternatives, but it does not remove the architecture requirement.

A canonical binary example makes the exclusion concrete. With `alpha=1`, `phi=1/2`, `B=1/2` and `L=1/4`, the oscillation threshold is `G_osc=1/8` and `BL=1/8`, so `q>=2` is necessary. Existing sharp binary bounds show that every task with at most five represented worlds has `Delta g<=1`; likewise every binary task with at most four declared cues, or with at most four minimal productive obligations, has `Delta g<=1`. All three architecture classes are therefore ruled out for every admissible monotone `L`-bounded lift. A six-world, five-cue linear special case attains `Delta g=2`, showing that the finite structural threshold itself is sharp when the marginal ceiling is realized.

### Ecological recurrence filters structural selection through time

Architecture limits the state-dependent reward contrast, but it does not determine the temporal fate of that reward. For recurrent ecological states, the reversible-chain decomposition

\[
\sigma_{\mathrm{eff}}^2=\sum_r w_r\frac{1+r_r}{1-r_r}
\]

shows that slow ecological modes amplify long-run evolutionary fluctuation only when structural reward variation aligns with those modes.

If `0<=g_i<=g_max` and the linear acquisition-cost special case has slope `lambda`, then

\[
\sigma_{\mathrm{eff}}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}},
\]

where `r_max<1` is the largest nontrivial algebraic eigenvalue. The bound is sharp in the extremal sense but not generically tight. Its slack separates into two factors: use of the available reward range and alignment of that reward variation with the slow ecological mode. Consequently, slowly changing ecological states need not produce long evolutionary memory when the sensing-generated reward is orthogonal to the slow mode.

### Oscillatory return diagnoses feedback but not its magnitude

The same local model yields a useful interpretive boundary. Stable monotone return can admit a decomposition with `G=0`. By contrast, if the local eigenvalues are a non-real conjugate pair and `0<=T<2`, the characteristic polynomial is positive for every admissible real ecological persistence value, so every model-compatible decomposition has `G>0`.

Thus compatible oscillatory return can exclude zero feedback, but it does not identify the magnitude of feedback, the separate persistence parameters or the causal contribution of sensing architecture. We use this only as a diagnostic consequence of the model, not as independent evidence that natural oscillations reveal sensing complexity.

## Discussion

The main result turns finite decision architecture into a constraint on evolutionary possibility. A sensing system is not merely more or less efficient: when its maximum adaptive advantage is too small, it cannot generate enough selection contrast to support a specified local feedback regime. In that sense, natural-history architecture can exclude dynamics.

The no-go orientation differs from the usual forward use of information in evolutionary models. Information-fitness theory asks how information changes growth or selection, and rate-distortion approaches can derive minimal mutual information for a target fitness outcome (Donaldson-Matasci et al. 2010; Rivoire & Leibler 2011; Moffett & Eckford 2022). Our object is instead the finite deterministic architecture of a guaranteed decision problem: how many ecological alternatives must be represented, how many cue resources must be available and how many irreducible distinctions a fixed strategy must cover. These structural quantities need not be recoverable from a scalar information rate.

The nonlinear extension is important biologically because exact proportionality between structural gap and selection would be a fragile basis for a general claim. The no-go theorem needs only an upper bound on the marginal selection effect of additional structural advantage. Saturation, diminishing returns and piecewise-linear effects therefore preserve the impossibility result. The price of this robustness is one-sidedness: crossing the architecture threshold does not guarantee that a particular nonlinear biological system will realize enough feedback. The linear acquisition-cost model remains useful because it is both interpretable and constructive.

The theory also separates **what organisms can distinguish** from **how ecological states recur**. Sensing architecture bounds the amplitude of state-dependent selection; ecological recurrence determines how that contrast is filtered through time. This distinction prevents a common collapse of ecological persistence into evolutionary timescale. A slowly changing environment matters evolutionarily only if the structural reward generated by the organism's decision problem loads onto that slow mode.

Several limitations define the present claim. Cue outcomes are deterministic and the sharp finite bounds use guaranteed resolution and unit acquisition costs. The feedback result is local and deterministic, not a global bifurcation theorem. The nonlinear class requires an upper marginal bound `L`; no empirical value of `L`, `B`, `alpha` or `phi` is claimed here. Mutation, migration, drift, demographic stochasticity, noisy observation channels and multivariate genetics are outside scope. These limitations are deliberate because the aim is a structural theorem, not a universal model of sensing.

The natural-history interpretation is similarly disciplined. The theory does not decide which alternatives or cues matter for a species. Those are biological inputs. But once a decision problem is declared, the mathematics gives a sharp question that can be carried to empirical systems: is the feasible sensing architecture rich enough even in principle to support the feedback regime being proposed? Negative answers are informative because they do not require estimating every mechanistic parameter downstream.

Finite sensing architecture therefore provides a constraint on eco-evolutionary reachability. Below a calculable complexity boundary, entire feedback regimes are unavailable; above it, ecological recurrence decides how the resulting structural selection is expressed through time. This connects decision architecture, natural history and evolutionary dynamics without treating finite combinatorial structure as a substitute for Shannon information.

## Data and code availability

No empirical datasets were generated or analysed for this theoretical study. Source code implementing the finite sensing bounds, nonlinear no-go theorem, ecological recurrence results and executable validation tests is publicly available in the `zuizui0223/adaptive-gain` repository. A permanent archival DOI should be added at submission if one has been minted by then.

## Author contributions

**AUTHOR INPUT REQUIRED.** Final author list and CRediT roles must be approved before submission and must not be inferred from repository activity.

## Funding

**AUTHOR INPUT REQUIRED.** Funding or no-specific-funding status must be verified by the final author(s).

## Conflict of interest statement

**AUTHOR INPUT REQUIRED.** The final declaration must be approved by the author(s).

## Acknowledgements

Add only if applicable after final author review.

## References

- Chakaravarthy, V. T., Pandit, V., Roy, S. & Sabharwal, Y. 2009. Approximating decision trees with multiway branches. In *Automata, Languages and Programming*, Part I, Lecture Notes in Computer Science 5555:210–221. https://doi.org/10.1007/978-3-642-02927-1_19.
- Dall, S. R. X., Giraldeau, L.-A., Olsson, O., McNamara, J. M. & Stephens, D. W. 2005. Information and its use by animals in evolutionary ecology. *Trends in Ecology & Evolution* 20:187–193. https://doi.org/10.1016/j.tree.2005.01.010.
- Donaldson-Matasci, M. C., Bergstrom, C. T. & Lachmann, M. 2010. The fitness value of information. *Oikos* 119:219–230. https://doi.org/10.1111/j.1600-0706.2009.17781.x.
- Dukas, R. 2004. Causes and consequences of limited attention. *Brain, Behavior and Evolution* 63:197–210. https://doi.org/10.1159/000076781.
- Eliassen, S., Andersen, B. S., Jørgensen, C. & Giske, J. 2016. From sensing to emergent adaptations: Modelling the proximate architecture for decision-making. *Ecological Modelling* 326:90–100. https://doi.org/10.1016/j.ecolmodel.2015.09.001.
- Hyafil, L. & Rivest, R. L. 1976. Constructing optimal binary decision trees is NP-complete. *Information Processing Letters* 5:15–17. https://doi.org/10.1016/0020-0190(76)90095-8.
- Katona, G. O. H. 1966. On separating systems of a finite set. *Journal of Combinatorial Theory* 1:174–194. https://doi.org/10.1016/S0021-9800(66)80024-8.
- Moffett, A. S. & Eckford, A. W. 2022. Minimal informational requirements for fitness. *Physical Review E* 105:014403. https://doi.org/10.1103/PhysRevE.105.014403.
- Rivoire, O. & Leibler, S. 2011. The value of information for populations in varying environments. *Journal of Statistical Physics* 142:1124–1166. https://doi.org/10.1007/s10955-011-0166-2.
- Schmidt, K. A., Dall, S. R. X. & Van Gils, J. A. 2010. The ecology of information: an overview on the ecological significance of making informed decisions. *Oikos* 119:304–316. https://doi.org/10.1111/j.1600-0706.2009.17573.x.
- Trimmer, P. C. & Houston, A. I. 2014. An evolutionary perspective on information processing. *Topics in Cognitive Science* 6:312–330. https://doi.org/10.1111/tops.12085.
