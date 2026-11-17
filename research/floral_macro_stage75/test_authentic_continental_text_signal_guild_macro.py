"""Stage75 source-free tests of macro visual TEXT and receiver-guild sampling."""
import importlib.util,unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch
p=Path(__file__).with_name("authentic_continental_text_signal_guild_macro.py")
spec=importlib.util.spec_from_file_location("macro75",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def trait(**kw):
    d={"taxon":"Gentiana punctata","flower colour":"","petal colour":"",
       "corolla colour":"","wfo":""}
    d.update(kw)
    return d

def row(hue,sp,network="n1"):
    return {
      "Study_id":"S1","Network_id":network,"Year":"2020",
      "species":sp.casefold(),"genus":sp.split()[0].casefold(),"hue":hue,
      "original_sampling_method":"Focal_observation",
      "source_observed_bombus_any_rank":500 if hue=="yellow" else 0,
    }

class MainMacroAdmissionTests(unittest.TestCase):
    def test_true_source_lexical_positive_not_uv_spatial_guide(self):
        r=m.source_text_trait(trait(**{"flower colour":"white, violet",
               "petal colour":"spotted, yellow"}))
        self.assertEqual(r["source_reported_hue_families"],["purple","white","yellow"])
        self.assertEqual(r["source_exclusive_lexical_hue"],"")
        self.assertEqual(r["source_colour_descriptor_spot_positive_report"],1)
        self.assertEqual(r["original_UV_spatial_guide_measured"],"UNKNOWN")
        self.assertTrue(r["source_spot_token_absent_is_NOT_negative"])

    def test_no_color_record_is_unknown_not_white(self):
        r=m.source_text_trait(trait())
        self.assertEqual(r["source_colour_recorded"],0)
        self.assertEqual(r["source_exclusive_lexical_hue"],"")
        self.assertEqual(r["source_colour_descriptor_spot_positive_report"],0)
        self.assertTrue(r["source_spot_token_absent_is_NOT_negative"])

    def test_one_colour_family_as_text_does_not_prove_true_monochromatic(self):
        r=m.source_text_trait(trait(**{"petal colour":"yellowish, golden"}))
        self.assertEqual(r["source_reported_hue_families"],["yellow"])
        self.assertEqual(r["source_exclusive_lexical_hue"],"yellow")
        self.assertTrue(r["source_lexical_single_hue_does_not_prove_monochromatic_biology"])

    def test_hues_chosen_before_guild_availability_observations(self):
        a=[row("yellow","Gentiana lutea"),row("white","Linum perenne")]
        f=m.predefine_color_pair_frames({("S1","n1","2020"):a})
        self.assertEqual(len(f[("yellow","white")]),1)
        a[0]["source_observed_bombus_any_rank"]=0
        a[1]["source_observed_bombus_any_rank"]=12000
        f2=m.predefine_color_pair_frames({("S1","n1","2020"):a})
        self.assertEqual(f,f2)

    def test_within_network_positive_bombus_alignment_null_score(self):
        rows=[row("yellow","Gentiana lutea"),row("white","Linum perenne")]
        e={
          (("S1","n1","2020"),"gentiana lutea"):Counter(B=9,O=1),
          (("S1","n1","2020"),"linum perenne"):Counter(B=1,O=9),
        }
        scored,why=m.null_score_pair(rows,e,("yellow","white"))
        self.assertEqual(why,"INFORMATIVE")
        self.assertGreater(scored["original_null_score"],0)
        self.assertGreater(scored["original_null_information"],0)
        summary,_=m.study_block_summary([scored])
        self.assertEqual(summary["informative_study_ids"],1)
        self.assertTrue(summary["null_score_not_glm_fitted_beta"])

    def test_bombus_nonreport_is_not_verified_local_absence(self):
        rows=[row("yellow","Gentiana lutea"),row("white","Linum perenne")]
        e={
           (("S1","n1","2020"),"gentiana lutea"):Counter(O=4),
           (("S1","n1","2020"),"linum perenne"):Counter(O=8),
        }
        score,why=m.null_score_pair(rows,e,("yellow","white"))
        self.assertIsNone(score)
        self.assertEqual(why,"ONLY_ONE_BEE_GUILD_OBSERVED_IN_INFORMATIVE_SOURCE_NETWORK")

    def test_no_bee_data_not_a_negative_response(self):
        rows=[row("yellow","Gentiana lutea"),row("white","Linum perenne")]
        score,why=m.null_score_pair(rows,{},("yellow","white"))
        self.assertIsNone(score)
        self.assertEqual(why,"NO_STRICT_BEE_SOURCE_EVENTS")

    def test_compared_colors_must_be_both_recorded_in_same_network(self):
        data={("S1","n1","2020"):[row("yellow","Gentiana lutea")],
              ("S1","n2","2020"):[row("white","Linum perenne","n2")]}
        frames=m.predefine_color_pair_frames(data)
        self.assertEqual(len(frames[("yellow","white")]),0)

    def test_study_bootstrap_is_not_species_phylogenetic_interval(self):
        f=[{
            "Study_id":"S1","original_null_score":1.,
            "original_null_information":2.,
            "original_field_strict_species_rank_bee_event_count":7,
            "has_two_colour_states_in_same_genus":0,
        },{
            "Study_id":"S2","original_null_score":-2.,
            "original_null_information":3.,
            "original_field_strict_species_rank_bee_event_count":8,
            "has_two_colour_states_in_same_genus":0,
        }]
        out,studies=m.study_block_summary(f)
        self.assertEqual(out["informative_study_ids"],2)
        self.assertEqual(out["informative_networks"],2)
        self.assertTrue(out["source_study_bootstrap_not_phylogenetic_confidence_interval"])
        self.assertEqual(len(out["descriptive_study_block_bootstrap_percentile_95"]),2)

    def test_source_blob_sha_pins_published_artifacts(self):
        self.assertEqual(len(m.NHM_SHA256),64)
        self.assertEqual(len(m.NETWORK_SHA256),64)
        with self.assertRaisesRegex(ValueError,"SOURCE_DERIVED_ARTIFACT_SHA_CHANGED"):
            m.source_sha(Path(__file__),m.NHM_SHA256)

if __name__=="__main__":
    unittest.main()
