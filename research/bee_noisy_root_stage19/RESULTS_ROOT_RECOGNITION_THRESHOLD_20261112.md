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
