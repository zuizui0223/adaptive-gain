import unittest
from collections import Counter,defaultdict
from randomization import (
    QA_SEED,ORDERS,WINDS,WIND_SEQUENCES,
    generate_allocation,audit_allocation,allocation_commitment,
    generate_receipt
)

class BeeCueOrderRandomizationTests(unittest.TestCase):
    def test_24_independent_colonies_12_bees_18432_trials(self):
        rows=generate_allocation(24,12)
        receipt=audit_allocation(rows,24,12)
        self.assertEqual(receipt["colonies"],24)
        self.assertEqual(receipt["bees"],24*12)
        self.assertEqual(receipt["trials"],18432)
        self.assertEqual(set(receipt["total_cell_counts"].values()),{4608})
        self.assertTrue(receipt["synthetic_design_QA_only"])
    def test_each_bee_has_exact_4_cells_and_side_rotation(self):
        rows=generate_allocation(12,4)
        bybee=defaultdict(list)
        for r in rows:bybee[(r["colony_id"],r["bee_id"])].append(r)
        for bee,subset in bybee.items():
            group=Counter((r["assigned_wind"],r["assigned_cue_order"],
                           r["high_reward_and_difficult_handling_side"])
                          for r in subset)
            self.assertEqual(set(group.values()),{8})
            self.assertEqual(len(group),8)
            self.assertEqual(len(subset),64)
            windseq=tuple(next(x["assigned_wind"] for x in subset
                               if x["block"]==i) for i in range(1,5))
            self.assertIn(windseq,WIND_SEQUENCES)
    def test_within_colony_cross_over_sequences_counterbalanced_across_bees(self):
        rows=generate_allocation(12,12)
        group=defaultdict(dict)
        for x in rows:
            group[x["colony_id"]].setdefault(x["bee_id"],{})[x["block"]]=x["assigned_wind"]
        for c,bee in group.items():
            seq=Counter(tuple(wind[i] for i in (1,2,3,4))
                        for wind in bee.values())
            self.assertEqual(set(seq),set(WIND_SEQUENCES))
            self.assertEqual(set(seq.values()),{6})
    def test_pub_seed_is_qa_only_never_real_allocation(self):
        a=generate_receipt(12,4)
        self.assertTrue(a["private_allocation_seed_NOT_GENERATED_OR_STORED"])
        self.assertTrue(a["do_not_release_real_trial_arm_schedule"])
        self.assertEqual(len(a["allocation_sha256_commitment"]),64)
        self.assertEqual(a["QA_seed_fixed_public"],QA_SEED)
        self.assertNotIn("trial_id",a)
        self.assertNotIn("bee_id",a)
    def test_deterministic_test_hash_and_distinct_seed(self):
        a=generate_allocation(4,4,seed=1)
        b=generate_allocation(4,4,seed=1)
        c=generate_allocation(4,4,seed=2)
        self.assertEqual(allocation_commitment(a),allocation_commitment(b))
        self.assertNotEqual(allocation_commitment(a),allocation_commitment(c))
    def test_duplicate_trial_does_not_pass(self):
        r=generate_allocation(4,4)
        r[1]=dict(r[0])
        with self.assertRaisesRegex(ValueError,"DUPLICATE"):
            audit_allocation(r)
    def test_any_midblock_wind_switch_is_a_protocol_violation(self):
        r=generate_allocation(4,4)
        r[3]["assigned_wind"]="crosswind" if r[3]["assigned_wind"]=="calm" else "calm"
        with self.assertRaisesRegex(ValueError,"WIND_SWITCHED_MID_BLOCK"):
            audit_allocation(r)
    def test_cue_access_before_second_reveal_fails_closed(self):
        r=generate_allocation(4,4)
        r[0]["both_options_accessible_s"]=3
        with self.assertRaisesRegex(ValueError,"CUE_TIMING_DRIFT"):
            audit_allocation(r)
    def test_wind_side_order_counts_not_only_average_balance(self):
        r=generate_allocation(4,4)
        block=[x for x in r if x["colony_id"]=="C001" and x["bee_id"]=="B001"
               and x["block"]==1]
        left=next(x for x in block
                  if x["assigned_cue_order"]=="reward_first" and
                  x["high_reward_and_difficult_handling_side"]=="left")
        right=next(x for x in block
                   if x["assigned_cue_order"]=="reward_first" and
                   x["high_reward_and_difficult_handling_side"]=="right")
        left["high_reward_and_difficult_handling_side"]="right"
        right["high_reward_and_difficult_handling_side"]="right"
        with self.assertRaisesRegex(ValueError,"ORDER_SIDE_NOT_BALANCED"):
            audit_allocation(r)

if __name__=="__main__":unittest.main()
