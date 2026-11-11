# Stage19 Results: root-cue recognition threshold in an asymmetric query task

**2026-11-12 | Exact mathematics / verification; 0 living bees tested.**

We have extended Stage18's "SKIP when R0; request V when R1" policy to a noisy observed root Z. For one fixed q=.2 and cost c=.25, the boundary is **strict s>11/16=68.75%** recognition accuracy; at/below that accuracy both observed Z conditions optimally SKIP under the source-free payoff model.

| Model root recognition s | Contingent-minus-precommit value | Uncalibrated fixed R0-skip/R1-V value vs precommit |
|---:|---:|---:|
| .50 | .000 | −.075 |
| .60 | .000 | −.035 |
| .6875 | .000 | .000 |
| .70 | +.005 | +.005 |
| .75 | +.025 | +.025 |
| .90 | +.085 | +.085 |
| 1.00 | +.125 | +.125 |

The exact formula is \(\Delta(s)=\max(0,2s/5-11/40)\) on s∈[.5,1]. \(V_F=.65\) is constant in the same model. This model assumes **symmetric root-bit flip error** and **perfect U/V sensing after paying a fixed dimensionless query cost**. Other cost/prior/confusion settings have different thresholds; no animal-level universal 68.75% threshold is claimed.

**Source-free validation:** [Stage19 eight-test independent-posterior-vs-joint-mass CI #43049021716](https://github.com/zuizui0223/adaptive-gain/actions/runs/43049021716) succeeded. At every one of 175 q×c×s test cases a separate posterior-normalized oracle agrees with exact-Fraction optimal action values to 1e−11; 315 math-only grid entries are generated. This is **not a biological replication**.

**Experiment requirement:** demonstrate root recognition and learnable q=.2 branch prior in separate animal pilots; identify root bit errors by colony/animal and root class, source-verify voluntary SKIP/U/V actions and true cost calibration, and report original sucrose intake and source-independent colonies. No real pilot or recruitment has been performed. The existing Stage17 optional-query design is NOT silently modified.


## Generalized exact threshold curve: cost fixed at 1/4

After the single-example TDD GREEN CI, the same eight-state model was generalized to any easy-branch minority target probability \(q\in[0,1/4]\), holding c=1/4. The two additional TDD tests passed on the source-free [Stage19 generalized mathematical workflow #43050503589](https://github.com/zuizui0223/adaptive-gain/actions/runs/43050503589) (**10 focused tests** total).

\[
s_{\rm crit}(q)=\frac{3/4-q}{1-q},\qquad
\Delta(q,s)=\max\!\big(0,[(1-q)s+q-3/4]/2\big).
\]

| Minority target probability q under R0 | Minimum root accuracy for strictly positive access value |
|---:|---:|
| 0 (R0 target certain) | **75.00%** |
| 0.10 | **72.22%** |
| 0.20 | **68.75%** |
| 0.25 | **66.67%** |

Counterintuitively, a MORE predictable R0 branch requires BETTER root recognition to make adaptive querying profitable in this c=1/4 task, because mistakes leading to an inappropriate V request matter more. Yet all those q settings reach the SAME **1/8** peak value when root recognition becomes perfect. This curve is **not** a universal physiological accuracy threshold and must NOT be applied if actual q, root confusion or U/V error rates differ from the assumptions.

The generalized curve was verified by Fraction-exact arithmetic against the full Bayesian oracle for seven q values and multiple s values; the RED workflow failed only because the threshold_family helper was not yet implemented, and the GREEN workflow passed. The retained 315-case math grid now includes a seven-value parametric threshold family.
