"""No original photograph is used, retrieved or synthesized in these tests."""
import unittest
from source_VOC_FCP_visible_photo_review import join,planned_split

def example():
    f=[]
    for i in range(4475):
        f.append({
          "inat_taxon_id":str(100000+i),
          "canonical_binomial_candidate":f"mockus taxon{i}",
          "fcp_species_as_reported":f"Mockus taxon{i}",
          "n_original_photos_attempted":"100",
          "n_fcp_four_coarse_colour_classifiable_photos":"52" if i%2==0 else "25",
          "actual_visible_guide_phenotype":"NOT_MEASURED_FROM_FCP_PHOTO",
          "actual_UV_guide_phenotype":"NOT_MEASURED_FROM_FCP_PHOTO",
          "nhm_visible_marking_TEXT_candidate_or_missing":"1" if i==2 else "0"
        })
    v=[]
    for j in range(305):
        v.append({
            "source_species_canonical_binomial_if_valid":f"Mockus taxon{j}" if j<3 else f"Otherus taxon{j}",
            "GBIF_strict_taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
            "GBIF_strict_accepted_species_key_or_unknown":str(3000+j),
            "source_VOC_positive_presence_columns_in_original_full_bouquet":"12",
            "source_wind_pollination_flag_yes_if_1_else_unknown":"1" if j==1 else ""
        })
    return f,v

class ReviewQueueOriginalSourceContracts(unittest.TestCase):
    def test_exact_no_guide_labels_and_selected_image_opportunities(self):
        f,v=example()
        rows,r=join(f,v)
        self.assertEqual(r["n_exact_verbatim_binomial_VOC_FCP_join_candidates"],3)
        self.assertEqual(r["n_species_classifiable_photo_ge_40"],2)
        self.assertEqual(r["n_unverified_NHM_marking_text_candidates"],1)
        self.assertEqual(r["n_NHM_text_candidates_with_40_photos"],1)
        self.assertEqual(r["n_wind_pollinated_source_VOC_photo_matches_NOT_wind_speed"],1)
        self.assertTrue(r["all_visible_UV_pattern_status_unknown_not_negative"])
        self.assertTrue(r["this_is_a_frozen_review_target_not_morphology_measured"])
        self.assertTrue(all(x["visible_intrapetal_guide_status"].startswith("NOT_YET")
                            and x["n_original_source_photo_bytes_rehosted"]==0 for x in rows))

    def test_no_qualitative_NHM_text_guide_is_automatically_accepted(self):
        f,v=example()
        rows,r=join(f,v)
        q=[x for x in rows if x["NHM_unverified_visible_marking_text_candidate"]=="1"][0]
        self.assertIn("TEXT_MARKING",q["precommitted_review_tier"])
        self.assertEqual(q["UV_pattern_status_from_FCP_photo"],"NOT_MEASURED_UV_WITH_RGB_PHOTO")

    def test_name_ambiguity_is_holdout_not_forced_to_species(self):
        f,v=example()
        f[4]["canonical_binomial_candidate"]=f[0]["canonical_binomial_candidate"]
        r,summary=join(f,v)
        self.assertEqual(len(r),2)
        self.assertEqual(summary["n_ambiguous_FCP_canonical_join_keys_heldout"],1)

    def test_ineligible_source_denominator_or_image_fake_status_hard_stop(self):
        f,v=example()
        with self.assertRaisesRegex(ValueError,"FCP4475_OR_VOC305"):
            join(f[:-1],v)
        f,v=example()
        f[0]["actual_visible_guide_phenotype"]="observed without provenance"
        with self.assertRaisesRegex(ValueError,"FCP_UNMEASURED_VISUAL"):
            join(f,v)

    def test_accurate_photo_attempts_and_frozen_outcome_free_split(self):
        f,v=example()
        rows,r=join(f,v)
        self.assertEqual(r["n_original_attempted_photos_for_matched_species"],300)
        self.assertEqual(r["n_coarse_classifiable_photos_for_matched_species"],129)
        self.assertEqual(planned_split("Mockus taxon1"),planned_split("Mockus taxon1"))
        self.assertTrue(all(x["local_plant_VOC_and_photo_same_individual"]=="NOT_ESTABLISHED"
                            for x in rows))
if __name__=="__main__":unittest.main()
