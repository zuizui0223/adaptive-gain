"""Stage64 test fixtures fake observation metadata; NO actual flower guide label."""
import unittest
from probe_original_iNat_flower_photo_source import (
    FCP_TARGETS,MAX_PER_TAXON,original_url,verified_photo_url,
    source_sample,validate_source_candidates
)

def source80():
    out=[]
    for n in range(80):
        if n<len(FCP_TARGETS):
            name,tid,count,tier=FCP_TARGETS[n]
            r={"source_original_VOC_binomial":name,
               "original_FCP_inat_taxon_id":str(tid),
               "original_FCP_coarse_colour_classifiable_photos":str(count),
               "precommitted_review_tier":(
                   "A_TEXT_MARKING_PLUS_40_OR_MORE_CLASSIFIABLE"
                   if tier.startswith("NHM") else "B_40_OR_MORE_CLASSIFIABLE")}
        else:
            r={"source_original_VOC_binomial":f"Otherus mock{n}",
               "original_FCP_inat_taxon_id":str(80000+n),
               "original_FCP_coarse_colour_classifiable_photos":"10",
               "precommitted_review_tier":"C_LOW_PHOTO_CLASSIFIABILITY_UNMEASURED_NOT_NEGATIVE"}
        out.append(r)
    return out

def obs(taxon=76647,oid=123,owner=12,license="cc-by",url=None):
    return {"id":oid,"user":{"id":owner},"taxon":{"id":taxon},
            "quality_grade":"research","captive":False,
            "observed_on":"2026-08-12",
            "photos":[{"id":oid+100000,
                       "url":url or "https://static.inaturalist.org/photos/123/square.jpg",
                       "license_code":license,
                       "attribution":"© Example attributed original photographer"}]}

class SourceOriginalIatPhotoCandidateContracts(unittest.TestCase):
    def test_4_advance_frozen_fcp_voc_taxa_validated_no_visual_label(self):
        validate_source_candidates(source80())
        q=source80()
        q[0]["original_FCP_coarse_colour_classifiable_photos"]="99"
        with self.assertRaisesRegex(ValueError,"FROZEN"):
            validate_source_candidates(q)
        with self.assertRaisesRegex(ValueError,"ORIGINAL_80"):
            validate_source_candidates(source80()[:-1])

    def test_only_same_taxon_licensed_photo_one_per_observer_and_observation(self):
        payload={"total_results":130,"results":[
            obs(oid=10,owner=12),obs(oid=11,owner=12),
            obs(oid=20,owner=13,license="all-rights-reserved"),
            obs(oid=30,owner=14,taxon=888),
            obs(oid=40,owner=15,license="cc0")]}
        photos,r=source_sample(payload,76647,"Dianthus deltoides","TEXT_LEAD_UNLABELLED")
        self.assertEqual(len(photos),2)
        self.assertEqual(len({v["original_observer_stable_hash_for_QC_only"] for v in photos}),2)
        self.assertEqual(r["source_exclusion_counts"]["second_photo_same_observer"],1)
        self.assertEqual(r["source_exclusion_counts"]["not_exact_original_taxon"],1)
        self.assertEqual(r["source_exclusion_counts"]["no_approved_licensed_photo_URL"],1)
        self.assertTrue(all(v["real_visible_intrapetal_guide_state"]=="UNKNOWN_UNREAD_IMAGE" for v in photos))
        self.assertTrue(all(v["UV_spatial_pattern_state"]=="UNKNOWN_NOT_MEASURED_BY_RGB" for v in photos))
        self.assertTrue(all(v["this_is_NEW_iNat_photo_sample_not_same_FCP_original_photo_IDs"] for v in photos))

    def test_source_https_image_host_and_no_user_phishing(self):
        self.assertEqual(verified_photo_url("http://static.inaturalist.org/photos/123.jpg"),"")
        self.assertEqual(verified_photo_url("https://evil.example.org/photos/123.jpg"),"")
        self.assertEqual(verified_photo_url("https://x@static.inaturalist.org/photos/123.jpg"),"")
        self.assertEqual(verified_photo_url("https://static.inaturalist.org/photos/123.jpg?secret=x"),"")
        self.assertTrue(verified_photo_url("https://static.inaturalist.org/photos/123.jpg"))
        self.assertIn("taxon_id=76647",original_url(76647))

    def test_api_malformed_results_fail_as_source_unavailable_not_biological_zero(self):
        with self.assertRaisesRegex(ValueError,"RESULTS_SCHEMA"):
            source_sample({"total_results":100,"results":"wrong"},
              76647,"Dianthus deltoides","unknown")
        with self.assertRaisesRegex(ValueError,"RESULT_COUNT"):
            source_sample({"total_results":"zero","results":[]},
              76647,"Dianthus deltoides","unknown")
if __name__=="__main__":unittest.main()
