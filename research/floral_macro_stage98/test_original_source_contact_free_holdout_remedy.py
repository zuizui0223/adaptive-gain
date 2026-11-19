"""Stage98B verify zero source geometry contact after training-only exclusion."""
import tempfile,zipfile,unittest
from pathlib import Path
from original_source_contact_free_holdout_remedy import (
    derive_contact_pruned_source_split,original_zip_rows
)

def example():
    folds=[
      {"TDWG_L3":"T1","shared_split":"exploration","spatial_block_id":"A","land_scope":"mainland"},
      {"TDWG_L3":"T2","shared_split":"exploration","spatial_block_id":"B","land_scope":"mainland"},
      {"TDWG_L3":"T3","shared_split":"exploration","spatial_block_id":"B","land_scope":"mainland"},
      {"TDWG_L3":"H1","shared_split":"holdout","spatial_block_id":"C","land_scope":"mainland"},
      {"TDWG_L3":"H2","shared_split":"holdout","spatial_block_id":"C","land_scope":"mainland"}
    ]
    contacts=[{"exploration_TDWG_L3":"T1","holdout_TDWG_L3":"H1",
               "pair_source_geometry_intersects":"True"},
              {"exploration_TDWG_L3":"T1","holdout_TDWG_L3":"H2",
               "pair_source_geometry_intersects":"True"}]
    return folds,contacts

class ContactOnlyRepair(unittest.TestCase):
    def test_remove_training_polygon_only_not_reassign_holdout(self):
        f,c=example()
        train,holdout,removed,s=derive_contact_pruned_source_split(f,c)
        self.assertEqual([r["TDWG_L3"] for r in train],["T2","T3"])
        self.assertEqual([r["TDWG_L3"] for r in holdout],["H1","H2"])
        self.assertEqual(len(removed),1)
        self.assertEqual(removed[0]["contacting_holdout_count"],2)
        self.assertTrue(s["no_train_polygon_contact_with_any_heldout_region_after_exclusion"])
        self.assertFalse(s["100km_geodesic_buffer_verified"])
        self.assertFalse(s["independent_plant_lineages_between_folds_verified"])
    def test_reject_duplicate_contact_pair(self):
        f,c=example()
        with self.assertRaisesRegex(ValueError,"DUPLICATE_CONTACT_PAIR"):
            derive_contact_pruned_source_split(f,c+[c[0]])
    def test_reject_wrong_source_region_in_contact(self):
        f,c=example();c[0]["exploration_TDWG_L3"]="MISSING"
        with self.assertRaisesRegex(ValueError,"CROSS_FOLD"):
            derive_contact_pruned_source_split(f,c)
    def test_noncontact_source_pair_not_a_contact(self):
        f,c=example();c[0]["pair_source_geometry_intersects"]="False"
        with self.assertRaises(ValueError):
            derive_contact_pruned_source_split(f,c)
    def test_island_record_must_not_appear_in_original_frame(self):
        f,c=example();f[0]["land_scope"]="island"
        with self.assertRaises(ValueError):
            derive_contact_pruned_source_split(f,c)
    def test_no_source_contact_only_keeps_original_train(self):
        f,_=example()
        train,holdout,removed,s=derive_contact_pruned_source_split(f,[])
        self.assertEqual(len(train),3)
        self.assertEqual(len(holdout),2)
        self.assertEqual(removed,[])
        self.assertEqual(s["source_exploration_regions_removed_contact"],0)
    def test_source_shas_are_required_not_just_matching_schema(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("stage94_original_mainland_shared_geoblock_split.csv","TDWG_L3\nT1\n")
            with self.assertRaisesRegex(ValueError,"SOURCE_ZIP_SHA_DRIFT"):
                original_zip_rows(p,"0"*64,"stage94_original_mainland_shared_geoblock_split.csv")

if __name__=="__main__":unittest.main()
