"""Exact conditional forecast delivery contracts, synthetic model only."""
import unittest
from fractions import Fraction as F
from adaptive_gain.wind_forecast_routing import forecast_accuracy
from adaptive_gain.deadline_mixture import hidden_deadline_accuracy

MIX=((3,F(1,2)),(7,F(1,2)))
COST=((1,1),(1,2))


class TimingTests(unittest.TestCase):
    def test_default_recovers_previous_result(self):
        expected=F(2484991535819,4096000000000)
        self.assertEqual(forecast_accuracy(MIX,4,(0,1),source_costs=COST,
                                           forecast_error=F(0)),expected)
        self.assertEqual(forecast_accuracy(MIX,4,(0,1),source_costs=COST,
                              forecast_error=F(0),available_from_tick=0),expected)

    def test_late_or_never_equals_original_hidden_deadline(self):
        base=hidden_deadline_accuracy(MIX,4,(0,1),source_costs=COST)
        for kwargs in (dict(available_from_tick=7),dict(forecast_ticks=()),
                       dict(forecast_error=F(1,2))):
            opts=dict(forecast_error=F(0));opts.update(kwargs)
            self.assertEqual(forecast_accuracy(MIX,4,(0,1),
                             source_costs=COST,**opts),base)

    def test_t1_timing_concentrates_value_but_initial_forecast_is_redundant(self):
        for p in (F(1,10),F(1,2),F(9,10)):
            kw=dict(source_costs=COST,stay=p,forecast_error=F(0))
            baseline=forecast_accuracy(MIX,4,(0,1),forecast_ticks=(),**kw)
            only_initial=forecast_accuracy(MIX,4,(0,1),forecast_ticks=(0,),**kw)
            one_step=forecast_accuracy(MIX,4,(0,1),forecast_ticks=(1,),**kw)
            full=forecast_accuracy(MIX,4,(0,1),forecast_ticks=tuple(range(7)),**kw)
            delayed=forecast_accuracy(MIX,4,(0,1),available_from_tick=1,**kw)
            self.assertEqual(only_initial,baseline)
            self.assertEqual(full,delayed)
            self.assertGreater(one_step-baseline,F(99,100)*(full-baseline))

    def test_more_free_forecasts_cannot_lower_accuracy(self):
        for p in (F(1,10),F(1,2),F(9,10)):
            kw=dict(source_costs=COST,stay=p,forecast_error=F(0))
            subsets=[(),(1,),(1,4),tuple(range(7))]
            values=[forecast_accuracy(MIX,4,(0,1),forecast_ticks=ts,**kw) for ts in subsets]
            self.assertTrue(all(x<=y for x,y in zip(values,values[1:])))

    def test_no_heterospecies_forecast_is_valueless(self):
        for arrival in (0,1,2,7):
            self.assertEqual(forecast_accuracy(MIX,4,(),
                                 forecast_error=F(0),available_from_tick=arrival),
                             hidden_deadline_accuracy(MIX,4,()))

    def test_earlier_delivery_never_worse(self):
        for p in (F(1,10),F(1,2),F(9,10)):
            values=[forecast_accuracy(MIX,4,(0,1),source_costs=COST,
                        stay=p,forecast_error=F(0),available_from_tick=t)
                        for t in (0,1,2,3,4,5,7)]
            self.assertTrue(all(x>=y for x,y in zip(values,values[1:])))

    def test_invalid_schedule_does_not_silently_change_model(self):
        for schedule in ((-1,),(1,1),(0,True),[1],"1"):
            with self.assertRaises(ValueError):
                forecast_accuracy(MIX,4,(0,1),source_costs=COST,forecast_ticks=schedule)
        for arrival in (-1,1.0,True):
            with self.assertRaises(ValueError):
                forecast_accuracy(MIX,4,(0,1),source_costs=COST,available_from_tick=arrival)

    def test_timing_at_noise_half_equals_baseline(self):
        base=hidden_deadline_accuracy(MIX,4,(0,1),source_costs=COST)
        for schedule in ((),(1,),(1,4),tuple(range(7))):
            self.assertEqual(forecast_accuracy(MIX,4,(0,1),source_costs=COST,
                          forecast_error=F(1,2),forecast_ticks=schedule),base)


if __name__=="__main__":
    unittest.main()
