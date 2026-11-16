"""Mock-only accepted-key dedup and distinct optical measurement states."""
import unittest
from join_source_authenticated_accepted_uv_studies import union_source_records

def make_2016(key="",state="1"):
    return {
      "original_taxon_code":"P_mockus",
      "original_S1_author_full_binomial_candidate":"Potentilla mockus",
      "source_measured_UV_pattern_present":state,
      "accepted_GBIF_species_match_status":(
         "EXACT_CONFIDENT_SPECIES_MAPPED" if key else "ORIGINAL_S1_NAME_UNRESOLVED"),
      "accepted_GBIF_taxon_key_or_empty":key
    }

def make_other(article,key="",state=""):
    return {
      "original_study_doi":article,
      "UV_spatial_guide_pattern_source_status":state,
      "gbif_match_status":("EXACT_CONFIDENT_SPECIES_MAPPED" if key else "UNRESOLVED"),
      "gbif_accepted_species_key":key,
      "published_taxon_string":"Mockus example",
      "canonical_binomial_candidate_unreconciled":"Mockus example"
    }

class SourceUnion(unittest.TestCase):
    def fixture(self):
        a=[make_2016() for _ in range(177)]
        b=[make_other("10.3389/fpls.2021.618028") for _ in range(80)]
        b.extend(make_other("10.1016/j.cub.2020.08.077",
                            state="NOT_CLASSIFIED_BY_TABLE_S1") for _ in range(41))
        return a,b

    def test_accepted_key_reduces_study_replicates_to_one_species(self):
        a,b=self.fixture()
        a[0]=make_2016("100","1")
        b[0]=make_other("10.3389/fpls.2021.618028","100","SOURCE_MEASURED_PATTERNED")
        b[80]=make_other("10.1016/j.cub.2020.08.077","200","NOT_CLASSIFIED_BY_TABLE_S1")
        out,r=union_source_records(a,b)
        self.assertEqual(r["n_unique_accepted_species_across_three_study_sources"],2)
        self.assertEqual(r["n_unique_species_with_consistent_directly_measured_UV_spatial_pattern"],1)
        self.assertEqual(r["n_unique_species_with_temporal_UVP_only_no_direct_binary"],1)
        self.assertTrue(r["never_sum_overlapping_published_species_denominators"])

    def test_original_UV_pattern_conflict_must_not_be_majority_resolved(self):
        a,b=self.fixture()
        a[0]=make_2016("100","0")
        b[0]=make_other("10.3389/fpls.2021.618028","100","SOURCE_MEASURED_PATTERNED")
        out,r=union_source_records(a,b)
        self.assertEqual(r["n_conflicting_direct_spatial_pattern_accepted_species"],1)
        self.assertEqual(out[0]["source_measured_UV_spatial_pattern_or_missing"],"")

    def test_2020_historical_UVP_must_not_be_reclassified_guide(self):
        a,b=self.fixture()
        b[80]=make_other("10.1016/j.cub.2020.08.077","200","SOURCE_MEASURED_PATTERNED")
        with self.assertRaisesRegex(ValueError,"NO_GO_HISTORICAL_UVP_TREATED_AS_GUIDE"):
            union_source_records(a,b)

    def test_unverified_source_denominator_never_accepted(self):
        a,b=self.fixture()
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_ARCHIVED_TAXON_DENOMINATORS"):
            union_source_records(a[:-1],b)

if __name__=="__main__":
    unittest.main()
