"""Exact Fraction weather look-ahead and source-cue ordering invariants."""
import unittest
from fractions import Fraction as F
from adaptive_gain.wind_forecast_routing import (
    forecast_joint_kernel,forecast_accuracy,cue_contexts,
)
from adaptive_gain.deadline_mixture import hidden_deadline_accuracy
from adaptive_gain.stochastic_weather import weather_kernel,kernel_powers


MIX=((3,F(1,2)),(7,F(1,2)))
COST=((1,1),(1,2))


class NextWindForecastTests(unittest.TestCase):
    def test_forecast_returns_unconditional_survival_transition(self):
        Q=weather_kernel();powers=kernel_powers(Q,7)
        for duration in range(1,8):
            for e in (F(0),F(1,10),F(1,2)):
                h=forecast_joint_kernel(duration,e,Q,powers)
                for w in (0,1):
                    for final in (0,1):
                        self.assertEqual(h[0][w][final]+h[1][w][final],
                                         powers[duration][w][final])

    def test_forecast_random_coin_exactly_previous_independent_solver(self):
        for p in (F(1,10),F(1,2),F(9,10)):
            for bits,costs in (((),((),())),((0,),((1,),(1,))),
                               ((1,),((1,),(2,))),((0,1),COST)):
                self.assertEqual(
                    forecast_accuracy(MIX,4,bits,source_costs=costs,
                                      stay=p,forecast_error=F(1,2)),
                    hidden_deadline_accuracy(MIX,4,bits,source_costs=costs,stay=p))

    def test_perfect_lookahead_cannot_reduce_accuracy_and_more_noise_weakens_value(self):
        for p in (F(1,10),F(1,2),F(9,10)):
            accuracies=[forecast_accuracy(MIX,4,(0,1),source_costs=COST,
                                         stay=p,forecast_error=e)
                        for e in (F(0),F(1,10),F(1,4),F(1,2))]
            self.assertTrue(all(x>=y for x,y in zip(accuracies,accuracies[1:])))

    def test_without_other_species_weather_prediction_is_not_target_information(self):
        for p in (F(1,10),F(1,2),F(9,10)):
            baseline=hidden_deadline_accuracy(MIX,4,(),source_costs=((),()),stay=p)
            for e in (F(0),F(1,10),F(1,2)):
                self.assertEqual(forecast_accuracy(MIX,4,(),source_costs=((),()),
                                  stay=p,forecast_error=e),baseline)

    def test_equal_weather_effects_make_weather_forecast_irrelevant(self):
        common={"survival":(F(4,5),F(4,5)),
                "source_costs":((1,1),(1,1)), "stay":F(9,10)}
        self.assertEqual(
            forecast_accuracy(MIX,4,(0,1),forecast_error=F(0),**common),
            forecast_accuracy(MIX,4,(0,1),forecast_error=F(1,2),**common))

    def test_exact_reproducibility_primary_values(self):
        perfect=forecast_accuracy(MIX,4,(0,1),source_costs=COST,forecast_error=F(0))
        null=forecast_accuracy(MIX,4,(0,1),source_costs=COST,forecast_error=F(1,2))
        self.assertEqual(perfect,F(2484991535819,4096000000000))
        self.assertEqual(null,F(77375740429,128000000000))
        self.assertGreater(perfect,null)

    def test_lookahead_value_higher_when_deadline_hidden_in_this_example(self):
        params={"d":4,"bits":(0,1),"source_costs":COST}
        hidden=lambda err:forecast_accuracy(MIX,forecast_error=err,**params)
        known=lambda err:sum((F(1,2)*forecast_accuracy(((k,F(1)),),
                   forecast_error=err,**params) for k in (3,7)),F(0))
        self.assertTrue(known(F(0))>=hidden(F(0)))
        self.assertTrue(known(F(1,2))>=hidden(F(1,2)))
        self.assertGreater(hidden(F(0))-hidden(F(1,2)),
                           known(F(0))-known(F(1,2)))

    def test_forecast_can_switch_followup_action_after_species_B(self):
        _,receipt=forecast_accuracy(MIX,4,(0,1),source_costs=COST,
                                    forecast_error=F(0),stats=True)
        self.assertEqual(receipt["initial_policy"]["0"]["0"],["B"])
        self.assertEqual(receipt["initial_policy"]["1"]["1"],["A"])
        self.assertGreater(receipt["reachable_policy_states"],100)
        self.assertTrue(any(
            x["elapsed"]==1 and x["source_read_mask"]==2
            and x["forecast_calm"]==["A"]
            and set(x["forecast_gust"])=={"flower_0","flower_1"}
            for x in receipt["strict_forecast_action_switch_examples"]))

    def test_invalid_prediction_accuracy_rejected(self):
        for e in (F(-1,10),F(3,5)):
            with self.assertRaises(ValueError):
                forecast_accuracy(MIX,4,(),forecast_error=e)

    def test_synergy_is_separate_from_accuracy_gain(self):
        a=cue_contexts(stay=F(1,2),forecast_error=F(0))
        self.assertEqual(a["synergy"],a["AB"]-a["A"]-a["B"]+a["none"])
        self.assertGreaterEqual(a["AB"],max(a[x] for x in ("none","A","B")))


if __name__=="__main__":
    unittest.main()
