# Stage15 — A falsifiable experiment for genuinely contingent information requests

**2026-11-11 | Mathematical benchmark + synthetic software validation complete. Real bee observations: ZERO.** Separate design branch stacked on Stage14 PR #92; existing PRs #85, #87–92, frozen V5/V6 and `main` are not altered.

## Scientific decision and why Stage14 was insufficient

The Stage14 (wind × experimenter-chosen cue order) mathematical counterexample proves that an externally imposed cue-order effect can be produced by a passive subject that **never selects which information to obtain**. Repeating that design or using retrospective wind × co-occurrence correlations cannot identify adaptive information querying. The next meaningful mechanism is **animal-origin requests** conditional on an earlier source observation, with a matched opportunity to guess or request a second cue and measured costs.

Stage15 creates an alternate, prospective **randomized contingent-access versus precommitted-access** design. It does NOT assert a causal result or pretend that any animal or independent colony has been recruited.

## Exact conditional-routing construction (8 states)

Each synthetic state consists of three mutually independent unbiased binary variables **R, U, V**. A target flower is defined by **U if R=0**, **V if R=1**; the target maps to one of two physical choices, with neither leaf value displayed before a source request.

After receiving the same R value:
- **Contingent arm**: subject chooses first U/V leaf request *after* receiving R. A perfectly trained, accuracy-maximizing conditional policy requests only the relevant leaf. Exact requests **1**.
- **Precommit arm**: subject must choose and physically bind the first U/V request *before* R arrives. The subject may still request the other leaf after R if its initial request was irrelevant. Because the 8 states are balanced and R is independent of the precommit choice, the wrong initial source has probability 1/2. Exact expected requests **1.5**, even when the animal is correct on every trial after taking any needed second cue.
- **Exact difference**: 0.5 leaf requests per trial, or including the common R exposure, 2 versus 2.5 total acquired items. A toy source cost of 0.1 reward units per leaf request gives a math-only expected full-information utility difference of **0.05 reward units**.
- This is a restriction of the *first* follow-up request; precommit permits a conditional second request, and should not be described as a universal mathematical extremum over all fixed information policies, nor as an achieved wild bee payoff.

Unlike PR92, both arms can initiate an actual information request through the same physical interface; the randomized factor is **whether the first leaf request is committed before or selected after observing R**, with a matched neutral motor act on the other side of the root reveal. Motor/expectation effects and real animal learning are not automatically solved.

## Verified software package (no original animals)

[Corrected source-independence GitHub Actions #42847101524](https://github.com/zuizui0223/adaptive-gain/actions/runs/42847101524): **SUCCESS**, **23 focused tests** and source-free exact 8-world enumeration. A synthetic balanced example has **24 pretend independent colonies ×12 pretend bee IDs ×64 pretend trials =18,432 fake allocations**; the 4 access-mode×wind cells each have 4,608 trials. In each 16-trial wind block, eight trial opportunities are allocated to each access mode; R/U/V are drawn INDEPENDENTLY WITH REPLACEMENT on every trial, preventing finite-deck prediction of future values. Wind block order is ABBA/BAAB-style balanced within colonies.

The source-free physical telemetry contract was tested against mock 3D wind vectors, on/off request timestamps, actual selection origin flags, root then leaf revelation, source bit identity, two physically available target choices, sensor mass/camera clock consistency, and at least 98% adherence **within every one of four factorial arms**. It rejects program-controlled selection disguised as a real animal's source query, precommit after R, preselected contingent leaf, doubled same leaf, fake no-consumption zeros, invalid source velocities and missing trial IDs. These *flags and mock wind recordings* DO NOT verify real instruments or video; an actual study must independently confirm the original video and instrument source logs.

The fixed colony-equal intention-to-treat estimator was tested with intentionally **INJECTED fake intake** `30 mg − 2 mg for each extra leaf request + Gaussian mock error (SD 0.5 mg)`, not a biological reward model. With independent-with-replacement source assignment, the finite simulator realized **0.5002170139** saved leaf requests, not exactly 0.5; the toy intake difference was **+1.00254858 mg/30s**, which was injected by a formula and is not independent biological evidence. **Both quantities are direct consequences of the simulator**, not independent positive results; no empirical confidence interval or p-value is reported.

The original root-reveal-to-outcome clock is the same 30-second fixed interval regardless of how many requests were made. This prevents artificially erasing real time opportunity costs by restarting observation only after the subject finishes information acquisition. Genuine no-choice/no-feeding trials remain zero only with verified functioning sensors; missing instrumentation remains NO_GO.

## Specific inference permitted by a future properly randomized study

Predeclared future **primary** is colony-equal contingent-minus-precommit **actual consumed sucrose mass per fixed 30 seconds anchored at the root cue**, averaging equally over both randomized wind conditions. Use all assigned trials and original tagged bees; first bee-equal within independently recruited colony, then colony-equal. Two-sided Student-t CI/p across actual independent colonies only when at least 12 real independent colonies are available; fewer give descriptive pilot. Do not treat thousands of trial events as independent animals.

Locked future secondary checks are: true physically counted U/V leaf requests, whether the first selected U/V request matches the R-dependent relevant cue, actual correct-target choice rates/no choices, and whether the contingent-access advantage changes in independently calibrated crosswind. Secondary signs **must not replace** a null primary intake benefit; full accuracy is a mathematical benchmark, not an assumption about real animals.

Prospective source and ethics no-go: animals must learn all R/U/V mappings and demonstrate control of the physical query interface in an independent blinded pilot; root/leaf cues must not leak, requests and their time must be physically observed rather than inferred from assigned treatment, actual wind/turbulence and feeder intake must be measured/calibrated, physical query costs and both available targets identical across randomized modes, and animal welfare feasibility approved before registration and data collection. The synthetic public QA random seed MUST NOT be used to assign future real animals.

## Why the present result is nontrivial but NOT ecological proof

This delivers a **testable mechanistic bridge** to adaptive decision topology: changing *when the subject can choose which information to request* modifies the minimal required information acquisition even with identical R/U/V world statistics. Its mathematical difference is exact. The model also makes explicit how a subject's guessing, training failure, motor cost or environmental wind response can eliminate or reverse any biological advantage.

Only a successfully randomized, source-video-verified original-animal study could identify a real benefit of **contingent access opportunity** in the engineered task. It would not by itself establish a universal wild ecological law, evolved optimized cognition, adaptive fitness, or that the full mathematical C_A/C_F bound is realized in nature. The conditional-versus-precommit intervention may still vary anticipation/commitment demands; this is not a clean neural mechanism isolation.

**Stop:** no realistic effect size, power claim, animal sample authorization, real stimulus discriminability, or future wind intensity was inferred from synthetic values. Future nulls would be frozen rather than rescued by changing cue bits, precommit choice rules or excluding nonresponsive animals.


### Post-source-only TDD correction to hidden-state independence (2026-11-11)
The initial synthetic allocation exactly exhausted eight worlds per trial block. Such a fixed deck makes future source states inferable from prior outcomes, contrary to the mathematical independent-world premise. The corrected allocation samples R, U and V independently **with replacement each trial**, fixing only treatment-arm counts. The original full-accuracy normative expectation of 0.5 fewer requests is unchanged; any finite simulator's realized saving now fluctuates around 0.5. The red-before-green test identified the leakage and the revised version uses 23 synthetic/source method tests. **No real animal outcome has been generated or examined** and no scientific effect model was tuned.
