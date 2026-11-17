"""Mock-only source-free Stage71C null score and fragility checks."""
import importlib.util,unittest
from pathlib import Path
p=Path(__file__).with_name("compare_original_uv_vs_identified_bees_null_score.py")
spec=importlib.util.spec_from_file_location("s71c",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def r(tax,uv,vis,b,o):
    return {
      "Study_id":"study1","Network_id":"network1","Year":"2021",
      "original_plant_species":tax,
      m.UV:str(uv),m.VISIBLE:str(vis),
      m.Y_B:str(b),m.Y_O:str(o),m.Y_N:str(b+o),
      "source_sampling_method":"Transect"
    }

class Stage71NullScoreGuards(unittest.TestCase):
    def test_higher_uv_bombus_positive_score(self):
        row,why=m.network_score([
          r("sp1",2,20,1,9),r("sp2",10,50,9,1)],1)
        self.assertEqual(why,"INFORMATIVE_NULL_SCORE")
        self.assertGreater(row["null_score_UV_per_10pct_points"],0)
        self.assertGreater(row["null_information_UV_per_10pct_points"],0)

    def test_reverse_direction_signed(self):
        row,why=m.network_score([
          r("sp1",2,20,9,1),r("sp2",10,50,1,9)],1)
        self.assertEqual(why,"INFORMATIVE_NULL_SCORE")
        self.assertLess(row["null_score_UV_per_10pct_points"],0)

    def test_both_guild_same_all_study_no_eligible_biological_false_absence(self):
        row,why=m.network_score([
          r("sp1",2,20,0,3),r("sp2",10,50,0,3)],1)
        self.assertIsNone(row)
        self.assertEqual(why,"SINGLE_RECORDED_BEE_GUILD")

    def test_no_uv_variation_unidentified(self):
        row,why=m.network_score([
          r("sp1",5,20,9,1),r("sp2",5,50,1,9)],1)
        self.assertIsNone(row)
        self.assertEqual(why,"NO_ORIGINAL_UV_VARIATION_AMONG_BEE_RECORDED_PLANTS")

    def test_low_visits_only_secondary_filter(self):
        row,why=m.network_score([
          r("sp1",2,20,1,0),r("sp2",10,50,0,1)],3)
        self.assertIsNone(row)
        self.assertEqual(why,"FEWER_THAN_TWO_BEE_OBSERVED_PLANTS")
        row,why=m.network_score([
          r("sp1",2,20,1,0),r("sp2",10,50,0,1)],1)
        self.assertEqual(why,"INFORMATIVE_NULL_SCORE")

    def test_invalid_guild_sum_rejected(self):
        a=r("sp1",2,20,2,3);a[m.Y_N]="1"
        with self.assertRaisesRegex(ValueError,"INVALID_OR_UNDERREPORTED_BEES"):
            m.network_score([a,r("sp2",10,50,1,1)],1)

    def test_study_one_out_not_counted_as_30_independent_sources(self):
        one,_=m.network_score([r("sp1",2,20,1,9),r("sp2",10,50,9,1)],1)
        one["Study_id"]="s1"
        two=dict(one);two["Study_id"]="s2";two["Network_id"]="n2"
        out,by_study=m.null_score_summary([one,two])
        self.assertEqual(out["informative_networks"],2)
        self.assertEqual(out["informative_studies"],2)
        self.assertEqual(len(by_study),2)
        self.assertIsNone(out.get("p_value"))

if __name__=="__main__":unittest.main()
