# Stage29 — chance control is a source-identification question, not bee maladaptation

**2026-11-15. Existing public-author data reanalysis + conditional mathematics only. No new animals.** Draft stacked on Stage28 PR #106. All previous Stages22–28, source copies, V5/V6 and main remain untouched.

## Frozen public-source observation

Author data for He et al. (2026), *Uncertainty-Guided Decision-Making in Bumble Bees*, bioRxiv DOI 10.64898/2026.09.15.751944, are held in Cuixiaojian21/bee_metacognition. The exact information-seeking CSV is identified by commit 7f886394b4de872ecdb19ca4ea214ec321d5dce9 and Git blob 26259c9071c6d73141d56b9bedd396cab1a04491.

Across the **existing 19,200 trials and 192 bees**, the Regular + Impossible + NO information-platform landing subset includes **183 correct of 883**: 20.7248% instead of a hypothetical 50% fair two-choice baseline. In the original bee identifiers 170/192 show <50% recorded accuracy, 12 equal 50%, and 10 >50%. Earlier trial numbers 1–50: 81/442; later numbers 51–100: 102/441. This is not the distinct forced-choice control experiment reported near 50% in the manuscript.

## Exact mathematical contrast under EXPLICIT, UNVERIFIED assumptions

If the true Zone2 correct LEFT/RIGHT target is assigned independently and fairly on every selected Impossible no-cue trial; it is unobservable before the animal makes its choice; scoring is faithful; and the 883 selected trials have non-informative selection or are fixed, then their correct count has Binomial(883, 1/2) distribution. The exact integer-derived tail is

    P(X<=183)=sum_{j=0}^{183} comb(883,j)/2**883
             = 3.3694828e-72.

The probability describes a **conditional fictional fair-side null**, NOT a valid confirmatory biological p-value. The source lacks the original randomization ledger and actual chosen LEFT/RIGHT sides that would verify these assumptions.

### Retrospective selection-robust diagnostic, also assumption gated

If a no-cue decision is predictable before the true target side is independently randomized, then every selected trial's correctness is conditionally fair. A mathematical test martingale for a fixed, prospectively chosen lambda is

    M_n(lambda)=exp(lambda*(n/2-k) - n*log(cosh(lambda/2))).

For n=883, k=183, lambda=1 as a RETROSPECTIVE demonstration: log M=152.439, M≈1.60e66, 1/M≈6.26e-67. Under authenticated conditional fairness and lambda fixed without inspecting data, Ville's inequality gives an anytime-valid bound; in this case neither fairness nor preregistration was established, so **this is NOT an empirical p-value**. The mere fact that bees can decide whether to request based on past trials cannot explain the discrepancy under this strong fair-side condition, but neither can that condition be assumed without the missing assignment records.

## Sensitivity and non-identification

Suppose (toy model) that target LEFT-side probability t is independent of the bee's chosen side and bee's LEFT-choice probability is a. Then p(correct)=t*a+(1-t)*(1-a)≥min(t,1-t). To reproduce observed 183/883≈0.20725 by **side imbalance alone**, the rewarded side would need to occur at least 79.275% of the time on one side in this analyzed subset. This is a mathematical requirement under a particular model, **not** evidence that such an imbalance really occurred.

Different latent worlds could both produce 20.7%: (A) a bee always chooses LEFT while rewarded side is LEFT with frequency 183/883, versus (B) a fair rewarded-side distribution but an unmeasured anticorrelated choice/scoring mechanism. The correctness field by itself cannot separate them.

## Source schema inventory

The information-seeking CSV has no trial-level true Correct_Target_Side, no actual final Bee_Choice / Chosen_Target_Side, no original colony ID and no target-side allocation log. The same author's distinct tactile experiment publishes a Correct_Answer column (data/5_cross_modal_tactile_generalization_trials.csv), and the memory experiment publishes both Correct_Answer and Bee_Choice (data/6_cross_domain_memory_generalization_trials.csv). Stage29 separately pins and verifies those other CSV blobs and their schema, NOT their biological interchangeability or linkage to information-seeking trials.

The repo's correct file byte identity is not a substitute for the original apparatus randomization record. Original instrument-level auditing remains mandatory before a valid chance-null claim.

## Stage29 implementation

A new source-locked Python module independently verifies the published 883/183 counts, each of 192 bee IDs and the early/late source tallies; computes the exact integer binomial lower tail and retrospective predictable-selection e-value; checks the side-label and assignment-source absence; checks the separate tactile/memory source headers after pinned hash verification; and generates a machine-readable no-go receipt. Ten separate unit tests validate arithmetic, invalid source rejection and missing-data gates without presenting synthetic fixtures as real bees.

Dedicated GitHub Actions retrieves the published CSVs into temporary checkout memory, verifies SHA1 Git blob hashes, saves only derived numeric JSON summary, and refuses any empirical adaptation/fitness claim. The repository-wide three-Python-version test matrix is a separate gate.

## Decisive future original record

Need trial-keyed independent colony identifier, pre-choice rewarded Zone2 target LEFT/RIGHT, actual bee final LEFT/RIGHT choice, target side assignment randomization seed/log, Zone1 physical platform landing, cue timing/presentation, treatment flag, and independent response verification. Without these fields there is no authenticated test of whether correctness was properly at chance, a side-label mismatch, a selection effect or a correlated choice process.

**STOP:** No original bees newly measured; no data-driven Stage24 8D Bayesian sensory parameters, randomization test, adapted cognition, altered evolutionary fitness or evidence of misconduct. The unresolved 20.7% is a data-identification question.
