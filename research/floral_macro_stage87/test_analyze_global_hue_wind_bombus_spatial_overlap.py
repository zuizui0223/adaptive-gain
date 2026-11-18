"""Source-free scientific null/NA guards for Stage87E spatial correspondence."""
from __future__ import annotations
import tempfile,unittest,zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from analyze_global_hue_wind_bombus_spatial_overlap import (
    verified_csv,source_blocks,all_outcomes,spatial_bootstrap,COLORS,OUTCOMES,
    WCVP_CLIMATE_ZIP_SHA,CLIMATE_MEMBER,CLIMATE_RECEIPT,bh_by_columns,
)

class Stage87EGuards(unittest.TestCase):
    def test_fictitious_source_refused_even_valid_zip(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"fake.zip"
            with zipfile.ZipFile(path,"w") as z:z.writestr("fake.csv","not source")
            with self.assertRaises(ValueError):
                verified_csv(path,WCVP_CLIMATE_ZIP_SHA,CLIMATE_MEMBER,CLIMATE_RECEIPT)
    def test_geoblocks_use_declared_coordinates_not_species_name(self):
        d=pd.DataFrame({"latitude":[20.,21.,-15.],
                        "longitude":[100.,120.,-80.]})
        a=source_blocks(d,20,45)
        self.assertEqual(a.shape,(3,2))
        self.assertNotEqual(tuple(a[0]),tuple(a[-1]))
    def test_source_record_missing_hue_never_zero_imputed(self):
        traits={r[0]:[.2,.3] for r in OUTCOMES}
        x=pd.DataFrame(traits)
        self.assertEqual(all_outcomes(x).shape,(2,len(OUTCOMES)))
        x.iloc[0,0]=np.nan
        with self.assertRaises(ValueError):all_outcomes(x)
    def test_block_bootstrap_behaviour_on_simulated_fraction_only(self):
        rng=np.random.default_rng(5)
        lat=np.repeat(np.arange(-40,80,10),3)
        lon=np.tile(np.array([-100.,0.,100.]),12)
        d=pd.DataFrame({"latitude":lat,"longitude":lon})
        x=pd.DataFrame({"const":np.ones(len(d)),"wind":rng.normal(size=len(d))})
        y=pd.DataFrame({"hue_green":np.clip(.25+.1*x.wind+rng.normal(scale=.01,size=len(d)),0,1)})
        result=spatial_bootstrap(d,x,y,reps=80,latitude_bin=20,longitude_bin=45)
        self.assertGreaterEqual(result["n_independent_approx_geographic_blocks"],10)
        self.assertEqual(result["intervals"].shape,(2,2,1))
        self.assertGreater(result["intervals"][0,1,0],0)
    def test_bh_family_cross_11_not_dynamically_selected_hues(self):
        rows=[]
        for level in ("pooled","genus_balanced"):
            for hue in COLORS:
                rows.append({"averaging":level,"hue":hue,
                    "coefficients":{"wind":{"HC3_exploratory_p":.03}}})
        bh_by_columns(rows,"coefficients")
        self.assertTrue(all(abs(r["coefficients"]["wind"]["BH_q_in_11_original_hues"]-.03)<1e-9
                            for r in rows))
if __name__=="__main__":unittest.main()
