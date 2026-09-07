from adaptive_gain.automorphism import residual_automorphism_group
from adaptive_gain.core import adaptive_gain_receipt
from adaptive_gain.isomorphism_quotient import ResidualPairCoverInstance
from adaptive_gain.minimal_normal_form import minimal_strict_gain_standard_task
from adaptive_gain.pair_cover import pair_cover_audit


def _fixed_pair_instance(task):
    names = tuple(query.name for query in task.queries)
    lookup = {name: i for i, name in enumerate(names)}
    audit = pair_cover_audit(task)
    rows = []
    for row in audit.rows:
        mask = 0
        for name in row.separator_queries:
            mask |= 1 << lookup[name]
        rows.append(mask)
    return ResidualPairCoverInstance(
        tuple(query.cost for query in task.queries),
        tuple(rows),
        sum(query.cost for query in task.queries),
    )


def test_one_query_automorphism_orbit_can_still_require_all_physical_resources():
    task = minimal_strict_gain_standard_task()
    instance = _fixed_pair_instance(task)
    group = residual_automorphism_group(instance)
    audit = pair_cover_audit(task)
    costs = adaptive_gain_receipt(task)

    assert group.automorphism_count == 6
    assert group.query_orbits == ((0, 1, 2),)
    assert set(audit.globally_essential_queries) == {query.name for query in task.queries}
    assert costs.adaptive_cost == 2
    assert costs.fixed_cost == 3

    # All three resources are symmetry-equivalent as labels, but every one has a
    # private cross-target obligation.  Orbit membership therefore licenses
    # canonical renaming, not collapse to one reusable physical token.
    assert len(group.query_orbits[0]) == costs.fixed_cost
