"""No real plant observations in tests: source-negative congener comparison QA."""
import csv,io,json,tempfile,unittest
from pathlib import Path
from match_uv_measured_negative_congeners_native import data_join,analysis

def source(key,pattern,lat=42,uvb=2800,temp=7,genus="Potentilla"):
    return {"gbif_accepted_species_key":str(key),
            "source_2016_UV_pattern":str(pattern),
            "original_2016_source_genus_or_unknown":genus,
            "published_latitude_mean":str(lat),
            "published_uvb_mean":str(uvb),
            "published_annual_temp_mean":str(temp)}

def kew(key,pattern,areas,matched=True):
    return {"gbif_accepted_species_key":str(key),
            "original_UV_spatial_pattern_binary":str(pattern),
            "WCVP_match_status":(
                "EXACT_AUTHOR_GENUS_SPECIES_SINGLE_WCVP_ACCEPTED_CONCEPT"
                if matched else "NO_EXACT_WCVP_ACCEPTED_OR_SYNONYM_NAME"),
            "WCVP_confirmed_native_extant_WGSRPD_L3_areas":json.dumps(areas),
            "WCVP_accepted_plant_name_id_or_unknown":str(key) if matched else ""}


class RealUVSignalNegativeComparatorContracts(unittest.TestCase):
    def test_source_positive_vs_source_measured_uniform_with_shared_native_area(self):
        a=[source(1,1),source(2,0,43,2880,7.5),source(3,0,45,2900,8,"Ivesia")]
        b=[kew(1,1,["FRA","ESP"]),kew(2,0,["ESP","ITA"]),
           kew(3,0,["ESP"])]
        data=data_join(a,b,expected=3)
        out,report=analysis(data)
        self.assertEqual(report["source_WCVP_species_with_any_native_L3"],3)
        tiers=report["tiers"]
        self.assertEqual(tiers["source_lat5_UVB700_temp4"]["n_nonoverlapping_opposite_UV_source_measured_congener_pairs"],1)
        target=[r for r in out if r["comparison_tier"]=="source_lat5_UVB700_temp4"][0]
        self.assertEqual(target["shared_original_native_area_codes"],["ESP"])
        self.assertTrue(target["does_not_prove_absence_of_visual_information_in_uniform_flower"])
        self.assertTrue(report["not_actual_sister_species_or_confirmed_native_cooccurrence"])

    def test_unmeasured_area_or_genus_mismatch_not_false_negative(self):
        a=[source(1,1),source(2,0,42,2800,7,"Potentilla"),
           source(3,0,42,2800,7,"Ivesia")]
        b=[kew(1,1,["FRA"]),kew(2,0,[],matched=False),kew(3,0,["FRA"])]
        rows,summary=analysis(data_join(a,b,expected=3))
        self.assertEqual(len(rows),0)
        self.assertEqual(summary["tiers"]["same_genus_and_overlapping_native_WGSRPD_L3"]
                         ["n_eligible_candidate_congener_pairs"],0)

    def test_UV_source_state_disagreement_hard_stop(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_UV_STATUS_CONFLICT"):
            data_join([source(1,1)],[kew(1,0,["FRA"])],expected=1)

    def test_native_geographic_unknown_does_not_become_true_zero(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_NATIVE_AREAS_WITH_UNRESOLVED"):
            data_join([source(1,1)],[kew(1,1,["FRA"],matched=False)],expected=1)


if __name__=="__main__":
    unittest.main()
