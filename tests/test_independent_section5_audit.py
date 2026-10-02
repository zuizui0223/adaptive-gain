from adaptive_gain.independent_section5_audit import run_independent_section5_audit


def test_independent_section5_audit():
    receipt = run_independent_section5_audit()
    assert receipt.one_copy_entropy_vector_match
    assert receipt.one_copy_fixed_costs == (4, 4)
    assert receipt.one_copy_adaptive_costs == (4, 3)
    assert receipt.two_copy_entropy_vector_match
    assert receipt.two_copy_fixed_costs == (8, 8)
    assert receipt.two_copy_adaptive_costs == (8, 6)
    assert receipt.one_copy_worlds == 12
    assert receipt.two_copy_worlds == 144
    assert receipt.theorem_holds
