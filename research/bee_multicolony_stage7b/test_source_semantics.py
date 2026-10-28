import unittest
from source_semantics import read_source_records,source_semantics,KNOWN_COLUMNS

class NativeRoboticSourceSemanticTests(unittest.TestCase):
    def source(self):
        head=",".join(KNOWN_COLUMNS)
        rows=[
          ["E1","test","10:05:02","2.5","flower3","20220401","control","tent1","A","BLUE","L1","healthy"],
          ["E1","test","10:05:03","2.5","flower3","20220401","control","tent1","A","BLUE","L1","healthy"],
          ["E1","test","10:06:10","7.2","flower4","20220401","quercetin","tent1","B","YELLOW","L1","healthy"],
          ["E2","test","#N/A","#N/A","device","20220401","#N/A","tent2","#N/A","#N/A","#N/A","#N/A"],
          ["E3","test","12:05:45","255","flower7","20220402","quercetin","tent2","A","BLUE","R1","fungus"],
        ]
        return (head+"\n"+"\n".join(",".join(row) for row in rows)+"\n").encode()
    def test_original_source_event_and_colony_semantics(self):
        records=read_source_records(self.source())
        valid,a=source_semantics(records,"x=filter(data,prob<250)")
        self.assertEqual(a["source_original_rows"],5)
        self.assertEqual(a["source_record_valid_for_timestamp_and_id"],4)
        self.assertEqual(a["invalid_source_row_count"],1)
        self.assertEqual(a["valid_colonies"],2)
        self.assertEqual(a["source_prob_seconds_over250"],1)
        self.assertEqual(a["original_field_levels"]["colony"]["nunique"],3)
        self.assertTrue(a["source_data_firmly_colony_level_no_individual_tags"])
        self.assertEqual(a["colony_source_group_date_device_profile"]["L1"]["original_raw_sensor_events"],3)
    def test_header_changes_are_no_go(self):
        src=self.source().replace(b"experiment,name",b"bee_id,name")
        with self.assertRaisesRegex(ValueError,"HEADER_DRIFT"):
            read_source_records(src)
    def test_source_500ms_nearby_events_stay_distinct_before_policy(self):
        records=read_source_records(self.source())
        vals,a=source_semantics(records,"")
        same=[x for x in vals if x["colony"]=="L1" and x["Flower"]=="flower3"]
        self.assertEqual(len(same),2)
        self.assertEqual(abs(same[1]["seconds"]-same[0]["seconds"]),1)

if __name__=="__main__":
    unittest.main()
