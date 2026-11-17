"""Mock-original photo credits and annotations; no actual visible mark invented as data."""
import unittest
from test_audit_eight_original_CC_photo_one_reviewer_labels import fixture
from audit_original_annotated_8_photo_marking import verified_stage65

def source27(rows):
    out=[]
    for r in rows:
        out.append({
          "fresh_2026_original_iNaturalist_photo_id":r["source_photo_id"],
          "source_original_iNat_species":r["source_species"],
          "fresh_2026_original_iNaturalist_observation_id":r["source_observation_id"],
          "source_annotation_plant_phenology_flowers_server_filtered":"True",
          "actual_individual_photo_visible_open_flower_status":"NOT_YET_VERIFIED_FROM_PIXELS"
        })
    for i in range(19):
        out.append({
          "fresh_2026_original_iNaturalist_photo_id":str(90000+i),
          "source_original_iNat_species":"Mockus extra",
          "fresh_2026_original_iNaturalist_observation_id":str(91000+i),
          "source_annotation_plant_phenology_flowers_server_filtered":"True",
          "actual_individual_photo_visible_open_flower_status":"NOT_YET_VERIFIED_FROM_PIXELS"
        })
    return out

class Stage65SourcePhotoIdImageAnnotationContracts(unittest.TestCase):
    def test_8_original_image_source_and_prior_review_overlap_explicit(self):
        credit,rows=fixture()
        prior=[dict(x) for x in rows]
        prior[0]["source_photo_id"]="9999"
        r=verified_stage65(credit,source27(rows),rows,prior)
        self.assertEqual(r["n_source_photos_visible_colour_marking_positive"],2)
        self.assertEqual(r["n_annotated_CC_original_photo_source_records"],27)
        self.assertEqual(r["n_stage65_images_reused_from_old_stage64_original_photo_sample"],7)
        self.assertEqual(r["n_stage65_images_not_in_old_stage64_eight_image_sample"],1)
        self.assertEqual(r["n_source_positive_photo_IDs_already_in_stage64_manual_review"],1)
        self.assertTrue(r["between_two_pilot_photographs_not_randomized_phenology_control"])
        self.assertTrue(r["source_cue_routing_wind_VOC_mechanism_not_measured"])

    def test_non_source_annotated_image_refused_even_if_CC_pixel_digest_exists(self):
        credit,rows=fixture()
        src=source27(rows)
        src[0]["fresh_2026_original_iNaturalist_photo_id"]="234888"
        with self.assertRaisesRegex(ValueError,"NOT_A_FLOWERING"):
            verified_stage65(credit,src,rows,rows)

    def test_fake_server_flower_status_and_source_population_require_stop(self):
        credit,rows=fixture()
        src=source27(rows)
        src[0]["source_annotation_plant_phenology_flowers_server_filtered"]="False"
        with self.assertRaisesRegex(ValueError,"NOT_AUTHENTICATED"):
            verified_stage65(credit,src,rows,rows)
        with self.assertRaisesRegex(ValueError,"_27_PHOTO_FRAME"):
            verified_stage65(credit,src[:-1],rows,rows)

    def test_prior_reused8_must_have_exact_ID_unique_records(self):
        credit,rows=fixture()
        prior=[dict(x) for x in rows]
        prior[0]["source_photo_id"]=prior[1]["source_photo_id"]
        with self.assertRaisesRegex(ValueError,"REUSED_PHOTO_ID"):
            verified_stage65(credit,source27(rows),rows,prior)
if __name__=="__main__":unittest.main()
