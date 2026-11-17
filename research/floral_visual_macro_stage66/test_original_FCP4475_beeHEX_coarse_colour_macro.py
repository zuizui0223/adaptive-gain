"""Stage66 offline synthetic tests; NEVER evidence of empirical ecology."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch
import numpy as np
import pandas as pd

MOD=Path(__file__).with_name("original_FCP4475_beeHEX_coarse_colour_macro.py")
spec=importlib.util.spec_from_file_location("floral_macro66",MOD)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class OriginalMacroContractTests(TestCase):
    def test_true_ineligible_source_hex_never_becomes_zero(self):
        rows=[]
        for i in range(10242):
            valid=i<2695
            rows.append({"source_siteid":f"HEX{i}",
                 "eligibility":("AUTHOR_TREE_AND_PA_CELL_CUTOFF" if valid
                                 else "OUTSIDE_AUTHOR_FILTERED_MODEL_NO_ABSENCE_INFERENCE"),
                 "n_source_tree_and_pa_cutoff_Bombus_taxa":i%3 if valid else np.nan,
                 "n_source_tree_and_pa_cutoff_all_bee_taxa":10 if valid else np.nan})
        with TemporaryDirectory() as tmp:
            f=Path(tmp)/"model.csv"
            pd.DataFrame(rows).to_csv(f,index=False)
            with patch.object(m,"BEES_SHA",m.sha(f)):
                data,receipt=m.source_bee_model(f)
            self.assertEqual(len(data),2695)
            self.assertEqual(receipt["uncovered_hex_NOT_TRUE_ABSENCE"],7547)
            self.assertEqual(int(data.n_Bombus.eq(0).sum()),899)
            self.assertNotIn("HEX2695",set(data.source_siteid))

    def test_species_cell_frac_and_no_photo_pseudoreplication(self):
        p=pd.DataFrame([
           ["a",3,"Alpha test","HEX11","white",10,20,28,100],
           ["b",3,"Alpha test","HEX11","red_pink",10,20,28,100],
           ["c",3,"Alpha test","HEX12","white",11,21,23,150],
           ["d",4,"Beta test","HEX999","yellow_orange",12,22,15,150]],
           columns=["photo_id","inat_taxon_id","species","source_hex_id","morph",
                    "latitude","longitude","BIO5","BIO12"])
        p["fcp_source_cohort"]="discovery"
        bees=pd.DataFrame([
           ["HEX11",3,10,.3,np.log1p(10)],
           ["HEX12",4,10,.4,np.log1p(10)]],
           columns=["source_siteid","n_Bombus","n_all_bee","Bombus_fraction","log_bees"])
        cells,c=m.species_hex(p,bees)
        self.assertEqual(c["classified_photos_in_eligible_model"],3)
        self.assertEqual(c["eligible_species"],1)
        self.assertEqual(c["species_x_hex_units"],2)
        self.assertEqual(cells.n_photos.tolist(),[2,1])
        self.assertEqual(cells.fraction_white.tolist(),[.5,1])
        self.assertEqual(cells.fraction_red_pink.tolist(),[.5,0])
        self.assertEqual(m.macro_within_species(cells,1,boot=5)["status"],
                         "NOT_ENOUGH_WITHIN_SPECIES_HEX_EXPOSURE")

    def test_no_within_exposure_prohibits_macro_inference(self):
        cells=pd.DataFrame({"inat_taxon_id":[1,1,2,2],
           "source_hex_id":["a","b","a","b"],
           "n_photos":[2]*4,"BIO5":[15,17,np.nan,19],
           "BIO12":[100,120,300,400],
           "Bombus_fraction":[.1,.2,.1,.2]})
        x=m.macro_within_species(cells,3,boot=5)
        self.assertEqual(x["status"],"NOT_ENOUGH_WITHIN_SPECIES_HEX_EXPOSURE")
        self.assertEqual(x["n_species"],0)

    def test_demean_species_equal_weight_not_independent_pictures(self):
        rows=[]
        for s in range(50):
            for k in range(4):
                rows.append({"inat_taxon_id":s,"species":f"Genus{s} test",
                    "source_hex_id":f"HEX{k}","n_photos":1,
                    "lat":s*.4+k*2,"lon":k*20+s*.3,
                    "BIO5":15+s*.01+k,"BIO12":200+s+30*k,
                    "Bombus_fraction":.06*k+.0003*s,"log_bees":np.log1p(8+k),
                    **{"fraction_"+c:float(k%4==j) for j,c in enumerate(m.COLORS)}})
        df=pd.DataFrame(rows)
        X=m.covariates(df)
        groups=df.inat_taxon_id
        for j in range(X.shape[1]):
            X[:,j]-=pd.Series(X[:,j]).groupby(groups).transform("mean").to_numpy()
        self.assertTrue(np.allclose(X.reshape(50,4,8).mean(axis=1),0,atol=1e-12))
        self.assertEqual(m.macro_within_species(df,3,boot=7)["n_species"],0)

    def test_requires_true_source_fcp_sha(self):
        with TemporaryDirectory() as tmp:
            f=Path(tmp)/"fake.gz";f.write_bytes(b"synthetic file")
            with self.assertRaisesRegex(ValueError,"ORIGINAL_FCP_GZIP_SHA"):
                m.source_photos(f)

if __name__=="__main__":
    import unittest
    unittest.main()
