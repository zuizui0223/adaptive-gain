"""Stage67 source-only systematic literature and evidence-unit gate tests."""
import importlib.util,json
from pathlib import Path
import unittest
from unittest.mock import patch

HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location("lit67",HERE/"systematic_source_europepmc_visual_and_multisensory.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def article(doi,name,yr="2025"):
    return {"doi":doi,"id":"123","pubYear":yr,"title":name}

class SourceLiteratureTests(unittest.TestCase):
    def test_stage57_predeclared_original_exact_reuse(self):
        self.assertEqual(len(mod.SEARCHES),28)
        self.assertIn('TITLE_ABS:"UV pattern"',mod.SEARCHES["measured_UV_pattern"])
        self.assertEqual(mod.PAGE_SIZE,100)
        self.assertEqual(mod.MAX_PAGES,10)

    def test_exact_pagination_and_topic_dedup(self):
        def source(q,page):
            # 120 article hits; page 1 has 100 and page 2 has 20.
            xs=[article(f"10.5555/a{i}","Case"+str(i)) for i in range(100)] if page==1 else [
                article(f"10.5555/b{i}","Case B"+str(i)) for i in range(20)]
            return {"hitCount":120,"resultList":{"result":xs}}
        rows,receipt=mod.source_topic("UV_test","TITLE_ABS:flower",puller=source)
        self.assertEqual(receipt["source_index_total_hits"],120)
        self.assertEqual(receipt["pages_downloaded"],2)
        self.assertFalse(receipt["page_ceiling_truncated"])
        self.assertEqual(len(rows),120)
        merged=mod.aggregate({"UV_test":rows,"second":[{**rows[0],"query_topics":["second"]}]})
        self.assertEqual(len(merged),120)
        self.assertEqual(set(merged[0]["query_topics"]),{"UV_test","second"})

    def test_zero_is_not_flower_guide_negative(self):
        def empty(q,page):return {"hitCount":0,"resultList":{"result":[]}}
        rows,r=mod.source_topic("none","TITLE_ABS:x",puller=empty)
        self.assertEqual(rows,[])
        self.assertTrue(r["query_returned_zero_is_not_trait_negative"])

    def test_metadata_never_claimed_taxon_measurement(self):
        row=mod.source_row(article("https://doi.org/10.1234/AbC","A flower experiment"),"UV")
        self.assertEqual(row["doi"],"10.1234/abc")
        self.assertEqual(row["original_species_count_verified_from_this_index"],"UNKNOWN")
        self.assertEqual(row["trait_observation_status"],"NOT_READ_FROM_SOURCE_DATA")
        self.assertEqual(row["primary_data_download_status"],"NOT_SCREENED")

    def test_registry_taxon_grain_and_original_absences(self):
        x=json.loads((HERE/"curated_original_floral_trait_pollinator_data_sources.json").read_text())
        sources={r["id"]:r for r in x["sources"]}
        self.assertEqual(x["n_discovered_curated_database_study_sources"],26)
        self.assertEqual(sources["fabales_2022"]["source_unit"],"GENUS_NOT_SPECIES")
        self.assertEqual(sources["costus_visual_VOC_2026"]["source_reported_n"],2)
        self.assertEqual(sources["angiosperm_pollination_2023"]["source_reported_n"],1201)
        self.assertEqual(sources["colour_change_review_2025"]["positive_negative_observability"],
                         "POSITIVE_ONLY_no_measured_negatives")
        self.assertTrue(x["distinct_sources_not_distinct_species"])
        self.assertTrue(all(r["not_a_global_nectar_guide_present_binary"] for r in sources.values()))

if __name__=="__main__":
    unittest.main()
