"""Regression: ecological opportunity can change while decision topology stays fixed.

These tests audit the deterministic guaranteed-resolution case only; they do
not treat changed ecological deadlines as evidence of altered cue partitions.
"""

from adaptive_gain.core import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
)


def four_world_private_pair_task() -> FiniteTask:
    return FiniteTask(
        worlds=(
            World("w0", 0),
            World("w1", 1),
            World("w2", 1),
            World("w3", 0),
        ),
        queries=(
            Query("root", 1, (0, 0, 1, 1)),
            Query("left", 1, (0, 1, 0, 0)),
            Query("right", 1, (0, 0, 0, 1)),
        ),
    )


def deterministic_opportunity_gain(adaptive_cost: int, fixed_cost: int, budget: int) -> int:
    return int(budget >= adaptive_cost) - int(budget >= fixed_cost)


def test_private_pair_topology_is_two_vs_three():
    task = four_world_private_pair_task()
    receipt = adaptive_gain_receipt(task)
    assert receipt.adaptive_cost == 2
    assert receipt.fixed_cost == 3
    assert receipt.strict_adaptive_gain


def test_opportunity_change_reverses_selection_without_structural_change():
    receipt = adaptive_gain_receipt(four_world_private_pair_task())
    assert receipt.adaptive_cost is not None
    assert receipt.fixed_cost is not None
    gains = [
        deterministic_opportunity_gain(receipt.adaptive_cost, receipt.fixed_cost, budget)
        for budget in (1, 2, 3)
    ]
    assert gains == [0, 1, 0]
    maintenance_cost = 0.2
    net = [gain - maintenance_cost for gain in gains]
    assert net == [-0.2, 0.8, -0.2]
    assert [value > 0 for value in net] == [False, True, False]


def test_species_label_replacement_alone_preserves_declared_decision_task():
    task = four_world_private_pair_task()
    renamed = FiniteTask(
        worlds=tuple(World("replacement_" + w.name, w.target) for w in task.worlds),
        queries=task.queries,
    )
    original = adaptive_gain_receipt(task)
    replacement = adaptive_gain_receipt(renamed)
    assert (original.adaptive_cost, original.fixed_cost) == (
        replacement.adaptive_cost,
        replacement.fixed_cost,
    )


def test_extension_explicitly_prohibits_budget_topology_conflation():
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "manuscript" / "ECOLOGICAL_NOVELTY_EXTENSION_V1.md"
    contents = path.read_text(encoding="utf-8")
    for phrase in (
        "Fixed topology, changing ecological opportunity: a separating witness",
        "value-layer change",
        "with zero compositional and zero decision-structural turnover",
        "Do not treat a changed ecological budget or reward as evidence",
        "accounting for detectability",
    ):
        assert phrase in contents
