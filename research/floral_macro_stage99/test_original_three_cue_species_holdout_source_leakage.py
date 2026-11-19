"""Stage99 exact species identity pseudoreplication and heldout-source guards."""
import tempfile,unittest,zipfile
from pathlib import Path
from original_three_cue_species_holdout_source_leakage import (
    novelty_report,source_region_holdout_novelty,
    original_tdwg_fold_ids,load_original_WFO_source_positive_and_negatives
)

class SourceSpeciesHoldoutGuards(unittest.TestCase):
    def test_known_species_not_recounted_as_new_holdout_evolution(self):
        train={"flora alba","flora rubra","herba alba"}
        test={"flora alba","flora nigra","sylva alba"}
        d=novelty_report(train,test,train|test)
        self.assertEqual(d["distinct_exact_species_shared_train_and_holdout"],1)
        self.assertEqual(d["distinct_exact_species_new_only_in_holdout"],2)
        self.assertAlmostEqual(d["holdout_exact_species_reuse_fraction"],1/3)
        self.assertEqual(d["distinct_holdout_genera_containing_new_species"],2)
        self.assertEqual(d["distinct_holdout_genera_absent_in_training"],1)
    def test_all_reused_sources_no_holdout_species_novelty(self):
        s={"flora alba","flora rubra"}
        d=novelty_report(s,s,s)
        self.assertEqual(d["distinct_exact_species_new_only_in_holdout"],0)
        self.assertEqual(d["holdout_exact_species_reuse_fraction"],1)
    def test_missing_trait_in_holdout_is_unknown_not_zero(self):
        d=novelty_report({"flora alba"},{"herba alba"},{"flora alba"})
        self.assertEqual(d["distinct_source_species_in_fixed_37holdout"],0)
        self.assertIsNone(d["holdout_exact_species_reuse_fraction"])
    def test_region_novelty_denominator_species_identity_only(self):
        native={"AAA":{"flora alba","flora nigra"},"BBB":{"herba alba"}}
        d=source_region_holdout_novelty(native,{"AAA","BBB"},{"flora alba"},
              {"scent_positive":{"flora alba","flora nigra","herba alba"}})
        a=next(x for x in d if x["TDWG_L3"]=="AAA")
        self.assertEqual(a["scent_positive_source_trait_species"],2)
        self.assertEqual(a["scent_positive_novel_trait_species_not_in_72train"],1)
        self.assertAlmostEqual(a["scent_positive_novel_fraction"],.5)
        self.assertEqual(a["this_is_source_identity_support_not_species_independent_fitness"],"YES")
    def test_original_source_fold_requires_real_sha(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/"wrong.zip"
            with zipfile.ZipFile(f,"w") as z:
                z.writestr("stage98B_holdout_original_mainland_37_UNCHANGED.csv","TDWG_L3\nAAA\n")
            with self.assertRaisesRegex(ValueError,"SOURCE_GEOGRAPHIC_ZIP_SHA_MISMATCH"):
                original_tdwg_fold_ids(f)
    def test_wfo_prose_states_require_real_original_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            f=Path(td)/"wrong.zip"
            with zipfile.ZipFile(f,"w") as z:
                z.writestr("stage93_derived/stage93_original_WFO_species_fragrance_lexical_states_NOT_VOC.csv","accepted_species\nAAA\n")
            with self.assertRaisesRegex(ValueError,"WFO_ORIGINAL_SPECIES_SOURCE_SHA_MISMATCH"):
                load_original_WFO_source_positive_and_negatives(f,set())

if __name__=="__main__":unittest.main()
