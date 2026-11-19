"""Source-free Stage90B paired geographic block and native-range source guards."""
from __future__ import annotations
import tempfile,unittest,zipfile
from pathlib import Path
import numpy as np,pandas as pd
from source_reweighted_GIFT_hue_wind_Bombus_spatial_pairs import (
    input_range_table,adjusted_mode_outcomes,paired_geo_bootstrap,
)
from compare_gift_animal_wind_hue_geographic_regimes import COLORS_ALL,AGG

class SourceRangeReweightingGuards(unittest.TestCase):
    def test_not_recover_unauthenticated_source_zip(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"synthetic.zip"
            with zipfile.ZipFile(f,"w") as z:z.writestr("fake","data")
            with self.assertRaises(ValueError):input_range_table(f)
    def test_same_region_animal_and_wind_weighted_fraction_difference(self):
        ids=("AAA","BBB","CCC")
        r=[]
        for code in ids:
            for mode in ("animal","wind"):
                x={"TDWG_L3":code,"pollination_mode":mode}
                for h in COLORS_ALL:
                    x[f"hue_{h}_pooled_inverse_native_range"]=0.3 if mode=="animal" else 0.2
                    x[f"hue_{h}_genus_equal_inverse_native_range"]=0.3 if mode=="animal" else 0.2
                r.append(x)
        frame=pd.DataFrame({"TDWG_L3":ids})
        vals,names=adjusted_mode_outcomes(frame,pd.DataFrame(r))
        self.assertEqual(vals.shape,(3,66))
        self.assertEqual(names[0],("pooled",COLORS_ALL[0],"animal"))
        self.assertAlmostEqual(vals[0,0]-vals[0,1],vals[0,2])
        self.assertAlmostEqual(vals[0,2],0.1)
    def test_same_region_bootstrap_keeps_original_weight_difference_paired(self):
        rng=np.random.default_rng(101)
        lat=np.repeat(np.arange(-60,60,10),6)
        lon=np.tile([-140,-80,-20,40,100,160],12)
        frame=pd.DataFrame({"latitude":lat,"longitude":lon})
        x=pd.DataFrame({"const":np.ones(72),"wind":rng.normal(size=72)})
        y0=np.tile((.3+.04*x["wind"].to_numpy())[:,None],(1,66))
        y1=y0+np.tile((.12*x["wind"].to_numpy())[:,None],(1,66))
        sampled,nblock=paired_geo_bootstrap(frame,x,y0,y1,20,45,80,20261119)
        self.assertGreaterEqual(nblock,12)
        self.assertEqual(sampled.shape[1:],(2,2,66))
        self.assertAlmostEqual(np.mean(sampled[:,1,1,0]-sampled[:,1,0,0]),.12,places=5)

if __name__=="__main__":unittest.main()
