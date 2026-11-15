"""Independent posterior-Bayes and source-free exact robustness regression."""
import unittest
from fractions import Fraction as F
from itertools import product

from exact_rectangle_certificate import (
    WORLDS, ORDER, BOX, BASE, certify, fixed_contingent_value,
    precommit_value, _root_joint, _leaf_joint, _target, _mass,
)


def posterior_precommit_oracle(q,s0,s1,u0,u1,v0,v1,c):
    """Independent normalized-posterior decision recursion, not joint-mass DP."""
    p={w:F(1,4)*(q if w[1] else 1-q) for w in WORLDS}
    channels={'Z':(0,s0,s1),'U':(1,u0,u1),'V':(2,v0,v1)}
    def update(d,source,report):
        k,a0,a1=channels[source]
        entries={w:pr*((a0 if report==0 else 1-a0) if w[k]==0
                         else ((1-a1) if report==0 else a1))
                 for w,pr in d.items()}
        z=sum(entries.values(),F(0))
        return (z,{w:v/z for w,v in entries.items()}) if z else (z,None)
    def best_guess(d):
        return max(sum((prob for w,prob in d.items() if _target(w)==b),F(0))
                   for b in (0,1))
    def first(d,action):
        if action=='SKIP':return best_guess(d)
        other='V' if action=='U' else 'U'
        output=-c
        for b in (0,1):
            pobs,after=update(d,action,b)
            if not pobs:continue
            second=-c
            for b2 in (0,1):
                pr,after2=update(after,other,b2)
                if pr:second+=pr*best_guess(after2)
            output+=pobs*max(best_guess(after),second)
        return output
    per_action={'SKIP':F(0),'U':F(0),'V':F(0)}
    for z in (0,1):
        pz,posterior=update(p,'Z',z)
        for action in per_action:
            per_action[action]+=pz*first(posterior,action)
    return max(per_action.values())


def direct_fixed_joint(q,s0,s1,u0,u1,v0,v1,c):
    roots=[_root_joint(q,s0,s1,z) for z in (0,1)]
    v=sum((m for w,m in roots[0].items() if _target(w)==0),F(0))
    v-=c*_mass(roots[1])
    for b in (0,1):
        after=_leaf_joint(roots[1],'V',b,u0,u1,v0,v1)
        v+=sum((m for w,m in after.items() if _target(w)==b),F(0))
    return v


class ExactRectangleCertificateTest(unittest.TestCase):
    def test_exact_sharp_8d_uniform_lower_bound(self):
        x=certify()
        self.assertEqual(x['status'],'STRICTLY_POSITIVE_CONTINGENT_ADVANTAGE_CERTIFIED')
        self.assertEqual(x['corner_count'],256)
        self.assertEqual(x['positive_corner_count_for_fixed_policy'],256)
        self.assertEqual(x['minimum_fixed_minus_optimal_precommit'],'63/6250')
        self.assertEqual(x['baseline_at_c_0point15'],'6/125')
        self.assertEqual(x['worst_corner'],{
            'q':'4/25','s0':'19/25','s1':'14/25','u0':'17/20',
            'u1':'17/20','v0':'24/25','v1':'43/50','c':'17/100'})

    def test_closed_form_vs_explicit_eight_world_sum_all_corners(self):
        bounds=[tuple(map(F,BOX[k])) for k in ORDER]
        for param in product(*bounds):
            with self.subTest(point=tuple(map(str,param))):
                self.assertEqual(fixed_contingent_value(*param),direct_fixed_joint(*param))

    def test_independent_normalized_posterior_vs_joint_mass_all_corners(self):
        bounds=[tuple(map(F,BOX[k])) for k in ORDER]
        for param in product(*bounds):
            with self.subTest(point=tuple(map(str,param))):
                self.assertEqual(precommit_value(*param),posterior_precommit_oracle(*param))

    def test_interior_rational_points_lower_bound(self):
        bound=F(63,6250)
        vals=[]
        for i,k in enumerate(ORDER):
            a,b=(F(x) for x in BOX[k]);vals.append((a+b)/2)
        for i in range(65):
            params=[]
            for j,k in enumerate(ORDER):
                a,b=map(F,BOX[k])
                mix=F((i*13+j*37+7)%67,67)
                params.append(a+(b-a)*mix)
            self.assertGreaterEqual(fixed_contingent_value(*params)-precommit_value(*params),bound)
        self.assertGreaterEqual(fixed_contingent_value(*vals)-precommit_value(*vals),bound)

    def test_fail_closed_out_of_domain(self):
        for bad in [dict((k,v) for k,v in BOX.items() if k!='u0'),
                    dict(BOX,q=('-0.01','.2')),
                    dict(BOX,v0=('0.4','1')),
                    dict(BOX,c=('0.3','0.2'))]:
            with self.assertRaises(ValueError):certify(bad)

    def test_broader_rectangle_not_falsely_certified(self):
        broad={
          'q':('.15','.25'),'s0':('.75','.85'),'s1':('.55','.65'),
          'u0':('.8','1'),'u1':('.8','1'),
          'v0':('.95','1'),'v1':('.85','.95'),'c':('.12','.18')}
        got=certify(broad)
        self.assertEqual(got['minimum_fixed_minus_optimal_precommit'],'-11/8000')
        self.assertEqual(got['status'],'NO_UNIFORM_POSITIVITY_CERTIFICATE')
        # This does NOT falsify the fully optimized contingent policy.

    def test_no_biological_attribution(self):
        x=certify()
        self.assertTrue(x['no_live_bees'])
        self.assertTrue(x['no_animal_measurements'])
        self.assertTrue(x['not_an_empirical_confidence_region'])
        self.assertTrue(x['not_fitness_measurement'])

if __name__=='__main__':
    unittest.main()
