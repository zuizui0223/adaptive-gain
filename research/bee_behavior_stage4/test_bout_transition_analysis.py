import unittest
from bout_transition_analysis import (
    EXPECTED_SOURCE_PREFIX, PHYSICAL_FLOWERS,
    parse_bouts, history_holdout_on_bouts
)

class OriginalBoutTransitionTests(unittest.TestCase):
    def fixture(self,bee_count=6,bouts_per_day=8,visits_per_bout=8):
        columns=list(EXPECTED_SOURCE_PREFIX)+[
            f"visit_slot_{i:03d}" for i in range(1,11)]
        out=[]
        for b in range(bee_count):
            for day in (1,2,3):
                for bout in range(bouts_per_day):
                    start=39000+bout*180+day*100
                    rec={"day":str(day),"bee":f"B{b}",
                         "foraging bout":str(bout+1),
                         "start_time":str(start),"end_time":str(start+100),
                         "duration":"100"}
                    # We repeat the same two flowers in deterministic alternation,
                    # so next physical flower is predictable beyond static margins.
                    values=[str(1+(idx%2)) for idx in range(visits_per_bout)]
                    for i in range(1,11):
                        rec[f"visit_slot_{i:03d}"]=values[i-1] if i<=len(values) else ""
                    out.append(rec)
        meta={"source_layout":"one_foraging_bout_per_row_ordered_unnamed_visit_slots",
              "columns":columns,"source_unnamed_ordered_visit_slots":10}
        return out,meta
    def test_one_source_csv_row_is_bout_not_visit(self):
        records,meta=self.fixture()
        bouts,audit=parse_bouts(records,meta)
        self.assertEqual(audit["source_original_bout_rows"],6*3*8)
        self.assertEqual(audit["original_recorded_total_visits"],6*3*8*8)
        self.assertEqual(audit["original_recorded_within_bout_transitions"],6*3*8*7)
        self.assertEqual(audit["distinct_bee_tags"],6)
        self.assertFalse(audit["social_displacement_outcomes_available"])
        self.assertFalse(audit["per_flower_precise_timestamp_available"])
    def test_heldout_history_signal_separate_trip_boundaries(self):
        records,meta=self.fixture()
        bouts,audit=parse_bouts(records,meta)
        result=history_holdout_on_bouts(bouts)
        self.assertEqual(result["status"],"FITTED_HELDOUT_BEHAVIORAL_DESCRIPTIVE")
        self.assertEqual(result["last_source_day_heldout"],3)
        self.assertEqual(result["heldout_within_bout_transitions_total"],6*8*7)
        self.assertGreater(result["mean_per_bee_gain_nats"],0)
        self.assertEqual(result["bees_with_positive_gain"],6)
        self.assertEqual(result["available_physical_flower_count"],10)
    def test_rare_bee_source_not_extrapolated_to_an_independent_colony(self):
        r,m=self.fixture(bee_count=3)
        b,a=parse_bouts(r,m)
        x=history_holdout_on_bouts(b)
        self.assertEqual(x["status"],"NO_GO_TOO_FEW_BEE_TAGS")
    def test_non_numeric_flower_field_does_not_get_guessed(self):
        r,m=self.fixture()
        r[0]["visit_slot_002"]="yellow"
        with self.assertRaisesRegex(ValueError,"NO_GO_VISIT_OUTSIDE"):
            parse_bouts(r,m)
    def test_middle_blank_does_not_erase_following_visits(self):
        r,m=self.fixture()
        r[0]["visit_slot_004"]=""
        with self.assertRaisesRegex(ValueError,"NO_GO_GAP"):
            parse_bouts(r,m)
    def test_reused_bee_day_bout_identifier_is_not_independent_trip(self):
        r,m=self.fixture()
        r[1]["foraging bout"]=r[0]["foraging bout"]
        with self.assertRaisesRegex(ValueError,"NO_GO_DUPLICATED_BOUT_ID"):
            parse_bouts(r,m)
    def test_original_experiment_wide_timestamp_larger_than_86400_is_valid(self):
        r,m=self.fixture()
        r[0]["start_time"]="380753"
        r[0]["end_time"]="380853"
        r[0]["duration"]="100"
        bouts,structure=parse_bouts(r,m)
        self.assertEqual(bouts[0]["start_time_seconds"],380753)

    def test_duration_inconsistency_is_reported_not_an_arrival_time(self):
        r,m=self.fixture()
        r[0]["duration"]="101"
        r[1]["duration"]="80"
        b,a=parse_bouts(r,m)
        self.assertEqual(a["duration_mismatch_gt1second_rows"],1)
        self.assertTrue(a["sequence_is_order_of_visits_within_each_bout_only"])

if __name__=="__main__":
    unittest.main()
