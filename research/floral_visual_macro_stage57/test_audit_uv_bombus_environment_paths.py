"""Stage57 mock-only tests never use artificial data as empirical results."""
from pathlib import Path
import tempfile,unittest
import numpy as np
import pandas as pd
from audit_uv_bombus_environment_paths import load_verified_inputs,report

def mock_frames():
    original=[];bee=[]
    classes=[0]*81+[1]*78
    permutation=np.random.default_rng(42).permutation(159)
    for i in range(159):
        k=str(100000+i)
        origclass=classes[permutation[i]]
        original.append({
          "gbif_accepted_species_key":k,
          "source_2016_UV_pattern":origclass,
          "original_2016_source_genus_or_unknown":(
              "Potentilla" if i<130 else "Ivesia" if i<145
              else "Drymocallis" if i<154 else "Otherus"),
          "published_uvb_mean":2500+12.1*i+100*np.sin(i*0.6),
          "published_annual_temp_mean":5+0.12*i+np.cos(i*.22),
          "published_precip_mean":650+i%23*31,
          "published_altitude_mean":300+i%31*19,
          "published_latitude_mean":52-i*0.14,
        })
        b=(i%7)+1; allb=90+i%43
        bee.append({
          "gbif_accepted_species_key":k,
          "source_qualified_records":12,
          "source_eligible_bee_hex_cells":3,
          "modelled_Bombus_names_mean":b,
          "modelled_all_bee_names_mean":allb,
          "modelled_Bombus_share_ratio_of_means_or_unknown":b/allb,
          "GBIF_sample_not_native_range":True,
        })
    return pd.DataFrame(original),pd.DataFrame(bee)

class EnvironmentBeeUVSourceContracts(unittest.TestCase):
    def _open(self,a,b):
        with tempfile.TemporaryDirectory() as d:
            pa=Path(d)/"original.csv";pb=Path(d)/"bee.csv"
            a.to_csv(pa,index=False);b.to_csv(pb,index=False)
            return load_verified_inputs(pa,pb)

    def test_source_159_same_key_provenance_and_dual_submodels(self):
        a,b=mock_frames()
        d=self._open(a,b)
        self.assertEqual(len(d),159)
        result=report(d)
        self.assertTrue(result["model_is_not_causal_SEM_or_an_indirect_effect"])
        self.assertTrue(result["source_coverage"]["no_p_values_or_indirect_causal_effects"])
        self.assertTrue(np.isfinite(result["observational_UV_binary_regressions"]
            ["environment_plus_grouped_genus_plus_pollinator"]["AIC"]))

    def test_incorrect_pattern_labels_refused(self):
        a,b=mock_frames()
        a.loc[0,"source_2016_UV_pattern"]=9
        with self.assertRaisesRegex(ValueError,"DIRECT_UV_POSITIVE_NEGATIVE"):
            self._open(a,b)

    def test_wrong_native_provenance_never_treated_as_site(self):
        a,b=mock_frames()
        b.loc[0,"GBIF_sample_not_native_range"]=False
        with self.assertRaisesRegex(ValueError,"NATIVE_PROVENANCE"):
            self._open(a,b)

    def test_species_key_mismatch_and_duplicate_refused(self):
        a,b=mock_frames()
        b.loc[0,"gbif_accepted_species_key"]=str(999999)
        with self.assertRaisesRegex(ValueError,"SAME_159"):
            self._open(a,b)
        a,b=mock_frames()
        b.loc[0,"gbif_accepted_species_key"]=b.loc[1,"gbif_accepted_species_key"]
        with self.assertRaisesRegex(ValueError,"NONUNIQUE"):
            self._open(a,b)

    def test_ratio_denominator_provenance_and_true_missing(self):
        a,b=mock_frames()
        b.loc[0,"modelled_Bombus_share_ratio_of_means_or_unknown"]=0.999
        with self.assertRaisesRegex(ValueError,"FRACTION_SOURCE"):
            self._open(a,b)
        a,b=mock_frames()
        b.loc[0,"modelled_all_bee_names_mean"]=np.nan
        with self.assertRaisesRegex(ValueError,"RICHNESS_UNKNOWN"):
            self._open(a,b)

    def test_low_coverage_never_becomes_zero_signal(self):
        a,b=mock_frames()
        b.loc[0,"source_qualified_records"]=0
        b.loc[0,"source_eligible_bee_hex_cells"]=0
        d=self._open(a,b)
        self.assertEqual(len(d),158)
        self.assertNotIn(str(100000),set(d["gbif_accepted_species_key"]))

if __name__=="__main__":
    unittest.main()
