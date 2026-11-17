"""Stage76 genuine macro native-site source source-free invariants."""
from __future__ import annotations
import importlib.util,unittest
from collections import defaultdict
from pathlib import Path
from unittest.mock import patch

p=Path(__file__).with_name("official_native_WCVP_Stage75_macro_field_guilds.py")
s=importlib.util.spec_from_file_location("st76_native",p)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)

def row(species,hue,b=10,o=2):
    return {
      "color_contrast":"yellow_vs_white",
      "Study_id":"A","Network_id":"n1","Year":"2020",
      "species":species,"genus":species.split()[0],
      "hue":hue,
      "original_sampling_method":"standard",
      "original_reported_pollinator_taxa_scope":"all",
      "Bioregion":"Atlantic","Country":"France",
      "EuPPollNet_habitat":"Grassland",
      "original_strict_Bombus_species_visit_records":str(b),
      "original_strict_other_bee_species_visit_records":str(o)
    }

def fixture():
    rows=[row("gentiana lutea","yellow"),
          row("linum perenne","white")]
    source={("A","n1","2020"):{
      "original_valid_polygon":("FRA","WITHIN_TDWG_L3_POLYGON",False),
      "repaired_invalid_polygon_sensitivity":("FRA","WITHIN_TDWG_L3_POLYGON",False),
      "original_site_coordinates_in_source":1}}
    accepted={"gentiana lutea":{"1"},"linum perenne":{"2"}}
    states=defaultdict(lambda:defaultdict(set))
    states["gentiana lutea"]["FRA"].add("native")
    states["linum perenne"]["FRA"].add("native")
    return rows,source,accepted,states

class Stage76NativeMacroSourceTests(unittest.TestCase):
    def test_WCVP_unlisted_native_is_UNKNOWN_never_introduced(self):
        rows,sites,accepted,states=fixture()
        self.assertEqual(m.native.classify_origin("gentiana lutea","ITA",accepted,states),
            "WCVP_L3_NOT_RECORDED_UNKNOWN")
        self.assertEqual(m.native.classify_origin("linum perenne","FRA",accepted,states),
            "WCVP_NATIVE_L3_COMPATIBLE")
        self.assertEqual(m.native.classify_origin("broken","FRA",accepted,states),
            "WCVP_SPECIES_NOT_EXACT_ACCEPTED")

    def test_native_cohort_cannot_depend_on_guild_visit_counts(self):
        rows,sites,accepted,states=fixture()
        with patch.object(m,"CONTRASTS",{"yellow_vs_white":("yellow","white",1)}):
            first,a=m.define_pre_guild_native_hue_frames(rows,sites,accepted,states)
            rows[0]["original_strict_Bombus_species_visit_records"]="0"
            rows[0]["original_strict_other_bee_species_visit_records"]="999999"
            other,b=m.define_pre_guild_native_hue_frames(rows,sites,accepted,states)
        self.assertEqual(first,other)
        self.assertEqual(a,b)
        self.assertEqual(a[("original_valid_polygon","yellow_vs_white")]["source_original_net_after_WCVP_native_before_guild"],1)

    def test_introduced_region_removes_plant_not_pretend_no_visitation(self):
        rows,sites,acc,states=fixture()
        states["linum perenne"]["FRA"]={"introduced"}
        with patch.object(m,"CONTRASTS",{"yellow_vs_white":("yellow","white",1)}):
            frame,audit=m.define_pre_guild_native_hue_frames(rows,sites,acc,states)
        self.assertEqual(frame[("original_valid_polygon","yellow_vs_white")],{})
        self.assertEqual(audit[("original_valid_polygon","yellow_vs_white")]["WCVP_INTRODUCED_L3_RECORDED"],1)
        self.assertTrue(m.ORIGIN_CEILING.startswith("REGIONAL_COMPATIBILITY"))

    def test_study_area_missing_never_arbitrarily_matched_to_country(self):
        rows,sites,acc,states=fixture()
        sites[("A","n1","2020")]["original_valid_polygon"]=(
            "","NO_SINGLE_UNAMBIGUOUS_SOURCE_COORDINATE",False)
        with patch.object(m,"CONTRASTS",{"yellow_vs_white":("yellow","white",1)}):
            frame,audit=m.define_pre_guild_native_hue_frames(rows,sites,acc,states)
        self.assertEqual(len(frame[("original_valid_polygon","yellow_vs_white")]),0)
        self.assertEqual(audit[("original_valid_polygon","yellow_vs_white")]["SITE_TDWG_L3_UNRESOLVED"],2)

    def test_border_native_is_excluded_only_under_border_sensitive_gate(self):
        rows,sites,acc,states=fixture()
        sites[("A","n1","2020")]["original_valid_polygon"]=(
            "FRA","NEAR_BOUNDARY_SENSITIVITY",True)
        with patch.object(m,"CONTRASTS",{"yellow_vs_white":("yellow","white",1)}):
            frame,audit=m.define_pre_guild_native_hue_frames(rows,sites,acc,states)
        self.assertEqual(len(frame[("original_valid_polygon","yellow_vs_white")]),0)
        self.assertEqual(audit[("original_valid_polygon","yellow_vs_white")]["WCVP_NATIVE_L3_NEAR_BORDER_SENSITIVITY_EXCLUDED"],2)

    def test_only_after_guild_selection_look_at_Bombus(self):
        rows,sites,acc,states=fixture()
        frame,_=m.define_pre_guild_native_hue_frames if False else (None,None)
        outcome=m.load_guild_outcome_only_after_frame_frozen(rows)
        self.assertEqual(outcome[(("A","n1","2020"),"gentiana lutea")]["B"],10)
        first=outcome.copy()
        rows[0]["original_strict_Bombus_species_visit_records"]="0"
        after=m.load_guild_outcome_only_after_frame_frozen(rows)
        self.assertNotEqual(first,after)

    def test_repaired_source_changes_geo_not_guesses_plant_ancestry(self):
        rows,sites,accepted,states=fixture()
        sites[("A","n1","2020")]["original_valid_polygon"]=(
            "","MULTIPLE_OR_ZERO_TDWG_POLYGON_CONTAINS",False)
        with patch.object(m,"CONTRASTS",{"yellow_vs_white":("yellow","white",1)}):
            f,_=m.define_pre_guild_native_hue_frames(rows,sites,accepted,states)
        self.assertEqual(len(f[("original_valid_polygon","yellow_vs_white")]),0)
        self.assertEqual(len(f[("repaired_invalid_polygon_sensitivity","yellow_vs_white")]),1)

    def test_existing_source_SHA_guard(self):
        self.assertEqual(len(m.STAGE75_HUES_SHA),64)
        self.assertEqual(len(m.STAGE75_MAIN_SHA),64)
        with self.assertRaisesRegex(ValueError,"SOURCE_DERIVED_SHA_CHANGED"):
            m.verify_sha(Path(__file__),m.STAGE75_HUES_SHA)

    def test_source_bioregion_is_not_measured_wind(self):
        fake={"mode":"original_valid_polygon","color_contrast":"yellow_vs_white",
              "Bioregion":"Atlantic","Study_id":"A",
              "original_null_score":3.,"original_null_information":5.}
        result=m.source_bioregions([fake])
        self.assertEqual(result[0]["source_local_null_score_ratio_if_information"],0.6)
        self.assertTrue(result[0]["regional_bioregion_not_wind_VOC_climate_temperature"])

if __name__=="__main__":
    unittest.main()
