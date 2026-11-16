"""Stage49 mock-only evidence-type and source-study dedup checks."""
import unittest
from assemble_literature_visual_species import assemble,_canonical

def uv(name,pattern):
    return {"taxon_as_published":name,
            "uv_pattern_present":int(pattern),
            "uv_pattern_type":"bullseye" if pattern else "uniform_uv_absorbing"}

def cb(name,continent,n):
    genus,epithet=name.split()
    return {"taxon_binomial_as_published":name,
            "continent":continent,
            "floral_anther_position_code":"E",
            "original_herbarium_samples":n}

class OriginalPaperVisualTraits(unittest.TestCase):
    def test_uncertain_genus_not_converted_into_species(self):
        self.assertEqual(_canonical("Eugenia sp."),"")
        self.assertEqual(_canonical("Caltha palustris L."),"Caltha palustris")

    def test_keep_UV_pattern_separate_from_UVP_temporal_slope(self):
        originals=[uv("Mockus alpha",1),uv("Mockus beta",0)]
        originals.extend(uv(f"Mockus extra{i}",0) for i in range(78))
        cbsource=[
            cb("Mockus alpha","N. America",4),
            cb("Mockus alpha","Eurasia",8),
            cb("Caltha palustris","Eurasia",10)
        ]
        rows,s=assemble(originals,cbsource)
        self.assertEqual(len(rows),82)
        self.assertEqual(s["UV_photo_2021_original_80_rows"],80)
        self.assertEqual(s["original_2020_continent_taxon_rows"],3)
        self.assertEqual(s["original_2020_unique_literal_binomial_names"],2)
        self.assertEqual(s["literal_cross_paper_binomial_string_overlap_n"],1)
        c=[x for x in rows if x["original_study_doi"]=="10.1016/j.cub.2020.08.077"]
        self.assertEqual(len(c),2)
        self.assertTrue(all(r["UV_spatial_guide_pattern_source_status"]==
                            "NOT_CLASSIFIED_BY_TABLE_S1" for r in c))
        self.assertEqual(next(r for r in c if r["published_taxon_string"]=="Mockus alpha")
                         ["published_sample_count"],12)
        p=[x for x in rows if x["original_study_doi"]=="10.3389/fpls.2021.618028"]
        self.assertEqual(p[0]["UV_spatial_guide_pattern_source_status"],
                         "SOURCE_MEASURED_PATTERNED")
        self.assertEqual(p[1]["UV_spatial_guide_pattern_source_status"],
                         "SOURCE_MEASURED_UNIFORM")
        self.assertTrue(s["no_inference_that_2020_UVP_slope_means_guide_presence"])

    def test_source_80_denominator_hard_stop(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_UV_80_SOURCE_GRANULARITY"):
            assemble([uv("Mockus a",1)],[cb("Mockus alpha","Australia",1)])

    def test_conflicting_structural_evidence_same_taxon_rejected(self):
        originals=[uv(f"Mockus i{i}",0) for i in range(80)]
        a=cb("Mockus alpha","Australia",1)
        b=cb("Mockus alpha","Eurasia",1)
        b["floral_anther_position_code"]="C"
        with self.assertRaisesRegex(ValueError,"NO_GO_FLORAL_ANATOMY_CONFLICT"):
            assemble(originals,[a,b])

if __name__=="__main__":
    unittest.main()
