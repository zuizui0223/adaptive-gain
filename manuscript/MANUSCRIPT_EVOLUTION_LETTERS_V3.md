# Finite sensing architecture defines an eco-evolutionary possibility space

## Teaser text

Finite sensing architecture can constrain more than decision cost. Exact adaptive-versus-fixed resolution geometry determines when contingent sensing alone can meet an ecological deadline, how large a structural selection contrast can exist between ecological states, and which local eco-evolutionary feedback regimes are therefore unreachable. These limits persist even when every binary cue is globally balanced and under a broad nonlinear class of sensing-to-selection maps, while ecological recurrence determines which structurally generated selection contrasts persist through time.

## Abstract

Organisms often resolve state-dependent ecological decisions by acquiring cues conditionally on earlier observations. We ask how the finite architecture of such sensing constrains eco-evolutionary possibility. For a declared deterministic decision target, let `C_A` be the minimum worst-case adaptive cue-acquisition cost and `C_F` the minimum fixed resolving-bundle cost. Exact finite theory gives `C_A<=C_F` and an adaptive-only ecological budget window `C_A<=B<C_F`. Across ecological states, the nonnegative structural gap `g_i=C_F(i)-C_A(i)` generates a between-state contrast `Delta g`, from which sharp binary minima or bounded-arity Pareto requirements follow for represented alternatives, cue resources and irreducible separation obligations. This advantage is not explained by simple marginal cue statistics: there are exactly balanced binary unit-cost families in which `C_F/C_A` diverges. We then connect the finite structure to evolution in two ways. A hard ecological deadline selects contingent sensing precisely in the adaptive-only budget window, whereas for any nondecreasing sensing-to-selection lift with bounded marginal effect, insufficient `Delta g` makes a requested oscillatory feedback regime impossible. Ecological recurrence finally filters structurally generated selection through its alignment with slow ecological modes. Thus finite decision architecture defines a constrained eco-evolutionary possibility space rather than merely changing sensing efficiency.

**Keywords:** adaptive information use; decision architecture; eco-evolutionary feedback; finite sensing; evolutionary dynamics; environmental information; decision trees

## Introduction

Organisms rarely respond to ecological conditions with unlimited information. They sample cues, integrate observations and decide whether further information is worth acquiring. These processes are central to evolutionary ecology because cue reliability, sampling costs, limited attention, memory and proximate decision architectures can shape behavior and fitness (Dukas 2004; Dall et al. 2005; Schmidt et al. 2010; Trimmer & Houston 2014; Eliassen et al. 2016). Environmental information also has a formal fitness value, and information-theoretic models can ask how much mutual information is required to attain a target growth rate or average selection coefficient (Donaldson-Matasci et al. 2010; Rivoire & Leibler 2011; Moffett & Eckford 2022). We do not propose a new general minimum-information principle or a lower bound on Shannon information.

Here we ask about a different object: the finite decision architecture by which ecological alternatives are distinguished. Suppose that in each recurrent ecological state an organism faces a finite set of relevant alternatives and a declared repertoire of cues. Some later cues are useful only after earlier observations have narrowed the alternatives. An adaptive strategy may therefore acquire different cues on different branches, whereas a fixed strategy must carry enough cue resources to guarantee target resolution before any outcomes are known.

The static distinction between adaptive decision trees and fixed separating systems is classical (Katona 1966; Hyafil & Rivest 1976; Chakaravarthy et al. 2009). Our contribution is to ask what that finite structure licenses or forbids biologically. We use the mathematics in three steps. First, exact target-resolution theory identifies when contingent sensing alone can meet a hard ecological budget. Second, sharp extremal results translate a required adaptive-versus-fixed gap into minimum or Pareto-minimal finite architecture and show that global cue balance does not control worst-case adaptive advantage. Third, the state dependence of these structural quantities is lifted into selection and local eco-evolutionary feedback.

This produces a reverse question: **what sensing architecture must be available before a specified ecological performance difference or feedback regime is even possible?** The answer depends on more than one scalar measure of information. It depends on the branch geometry of represented alternatives, on which cue resources are fixed-mandatory, and on how those structures differ between ecological states.

We derive a nonlinear no-go theorem showing that below a calculable structural contrast, a requested local oscillatory feedback regime cannot occur within the declared model class. We also derive an independent threshold-selection result in which no linear cost-to-fitness conversion is required: if an ecological deadline lies between `C_A` and `C_F`, contingent sensing succeeds while every fixed resolver fails. Finally, ecological recurrence determines how the resulting state-specific selection projects onto slow community modes.

## Methods

### Finite sensing architecture within ecological states

Consider recurrent ecological states indexed by `i`. In state `i`, an organism must resolve a declared target distinction among `n_i` represented alternatives. A **cue** is a deterministic partition of those alternatives by its possible outcomes. The maximum number of outcomes of a cue is its arity `b`. Not every pair of alternatives must be distinguished; the biological target specifies which distinctions are required before the state-contingent action is guaranteed.

Let `C_A(i)` denote the minimum worst-case cue-acquisition cost of an adaptive decision tree and `C_F(i)` the minimum cost of a fixed cue set that guarantees the same target resolution. Any fixed resolving bundle is a feasible adaptive policy that simply ignores intermediate outcomes, so

\[
C_A(i)\le C_F(i).
\]

Under unit costs,

\[
g_i=C_F(i)-C_A(i)\ge0
\]

is the structural gap of state `i`. It measures avoidable fixed information burden, not fitness itself.

For the fixed problem we retain the inclusion-minimal productive obligations `H_min(i)` and write

\[
E_i=|H_{\min}(i)|.
\]

The main paper uses only the consequence that `E_i`, cue count `m_i`, represented-world count `n_i` and arity `b` bound how large `g_i` can be. Exact Bellman kernels, continuation quotients, residual kernels and proof certificates remain supplementary.

### Exact ecological budget window

Let `B` be a hard ecological budget measured on the same acquisition-cost scale as `C_A` and `C_F`. The budget can represent time, energy, exposure, handling opportunity or another physically justified ceiling in a focal system.

Guaranteed adaptive resolution is feasible when `C_A<=B`, whereas fixed resolution is feasible when `C_F<=B`. Therefore adaptive sensing alone can resolve the target exactly when

\[
\boxed{C_A\le B<C_F.}
\]

This interval is exact. Below `C_A`, neither architecture can guarantee resolution; at or above `C_F`, both can.

### Target-relevant reduction

Raw natural history can distinguish ecological alternatives or cues that are irrelevant to the declared decision target. The repository proves exact state-local reductions on both sides of the adaptive Bellman problem. Same-target worlds with identical remaining cross-target separation profiles can be quotient-collapsed, and a query `r` can be removed when another query `q` separates a superset of active cross-target pairs at no greater cost. Their recursive composition preserves the exact adaptive optimum,

\[
C_A^{\mathrm{kernel}}=C_A^{\mathrm{direct}}.
\]

We use this result only to define the decision-relevant architecture: descriptive differences that preserve the declared target-relevant continuation structure need not be counted as separate sensing complexity. Detailed kernel proofs remain supplementary.

### Structural contrast and selection

Between two ecological states with `g_2>=g_1`, define

\[
\Delta g=g_2-g_1.
\]

A simple additive cue-acquisition bridge writes

\[
s_i=cg_i-\kappa,
\]

with per-unit selection value `c>0` and state-independent maintenance cost `kappa`, giving `Delta s=c Delta g`.

The principal no-go theorem does not require exact linearity. Let instead

\[
s_i=f(g_i)-\kappa
\]

with `f` nondecreasing and bounded marginal effect on the relevant gap domain:

\[
0\le f(g_2)-f(g_1)\le L(g_2-g_1)=L\Delta g
\]

for finite `L>0`. This class includes linear, saturating, diminishing-return and piecewise-linear mappings without requiring differentiability.

### Hard-budget evolutionary selection

The exact budget interval gives a second evolutionary bridge that does not assign fitness to each saved cue. Define

\[
S_A(X,B)=\mathbf 1\{C_A(X)\le B\},
\qquad
S_F(X,B)=\mathbf 1\{C_F(X)\le B\}.
\]

Let `w_0>0` be baseline fitness, `v>=0` the benefit of resolving the target before the budget expires, and `kappa>=0` the log maintenance cost of contingent control. Define

\[
W_A=e^{-\kappa}[w_0+vS_A(X,B)],
\qquad
W_F=w_0+vS_F(X,B),
\]

and

\[
s_B(X)=\log\frac{W_A}{W_F}.
\]

This threshold model separates the biological question of completing a decision before a deadline from the continuous cost-to-selection lift above.

### Local eco-evolutionary feedback

Let `alpha` denote intrinsic persistence of a local evolutionary coordinate and `phi` persistence of a local ecological coordinate. Let `G` be net restoring feedback gain. A mechanistic factorization is

\[
G=-\beta\,\Delta s\,e,
\]

where `beta` is evolutionary responsiveness and `e<0` is the effect of the evolutionary coordinate on the ecological target. Define `B_f=-\beta e>0` to distinguish this feedback-per-selection scale from the ecological budget `B`. Then every monotone-Lipschitz lift obeys

\[
0\le G\le B_fL\Delta g.
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

Stable oscillatory return requires `G>G_osc` while remaining below

\[
G_+=\frac{1-\alpha\phi}{1-\phi}.
\]

### Translating a required contrast into finite architecture

Suppose a dynamical regime requires structural contrast `Delta g>=q` for integer `q>=1`. Since all state gaps are nonnegative, at least one state satisfies `g_i>=q`. We can therefore apply sharp single-task finite bounds to that high-gap state.

For binary unit-cost sensing define

\[
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\}.
\]

The exact first componentwise corner capable of gap `q` is

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

For `b>2` these minima need not be attained by the same task, so the exact requirement is generally a Pareto frontier over `(n,m,E)`.

### Ecological recurrence

Let ecological states evolve as a finite ergodic Markov chain with stationary distribution `pi`. State `i` carries selection contribution `s_i`. For centered reward vector `c=s-bar{s}1`, a reversible chain has asymptotic variance rate

\[
\sigma_{\mathrm{eff}}^2=\sum_r w_r\frac{1+r_r}{1-r_r},
\]

where `r_r` is a nontrivial ecological eigenvalue and `w_r` is the squared projection of centered structural reward onto that mode. Slow ecological modes therefore matter only when sensing-generated selection variation projects onto them.

## Results

### Exact adaptive-only budgets create a natural selection window

The containment `C_A<=C_F` partitions every hard budget into three exact regions. If `B<C_A`, both strategies fail to guarantee target resolution and the threshold model gives

\[
s_B=-\kappa.
\]

If

\[
C_A\le B<C_F,
\]

then contingent sensing succeeds while every fixed resolving bundle exceeds the ecological budget, so

\[
\boxed{
s_B=\log\frac{w_0+v}{w_0}-\kappa.
}
\]

Adaptive sensing is favored exactly when this resolution benefit exceeds its maintenance cost. Once `B>=C_F`, both architectures resolve the target and the selection difference returns to `-kappa` under the declared threshold payoff.

Thus the mathematical interval `[C_A,C_F)` is not only a cost gap. Under a hard ecological deadline it is the exact region in which contingent sensing can convert otherwise impossible target resolution into a fitness advantage. Ecological state changes can move `C_A` or `C_F` around a fixed physiological budget, generating state-dependent selection without any linear per-cue fitness assumption.

### Global cue balance does not control adaptive advantage

The structural value of adaptivity is not explained by simple marginal cue statistics. For routing depth `d`, the repository constructs finite deterministic tasks in which every declared query is binary, unit cost and exactly 50/50 balanced over represented worlds, yet fixed resolution requires at least `2^d` branch-specific terminal resources while an adaptive policy uses at most `d+1` queries. Hence

\[
\boxed{
\frac{C_F}{C_A}
\ge
\frac{2^d}{d+1}
\longrightarrow\infty.
}
\]

This is an existence result rather than a sharp maximum at fixed `(n,m)`. Its biological implication is nevertheless strong: a globally balanced cue can still have branch-exclusive decision value. Fixed sensing must provision every branch-specific obligation simultaneously, whereas adaptive sensing first learns which branch is relevant and acquires only its terminal resource. Consequently, global cue prevalence or marginal balance is not the structural quantity that bounds adaptive value.

### Insufficient structural contrast rules out oscillatory feedback

Because

\[
G\le B_fL\Delta g,
\]

a necessary condition for entering the complex-eigenvalue region is

\[
\Delta g>\frac{G_{\mathrm{osc}}}{B_fL}.
\]

Hence the minimum necessary integer contrast is

\[
q_{\mathrm{osc}}^{\mathrm{nec}}
=
\left\lfloor\frac{G_{\mathrm{osc}}}{B_fL}\right\rfloor+1,
\]

with equality excluded because oscillation requires the strict inequality `G>G_osc`.

This gives a no-go criterion. If admissible sensing architectures imply maximum possible contrast `Delta g_max` and

\[
B_fL\Delta g_{\max}\le G_{\mathrm{osc}},
\]

then **no sensing-to-selection map in the declared nondecreasing `L`-bounded class can generate the requested oscillatory regime**. Crossing the bound is only necessary: an admissible nonlinear map may realize less than its allowed marginal ceiling.

The result is stronger than the original linear construction in one direction and deliberately weaker in the other. Exact linearity is unnecessary for excluding undersized architectures, but constructive reachability still requires a biological lift that actually realizes enough selection contrast.

### Required structural contrast forces finite state-specific architecture

If `Delta g>=q`, nonnegativity of state gaps implies that at least one state has `g_i>=q`. The single-task extremal results therefore provide a necessary architecture for any system capable of that contrast.

For binary sensing, required contrast `q` forces at least one state to admit the exact first gap-capable corner

\[
(n^*,m^*,E^*)=(h_2^*+q+1,\;h_2^*+q,\;h_2^*+q).
\]

Adaptive depth grows only logarithmically in `q`, whereas fixed cue and productive-obligation requirements grow essentially linearly. Increasingly demanding feedback regimes therefore require disproportionately larger fixed information architecture even when contingent sensing remains shallow.

For richer cues the answer is generally Pareto-valued. At `q=3` and arity `b=4`, `(8,5,5)` and `(7,6,6)` are both nondominated. A richer cue outcome space can trade fewer declared cues and irreducible obligations against more represented alternatives without eliminating the architecture requirement.

A canonical binary example makes the exclusion concrete. Let `alpha=1`, `phi=1/2`, `B_f=1/2` and `L=1/4`. Then `G_osc=1/8` and `B_fL=1/8`, so structural contrast at least two is necessary. Existing sharp binary bounds show that any state-specific task with at most five represented worlds has `g_i<=1`; the same is true for any binary task with at most four declared cues or at most four minimal productive obligations. If both ecological states are drawn from any one of these architecture classes, their gaps lie in `[0,1]`, so `Delta g<=1`. All three classes are therefore ruled out for every admissible monotone `L`-bounded lift. A six-world, five-cue linear special case attains state gap two; paired against a zero-gap state it attains the necessary contrast, showing that the finite structural threshold itself is sharp when the marginal ceiling is realized.

### Ecological recurrence filters structural selection through time

Architecture limits available state-to-state selection contrasts, but it does not determine their temporal fate. For recurrent ecological states,

\[
\sigma_{\mathrm{eff}}^2=\sum_r w_r\frac{1+r_r}{1-r_r}
\]

shows that slow ecological modes amplify long-run evolutionary fluctuation only when structural reward variation aligns with those modes.

In the linear acquisition-cost special case `s_i=lambda g_i-kappa`, if `0<=g_i<=g_max`, then

\[
\sigma_{\mathrm{eff}}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}},
\]

where `r_max<1` is the largest nontrivial algebraic eigenvalue. The bound is sharp in the extremal sense but not generically tight. Its slack separates use of the available reward range from alignment of reward variation with the slow ecological mode. Consequently, slowly changing ecological states need not produce long evolutionary memory when sensing-generated reward is weakly aligned with the slow mode.

### Oscillatory return diagnoses feedback but not its magnitude

The same local model yields an interpretive boundary. Stable monotone return can admit a decomposition with `G=0`. By contrast, if the local eigenvalues are a non-real conjugate pair and `0<=T<2`, the characteristic polynomial is positive for every admissible real ecological persistence value, so every model-compatible decomposition has `G>0`.

Thus compatible oscillatory return can exclude zero feedback, but it does not identify feedback magnitude, the separate persistence parameters or the causal contribution of sensing architecture. We use this only as a diagnostic consequence of the model.

## Discussion

The central result is not that adaptive sensing is always better or that information has a universal fitness value. It is that a declared finite decision architecture defines a constrained set of ecological performances and eco-evolutionary dynamics. Exact finite mathematics identifies the adaptive-only budget window; sharp extremal theory identifies the architecture required for a given structural contrast; the nonlinear lift converts insufficient contrast into a dynamical no-go region; and ecological recurrence determines how the resulting selection is expressed through time.

This perspective changes what should be measured in natural history. Raw numbers of cues, global cue balance and environmental persistence are not sufficient summaries. The exactly-balanced construction shows that even perfectly balanced binary cues can support unbounded adaptive advantage when the required resources are branch exclusive. Conversely, the exact target-relevant kernel shows that descriptive differences among worlds or cues can sometimes be quotient-collapsed without changing the optimal contingent decision. What matters is the geometry of target-relevant branches and obligations.

The hard-budget result provides a second route from this geometry to selection. If behavior must be completed before a predator strike, host departure, handling deadline, energetic ceiling or developmental window, the interval `C_A<=B<C_F` is the precise region in which contingent sensing can succeed while fixed sensing cannot. This mechanism does not require each unit of saved cue acquisition to carry a linear fitness value. It therefore complements rather than replaces the monotone-Lipschitz structural-contrast result.

The no-go orientation also differs from the usual forward use of information in evolutionary models. Information-fitness theory asks how information changes growth or selection, and rate-distortion approaches can derive minimal mutual information for target fitness outcomes (Donaldson-Matasci et al. 2010; Rivoire & Leibler 2011; Moffett & Eckford 2022). Our object is instead a finite deterministic architecture of guaranteed decision problems: how many alternatives must be represented, which cue resources must be available, which distinctions are fixed-mandatory, and how these structures differ between ecological states.

The theory separates **what organisms can distinguish and route around** from **how ecological states recur**. State-specific decision architecture bounds available selection contrasts and determines exact success windows under hard budgets; ecological recurrence determines how those contrasts are filtered through time. A slowly changing environment matters evolutionarily only if structurally generated selection loads onto that slow mode.

Several limitations define the claim. Cue outcomes are deterministic and the sharp finite bounds use guaranteed resolution and unit acquisition costs. The kernel reductions preserve worst-path exact target resolution, not noisy Bayesian or expected-loss objectives. The budget-gated selection result requires a biologically justified hard ceiling and threshold benefit. The feedback result is local and deterministic, not a global bifurcation theorem. The nonlinear class requires an upper marginal bound `L`; no empirical value of `L`, `B_f`, `alpha` or `phi` is claimed here. Mutation, migration, drift, demographic stochasticity, noisy observation channels and multivariate genetics are outside scope.

Finite sensing architecture therefore constrains eco-evolutionary possibility in a hierarchy. Target-relevant natural history determines an exact adaptive/fixed cost pair; ecological budgets and state contrasts determine when that pair creates selection; finite extremal geometry limits how large those effects can be; and ecological recurrence determines which part persists through time. The mathematics is useful precisely because it can identify regimes that are feasible, selectively exposed, or impossible before every downstream biological parameter is known.

## Data and code availability

No empirical datasets were generated or analysed for this theoretical study. Source code implementing exact adaptive and fixed resolution, target-relevant kernels, sharp finite bounds, the balanced-query construction, budget-gated selection, nonlinear feedback reachability and ecological recurrence results is publicly available in the `zuizui0223/adaptive-gain` repository. A permanent archival DOI should be added at submission if one has been minted by then.

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
