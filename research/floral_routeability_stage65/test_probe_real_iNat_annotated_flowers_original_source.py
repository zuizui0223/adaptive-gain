"""Only invented photo ID metadata; no actual phenology verified in these tests."""
import io,json,unittest
from probe_real_iNat_annotated_flowers_original_source import (
    annotated_url,get_annotated_source,compare_prior,ANNOTATION_ID,
    FLOWERS_VALUE_ID)

class FakeResponse:
    def __init__(self,url,content):
        self.url=url;self.content=content
    def geturl(self):return self.url
    def read(self,n):return self.content[:n]
    def __enter__(self):return self
    def __exit__(self,*args):pass

def entry(s,p):
    return {"source_original_iNat_species":s,
            "fresh_2026_original_iNaturalist_photo_id":str(p)}

class IatOriginalFloweringAnnotationSourceTest(unittest.TestCase):
    def test_source_query_uses_official_annotation_term_pair_only(self):
        url=annotated_url(76647)
        self.assertIn("taxon_id=76647",url)
        self.assertIn("term_id=12&term_value_id=13",url)
        self.assertEqual(ANNOTATION_ID,12)
        self.assertEqual(FLOWERS_VALUE_ID,13)

    def test_source_annotated_query_json_is_not_a_flower_pixel_classification(self):
        u=annotated_url(76647)
        payload=json.dumps({"total_results":1,"results":[]}).encode("utf8")
        r,sha=get_annotated_source(76647,opener=lambda req,timeout:
                                  FakeResponse(u,payload))
        self.assertEqual(len(sha),64)
        self.assertEqual(r["total_results"],1)
        self.assertEqual(r["results"],[])

    def test_not_reusing_same_api_url_as_unfiltered_source(self):
        u=annotated_url(76647)
        self.assertNotEqual(u,"https://api.inaturalist.org/v1/observations?taxon_id=76647")
        payload=b'{"total_results":1,"results":[]}'
        with self.assertRaisesRegex(ValueError,"EXTERNAL_REDIRECT"):
            get_annotated_source(76647,opener=lambda req,timeout:
                       FakeResponse("https://evil.invalid",payload))

    def test_source_metadata_overlap_never_claims_two_independent_samples(self):
        a=[entry("Dianthus deltoides",1),entry("Dianthus barbatus",3)]
        b=[entry("Dianthus deltoides",1),entry("Dianthus deltoides",2)]
        d=compare_prior(a,b)
        self.assertEqual(d["n_selected_photo_IDs_in_both_queries"],1)
        self.assertEqual(d["n_new_annotated_photo_IDs_not_in_old_filtered_source_list"],1)
        self.assertTrue(d["flower_annotation_not_equivalent_to_photo_open_corolla"])
        self.assertTrue(d["both_pilots_same_iNaturalist_source_not_independent_provider"])

    def test_missing_photo_identifier_is_an_error_not_a_negative_morph(self):
        with self.assertRaisesRegex(ValueError,"UNKNOWN_PHOTO_ID"):
            compare_prior([entry("Dianthus deltoides","")],
                          [entry("Dianthus deltoides",2)])
if __name__=="__main__":
    unittest.main()
