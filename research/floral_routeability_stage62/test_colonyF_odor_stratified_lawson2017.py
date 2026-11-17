"""Fake 72 bee rows only; never present constructed data as original Lawson results."""
import unittest
from collections import Counter
from colonyF_odor_stratified_lawson2017 import (
    audit,exact_reference,_weight_and_stats,_selected,
    EXPECTED_GROUP_ODOR,EXPECTED_GROUP_N,ODORS
)

def invented_bees():
    samples=[]
    for index,g in enumerate(("A","B","C","D")):
        f_n=EXPECTED_GROUP_N.get(g,0)
        odours=sum(([k]*n for k,n in EXPECTED_GROUP_ODOR.get(g,{}).items()),[])
        assert len(odours)==f_n
        for i in range(18):
            in_f=i<f_n
            scent=(odours[i] if in_f else ("no scent" if g=="D"
                        else "lav" if i%2==0 else "mint"))
            samples.append({
              "group":g,
              "colony_as_published":"F" if in_f else "OTHER-"+g,
              "reward_scent_as_published":scent,
              "visits_to_learning_criterion":24 + index*3 + i%7,
              "correct_choices_after_landing_count":35 - index*2 -i%3,
              "rewarding_flower_landings_count":20 + index+i%5,
            })
    return samples

class OriginalLawson2017FColonyOdorContracts(unittest.TestCase):
    def test_original_source_F_odor_counter_and_exact_two_reference_space_sizes(self):
        rows=invented_bees()
        out=audit(rows)
        self.assertEqual(out["n_source_F_bees_A_B_C"],29)
        a=out["observational_comparisons"]
        self.assertEqual(a["A_to_B"]["original_endpoints"][
            "visits_to_learning_criterion"][
            "source_odor_constrained_hypothetical_label_reassignment_count"],17820)
        self.assertEqual(a["B_to_C"]["original_endpoints"][
            "visits_to_learning_criterion"][
            "source_odor_constrained_hypothetical_label_reassignment_count"],3465)
        self.assertEqual([a["A_to_B"]["n_bees_left"],
                         a["A_to_B"]["n_bees_right"]],[11,10])
        self.assertEqual([a["B_to_C"]["n_bees_left"],
                         a["B_to_C"]["n_bees_right"]],[10,8])
        self.assertTrue(out["no_real_p_value_or_replicated_colony_inference"])
        self.assertTrue(out["no_2017_per_bee_cue_order_decision_route_measurement"])

    def test_same_outcome_all_bees_yields_exact_zero_every_reassignment(self):
        rows=invented_bees()
        for r in rows:
            for k in ("visits_to_learning_criterion",
                      "correct_choices_after_landing_count",
                      "rewarding_flower_landings_count"):
                r[k]=18
        out=audit(rows)
        for group in out["observational_comparisons"].values():
            for x in group["original_endpoints"].values():
                self.assertEqual(x["source_F_odor_pool_standardized_mean_right_minus_left"],0)
                self.assertEqual(x["reference_2p5_percentile_not_confidence_bound"],0)
                self.assertEqual(x["reference_97p5_percentile_not_confidence_bound"],0)
                self.assertTrue(x["stratified_reassignment_NOT_randomized_p_value"])

    def test_source_odor_imbalance_and_missing_original_endpoint_refused(self):
        rows=invented_bees()
        for r in rows:
            if r["colony_as_published"]=="F" and r["group"]=="B":
                r["reward_scent_as_published"]=(
                    "mint" if r["reward_scent_as_published"]=="lav" else "lav")
                break
        with self.assertRaisesRegex(ValueError,"BY_ODOR_COVERAGE"):
            _selected(rows)
        rows=invented_bees()
        rows[0]["visits_to_learning_criterion"]=None
        with self.assertRaisesRegex(ValueError,"MISSING_ENDPOINT"):
            _selected(rows)

    def test_all_bees_72_source_required_and_group_F_missing(self):
        rows=invented_bees()
        with self.assertRaisesRegex(ValueError,"72_BEE_FRAME"):
            audit(rows[:-1])
        rows=invented_bees()
        rows[0]["colony_as_published"]="not_F"
        with self.assertRaisesRegex(ValueError,"BY_ODOR_COVERAGE"):
            audit(rows)

    def test_standardization_equal_observed_difference_when_no_scent_imbalance(self):
        rows=invented_bees()
        data=[r for r in rows if r["colony_as_published"]=="F"
              and r["group"] in ("B","C")]
        observed,parts=_weight_and_stats(data,"B","C",
                          "correct_choices_after_landing_count")
        self.assertEqual(set(parts),set(ODORS))
        check=sum((parts[s]["right_minus_left_float"]*
                   (parts[s]["n_left"]+parts[s]["n_right"]))
                  for s in ODORS) / len(data)
        self.assertAlmostEqual(check,float(observed),12)
if __name__=="__main__":
    unittest.main()
