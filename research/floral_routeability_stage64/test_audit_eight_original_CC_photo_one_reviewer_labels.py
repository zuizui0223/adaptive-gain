"""Mock source pixel credit fixtures; not new flower image observations."""
import unittest
from audit_eight_original_CC_photo_one_reviewer_labels import audit,TOTAL

def fixture():
    annotations=[]
    original=[]
    for i in range(TOTAL):
        pid=str(7000+i)
        name="Mockus firstus" if i<2 else "Mockus vegetans"
        stage="OPEN_COROLLA_DETAIL_PRESENT" if i<2 else "VEGETATIVE_NO_OPEN_FLOWER"
        mark="VISIBLE_COLOUR_PATTERN_PRESENT" if i<2 else "UNKNOWN_NOT_EVALUABLE"
        annotations.append({
            "source_photo_id":pid,
            "source_observation_id":str(40000+i),
            "source_species":name,
            "original_medium_photo_SHA256":"a"*64,
            "photo_eligibility_photo_only":stage,
            "reviewed_visible_intrapetal_marking":mark,
            "reviewer_status":"ONE_UNBLINDED_ASSISTANT_SOURCE_IMAGE_REVIEW",
            "source_RGB_UV_pattern_status":"UNOBSERVABLE_IN_RGB",
            "source_VOC_same_plant_status":"NOT_MEASURED_SAME_INDIVIDUAL"})
        original.append({
            "source_original_photo_id":pid,
            "source_original_observation_id":str(40000+i),
            "source_species":name,
            "source_verified_medium_image_SHA256":"a"*64,
            "status":"ORIGINAL_CC_LICENSED_PIXEL_DOWNLOADED_FOR_BOTANICAL_REVIEW",
            "original_license":"cc-by",
            "source_original_attribution":"© Example original contributor"
        })
    return {"status":"LICENSED_ORIGINAL_INAT_FOUR_TAXON_SOURCE_PIXEL_REVIEW_GATE",
        "n_licensed_actual_medium_photo_pixels_read":8,
        "source_image_credits_and_exceptions":original},annotations

class SourceOriginalEightBotanicalPhotoEligibilityContracts(unittest.TestCase):
    def test_all_eight_original_photo_ids_and_source_hashes_eligible(self):
        meta,rows=fixture()
        result=audit(meta,rows)
        self.assertEqual(result["n_source_photos_with_reviewable_open_corolla"],2)
        self.assertEqual(result["n_source_photos_visible_colour_marking_positive"],2)
        self.assertEqual(result["n_source_photos_flower_pattern_unknown_not_absent"],6)
        self.assertEqual(result["n_source_photos_verified_within_corolla_uniform"],0)
        self.assertTrue(result["unblinded_assistant_one_reviewer_no_second_independent_verifier"])
        self.assertTrue(result["no_species_level_absence_or_frequency_inference"])
        self.assertTrue(result["RGB_is_not_UV_measured"])

    def test_no_flowers_cannot_be_called_source_visible_pattern_absent(self):
        meta,rows=fixture()
        rows[3]["reviewed_visible_intrapetal_marking"]="VISIBLE_COLOUR_PATTERN_VERIFIED_UNIFORM"
        with self.assertRaisesRegex(ValueError,"CALLED_PATTERN_NEGATIVE"):
            audit(meta,rows)

    def test_source_image_SHA_provenance_required_for_any_visual_annotation(self):
        meta,rows=fixture()
        rows[0]["original_medium_photo_SHA256"]="b"*64
        with self.assertRaisesRegex(ValueError,"SPECIES_DIGEST"):
            audit(meta,rows)
        meta,rows=fixture()
        rows[0]["source_photo_id"]="999999"
        with self.assertRaisesRegex(ValueError,"UNAUDITED"):
            audit(meta,rows)

    def test_one_reviewer_not_silent_independent_replication(self):
        meta,rows=fixture()
        rows[0]["reviewer_status"]="TWO_HUMAN_REVIEWERS"
        with self.assertRaisesRegex(ValueError,"ONE_REVIEWER"):
            audit(meta,rows)
        meta,rows=fixture()
        rows[0]["source_RGB_UV_pattern_status"]="MEASURED_UV"
        with self.assertRaisesRegex(ValueError,"ONE_REVIEWER"):
            audit(meta,rows)

    def test_complete_eight_source_photos_only_and_original_credits(self):
        meta,rows=fixture()
        with self.assertRaisesRegex(ValueError,"LABEL_COUNT"):
            audit(meta,rows[:-1])
        meta,rows=fixture()
        meta["source_image_credits_and_exceptions"][0]["original_license"]="all-rights-reserved"
        with self.assertRaisesRegex(ValueError,"LICENSE"):
            audit(meta,rows)
if __name__=="__main__":unittest.main()
