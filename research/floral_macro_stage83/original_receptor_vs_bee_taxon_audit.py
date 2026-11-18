"""Stage83: original Ohashi pavo honeybee receptor traits x true EuPP bee records.

Examines four explicit distal/near flower-age optical contrasts and tests
whether network-level score signals survive plant-taxonomic reshuffling.

No measured Bombus discrimination, true source-local flower-age at visitation,
scent-plume/landing motion, phylogenetic independent origins, or fitness is
identified by joining Japan spectral measurements to European visitor records.
"""
from __future__ import annotations
import argparse,hashlib,io,json,zipfile
from pathlib import Path
import numpy as np
import pandas as pd

ORIGINAL_EUPP_SHA="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"
ORIGINAL_RECEPTOR_CI_ZIP_SHA="9139935f10fbd94a8fb888d807af872c9e5289422249d138fb8a61ac799a0b2a"
ORIGINAL_RECEPTOR_ARTIFACT_ID=14409142056
RECEPTOR_MEMBER="stage81d_derived_bee_receptor_metrics/stage81d_original_28_apis_far_near_species.csv"
RECEIPT_MEMBER="stage81d_derived_bee_receptor_metrics/stage81d_original_28_apis_d65_far_near_source_receipt.json"
TARGETS={
 "far_green_signed_delta":"median_delta_far_green_abs",
 "near_hex_signed_delta":"median_delta_near_hex_chroma",
 "age_hex_shift_magnitude":"median_age_colour_shift_hex",
 "far_maintained_near_reduced_indicator":"_stage_discordance",
}
KEY=("Study_id","Network_id","Year_from_original_date")
TAXON="Original_plant_accepted_name_literal"

def publication_id(source_id):
    s=str(source_id)
    return "23_24_25_ONE_PUBLISHED_STUDY" if s.split("_",1)[0] in {"23","24","25"} else s

def source_eupp(path):
    b=Path(path).read_bytes()
    if hashlib.sha256(b).hexdigest()!=ORIGINAL_EUPP_SHA:
        raise ValueError("STAGE83_ORIGINAL_EUPP_SOURCE_DIGEST_CHANGED")
    d=pd.read_csv(io.BytesIO(b))
    if len(d)!=18798 or d[TAXON].nunique()!=1408:
        raise ValueError("STAGE83_ORIGINAL_EUPP_FLORA_18798_1408_CHANGED")
    return d

def source_receptor(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ORIGINAL_RECEPTOR_CI_ZIP_SHA:
        raise ValueError("STAGE83_SOURCE_PAVO_RECEPTOR_CI_ZIP_SHA_CHANGED")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        d=pd.read_csv(io.BytesIO(z.read(RECEPTOR_MEMBER)))
        receipt=json.loads(z.read(RECEIPT_MEMBER))
    if len(d)!=28 or d.source_species.nunique()!=28:
        raise ValueError("STAGE83_RECEPTOR_28_ORIGINAL_SPECIES_CHANGED")
    if (receipt["original_spectra_n"]!=1360
        or receipt["original_source_age_parts"]!=53
        or receipt["source_28_species_with_model_detectable_hex_change"]!=5
        or receipt["fitted_visual_system"]!="pavo_APIS_HONEYBEE_D65_GREEN_VON_KRIES_Ei_colour_hexagon"):
        raise ValueError("STAGE83_RECEPTOR_PROVENANCE_CHANGED")
    d["_stage_discordance"]=(
      (d["median_delta_far_green_abs"]>=0)&
      (d["median_delta_near_hex_chroma"]<0)).astype(float)
    if d["_stage_discordance"].sum()!=12:
        raise ValueError("STAGE83_NOT_12_SOURCE_OPTICAL_STAGE_DISCORDANCES")
    return d

def original_frame(flora,traits):
    f=flora.loc[flora[TAXON].isin(set(traits.source_species))].copy()
    if f[list(KEY)+[TAXON]].duplicated().any():
        raise ValueError("STAGE83_DUPLICATE_PLANT_SITE")
    if len(f)!=1921 or f.groupby(list(KEY)).ngroups!=1040:
        raise ValueError("STAGE83_ORIGINAL_SOURCE_VISITED_PLANT_GRAIN_CHANGED")
    eligible=f.groupby(list(KEY),sort=True).filter(lambda g:g[TAXON].nunique()>=2)
    if eligible.groupby(list(KEY)).ngroups!=537:
        raise ValueError("STAGE83_SOURCE_537_PRE_BEE_NETWORKS_CHANGED")
    names=sorted(traits.source_species)
    t=traits.set_index("source_species").loc[names]
    z=[]
    for name,col in TARGETS.items():
        v=t[col].to_numpy(dtype=float)
        if name!="far_maintained_near_reduced_indicator":
            v=(v-v.mean())/v.std(ddof=1)  # each 28 plant species one unit
        if not np.isfinite(v).all():raise ValueError("STAGE83_BAD_BEE_SOURCE_RECEPTOR_VALUES")
        z.append(v)
    z=np.stack(z,axis=1)
    index={sp:i for i,sp in enumerate(names)}
    records=[]
    for key,g in eligible.groupby(list(KEY),sort=True):
        b=g.n_observed_Bombus.to_numpy(dtype=float)
        o=g.n_observed_other_bee.to_numpy(dtype=float)
        n=b+o
        if (n>0).sum()<2 or b.sum()<=0 or o.sum()<=0:continue
        p=b.sum()/n.sum()
        bi=np.zeros(len(names));oi=np.zeros(len(names))
        for name,bb,oo in zip(g[TAXON],b,o):
            i=index[name];bi[i]+=bb;oi[i]+=oo
        ni=bi+oi
        records.append({"pub":publication_id(g["Study_id"].iloc[0]),
                        "study":str(g["Study_id"].iloc[0]),
                        "key":tuple(map(str,key)),
                        "b":bi,"o":oi,"n":ni,"p":p,
                        "N":n.sum(),"u":bi-ni*p})
    if len(records)!=194 or len({r["pub"] for r in records})!=30:
        raise ValueError("STAGE83_REAL_194_NETWORK_30_PUBLICATION_GUILD_PANEL_CHANGED")
    spp={names[i] for r in records for i,weight in enumerate(r["n"]) if weight>0}
    if len(spp)!=23:
        raise ValueError("STAGE83_REAL_23_OF_28_TRAITS_SAMPLED_WITH_INFORMATIVE_GUILDS_CHANGED")
    return z,names,records,{"original_28_source_flora_rows":len(f),
            "outcome_blind_two_species_networks":537,
            "bee_informative_network_years":194,
            "independent_original_publications":30,
            "species_with_some_bee_information":len(spp)}

def score_records(z,records,details=False):
    if not records:raise ValueError("STAGE83_EMPTY_SOURCE_NETWORK")
    u=np.stack([r["u"] for r in records])
    n=np.stack([r["n"] for r in records])
    p=np.array([r["p"] for r in records]);N=np.array([r["N"] for r in records])
    U=u@z
    Ns=n@z
    I=(p*(1-p))[:,None]*(n@(z*z)-Ns*Ns/N[:,None])
    I=np.maximum(I,0)
    allowed=I>1e-9
    U=U*allowed;I=I*allowed
    numerator=U.sum(axis=0);denominator=I.sum(axis=0)
    result={"score":np.divide(numerator,denominator,out=np.full(z.shape[1],np.nan),where=denominator>1e-9),
            "z":np.divide(numerator,np.sqrt(denominator),out=np.full(z.shape[1],np.nan),where=denominator>1e-9),
            "network_counts":allowed.sum(axis=0),
            "U":numerator,"I":denominator}
    if details:
        result.update({"U_network":U,"I_network":I,"pubs":np.array([r["pub"] for r in records])})
    return result

def bootstrap_studies(result,reps=5000,seed=20261118):
    names=sorted(set(result["pubs"]))
    pu=np.stack([result["U_network"][result["pubs"]==p].sum(axis=0) for p in names])
    pi=np.stack([result["I_network"][result["pubs"]==p].sum(axis=0) for p in names])
    rng=np.random.default_rng(seed)
    ix=rng.integers(0,len(names),size=(reps,len(names)))
    numer=pu[ix].sum(axis=1);denom=pi[ix].sum(axis=1)
    ratios=np.divide(numer,denom,out=np.full_like(numer,np.nan),where=denom>1e-9)
    rows=[]
    for j in range(pi.shape[1]):
        weights=pi[:,j]/pi[:,j].sum()
        valid=ratios[:,j];valid=valid[np.isfinite(valid)]
        rows.append({"publication_info_effective_n":float(1/(weights*weights).sum()),
                     "largest_single_publication_information_fraction":float(weights.max()),
                     "publications_with_information":int((pi[:,j]>1e-9).sum()),
                     "publication_cluster_bootstrap_95_descriptive":[float(v) for v in np.quantile(valid,[.025,.975])]})
    return rows

def permute_source_taxon_vectors(z,records,reps=9999,seed=20261119):
    """Shuffle all four traits TOGETHER across 28 taxa; never by network."""
    n=np.stack([r["n"] for r in records]);u=np.stack([r["u"] for r in records])
    p=np.array([r["p"] for r in records]);N=np.array([r["N"] for r in records])
    rng=np.random.default_rng(seed)
    results=np.empty((reps+1,z.shape[1]))
    for start in range(0,reps+1,100):
        stop=min(start+100,reps+1)
        batch=[z] if start==0 else []
        while len(batch)<stop-start:
            batch.append(z[rng.permutation(len(z))])
        x=np.stack(batch,axis=1) # taxon, trial, signal
        U=np.einsum("nt,trc->nrc",u,x)
        T=np.einsum("nt,trc->nrc",n,x)
        I=(p*(1-p))[:,None,None]*(np.einsum("nt,trc->nrc",n,x*x)-T*T/N[:,None,None])
        I=np.maximum(I,0)
        ok=I>1e-9
        results[start:stop]=(U*ok).sum(axis=0)/np.sqrt((I*ok).sum(axis=0))
    observed=results[0];null=results[1:];maxnull=np.abs(null).max(axis=1)
    return [{"observed_naive_U_over_sqrtI":float(observed[j]),
      "species_vector_permutation_two_sided_tail_fraction":float(
          (1+(np.abs(null[:,j])>=abs(observed[j])).sum())/(reps+1)),
      "four_signal_maxT_familywise_diagnostic_tail_fraction":float(
          (1+(maxnull>=abs(observed[j])).sum())/(reps+1))}
     for j in range(z.shape[1])]

def exclude_taxa_and_recalculate(records,banned):
    new=[]
    for r in records:
        b=r["b"].copy();o=r["o"].copy()
        b[list(banned)]=0;o[list(banned)]=0
        n=b+o
        if (n>0).sum()<2 or b.sum()<=0 or o.sum()<=0:continue
        p=b.sum()/n.sum()
        new.append({**r,"b":b,"o":o,"n":n,"N":n.sum(),"p":p,"u":b-n*p})
    return new

def exclusions(records,z,names,mode):
    grouped={g:{i for i,s in enumerate(names) if s.split()[0]==g}
             for g in {s.split()[0] for s in names}} if mode=="genus" else {
             s:{i} for i,s in enumerate(names)}
    output=[]
    for label,excluded in sorted(grouped.items()):
        new=exclude_taxa_and_recalculate(records,excluded)
        if len(new)<10:continue
        q=score_records(z,new)
        output.append({"excluded_"+mode:label,
                       "networks_after_recalculating_network_bee_baseline":len(new),
                       "original_publications":len({v["pub"] for v in new}),
                       "scores_after_exclusion":[float(v) if np.isfinite(v) else None for v in q["score"]],
                       "informative_networks_per_channel":[int(n) for n in q["network_counts"]]})
    return output

def analyze(flora,traits,reps):
    z,names,records,roster=original_frame(flora,traits)
    q=score_records(z,records,details=True)
    bootstrap=bootstrap_studies(q)
    permutation=permute_source_taxon_vectors(z,records,reps=reps)
    channels=[]
    for j,(label,col) in enumerate(TARGETS.items()):
        channels.append({"channel":label,"original_source_receptor_trait_column":col,
          "taxon_standardization":"z_across_28_source_species" if j<3 else "binary_descriptive_only",
          "local_null_score_U_over_I_NOT_a_fitted_bee_response_beta":float(q["score"][j]),
          "source_bee_informative_networks":int(q["network_counts"][j]),
          **bootstrap[j],**permutation[j]})
    return {"schema":"stage83_source_honeybee_D65_far_near_28_taxa_vs_original_EuPP_bee_networks",
        "original_source_receipt":{"stage81d_apis_artifact_id":ORIGINAL_RECEPTOR_ARTIFACT_ID,
             "stage81d_apis_artifact_zip_sha256":ORIGINAL_RECEPTOR_CI_ZIP_SHA,
             "original_eupp_source_sha256":ORIGINAL_EUPP_SHA,
             "published_Ohashi_219_not_reclassified_using_28_source_subset":True,
             "honeybee_D65_pavo_signal_is_not_Bombus_local_vision":True,
             "Japan_spectra_not_same_European_field_flower_or_year":True},
        "original_source_support":roster,
        "trait_visual_metrics_source_species":28,
        "model_detected_age_chromatic_shift_species_of_28":5,
        "model_far_maintained_near_reduced_species_of_28":12,
        "channels":channels,
        "source_plant_genus_leave_out_recalculating_entire_network":exclusions(records,z,names,"genus"),
        "source_plant_species_leave_out_recalculating_entire_network":exclusions(records,z,names,"species"),
        "scientific_stop_gates":{
            "taxon_exchangeability_ignores_phylogenetic_nonindependence":True,
            "source_study_cluster_intervals_not_taxon_level_intervals":True,
            "no_study_time_flower_age_or_cue_access_sequence_measured":True,
            "no_actual_strong_gust_scent_plume_learning_landing_mediation":True,
            "low_near_green_discordance_not_a_verified_functional_UV_guide":True,
            "no_cross_species_causal_preference_or_selection_claim":True}}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-eupp",type=Path,required=True)
    p.add_argument("--stage81d-receptor-zip",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--permutations",type=int,default=9999)
    a=p.parse_args()
    out=analyze(source_eupp(a.original_eupp),source_receptor(a.stage81d_receptor_zip),a.permutations)
    a.outdir.mkdir(parents=True,exist_ok=True)
    (a.outdir/"stage83_original_true_apis_receptor_source_4signal_28taxon_194network.json").write_text(
      json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE83_28_ORIGINAL_APIS_BEE_RECEPTOR_MACRO_TAXON_FALSIFICATION",json.dumps(
      {"support":out["original_source_support"],
       "channels":[{"name":v["channel"],
         "score":v["local_null_score_U_over_I_NOT_a_fitted_bee_response_beta"],
         "interval":v["publication_cluster_bootstrap_95_descriptive"],
         "taxon_permutation_tail":v["species_vector_permutation_two_sided_tail_fraction"],
         "maxT_diagnostic":v["four_signal_maxT_familywise_diagnostic_tail_fraction"],
         "effective_publications":v["publication_info_effective_n"]} for v in out["channels"]]},sort_keys=True))
if __name__=="__main__":main()
