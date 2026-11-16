"""Stage53 tests use only invented WCVP rows, not invented real native taxa."""
import csv,io,tempfile,unittest,zipfile
from pathlib import Path
from join_kew_wcvp_native_regions_to_uv_species import (
    process,source_species,_region_status
)

NAMES=["plant_name_id","ipni_id","taxon_rank","taxon_status",
       "family","genus_hybrid","genus","species_hybrid","species",
       "accepted_plant_name_id","taxon_name"]
AREAS=["plant_locality_id","plant_name_id","continent_code_l1",
       "continent","region_code_l2","region","area_code_l3","area",
       "introduced","extinct","location_doubtful"]

def pack(rows,headers):
    o=io.StringIO()
    w=csv.DictWriter(o,fieldnames=headers,delimiter="|")
    w.writeheader();w.writerows(rows)
    return o.getvalue()

def n(key,genus,epithet,status,accepted=""):
    return dict(plant_name_id=key,ipni_id="",taxon_rank="Species",
                taxon_status=status,family="Rosaceae",genus_hybrid="",
                genus=genus,species_hybrid="",species=epithet,
                accepted_plant_name_id=accepted,
                taxon_name=genus+" "+epithet)

def d(key,area,introduced="0",extinct="0",doubtful="0"):
    return dict(plant_locality_id="1",plant_name_id=key,continent_code_l1="1",
                continent="EUROPE",region_code_l2="10",region="Europe",
                area_code_l3=area,area=area,introduced=introduced,
                extinct=extinct,location_doubtful=doubtful)

class OfficialKewSourceContracts(unittest.TestCase):
    def example_zip(self):
        z=io.BytesIO()
        with zipfile.ZipFile(z,"w") as f:
            f.writestr("wcvp_names.csv",pack([
                n("1","Potentilla","erecta","Accepted"),
                n("2","Tormentilla","erecta","Synonym","1"),
                n("3","Potentilla","alba","Accepted"),
                n("4","Potentilla","unrelated","Accepted"),
            ],NAMES))
            f.writestr("wcvp_distribution.csv",pack([
                d("1","FRA","0"),
                d("2","FRA","1"), # conflict, must NOT accept
                d("2","ESP","0"), # synonym region must be joined
                d("3","ITA","0"),
                d("3","GER","0",doubtful="1"), # exclude doubtful
                d("4","POL","0") # unrelated plant never joined
            ],AREAS))
        z.seek(0)
        return zipfile.ZipFile(z)

    def test_WCVP_original_accepted_and_synonym_ranges_and_conflict(self):
        original={
          "100":{"gbif_accepted_species_key":"100",
                 "source_exact_binomial_candidates":["potentilla erecta","tormentilla erecta"],
                 "original_UV_spatial_pattern_binary":1},
          "101":{"gbif_accepted_species_key":"101",
                 "source_exact_binomial_candidates":["potentilla alba"],
                 "original_UV_spatial_pattern_binary":0}
        }
        with self.example_zip() as z:
            rows,receipt=process(original,z)
        indexed={r["gbif_accepted_species_key"]:r for r in rows}
        self.assertEqual(indexed["100"]["WCVP_accepted_plant_name_id_or_unknown"],"1")
        self.assertEqual(indexed["100"]["WCVP_confirmed_native_extant_WGSRPD_L3_areas"],["ESP"])
        self.assertEqual(indexed["100"]["WCVP_conflicting_WGSRPD_L3_areas_excluded"],["FRA"])
        self.assertEqual(indexed["101"]["WCVP_confirmed_native_extant_WGSRPD_L3_areas"],["ITA"])
        self.assertEqual(indexed["101"]["WCVP_doubtful_extinct_or_unknown_WGSRPD_L3_areas"],["GER"])
        self.assertTrue(receipt["native_area_is_TDWG_WGSRPD_L3_not_ISO_or_source_specimen_point"])
        self.assertTrue(receipt["no_modelled_Bombus_UV_pattern_effect_yet"])

    def test_absent_source_name_unknown_not_non_native(self):
        x={"999":{"gbif_accepted_species_key":"999",
                  "source_exact_binomial_candidates":["potentilla nonexistent"],
                  "original_UV_spatial_pattern_binary":1}}
        with self.example_zip() as z:
            rows,receipt=process(x,z)
        self.assertEqual(rows[0]["WCVP_match_status"],
                         "NO_EXACT_WCVP_ACCEPTED_OR_SYNONYM_NAME")
        self.assertEqual(rows[0]["WCVP_confirmed_native_extant_WGSRPD_L3_areas"],[])
        self.assertTrue(rows[0]["WCVP_taxonomic_concept_not_equivalent_to_GBIF_without_validation"])

    def test_missing_native_flag_does_not_imply_native(self):
        self.assertEqual(_region_status(d("1","FRA",introduced="",extinct="0",
                                          doubtful="0")),"UNRESOLVED_INVALID_SOURCE_STATUS")
        self.assertEqual(_region_status(d("1","FRA",introduced="0",extinct="1",
                                          doubtful="0")),"EXTINCT_REGION_NOT_CURRENT_NATIVE")

    def test_source_infraspecific_duplicated_records_are_one_GBIF_species(self):
        source=[
            {"accepted_GBIF_species_match_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
             "accepted_GBIF_taxon_key_or_empty":"100",
             "original_S1_author_full_binomial_candidate":"Ivesia lycopodioides",
             "source_measured_UV_pattern_present":"0"},
            {"accepted_GBIF_species_match_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
             "accepted_GBIF_taxon_key_or_empty":"100",
             "original_S1_author_full_binomial_candidate":"Ivesia lycopodioides",
             "source_measured_UV_pattern_present":"0"},
            {"accepted_GBIF_species_match_status":"ORIGINAL_S1_NAME_UNRESOLVED",
             "accepted_GBIF_taxon_key_or_empty":"",
             "source_measured_UV_pattern_present":"1"}
        ]
        d=source_species(source,expected=3)
        self.assertEqual(len(d),1)
        self.assertEqual(d["100"]["source_original_taxon_units"],2)
        self.assertEqual(d["100"]["source_exact_binomial_candidates"],
                         ["ivesia lycopodioides"])

if __name__=="__main__":
    unittest.main()
