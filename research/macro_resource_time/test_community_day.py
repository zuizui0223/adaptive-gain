import unittest
import numpy as np
import pandas as pd
from community_day import site_day_conditional_null, _information_for_visitors


def cells(spec):
    return pd.DataFrame(spec, columns=['date','higher','lower','freq'])


class ConditionalDayTests(unittest.TestCase):
    def test_vectorized_information_matches_independent_entropy(self):
        from temporal import entropy_parts
        v=np.array([0]*12+[1]*8)
        d=np.array([0]*4+[1]*8+[0]*6+[1]*2)
        p=np.array([0,0,0,1,1,1,0,0,1,1,1,1,0,0,1,1,0,1,0,1])
        result=_information_for_visitors(v,d,p,2,2,2)
        for j in range(2):
            tab=np.zeros((2,2),dtype=int)
            for dt,pl in zip(d[v==j],p[v==j]):tab[dt,pl]+=1
            self.assertAlmostEqual(result[j],entropy_parts(tab)['I'],places=12)

    def test_community_wide_phenology_not_visitor_specific(self):
        # Every date offers a different visited plant to both visitor taxa.
        x=cells([('d1','A','flower1',10),('d1','B','flower1',10),
                 ('d2','A','flower2',10),('d2','B','flower2',10)])
        result=site_day_conditional_null(x,['A','B'],49,7)
        np.testing.assert_allclose(result.I_observed,np.log(2))
        np.testing.assert_allclose(result.excess_community_day,0,atol=1e-12)
        self.assertFalse(result.shared_testable.any())

    def test_taxon_specific_temporal_switching_is_detected(self):
        x=cells([('d1','A','flower1',40),('d1','B','flower2',40),
                 ('d2','A','flower2',40),('d2','B','flower1',40)])
        result=site_day_conditional_null(x,['A','B'],199,13)
        self.assertTrue(result.shared_testable.all())
        self.assertTrue((result.excess_community_day>0.3).all())
        self.assertTrue((result.p_high<=0.05).all())
        self.assertEqual(result.shared_informative_dates.tolist(),[2,2])
        self.assertEqual(result.focal_permutable_fraction.tolist(),[1.0,1.0])

    def test_static_preferences_do_not_imply_extra_temporal_structure(self):
        x=cells([('d1','A','flower1',40),('d1','B','flower2',40),
                 ('d2','A','flower1',40),('d2','B','flower2',40)])
        result=site_day_conditional_null(x,['A','B'],99,13)
        np.testing.assert_allclose(result.I_observed,0,atol=1e-12)
        self.assertTrue((result.excess_community_day<0).all())
        self.assertTrue((result.p_high>=0.95).all())

    def test_reproducible_and_all_visitors_are_in_shuffling_pool(self):
        x=cells([('d1','A','plant1',20),('d1','B','plant2',20),
                 ('d2','A','plant2',20),('d2','B','plant1',20),
                 ('d1','rare','plant2',10),('d2','rare','plant1',10)])
        a=site_day_conditional_null(x,['A'],29,13)
        b=site_day_conditional_null(x,['A'],29,13)
        pd.testing.assert_frame_equal(a,b)
        self.assertEqual(a.community_visitors.tolist(),[3])

    def test_visit_and_positive_row_counting_are_distinct(self):
        x=cells([('d1','A','p1',12),('d1','B','p2',5),
                 ('d2','A','p2',5),('d2','B','p1',12)])
        visits=site_day_conditional_null(x,['A','B'],99,19,count_policy='visits')
        rows=site_day_conditional_null(x,['A','B'],99,19,count_policy='positive_rows')
        self.assertEqual(visits.visits.tolist(),[17,17])
        self.assertEqual(rows.visits.tolist(),[2,2])
        self.assertTrue((visits.shared_testable).all())
        self.assertTrue((rows.shared_testable).all())
        self.assertFalse(np.allclose(visits.I_observed,rows.I_observed))
        with self.assertRaises(ValueError):
            site_day_conditional_null(x,['A'],count_policy='unknown')

    def test_invalid_counts_and_missing_focal_fail(self):
        x=cells([('d1','A','plant1',1)])
        with self.assertRaises(ValueError):site_day_conditional_null(x,['B'])
        with self.assertRaises(ValueError):site_day_conditional_null(x,['A'],reps=0)
        with self.assertRaises(ValueError):site_day_conditional_null(cells([('d1','A','p',1.5)]),['A'])


if __name__=='__main__':unittest.main()
