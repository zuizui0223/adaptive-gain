"""Stage82: species-level falsification and original-publication weighting.

Digest-locked original 18,798 EuPPollNet source rows and 53 Ohashi
age x flower-part source summaries. Recompute Stage81C's source network scores
(194 networks / 30 real publications), then explicitly inspect repeated
plant-trait pseudoreplication. No confirmed bee behaviour, wind or selection.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np,pandas as pd

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'floral_macro_stage81'))
from source_ohashi_age_shift_vs_real_EuPP_guild import (
    SOURCE_ORIGINAL_EUPP_SHA,SOURCE_OHASHI_DERIVED_28_SHA,
    validated_source_csv,build_taxon_traits,source_network_preguild,
    one_network_score,informative_scores,publication_bootstrap,
)

KEY=('Study_id','Network_id','Year_from_original_date')
NAME='Original_plant_accepted_name_literal'


def score_with_exclusions(matched, exclude_species=None, exclude_genus=None):
    sub=matched
    if exclude_species is not None:sub=sub.loc[sub[NAME]!=exclude_species]
    if exclude_genus is not None:sub=sub.loc[sub.genus!=exclude_genus]
    rows=[]
    for _,g in sub.groupby(list(KEY),sort=True):
        one=one_network_score(g)
        if one:rows.append(one)
    return pd.DataFrame(rows)


def study_equal_weight_and_bootstrap(scores,reps=4000,seed=20261118):
    p=scores.groupby('source_publication',sort=True)[[
      'source_U_local_score','source_I_local_null_fisher_information']].sum().to_numpy()
    if len(p)<10 or (p[:,1]<=0).any():raise ValueError('STAGE82_INSUFFICIENT_SOURCE_PAPERS')
    ratios=p[:,0]/p[:,1]
    rng=np.random.default_rng(seed)
    sampled=rng.integers(0,len(p),size=(reps,len(p)))
    equal=ratios[sampled].mean(axis=1)
    return {'distinct_original_publications':int(len(p)),
       'source_equal_publication_mean_U_over_I':float(ratios.mean()),
       'source_publication_bootstrap_95_interval':[float(x) for x in np.quantile(equal,[.025,.975])],
       'small_publication_information_can_dominate_unweighted_ratio':True}


def permutation_source_trait_labels(eligible,trait,reps=9999,seed=20261118):
    """A descriptive falsification null, NOT phylogeny-preserving exchangeability."""
    names=sorted(trait.source_original_accepted_species)
    n_taxon=len(names)
    index={n:i for i,n in enumerate(names)}
    x=trait.set_index('source_original_accepted_species').loc[names,
      'x_28species_equal_taxon_standardized_log1p_raw_age_RMS'].to_numpy(dtype=float)
    coef=[];denom=[];premult=[];tot=[]
    for _,g in eligible.groupby(list(KEY),sort=True):
        b=g.n_observed_Bombus.to_numpy(dtype=float)
        oth=g.n_observed_other_bee.to_numpy(dtype=float);n=b+oth
        if (n>0).sum()<2 or b.sum()<=0 or oth.sum()<=0:continue
        q=b.sum()/n.sum()
        u=np.zeros(n_taxon);w=np.zeros(n_taxon)
        for species,bb,nn in zip(g[NAME],b,n):
            i=index[species];u[i]+=bb-nn*q;w[i]+=nn
        coef.append(u);denom.append(w);premult.append(q*(1-q));tot.append(n.sum())
    if len(coef)!=194:raise ValueError('STAGE82_REAL_ORIGINAL_NETWORK_194_CHANGED')
    coef=np.asarray(coef);denom=np.asarray(denom);premult=np.asarray(premult)[:,None]
    tot=np.asarray(tot)[:,None]
    rng=np.random.default_rng(seed)
    labels=np.stack([x]+[rng.permutation(x) for _ in range(reps)],axis=1)
    allratios=[];counts=[]
    for start in range(0,reps+1,500):
        v=labels[:,start:start+500]
        u=coef@v;n=denom@v
        info=premult*((denom@(v*v))-n*n/tot)
        good=info>1e-8
        counts.extend(good.sum(axis=0).tolist())
        allratios.extend(((u*good).sum(axis=0)/(info*good).sum(axis=0)).tolist())
    baseline=float(allratios[0]);null=np.array(allratios[1:])
    return {'observed_source_score_U_over_I':baseline,
       'fixed_28_source_taxa':n_taxon,'original_scored_networks':counts[0],
       'source_networks_retained_min_after_shuffling':int(min(counts)),
       'independent_permutations':reps,
       'permutation_95_percentile_interval':[float(v) for v in np.quantile(null,[.025,.975])],
       'two_sided_tail_probability_descriptive':float((1+np.sum(np.abs(null)>=abs(baseline)))/(reps+1)),
       'negative_tail_probability_descriptive':float((1+np.sum(null<=baseline))/(reps+1)),
       'trait_exchangeability_ignores_phylogeny_and_is_only_falsification_diagnostic':True}


def run(flora,ages):
    trait,_=build_taxon_traits(ages)
    matched,eligible=source_network_preguild(flora,trait)
    scores=informative_scores(eligible)
    if len(scores)!=194 or scores.source_publication.nunique()!=30 or scores.Study_id.nunique()!=31:
        raise ValueError('STAGE82_AUTHENTIC_194_30_31_SOURCE_CHANGED')
    score=float(scores.source_U_local_score.sum()/scores.source_I_local_null_fisher_information.sum())
    if abs(score-(-0.9883058722019229))>1e-9:raise ValueError('STAGE82_STAGE81C_SCORE_NOT_REPRODUCED')
    pub=scores.groupby('source_publication').source_I_local_null_fisher_information.sum()
    concentration=pub/pub.sum()
    exclusions={}
    for label,name,genus in [('trifolium_pratense','trifolium pratense',None),
                             ('trifolium_repens','trifolium repens',None),
                             ('trifolium_all',None,'trifolium')]:
        one=score_with_exclusions(matched,name,genus)
        effect=float(one.source_U_local_score.sum()/one.source_I_local_null_fisher_information.sum())
        exclusions[label]={'original_networks':int(len(one)),
          'independent_source_publications':int(one.source_publication.nunique()),
          'local_null_score_ratio':effect,
          'paper_cluster_bootstrap':publication_bootstrap(one,seed=20261118),}
    source_species=matched.merge(scores[list(KEY)],on=list(KEY),validate='many_to_one')[NAME].nunique()
    out={'schema':'stage82_source_age_RMS_guild_dual_independence_audit',
         'source_species_ever_measured':28,
         'source_species_present_in_actual_194_scored_networks':int(source_species),
         'source_measured_early_late_flower_parts':53,
         'original_outcome_blind_2_species_source_networks':537,
         'source_networks_with_two_strict_bee_guilds':194,
         'source_publications':int(len(pub)),
         'source_source_StudyIDs':int(scores.Study_id.nunique()),
         'original_null_score_U_over_I':score,
         'source_study_information_largest_fraction':float(concentration.max()),
         'source_study_information_effective_studies':float(1/(concentration*concentration).sum()),
         'source_publication_sampling':publication_bootstrap(scores,seed=20261118),
         'source_publication_equal_weighting':study_equal_weight_and_bootstrap(scores),
         'source_taxon_exchangeability_diagnostic':permutation_source_trait_labels(eligible,trait),
         'one_source_species_or_genus_removed':exclusions,
         'source_Japan_spectra_Europe_visits_are_not_cotemporal_or_geographically_matched':True,
         'no_measured_floral_aging_at_visits_or_wind_scent_learning_landing':True,
         'no_confirmed_taxon_level_effect_or_wind_reordering':True}
    leave=[]
    for sp in sorted(trait.source_original_accepted_species):
        q=score_with_exclusions(matched,sp)
        leave.append({'excluded_species':sp,'remaining_original_networks':len(q),
                      'remaining_independent_publications':int(q.source_publication.nunique()),
                      'remaining_local_null_score':float(q.source_U_local_score.sum()/q.source_I_local_null_fisher_information.sum())})
    return out,pd.DataFrame(leave)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--original-stage69-flora',type=Path,required=True)
    p.add_argument('--original-stage81b-ages',type=Path,required=True)
    p.add_argument('--outdir',type=Path,required=True)
    args=p.parse_args()
    result,loo=run(validated_source_csv(args.original_stage69_flora,SOURCE_ORIGINAL_EUPP_SHA),
         validated_source_csv(args.original_stage81b_ages,SOURCE_OHASHI_DERIVED_28_SHA))
    args.outdir.mkdir(parents=True,exist_ok=True)
    (args.outdir/'stage82_true_original_taxon_exchangeability_vs_publication_source.json').write_text(
         json.dumps(result,sort_keys=True,indent=2)+'\n')
    loo.to_csv(args.outdir/'stage82_real_28_source_species_leave_out.csv',index=False)
    print('STAGE82_SOURCE_ORIGINAL_PAPER_X_TAXON_CHECK',json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
