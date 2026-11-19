"""Stage101 original flower-size source grade union and strict crossfold tests."""
import unittest,tempfile,zipfile
from pathlib import Path
from verify_original_WFO_AusTraits_diameter_union_mainland import (
   size_source_groups,source_ledger,frozen_mainland_codes
)

class Stage101SourceIdentity(unittest.TestCase):
    def sample(self):
        native={"A":{"flora alba","flora rubra","herba alba"},
                "B":{"flora rubra","sylva alba"}}
        aus={"flora alba":10,"flora rubra":8}
        wfo={"flora rubra":9,"sylva alba":13}
        corolla={"herba alba":20}
        return native,aus,wfo,corolla
    def test_source_grade_union_not_sum_when_same_species(self):
        native,aus,wfo,corolla=self.sample()
        summary,regions,grades=size_source_groups(native,aus,wfo,corolla,{"A"},{"B"})
        self.assertEqual(summary["source_union_ANY_size_record_not_all_direct_measured"]["source_distinct_global_species"],3)
        self.assertEqual(summary["AusTraits_and_WFO_exact_species_overlap"]["source_distinct_global_species"],1)
        self.assertEqual(summary["source_union_ANY_size_record_not_all_direct_measured"]["source_original_holdout_species"],2)
        self.assertEqual(summary["source_union_ANY_size_record_not_all_direct_measured"]["exact_reused_species_train_and_holdout"],1)
        self.assertEqual(summary["source_union_ANY_size_record_not_all_direct_measured"]["distinct_holdout_species_NOT_seen_in_train"],1)
    def test_corolla_is_never_added_to_wholeflower_size_union(self):
        native,aus,wfo,corolla=self.sample()
        summary,regions,grades=size_source_groups(native,aus,wfo,corolla,{"A"},{"B"})
        self.assertEqual(len(grades["source_union_ANY_size_record_not_all_direct_measured"]),3)
        self.assertEqual(next(r for r in regions if r["TDWG_L3"]=="A")["n_unreviewed_WFO_corolla_width_only_NOT_whole_flower"],1)
    def test_region_has_original_fold_not_reassigned(self):
        native,aus,wfo,corolla=self.sample()
        _,rows,_=size_source_groups(native,aus,wfo,corolla,{"A"},{"B"})
        self.assertEqual(next(r for r in rows if r["TDWG_L3"]=="B")["predeclared_original_geographic_source_fold"],"holdout")
    def test_forged_WFO_size_source_fails_sha(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("stage100_WFO_original_accepted_species_whole_flower_diameter_SOURCE_CANDIDATE.csv","fake")
            with self.assertRaisesRegex(ValueError,"DIGEST_MISMATCH"):
                source_ledger(p,"a"*64,{"flora alba"})
    def test_unknown_sha_not_accepted_as_original_source(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            p.write_bytes(b"")
            with self.assertRaisesRegex(ValueError,"UNPINNED_SOURCE_WFO_DIGEST"):
                source_ledger(p,"not a verified SHA",{"flora alba"})
    def test_unaudited_region_source_cannot_enter_mainland_analysis(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            p.write_bytes(b"")
            with self.assertRaisesRegex(ValueError,"GEOGRAPHY_SHA_CHANGED"):
                frozen_mainland_codes(p)

if __name__=="__main__":unittest.main()
