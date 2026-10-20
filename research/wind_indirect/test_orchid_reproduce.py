"""Independent small-data invariants; original provenance checked during CI run."""
import unittest
import numpy as np
from orchid_reproduce import center,reshuffle,abundance_stat,composition_stat

class OriginalWindNullTests(unittest.TestCase):
    def test_center_by_declared_exchangeability_group(self):
        a=np.array([2.,4.,20.,22.,24.])
        g=np.array(["a","a","b","b","b"])
        np.testing.assert_allclose(center(a,g),[-1.,1.,-2.,0.,2.])
    def test_permutation_keeps_original_block_values(self):
        a=np.arange(8.);g=np.array([0,0,1,1,1,2,2,2])
        b=reshuffle(a,g,np.random.default_rng(19))
        for k in set(g):np.testing.assert_array_equal(np.sort(a[g==k]),np.sort(b[g==k]))
    def test_constant_within_block_wind_has_zero_association(self):
        a=np.array([1.,1.,3.,3.]);g=np.array([0,0,1,1])
        self.assertEqual(abundance_stat(a,np.array([2.,8.,3.,7.]),g),0.)
        self.assertEqual(composition_stat(a,np.array([[1,3],[2,4],[1,3],[4,5]],float),g),0.)
    def test_species_column_permutation_does_not_change_score(self):
        a=np.array([1.,2.,3.,4.]);g=np.zeros(4)
        c=np.array([[3,1,0],[0,4,1],[1,3,0],[0,0,4]],float)
        self.assertAlmostEqual(composition_stat(a,c,g),composition_stat(a,c[:,[2,1,0]],g))

if __name__=="__main__":unittest.main()
