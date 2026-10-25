"""Independent second implementation: full latent-state posterior vs compressed DP."""
import unittest
from fractions import Fraction as F

from adaptive_gain.wind_forecast_routing import forecast_accuracy
from research.wind_forecast.independent_timed_posterior import direct_posterior_accuracy


class TimingIndependentFullPosterior(unittest.TestCase):
    def test_135_exact_small_state_grid(self):
        dist=((3,F(1,2)),(4,F(1,2)))
        cost=((1,1),(1,2))
        checked=0
        for p in (F(1,10),F(1,2),F(9,10)):
            for forecast_noise in (F(0),F(1,4),F(1,2)):
                for schedule in ((),(0,),(1,),(1,2),tuple(range(4))):
                    for bits,prices in (((),((),())),((0,),((1,),(1,))),
                                        ((0,1),cost)):
                        params=dict(source_costs=prices,stay=p,
                            forecast_error=forecast_noise,forecast_ticks=schedule)
                        a=forecast_accuracy(dist,2,bits,**params)
                        b=direct_posterior_accuracy(dist,2,bits,**params)
                        self.assertEqual(a,b,(bits,p,forecast_noise,schedule))
                        checked+=1
        self.assertEqual(checked,135)


if __name__=="__main__":unittest.main()
