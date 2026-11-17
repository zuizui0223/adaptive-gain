"""Stage67 real source-gating function tests; synthetic fixture != empirical species."""
from __future__ import annotations
import importlib.util,unittest
from pathlib import Path
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location("gbif73",HERE/"strict_GBIF_73_published_petal_spectra_vs_817_flower_evidence.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def fixture():
    rr={"source_data_DOI":m.FIGSHARE_DOI,
        "original_figshare":{"original_source_sha256":m.FIGSHARE_ORIGINAL_SHA},
        "actual_source_petal_columns":{"n_source_columns_with_complete_UV_and_visible":73}}
    spectra=[]
    for i in range(73):
        nm=f"Example{i} plant{i}"
        spectra.append({
           "source_literal_species_candidate":nm,
           "flower_part":"petal",
           "source_measured_spectrum_status":"SPECTRUM_MEASURED_WITH_UV_AND_VIS",
           "UV_spatial_guide_status":"NOT_OBSERVABLE_FROM_ONE_PETAL_MEAN_SPECTRUM",
           "UV_mean_reflectance_300_399_or_unknown":"12.5",
           "visible_mean_reflectance_400_700_or_unknown":"40",
           "original_spectral_column_name":nm.replace(" ","_"),
           "original_source_spectral_member":"petals/test.csv"})
    atlas=[]
    for j in range(817):
        atlas.append({"gbif_accepted_species_key":str(j+100),
               "source_UV_pattern_directly_measured_or_unknown":"1" if j<101 else "0" if j<230 else ""})
    tax={r["source_literal_species_candidate"]:{"taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
          "gbif_accepted_usage_key":int(100+i) if i<2 else int(2000+i)} for i,r in enumerate(spectra)}
    return spectra,atlas,rr,tax

class OriginalGBIFPetalSourceTests(unittest.TestCase):
    def test_correct_source_73_and_817_conserved(self):
        a,b,c,t=fixture()
        names,prior=m.source_records(a,b,c)
        self.assertEqual(len(names),73)
        self.assertEqual(len(prior),817)
    def test_union_and_overlapping_direct_uv_distinct(self):
        a,b,c,t=fixture()
        out,receipt=m.attach(a,b,c,t)
        self.assertEqual(receipt["strict_cross_study_accepted_species_overlap"],2)
        self.assertEqual(receipt["new_2024_strict_accepted_species_not_in_prior"],71)
        self.assertEqual(receipt["union_accepted_evidence_species_not_all_guide_positive"],888)
        self.assertEqual(receipt["2024_spectral_sample_also_measured_UV_pattern_in_prior"],2)
        self.assertEqual(float(out[0]["source_UV_300_399_mean_reflectance_fraction_if_needed"]),.125)
        self.assertEqual(out[0]["UV_spatial_guide_present_or_absent"],
                         "NOT_MEASURED_IN_THIS_PETAL_SPECTRA_SOURCE")
    def test_unresolved_species_not_added_as_new(self):
        a,b,c,t=fixture()
        t[a[2]["source_literal_species_candidate"]]={"taxonomy_status":"API_FAILURE_UNRESOLVED_NOT_ABSENT"}
        o,r=m.attach(a,b,c,t)
        self.assertEqual(r["not_strictly_resolved_source_names"],1)
        self.assertEqual(r["union_accepted_evidence_species_not_all_guide_positive"],887)
        self.assertTrue(o[2]["gbif_accepted_species_key_or_unknown"]=="")
    def test_missing_2024_spectra_is_not_guide_negative(self):
        a,b,c,t=fixture()
        a[0]["source_measured_spectrum_status"]="INCOMPLETE_SPECTRUM_NOT_ZERO"
        with self.assertRaisesRegex(ValueError,"NOT_COMPLETE"):
            m.source_records(a,b,c)
    def test_wrong_2024_archive_digest_rejected(self):
        a,b,c,t=fixture();c["original_figshare"]["original_source_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"AUTHENTICITY"):
            m.source_records(a,b,c)
if __name__=="__main__":unittest.main()
