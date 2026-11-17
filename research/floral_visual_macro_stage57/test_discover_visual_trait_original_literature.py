"""Mock search index only; tests never create real plant trait records."""
import unittest
from discover_visual_trait_original_literature import (
    parse_source_payload,assemble,TOPICS,url_for)

class BoundedVisualTraitOriginalLiteratureContract(unittest.TestCase):
    def test_query_set_fixed_and_url_source_scoped(self):
        self.assertGreaterEqual(len(TOPICS),6)
        q=url_for(TOPICS["measured_UV_pattern"])
        self.assertTrue(q.startswith("https://www.ebi.ac.uk/europepmc/webservices/rest/search?"))
        self.assertIn("pageSize=50",q)
    def test_doi_dedup_not_plant_species_replicates(self):
        f={"hitCount":2,"resultList":{"result":[
           {"id":"123","doi":"10.1111/example","title":"UV floral pattern","pubYear":"2021"},
           {"id":"124","doi":"10.1111/other","title":"Petal","pubYear":"2020"}]}}
        a,r=parse_source_payload("pattern",f)
        b=[dict(a[0],literature_query_topic="colour_change")]
        d=assemble({"pattern":a,"colour_change":b})
        self.assertEqual(len(d),2)
        self.assertEqual(len([q for q in d if q["DOI_or_unresolved"]=="10.1111/example"][0]["query_categories"]),2)
        self.assertFalse(r["truncated_first_page_not_exhaustive"])
        self.assertTrue(a[0]["source_authored_article_only_NOT_taxon_UV_state"])
    def test_truncation_does_not_imply_all_original_papers_found(self):
        f={"hitCount":101,"resultList":{"result":[
            {"id":"123","doi":"10.1111/extra","title":"UV floral","pubYear":"2017"}]}}
        _,r=parse_source_payload("pattern",f)
        self.assertTrue(r["truncated_first_page_not_exhaustive"])
    def test_bad_api_payload_and_page_count_hard_stop(self):
        with self.assertRaisesRegex(ValueError,"SEARCH_SCHEMA"):
            parse_source_payload("q",{"hitCount":0})
        with self.assertRaisesRegex(ValueError,"HIT_COUNT_INCONSISTENT"):
            parse_source_payload("q",{"hitCount":0,"resultList":{"result":[{"title":"T","id":"123"}]}})
if __name__=="__main__":
    unittest.main()
