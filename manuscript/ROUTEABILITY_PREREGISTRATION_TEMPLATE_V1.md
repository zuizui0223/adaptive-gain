# Direct ecological routeability experiment — preregistration template

Status: **TEMPLATE ONLY — NOT YET PREREGISTERABLE**

This file contains the frozen scientific structure of the direct routeability experiment. Fields in double braces are unresolved operational inputs. A final preregistration must be generated only after the procedural pilot, final operating-characteristic surface, apparatus freeze and ethics review.

## 1. Study identity

- preregistration version: {{preregistration_version}}
- study species: {{species}}
- laboratory / study site: {{study_site}}
- ethics / regulatory approval: {{ethics_approval}}
- planned study start: {{planned_start_date}}

## 2. Scientific question

Does contingent cue architecture change behavioral success when the physical cue environment is held constant?

The experiment compares two target mappings over the same four physical cue vectors:

| cue vector | routeable target | bypass target |
| --- | ---: | ---: |
| `000` | 0 | 1 |
| `001` | 1 | 0 |
| `011` | 0 | 0 |
| `111` | 1 | 1 |

The two architectures have the same four cue combinations, cue frequencies, cue costs, target balance, pairwise information surface and full cue-only joint distribution.

Exact structural costs:

- routeable: (C_A=2,;C_F=3);
- bypass control: (C_A=C_F=2).

## 3. Confirmatory hypotheses

For budget (B), define

[
Delta_B=
[p_{R,C,B}-p_{R,F,B}]
-
[p_{K,C,B}-p_{K,F,B}],
]

where (R) is routeable architecture, (K) is bypass control, (C) is contingent access and (F) is fixed access.

Primary confirmatory hypothesis:

[
H1:Delta_{B=2}>0.
]

Hierarchically gated secondary confirmatory hypothesis:

[
H2:
Delta_{B=2}
-rac12(Delta_{B=1}+Delta_{B=3})
>0.
]

H2 retains confirmatory status only if H1 passes the frozen two-sided inferential gate with the preregistered directional interpretation.

## 4. Experimental design

The primary design is a (2	imes2	imes3) between-subject factorial:

- architecture: routeable / bypass control;
- access: contingent / fixed;
- budget: (B=1,2,3).

Final randomized biological sample:

- individuals per cell: {{individuals_per_cell}}
- total randomized individuals: {{total_randomized_individuals}}
- colonies: {{colony_count}}
- trials per individual: {{trials_per_individual}}

The final allocation must come from the frozen operating-characteristic procedure documented in:

- `validation/routeability_glmm_operating_characteristic_gate_v1.json`;
- {{power_surface_reference}}.

External SESOI used for planning:

- H1 probability-scale SESOI: {{h1_sesoi}}
- H2 localization SESOI: {{h2_sesoi}}
- provenance: {{sesoi_provenance}}

The theoretical 0.25 information ceiling is not the behavioral effect size used for power.

## 5. Apparatus and cues

Apparatus: {{apparatus_description}}

Physical cue alphabet / materials: {{cue_alphabet_description}}

Frozen cue timing:

- nominal cue-stage duration: {{nominal_cue_duration_seconds}} s
- allowed duration tolerance: ±{{cue_duration_tolerance_seconds}} s
- response window: {{response_window_seconds}} s

The response window is frozen from the architecture-neutral procedural pilot:

- pilot receipt: {{pilot_receipt_reference}}

Contingent access uses context first, followed by the context-selected terminal cue while context remains visible.

Fixed access uses one terminal cue first, followed by the other terminal cue while the first remains visible. A→B versus B→A order is counterbalanced independently of state.

Thus the manipulation is not sequential versus simultaneous presentation.

## 6. Familiarization and training

Architecture-neutral familiarization: {{familiarization_protocol}}

After randomized assignment, each individual receives the same fixed architecture-specific full-information training dose:

- training blocks / trials: {{training_dose}}

There is no architecture-specific accuracy threshold for entry into the randomized primary test.

Architecture-specific training performance is recorded as a treatment-dependent diagnostic rather than used as an exclusion criterion.

## 7. Randomization and counterbalancing

Final schedule seed: {{randomization_seed}}

Schedule generator:

- `adaptive_gain/routeability_experiment_schedule.py`
- `examples/build_routeability_experiment_schedule.py`

Within each individual:

- every four-trial block contains all four cue states once;
- terminal physical positions are balanced;
- fixed cue order is balanced independently of state.

Across individuals within each treatment cell, cue-symbol mappings use the orthogonal profiles:

`000, 011, 101, 110`.

Colony allocation rule: {{colony_allocation_rule}}

## 8. Primary endpoint

Each initiated protocol-valid test trial is scored:

- 1 = correct accept/reject decision within the frozen response window;
- 0 = incorrect decision or no terminal decision before timeout.

Timeouts remain in the primary denominator.

Cue-presentation errors, apparatus errors or machine-detected protocol deviations are protocol-invalid rather than biological failures and are reported separately.

Trial validation is performed against the frozen schedule with:

- `adaptive_gain/routeability_trial_validation.py`.

## 9. Exclusions and missingness

Allowed biological-unit exclusions before / during test:

{{exclusion_rules}}

Not allowed:

- exclusion for low architecture-specific training accuracy;
- exclusion for low test accuracy;
- exclusion for slow but protocol-valid decisions;
- dropping timeout trials from the primary denominator.

All exclusions are reported by randomized treatment cell.

## 10. Primary statistical model

Primary family:

binomial logistic mixed model

[
	ext{success}
sim
	ext{architecture}	imes	ext{access}	imes	ext{categorical budget}
+
(1|	ext{individual})
+
(1|	ext{colony}),
]

with the colony term used when multiple colonies are represented.

Biological independent unit: individual forager.

Repeated unit: trial.

Alpha: 0.05, two-sided inferential test with preregistered directional interpretation.

Multiplicity: hierarchical H1 → H2 gatekeeping.

Probability-scale contrasts are population-averaged over the fitted random-intercept distribution according to the frozen operating-characteristic implementation.

## 11. Secondary endpoints

Prespecified secondary outcomes:

- conditional accuracy among trials with a terminal response;
- timeout / abandonment probability;
- decision latency after the final allowed cue;
- context-conditioned terminal-window choice in the autonomous-routing phase;
- learning slope across test trials.

Secondary outcomes do not replace the primary endpoint after outcome inspection.

## 12. Manipulation checks

Required checks:

1. cue-stage durations remain within frozen tolerance;
2. required context persists during terminal presentation;
3. state and reward frequencies match the schedule;
4. cue-symbol and physical-position counterbalancing is realized;
5. (B=3) confirms operational learnability under full information;
6. protocol-invalid trials are separated from biological failures.

## 13. Sample-size provenance

Procedural pilot nuisance receipt:

{{pilot_receipt_reference}}

SHA-256: `{{pilot_receipt_sha256}}`

Final operating-characteristic output:

{{power_surface_reference}}

SHA-256: `{{power_surface_sha256}}`

Final N decision rule:

{{final_n_decision_rule}}

The final N must be chosen from the preregistered robustness surface, not from the most favorable scenario.

## 14. Data and code freeze

Repository: `zuizui0223/adaptive-gain`

Frozen pre-collection commit: {{frozen_precollection_commit}}

Final schedule artifact: {{final_schedule_reference}}

SHA-256: `{{final_schedule_sha256}}`

Final stimulus artifact: {{final_stimulus_reference}}

SHA-256: `{{final_stimulus_sha256}}`

Any deviations from this preregistration are documented before opening the confirmatory treatment contrasts whenever possible.

## 15. Claim ceiling

A positive H1 with localized H2 would support a behavioral consequence of contingent information architecture in this controlled artificial-flower task.

It would not by itself establish that routeability explains natural-network rewiring, niche breadth, community stability or ecosystem function.
