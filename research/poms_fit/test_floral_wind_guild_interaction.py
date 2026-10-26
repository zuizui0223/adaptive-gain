import unittest
import numpy as np
import pandas as pd

from fit_associations import WIND
from floral_wind_guild_interaction import prepare_interaction, fit_interaction

class FloralStructureInteractionTests(unittest.TestCase):
    def fixture(self,n=960):
        rng=np.random.default_rng(91023)
        flower=rng.choice(["Thistle","Buttercup","Clover","Heather"],n)
        structure=np.where(np.isin(flower,["Clover","Heather"]),"closed","open")
        wind=rng.choice(WIND,n,p=[.41,.40,.19])
        site=rng.choice([f"S{i}" for i in range(30)],n)
        p=1/(1+np.exp(-(-.6+1.0*((wind==WIND[2]) & (structure=="closed")))))
        bee=rng.binomial(12,p)
        return pd.DataFrame({
            "sample_id":np.arange(n),
            "date":pd.Timestamp("2022-04-25") + pd.to_timedelta(rng.integers(0,150,n),unit="D"),
            "year":2022,
            "target_flower_corrected":flower,
            "flower_structure":structure,
            "floral_unit":np.where(structure=="closed","flower head","individual flower"),
            "floral_unit_count":rng.integers(5,70,n),
            "wind_speed":wind,
            "sunshine":rng.choice(["Entirely in sunshine",
                                    "Entirely shaded",
                                    "Partly in sun and partly shaded"],n),
            "location_code":site,
            "x1km_square":site,
            "country":rng.choice(["England","Wales","Scotland"],n),
            "habitat_type":rng.choice(["Grassland","Woodland"],n),
            "count_start_time":[f"{h:02d}:15" for h in rng.integers(10,18,n)],
            "recorder_type":rng.choice(["high","low",None],n),
            "flower_cover":rng.choice(["less than half","about half"],n),
            "bumblebees":bee,
            "other_flies":12-bee,
            "all_insects_total":np.full(n,12),
        })
    def test_support_succeeds_and_true_binary_interaction_detected(self):
        source=self.fixture()
        df,admission=prepare_interaction(source,"one_km",include_other=False)
        self.assertEqual(admission["status"],"ELIGIBLE",admission)
        self.assertTrue((df.bumblebees+df.other_flies>0).all())
        result=fit_interaction(df,"one_km")
        self.assertEqual(result["status"],"FITTED",result.get("error",str(result)))
        self.assertEqual(result["design_rank"],result["design_columns"])
        self.assertGreater(result["strong_wind_effect_modification_closed_vs_open"]["OR"],1.5)
        self.assertLess(result["interaction_joint_wald"]["p"],0.05)
    def test_sparse_closed_strong_is_no_go(self):
        data=self.fixture()
        data.loc[(data.flower_structure=="closed")&(data.wind_speed==WIND[2]),"wind_speed"]=WIND[1]
        df,info=prepare_interaction(data,"one_km")
        self.assertIsNone(df)
        self.assertEqual(info["status"],"NO_GO_INSUFFICIENT_STRUCTURE_OVERLAP")
        self.assertTrue(any("closed: strong" in x for x in info["support_failure_reasons"]))
    def test_anomalous_structure_is_excluded(self):
        data=self.fixture()
        data.loc[:5,"flower_structure"]=None
        df,info=prepare_interaction(data,"one_km")
        self.assertEqual(info["uncertain_morphology_excluded"],6)
        self.assertFalse(df.structure.isna().any())
    def test_public_mode_uses_country_habitat_rather_than_site_fe(self):
        data=self.fixture()
        df,info=prepare_interaction(data,"public")
        self.assertEqual(info["status"],"ELIGIBLE")
        out=fit_interaction(df,"public")
        self.assertEqual(out["status"],"FITTED",out.get("error",str(out)))
        self.assertIn("C(country)",out["model_formula"])
        self.assertNotIn("C(location_code)",out["model_formula"])
    def test_missing_wind_cannot_be_recast_to_calm(self):
        data=self.fixture()
        data.loc[:6,"wind_speed"]="Not recorded"
        df,rec=prepare_interaction(data,"one_km")
        self.assertEqual(rec["first_stage_exclusions"]["wind_recorded_excluded"],7)
        self.assertTrue((df.wind_speed != "Not recorded").all())

if __name__=="__main__":unittest.main()
