import unittest
import numpy as np
from lineage_source_null import group_indices,conditional_null
class TestNull(unittest.TestCase):
    def test_fixed_counts_and_expected(self):
        y=np.array([1.,0.,0.,1.,1.]);W=np.array([[1.,2.,3.,4.,5.]])
        groups=group_indices(["a","a","a","b","b"])
        r=conditional_null(None,y,W,groups,99,42)
        self.assertEqual(r["movable_positive_labels"],1)
        self.assertEqual(r["mixed_strata"],1)
        self.assertAlmostEqual(r["conditional_expected"][0],11.)
        self.assertAlmostEqual(r["observed"][0],10.)
        self.assertGreaterEqual(r["null_q025"][0],10.)
        self.assertLessEqual(r["null_q975"][0],12.)
    def test_fixed_singletons(self):
        y=np.array([1.,0.]);W=np.array([[3.,2.]])
        r=conditional_null(None,y,W,group_indices(["a","b"]),19,42)
        self.assertEqual(r["movable_positive_labels"],0)
        self.assertEqual(r["two_sided_centered_tail_fraction"][0],1.)
if __name__=="__main__":unittest.main()
