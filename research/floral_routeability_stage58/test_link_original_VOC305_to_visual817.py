"""Mock-only original source identity records, no artificial VOC emission claim."""
import unittest
from link_original_VOC305_to_visual817 import attach_accepted

def visual817():
    out=[]
    for i in range(817):
        out.append({"gbif_accepted_species_key":str(900000+i),
                    "source_UV_pattern_directly_measured_or_unknown":("1" if i==0 else "0" if i==1 else ""),
                    "original_Oliveira2025_UV_mean_source":"True" if i in (0,1,2) else "False",
                    "original_Ohashi2015_spectral_taxon_source":"True" if i==0 else "False",
                    "original_2025_literature_colour_change_reported":"False"})
    return out

def source305():
    return [{
        "original_VOC_source_taxon_verbatim":f"Mockus plantus{i}",
        "original_VOC_source_canonical_binomial_or_unknown":f"Mockus plantus{i}",
        "source_wind_column_NOT_airflow_velocity":True
    } for i in range(305)]

class VOCAcceptedVisualModalityNoFalseJointInference(unittest.TestCase):
    def test_some_shared_accepted_species_are_not_same_individual(self):
        vac=source305();vis=visual817()
        lookups={
            "Mockus plantus0":{"taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED","gbif_accepted_usage_key":900000},
            "Mockus plantus1":{"taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED","gbif_accepted_usage_key":900001},
            "Mockus plantus2":{"taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED","gbif_accepted_usage_key":990005}}
        rows,res=attach_accepted(vac,lookups,vis)
        self.assertEqual(res["n_distinct_VOC_accepted_species"],3)
        self.assertEqual(res["n_accepted_VOC_species_also_in_visual_source817"],2)
        self.assertEqual(res["n_combined_visual817_and_VOC_accepted_botanical_source_UNION"],818)
        self.assertEqual(res["same_species_modalities_but_NOT_same_voucher_or_original_native_sample"]["measured_UV_spatial_binary"],2)
        self.assertTrue(res["no_identified_VOC_x_UV_x_Bombus_env_wind_pollen_interaction"])
        self.assertTrue(rows[0]["candidate_joint_MODALITY_evidence_NOT_same_individual"])

    def test_unmapped_from_gbif_is_not_scentless_nor_no_visual_guides(self):
        rows,r=attach_accepted(source305(),{},visual817())
        self.assertEqual(r["n_distinct_VOC_accepted_species"],0)
        self.assertEqual(r["n_accepted_VOC_species_also_in_visual_source817"],0)
        self.assertTrue(rows[0]["floral_VOC_unobserved_species_not_scentless"])
        self.assertTrue(rows[0]["source_visual_unobserved_species_not_without_guide"])
        self.assertEqual(rows[0]["gbif_accepted_species_key_or_unknown"],"")

    def test_source_species_denominator_and_accepted_reference_uniqueness(self):
        with self.assertRaisesRegex(ValueError,"305_VOC_OR_817"):
            attach_accepted(source305()[:-1],{},visual817())
        dup=visual817()
        dup[1]["gbif_accepted_species_key"]=dup[0]["gbif_accepted_species_key"]
        with self.assertRaisesRegex(ValueError,"817_ACCEPTED_KEY_IDENTITY"):
            attach_accepted(source305(),{},dup)

if __name__=="__main__":unittest.main()
