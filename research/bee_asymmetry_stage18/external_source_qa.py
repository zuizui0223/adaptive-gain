"""Read-only audit of published bee information-request source labels, no effects fitted.

This is another author's 2026 bioRxiv PREPRINT and its public source
dataset. It does not document source selection U/V or our R-conditioned
stopping treatment. It must never be called an independent Stage18 result.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
from collections import Counter,defaultdict
from pathlib import Path
from urllib.request import Request,urlopen

ORIGINAL_REPO="Cuixiaojian21/bee_metacognition"
COMMIT="7f886394b4de872ecdb19ca4ea214ec321d5dce9"
FILE="data/4_active_information_seeking_trials.csv"
ORIGINAL_GIT_BLOB_SHA1="26259c9071c6d73141d56b9bedd396cab1a04491"
SOURCE_URL=f"https://raw.githubusercontent.com/{ORIGINAL_REPO}/{COMMIT}/{FILE}"
PREPRINT_DOI="10.64898/2026.09.15.751944"
FIELDS=("Trial_ID","Bee_ID","Trial_Number","Difficulty","Trial_Type",
        "Info_Requested","Actually_Landed_On_Platform",
        "Post_Request_Accuracy","Is_Post_Request_Correct",
        "Non_Request_Accuracy","Is_Post_Non_Request_Correct")


def git_blob_sha1(data):
    if not isinstance(data,bytes):
        raise ValueError("NO_GO_GIT_SOURCE_NOT_BYTES")
    return hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()


def audit_rows(rows,strict_original=True):
    if not rows:raise ValueError("NO_GO_EMPTY_ORIGINAL_TRIAL_SOURCE")
    ids=set();perbee=defaultdict(list)
    groups=defaultdict(lambda:{"n":0,"info":0,"landed":0})
    group_count=Counter()
    mismatch=Counter()
    for row in rows:
        if set(FIELDS)-set(row):
            raise ValueError("NO_GO_SOURCE_EXPECTED_BEHAVIOR_COLUMNS_MISSING")
        ident=row["Trial_ID"]
        if ident in ids:raise ValueError("NO_GO_DUPLICATE_SOURCE_TRIAL_ID")
        ids.add(ident)
        bee=row["Bee_ID"]
        if not bee:raise ValueError("NO_GO_MISSING_SOURCE_BEE_ID")
        difficulty=row["Difficulty"];trial=row["Trial_Type"]
        if difficulty not in ("Easy","Hard","Impossible") or trial not in ("Regular","Random_Free_Cue"):
            raise ValueError("NO_GO_UNKNOWN_AUTHOR_ORIGINAL_TRIAL_CONDITION")
        request=row["Info_Requested"];land=row["Actually_Landed_On_Platform"]
        if request not in ("0","1") or land not in ("0","1"):
            raise ValueError("NO_GO_INVALID_ORIGINAL_SOURCE_BINARY")
        key=(trial,difficulty)
        group_count[key]+=1
        groups[key]["n"]+=1
        groups[key]["info"]+=int(request)
        groups[key]["landed"]+=int(land)
        if request!=land:mismatch[trial]+=1
        perbee[bee].append(row)
    monotonic=Counter()
    for bee,records in perbee.items():
        regular=[x for x in records if x["Trial_Type"]=="Regular"]
        means={}
        for diff in ("Easy","Hard","Impossible"):
            sub=[x for x in regular if x["Difficulty"]==diff]
            if not sub:
                raise ValueError("NO_GO_MISSING_BEE_DIFFICULTY_CELL")
            means[diff]=sum(int(x["Actually_Landed_On_Platform"]) for x in sub)/len(sub)
        if means["Hard"]>means["Easy"]:monotonic["hard_gt_easy"]+=1
        if means["Impossible"]>means["Hard"]:monotonic["impossible_gt_hard"]+=1
        if means["Impossible"]>means["Easy"]:monotonic["impossible_gt_easy"]+=1
        if means["Easy"]<means["Hard"]<means["Impossible"]:
            monotonic["strict_increase"]+=1
    if strict_original:
        counts={(t,d):n for (t,d),n in group_count.items()}
        expected={
            ("Regular","Easy"):6140,("Regular","Hard"):6108,
            ("Regular","Impossible"):3112,
            ("Random_Free_Cue","Easy"):1540,("Random_Free_Cue","Hard"):1572,
            ("Random_Free_Cue","Impossible"):728}
        if len(rows)!=19200 or len(perbee)!=192 or counts!=expected:
            raise ValueError("NO_GO_ORIGINAL_PUBLIC_SAMPLE_CHANGED")
        if any(len(v)!=100 for v in perbee.values()):
            raise ValueError("NO_GO_AUTHOR_ORIGINAL_REPEATED_BEE_GRAIN_CHANGED")
        if mismatch["Regular"]!=0 or mismatch["Random_Free_Cue"]!=1812:
            raise ValueError("NO_GO_SOURCE_FREE_CUE_SEMANTICS_CHANGED")
        if monotonic["hard_gt_easy"]!=192 or monotonic["strict_increase"]!=181:
            raise ValueError("NO_GO_AUTHOR_ORIGINAL_BEE_DIFFICULTY_SUMMARY_CHANGED")
    return {
        "status":"ORIGINAL_PREPRINT_SOURCE_GRAIN_AUDITED_NO_NEW_CAUSAL_ANALYSIS",
        "source_repository":ORIGINAL_REPO,
        "source_original_commit":COMMIT,
        "source_original_git_blob_sha1":ORIGINAL_GIT_BLOB_SHA1,
        "bioRxiv_preprint_doi":PREPRINT_DOI,
        "peer_review_not_independently_verified":True,
        "total_rows":len(rows),"source_bees":len(perbee),
        "trial_type_by_difficulty":{
           "__".join(key):dict(v) for key,v in sorted(groups.items())},
        "free_cue_info_requested_unconditional":
             sum(v["info"] for (t,d),v in groups.items() if t=="Random_Free_Cue"),
        "free_cue_actual_landed":
             sum(v["landed"] for (t,d),v in groups.items() if t=="Random_Free_Cue"),
        "auto_info_vs_platform_mismatch":mismatch["Random_Free_Cue"],
        "regular_flag_vs_actual_landing_mismatch":mismatch["Regular"],
        "n_bees_hard_request_gt_easy":monotonic["hard_gt_easy"],
        "n_bees_impossible_request_gt_hard":monotonic["impossible_gt_hard"],
        "n_bees_easy_lt_hard_lt_impossible":monotonic["strict_increase"],
        "not_independent_colonies":True,
        "data_without_actual_selectable_U_V_channel_identity":True,
        "not_root_observation_contingent_querying":True,
        "no_new_statistical_effect_fitted":True,
        "no_source_rows_redistributed":True,
    }


def run(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    request=Request(SOURCE_URL,headers={"User-Agent":"adaptive-gain-source-integrity-audit/1.0",
                                       "Accept":"text/csv,*/*"})
    with urlopen(request,timeout=60) as resp:
        if resp.status!=200:raise ValueError("NO_GO_ORIGINAL_SOURCE_HTTP")
        raw=resp.read(2_000_001)
    if len(raw)>2_000_000:
        raise ValueError("NO_GO_ORIGINAL_DATA_SIZE_LIMIT")
    sha=git_blob_sha1(raw)
    if sha!=ORIGINAL_GIT_BLOB_SHA1:
        raise ValueError("NO_GO_ORIGINAL_AUTHOR_GIT_BLOB_SHA_CHANGED "+sha)
    text=raw.decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(text,newline=""))
    if tuple(reader.fieldnames or [])!=FIELDS:
        raise ValueError("NO_GO_NATIVE_ORIGINAL_COLUMN_GRAIN_CHANGED")
    rows=list(reader)
    result=audit_rows(rows,strict_original=True)
    result["original_content_sha256"]=hashlib.sha256(raw).hexdigest()
    result["original_bytes"]=len(raw)
    out=root/"stage18_external_information_request_source_qa.json"
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE18_EXTERNAL_SOURCE_GRAIN "+json.dumps({
        k:v for k,v in result.items() if k!="trial_type_by_difficulty"
    },ensure_ascii=False,allow_nan=False),flush=True)
    return result


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="stage18_exact_outputs")
    run(p.parse_args().out)
