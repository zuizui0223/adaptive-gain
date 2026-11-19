"""Stage94B source-only join guards: no data leaks or false zeroes."""
import tempfile,unittest,zipfile
from pathlib import Path
from real_source_mainland_three_cue_support import read_derived_zip,merge,summary_for

def fixture():
    a={};b={};g={};s={}
    for i in range(367):
        code=f"R{i:03d}"
        a[code]={"n_native":"100","n_mark_positive_source_only":"12","n_marking_positive_genera":"3"}
        b[code]={"n_original_WCVP_native_species_in_region":"100",
          "n_original_AusTraits_flower_diameter_species":"5",
          "n_distinct_source_diameter_genera":"4",
          "n_diameter_species_GIFT_animal":"2","n_diameter_species_GIFT_wind":"0",
          "n_diameter_species_GIFT_UNKNOWN":"3"}
        scope="island" if i==0 else ("mixed" if i==1 else "mainland")
        g[code]={"land_scope":scope}
        if scope=="mainland":s[code]={"shared_split":"exploration","spatial_block_id":"B1"}
    return a,b,g,s

class Stage94B(unittest.TestCase):
    def test_original_367_and_exclude_islands(self):
        a,b,g,s=fixture();rows,blocks=merge(a,b,g,s)
        self.assertEqual(len(rows),367)
        self.assertEqual(len([r for r in rows if r["shared_split"]=="exploration"]),365)
        self.assertEqual(rows[0]["shared_split"],"excluded")
        self.assertEqual(rows[1]["shared_split"],"excluded")
        self.assertTrue(all(r["mainland_gust_flower_effect_fitted"]=="NO" for r in rows))
        self.assertEqual(blocks,{"B1":"exploration"})
    def test_reject_wrong_spatial_source_universe(self):
        a,b,g,s=fixture();a.pop("R366")
        with self.assertRaises(ValueError):merge(a,b,g,s)
    def test_reject_island_admitted_to_holdout(self):
        a,b,g,s=fixture();s["R000"]={"shared_split":"holdout","spatial_block_id":"B2"}
        with self.assertRaises(ValueError):merge(a,b,g,s)
    def test_reject_repeated_block_across_holdout(self):
        a,b,g,s=fixture();s["R100"]={"shared_split":"holdout","spatial_block_id":"B1"}
        with self.assertRaises(ValueError):merge(a,b,g,s)
    def test_reject_original_source_diameter_unit_denominator_drift(self):
        a,b,g,s=fixture();b["R200"]["n_original_WCVP_native_species_in_region"]="99"
        with self.assertRaises(ValueError):merge(a,b,g,s)
    def test_source_size_mode_count_is_conserved(self):
        a,b,g,s=fixture();b["R200"]["n_diameter_species_GIFT_wind"]="1"
        with self.assertRaises(ValueError):merge(a,b,g,s)
    def test_source_five_species_not_misreported_as_ten(self):
        a,b,g,s=fixture();rows,_=merge(a,b,g,s)
        sm=summary_for([r for r in rows if r["shared_split"]=="exploration"])
        self.assertEqual(sm["n_true_AusTraits_LABELLED_flower_diameter_species_regions_at_least_10"],0)
        self.assertEqual(sm["n_positive_marking_TEXT_SOURCE_CANDIDATES_regions_at_least_10"],365)
    def test_fake_source_zip_rejected_before_read(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("data.csv","TDWG_L3\nAAA\n")
            with self.assertRaises(ValueError):
                read_derived_zip(p,"f"*64,"data.csv")

if __name__=="__main__":unittest.main()
