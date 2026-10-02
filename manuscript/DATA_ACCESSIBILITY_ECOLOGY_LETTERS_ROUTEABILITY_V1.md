# Data accessibility statement — Ecology Letters routeability v1

The mathematical constructions, exact certificates, validation receipts,
public-data reanalysis code and figure-source files supporting this study are
contained in the `adaptive-gain` repository. Before final submission, the
exact submitted repository state will be deposited in a permanent archive and
the resulting DOI will be inserted here.

The empirical-convergence section reanalyses or summarizes previously public
*Bombus* data. No new animal data were collected for this study.

## Yuan et al. 2026

Active-information-seeking trial data were obtained from the public repository

`Cuixiaojian21/bee_metacognition`

at source commit

`7f886394b4de872ecdb19ca4ea214ec321d5dce9`.

The reanalysis uses

`data/4_active_information_seeking_trials.csv`

with source blob SHA

`26259c9071c6d73141d56b9bedd396cab1a04491`.

The frozen raw-data aggregation and access-mode interaction used in the
manuscript are recorded in:

- `validation/bombus_public_data_component_receipt_v1.json`;
- `validation/yuan_free_cue_acquisition_interaction_v1.json`;
- `validation/bombus_empirical_convergence_panel_v1.json`.

## Independent theorem verification

The complete-Shannon-equivalence theorem was also reimplemented independently
of the repository's main finite-task solver and information helpers. The
separate audit rebuilds the literal one-copy and two-copy tasks and recomputes
the exact entropy fingerprints and minimax costs:

- `adaptive_gain/independent_section5_audit.py`;
- `tests/test_independent_section5_audit.py`;
- `validation/independent_section5_audit_v1.json`.

The nonlinear eco-evolutionary no-go is separately executable and certified in:

- `adaptive_gain/nonlinear_feedback_reachability.py`;
- `tests/test_nonlinear_feedback_reachability.py`;
- `validation/nonlinear_lipschitz_no_go_v2.json`.

## Spaethe et al. 2026

Individual cue-conflict values were reconstructed from the authors' public
analysis repository:

`stoeckl-lab/Spaethe_et_al_2024_beeDecisions`.

Archived code release:
Zenodo DOI **10.5281/zenodo.15911965**.

The prospectively defined secondary-cue recruitment analysis is implemented in:

- `adaptive_gain/bumblebee_public_bridge.py`;
- `tests/test_bumblebee_public_bridge.py`.

## MaBouDi et al. 2025

Public behavioural trajectories and analysis materials are archived at
Figshare DOI **10.15131/shef.data.14185865.v1**.

These data are used as external mechanistic support for selective sequential
sensory sampling; no new pooled effect size is computed in the main
quantitative panel.

## Chow et al. 2022

Public match-to-sample/tool-selection data are archived at
Dryad DOI **10.5061/dryad.tqjq2bw36**.

These data are used as external support for context-conditioned action mapping.

## Essenberg et al. 2015

The published experiment is cited as the closest biological precedent for
branch-specific cue relevance. No reusable public raw table for this study was
located or reanalysed, and no numerical effect from this study enters the main
public-data panel.

## Code archive — required before submission

Replace this paragraph at finalization with:

> Code and exact computational materials are archived at [PERMANENT DOI].
> The submitted manuscript corresponds to Git commit [SUBMITTED COMMIT SHA].

Do not submit with the placeholder unresolved.
