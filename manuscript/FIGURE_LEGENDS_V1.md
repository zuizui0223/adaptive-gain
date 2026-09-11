# Figure legends v1

These legends correspond to the four deterministic SVGs in `manuscript/figures/`. They are written for the line-edited Theoretical Ecology manuscript and preserve the current result hierarchy.

## Figure 1. Finite sensing architecture and ecological recurrence share one state space

**Figure 1 | Finite sensing architecture and recurrence are indexed by the same ecological states.** (A) A generic sequential sensing task illustrates the distinction between contingent and fixed cue use. After a coarse cue identifies the relevant branch, a contingent strategy samples only the fine-scale cue needed on that branch, whereas a fixed strategy must carry the cues required across all branches. In the schematic, the guaranteed adaptive and fixed costs are `C_A=2` and `C_F=3`, giving structural gap `g=C_F-C_A=1`. (B) The same recurrent ecological states are connected by transition operator `P`. State-specific sensing structure generates `g_i` and, under the declared ecological lift, `s_i=lambda g_i-kappa`; transitions among those states determine recurrence of the same state-indexed rewards. The sensing tree is illustrative rather than an empirical measurement protocol.

**Preferred first callout:** end of Model section 2.2, after the definition of `g_i` and `E_i`.

Suggested callout sentence: `The distinction between contingent and fixed cue use, and its connection to recurrence of the same ecological states, is summarized in Fig. 1.`

## Figure 2. Required dynamics imply required finite sensing structure

**Figure 2 | Principal reachability result: a required local regime imposes a minimum or Pareto-minimal finite sensing architecture.** The top sequence maps local response parameters to a required dynamical phase, then to the required integer adaptive/fixed structural gap, and finally to the admissible finite structural set. (A) For binary unit-cost sensing with required gap `q=2`, `h_2^*(2)=3` and the exact componentwise first corner is `(n,m,E)=(6,5,5)`. (B) With bounded cue arity, componentwise minima need not be jointly attainable. For `q=3,b=4`, `(n,m,E)=(8,5,5)` and `(7,6,6)` are both nondominated Pareto points. (C) For the displayed `q=2` example, increasing cue arity from two to three or more reduces the minimum cue/obligation burden from five to four while the minimum represented-alternative count remains six. The plotted quantities are finite structural counts, not Shannon-information lower bounds.

**Preferred first callout:** end of Results section 3.1.

Suggested callout sentence: `The reverse map, its binary exact corner, and the bounded-arity Pareto trade-off are summarized in Fig. 2.`

## Figure 3. Structural-temporal extremal envelope and exact slack

**Figure 3 | A sharp structural-temporal ceiling can remain loose for a particular ecological system.** The long-run fluctuation bound combines the maximum state-dependent reward range with the largest algebraic temporal amplification factor of a reversible ecological chain. (A) The multiplier `f(r)=(1+r)/(1-r)` increases with the ecological eigenvalue `r`, so slow recurrent modes can amplify long-run variance. (B) Realized variance relative to the theorem ceiling factors exactly into range/variance saturation and reward alignment with the slowest mode; both factors are at most one. (C) A symmetric two-state chain with endpoint rewards attains equality, establishing extremal sharpness. The contrasting three-state reversible fixture uses transition matrix `[[0.7,0.3,0],[0.3,0.4,0.3],[0,0.3,0.7]]` and reward vector `[0,1,0]`, giving range/variance saturation `8/9`, slow-mode alignment `11/51`, and realized-to-bound ratio `88/459` (approximately `0.192`). Thus mathematical sharpness does not imply generic empirical tightness.

**Preferred first callout:** end of Results section 3.2.

Suggested callout sentence: `Fig. 3 separates extremal sharpness from realized tightness by displaying the two exact multiplicative sources of slack.`

## Figure 4. Long-time outcomes and the diagnostic status of oscillation

**Figure 4 | Similar long-term net change can arise from dynamically distinct mechanisms.** Four schematic trajectories distinguish directional accumulation, neutral temporal cancellation, monotone restoring return, and oscillatory restoring return. Under neutral cancellation, a zero-drift period map has multiplier one, so perturbations persist. A stable monotone local return may remain compatible with a zero-feedback decomposition. By contrast, a non-real local eigenpair forces positive feedback only after the observed trace is shown to satisfy the generalized persistence-domain gate `0<=T<2`. The displayed oscillatory fixture (`alpha=1`, `phi=0.5`, `G=0.5`) has `T=1.5`, `D=0.75`, oscillation threshold `G_osc=0.125`, eigenvalue modulus `sqrt(3/4)`, and period 12 generations. The cancellation/restoration distinction is a mechanistic proposition; the feedback implication of a model-compatible complex mode is the diagnostic theorem.

**Preferred first callout:** end of Results section 3.4, after sections 3.3 and 3.4 have established the diagnostic and mechanistic distinctions.

Suggested callout sentence: `The four long-time outcomes and the stronger feedback implication of model-compatible oscillatory restoration are contrasted in Fig. 4.`

## Submission control

- Keep Figures 1-4 in this order.
- Do not promote Figures 3 or 4 into coequal headline claims with the principal reachability result in Figure 2.
- Do not label any Figure 2 axis or annotation as `bits`, `mutual information`, or a generic `minimum information requirement`.
- Do not add an observation-design figure to the main text.
