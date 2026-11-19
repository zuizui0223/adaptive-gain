"""Source-free GIFT conditional spatial arm tests, not fake field evidence."""
import tempfile,unittest,zipfile
from pathlib import Path
import numpy as np,pandas as pd
from compare_gift_animal_wind_hue_geographic_regimes import (
  source_modes,model_design,geographically_blocked_beta,full_hue_table,AGG,COLORS_ALL
)

class ModeSpatialGuards(unittest.TestCase):
    def test_non_genuine_original_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            fn=Path(d)/"fake.zip"
            with zipfile.ZipFile(fn,"w") as z:z.writestr("fake","dataset")
            with self.assertRaises(ValueError):source_modes(fn)
    def test_never_use_unreported_hue_in_some_mode_as_measurement(self):
        n=4
        data=pd.DataFrame(index=range(n))
        for mode in ("animal","wind"):
            for hue in COLORS_ALL:
                for _,suffix in AGG:data[f"{mode}_hue_{hue}_{suffix}"]=.05
        a,names=full_hue_table(data)
        self.assertEqual(a.shape,(4,66));self.assertEqual(len(names),66)
        data.loc[0,"wind_hue_yellow_mean_of_genus_fractions"]=np.nan
        with self.assertRaises(ValueError):full_hue_table(data)
    def test_genuine_geoblocks_preserve_mode_hue_pairs(self):
        rng=np.random.default_rng(20261119)
        lats=np.repeat(np.arange(-40,60,10),6)
        lons=np.tile([-120,-80,-40,0,40,80],10)
        frame=pd.DataFrame({"latitude":lats,"longitude":lons})
        X=pd.DataFrame({"const":np.ones(len(frame)),"wind":rng.normal(size=len(frame))})
        Y=np.column_stack([.5+.1*X.wind,.2+.02*X.wind,.3+.08*X.wind])
        r,b=geographically_blocked_beta(frame,X,Y,20,45,99,20261119)
        self.assertEqual(r.shape[1:],(2,3))
        self.assertGreaterEqual(b,10)
        self.assertAlmostEqual(np.mean(r[:,1,0]-r[:,1,1]),.08,places=5)
    def test_mode_interaction_is_not_read_as_unobserved_source_column(self):
        rng=np.random.default_rng(8)
        n=55
        fields={"wind":rng.normal(size=n),"temperature":rng.normal(size=n),
           "logprec":rng.normal(size=n),"solar":rng.normal(size=n),
           "vapour":rng.normal(size=n),"animal_coverage":rng.normal(size=n),
           "wind_coverage":rng.normal(size=n),"animal_log_plant_hues":rng.normal(size=n),
           "wind_log_plant_hues":rng.normal(size=n),"latitude":rng.normal(size=n),
           "latitude_sq":rng.normal(size=n),"sin_longitude":rng.normal(size=n),
           "cos_longitude":rng.normal(size=n),"log_bombus_richness":rng.normal(size=n),
           "log_gbif_cells":rng.normal(size=n)}
        x=model_design(pd.DataFrame(fields),True)
        self.assertIn("wind_x_bombus",x)
        self.assertEqual(x.shape[1],16+1)
if __name__=="__main__":unittest.main()
