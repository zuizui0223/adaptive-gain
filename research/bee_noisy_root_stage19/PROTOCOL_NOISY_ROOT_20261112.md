# Stage19 — recognition-limited conditional information acquisition

**2026-11-12 | MATHEMATICAL MODEL ONLY. ZERO new bee experiments, calibrated confusion matrices, or reward measurements.** Source-free extension stacked on the already-frozen Stage18 PR #96. None of Stage9b–18, frozen manuscripts, or \`main\` are changed.

## New inference boundary

Stage18 had **perfect initial root recognition**. Its q=.20,c=.25 model predicted "observed R0 → SKIP additional sources; observed R1 → request V" and +.125 normalized expected reward advantage for conditional access over a precommitted first action. That result cannot be projected onto real bees before checking how reliably they distinguish the two root values.

Stage19 puts a symmetric, independently noisy sensory channel between true R and its observed report Z:
\[
P(Z=R)=s,\quad s\in[1/2,1].
\]
The hidden world distribution is still R~Bern(.5), U~Bern(q=.2), V~Bern(.5), independently sampled WITH REPLACEMENT on every trial, T=U for R0 and T=V for R1. Correct final flower reward=1, wrong reward=0; each U/V request costs c=.25 units. **Both access conditions receive the same Z before any leaf is revealed.** The treatment only changes whether first SKIP/U/V is bound *before Z* or chosen *after Z*. A second distinct leaf request remains available after the first. A valid SKIP binds no first request and does not opportunistically become a later first request in the precommit condition.

## Exact new sharp signal-recognition threshold

For \((q,c)=(1/5,1/4)\), unnormalized eight-world Bayesian decision enumeration reduces exactly to:

- When Z=0, **SKIP** is optimal for every s∈[1/2,1]. The correct-target prediction before another request has accuracy \(0.5+0.3s\); paid U yields net \(0.25+0.5s\), which cannot surpass it in this interval; paid V is also inferior.
- When Z=1, **SKIP** gives \(0.8-0.3s\) and paid V gives \(0.25+0.5s\). Thus paid V is worthwhile if and only if \(0.8s>0.55\), or
\[
\boxed{s>11/16=68.75\%.}
\]
At equality the cost-free SKIP action is preferred by our fixed no-unnecessary-query tie rule.
- The optimal **precommitted** first action is SKIP (sometimes tied) and gives expected value exactly \(13/20=.65\) across the whole interval.
- The optimized contingent advantage is therefore
\[
\boxed{\Delta(s)=V_A(s)-V_F(s)=\max(0,\frac25s-\frac{11}{40}).}
\]
It is 0 at s=.60, +.005 at s=.70, +.025 at s=.75, +.085 at s=.90 and +.125 at s=1.

This is an **exact threshold only for the given asymmetric prior, cost and perfect leaf-reveal game**; it is NOT a universal bumblebee perceptual threshold. The cost is not mg of sucrose, milliseconds of motor effort or a measured survival cost.

## Nontrivial operational implication: an overconfident fixed rule can HURT

If an animal incorrectly behaves as if s=1 and uses the **non-optimal fixed** "Z0 → SKIP; Z1 → V" strategy despite true accuracy s<11/16, that strategy has expected net value \(.375+.4s\). The best precommitted policy remains .65. At s=.60, this learned-or-prescribed rule has relative disadvantage **−.035 normalized reward units**, whereas the truly Bayesian contingent optimum is to SKIP in both Z conditions and lose nothing relative to precommit. This is a **constructed prediction** about policy mismatch, not evidence that bees are overconfident or maladapted.

## Independent verification

[Source-free Stage19 test CI #43049021716](https://github.com/zuizui0223/adaptive-gain/actions/runs/43049021716) succeeded with **8 tests**: exact Fraction-valued joint probability dynamic programming versus an independently written *normalized-posterior eight-world oracle* on **175 combinations** of q (0–.5), paid-leaf cost and root recognition accuracy. It additionally tests a root-uninformative negative control s=.5, reduction to Stage18's perfect root limit, the exact 11/16 boundary and a harmful uncalibrated fixed strategy. The separate exported math-only grid has **315 parameter cases**.

The original RED TDD CI #43048787819 failed because \`root_noisy\` was not implemented yet; the GREEN run #43049021716 is successful. Pure mathematics—not biological data—was used for all numeric results.

## Pilot-level decision gate before any animal experiment

The **necessary** experimental ingredients for evaluating this particular quantitative threshold are:

1. A separate and blinded root-cue test to estimate **per-original-bee and per-colony recognition confusion matrices** \(P(Z=0|R=0)\) and \(P(Z=1|R=1)\), rather than a single naive pooled proportion of thousands of repeated trials. The sharp 11/16 theorem assumes symmetric errors; an asymmetric confusion matrix requires a different Bayesian frontier, not substitution of the average accuracy.
2. An independently verified learned branch prior: when R0, source target0 must actually be expected at ~80% without acquiring any leaf information; when R1, targets remain 50:50. This is **not** established by demonstrating that the bee visually distinguishes the R cue. The source task must also rule out unintended target location, odor or feeder reward leakage.
3. Verify that animal-origin **SKIP/U/V** choices are recorded, and that U/V values are recognizable when revealed; perfect leaf recognition is an *assumption* of this theorem. A weak U/V sensory channel changes the threshold.
4. Independently calibrate paid requests and blank-corrected reward within the fixed root-anchored 30s measurement. The toy c=.25 cannot be directly dialed in using arbitrary seconds of waiting.
5. Ethics/welfare and separately concealed prospective randomization must precede real animal data. A prospective independent-colony analysis is required; repeated trials from one bee do not constitute independent colonies.

At this stage there is **no actual measurement of s or q, no pilot source video, no learned stopping policy and no real sucrose payoff**. Do not treat s>68.75% alone as sufficient proof of a positive experimental effect. If these prerequisites fail, conclude the particular mechanistic claim is untestable under the assumed observation model, rather than post hoc retuning q,c or training selection after looking at outcomes.

## Research stop
Stage19 proves a *condition* for prospective routeability of a finite decision procedure under imperfect initial information. It does not prove evolved animal cognition, causal use of root information by pollinators in the wild, a general macroecological law, or observed fitness differences. Stage18's perfect-root mathematics remains valid as its s=1 special case.
