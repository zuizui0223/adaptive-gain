# Cue-trace fidelity audit for the bee policy-access pilot

**Status:** Prospective supplemental data-quality/process check for adaptive-gain PR #68. No real bee data have been analyzed. This protocol does not revise the randomized ITT outcome, prove cue perception, identify natural selection, or introduce an additional theorem.

## Why this is needed

The randomized ITT contrast in `BEE_POLICY_ACCESS_PILOT_PREREG_V1.md` asks whether *offering* outcome-contingent cue access improves correct final choice relative to a fair, ordered precommitted control. The primary `pilot_itt.py` intentionally reads only the enrollment roster, scheduled target and final action. **Even a positive ITT contrast could reflect unequal acquisition opportunities, a fixed arm covertly choosing its second cue after the first result, additional cue exposures, different latencies, or technical absence of cue delivery.** These mechanisms cannot be excluded by final choices alone.

The present audit is a **separate secondary/descriptive measurement**. Its purpose is to report these anomalies without deleting noncompliant or unobserved bees from the assigned-arm ITT analysis.

## Four source files

1. The original *immutable pre-randomization* `bee_roster.csv` (`bee_id,colony_id,assigned_access`), one row per enrolled bee.
2. The original `bee_trials.csv` (`trial_id,bee_id,slot,target,outcome_status,final_action,unobserved_reason,delivered_access`), one row per scheduled slot, including no-exposure/dropout placeholders.
3. A **pre-exposure sealed fixed-plan** file with the header in `experiments/templates/pilot_fixed_plans_schema.csv`: `trial_id,bee_id,second_cue,plan_archive_id`. There must be a plan row for *every precommitted-assigned trial*, even if the trial is never delivered. `second_cue` is B or C, chosen before the first trial cue and before the target reveal in any design where advance target knowledge could leak. For contingent-assigned trials, do not include a fixed-plan row. The archive ID points to an independently stored and time-stamped, preregistered assignment manifest. **An ID string or a SHA-256 digest by itself is not proof the plan was fixed beforehand.**
4. A long-form **actually offered/acquired cue-event** file with the header in `experiments/templates/pilot_cue_events_schema.csv`: `trial_id,bee_id,step,cue,response,elapsed_ms`. `step=1` denotes first cue A, `step=2` denotes B/C, and additional steps are retained as explicit budget violations, not deleted. `response` is a separately scored/reportable perceived-cue bit 0/1 or blank when unknown. `elapsed_ms` measures time from the start of the **same trial opportunity**, not time since the preceding cue; the maximum allowed elapsed time is the preregistered `deadline_ms`. A blank time is unverified timing. Include *only actual cue events*, never invent planned events as if delivered. Keep the original video/stimulus and blinded scorer metadata in an auditable supplemental event registry.

The event schema is deliberately separate from the minimal trial CSV: presenting an image, the insect visually attending to it, and obtaining an independent report about its content are different observations. If behavior lacks a trustworthy cue-perception reporting assay, use `response` blank and **do not treat branch-rate summaries as evidence of an internal perceptual mechanism**.

## Runnable quality-control check

```bash
python -m adaptive_gain.pilot_process \
  --roster bee_roster.csv \
  --trials bee_trials.csv \
  --events bee_cue_events.csv \
  --fixed-plans bee_fixed_plans.csv \
  --planned-trials-per-bee 4 \
  --deadline-ms 3000
```

The 4 planned slots and 3000 ms deadline above are **illustrative command values**, not a biological recommendation. Set both according to the pilot's sealed protocol. The command outputs JSON with separate `process`, unchanged `itt`, and SHA-256 hashes of the four input files for provenance. Save the JSON alongside the locked schedule and scorer's decision trail.

## What is inspected, and what is not established

The code requires the same enrolled bees and every scheduled trial slot as `pilot_itt.py`. It cross-checks the precommitted schedule with actually observed second-cue identities and counts missing fixed plans, plan mismatches, first-cue misidentification, duplicate/invalid event paths, more than two acquired cues, events after the deadline, missing response or timing, and cue events in trials explicitly recorded as `not_delivered`. Unknown or cross-arm delivered access remains an ITT fidelity diagnostic. These are **counts on the complete trial frame**—they never remove trials or switch a bee's randomized arm.

For **contingent-assigned, actually delivered trials** with a valid A→B/C trace, observed A response, and valid timing, the tool reports the two descriptive conditional frequencies `P(request B | observed A=0, acquired a second cue)` and `P(request B | observed A=1, acquired a second cue)`. Their difference documents whether next-cue identities vary with earlier reported outcomes. **It is not a causal effect, does not establish an optimal policy, and is conditional on actually reaching the second cue** (a post-randomization selection event). All zero-cue/early-stopping and no-choice trials remain in the ITT and must be reported separately.

`mechanism_status` has three strictly limited labels:

- `process_fidelity_or_measurement_unresolved`: missing/invalid cue plans, timing or response, budget overrun, plan mismatch, unknown/cross-arm delivery, or a trial reported as not delivered despite observed cue events.
- `insufficient_branch_data`: no valid two-cue observations in at least one observed A context, despite otherwise clean supplied logs.
- `branch_order_observable_not_causal_proof`: valid traces in both A contexts and no recorded integrity anomaly; **not** a claim of information-driven behavior, no-interference, treatment consistency, reliable internal perception, or evolutionary fitness.

If the apparatus deliberately **offers** a cue but the animal refuses to inspect it, the investigator must preregister whether `CueEvent` means *physical delivery*, *verified attention*, or *reportable acquisition*, and keep those layers separately in richer video metadata. The minimal checker treats each event as a purported acquired cue; it cannot resolve this distinction. It also cannot cryptographically verify a plan's ex ante sealing or the correctness of recorded timestamps. Periodic, independently verified video scoring and the raw apparatus logs remain essential.

## An actual ecology experiment: the stop rules

The principal effect remains the **assigned-arm ITT** from `pilot_itt.py`. Before any ecological routeability claim, ensure (a) true randomization of bee assignment within each colony, no cross-bee interference, and locked preassignment roster; (b) the fixed plan really predated the first cue and was not correlated with unblinded target truth; (c) both arms received equal budget, physical exposure and deadline; (d) event history and final action are independently observed or missingness sensitivity reported; and (e) perceived first-cue responses are independently calibrated rather than inferred from a successful final flower visit.

A positive ITT with high plan mismatch, budget overruns or missing event histories is **an effect of an experimentally offered procedure**, not identified evidence of conditional cue acquisition. A significant descriptive branch-order association is not sufficient either; it may reflect differential continuation, motivation, learning, or sensory acquisition. The timing of the experience and training context should be assessed with preregistered within-bee and colony stratification, and a real confirmation study needs adequate colonies, independently determined feasible sample size and explicit welfare decisions.

**Boundary:** This is a data-collection readiness audit for an already existing experiment design. There are no observed pollinator response data, ecological fitness measurements, or identified interaction-network rewiring in these examples.
