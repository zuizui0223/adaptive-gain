"""Source-free synthetic 72 individuals; no reported 2017 wind effects in tests."""
import unittest
from refit_2017_wind_bees_group_outcomes import GROUPS,ENDPOINTS,clean_original,describe

def fake():
    out=[]
    for j,(key,treat) in enumerate(GROUPS.items()):
        for i in range(18):
            out.append([treat,key,str(11+j*2+i%4),str(18+j*3+i%3),
                        str(13+j+i%3),"Colony-"+str(i%3),
                        "lav" if i%2==0 else "mint"])
    return out

class WindBackUpOriginal72BeeSourceGrainContracts(unittest.TestCase):
    def test_four_groups_have_18_individuals_each_and_no_cue_order(self):
        rows=clean_original(fake())
        report=describe(rows)
        self.assertEqual(report["source_authored_wind_bees"],72)
        for k in GROUPS:
            self.assertEqual(report["source_wind_treatment_groups"][k]["n_bees"],18)
        self.assertTrue(report["no_original_per_trial_cue_order_or_first_cue_policy"])
        self.assertTrue(report["no_measured_animal_pollen_or_plant_fitness"])
        self.assertTrue(report["no_wind_by_odor_by_visual_full_factorial_effect"])

    def test_only_observed_edges_not_full_factorial(self):
        q=describe(clean_original(fake()))
        d=q["published_reanalysis_original_four_arm_observed_edge_differences"]
        self.assertEqual(len(d),3)
        self.assertTrue(all(x["not_wind_by_visual_or_odor_factorial_interaction"]
                            for x in d.values()))
        self.assertAlmostEqual(d[ENDPOINTS[0]]["B_minus_A_wind_effect_odour_only"],2.0)

    def test_same_source_colony_only_sensitivity_not_paired_bee_or_causal(self):
        original=clean_original(fake())
        q=describe(original)
        # The synthetic fixture has colony 0/1/2 in all three A/B/C groups.
        self.assertEqual(set(q["original_colonies_shared_by_groups_A_B_C"]),
                         {"Colony-0","Colony-1","Colony-2"})
        self.assertFalse(q["original_source_group_D_has_no_common_colony_with_A_B_C"])
        for colony,receipt in q["original_colony_restricted_source_sensitivity"].items():
            self.assertEqual(set(receipt["group_source_summary"]),{"A","B","C"})
            self.assertTrue(receipt[
                "cannot_infer_original_randomization_within_source_colony"])
        self.assertTrue(q["colony_overlap_does_not_identify_first_cue_or_pollen"])

    def test_unshared_source_colony_D_detected_without_spurious_pairing(self):
        original=clean_original(fake())
        for row in original:
            if row["group"]=="D":
                row["colony_as_published"]="Different-colony"
        q=describe(original)
        self.assertTrue(q[
            "original_source_group_D_has_no_common_colony_with_A_B_C"])

    def test_missing_cell_remains_unknown_not_zero(self):
        raw=fake()
        raw[0][2]=""
        rows=clean_original(raw)
        report=describe(rows)
        self.assertEqual(report["source_wind_treatment_groups"]["A"]
            ["source_authored_endpoint_counts"][ENDPOINTS[0]]["n_observed"],17)

    def test_wrong_n_bad_group_and_noninteger_count_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"72_BEES"):
            clean_original(fake()[:-1])
        r=fake();r[1][1]="E"
        with self.assertRaisesRegex(ValueError,"GROUP_OR_COLONY"):
            clean_original(r)
        r=fake();r[1][3]="22.5"
        with self.assertRaisesRegex(ValueError,"COUNT_INVALID"):
            clean_original(r)

    def test_colony_difference_and_condition_mixing_blocked(self):
        r=fake();r[1][5]=""
        with self.assertRaisesRegex(ValueError,"GROUP_OR_COLONY"):
            clean_original(r)
        r=fake();r[0][0]="different_synthetic_condition"
        with self.assertRaisesRegex(ValueError,"TREATMENT_MIXED"):
            clean_original(r)

if __name__=="__main__":unittest.main()
