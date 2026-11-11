"""Stage17 synthetic source-concealed 2×3 optional-query experiment allocations.

Cost blocks are counterbalanced; access mode and target-zero physical side
are balanced within block. Hidden (R,U,V) bits drawn IID WITH REPLACEMENT,
never from a deck depleted by previous source trials.
"""
from __future__ import annotations
import hashlib,json,random
from collections import Counter,defaultdict
from itertools import permutations

COSTS=("low","medium","high")
MODES=("contingent","precommit")
SIDES=("left","right")
COST_ORDERS=tuple(permutations(COSTS))
QA_SEED=20261111

def generate(n_colonies=24,bees_per_colony=12,seed=QA_SEED):
    if (type(n_colonies) is not int or not 2<=n_colonies<=100 or
        type(bees_per_colony) is not int or not 6<=bees_per_colony<=60 or
        bees_per_colony%len(COST_ORDERS)!=0):
        raise ValueError("NO_GO_COST_ORDER_COUNTERBALANCING_NEEDS_SIX_BEE_MULTIPLE")
    rng=random.Random(seed)
    rows=[]
    for col in range(n_colonies):
        colony=f"MOCK_C{col+1:03d}"
        for idx in range(bees_per_colony):
            bee=f"MOCK_B{idx+1:03d}"
            order=COST_ORDERS[idx%len(COST_ORDERS)]
            for block,tier in enumerate(order,1):
                arms=[(mode,side) for mode in MODES for side in SIDES for _ in range(4)]
                rng.shuffle(arms)
                for trial,(mode,zero_side) in enumerate(arms,1):
                    r,u,v=(rng.randrange(2) for _ in range(3))
                    target=u if r==0 else v
                    physical_target=zero_side if target==0 else (
                        "right" if zero_side=="left" else "left")
                    rows.append({
                        "trial_id":f"{colony}_{bee}_T{(block-1)*16+trial:03d}",
                        "colony_id":colony,"bee_id":bee,
                        "block":block,"trial_in_block":trial,
                        "cost_tier":tier,"access_mode":mode,
                        "target_zero_side":zero_side,
                        "hidden_target_side":physical_target,
                        "r":r,"u":u,"v":v,
                        "correct_target":target,
                        "source_world_concealed":True,
                        "source_is_synthetic_QA_only":True})
    audit(rows)
    return rows

def audit(rows):
    if not rows:raise ValueError("NO_GO_EMPTY_STAGE17_ASSIGNMENT")
    bybee=defaultdict(list)
    unique=set()
    bycol=defaultdict(dict)
    arm_counts=Counter()
    for r in rows:
        key=r["trial_id"]
        if key in unique:raise ValueError("NO_GO_DUPLICATED_SOURCE_TRIAL_ID")
        unique.add(key)
        cost,mode,side=(r[k] for k in ("cost_tier","access_mode","target_zero_side"))
        if cost not in COSTS or mode not in MODES or side not in SIDES:
            raise ValueError("NO_GO_UNKNOWN_COST_MODE_OR_PHYSICAL_SIDE")
        if any(type(r[k]) is not int or r[k] not in (0,1) for k in ("r","u","v","correct_target")):
            raise ValueError("NO_GO_INVALID_SOURCE_BITS")
        target=r["u"] if r["r"]==0 else r["v"]
        physical=side if target==0 else ("right" if side=="left" else "left")
        if target!=r["correct_target"] or physical!=r["hidden_target_side"]:
            raise ValueError("NO_GO_SOURCE_TARGET_MAPPING_INCONSISTENT")
        if r.get("source_world_concealed") is not True or r.get("source_is_synthetic_QA_only") is not True:
            raise ValueError("NO_GO_SYNTHETIC_QA_RELABELED_REAL")
        bybee[r["colony_id"],r["bee_id"]].append(r)
        bycol[r["colony_id"]][r["bee_id"]]=True
        arm_counts[cost,mode]+=1
    for (col,bee),sub in bybee.items():
        if len(sub)!=48:raise ValueError("NO_GO_ORIGINAL_BEE_NOT_48_TRIALS")
        blocks=defaultdict(list)
        for r in sub:blocks[r["block"]].append(r)
        if set(blocks)!={1,2,3}:raise ValueError("NO_GO_MISSING_COST_BLOCKS")
        sequence=[]
        for b in range(1,4):
            block=blocks[b]
            if len(block)!=16 or {x["trial_in_block"] for x in block}!=set(range(1,17)):
                raise ValueError("NO_GO_SOURCE_BLOCK_INCOMPLETE")
            costs={x["cost_tier"] for x in block}
            if len(costs)!=1:raise ValueError("NO_GO_COST_CHANGES_INSIDE_BLOCK")
            sequence.append(next(iter(costs)))
            assignment=Counter(x["access_mode"] for x in block)
            if assignment!=Counter({"contingent":8,"precommit":8}):
                raise ValueError("NO_GO_SOURCE_MODE_BALANCE")
            for mode in MODES:
                mapping=Counter(x["target_zero_side"] for x in block if x["access_mode"]==mode)
                if mapping!=Counter({"left":4,"right":4}):
                    raise ValueError("NO_GO_SOURCE_SIDE_BALANCE")
        if tuple(sequence) not in COST_ORDERS:
            raise ValueError("NO_GO_COST_ORDER_NOT_PERMUTATION")
    for col,bees in bycol.items():
        sequence_counts=Counter(tuple(next(row["cost_tier"] for row in bybee[col,bee]
                if row["block"]==block) for block in (1,2,3)) for bee in bees)
        if set(sequence_counts)!=set(COST_ORDERS) or len(set(sequence_counts.values()))!=1:
            raise ValueError("NO_GO_WITHIN_COLONY_LATIN_SQUARE_UNBALANCED")
    return {
        "status":"SYNTHETIC_2x3_OPTIONAL_QUERY_ALLOCATION_VERIFIED",
        "n_trials":len(rows),"n_fake_bees":len(bybee),"n_fake_colonies":len(bycol),
        "arm_counts":{"__".join(x):n for x,n in sorted(arm_counts.items())},
        "trials_per_mock_bee":48,
        "source_world_sampling":"iid_with_replacement",
        "source_original_cost_order_counterbalance":"all_six_permutations",
        "source_physical_target_mapping_balanced":True,
        "no_real_animal_assignments":True}

def receipt():
    rows=generate()
    data=audit(rows)
    canonical=json.dumps(rows,sort_keys=True,separators=(",",":")).encode()
    data["public_mock_schedule_sha256"]=hashlib.sha256(canonical).hexdigest()
    data["real_experimental_seed_and_schedule_not_generated"]=True
    return data

if __name__=="__main__":
    import argparse
    from pathlib import Path
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="stage17_outputs")
    root=Path(p.parse_args().out);root.mkdir(parents=True,exist_ok=True)
    print("STAGE17_ALLOCATION_QA "+json.dumps(receipt(),sort_keys=True))
