import unittest

import numpy as np
import pandas as pd

from fit_associations import WIND, prepare
from guild_composition import fit_guild_pair
from guild_sensitivities import trim_high_counts, matched_stratum_cm_h


class GuildStressTests(unittest.TestCase):
    def synthetic(self,n=480,surface='one_km'):
        rng=np.random.default_rng(76012)
        w=rng.choice(WIND,size=n,p=[0.38,0.42,0.20])
        p=1/(1+np.exp(-(-0.2+1.0*(w==WIND[2]))))
        b=rng.binomial(10,p)
        fly=10-b
        d=pd.DataFrame({
            'sample_id':np.arange(n),
            'date':pd.Timestamp('2021-05-01')+
                     pd.to_timedelta(rng.integers(0,120,n),unit='D'),
            'year':2021,
            'target_flower_corrected':rng.choice(['Buttercup','Clover','Thistle'],n),
            'floral_unit':rng.choice(['flower head','individual flower'],n),
            'floral_unit_count':rng.integers(1,30,n),
            'wind_speed':w,
            'sunshine':rng.choice(['Entirely in sunshine','Partly in sun and partly shaded','Entirely shaded'],n),
            'location_code':rng.choice([f'site{i}' for i in range(24)],n),
            'x1km_square':rng.choice([f'g{i}' for i in range(40)],n),
            'country':rng.choice(['England','Scotland'],n),
            'habitat_type':rng.choice(['grassland','garden'],n),
            'bumblebees':b,
            'other_flies':fly,
            'all_insects_total':b+fly,
        })
        return d

    def test_public_mode_cluster_and_guild_estimate(self):
        original=self.synthetic(surface='public')
        p,_=prepare(original,'public')
        result=fit_guild_pair(p,'other_flies',surface='public')
        self.assertEqual(result['status'],'fitted',result.get('error',''))
        self.assertEqual(result['surface'],'public')
        self.assertEqual(result['site_clusters'],40)
        self.assertGreater(result['strong_OR'],1)

    def test_high_count_entire_source_record_removed(self):
        d=self.synthetic(300)
        d.loc[0,'bumblebees']=2000
        clipped,receipt=trim_high_counts(d)
        self.assertEqual(receipt['surveys_removed'],1)
        self.assertNotIn(0,clipped.index)
        self.assertEqual(receipt['bumble_visits_removed'],2000)
        self.assertEqual(clipped.shape[0],299)

    def test_matched_site_year_flower_controls(self):
        rows=[]
        for i in range(24):
            for w in (WIND[0],WIND[2]):
                rows.append({'location_code':f's{i}','year':'2022',
                             'target_flower_corrected':'Thistle',
                             'wind_speed':w,
                             'bumblebees':7 if w==WIND[2] else 4,
                             'other_flies':3 if w==WIND[2] else 6})
        r=matched_stratum_cm_h(pd.DataFrame(rows))
        self.assertEqual(r['status'],'computed_descriptive_only')
        self.assertEqual(r['matched_strata'],24)
        self.assertGreater(r['pooled_OR_strong_bumble_to_fly'],1)

    def test_matched_no_support_not_misread_as_biological_zero(self):
        d=self.synthetic(80)
        d['wind_speed']=WIND[0]
        r=matched_stratum_cm_h(d)
        self.assertEqual(r['status'],'insufficient_matched_coverage')
        self.assertEqual(r['matched_strata'],0)

    def test_bad_public_surface_rejected(self):
        with self.assertRaises(ValueError):
            fit_guild_pair(self.synthetic(100),'other_flies',surface='unknown')

if __name__=='__main__':
    unittest.main()
