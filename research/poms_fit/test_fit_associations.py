import unittest
import numpy as np
import pandas as pd
from fit_associations import WIND, prepare, fit, source_wind_support

class FitAssociationTests(unittest.TestCase):
    def fixture(self,n=360):
        rng=np.random.default_rng(711)
        w=rng.choice(WIND,n,p=[.45,.40,.15])
        sites=rng.choice([f'S{i}' for i in range(24)],n)
        plants=rng.choice(['Thistle','Buttercup','Clover'],n)
        fl=rng.integers(1,50,n)
        visits=rng.poisson(np.exp(.8+.15*np.log1p(fl)-.8*(w==WIND[2])))
        x=pd.DataFrame({'sample_id':np.arange(n),'date':pd.Timestamp('2022-05-10')+
                        pd.to_timedelta(rng.integers(0,125,n),unit='D'),
                        'year':2022,'target_flower_corrected':plants,
                        'floral_unit':rng.choice(['flower head','flower spike'],n),
                        'floral_unit_count':fl,'wind_speed':w,
                        'sunshine':rng.choice(['Entirely shaded','Entirely in sunshine',
                            'Partly in sun and partly shaded'],n),
                        'location_code':sites,'all_insects_total':visits})
        return x
    def test_zero_surveys_not_discarded(self):
        x=self.fixture()
        x.loc[0,'all_insects_total']=0
        d,flow=prepare(x,'one_km')
        self.assertEqual(flow['raw'],len(x))
        self.assertEqual(flow['eligible'],len(x))
        self.assertTrue(d.y.eq(0).any())
    def test_missing_wind_rejected_not_imputed(self):
        x=self.fixture()
        x.loc[0,'wind_speed']='Not recorded'
        d,flow=prepare(x,'one_km')
        self.assertEqual(flow['wind_recorded_excluded'],1)
        self.assertEqual(len(d),len(x)-1)
    def test_heterogeneous_other_exclusion_is_explicit(self):
        x=self.fixture()
        x.loc[:4,'target_flower_corrected']='Other - please describe below'
        d,flow=prepare(x,'one_km',exclude_other=True)
        self.assertEqual(flow['named_target_excluded'],5)
    def test_cluster_poisson_returns_wind_contrasts(self):
        x=self.fixture()
        d,_=prepare(x,'one_km')
        z=fit(d,'one_km')
        self.assertEqual(z['status'],'fitted')
        self.assertEqual(z['wind_wald']['status'],'ok')
        self.assertEqual(len(z['wind_terms']),2)
        self.assertEqual(source_wind_support(d,'one_km')['sites'],24)
        strong=[q for k,q in z['wind_terms'].items() if WIND[2] in k][0]
        self.assertLess(strong['IRR'],1)
    def test_exploratory_negative_binomial_model_is_separate(self):
        x=self.fixture()
        d,_=prepare(x,'one_km')
        a=fit(d,'one_km','nb_alpha1')
        self.assertEqual(a['status'],'fitted')
        self.assertEqual(a['family_variant'],'nb_alpha1')
        self.assertTrue(0<a['zero_rate_under_fitted_family']<1)

    def test_invalid_insect_count_is_not_used(self):
        x=self.fixture()
        x.loc[1,'all_insects_total']=-5
        d,flow=prepare(x,'one_km')
        self.assertEqual(flow['count_integer_nonnegative_excluded'],1)
        self.assertEqual(len(d),len(x)-1)

if __name__=='__main__':unittest.main()
