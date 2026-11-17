"""Adversarial source-only DoPI macro external visitor evidence tests."""
import csv,importlib.util,unittest,tempfile
from pathlib import Path
from unittest.mock import patch

p=Path(__file__).with_name("original_DoPI2026_external_study_hue_guild_macro.py")
sp=importlib.util.spec_from_file_location("st76b_original_DoPI",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class OriginalDopiPositiveStudyMacro(unittest.TestCase):
    def test_original_source_v2_exact_record_sha_and_DPI_release(self):
        self.assertEqual(m.EXPECTED_DOPI_ROWS,676900)
        self.assertEqual(m.SOURCE_DOPI_SIZE,384896230)
        self.assertEqual(len(m.SOURCE_DOPI_SHA),64)
        self.assertEqual(len(m.SOURCE_NHM_SHA),64)
        self.assertEqual(m.MIN_STUDIES,10)

    def test_positive_Bombus_species_is_separate_from_other_bees(self):
        z={"pollinator_order":"Hymenoptera","pollinator_family":"Apidae",
           "pollinator_species":"Bombus terrestris"}
        self.assertEqual(m.source_guild(z),"Bombus")
        z["pollinator_species"]="Apis mellifera"
        self.assertEqual(m.source_guild(z),"other_bee")
        z["pollinator_order"]="Diptera"
        self.assertEqual(m.source_guild(z),"")

    def test_unobserved_guild_is_not_negative_evidence(self):
        study="10.1111/abc"
        hue={"gentiana lutea":"yellow","linum perenne":"white"}
        positive={"positive_visits_or_pollen_123":{study:set(hue)}}
        source={"positive_visits_or_pollen_123":{
             study:{"Bombus":{"gentiana lutea"}}}}
        cohort,actual,gates=m.compare_published_source_hue_composition(
            positive,source,hue,"positive_visits_or_pollen_123",("yellow","white"))
        self.assertEqual(len(cohort),1)
        self.assertEqual(len(actual),0)
        self.assertEqual(gates["one_source_guild_no_positive_documentation"],1)

    def test_complete_shared_species_is_not_independent_preference(self):
        study="10.1111/test"
        hue={"gentiana lutea":"yellow","linum perenne":"white"}
        positive={"positive_visits_or_pollen_123":{study:set(hue)}}
        source={"positive_visits_or_pollen_123":{
             study:{"Bombus":set(hue),"other_bee":set(hue)}}}
        cohort,actual,gates=m.compare_published_source_hue_composition(
            positive,source,hue,"positive_visits_or_pollen_123",("yellow","white"))
        self.assertEqual(len(cohort),1)
        self.assertEqual(len(actual),1)
        self.assertEqual(actual[0]["source_plant_species_both_guilds_documented"],2)
        self.assertEqual(actual[0]["source_positive_study_difference_yellow_share_Bombus_minus_other_bee"],0.)

    def test_source_guild_counts_do_not_select_study_hue_frame(self):
        study="X"
        hue={"gentiana lutea":"yellow","linum perenne":"white"}
        positive={"positive_visits_or_pollen_123":{study:set(hue)}}
        first={"positive_visits_or_pollen_123":{
             study:{"Bombus":{"gentiana lutea"},"other_bee":{"linum perenne"}}}}
        second={"positive_visits_or_pollen_123":{
             study:{"other_bee":set(hue)}}}
        a,_,_=m.compare_published_source_hue_composition(
            positive,first,hue,"positive_visits_or_pollen_123",("yellow","white"))
        b,_,_=m.compare_published_source_hue_composition(
            positive,second,hue,"positive_visits_or_pollen_123",("yellow","white"))
        self.assertEqual(a,b)

    def test_doPI_source_grade_four_and_unknown_never_visit_negative(self):
        headers=["plant_species","pollinator_species","pollinator_order",
            "pollinator_family","pollination","doi","publication"]
        rows=[{
             "plant_species":"Gentiana lutea",
             "pollinator_species":"Bombus terrestris",
             "pollinator_family":"Apidae","pollinator_order":"Hymenoptera",
             "pollination":grade,"doi":"10.1111/foo","publication":""
            } for grade in ("1","2","3","4","")]
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"small.csv"
            with path.open("w",newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=headers);w.writeheader();w.writerows(rows)
            with patch.object(m,"EXPECTED_DOPI_ROWS",5):
                positive,guild,pubs,stats=m.original_positive_doPI_dedup(
                    path,{"gentiana lutea":"yellow"})
        self.assertEqual(stats["original_DOPI_v2_source_rows"],5)
        self.assertEqual(positive["positive_visits_or_pollen_123"]["10.1111/foo"],{"gentiana lutea"})
        self.assertEqual(guild["confirmed_1"]["10.1111/foo"]["Bombus"],{"gentiana lutea"})
        self.assertEqual(guild["pollen_evidence_12"]["10.1111/foo"]["Bombus"],{"gentiana lutea"})
        self.assertEqual(stats["matched_source_rows_missing_pub_or_admitted_grade"],2)

    def test_original_DOI_normalize_and_study_fallback(self):
        self.assertEqual(m.doi_id("https://doi.org/10.1111/Foo.2025"),"10.1111/foo.2025")
        self.assertEqual(m.doi_id("not recorded"),"")
        self.assertEqual(m.study_id({"doi":"NA","publication":"Paper 1998"}),"paper 1998")

    def test_bootstrap_only_qualifies_at_ten_original_publications(self):
        self.assertIsNone(m.study_bootstrap([0.,1.]))
        value=m.study_bootstrap([0.]*11)
        self.assertEqual(value,[0.,0.])

if __name__=="__main__":
    unittest.main()
