"""Synthetic-only Stage12 single-effect specification tests."""
import math,unittest
import numpy as np
import pandas as pd
from model import add_within_plant, design, scores, fit_stage12

def synthetic(n=130):
    rng=np.random.default_rng(872)
    plant=np.array(["A","B","C","D"])[np.arange(n)%4]
    site=np.array(["Brighton","Edinburgh"])[rng.integers(0,2,n)]
    rawwind=rng.integers(0,5,n).astype(float)
    other=rng.uniform(.05,.85,n)
    flight=rng.integers(4,50,n)
    walking=rng.integers(0,40,n)
    return pd.DataFrame({
        "survey":[f"S{i}" for i in range(n)],
        "date":pd.date_range("2024-04-01",periods=n,freq="D").strftime("%Y-%m-%d"),
        "site":site,"plant":plant,
        "flights":flight,"walks":walking,
        "beaufort":rawwind,"other_share":other,
        "temperature":rng.uniform(12,24,n),
        "blue_sky":rng.uniform(0,100,n),
        "flower_density":rng.uniform(50,1000,n),
        "behavior_rows":np.ones(n,dtype=int)
    })

class Stage12ModelTests(unittest.TestCase):
    def test_zero_walk_is_finite_without_discarding_original_survey(self):
        d=synthetic(20);d.loc[0,"walks"]=0
        y=scores(d)
        self.assertTrue(np.isfinite(y).all())
        self.assertAlmostEqual(y[0],math.log((d.loc[0,"flights"]+0.5)/0.5))
        self.assertEqual(len(y),20)
    def test_plant_centering_and_only_one_primary_cross_term(self):
        d=synthetic(130)
        z,sd=add_within_plant(d)
        self.assertGreater(sd,0)
        np.testing.assert_allclose(z.groupby("plant")[["w","h"]].mean(),0,atol=1e-12)
        X,names=design(z)
        self.assertEqual(names.count("wind:other"),1)
        np.testing.assert_allclose(X[:,names.index("wind:other")],z.w*z.h)
        self.assertFalse(any(n in names for n in ["flights","walks","movement_events"]))
    def test_synthetic_fixed_interaction_is_recoverable(self):
        d=synthetic(130)
        z,_=add_within_plant(d)
        X,names=design(z)
        rng=np.random.default_rng(997)
        y=X@np.r_[2.,np.zeros(X.shape[1]-1)]
        y+=0.4*X[:,names.index("wind:other")]+rng.normal(scale=.04,size=len(y))
        assert X.shape[1]==len(names)
        from model import clustered_ols
        grp=(z.site+"|"+z.date).to_numpy()
        out=clustered_ols(X,y,grp)
        self.assertAlmostEqual(out["beta"][names.index("wind:other")],0.4,delta=.02)
    def test_one_survey_one_weight_not_16678_independent_animals(self):
        d=synthetic(130)
        d.loc[0,"flights"]=10000
        result=fit_stage12(d)
        self.assertEqual(result["surveys"],130)
        self.assertEqual(result["model_contrast"],"wind:other")
        self.assertEqual(result["survey_weight_semantics"],"every original survey equal weight")

if __name__=="__main__":unittest.main()
