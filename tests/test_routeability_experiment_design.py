from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "manuscript" / "ROUTEABILITY_EXPERIMENT_DESIGN_V1.md"


def _text() -> str:
    assert DOC.exists()
    return DOC.read_text(encoding="utf-8")


def test_experiment_design_freezes_exact_two_by_two_contrast():
    text = _text()
    for phrase in (
        "Primary 2 × 2 manipulation",
        "routeable",
        "matched bypass control",
        "contingent",
        "fixed",
        "1.00 | 0.75",
        "1.00 | 1.00",
        "25 percentage-point value is an information ceiling contrast",
    ):
        assert phrase in text


def test_experiment_design_targets_budget_window():
    text = _text()
    for phrase in (
        "B = 1 — below adaptive cost",
        "B = 2 — routeability-sensitive window",
        "B = 3 — above fixed cost",
        "`2 <= 2 < 3`",
        "budget-window localization",
        "| B=1 | 0.00 |",
        "| B=2 | 0.25 |",
        "| B=3 | 0.00 |",
    ):
        assert phrase in text


def test_experiment_design_uses_individual_not_trial_as_unit():
    text = _text()
    assert "independent biological unit is the individual forager" in text
    assert "Trials are repeated observations, not independent animals." in text
    assert "Do not report trial count as the biological sample size." in text


def test_experiment_design_keeps_claim_ceiling():
    text = _text()
    for phrase in (
        "Do not require the observed interaction to equal 0.25.",
        "A failed behavioral experiment does not falsify the exact finite theorem.",
        "would not by itself establish that routeability explains natural plant-pollinator network rewiring",
    ):
        assert phrase in text


def test_experiment_design_uses_persistent_context_and_timing_controls():
    text = _text()
    for phrase in (
        "while the context remains visible",
        "persistent-context rule",
        "fragile delayed-context memory",
        "Cue timing and persistence must therefore be matched",
        "pretested for discriminability",
    ):
        assert phrase in text


def test_experiment_design_separates_guided_and_autonomous_routing():
    text = _text()
    for phrase in (
        "Phase 1 — guided contingent presentation",
        "Phase 2 — autonomous routing",
        "context = 0 → inspect terminal B",
        "context = 1 → inspect terminal A",
        "policy-learning or action-selection bottleneck",
    ):
        assert phrase in text


def test_experiment_design_matches_pairwise_information_not_just_marginals():
    text = _text()
    for phrase in (
        "Stronger match: pairwise information is also identical",
        "same **pairwise mutual information**",
        "higher-order conditional organization",
        "not reducible to how informative individual cues are",
        "Fixed semantic 0/1 labels are not claimed to have identical signed contingency tables",
    ):
        assert phrase in text


def test_experiment_design_blocks_post_randomization_training_selection():
    text = _text()
    for phrase in (
        "fixed amount",
        "Do not require an architecture-specific accuracy threshold",
        "part of the randomized biological response",
        "per-protocol",
        "Differential training completion or non-response",
    ):
        assert phrase in text
    assert "failure to meet a prespecified training criterion" not in text


def test_experiment_design_keeps_timeout_trials_in_primary_endpoint():
    text = _text()
    for phrase in (
        "within a frozen response window",
        "incorrect decision **or no terminal decision before timeout**",
        "remain in the primary denominator",
        "must not condition on having produced a response",
        "conditional choice accuracy among trials with a terminal response",
    ):
        assert phrase in text


def test_experiment_design_separates_pilot_nuisance_from_focal_power_target():
    text = _text()
    for phrase in (
        "ROUTEABILITY_PROCEDURAL_PILOT_V1.md",
        "The pilot is not permitted to estimate H1, H2",
        "externally justified probability-scale SESOI",
        "not labelled the final powered N",
        "The focal architecture × access effect never feeds backward into its own sample-size target.",
    ):
        assert phrase in text


def test_experiment_design_reuses_identical_physical_cue_surface():
    text = _text()
    for phrase in (
        "same four cue combinations in both architecture groups",
        "Only `000` and `001` change reward / accept–reject assignment.",
        "physical environmental cue surface is held fixed",
        "focal action map changes",
    ):
        assert phrase in text


def test_experiment_design_matches_sequential_timing_across_access_arms():
    text = _text()
    for phrase in (
        "The first terminal cue remains visible while the second is presented",
        "not sequential versus simultaneous presentation",
        "Both arms receive two sequentially staged observations",
        "stage durations and cue-persistence rules are matched",
    ):
        assert phrase in text
