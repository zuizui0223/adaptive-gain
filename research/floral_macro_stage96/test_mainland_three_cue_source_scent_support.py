"""Stage96 guards: false scent negatives, no island leakage, no source swap."""
import tempfile,unittest,zipfile
from pathlib import Path
from mainland_three_cue_source_scent_support import count,join,open_zip

def fixture():
    a={};b={}
    for k in range(367):
        key=f"X{k:03d}"
        island=k>=125 and k<245
        mixed=k>=245
        scope="island" if island else "mixed" if mixed else "mainland"
        fold="exploration" if k<88 else "holdout" if k<125 else "excluded"
        a[key]={"TDWG_L3":key,"n_native_source_species":"200",
            "source_geographic_scope":scope,"shared_split":fold,
            "spatial_block_id":"blockA" if k<88 else "blockB" if k<125 else "",
            "n_positive_marking_TEXT_SOURCE_CANDIDATES":"12",
            "n_true_AusTraits_LABELLED_flower_diameter_species":"10"}
        b[key]={"TDWG_L3":key,"n_native":"200","n_full_original_flora_descriptions":"100",
            "n_flora_scent_positive_SOURCE_CANDIDATE":"12",
            "n_flora_scent_explicit_negative_SOURCE_CANDIDATE":"3",
            "n_flora_scent_unmentioned_NOT_negative":"85",
            "n_flora_scent_conflict":"0",
            "n_source_scent_positive_GIFT_animal":"2",
            "n_source_scent_positive_GIFT_wind":"0",
            "n_source_scent_positive_GIFT_unknown":"10",
            "n_scent_positive_distinct_genera":"5"}
    return a,b

class Source96Guard(unittest.TestCase):
    def test_original_367_and_three_cue_coverage_consistent(self):
        a,b=fixture();rows=join(a,b)
        self.assertEqual(len(rows),367)
        self.assertEqual(len([r for r in rows if r["shared_split"]=="holdout"]),37)
        self.assertEqual(count([r for r in rows if r["shared_split"]=="holdout"])["regions_three_distinct_cue_source_counts_ge10_each"],37)
    def test_negative_and_unknown_separate(self):
        a,b=fixture();r=join(a,b)[0]
        self.assertEqual(r["n_source_floral_fragrance_lexical_explicit_negative"],3)
        self.assertEqual(r["n_source_floral_fragrance_lexical_undocumented"],85)
    def test_unnatural_geo_join_refused(self):
        a,b=fixture();a.pop("X366")
        with self.assertRaises(ValueError):join(a,b)
    def test_unverified_negative_never_assigned(self):
        a,b=fixture()
        b["X100"]["n_flora_scent_unmentioned_NOT_negative"]="84"
        with self.assertRaises(ValueError):join(a,b)
    def test_gift_mode_source_margins_conserved(self):
        a,b=fixture();b["X100"]["n_source_scent_positive_GIFT_animal"]="3"
        with self.assertRaises(ValueError):join(a,b)
    def test_island_in_holdout_refused(self):
        a,b=fixture();a["X140"]["shared_split"]="holdout"
        with self.assertRaises(ValueError):join(a,b)
    def test_real_derived_source_sha_required(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake","data")
            with self.assertRaises(ValueError):open_zip(p,"f"*64)

if __name__=="__main__":unittest.main()
