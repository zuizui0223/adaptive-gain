import unittest

import numpy as np
import pandas as pd

from fit_associations import prepare
from guild_clock_observer import parse_clock,run_adjusted
from test_guild_sensitivities import GuildStressTests

class TimeObserverTests(unittest.TestCase):
    def test_clock_24h_ampm_and_missing(self):
        x=pd.Series(['09:15','10:30:00','1:15 PM','12:30 AM','16:00',
                     'Not recorded','24:60',None])
        cats,summary=parse_clock(x)
        self.assertEqual(summary['parsed'],5)
        self.assertEqual(summary['unparseable_or_missing'],3)
        self.assertEqual([str(z) for z in cats.iloc[:5]],
                         ['before_10','10_to_12','12_to_14','before_10','16_or_later'])

    def test_clock_audit_does_not_invent_missing_hour(self):
        x=pd.Series(['12:30',None,None,'unknown'])
        a,s=parse_clock(x)
        self.assertAlmostEqual(s['parsed_fraction'],.25)
        self.assertEqual(int(a.notna().sum()),1)

    def test_posthoc_extra_controls_recover_known_sign(self):
        rng=np.random.default_rng(770123)
        d=GuildStressTests().synthetic(800)
        d['count_start_time']=rng.choice(['09:30','11:00','13:15','15:40','17:10'],len(d))
        d['recorder_type']=rng.choice(['Experienced','Some experience','New'],len(d))
        d['flower_cover']=rng.choice(['less than half','half','more than half'],len(d))
        p,_=prepare(d,'one_km')
        r=run_adjusted(p,'one_km')
        self.assertEqual(r['status'],'fitted',r.get('error',''))
        self.assertGreater(r['strong_wind_OR'],1)
        self.assertEqual(r['pair_positive_surveys_with_valid_clock'],len(d))

    def test_missing_clock_blocks_model_if_below95pct(self):
        rng=np.random.default_rng(77)
        d=GuildStressTests().synthetic(200)
        d['count_start_time']=['no timestamp']*200
        d['recorder_type']=rng.choice(['Experienced','Other'],len(d))
        d['flower_cover']='middle'
        p,_=prepare(d,'one_km')
        r=run_adjusted(p,'one_km')
        self.assertEqual(r['status'],'clock_format_unqualified')

if __name__=='__main__':
    unittest.main()
