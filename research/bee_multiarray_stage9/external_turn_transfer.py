"""Stage9 transport of dimensionless κ=1.0 from independent 2019 bee array.

The original 2017 experiment has THREE physically distinct 4-flower layouts,
29 tagged bees and two colonies. Real source Figure1 coordinates were manually
digitized from an original published JPEG to ±10cm (not exact measured GPS).

Frozen test:
- train original numbered bouts 1..15, final bouts16..20 fully heldout;
- any 20 source-invalid nest-marker bouts supply ZERO constructed routes;
- train λ per array with fixed grid on true earlier switched flower pairs;
- test Mgeo vs Mtransport κ=1 on original source A!=B,B!=C triplets;
- original colony, bee and array are actual nested units;
- separately report original figure-coordinate ±10cm jitter (21 fixed draws).
No direct recorded flight headings, wind or cognitive cue-access measurement.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import json
import math
from pathlib import Path
import random

from bout_grain import FLOWERS

FROZEN_EXTERNAL_KAPPA=1.0
LAMBDA_GRID=(0.0,0.25,0.5,1.0,2.0,4.0)
ALPHA=0.5
SEED=20261029
PERMUTATIONS=199
FIG_JITTER_REPLICATES=21
FIG_JITTER_ERROR_M=0.10
MIN_VALID_TRAIN_BOUTS=10
MIN_VALID_TEST_BOUTS=3
MIN_BEE_TRIPLETS=5
MIN_BEES_PER_ARRAY=20
MIN_TEST_TRIPLETS_PER_ARRAY=100
MIN_EXCHANGEABLE_TRIPLETS=100
MIN_EXCHANGEABLE_BEES=10
MIN_PERMUTABLE_PER_BEE=5
FIG_SOURCE_HASH="4277dcc8ec52598037a7a4fd6d6bc47d4877a68593a400723508a2d7c0cd40ac"
GEOFILE=Path(__file__).resolve().with_name("flower_positions_figure1_digitized.json")
ALTERNATIVES=("1","2","3","4")

def verify_source_plot_coordinates(path=GEOFILE,source_image=None):
    doc=json.loads(Path(path).read_text())
    if doc.get("source_figure_sha256")!=FIG_SOURCE_HASH:
        raise ValueError("NO_GO_ORIGINAL_PLOT_FIGURE_SHA256")
    if doc.get("plotted_original_units")!="centimetres":
        raise ValueError("NO_GO_SOURCE_PLOT_UNIT_CONVERSION")
    if doc.get("nominal_digitization_absolute_error_per_coordinate_cm")!=10:
        raise ValueError("NO_GO_PLOT_MANUAL_RESOLUTION_WAS_CHANGED")
    if source_image is not None:
        import hashlib
        d=hashlib.sha256(Path(source_image).read_bytes()).hexdigest()
        if d!=FIG_SOURCE_HASH:
            raise ValueError("NO_GO_PLOT_ACTUAL_ORIGINAL_IMAGE_BYTES_MISMATCH")
    if set(doc.get("arrays_cm",{}))!={"1","2","3"}:
        raise ValueError("NO_GO_MISSING_FOUR_FLOWER_PLOT_ARRAYS")
    maps={}
    for layout,original in doc["arrays_cm"].items():
        if set(original)!=set(ALTERNATIVES):
            raise ValueError("NO_GO_SOURCE_FOUR_FLOWER_LABELS")
        mapped={}
        for flower,(x,y) in original.items():
            if not 0<=x<=670 or not 0<=y<=520:
                raise ValueError("NO_GO_ORIGINAL_FIGURE_CM_OUTSIDE_AXES")
            mapped[flower]=(x/100.0,y/100.0)
        if len(set(mapped.values()))!=4:
            raise ValueError("NO_GO_DUPLICATE_ACTUAL_PLOT_FOUR_POINTS")
        maps[layout]=mapped
    # These are source FIGURE transcriptions, not measured flight movements.
    return maps,{
        "original_publisher_jpeg_sha256":doc["source_figure_sha256"],
        "original_publisher_url":doc["original_publisher_url"],
        "digitization_precision_note":doc["coordinates_are"],
        "plot_absolute_error_per_coordinate_m":FIG_JITTER_ERROR_M,
        "units_converted_from_cm_to_m":True,
        "not_actual_tracked_bee_heading":True,
        "source_arrays":doc["arrays_cm"]
    }

def flower_distance(coords,b,c):
    return math.dist(coords[b],coords[c])

def turn_cosine(coords,a,b,c):
    if a==b or b==c:raise ValueError("NO_GO_ZERO_INCOMING_OR_OUTGOING_SOURCE_MOVE")
    ba=(coords[b][0]-coords[a][0],coords[b][1]-coords[a][1])
    cb=(coords[c][0]-coords[b][0],coords[c][1]-coords[b][1])
    norm=math.hypot(*ba)*math.hypot(*cb)
    if norm<=0:raise ValueError("NO_GO_DUPLICATE_SOURCE_COORDINATES")
    value=(ba[0]*cb[0]+ba[1]*cb[1])/norm
    if not math.isfinite(value):raise ValueError("NO_GO_NONFINITE_PLOT_TURN")
    return max(-1.0,min(1.0,value))

def source_bout_events(rows):
    if not rows:raise ValueError("NO_GO_EMPTY_SOURCE_ARRAY_ROUTES")
    groups=defaultdict(list)
    source=Counter()
    for r in rows:
        source["original_bouts"]+=1
        colony,bee,layout,bout=r["colony"],r["bee"],r["array"],int(r["bout"])
        if not 1<=bout<=20 or layout not in ("1","2","3"):
            raise ValueError("NO_GO_NONNATIVE_EXPERIMENT_LAYOUT_OR_BOUT")
        if not r.get("eligible_strict_complete_nest_borders",False):
            source["excluded_nest_boundary_bouts"]+=1
            continue
        seq=r["flower_sequence"]
        if not (seq.startswith("0") and seq.endswith("0") and
                all(x in ALTERNATIVES for x in seq[1:-1])):
            raise ValueError("NO_GO_SOURCE_INVALID_NEST_ROUTE_SLIPPED_IN")
        visits=tuple(seq[1:-1])
        group=(colony,bee,layout)
        groups[group].append({"source_bout":bout,
                              "source_line":r["source_file_row"],
                              "visits":visits})
        source["valid_bouts"]+=1
        source["valid_bout_flower_visits"]+=len(visits)
    for key,items in groups.items():
        items.sort(key=lambda r:r["source_bout"])
        if len({r["source_bout"] for r in items})!=len(items):
            raise ValueError("NO_GO_DUPLICATE_SOURCE_EXPERIMENT_BOUT")
    if source["original_bouts"]!=source["valid_bouts"]+source["excluded_nest_boundary_bouts"]:
        raise ValueError("NO_GO_SOURCE_BOUT_ACCOUNTING")
    return groups,dict(source)

def _source_switch_pairs(visits):
    return [(a,b) for a,b in zip(visits[:-1],visits[1:]) if a!=b]

def _source_triplets(visits):
    return [(a,b,c) for a,b,c in zip(visits[:-2],visits[1:-1],visits[2:])
            if a!=b and b!=c]

def split_bouts(groups,expected_original=True):
    """Fixed original numeric source bout 1-15 train, 16-20 test, no refill."""
    if expected_original and len(groups)!=87:
        raise ValueError("NO_GO_ORIGINAL_BEE_ARRAY_POPULATION_CHANGED")
    population={}
    exclusions=[]
    for key,bouts in sorted(groups.items()):
        train=[x for x in bouts if x["source_bout"]<=15]
        test=[x for x in bouts if x["source_bout"]>=16]
        if len(train)<MIN_VALID_TRAIN_BOUTS or len(test)<MIN_VALID_TEST_BOUTS:
            exclusions.append({"source_colony":key[0],"tag":key[1],"array":key[2],
                               "reason":"source_malformed_nest_bouts_cut_below_admission",
                               "valid_original_bouts_first15":len(train),
                               "valid_original_bouts_last5":len(test)})
            continue
        train_visits=[v for bout in train for v in bout["visits"]]
        train_pairs=[pair for bout in train for pair in _source_switch_pairs(bout["visits"])]
        test_triplets=[{"colony":key[0],"bee":key[1],"array":key[2],
                        "source_bout":bout["source_bout"],
                        "a":a,"b":b,"c":c}
                       for bout in test
                       for a,b,c in _source_triplets(bout["visits"])]
        if len(train_visits)<4 or len(train_pairs)<4:
            exclusions.append({"source_colony":key[0],"tag":key[1],"array":key[2],
                               "reason":"insufficient_authentic_train_visits_and_switches",
                               "first15_train_switched_pairs":len(train_pairs)})
            continue
        if not set(r["source_bout"] for r in test_triplets).isdisjoint(
            set(x["source_bout"] for x in train)
        ):raise ValueError("NO_GO_TRAIN_TEST_ORIGINAL_BOUT_LEAKAGE")
        population[key]={"train_visits":train_visits,
                         "train_switch_pairs":train_pairs,
                         "test_triplets":test_triplets,
                         "n_train_source_bouts":len(train),
                         "n_test_source_bouts":len(test),
                         "train_source_max_bout":max(x["source_bout"] for x in train),
                         "test_source_min_bout":min(x["source_bout"] for x in test)}
    return population,exclusions

def static_prior(train_visits):
    counts=Counter(train_visits)
    n=len(train_visits)
    p={f:(counts[f]+ALPHA)/(n+ALPHA*4) for f in ALTERNATIVES}
    if abs(sum(p.values())-1)>1e-12:
        raise ValueError("NO_GO_SOURCE_STATIC_PROBABILITY_MASS")
    return p

def geo_destination_probs(prior,coords,b,lam):
    if lam not in LAMBDA_GRID:raise ValueError("NO_GO_LAMBDA_NOT_FROZEN_GRID")
    choices=[f for f in ALTERNATIVES if f!=b]
    values={f:math.log(prior[f])-lam*flower_distance(coords,b,f)
            for f in choices}
    high=max(values.values())
    weights={f:math.exp(v-high) for f,v in values.items()}
    total=sum(weights.values())
    p={f:weights[f]/total for f in choices}
    if not all(0<x<1 for x in p.values()) or abs(sum(p.values())-1)>1e-10:
        raise ValueError("NO_GO_NONPOSITIVE_OR_UNNORMALIZED_DESTINATION")
    return p

def directed_destination_probs(geo,coords,a,b,kappa=FROZEN_EXTERNAL_KAPPA):
    if kappa!=FROZEN_EXTERNAL_KAPPA:
        raise ValueError("NO_GO_REESTIMATED_EXTERNAL_DIRECTION_PARAMETER")
    if a==b:raise ValueError("NO_GO_ZERO_INCOMING_CHORD")
    scores={c:math.log(p)+kappa*turn_cosine(coords,a,b,c)
            for c,p in geo.items()}
    high=max(scores.values())
    weights={c:math.exp(v-high) for c,v in scores.items()}
    total=sum(weights.values())
    p={c:weights[c]/total for c in geo}
    if not all(0<x<1 for x in p.values()) or abs(sum(p.values())-1)>1e-10:
        raise ValueError("NO_GO_SOURCE_TURN_PROBABILITY_NOT_NORMALIZED")
    return p

def choose_array_lambdas(population,coordinates):
    """Train λ on genuine source 1-15 flower switches only. No final 5."""
    audit={}
    choices={}
    for array,coords in coordinates.items():
        rows=[(key,r) for key,r in population.items() if key[2]==array]
        if not rows:raise ValueError("NO_GO_EMPTY_EARLY_ARRAY_TRAINING")
        priors={key:static_prior(data["train_visits"]) for key,data in rows}
        per_lambda={}
        for lam in LAMBDA_GRID:
            total_loss=0.0;nt=0
            for key,data in rows:
                for b,c in data["train_switch_pairs"]:
                    total_loss-=math.log(
                        geo_destination_probs(priors[key],coords,b,lam)[c])
                    nt+=1
            if not nt:raise ValueError("NO_GO_NO_TRAINING_SWITCH_PAIRS")
            per_lambda[str(lam)]={"original_early_source_switched_pairs":nt,
                                 "early_source_switch_mean_nll":total_loss/nt}
        chosen=min(LAMBDA_GRID,key=lambda x:(
            per_lambda[str(x)]["early_source_switch_mean_nll"],x))
        choices[array]=chosen
        audit[array]={"source_train_only_grid":per_lambda,
                      "selected_source_train_only_lambda_per_m":chosen,
                      "training_source_bout_indices":[1,15]}
    return choices,audit

def _signed_flips(values):
    """Only descriptive bee-unit within TWO original colonies."""
    if not values or len(values)>16:return None
    import itertools
    real=abs(sum(values)/len(values))
    bigger=0
    for signs in itertools.product((-1,1),repeat=len(values)):
        v=abs(sum(sign*x for sign,x in zip(signs,values))/len(values))
        if v+1e-12>=real:bigger+=1
    return bigger/(2**len(values))

def score_heldout(population,coords,lambdas,
                  require_source_support=True):
    perbee=[]
    all_test_events=defaultdict(list)
    sample_summary=defaultdict(Counter)
    for key,data in sorted(population.items()):
        col,bee,array=key
        triples=data["test_triplets"]
        sample_summary[array]["source_bee_cells"]+=1
        sample_summary[array]["source_heldout_triplets_all"]+=len(triples)
        if len(triples)<MIN_BEE_TRIPLETS:
            sample_summary[array]["source_bees_insufficient_true_test_triplets"]+=1
            continue
        prior=static_prior(data["train_visits"])
        lgeo=ldir=0.0
        for e in triples:
            a,b,c=e["a"],e["b"],e["c"]
            pgeo=geo_destination_probs(prior,coords[array],b,lambdas[array])
            pturn=directed_destination_probs(pgeo,coords[array],a,b)
            lgeo-=math.log(pgeo[c])
            ldir-=math.log(pturn[c])
            all_test_events[array].append(e)
        perbee.append({
            "colony":col,"bee":bee,"array":array,
            "source_train_bouts":data["n_train_source_bouts"],
            "source_test_bouts":data["n_test_source_bouts"],
            "source_train_flower_visits":len(data["train_visits"]),
            "source_genuine_heldout_triplets":len(triples),
            "Mgeo_nll":lgeo/len(triples),
            "Mexternal_direction_nll":ldir/len(triples),
            "Mgeo_to_externally_frozen_kappa1_gain_nats":(lgeo-ldir)/len(triples)
        })
    result={}
    for array in ("1","2","3"):
        vals=[x for x in perbee if x["array"]==array]
        bycol=defaultdict(list)
        for x in vals:bycol[x["colony"]].append(x)
        valid_support=(len(vals)>=MIN_BEES_PER_ARRAY
                       and len(bycol)==2
                       and sum(x["source_genuine_heldout_triplets"] for x in vals)
                       >=MIN_TEST_TRIPLETS_PER_ARRAY)
        cmean={col:sum(x["Mgeo_to_externally_frozen_kappa1_gain_nats"] for x in ls)/len(ls)
               for col,ls in bycol.items()}
        result[array]={
            "status":"HELDOUT_TEST_SUPPORT_PASS" if valid_support else "NO_GO_ARRAY_HELDOUT_SUPPORT",
            "original_colonies":len(bycol),
            "qualifying_original_individuals":len(vals),
            "original_source_test_genuine_triplets":sum(x["source_genuine_heldout_triplets"] for x in vals),
            "source_bout_support":dict(sample_summary[array]),
            "bee_equal_Mgeo_nll":sum(x["Mgeo_nll"] for x in vals)/len(vals) if vals else None,
            "bee_equal_Mexternalkappa1_nll":sum(x["Mexternal_direction_nll"] for x in vals)/len(vals) if vals else None,
            "bee_equal_external_direction_gain_nats":sum(x["Mgeo_to_externally_frozen_kappa1_gain_nats"] for x in vals)/len(vals) if vals else None,
            "bees_with_positive_gain":sum(x["Mgeo_to_externally_frozen_kappa1_gain_nats"]>0 for x in vals),
            "bees_with_negative_gain":sum(x["Mgeo_to_externally_frozen_kappa1_gain_nats"]<0 for x in vals),
            "independent_colony_mean_gain":cmean,
            "both_colonies_positive":len(cmean)==2 and all(v>0 for v in cmean.values()),
            "source_bee_scores":[x for x in vals],
            "source_original_array_presented_after_prior_array":int(array)>1
        }
    if require_source_support and any(x["status"]!="HELDOUT_TEST_SUPPORT_PASS" for x in result.values()):
        raise ValueError("NO_GO_ORIGINAL_SOURCE_LAYOUT_HOLDOUT_SUPPORT "+json.dumps({
            k:{"bees":v["qualifying_original_individuals"],
               "triplets":v["original_source_test_genuine_triplets"],
               "colonies":v["original_colonies"]}
            for k,v in result.items()}))
    return result,all_test_events

def permutation_null_by_array(events,population,coords,lambdas,
                              observed,permutations=PERMUTATIONS,seed=SEED):
    rng=random.Random(seed)
    out={}
    priors={key:static_prior(data["train_visits"]) for key,data in population.items()}
    for array,source_events in events.items():
        by_bee_b=defaultdict(list)
        for i,e in enumerate(source_events):
            by_bee_b[(e["colony"],e["bee"],e["b"])].append(i)
        candidates=set()
        bee_mixes=Counter()
        for idxs in by_bee_b.values():
            if len(idxs)>1 and len({source_events[i]["a"] for i in idxs})>1:
                candidates.update(idxs)
        for i in candidates:bee_mixes[(source_events[i]["colony"],source_events[i]["bee"])]+=1
        gate=(len(candidates)>=MIN_EXCHANGEABLE_TRIPLETS and
              sum(n>=MIN_PERMUTABLE_PER_BEE for n in bee_mixes.values())>=MIN_EXCHANGEABLE_BEES)
        receipt={
            "status":"QUALIFYING_LAYOUT_SHUFFLE_PASS" if gate else "NO_GO_INSUFFICIENT_EXCHANGEABLE_SOURCE_TRIPLETS",
            "source_array":array,
            "actual_heldout_triplets":len(source_events),
            "exchangeable_incoming_tags":len(candidates),
            "eligible_original_bees_ge5_exchangeable":sum(n>=MIN_PERMUTABLE_PER_BEE for n in bee_mixes.values()),
            "null_method":"shuffle A within same source (bee, current flower B, array); keep source actual B,C and trained lambda + fixed external κ untouched",
            "not_a_physically_realizable_or_randomized_flight_path":True,
            "permutations":permutations,"seed":seed}
        if not gate:
            out[array]=receipt;continue
        # Score each (bee's) original triplet with A shuffled and the actual
        # true B->C unchanged. A permutation does NOT construct new source data.
        valid_bee_keys={(x["colony"],x["bee"])
                        for x in observed[array]["source_bee_scores"]}
        grouped=defaultdict(list)
        for i,e in enumerate(source_events):
            key=(e["colony"],e["bee"])
            if key in valid_bee_keys:
                grouped[key].append(i)
        static_per={}
        g_loss={}
        for i,e in enumerate(source_events):
            key=(e["colony"],e["bee"],array)
            prior=priors[key]
            geo=geo_destination_probs(prior,coords[array],e["b"],lambdas[array])
            static_per[i]=geo
            g_loss[i]=-math.log(geo[e["c"]])
        def delta_assigned(incoming):
            s=defaultdict(float)
            for i,e in enumerate(source_events):
                p=directed_destination_probs(
                    static_per[i],coords[array],incoming[i],e["b"])
                s[(e["colony"],e["bee"])]+=g_loss[i]+math.log(p[e["c"]])
            return sum(s[k]/len(ix) for k,ix in grouped.items())/len(grouped)
        original=[e["a"] for e in source_events]
        actual=delta_assigned(original)
        if abs(actual-observed[array]["bee_equal_external_direction_gain_nats"])>1e-10:
            raise ValueError("NO_GO_ORIGINAL_SHUFFLE_BASELINE_DISAGREES_WITH_SOURCE")
        null=[];changed=[]
        for run in range(permutations):
            incoming=list(original)
            for ids in by_bee_b.values():
                vals=[incoming[i] for i in ids]
                rng.shuffle(vals)
                for j,a in zip(ids,vals):incoming[j]=a
            null.append(delta_assigned(incoming))
            changed.append(sum(x!=y for x,y in zip(original,incoming)))
        sorted_null=sorted(null)
        receipt.update({
            "status":"COMPUTED_SOURCE_ARRAY_CONDITIONAL_INCOMING_DIRECTION_NULL",
            "actual_bee_equal_gain_nats":actual,
            "null_mean_bee_equal_gain_nats":sum(null)/len(null),
            "actual_minus_null_mean_nats":actual-sum(null)/len(null),
            "null_q05_nats":sorted_null[int(.05*(permutations-1))],
            "null_q95_nats":sorted_null[int(.95*(permutations-1))],
            "one_tailed_source_conditional_p":(
                1+sum(v>=actual-1e-12 for v in null))/(permutations+1),
            "source_incoming_labels_reassigned_per_shuffle_mean":sum(changed)/len(changed)
        })
        out[array]=receipt
    return out

def jitter_plot_uncertainty(population,baseline_coords,
                            replicates=FIG_JITTER_REPLICATES,seed=SEED):
    rng=random.Random(seed)
    gains=defaultdict(list)
    lambdas=defaultdict(Counter)
    for trial in range(replicates):
        positions={}
        for array,coords in baseline_coords.items():
            positions[array]={
                f:(x+rng.uniform(-FIG_JITTER_ERROR_M,FIG_JITTER_ERROR_M),
                   y+rng.uniform(-FIG_JITTER_ERROR_M,FIG_JITTER_ERROR_M))
                for f,(x,y) in coords.items()}
        elected,_=choose_array_lambdas(population,positions)
        try:
            values,_=score_heldout(population,positions,elected,require_source_support=False)
        except Exception as e:
            raise ValueError("NO_GO_DIGITIZATION_PERTURBATION_MODEL_FAILED") from e
        for array,r in values.items():
            if r["status"]!="HELDOUT_TEST_SUPPORT_PASS":
                raise ValueError("NO_GO_JITTER_CHANGED_SOURCE_SAMPLE_SUPPORT")
            gains[array].append(r["bee_equal_external_direction_gain_nats"])
            lambdas[array][str(elected[array])]+=1
    return {
        array:{
            "source_figure_perturbations":replicates,
            "seed":seed,
            "nominal_original_figure_per_coordinate_error_m":FIG_JITTER_ERROR_M,
            "mean_bee_equal_gain_nats_across_jitter":sum(xs)/len(xs),
            "minimum_bee_equal_gain_nats_across_jitter":min(xs),
            "maximum_bee_equal_gain_nats_across_jitter":max(xs),
            "replicates_positive_direction":sum(x>0 for x in xs),
            "source_train_only_selected_distance_penalty_count":dict(lambdas[array]),
            "jitter_not_new_independent_animal_or_study_replication":True
        }
        for array,xs in gains.items()
    }

def analyze(source_rows,geometry_path=GEOFILE,image_path=None,
            expected_original=True,permutations=PERMUTATIONS,
            jitter_replicates=FIG_JITTER_REPLICATES):
    coords,figure=verify_source_plot_coordinates(
        geometry_path,source_image=image_path)
    groups,source=source_bout_events(source_rows)
    if expected_original and (source.get("original_bouts"),
                              source.get("valid_bouts"),
                              source.get("excluded_nest_boundary_bouts"))!=(1740,1720,20):
        raise ValueError("NO_GO_SOURCE_AMENDMENT_20_STRUCTURAL_BOUTS_CHANGED")
    pop,excluded=split_bouts(groups,expected_original=expected_original)
    lambdas,laudit=choose_array_lambdas(pop,coords)
    comparisons,events=score_heldout(
        pop,coords,lambdas,require_source_support=expected_original)
    if expected_original and any(v["status"]!="HELDOUT_TEST_SUPPORT_PASS" for v in comparisons.values()):
        raise ValueError("NO_GO_SOURCE_HELDOUT_SUPPORT_NOT_MET")
    null=permutation_null_by_array(
        events,pop,coords,lambdas,comparisons,permutations=permutations)
    sensitivity=jitter_plot_uncertainty(
        pop,coords,replicates=jitter_replicates)
    return {
        "status":"REAL_ORIGINAL_SOURCE_DIRECTION_RULE_TRANSPORT_EVALUATED",
        "source_doi":"10.1038/s41598-017-04919-8",
        "external_prior_model":"Pasquaretta2019 Stage6 κ=1.0 frozen on different experiment, not fit in this study",
        "original_2017_colony_replication_ceiling":2,
        "source_original_bout_accounting":source,
        "source_exclusions_prior_outcome":excluded,
        "source_original_publisher_figure1_quality":figure,
        "train_only_lambda_by_original_array":laudit,
        "original_heldout_comparisons_by_array":comparisons,
        "original_heldout_conditional_direction_null_by_array":null,
        "fixed_21_plot_digitization_perturbations":sensitivity,
        "not_measured_individual_flight_heading":True,
        "not_randomized_experimental_array_order":True,
        "no_adaptive_information_query_cost_identified":True
    }
