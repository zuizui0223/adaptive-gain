import unittest
from collections import Counter,defaultdict
from allocation import generate,audit,COST_ORDERS

class OptionalAllocationTests(unittest.TestCase):
    def test_balances_mode_and_physical_sides_without_depleting_hidden_worlds(self):
        a=generate(6,6,seed=71);q=audit(a)
        self.assertEqual(q["n_trials"],6*6*48)
        self.assertEqual(q["n_fake_colonies"],6)
        self.assertEqual(q["n_fake_bees"],36)
        self.assertEqual(set(q["arm_counts"].values()),{288})
        self.assertEqual(q["source_world_sampling"],"iid_with_replacement")
        self.assertTrue(q["no_real_animal_assignments"])
        by=defaultdict(list)
        for row in a:by[row["colony_id"],row["bee_id"],row["cost_tier"]].append(row)
        for cells in by.values():
            self.assertEqual(len(cells),16)
            for mode in ("contingent","precommit"):
                subset=[x for x in cells if x["access_mode"]==mode]
                self.assertEqual(len(subset),8)
                self.assertEqual(Counter(x["target_zero_side"] for x in subset),Counter({"left":4,"right":4}))
        distinct={}
        for r in a:
            distinct.setdefault((r["colony_id"],r["bee_id"],r["cost_tier"],r["access_mode"]),[]).append((r["r"],r["u"],r["v"]))
        self.assertTrue(any(len(set(vals))<len(vals) for vals in distinct.values()))
    def test_all_six_cost_orders_balanced_within_each_colony(self):
        a=generate(6,12,seed=97)
        by=defaultdict(dict)
        for x in a:by[x["colony_id"],x["bee_id"]][x["block"]]=x["cost_tier"]
        for colony in set(c for c,b in by):
            orders=Counter(tuple(by[c,b][k] for k in (1,2,3)) for c,b in by if c==colony)
            self.assertEqual(set(orders),set(COST_ORDERS))
            self.assertEqual(set(orders.values()),{2})
    def test_hidden_world_error_is_rejected(self):
        a=generate(6,6,seed=31)
        a[0]["correct_target"]=1-a[0]["correct_target"]
        with self.assertRaisesRegex(ValueError,"TARGET"):audit(a)
    def test_mode_imbalance_rejected_but_world_imbalance_is_not(self):
        a=generate(6,6,seed=3)
        a[0]["access_mode"]="precommit" if a[0]["access_mode"]=="contingent" else "contingent"
        with self.assertRaisesRegex(ValueError,"MODE"):audit(a)

if __name__=="__main__":unittest.main()
