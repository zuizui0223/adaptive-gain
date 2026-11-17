"""Offline-only mock 245 record table tests, no original observations fabricated."""
import unittest
from extract_oliveira245_gbif_union import (
    REQUIRED_HEADERS,source_entries,attach_taxonomy_and_prior,PIN_DOCX_SHA)

def fixture():
    header=list(REQUIRED_HEADERS)+["RI","Citation"]
    out=[header]
    for i in range(245):
        out.append(["Mockus plantus A.", "Mockus","Mockaceae","P",
                    "EN","bee","bee","UV-White","0.023","16","Mock ref"])
    return out

def prior_583():
    return [{"gbif_accepted_species_key":str(600000+i)} for i in range(583)]

class Original245UVReflectionSpeciesContracts(unittest.TestCase):
    def test_exact_original_245_row_header_and_reflection_range(self):
        r=source_entries(fixture())
        self.assertEqual(len(r),245)
        self.assertEqual(r[0]["source_canonical_binomial_if_lexically_exact"],"Mockus plantus")
        self.assertEqual(r[0]["source_average_UV_reflection_proportion_or_unknown"],0.023)
        self.assertTrue(r[0]["original_average_UV_reflectance_is_not_spatial_UV_pattern"])
        self.assertTrue(r[0]["original_source_site_GPS_undetermined"])

    def test_source_rows_not_guessed_if_denominator_is_292(self):
        a=fixture()+[fixture()[1]]
        with self.assertRaisesRegex(ValueError,"ROW_COUNT"):
            source_entries(a)

    def test_no_true_zero_if_numeric_reflection_missing(self):
        a=fixture()
        a[1][8]=""
        self.assertIsNone(source_entries(a)[0]["source_average_UV_reflection_proportion_or_unknown"])

    def test_out_of_range_reflection_and_genus_mismatch_not_false_exact_name(self):
        a=fixture()
        a[1][8]="3.7"
        with self.assertRaisesRegex(ValueError,"OUT_OF_RANGE"):
            source_entries(a)
        a=fixture()
        a[1][1]="Otherus"
        self.assertEqual(source_entries(a)[0]["source_canonical_binomial_if_lexically_exact"],"")

    def test_source_taxon_aliases_overlap_by_accepted_id_not_literal_names(self):
        src=source_entries(fixture())
        lookup={"Mockus plantus":{"taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
                                  "gbif_accepted_usage_key":600000}}
        out,res=attach_taxonomy_and_prior(src,lookup,prior_583())
        self.assertEqual(res["n_distinct_GBIF_accepted_species_in_2025_reflectance_source"],1)
        self.assertEqual(res["n_source_2025_overlap_prior_accepted_583"],1)
        self.assertEqual(res["n_combined_prior_and_2025_unique_accepted"],583)
        self.assertEqual(res["source_245_original_Wiley_PMC_docx_rows"],245)
        self.assertEqual(res["source_original_OA_docx_SHA256"],PIN_DOCX_SHA)
        self.assertTrue(res["no_UV_spatial_pattern_or_native_guild_causal_or_SEM_claim"])

if __name__=="__main__":
    unittest.main()
