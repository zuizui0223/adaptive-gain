"""Stage67 authentic paper-only overlap: independently published UV vs pollination.

Source A: Stage49 original Koski2016+Tunes2021 measured 230 UV pattern
positive/uniform states among 262 accepted species, source artifact 43863056927.
Source B: Stephens et al 2023 original Angiosperm pollination macroevolution
published Github data_output/pollination1209.csv, 1201 phylogenetic taxa.
No FCP images / GBIF opportunistic flower photo traits / imputed scent.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,urllib.request
from collections import Counter,defaultdict
from pathlib import Path

URL="https://raw.githubusercontent.com/rubysaltbush/pollination-macroevolution/main/data_output/pollination1209.csv"
GIT_BLOB_SHA1="0b5f841eecbf55a2e8ba9c21603f5eccd8bddfbf"
EXPECTED_POLLINATION_ORIGINAL=1201
EXPECTED_UV_REGISTRY=262
EXPECTED_DIRECT_UV={"1":101,"0":129,"":32}
SOURCE_DOI_POLLINATION="10.1111/nph.18993"
SOURCE_DOIS_UV=("10.1111/nph.13921","10.3389/fpls.2021.618028")

def check(ok,why):
    if not ok:raise ValueError("STAGE67_ORIGINAL_LITERATURE_NO_GO_"+why)

def fetch_author_supplement(opener=urllib.request.urlopen):
    req=urllib.request.Request(URL,headers={
        "Accept":"text/csv,text/plain,*/*",
        "User-Agent":"adaptive-gain-stage67-authentic-pollination2023-species-source/2026"})
    with opener(req,timeout=50) as f:
        data=f.read(1_800_000)
    blob=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
    check(blob==GIT_BLOB_SHA1,"GITHUB_ORIGINAL_SOURCE_BLOB_BYTES")
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig")))),hashlib.sha256(data).hexdigest()

def verified_original_uv(path):
    rows=list(csv.DictReader(Path(path).open(encoding="utf-8",newline="")))
    check(len(rows)==EXPECTED_UV_REGISTRY,"ORIGINAL_UV262_ACCEPTED_REGISTRY")
    keys=[r["gbif_accepted_species_key"] for r in rows]
    check(all(k.isdigit() for k in keys) and len(set(keys))==len(keys),
          "ORIGINAL_GBIF262_KEYS_NONUNIQUE")
    check(Counter(r["source_measured_UV_spatial_pattern_or_missing"] for r in rows)
          ==Counter(EXPECTED_DIRECT_UV),"ORIGINAL_UV230_SOURCE_LABELS")
    return rows

def literal_binomial(s):
    v=" ".join(str(s or "").replace("_"," ").strip().split())
    chunks=v.split()
    if len(chunks)!=2 or not (chunks[0][:1].isupper()
                              and chunks[1][:1].islower()):
        return ""
    return v.casefold()

def audit(pollination,uv_rows,source_digest="UNIT_TEST_ONLY"):
    check(len(pollination)==EXPECTED_POLLINATION_ORIGINAL,
          "PUBLISHED_1201_POLLINATION_TAXA_DENOMINATOR")
    check(len(uv_rows)==EXPECTED_UV_REGISTRY,
          "PUBLISHED_262_ACCEPTED_UV_REGISTRY_DENOMINATOR")
    require={"taxon_name","pollination","syndrome_or_system","rank_scored_at",
             "scent","nectar","pollination_data_source","ParFamTax"}
    check(all(require.issubset(r) for r in pollination),"POLLINATION_SCHEMA")
    authors={}
    for r in pollination:
        key=literal_binomial(r["taxon_name"])
        if not key:continue
        check(key not in authors,"ORIGINAL_2023_BINOMIAL_DUPLICATE")
        authors[key]=r
    matched=[];observed=[]
    uv_genera=set()
    for r in uv_rows:
        key=literal_binomial(r["source_taxon_aliases"])
        if not key:continue
        uv_genera.add(key.split()[0])
        if key in authors:
            orig=authors[key]
            u=r["source_measured_UV_spatial_pattern_or_missing"]
            matched.append({
                "published_literal_exact_binomial":key,
                "original_gbif_accepted_key_from_UV_only":r["gbif_accepted_species_key"],
                "UV_spatial_source_binary_or_unknown":u,
                "UV_study_source_DOIs":r["source_study_DOIs"],
                "original_2023_pollination_label":orig["pollination"],
                "original_2023_syndrome_or_system":orig["syndrome_or_system"],
                "original_2023_rank_scored_at":orig["rank_scored_at"],
                "original_2023_scent_reported_or_UNKNOWN":orig["scent"],
                "original_2023_nectar_reported_or_UNKNOWN":orig["nectar"],
                "original_2023_pollination_scoring_source":orig["pollination_data_source"],
                "two_studies_different_taxonomy_concepts_not_verified_sisters":True,
                "flower_photographed_in_either_source":False,
                "not_same_population_or_true_pollinator_visits":True})
            if u in ("0","1"):
                observed.append(matched[-1])
    name_genera={v.split()[0] for v in authors}
    reported_p=Counter(r["pollination"] for r in pollination)
    missing_p=sum(r["pollination"] in ("NA","","unknown","?") for r in pollination)
    check(missing_p==41,"ORIGINAL_2023_1160_KNOWN_POLLINATION_LABELS")
    dist={
      "schema":"authentic_published_species_pollination1201_x_UV230_literal_cross_study_coverage",
      "original_2023_pollination_source_DOI":SOURCE_DOI_POLLINATION,
      "original_2023_original_GitHub_blob_SHA1":GIT_BLOB_SHA1,
      "original_2023_original_source_sha256":source_digest,
      "original_2023_phylogenetic_named_taxa":len(pollination),
      "original_2023_pollination_nonmissing_labels":len(pollination)-missing_p,
      "original_2023_pollination_syndrome_or_system_counts":dict(sorted(
          Counter(r["syndrome_or_system"] for r in pollination).items())),
      "original_2023_scent_yes_no_unknown":dict(sorted(Counter(
          r["scent"] for r in pollination).items())),
      "original_2023_nectar_yes_no_unknown":dict(sorted(Counter(
          r["nectar"] for r in pollination).items())),
      "original_2023_flower_pollinator_class_counts":dict(sorted(reported_p.items())),
      "original_2023_scoring_at_taxonomic_rank_counts":dict(sorted(Counter(
          r["rank_scored_at"] for r in pollination).items())),
      "prior_independently_measured_UV_spatial_original_accepted_taxa":230,
      "prior_independently_measured_UV_spatial_positive":101,
      "prior_independently_measured_UV_spatial_uniform_negative":129,
      "n_source_exact_original_binomials_across_papers":len(matched),
      "n_source_direct_UV_original_binomials_with_known_original_2023_pollination":sum(
          r["UV_spatial_source_binary_or_unknown"] in ("0","1")
          and r["original_2023_pollination_label"] not in ("NA","","?") for r in matched),
      "n_source_direct_UV_original_binomials_with_any_pollination_label":len(observed),
      "n_source_UV_original_genera_shared_with_2023_pollination":len(uv_genera&name_genera),
      "shared_original_genera_only_not_valid_species_trait_imputation":True,
      "original_pollination_syndrome_is_NOT_a_real_visitation_or_biochemical_scent_measurement":True,
      "no_nonmatching_plant_becomes_UV_or_scent_negative":True,
      "no_2023_pollination_species_key_accepted_by_GBIF_without_new_validation":True,
      "n_suitable_paired_study_species_for_independent_macro_association_if_at_least30":(
          len(observed) if len(observed)>=30 else 0),
      "NO_GO_joint_uv_pollinator_species_effect_if_under30":len(observed)<30,
    }
    return matched,dist

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--original-262-author-measured-UV",required=True)
    ap.add_argument("--outdir",default="stage67_published_original_UV_x_pollination_species")
    a=ap.parse_args()
    uv=verified_original_uv(a.original_262_author_measured_UV)
    original,source_sha=fetch_author_supplement()
    rows,receipt=audit(original,uv,source_sha)
    out=Path(a.outdir);out.mkdir(parents=True,exist_ok=True)
    (out/"published_original_1201_pollination_x_262_UV_evidence_receipt.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    with (out/"literal_source_species_overlap_original_UV_pollination.csv").open(
          "w",encoding="utf8",newline="") as handle:
        cols=["published_literal_exact_binomial","original_gbif_accepted_key_from_UV_only",
            "UV_spatial_source_binary_or_unknown","UV_study_source_DOIs",
            "original_2023_pollination_label","original_2023_syndrome_or_system",
            "original_2023_rank_scored_at","original_2023_scent_reported_or_UNKNOWN",
            "original_2023_nectar_reported_or_UNKNOWN","original_2023_pollination_scoring_source",
            "two_studies_different_taxonomy_concepts_not_verified_sisters",
            "flower_photographed_in_either_source","not_same_population_or_true_pollinator_visits"]
        w=csv.DictWriter(handle,fieldnames=cols);w.writeheader();w.writerows(rows)
    print("STAGE67_REAL_LITERATURE_ONLY_2023_ANGIOSPERM_POLLINATION_VS_230_UV",
          json.dumps({k:v for k,v in receipt.items() if k.startswith("n_") or k.startswith("NO_GO")},
                     sort_keys=True))
    print("NO_FCP_PHOTO_OR_PSEUDO_UV_LABEL_AND_NO_UNMEASURED_SCENT_AS_NEGATIVE")
if __name__=="__main__":main()
