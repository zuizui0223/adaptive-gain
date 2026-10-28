import unittest
from reproduce_original_sensor_cleaning import build_original_clustered_events
from source_semantics import KNOWN_COLUMNS

class SourceAuthorSensorCleaningTests(unittest.TestCase):
    def row(self,flower="flower3",time="10:05:00",prob="2",
            experiment="1",colony="L1",nectar="CONTROL",date="20220401"):
        return dict(zip(KNOWN_COLUMNS,[
            experiment,"RobotFile",time,prob,flower,date,nectar,
            "L","A","BLUE",colony,"Healthy"
        ]))
    def test_source_same_device_gap_from_previous_end_le2_merges(self):
        a=self.row(time="10:05:00",prob="2")
        b=self.row(time="10:05:03",prob="2") # gap 1 second
        c=self.row(time="10:05:09",prob="1") # gap 4 sec
        events,receipt=build_original_clustered_events([a,b,c])
        self.assertEqual(len(events),2)
        self.assertEqual(receipt["source_2second_clusters_before_probing_bounds"],2)
        self.assertEqual(receipt["source_exact_duplicate_rows"],0)
        self.assertEqual(events[0]["probing_seconds"],5)
        self.assertEqual(events[0]["original_sensor_rows_collapsed"],2)
        self.assertEqual(events[1]["probing_seconds"],1)
    def test_distinct_robot_flower_repeated_sensor_not_independent_honeybee(self):
        a=self.row(flower="flower3",time="10:05:00")
        b=self.row(flower="flower4",time="10:05:01")
        events,receipt=build_original_clustered_events([a,b])
        self.assertEqual(len(events),2)
        self.assertEqual({x["flower_id"] for x in events},{3,4})
        self.assertTrue(receipt["requires_explicit_individual_animal_identifier_for_route_replication"])
    def test_original_exact_duplicate_and_strict250_filter(self):
        a=self.row(time="10:05:00",prob="250")
        b=self.row(time="10:09:00",prob="1")
        c=self.row(time="10:10:00",prob="0")
        result,receipt=build_original_clustered_events([a,a,b,c])
        self.assertEqual(receipt["source_exact_duplicate_rows"],1)
        self.assertEqual(receipt["after_original_R_distinct_and_drop_na"],3)
        self.assertEqual(len(result),1)
        self.assertEqual(receipt["source_over_250_or_nonpositive_cluster_count"],2)
    def test_source_cross_colony_collision_fails_audit_not_invented(self):
        a=self.row(time="10:00:00",prob="2",colony="L1")
        b=self.row(time="10:00:04",prob="2",colony="R1")
        result,receipt=build_original_clustered_events([a,b])
        self.assertEqual(receipt["experiment_flower_group_cross_colony_count"],1)
        self.assertEqual(receipt["multiple_colony_in_merged_cluster_count"],0)
    def test_filter_nonempty_source_rows_with_na(self):
        a=self.row()
        b=self.row(time="#N/A",flower="device")
        events,receipt=build_original_clustered_events([a,b])
        self.assertEqual(len(events),1)
        self.assertEqual(receipt["after_original_R_distinct_and_drop_na"],1)

if __name__=="__main__":
    unittest.main()
