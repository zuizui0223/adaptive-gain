"""Test first: algebraic consistency and date-block-preserving analysis."""
import unittest
import numpy as np
import pandas as pd
from field_wind import fit_ols_with_controls, date_shuffle_reference, load_balfour

class FieldWindTests(unittest.TestCase):
    def test_algebraic_slope_ratio_is_numerator_minus_denominator(self):
        d=pd.DataFrame({"Wind":[.1,.2,.3,.4,.5,.8,1.2,2.1,2.9,3.2],
         "group":["A"]*5+["B"]*5,
         "I":[2,2,3,3,4,4,5,5,6,7], "F":[10,10,12,12,15,15,18,19,21,23]})
        z=pd.get_dummies(d[['group']],drop_first=True,dtype=float)
        a=fit_ols_with_controls(d.Wind.to_numpy(),np.log(d.I.to_numpy()),z)
        b=fit_ols_with_controls(d.Wind.to_numpy(),np.log(d.F.to_numpy()),z)
        c=fit_ols_with_controls(d.Wind.to_numpy(),np.log(d.I.to_numpy()/d.F.to_numpy()),z)
        self.assertAlmostEqual(a-b,c,places=11)

    def test_within_date_shuffle_never_moves_wind_across_dates(self):
        wind=np.array([.1,.7,1.2,.5,.9,1.3]);date=np.array(['a']*3+['b']*3)
        m=date_shuffle_reference(wind,date,np.random.default_rng(19),reps=59)
        self.assertEqual(m.shape,(59,6))
        for x in m:
            np.testing.assert_array_equal(np.sort(x[:3]),np.sort(wind[:3]))
            np.testing.assert_array_equal(np.sort(x[3:]),np.sort(wind[3:]))

    def test_exact_original_published_source_digest(self):
        df,receipt=load_balfour('Balfouretal_Inflorescence_Switch_Rate_DataDryad.csv')
        self.assertEqual(len(df),210)
        self.assertEqual(df.Date.nunique(),22)
        self.assertTrue(receipt['original_sha256_verified'])
        self.assertTrue((df.Inflorences<=df.Flowers).all())

if __name__=='__main__':unittest.main()