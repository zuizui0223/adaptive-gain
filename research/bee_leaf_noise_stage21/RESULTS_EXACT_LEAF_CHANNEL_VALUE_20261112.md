# Stage21 verified exact result — the *requested information itself* can be too unreliable

**2026-11-12. Exact Bayesian original-source-free mathematics; no bees or other animal sources measured.**

Stage20 assumed U/V cues were perfect after physically paying for them. We replaced that with independent symmetric binary readout channels, of accuracies \(a_U\) and \(a_V\). For the original Stage18–20 world \(q=.2,\ c=.25\), root confusion \(s_0,s_1\), exact eight-world Bayesian optimization yields:

\[
\Delta=\max\{0,\,[s_1(a_V-.75)-.55(1-s_0)]/2\}.
\]

As in Stage20, the best precommit first action and the contingent action on observed Z0 are SKIP. On observed Z1, the optimal animal requests V only when \(a_V>.75+.55(1-s_0)/s_1\). The bound is **sharp in this restricted model**, not a generalized sensory lower bound for real bumblebees.

For example at root \((s_0,s_1)=(.8,.6)\):

| Accuracy of requested V | Mathematical gain of contingent access |
|---:|---:|
| .80 | .000 |
| .90 | .000 |
| 14/15=.933333... | .000 (tie: SKIP) |
| .94 | +.002 |
| .95 | +.005 |
| 1.00 | +.020 |

**Non-obvious source-channel result:** at q=.2,c=.25, any U readout (including perfectly accurate U) never justifies its .25 acquisition cost. U's optimal-action impact is zero in this particular theorem, while V's accuracy determines whether the strategy should continue sampling at all. This does NOT mean U has no ecological importance or that the theorem applies under a lower cost.

## Two different averages cannot replace animal/source-specific decisions

At the same root confusion (.8,.6), U/V reliabilities (.8,1.) and (1.,.8) both have average accuracy 90%, yet their math benefits are +.020 and zero. Taking two imaginary equally weighted source colonies carrying these two patterns gives mean predicted value .010, but applying the nonlinear decision rule once to the pooled (.9,.9) source accuracies gives zero. Inference from aggregate classification percentages can therefore differ from inference after individual decision values are computed. No real colony was measured, and these equal weights are assumptions.

The separate 40-row QA fixture checks each leaf's true 0 and true 1 recognition separately, tied to fake bee and fake colony IDs, before feedback and without root/reward/other source visibility. By design mock U and V both pool to .90 and their gain-at-pooled is 0, while equal-colony average math gain is .010. The source gate fails closed on missing true-bit classes, invalid action origin, premature feedback, duplicate IDs, real data disguised as mock and a misspecified symmetric bit-error model. A real pilot will require uncertainty and complete class-specific confusion matrices, not exact equality of empirical rates.

[Independent Stage21 exact and mock source CI #43216365839](https://github.com/zuizui0223/adaptive-gain/actions/runs/43216365839) **SUCCESS, 17 tests**. Independently coded normalized-posterior oracle checks the exact Fraction source DP, 480 grid values, Stage20 perfect-leaf reduction and the strict \(a_V>14/15\) criterion. Original animal measurements = **ZERO**.

**Next real-data gate:** independently acquire root confusion, U/V class-conditional readout, actual source-selected SKIP/U/V and paid query delay, then measure original source-correctness/reward before claiming cognitive adaptation. A mathematical positive value alone does not license animal welfare recruitment, uncalibrated reward-cost levels, a Darwinian fitness effect or a general macroecological claim.
