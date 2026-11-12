# Stage20 — Class-specific root-cue errors and observable pilot gate

**12 November 2026 | EXACT SOURCE-FREE THEORY and MOCK SOURCE-QA ONLY; ZERO NEW LIVING BEE OBSERVATIONS.** Research extension stacked on Stage19 PR #97, with all Stage9b–19 results and main unchanged.

## Distinct two-error-class hypothesis

Stage19 assumed identical recognition correctness s for both root signal classes. In a real blinded root-classification pilot the actual source confusion matrix must distinguish:

- s0 = P(observed label Z=0 | true source R=0),
- s1 = P(observed label Z=1 | true source R=1).

The complete 2×2 source confusion matrix is R0→Z0=s0, R0→Z1=1−s0, R1→Z0=1−s1, R1→Z1=s1. Source root R has equal prior frequency, but with unequal errors the observed Z need NOT be equally frequent. Specifically P(Z0)=(1+s0−s1)/2 and P(Z1)=(1−s0+s1)/2. A naïve average of the two percentages cannot replace the full conditional likelihood in the Bayes decision.

## Frozen exact finite game

Same hidden task as Stage18/19: independent R~Bern(.5), U~Bern(q=.2), V~Bern(.5), target U when true R0 and V when true R1, with hidden worlds drawn IID WITH REPLACEMENT each trial. Correct outcome pays 1, incorrect 0, optional initial SKIP/U/V and optional second distinct leaf request, leaf sensor perfectly accurate, and fixed c=.25 normalized reward units per actually requested leaf. Contingent chooses initial SKIP/U/V after seeing Z. Precommit chooses initial SKIP/U/V before Z but may order a second leaf after Z and seeing the first. Root confusion is the only new source uncertainty. The sharp claim is restricted to BOTH s0,s1 in [.5,1].

Exact evaluation of the three original first actions and the optional second request gives an optimal precommitted action SKIP with value 13/20 (.65) across that entire two-dimensional class-accuracy domain; the conditional arm SKIPs after Z0 and requests V after Z1 precisely when 11*s0 + 5*s1 > 11. Hence:

    Delta(s0,s1) = max(0, (11*s0 + 5*s1 − 11)/40).

This condition reduces to Stage19's s>11/16 for s0=s1=s. At exact equality the no-unnecessary-query tie rule chooses SKIP. In the strictly positive region the marginal sensitivity weights are 11/40=.275 for s0 versus 5/40=.125 for s1, a 2.2× difference. This is not a universal biological asymmetry: it derives from q=.2, c=.25 and the above policy set.

## Two independently checkable non-identification examples

1. Same 70% balanced classification accuracy: (s0,s1)=(.80,.60) gives Delta=.020; reversing class accuracies to (.60,.80) gives Delta=0. Same 80% balanced classification accuracy: (.90,.70) yields .060, (.70,.90) yields .030. Balanced accuracy is therefore not sufficient to identify the expected value of information.
2. Two hypothetical equally-weighted animals/colonies with confusion (.9,.9) and (.5,.5) have individual idealized optimal gains .085 and 0, mean .0425. Their average confusion (.7,.7) would yield only .005. Because the positive-part of a linear expression is convex, gain-at-average can be smaller than average gain. This comparison is exact only for equal-weight homogeneous q and c and must not be extrapolated to unequal real trial counts or hierarchical inference.

An animal that blindly uses the fixed Z0-SKIP/Z1-V policy when (.6,.8) would lose .010 relative to optimal precommit, while an optimally contingent policy chooses SKIP in both observed states and never loses value relative to the precommitted action set. No actual bee overconfidence, fitness loss or natural cognitive strategy is claimed.

## First source-quality pilot contract (NOT real data)

Mock-only code records a true R label and a distinct reported Z before any correctness feedback; an R-only classification phase (no U/V request interface); original video-verification flags, visible-trial timestamps, unique trial ID and bee-within-original-colony IDs. The public mock fixture contains ONLY 40 invented trials from two invented colony IDs; its 70% pooled class accuracy and unequal gains are deliberately injected. It rejects missing R0/R1 class support within a bee, duplicate IDs, response after feedback, leaf exposure during classification, and an actual-animal row masquerading as a synthetic demonstration. The QA contract explicitly does NOT calculate an animal population p-value or confidence interval.

Before any real animal study: independently measure BOTH off-diagonal probabilities and interval uncertainty within original bees and independent source colonies; separately verify root-bit comprehension, learned 80/50 target prior, leaf cue confusion, true animal-origin SKIP/U/V requests, actual calibrated information delay/reward and no external feeder cue leakage. Original R0 and R1 classification should occur before task feedback, and primary trials must be separately randomized with independent hidden worlds. Source classification response may combine sensory and decision biases and does not by itself isolate retinal sensitivity.

**Scientific stop:** An observed mean recognition percentage—even if >68.75%—is NOT sufficient when s0≠s1. Passing 11*s0+5*s1>11 using noisy point estimates would only satisfy an idealized mathematical necessary-and-sufficient value condition, not prove animal adaptive routing. Real population inference needs original-colony replication, uncertainty and independently calibrated q,c, and cannot reuse the 40 mock records or call them an approved pilot. Do not retune q,c, first-request choice sets or exclude animal 'nonlearners' after observing an outcome.

## Source-free code execution

[Stage20 exact + fake pilot GitHub Actions #43125720023](https://github.com/zuizui0223/adaptive-gain/actions/runs/43125720023) SUCCESS: 14 focused tests, 192 independent posterior-oracle comparisons (3 q levels ×4 costs ×4 s0 ×4 s1), 121 two-class confusion-grid cases and 40 fake classification event QA rows. This source-only CI has no empirical bee data.