"""Klein et al. (2017): exact original 1,740 per-bout flower sequences.

Source CSV: Supplement S1, DOI 10.1038/s41598-017-04919-8.
The source 'sqce_tot' stores nest (0) and four physical flowers 1..4.
Do not strip visits, invent unavailable options, infer flight coordinates
or fit any directional regression until the original Fig1 positions pass.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from pathlib import Path
import csv
import hashlib
import io
import json
import re

SOURCE_S1="41598_2017_4919_MOESM2_ESM.csv"
SOURCE_S2="41598_2017_4919_MOESM3_ESM.csv"
SHA_S1="e1b660125c389fc873a70eaf0edaaec053637cc814d8bcb50f1a61a01b7e3e04"
SHA_S2="68e663f50d7d741c3a162f67b03db89499aff4c328aecf09361cf15955440535"
HEAD_S1=("bee_ID","colony","age","body","array","bout","nb_flower",
         "imm_revisit","non_imm_revisit","speed","prop","sqce_tot")
HEAD_S2=("bee_ID","colony","array","nb_flower","se_nb_flower","imme_revisit",
         "se_imme_revisit","non_imm_revis","se_non_imm_revis","speed",
         "se_speed","prop","DET","age","body")
EXACT_SOURCE_BOUTS=1740
EXACT_BEE_ARRAY_CELLS=87
COLONIES_EXPECTED=2
BEES_EXPECTED=29
LAYOUTS=("1","2","3")
TRIPS=range(1,21)
FLOWERS=frozenset("1234")

def pinned_csv(path:Path,sha,columns):
    raw=path.read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=sha:
        raise ValueError("NO_GO_ORIGINAL_2017_SOURCE_SHA256_CHANGED "+path.name)
    txt=raw.decode("utf-8-sig",errors="strict")
    # Original Springer CSV uses carriage-return line endings; preserve them
    # with newline="" so the csv module, not StringIO, handles record lines.
    reader=csv.DictReader(io.StringIO(txt,newline=""),delimiter=",")
    if tuple(reader.fieldnames)!=tuple(columns):
        raise ValueError("NO_GO_ORIGINAL_2017_CSV_HEADER_CHANGED "+path.name)
    rows=list(reader)
    if any(None in row or any(v is None for v in row.values()) for row in rows):
        raise ValueError("NO_GO_SOURCE_HAS_RAGGED_OR_NULL_ROW")
    return rows,{"original_sha256":digest,"original_bytes":len(raw),
                 "native_columns":list(reader.fieldnames),
                 "native_rows":len(rows)}

def parse_quoted_sequence(raw):
    """A source cell may retain an unmatched trailing quote in its text.
    Remove only non-signifying outer ASCII quotes; never alter digits, zeros,
    flower visits, or their left-to-right original order.
    """
    stripped=str(raw).strip()
    cleaned=stripped.strip('"').strip()
    if not cleaned or not re.fullmatch(r"[0-9]+",cleaned):
        raise ValueError("NO_GO_UNRECOGNIZED_SOURCE_SEQUENCE_SYMBOL "+repr(stripped[:100]))
    if any(symbol not in "01234" for symbol in cleaned):
        raise ValueError("NO_GO_SOURCE_FLOWER_ID_OUTSIDE_REAL_FOUR_LOCATION_ARRAY")
    return cleaned

def validate_bouts(rows,expected=True):
    key_counts=Counter()
    bee_colonies=defaultdict(set)
    by_colony=Counter()
    by_array=Counter()
    source_stats=Counter()
    length_hist=Counter()
    flower_visits=Counter()
    extra_zero_pos=0
    missing_source_details=Counter()
    original_sequence_shapes=Counter()
    parsed=[]
    source_boundary_anomalies=[]
    for idx,row in enumerate(rows):
        bee=row["bee_ID"].strip()
        col=row["colony"].strip()
        array=row["array"].strip()
        try:bout=int(row["bout"].strip())
        except Exception as e:raise ValueError("NO_GO_UNPARSEABLE_BOUT_NUMBER") from e
        if not bee or not col or array not in LAYOUTS or bout not in TRIPS:
            raise ValueError("NO_GO_INVALID_ORIGINAL_BEE_COLONY_ARRAY_BOUT")
        source_seq=row["sqce_tot"]
        original_sequence_shapes[
            (source_seq.startswith('"'),source_seq.endswith('"'))]+=1
        seq=parse_quoted_sequence(source_seq)
        original_sequence_symbols=list(seq)
        if seq[0]!="0" or seq[-1]!="0":
            source_stats["bouts_without_explicit_source_nest_start_and_end"]+=1
            source_boundary_anomalies.append({
                "kind":"missing_nest_start_or_end",
                "colony":col,"bee_tag":bee,"array":array,"bout":bout,
                "source_line":idx+2,
                "original_source_string_repr":repr(source_seq),
                "cleaned_native_symbols":seq,
                "source_reported_nb_flower":row["nb_flower"].strip()
            })
        internal=seq[1:-1]
        if "0" in internal:
            extra_zero_pos+=1
            source_boundary_anomalies.append({
                "kind":"internal_nest_marker",
                "colony":col,"bee_tag":bee,"array":array,"bout":bout,
                "source_line":idx+2,
                "original_source_string_repr":repr(source_seq),
                "cleaned_native_symbols":seq,
                "source_reported_nb_flower":row["nb_flower"].strip()
            })
        for k in ("nb_flower","imm_revisit","non_imm_revisit","speed","body"):
            if not row[k].strip():missing_source_details[k]+=1
        keys=(col,bee,array,bout)
        key_counts[keys]+=1
        bee_colonies[bee].add(col)
        by_colony[col]+=1
        by_array[array]+=1
        source_stats["rows"]+=1
        source_stats["all_sequence_positions"]+=len(seq)
        source_stats["source_flower_visit_tokens"]+=sum(symbol in FLOWERS for symbol in seq)
        source_stats["within_bout_adjacent_flower_pairs"]+=sum(
            a in FLOWERS and b in FLOWERS for a,b in zip(seq[:-1],seq[1:]))
        source_stats["within_bout_real_two_step_triplets"]+=sum(
            a in FLOWERS and b in FLOWERS and c in FLOWERS and a!=b and b!=c
            for a,b,c in zip(seq[:-2],seq[1:-1],seq[2:]))
        flower_visits.update(symbol for symbol in seq if symbol in FLOWERS)
        length_hist[str(len(seq))]+=1
        valid_direction=(seq[0]=="0" and seq[-1]=="0"
                         and "0" not in seq[1:-1])
        parsed.append({"colony":col,"bee":bee,"array":array,
                       "bout":bout,"flower_sequence":seq,
                       "source_file_row":idx+2,
                       "eligible_strict_complete_nest_borders":valid_direction})
    collisions={k:v for k,v in key_counts.items() if v!=1}
    by_bee_array=Counter((c,b,a) for c,b,a,i in key_counts)
    qualified=Counter(key_counts.keys())
    bees=set((c,b) for c,b,a,i in key_counts)
    layout_counts=Counter((c,b,a) for c,b,a,i in key_counts)
    incomplete={str(key):n for key,n in layout_counts.items() if n!=20}
    result={
        "source_S1_rows":len(rows),
        "source_distinct_experimental_bees":len(bees),
        "source_bee_labels_reused_between_colonies":sum(len(v)>1 for v in bee_colonies.values()),
        "source_independent_colonies":len(by_colony),
        "source_bout_rows_by_colony":dict(by_colony),
        "source_bout_rows_by_array":dict(sorted(by_array.items())),
        "original_unique_bee_array_cells":len(layout_counts),
        "source_bouts_per_bee_array_min":min(layout_counts.values()) if layout_counts else None,
        "source_bouts_per_bee_array_max":max(layout_counts.values()) if layout_counts else None,
        "source_bee_array_cells_with_non20_bouts":incomplete,
        "source_duplicate_colony_bee_array_bout_keys":len(collisions),
        "native_sequence_fields":dict(source_stats),
        "source_flower_id_visit_frequency":dict(sorted(flower_visits.items())),
        "original_unbalanced_outer_ascii_quotes":{str(k):v for k,v in original_sequence_shapes.items()},
        "source_bouts_with_extra_internal_nest_marker":extra_zero_pos,
        "source_boundary_anomalies":source_boundary_anomalies[:30],
        "anomalies_count_no_silent_imputation":len(source_boundary_anomalies),
        "source_sequence_length_distribution":dict(sorted(length_hist.items(),key=lambda x:int(x[0]))),
        "original_nullable_nonsequence_fields":dict(missing_source_details),
        "source_grain":"one authentic bee per array per foraging bout, full raw nest→flower...→nest sequence",
        "source_physical_positions_not_in_S1":True,
        "array_ID_part_of_physical_flower_identity":True
    }
    gates=[
        len(rows)==EXACT_SOURCE_BOUTS,
        len(bees)==BEES_EXPECTED,
        len(by_colony)==COLONIES_EXPECTED,
        len(layout_counts)==EXACT_BEE_ARRAY_CELLS,
        not collisions,not incomplete,
        set(by_array)==set(LAYOUTS),
        not result["source_bouts_with_extra_internal_nest_marker"],
        not source_stats["bouts_without_explicit_source_nest_start_and_end"],
        set(flower_visits)==set(FLOWERS)
    ]
    # Original-source audit before any movement model discovered exactly
    # 16 unclosed and 4 internally-nested source bouts. The frozen *post-
    # source, pre-outcome* exception excludes those 20 source rows ONLY from
    # actual direction-triplet models, retaining all 1740 provenance rows.
    # An arbitrary different count remains NO_GO rather than trimming data.
    boundary_bad=(source_stats["bouts_without_explicit_source_nest_start_and_end"],
                  extra_zero_pos)
    allkeys_ok=all(gates[:7]) and set(flower_visits)==set(FLOWERS)
    source_allowed=(boundary_bad==(0,0) or boundary_bad==(16,4))
    clean=sum(p["eligible_strict_complete_nest_borders"] for p in parsed)
    result["original_design_keys_gate"]="PASS" if allkeys_ok else "NO_GO_EXPERIMENTAL_DESIGN"
    result["source_explicit_boundary_anomaly_pair"]=list(boundary_bad)
    result["source_original_bouts_eligible_for_direction"]=clean
    result["source_original_bouts_excluded_only_for_nest_quality"]=len(parsed)-clean
    result["original_grain_gate"]=(
       "PASS_WITH_2017_SOURCE_BOUNDARY_AMENDMENT" if
       allkeys_ok and boundary_bad==(16,4) and clean==1720 else
       "PASS_FULLY_NEST_BOUNDED" if allkeys_ok and boundary_bad==(0,0) else
       "NO_GO_ORIGINAL_BEE_SOURCE_GRAIN")
    if expected and result["original_grain_gate"].startswith("NO_GO"):
        raise ValueError("NO_GO_ORIGINAL_BEE_SOURCE_GRAIN "+json.dumps(result)[:6000])
    return parsed,result

def source_run(folder):
    s1,receipt1=pinned_csv(folder/SOURCE_S1,SHA_S1,HEAD_S1)
    s2,receipt2=pinned_csv(folder/SOURCE_S2,SHA_S2,HEAD_S2)
    parsed,qa=validate_bouts(s1,expected=False)
    s2keys=Counter((r["colony"].strip(),r["bee_ID"].strip(),r["array"].strip()) for r in s2)
    s1keys=set((x["colony"],x["bee"],x["array"]) for x in parsed)
    qa["source_S2_rows"]=len(s2)
    qa["source_S2_duplicate_bee_array_cells"]=sum(v>1 for v in s2keys.values())
    qa["source_S2_aligned_with_S1_bee_array_keys"]=set(s2keys)==s1keys
    qa["source_S2_original_sha256"]=SHA_S2
    if len(s2)!=87 or not qa["source_S2_aligned_with_S1_bee_array_keys"] or qa["source_S2_duplicate_bee_array_cells"]:
        raise ValueError("NO_GO_SOURCE_S1_S2_BEE_ARRAY_RECONCILIATION")
    status=("ORIGINAL_2017_BOUTS_AND_S1_S2_MATCHED_WITH_EXPLICIT_20_EXCLUSIONS"
            if qa["original_grain_gate"]=="PASS_WITH_2017_SOURCE_BOUNDARY_AMENDMENT"
            else "NO_GO_ORIGINAL_NEST_MARKER_BOUNDARIES")
    report={"status":status,
            "source_doi":"10.1038/s41598-017-04919-8",
            "publisher_original_S1":receipt1,
            "publisher_original_S2":receipt2,
            "original_grain_quality":qa,
            "not_fitted_direction_model":True}
    (folder/"klein2017_true_bout_grain.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False))
    print("STAGE9_ORIGINAL_BOUT_GRAIN "+json.dumps(report,ensure_ascii=False),flush=True)
    print("STAGE9_ORIGINAL_BOUT_GRAIN_COMPLETE",flush=True)
    if status!="ORIGINAL_2017_BOUTS_AND_S1_S2_MATCHED_WITH_EXPLICIT_20_EXCLUSIONS":
        raise ValueError("NO_GO_ORIGINAL_SEQUENCE_BOUNDARY_SEMANTICS_UNRESOLVED")
    return parsed,report
if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="bee_stage9_original")
    args=parser.parse_args()
    source_run(Path(args.out))
