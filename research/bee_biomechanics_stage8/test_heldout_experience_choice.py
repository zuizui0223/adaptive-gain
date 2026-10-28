import random
import unittest
from collections import Counter

from episode_audit import EXPECTED_HEADERS,source_episode_audit
from heldout_experience_choice import (
    ALPHA,BETA,GAMMA,NO_GO_INCOMPLETE_BEES,
    true_visited_pairs,split_bee_source_trips,fit_probabilities,
    evaluate,score_edges
)

def fixture(colonies=3, bees_per_colony=4, trips=10, episodes_per_trip=8,
            rest_between=False):
    rng=random.Random(2011)
    rows=[]
    for c in range(colonies):
        for b in range(bees_per_colony):
            bee=f"Bee {c}-{b}"
            for trip in range(1,trips+1):
                prev_drank=(rng.random()<.5)
                for vi in range(episodes_per_trip):
                    # Next choice orientation has information from previous
                    # drink outcome even when previous orientation is used.
                    if vi==0:
                        orient=("horizontal" if rng.random()<.5 else "vertical")
                    else:
                        orient=("horizontal" if rng.random()<
                                (.85 if prev_drank else .15) else "vertical")
                    drank=rng.random()<.5
                    if orient=="horizontal":
                        action="horizontalLandVisit"
                        reward="horizontalLandDrink"
                    else:
                        action="hoverVisit"
                        reward="hoverDrink"
                    group=f"{c}-{b}-{trip}-{vi}"
                    base=[str(c+1),bee,"Control","Micro-rough",
                          group,action,"30",str(trip),str(vi+1),str(vi)]
                    rows.append(dict(zip(EXPECTED_HEADERS,base)))
                    if drank:
                        drinkrow=list(base)
                        drinkrow[5]=reward
                        drinkrow[6]="100"
                        rows.append(dict(zip(EXPECTED_HEADERS,drinkrow)))
                    if rest_between and vi==2:
                        pause=list(base)
                        pause[4]=f"rest-{group}"
                        pause[5]="rest"
                        pause[6]="10"
                        rows.append(dict(zip(EXPECTED_HEADERS,pause)))
                    prev_drank=drank
    return rows

class CambridgeForwardExperienceTests(unittest.TestCase):
    def test_source_rest_is_interruption_not_implicit_flower_choice(self):
        rows=fixture(colonies=1,bees_per_colony=1,
                     trips=1,episodes_per_trip=5,rest_between=True)
        episodes,qa=source_episode_audit(rows,source_expected=None)
        transitions,dates,diagnostic=true_visited_pairs(episodes,rows)
        self.assertEqual(len(transitions[("1","Bee 0-0")]),3)
        self.assertEqual(diagnostic["source_true_pair_exclusions"]
                         ["genuine_rest_or_bout_marker_in_between"],1)
    def test_trip_holdout_keeps_all_later_visits_untouched(self):
        rows=fixture()
        episodes,qa=source_episode_audit(rows,source_expected=None)
        all_pairs,first,receipt=true_visited_pairs(episodes,rows)
        bees,bad=split_bee_source_trips(all_pairs,first)
        self.assertEqual(len(bees),12)
        self.assertEqual(len(bad),0)
        self.assertTrue(all(x["early_fitting_trips"]==7 for x in bees))
        self.assertTrue(all(x["heldout_later_trips"]==3 for x in bees))
        self.assertTrue(all(len(x["test_pairs"])==3*7 for x in bees))
        self.assertTrue(all({x["trip"] for x in bee["train_pairs"]}.
                            isdisjoint({x["trip"] for x in bee["test_pairs"]})
                            for bee in bees))
    def test_m2_is_fixed_action_history_versus_first_order_orientation(self):
        rows=fixture()
        eps,qa=source_episode_audit(rows,source_expected=None)
        result,cache=evaluate(eps,qa,rows,expected_original=None)
        self.assertEqual(result["status"],"FITTED_ORIGINAL_CAMBRIDGE_HELDOUT_BEE_CHOICE")
        self.assertEqual(result["eligible_bees"],12)
        self.assertEqual(result["eligible_independent_colonies"],3)
        self.assertEqual(result["heldout_source_next_flower_orientation_decisions"],252)
        self.assertTrue(all(0<z for z in result["mean_bee_equal_nll"].values()))
        self.assertTrue(result["primary_M1_to_M2_gain_bee_equal"]>0)
        self.assertEqual(len(result["colonies"]),3)
        self.assertEqual(len(result["per_bee"]),12)
    def test_fixed_smoothing_and_positive_probability_when_no_history_cell(self):
        fitted=fit_probabilities([
            {"previous_orientation":"horizontal",
             "previous_recorded_drink":True,
             "next_horizontal":True} for _ in range(20)])
        self.assertEqual(fitted["train_edges"],20)
        self.assertGreater(fitted["M0"],.5)
        self.assertGreater(fitted["M2"][("vertical",0)],0)
        self.assertLess(fitted["M2"][("vertical",1)],1)
        self.assertEqual(BETA,GAMMA)
    def test_no_go_sparse_or_one_colony_cannot_claim_36_bees_replication(self):
        rows=fixture(colonies=1)
        e,q=source_episode_audit(rows,source_expected=None)
        result,cache=evaluate(e,q,rows,expected_original=None)
        self.assertEqual(result["status"],"NO_GO_LATER_TRIP_OR_COLONY_SUPPORT")
    def test_source_incomplete_bee_is_excluded_not_fabricated_as_normal_36(self):
        rows=fixture(colonies=3,bees_per_colony=4)
        for r in rows:
            if r["Bee"]=="Bee 0-0":
                r["Bee"]="Yellow 4"
        e,q=source_episode_audit(rows,source_expected=None)
        result,cache=evaluate(e,q,rows,expected_original=None)
        self.assertEqual(result["eligible_bees"],11)
        self.assertIn("Yellow 4",NO_GO_INCOMPLETE_BEES)
    def test_source_absolute_clock_cannot_be_inferred_from_action_time(self):
        rows=fixture()
        rows[0]["Time (ms)"]="9999999"
        e,q=source_episode_audit(rows,source_expected=None)
        result,cache=evaluate(e,q,rows,expected_original=None)
        self.assertEqual(result["status"],"FITTED_ORIGINAL_CAMBRIDGE_HELDOUT_BEE_CHOICE")

if __name__=="__main__":
    unittest.main()
