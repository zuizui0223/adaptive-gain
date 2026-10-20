import unittest
import numpy as np
import pandas as pd
import site_holdout_model as m


def synthetic_panel():
    rows = []
    for site in range(10):
        for p in range(2):
            for mo in range(2):
                r = {c:'same' for c in m.CATEGORICAL}
                r.update(site=f's{site}',target=f'p{p}',month=str(5+mo),year='2020',
                         flowers=float(2+p*6+mo),target_month=f'p{p} × {5+mo}',
                         bumblebees=float(1+3*p+mo+5*p*mo))
                rows.append(r)
    return pd.DataFrame(rows)


class SiteHoldoutTests(unittest.TestCase):
    def test_offset_prediction_invariant_to_global_exposure_units(self):
        a=synthetic_panel(); b=a.copy(); b['flowers']*=10
        parts=m.folds(a)
        first=m.fit_eval(a,parts,'bumblebees','floral_offset')
        second=m.fit_eval(b,parts,'bumblebees','floral_offset')
        self.assertAlmostEqual(first['mean_baseline_nll'],second['mean_baseline_nll'],places=5)
        self.assertAlmostEqual(first['mean_interaction_nll'],second['mean_interaction_nll'],places=5)

    def test_folds_have_no_site_leakage_and_cover_every_row_once(self):
        df=synthetic_panel(); parts=m.folds(df)
        seen=[]
        for tr,te in parts:
            self.assertFalse(set(df.iloc[tr].site)&set(df.iloc[te].site))
            seen.extend(te)
        self.assertEqual(sorted(seen),list(range(len(df))))

    def test_training_encoder_does_not_add_unseen_test_categories(self):
        train=synthetic_panel(); test=train.iloc[:2].copy()
        test['target_month']='unobserved combo'
        x,y=m.features(train,test,True,'floral_covariate')
        self.assertEqual(x.shape[1],y.shape[1])
        self.assertTrue(np.isfinite(y.data).all())

    def test_nonfinite_or_invalid_prediction_rejected(self):
        for pred in ([np.nan], [np.inf], [-1.0]):
            with self.assertRaises(ValueError):
                m.score([1.0],pred)

    def test_incomplete_fold_coverage_rejected(self):
        w=synthetic_panel()
        with self.assertRaises(ValueError):
            m.fit_eval(w,m.folds(w)[:2],'bumblebees','floral_offset')

    def test_fit_returns_five_fold_diagnostics(self):
        w=synthetic_panel()
        r=m.fit_eval(w,m.folds(w),'bumblebees','floral_covariate')
        self.assertIn('fold_site_equal_deltas',r)
        self.assertEqual(len(r['fold_site_equal_deltas']),5)
        self.assertEqual(r['unknown_target_month_test_rows'],0)

    def test_interaction_block_has_no_training_main_effect_component(self):
        w=synthetic_panel()
        base,_=m.features(w,w,False,'floral_covariate')
        full,_=m.features(w,w,True,'floral_covariate')
        np.testing.assert_allclose(full[:,:base.shape[1]].toarray(),base.toarray())
        new=full[:,base.shape[1]:].toarray()
        b=np.column_stack([np.ones(len(w)),base.toarray()])
        np.testing.assert_allclose(b.T@new,0.,atol=1e-8)

    def test_zero_count_score_is_prediction(self):
        np.testing.assert_allclose(m.score(np.array([0.,0.]),np.array([1.,3.])),[1.,3.])

if __name__=='__main__':unittest.main()
