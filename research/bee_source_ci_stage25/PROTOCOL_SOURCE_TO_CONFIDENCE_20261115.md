# Stage25 — original-source readiness gate and simultaneous recognition confidence intervals

**2026-11-15. Prospective source-validation protocol, source-free statistical software and mock-only tests. ZERO new observed bees.** Draft extension stacked on Stage24 PR #102. Stage22–24 scientific results, prior source data, V5/V6 and main are unchanged.

## What this stage actually delivers

A runnable **fail-closed original-trial validator** and conservative simultaneous statistical confidence interval calculator. The program reads a prospectively collected trial table and rejects duplicated original animal/class records, absent true bits, leaking root/other signals, cue-response-feedback ordering errors and mismatched SHA-256 trial-table digests. None of this proves source authenticity and no actual bee source data have been supplied.

The six independently observable class-conditional recognition rates are:

| Rate | Correct original response | Independent sampling unit per colony |
|---|---|---|
| s0 | report root Z0 given true R0 | one independent bee responding to true R0 |
| s1 | report root Z1 given true R1 | one independent bee responding to true R1 |
| u0 | report U0 given true U0 | one independent bee responding to true U0 |
| u1 | report U1 given true U1 | one independent bee responding to true U1 |
| v0 | report V0 given true V0 | one independent bee responding to true V0 |
| v1 | report V1 given true V1 | one independent bee responding to true V1 |

A bee may contribute one record in different source/true-bit classes, but **never two frames or repeated trials within the same class**. Distinct colonies are not silently pooled. Independence of sampled bees within each original colony/source class and stationary Bernoulli hit rates are sampling assumptions that MUST be independently reviewed, not inferred from flags. Cross-class dependence is permitted by Bonferroni even though same-bee within-class pseudoreplication is not.

## Conditional simultaneous coverage (not an 8D biological confidence region)

For K colonies, compute six separate two-sided equal-tailed exact Clopper-Pearson binomial confidence intervals per colony, each using alpha=0.05/(6K). The Bonferroni bound guarantees at least 95% simultaneous coverage of the 6K colony-specific class-recognition probabilities, **conditional** on original independent Bernoulli sampling units and the calibrated classification design. Endpoints are conservatively rounded OUTWARD to six decimals.

The other two Stage24 parameters, q (the animal's genuinely LEARNED branch prior, not the programmed stimulus frequency) and c (the unit-correct-reward-equivalent PAID-query cost), are NOT estimated by this procedure. An input JSON may supply intervals for q/c, but these are explicitly EXTERNAL ASSUMPTIONS with no verified confidence coverage in Stage25. No 95% joint coverage of all eight inputs is asserted.

If every rate interval lies in the original Stage24 recognition domain [0.5,1] and external q/c intervals are present, the gate passes these intervals into the existing exact 256-corner Stage24 theorem separately for each colony. It NEVER truncates a rate interval to [0.5,1] to manufacture a positive result. A positive mathematical bound means only: **if all parameter and channel-assumption premises are correct, the model predicts conditional net reward advantage**. It is NOT a measured biological difference.

The Stage24 Bayesian model additionally assumes independent sensory channels conditional on hidden world state, independently redrawn R/U/V each trial, stationary source use and an appropriately calibrated cost. Marginal correct-rate records do NOT test source-noise correlation across successive decisions. Individual animal SKIP/U/V requests, prospective reward equivalence and randomized contingent-vs-precommit payoffs are absent.

## Machine-readable input contract

One JSON object has a manifest object and trials array.

The manifest must state source_kind = mock or declared_original_unverified, the canonical SHA-256 of the trial array and four prospective source design flags:

- independent_bee_sampling_by_class = true
- randomized_and_blinded_true_classes = true
- source_specific_isolation_verified = true
- recorded_before_correctness_feedback = true

It may include q_interval and c_interval as numeric string endpoint pairs. A declared-original input additionally requires ethics_reference and original_source_uri. These are self-declarations; an internally matching digest proves file integrity only, NOT source provenance or valid ethics permission.

Each original trial includes trial_id, colony_id, bee_id, cue in Z/U/V, binary true_bit, binary reported_bit and timezone-aware cue_time_utc, response_time_utc and feedback_time_utc (strict chronological order). original_response_blinded, other_sources_hidden and reward_hidden must be true. Every bee ID must belong to exactly one colony and may contribute at most one record for each cue/true-bit class. File SHA-256 uses UTF-8 JSON of the trials array with sorted keys, compact comma/colon separators and no ASCII escaping. The trial input itself must remain externally inspectable; the CI only uploads derived source-free receipts by default.

Commands:

    cd research/bee_source_ci_stage25
    PYTHONPATH=../bee_robust_stage24:. python -m unittest test_source_confidence_gate -v
    PYTHONPATH=../bee_robust_stage24:. python source_confidence_gate.py --out stage25_source_gate_outputs
    PYTHONPATH=../bee_robust_stage24:. python source_confidence_gate.py --input /absolute/path/to/original_trial_manifest.json --out analysis_receipts

With no input, the tool writes NO_GO_NO_ORIGINAL_TRIALS rather than fabricating a validation dataset. Test fixtures use invented mock-colony and bee IDs only; even an artificially strong positive mathematical model bound NEVER sets biological_positive_claim to true. A source marked declared_original_unverified remains unverified by this tool.

## Prospective feasibility calculation

For K=2 original colonies there are 6K=12 separately protected recognition rates. The nominal per-class two-sided alpha=0.05/12; each tail uses 0.05/24=0.0020833. Even in the best possible case of ALL animal classifications correct, it takes at least **152 distinct independent bee responses in one class, within each colony**, for the lower confidence bound in that class to reach 0.96. Hundreds or thousands more independent animals may be needed to constrain a rate around 0.8 to a narrow interval. Recording more frames or repeated visits from one bee is NOT a substitute for additional independent units.

## Pending biological identification steps

1. Acquire externally authenticated original independent bee/colony classification trials with separate true0/true1, blinding and no root/leaf/reward leakage. Review within-class independence and between-animal/colony heterogeneity.
2. Independently establish the LEARNED branch prior q and measured normalized query cost c with justified simultaneous interval coverage and source receipts.
3. Test model structure (class channel invariance across time and conditional cross-source noise dependence) rather than silently treating independent marginal error rates as a full sensory model.
4. Record genuinely animal-initiated first SKIP/U/V and optional second query, with video timing and original reward mapping; automatic cue presentation is not a chosen query.
5. Conduct preregistered independent-colony randomized precommit-vs-contingent realized reward comparisons, under applicable animal ethics permission.

**BIOLOGICAL STOP:** No measured original animal confusion, calibrated q/c, actual information requests or realized animal reward comparison is present in this PR. Stage24's 0.01008 is NOT an empirical estimate and is never converted into seed set, reproduction or animal fitness.
