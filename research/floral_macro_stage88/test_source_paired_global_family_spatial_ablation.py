"""Source-free controls; no synthetic outcome is called field evidence."""
from __future__ import annotations
import tempfile,unittest,zipfile
from pathlib import Path
import numpy as np,pandas as pd
from source_paired_global_family_spatial_ablation import (
 source_family,paired_region_bootstrap,DESIGNS,COLORS
)

class SourcePairedGeography(unittest.TestCase):
    def test_nonauthor_binary_not_admitted_as_source_families(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("bogus","not original")
            with self.assertRaises(ValueError):source_family(p)
    def test_geographic_paired_bootstrap_preserves_common_region_ids(self):
        rng=np.random.default_rng(25)
        n=72
        frame=pd.DataFrame({"latitude":np.repeat(np.arange(-60,60,10),6),
           "longitude":np.tile([-150,-100,-50,0,50,100],12)})
        X=np.stack([np.ones(n),rng.normal(size=n)],axis=1)
        a=(0.2+0.12*X[:,1])[:,None]
        y={DESIGNS[0]:(np.tile(a,(1,22)),None),
           DESIGNS[1]:(np.tile(a-0.02*X[:,1,None],(1,22)),None),
           DESIGNS[2]:(np.tile(a-0.03*X[:,1,None],(1,22)),None)}
        r,nblocks=paired_region_bootstrap(frame,X,y,80,20,45,20261118)
        self.assertEqual(r.shape[1:],(2,3,22))
        self.assertGreaterEqual(nblocks,12)
        self.assertAlmostEqual(float(np.mean(r[:,1,1,4]-r[:,1,0,4])),-0.02,places=4)
    def test_source_original_fixed_11_hue_families(self):
        self.assertEqual(len(COLORS),11)
        self.assertEqual(len(set(COLORS)),11)
        self.assertEqual(len(DESIGNS),3)

if __name__=="__main__":unittest.main()
