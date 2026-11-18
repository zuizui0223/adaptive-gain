# Routeability direct experiment — pre-collection runbook v1

Status: operational handoff surface. No biological data are created by this file.

This runbook fixes the order from the frozen routeability design to real animal work. Machine-readable validation gates remain authoritative.

## Gate 1 — candidate physical material set

Record the exact local Bombus species/colony source, apparatus geometry, q_route/q_left/q_right physical materials, dimensions, viewing distance, colour/display or reflectance specification, reward implementation, and cleaning protocol.

Do not proceed if the material set is still mutable.

Authoritative gate: validation/routeability_physical_cue_feasibility_gate_v1.json

## Gate 2 — architecture-neutral material pretest

Use animals outside the confirmatory roster.

A material set passes only if:
- q_route final-20 accuracy >= 0.80;
- q_left final-20 accuracy >= 0.80;
- q_right final-20 accuracy >= 0.80;
- best-minus-worst final-20 accuracy <= 0.10;
- all rows are architecture-neutral;
- no confirmatory-roster animal is used.

Generate the hash-locked receipt with examples/build_routeability_material_pretest_receipt.py.

Failure means redesign and a new architecture-neutral pretest. Do not rescue a failed material set by excluding randomized animals or altering cue identities after allocation.

## Gate 3 — Pilot A

Pilot A is architecture-neutral apparatus and timing calibration.

Freeze the candidate response-window grid and upper bound before collection.

Response window rule:
smallest prespecified candidate window containing at least 95% of terminal decisions among successfully engaged calibration trials, subject to the frozen upper bound.

If no candidate reaches 95%, redesign the apparatus and rerun Pilot A.

Never choose the response window using architecture-specific or B=2 performance.

## Gate 4 — Pilot B

Pilot B uses the qualified physical cue set at B=3 full information only.

Allowed:
- pooled correctness;
- pooled timeout fraction;
- individual repeated-trial variation;
- colony variation;
- learning/fatigue summaries;
- apparatus error;
- dropout/non-completion.

Forbidden:
- architecture-specific accuracy;
- routeable-minus-bypass contrast;
- architecture x access contrast;
- B=2 data;
- H1;
- H2.

Generate the nuisance receipt with examples/build_routeability_procedural_pilot_receipt.py. The receipt must certify that the focal contrast was not opened.

## Gate 5 — freeze real nuisance inputs

Freeze:
- Pilot A response window;
- pooled B=3 nuisance receipt;
- contributing colony_count;
- colony allocation constraints;
- operational maximum individuals_per_cell;
- trials_per_individual if operationally variable.

H1 SESOI = 0.10 and H2 SESOI = 0.10 are already frozen.

The exact theoretical 0.25 information ceiling is forbidden as a behavioral power target.

## Gate 6 — build the robustness surface

Fit the frozen pooled-B3 nuisance GLMM without focal treatment labels.

Instantiate the frozen 3 baseline x 4 nuisance policy, giving the same 12 robustness IDs at every candidate N.

Candidate N values must be gapless multiples of four starting at the smallest colony-feasible value:
4 * ceil(colony_count / 4)

and continuing through the separately frozen operational maximum.

## Gate 7 — run final GLMM operating characteristics

For every candidate N and every one of the same 12 robustness IDs:
- use the same H1/H2 SESOI;
- use the same simulation count;
- run at least 1000 simulations per scenario;
- keep fit failures in the denominator;
- report singular fits separately.

The CI synthetic fixture is software validation only and is not final power evidence.

## Gate 8 — select N mechanically

Run examples/select_routeability_final_n.py.

Select the smallest colony-feasible individuals_per_cell that passes every robustness scenario:
- fit success >= 0.95;
- H1 directional rejection >= 0.80;
- hierarchical H2 pass >= 0.80.

Do not hand-select N.
Do not average away a failing scenario.
Do not change thresholds after seeing the final power surface.

## Gate 9 — freeze eligible roster and randomize

Only after final N is selected:
1. apply architecture-neutral eligibility;
2. hash the eligible roster;
3. freeze the randomization seed;
4. randomize complete 12-cell blocks within colony;
5. hash assignment and randomization receipt.

No confirmatory performance may enter roster eligibility.

## Gate 10 — compile the final schedule

Compile from the hash-matching assignment using examples/compile_routeability_final_schedule.py.

The schedule must preserve individual, colony, architecture, access, budget, counterbalance profile, and exact trials per individual.

Do not hand-edit the schedule after assignment freeze.

## Gate 11 — finalize preregistration

Use examples/finalize_routeability_preregistration.py.

The finalizer must independently verify:
- material-pretest log/spec/receipt hashes;
- pilot receipt;
- frozen SESOI;
- power surface;
- final-N rule and selected N;
- candidate-N coverage;
- randomization receipt;
- assignment balance;
- final schedule fidelity;
- stimulus mapping;
- ethics/regulatory input;
- frozen pre-collection Git commit.

No unresolved placeholders may remain.

## Gate 12 — confirmatory collection may begin

Only after Gate 11 passes.

Primary endpoint:
1 = correct terminal decision within the frozen response window;
0 = incorrect decision or timeout.

Timeouts remain in the primary denominator.

Architecture-specific training accuracy is not an exclusion criterion.

Confirmatory hierarchy:
1. H1: Delta_B2 > 0
2. H2: budget localization, confirmatory only after H1 passes.

## Hard prohibitions

Do not:
- open B=2 or H1/H2 during Pilot A/B;
- use the 0.25 information ceiling as a behavioral effect size;
- use pilot H1/H2 to power the study;
- alter a passed material set without a new architecture-neutral pretest;
- exclude animals for low architecture-specific training accuracy;
- drop timeout trials from the primary endpoint;
- hand-select final N;
- hand-edit the final randomized schedule;
- begin confirmatory collection before preregistration finalization.

## Current stop point

Formal design: PASS.
Material qualification algorithm: PASS code, real materials pending.
Pilot A/B protocol and receipt code: PASS, real pilot pending.
SESOI and final-N thresholds: FROZEN.
Power/robustness/final-N machinery: PASS code, real nuisance inputs pending.
Ethics, local colony supply and apparatus: pending.

Next real action:
choose the exact local Bombus/apparatus/material set, run the architecture-neutral material pretest, and produce the hash-locked PASS material qualification receipt.
