import unittest

import numpy as np
import pandas as pd

from fit_associations import WIND, prepare
from guild_composition import COMPARATORS, fit_guild_pair, holm_adjust


class CompositionTests(unittest.TestCase):
    def _survey(self, n=480):
        rng = np.random.default_rng(23)
        wind = rng.choice(WIND, size=n, p=[.40,.40,.20])
        logodds = -.1 + .8*(wind == WIND[2])
        p = 1/(1+np.exp(-logodds))
        visits = rng.binomial(9,p)
        d = pd.DataFrame({
            'sample_id':np.arange(n),
            'date':pd.Timestamp('2022-05-01') +
                   pd.to_timedelta(rng.integers(0,130,n),unit='D'),
            'year':2022,
            'target_flower_corrected':rng.choice(['Thistle','Clover','Bramble'],n),
            'floral_unit':rng.choice(['flower head','individual flower'],n),
            'floral_unit_count':rng.integers(1,50,n),
            'wind_speed':wind,
            'sunshine':rng.choice(['Entirely in sunshine',
                   'Partly in sun and partly shaded','Entirely shaded'],n),
            'location_code':rng.choice([f'grid{i}' for i in range(28)],n),
            'bumblebees':visits,
            'hoverflies':9-visits,
            'other_flies':9-visits,
            'butterflies_moths':9-visits,
            'all_insects_total':visits+3*(9-visits)
        })
        return d

    def test_holm_three_family(self):
        r=holm_adjust({'a':.01,'b':.04,'c':.03})
        self.assertAlmostEqual(r['a'],.03)
        self.assertAlmostEqual(r['b'],.06)
        self.assertAlmostEqual(r['c'],.06)

    def test_source_zero_total_not_fake_choice(self):
        d=self._survey()
        d.loc[0,['bumblebees','hoverflies','other_flies',
                  'butterflies_moths','all_insects_total']]=0
        eligible,flow=prepare(d,'one_km')
        self.assertEqual(flow['eligible'],len(d))
        result=fit_guild_pair(eligible,'hoverflies')
        self.assertEqual(result['pair_absent_surveys_excluded'],1)
        self.assertEqual(result['pair_observed_surveys'],len(d)-1)

    def test_known_posthoc_comparison_orientation(self):
        d,_=prepare(self._survey(),'one_km')
        result=fit_guild_pair(d,'hoverflies')
        self.assertEqual(result['status'],'fitted',result.get('error',''))
        self.assertGreater(result['strong_OR'],1)
        self.assertEqual(result['site_clusters'],28)
        self.assertEqual(result['wind_joint_wald']['status'],'ok')

    def test_unplanned_comparator_rejected(self):
        d,_=prepare(self._survey(100),'one_km')
        with self.assertRaises(ValueError):
            fit_guild_pair(d,'honeybees')

    def test_bad_counts_rejected(self):
        d,_=prepare(self._survey(),'one_km')
        d.loc[d.index[0],'bumblebees']=-1
        with self.assertRaises(ValueError):
            fit_guild_pair(d,'hoverflies')


if __name__=='__main__':
    unittest.main()
