from pathlib import Path

from adaptive_gain.ecological_routeability_experiment import (
    bypass_matched_control_task,
    ecological_routeability_experiment_contrast,
    pairwise_information_signature,
)
from adaptive_gain.minimal_normal_form import minimal_strict_gain_standard_task

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "theory" / "PAIRWISE_INFORMATION_ROUTEABILITY_NONIDENTIFIABILITY.md"


def test_pairwise_information_nonidentifiability_witness_is_exact():
    routeable = minimal_strict_gain_standard_task()
    control = bypass_matched_control_task()
    receipt = ecological_routeability_experiment_contrast()

    assert pairwise_information_signature(routeable) == pairwise_information_signature(control)
    assert receipt.routeable_adaptive_cost == receipt.control_adaptive_cost == 2
    assert receipt.routeable_fixed_cost == 3
    assert receipt.control_fixed_cost == 2
    assert receipt.routeable_strict_gain
    assert not receipt.control_strict_gain


def test_pairwise_information_nonidentifiability_document_keeps_novelty_boundary():
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "pairwise information is insufficient to identify routeability",
        "No novelty is claimed for that generic fact",
        "same full named pairwise-information surface",
        "Physical cue salience, timing and learned symbol meaning still require counterbalancing",
    ):
        assert phrase in text


def test_pairwise_information_nonidentifiability_document_does_not_overclaim():
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "pairwise mutual information is generally useless",
        "generic higher-order information or synergy is new",
        "weak pairwise association in natural data implies routeability",
        "symbolic information matching automatically matches animal perceptual salience",
    ):
        assert phrase in text


def test_relational_witness_holds_physical_cue_surface_fixed():
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "Relationality witness — same physical environment, different focal action map",
        "same four physical cue combinations",
        "Only two cue vectors change target assignment.",
        "same environmental cue distribution",
        "The relevant object is the environment together with the focal action map.",
    ):
        assert phrase in text
