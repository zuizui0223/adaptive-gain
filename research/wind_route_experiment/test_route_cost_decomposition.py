"""Behavior contract before decomposition implementation (synthetic, no source-dependent fitting)."""
import unittest
import numpy as np
from route_cost_decomposition import components, height_components, bootstrap_components


class DecompositionTests(unittest.TestCase):
    def test_exact_identity(self):
        p=np.array([[.4,.6],[.7,.3]])
        v=np.array([[.1,.5],[.3,.9]])
        o=components(p,v)
        self.assertAlmostEqual(o['delta'],o['composition']+o['within_route'],places=12)
        self.assertAlmostEqual(o['delta'], .7*.3+.3*.9-(.6*.5+.4*.1),places=12)

    def test_no_route_reassignment_has_no_composition_term(self):
        p=np.array([[.6,.4],[.6,.4]])
        v=np.array([[1.,3.],[2.,4.]])
        self.assertAlmostEqual(components(p,v)['composition'],0.)
        self.assertAlmostEqual(components(p,v)['within_route'],1.)

    def test_no_route_specific_speed_change_has_no_within_term(self):
        p=np.array([[.6,.4],[.3,.7]])
        v=np.array([[1.,3.],[1.,3.]])
        self.assertAlmostEqual(components(p,v)['within_route'],0.)
        self.assertAlmostEqual(components(p,v)['composition'],.6)

    def test_route_label_exchange_does_not_change_contributions(self):
        p=np.array([[.2,.8],[.4,.6]])
        v=np.array([[2.,5.],[3.,4.]])
        a=components(p,v);b=components(p[:,::-1],v[:,::-1])
        for k in ['composition','within_route','delta']:
            self.assertAlmostEqual(a[k],b[k])

    def test_different_flight_counts_do_not_overweight_bee(self):
        arr=np.zeros((2,2,2,2))
        # Bee 1 takes twice as many above-flight films as within, Bee 2 many more within.
        arr[0,:,:,0]=[[1,2],[1,2]]
        arr[1,:,:,0]=[[9,1],[1,1]]
        arr[:,:,:,1]=arr[:,:,:,0]*np.array([[2.,4.],[3.,5.]])[None,:,:]
        a=height_components(arr)
        self.assertAlmostEqual(a['p'][0][1],(.6666666667+.1)/2,places=8)
        self.assertAlmostEqual(a['p'][1][1],(.6666666667+.5)/2,places=8)
        self.assertAlmostEqual(a['delta'],a['composition']+a['within_route'],places=12)
        self.assertAlmostEqual(a['route_above_wind_minus_still'], a['p'][1][1]-a['p'][0][1], places=12)

    def test_missing_route_cell_must_not_be_filled_with_zero_speed(self):
        a=np.ones((3,2,2,2),float)
        a[:,1,0,0]=0
        a[:,1,0,1]=0
        with self.assertRaisesRegex(ValueError,'EMPTY_.*ROUTE'):
            height_components(a)

    def test_site_unit_bootstrap_stratifies_height_and_is_deterministic(self):
        rng=np.random.default_rng(15)
        base=np.empty((7,2,2,2),float)
        base[:,:,:,0]=rng.integers(1,5,size=(7,2,2))
        base[:,:,:,1]=base[:,:,:,0]*rng.uniform(.1,.9,size=(7,2,2))
        x=bootstrap_components({98:base,127:base*1.2},[98,127],nrep=199,seed=21)
        y=bootstrap_components({98:base,127:base*1.2},[98,127],nrep=199,seed=21)
        self.assertEqual(x['bootstrap_reps'],199)
        self.assertEqual(x['valid_reps'],199)
        self.assertAlmostEqual(x['observed']['delta'],x['observed']['composition']+x['observed']['within_route'])
        self.assertEqual(x['bootstrap_ci95'],y['bootstrap_ci95'])

if __name__=='__main__':unittest.main()