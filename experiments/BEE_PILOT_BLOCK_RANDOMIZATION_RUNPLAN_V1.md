# Artificial-flower bee pilot: sealed allocation and stimulus run plan

**Status: prospective study logistics, not biological results.** This supplements the existing PR #68 colony-blocked, bee-assigned ITT protocol. No real bees have been enrolled or measured here; example inventory identifiers and the demonstration seed are synthetic. No change is made to the frozen V5/V6 manuscripts or the ITT estimator.

## Why add this after the cue-trace and missingness audits?

`pilot_itt.py` already audits an enrolled roster and every planned trial, and `pilot_process.py` can flag over-budget cue acquisition and deviations from fixed plans. They did **not create or independently rederive** the initial blocked assignment, true target presentations, or fixed-arm schedule. An experiment that fills in these records *after seeing outcomes* could pass many downstream format tests without implementing the planned randomization. This addition addresses that prospective workflow gap, not a new mathematical result.

## Proposed design and restrictions

- **Enrollment unit:** individually identified bee (`bee_id`), with an immutable pre-exposure colony assignment (`colony_id`). The whole inventory must be locked **before** producing or viewing randomization results. Use only laboratory anonymized IDs in any shareable outputs.
- **Arm randomization:** within each colony, exactly half the enrolled bees are assigned once to `contingent`, the other half to `precommitted`. Each colony must contain an **even number of at least four bees**. The pseudorandom allocation is deterministic under a user-held 256-bit secret seed. The seed must be generated independently of the roster and never repeatedly searched to obtain a preferred allocation.
- **Stimulus schedule:** each bee receives an *illustrative* **multiple of eight** planned trial slots, covering every `(target 0/1, context_truth A=0/1)` combination equally. Order is shuffled independently of the treatment arm. This prevents gross target/context opportunity imbalance by design. It is **not** a sample-size, power, training or animal-welfare recommendation. A shorter four-slot pilot needs a separately justified, pre-locked design and must not silently reuse this eight-cell generator.
- **Fixed arm:** every target/context combination is also crossed equally with preselected second cue `B` or `C`. The fixed second-cue plan is created **before** any first-cue readout, and it cannot be revised after A=0/1. A `plan_archive_id` is a reference label, not proof of the time at which the file was locked.
- **Contingent arm:** no preselected second cue is entered in the fixed-plan CSV. A live actor may choose its next cue conditional on independently observed A and within exactly the same two-cue/elapsed-time opportunity as the control. Experimenters must verify the real apparatus permits the choice and does not provide extra cues or more time.
- **Target vs perception:** `context_truth` is the physical stimulus assigned by the apparatus. It is **not** a bee's perceived `A.response`. Do not substitute stimulus truth for an independently recorded first-cue response in the process audit.
- **Colony interference:** shared foraging, odor marks, social transmission, altered resource availability, or other spillover can invalidate bee-level no-interference. In such a case the pilot needs a separately preregistered colony-randomized design; the existing within-colony bee-label permutation test is not valid.

## Generate exactly once; archive before any exposure

The `pilot_inventory_example.csv` in `experiments/templates/` is only a sample; replace it with a locked inventory of anonymized real enrolled bees if and when ethically approved experimental observations are undertaken. **Keep the secret seed file and experiment-generated allocation/schedule outside public GitHub.**

```bash
# Prepare a secret 256-bit seed in a PRIVATE location; refuses to overwrite.
python -m adaptive_gain.pilot_design new-seed --out PRIVATE/pilot_seed.hex

# Generate one blocked allocation and eight-cell balanced schedule.
python -m adaptive_gain.pilot_design generate \
  --inventory PRIVATE/bee_inventory.csv \
  --seed-file PRIVATE/pilot_seed.hex \
  --slots-per-bee 8 \
  --outdir PRIVATE/pilot_locked_plan

# Verify the locked assignment/schedule against the seed and inventory.
python -m adaptive_gain.pilot_design verify \
  --inventory PRIVATE/bee_inventory.csv \
  --seed-file PRIVATE/pilot_seed.hex \
  --slots-per-bee 8 \
  --outdir PRIVATE/pilot_locked_plan
```

The generator emits `bee_roster.csv`, `stimulus_schedule.csv`, `bee_fixed_plans.csv`, `design_manifest.json`, and `bee_trials_template.csv`. The first three are **locked**; the manifest contains their SHA-256 hashes, the secret **seed commitment** (not its value), the per-colony arm counts and a plan label. Save the manifest and the locked files with an **independently verifiable external timestamp before data collection**. Even a matching SHA-256 digest and `verify` command do *not* establish that they predated the observations. An experimenter with the seed can recompute variants; independent custody and a documented once-only random draw are essential. Record who generated and approved the schedule, blinded scorer identity, protocol version, and any deviations.

**No overwritten plans:** `generate` fails if the destination directory already exists. `verify` refuses a changed locked schedule, fixed-plan CSV or manifest, but deliberately ignores `bee_trials_template.csv`, which is a **copyable blank experiment log** rather than a sealed result. Never edit the locked allocation or target schedule when a bee drops out or a cue is not delivered. An unrun slot must remain in the *actual* trial log with explicit `unobserved` status and a valid missing reason.

## Example structure and existing analysis interoperability

`stimulus_schedule.csv` includes `trial_id,bee_id,slot,target,context_truth,first_cue`. The first cue is A for every slot. The `bee_fixed_plans.csv` header is `trial_id,bee_id,second_cue,plan_archive_id`, and contains a row only for a bee assigned the precommitted arm. `bee_roster.csv` has the exact headers already used by the ITT analyzer. The template outcome log uses the exact required `pilot_itt.py` fields, with `outcome_status=unobserved`, `unobserved_reason=not_yet_run`, and blank final/delivered action fields to **prevent fabricated observations**.

These template placeholders are **not observations of missing bee behavior**. Copy them to a new actual-data file when the apparatus is ready, then record actual `choice` / confirmed `abstain` / technical `unobserved` and each cue event independently. The original sealed design stays unchanged. Never interpret the template's trivial all-missing interval as an empirical effect.

After collecting *actual* data, run the primary analysis and the independent process audit using actual trial and cue-event logs:

```bash
python -m adaptive_gain.pilot_itt \
  --roster PRIVATE/pilot_locked_plan/bee_roster.csv \
  --trials PRIVATE/bee_trials_actual.csv \
  --planned-trials-per-bee 8

python -m adaptive_gain.pilot_process \
  --roster PRIVATE/pilot_locked_plan/bee_roster.csv \
  --trials PRIVATE/bee_trials_actual.csv \
  --events PRIVATE/bee_cue_events_actual.csv \
  --fixed-plans PRIVATE/pilot_locked_plan/bee_fixed_plans.csv \
  --planned-trials-per-bee 8 --deadline-ms 3000
```

`3000` ms is illustrative. Predefine the actual deadline after a small feasibility test; validate apparatus timestamps, response detection, training mastery and treatment fidelity. A positive ITT on actual observations tests **offered conditional cue access**, not automatically endogenous cue perception, heritable fitness or natural network rewiring. Conditional branch rates are descriptive and must not displace the assigned-arm primary estimand.

## Checks performed before data collection

`tests/test_pilot_design.py` validates seeded reproducibility across input ordering, changing seed, equal within-colony allocation, treatment-independent balanced target/context sequences, each bee's target × context × fixed-cue factorial balance, compatibility with existing ITT and process intake, secret seed nonpublication, file-level tamper detection, and refusal to replace existing plans. The fixture additionally verifies the offline `new-seed` command creates a non-overwritten file with POSIX permissions `0600`.

The new generator is a **design tool**, not evidence that the actual biological protocol has been approved, implemented or randomized faithfully. Before a confirmatory trial, use feasible bee and colony numbers, animal-welfare requirements, attrition, and independently measured within-bee/within-colony variation to justify sample size and the selected trial count. This is aligned with established ARRIVE 2.0 experimental design and reporting principles, not a claim of new statistical methodology.
