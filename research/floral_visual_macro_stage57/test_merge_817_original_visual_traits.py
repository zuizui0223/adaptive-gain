"""All species here are mock rows. Real input must come from two source artifacts."""
import unittest
from merge_817_original_visual_traits import combine,UNION_N

def fixture():
    prior=[]
    for i in range(583):
        uv="1" if i<101 else "0" if i<230 else ""
        prior.append({
          "gbif_accepted_species_key":str(500000+i),
          "direct_UV_2016_2021_pattern_or_missing":uv,
          "source_original_direct_UV_studies":"10.1111/nph.13921" if i<262 else "",
          "original_Ohashi_2015_age_reflectance_archive":"True" if i<207 else "False",
          "original_2025_colour_change_literature_reviewed":"True" if i<124 else "False",
        })
    current=[]
    for i in range(243):
        key=500000+i if i<9 else 700000+i
        current.append({
            "accepted_GBIF_species_key":str(key),
            "source_literature_primary_pollination_system":"bee" if i<134 else "bird",
            "mean_original_source_UV_reflectance":str(0 if i==0 else .002+i*.0005),
            "source_broad_area":"N" if i%2 else "EN",
            "source_family":"Mockaceae",
            "original_hue_UV_positive_any":"True" if i%3 else "False",
            "number_original_source_measurement_rows":"2" if i==2 else "1"
        })
    return prior,current

class OriginalModalityUnion817Contracts(unittest.TestCase):
    def test_precise_study_counts_unique_accepted_and_unknown_not_zero(self):
        p,n=fixture()
        rows,report=combine(p,n)
        self.assertEqual(len(rows),UNION_N)
        self.assertEqual(report["new_2025_source_unique_accepteds_not_in_prior"],234)
        self.assertEqual(report["source_accepted_species_overlap"],9)
        self.assertEqual(report["source_original_directly_measured_UV_spatial_patterned"],101)
        self.assertEqual(report["source_original_directly_measured_UV_spatial_uniform"],129)
        self.assertEqual(report["n_species_without_direct_UV_spatial_contrast_classification"],587)
        self.assertEqual(report["source_original_Oliveira_2025_primary_guild_labels"],
                         {"bee":134,"bird":109})
        self.assertTrue(report["no_unknown_visual_state_encoded_as_false_zero"])
        # A truly numerically-zero reflection is not a binary absent guide.
        r=next(x for x in rows if x["gbif_accepted_species_key"]=="500000")
        self.assertEqual(r["original_Oliveira2025_mean_UV_reflection_or_unknown"],0.)
        self.assertEqual(r["source_UV_pattern_directly_measured_or_unknown"],"1")
        unseen=next(x for x in rows if x["gbif_accepted_species_key"]=="700143")
        self.assertEqual(unseen["source_UV_pattern_directly_measured_or_unknown"],"")

    def test_duplicate_accepted_species_from_second_source_must_fail(self):
        p,n=fixture()
        n[0]["accepted_GBIF_species_key"]=n[1]["accepted_GBIF_species_key"]
        with self.assertRaisesRegex(ValueError,"SOURCE_243_ACCEPTED_NONUNIQUE"):
            combine(p,n)

    def test_receptor_age_colour_change_and_review_not_inferred_from_unmeasured(self):
        p,n=fixture()
        rows,_=combine(p,n)
        e=next(x for x in rows if x["gbif_accepted_species_key"]=="700242")
        self.assertFalse(e["original_Ohashi2015_spectral_taxon_source"])
        self.assertFalse(e["original_2025_literature_colour_change_reported"])
        self.assertEqual(e["Ohashi2015_bee_age_colour_change_perceptible"],
                         "NOT_SPECIES_CLASSIFIED")
        self.assertTrue(e["no_unknown_visual_modality_inferred_as_absent"])

    def test_original_source_boolean_missing_not_interpreted_false(self):
        p,n=fixture()
        p[0]["original_Ohashi_2015_age_reflectance_archive"]=""
        with self.assertRaisesRegex(ValueError,"BOOLEAN_TRAIT_PROVENANCE"):
            combine(p,n)

    def test_2025_missing_or_impossible_mean_UV_must_fail(self):
        p,n=fixture()
        n[0]["mean_original_source_UV_reflectance"]=1.1
        with self.assertRaisesRegex(ValueError,"NUMERIC_UV_REFLECTION"):
            combine(p,n)

if __name__=="__main__":
    unittest.main()
