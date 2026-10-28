import random
import unittest
from collections import Counter
from datetime import datetime,timedelta

from colony_temporal_persistence import (
    BIN_SECONDS,MIN_BIN_VISITS,
    conditional_temporal_test,prepare_hours,qualified_colonies,
    _shuffle_source_hour,_smooth_share
)

def synthetic_colony_events(colonies=8,skip_slots=(),stable=False,hours=1):
    rows=[]
    day=datetime(2022,4,1,11,0,0)
    for c in range(colonies):
        for hour_offset in range(hours):
            for slot in range(12):
                if slot in skip_slots:continue
                for visit in range(5):
                    if stable:
                        nectar="quercetin" if visit<2 else "control"
                    else:
                        nectar="control" if slot<6 else "quercetin"
                    stamp=day+timedelta(hours=hour_offset,minutes=5*slot,
                                        seconds=visit+3)
                    rows.append({
                        "colony":f"C{c}","day":stamp.date().isoformat(),
                        "timestamp_local":stamp,"nectar":nectar,
                        "flower_id":2 if nectar=="quercetin" else 3})
    return rows

class IndependentColonyTemporalTests(unittest.TestCase):
    def test_locked_5min_bin_adjacency(self):
        src=synthetic_colony_events(colonies=1,skip_slots=(4,5))
        hours,receipt=prepare_hours(src,required_events=None)
        self.assertEqual(len(hours),1)
        self.assertEqual(receipt["eligible_adjacent_5minute_pairs_all_colonies"],8)
        self.assertEqual(hours[0]["pair_indices"],(
            (0,1),(1,2),(2,3),(6,7),(7,8),(8,9),(9,10),(10,11)))
    def test_gap_never_crosses_hour_or_day(self):
        src=synthetic_colony_events(colonies=1,hours=2)
        hours,receipt=prepare_hours(src,required_events=None)
        self.assertEqual(len(hours),2)
        self.assertEqual(receipt["eligible_adjacent_5minute_pairs_all_colonies"],22)
        self.assertEqual(sum(len(x["pair_indices"]) for x in hours),22)
    def test_nonempty_local_cluster_has_positive_permutation_smoothness_signal(self):
        src=synthetic_colony_events(colonies=8)
        result=conditional_temporal_test(src,required_events=None,
                                         permutations=99,seed=42)
        self.assertEqual(result["status"],"COMPUTED_COLONY_LEVEL_WITHIN_HOUR_TEMPORAL_PERSISTENCE")
        self.assertEqual(result["admission"]["eligible_source_colonies"],8)
        t=result["observed_vs_conditional_null"]
        self.assertGreater(t["extra_local_smoothness_null_minus_observed_D"],0.2)
        self.assertLessEqual(t["one_tailed_Monte_Carlo_p_for_temporal_smoothness"],0.02)
        self.assertEqual(t["source_colonies_with_positive_local_smoothness"],8)
    def test_time_constant_reward_fraction_has_no_spurious_local_effect(self):
        src=synthetic_colony_events(colonies=8,stable=True)
        result=conditional_temporal_test(src,required_events=None,
                                         permutations=19,seed=9)
        self.assertEqual(result["status"],"COMPUTED_COLONY_LEVEL_WITHIN_HOUR_TEMPORAL_PERSISTENCE")
        score=result["observed_vs_conditional_null"]
        self.assertAlmostEqual(score["observed_equal_colony_mean_D"],0)
        self.assertAlmostEqual(score["extra_local_smoothness_null_minus_observed_D"],0)
        self.assertEqual(score["one_tailed_Monte_Carlo_p_for_temporal_smoothness"],1)
    def test_no_go_fewer_independent_colonies(self):
        src=synthetic_colony_events(colonies=7)
        result=conditional_temporal_test(src,required_events=None,
                                         permutations=5)
        self.assertEqual(result["status"],"NO_GO_COLONY_LEVEL_HOUR_MATCHING")
        self.assertEqual(result["admission"]["eligible_source_colonies"],7)
        self.assertNotIn("observed_vs_conditional_null",result)
    def test_permutation_preserves_hour_exact_n_q_and_flower_bag(self):
        src=synthetic_colony_events(colonies=1,skip_slots=(3,8))
        hs,_=prepare_hours(src,required_events=None)
        h=hs[0]
        moved=_shuffle_source_hour(h,random.Random(29))
        good=h["eligible_positions"]
        self.assertEqual(
            sorted((h["bins"][i]["n"],h["bins"][i]["q"],
                    tuple(sorted(h["bins"][i]["devices"].items()))) for i in good),
            sorted((moved[i]["n"],moved[i]["q"],
                    tuple(sorted(moved[i]["devices"].items()))) for i in good))
        self.assertEqual([i for i,b in enumerate(moved) if b["n"]<3],
                         [i for i,b in enumerate(h["bins"]) if b["n"]<3])
        self.assertEqual(len(h["pair_indices"]),sum(
            1 for i in range(11)
            if moved[i]["n"]>=3 and moved[i+1]["n"]>=3))
    def test_n_q_not_ever_an_individual_bee_id(self):
        src=synthetic_colony_events(colonies=8)
        a=conditional_temporal_test(src,required_events=None,
                                    permutations=1,seed=0)
        self.assertTrue(a["not_individual_bee_routes_or_visual_flower_perception"])
        self.assertEqual(a["original_source_grain"]["source_original_distinct_colonies"],8)
        self.assertEqual(a["original_source_grain"]["source_processed_robotic_events"],len(src))
    def test_source_count_and_treatment_contract_fail_closed(self):
        src=synthetic_colony_events(colonies=8)
        with self.assertRaisesRegex(ValueError,"NO_GO_PUBLISHED_PROCESSED_EVENT_COUNT"):
            prepare_hours(src,required_events=54362)
        src[0]["nectar"]="unknown"
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_ROBOTIC_SOURCE_FIELDS_INVALID"):
            prepare_hours(src,required_events=None)

if __name__=="__main__":
    unittest.main()
