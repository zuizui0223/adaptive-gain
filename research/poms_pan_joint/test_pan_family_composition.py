import unittest
import numpy as np
import pandas as pd
from test_pan_richness_model import PanContextModelTests
from pan_family_composition import (
    build_pan_family_context, make_matched_family_data,
    fit_family_control, _normalized_family, FEATURES
)

class FamilyCompositionSourceTests(unittest.TestCase):
    def fixture(self):
        fit,stations,flowers=PanContextModelTests().fixture()
        # Plant identity is defined independently from FIT outcome.
        taxon_number=flowers.source_taxon_version_key.str.extract(r"(\d+)",expand=False).astype(int)
        family_names=["Asteraceae","Fabaceae","Apiaceae","Rosaceae"]
        flowers["family"]=[family_names[int(i)%4] for i in taxon_number]
        return fit,stations,flowers
    def test_three_source_families_and_exact_denominator(self):
        fit,s,f=self.fixture()
        pan,meta=build_pan_family_context(s,f)
        selected=meta["families_selected_source_only"]
        self.assertEqual(len(selected),3)
        self.assertEqual(selected[0]["name"],"apiaceae")  # tie-break alphabetical
        self.assertEqual(meta["five_station_site_days_with_named_taxa"],140)
        self.assertEqual(meta["source_orphan_flower_occurrences_quarantined"],0)
        self.assertFalse(pan.loc[pan.stations.eq(5),list(FEATURES)].isna().any().any())
        self.assertTrue((pan[list(FEATURES)].sum(axis=1)<=1.00000000001).all())
        self.assertGreater(meta["taxon_families_in_source"],3)
    def test_unchanged_fit_grain_and_model(self):
        fit,s,f=self.fixture()
        pan,meta=build_pan_family_context(s,f)
        d,support=make_matched_family_data(fit,pan,meta,expected_stage3f=None)
        self.assertEqual(support["matched_pair_positive_fit_surveys"],len(fit))
        self.assertEqual(support["family_composition_gate"],"PASS",support)
        self.assertEqual(len(d.sample_id.unique()),len(fit))
        r=fit_family_control(d)
        self.assertEqual(r["status"],"FITTED",r.get("error",str(r)))
        self.assertEqual(r["design_columns"],r["design_rank"])
        self.assertTrue(0<=r["family_composition_joint_wald"]["p"]<=1)
        self.assertGreater(r["strong_wind_OR"]["OR"],0)
    def test_conflicting_known_source_taxon_families_fail_closed(self):
        fit,s,f=self.fixture()
        f.loc[f.index[-1],"family"]="Inventedaceae"
        with self.assertRaisesRegex(ValueError,"conflicting known families"):
            build_pan_family_context(s,f)
    def test_duplicate_observation_does_not_create_extra_site_day_taxa(self):
        fit,s,f=self.fixture()
        p,meta=build_pan_family_context(s,f)
        duplicate=f.iloc[[0]].copy()
        duplicate["occurrence_id"]="synthetic-duplicate"
        with_extra=pd.concat([f,duplicate],ignore_index=True)
        second,other=build_pan_family_context(s,with_extra)
        self.assertEqual(meta["families_selected_source_only"],other["families_selected_source_only"])
        pd.testing.assert_frame_equal(
            p[list(FEATURES)].reset_index(drop=True),
            second[list(FEATURES)].reset_index(drop=True)
        )
    def test_unknown_source_family_stays_in_denominator(self):
        fit,s,f=self.fixture()
        f.loc[f.source_taxon_version_key.eq("Key8"),"family"]=pd.NA
        pan,receipt=build_pan_family_context(s,f)
        self.assertGreater(receipt["unknown_family_site_day_taxa"],0)
        self.assertTrue((pan[list(FEATURES)].sum(axis=1)<=1+1e-10).all())
    def test_family_labels_cleaned_without_inventing_taxonomy(self):
        x=pd.Series([" Asteraceae ","ASTERACEAE",pd.NA,"not recorded"])
        self.assertEqual(_normalized_family(x).tolist(),
                         ["asteraceae","asteraceae","__SOURCE_UNKNOWN_FAMILY__",
                          "__SOURCE_UNKNOWN_FAMILY__"])

if __name__=="__main__":
    unittest.main()
