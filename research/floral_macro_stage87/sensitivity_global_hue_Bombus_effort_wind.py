"""Stage87F: source-authenticated independent GBIF recording-effort restrictions.

Source source regional 274/139 split, 11 original lexical hue categories with
both species pooling and genus-balanced composition. No regions missing
Bombus GBIF observations are assigned a true zero. An observed species
supported by 2 cells and <=10km coordinate uncertainty is a stricter
record-backed sensitivity, NOT an independently estimated native richness.

Recompute whole adjusted regional models in frozen source-only subsamples:
base (>=5 source 1-degree cells), >=10 cells, >=20 cells,
>=100 source hue species, and stricter coordinate uncertainty richness.
P-values are exploratory, not statistical replication across family members
or original botanical species. Note predictor standardization is cohort-wise.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests
from analyze_global_hue_wind_bombus_spatial_overlap import (
    source_join,source_design,OUTCOMES,COLORS,PRIMARY,STRICT,CELLS,
)
TERMS=("wind","log_bombus_richness","wind_x_bombus")

def analysis_scenarios(positive):
    cases={
      "base_primary_5_1degree_cells":positive,
      "GBIF_reporting_10_1degree_cells":positive.loc[positive[CELLS]>=10],
      "GBIF_reporting_20_1degree_cells":positive.loc[positive[CELLS]>=20],
      "NHM_source_at_least_100_exclusive_hue_taxa":
          positive.loc[positive.n_source_single_explicit_hue>=100],
      "coordinate_uncertainty_le10km_recorded_richness":positive.copy()
    }
    cases["coordinate_uncertainty_le10km_recorded_richness"]["log_bombus_richness"]=(
       np.log1p(cases["coordinate_uncertainty_le10km_recorded_richness"][STRICT]))
    if len(cases["base_primary_5_1degree_cells"])!=139 or len(cases["GBIF_reporting_10_1degree_cells"])!=109 or len(cases["GBIF_reporting_20_1degree_cells"])!=76 or len(cases["NHM_source_at_least_100_exclusive_hue_taxa"])!=135:
        raise ValueError("STAGE87F_ORIGINAL_EFFORT_AND_SOURCE_FLORA_FRAME_CHANGED")
    if (cases["coordinate_uncertainty_le10km_recorded_richness"][STRICT]<=0).any():
        raise ValueError("STAGE87F_STRICT_SOURCE_OCCURRENCE_QUALITY_NULL_NOT_ACCEPTED")
    return cases

def estimate(positive):
    cases=analysis_scenarios(positive)
    out=[]
    for scope,source in cases.items():
        x=source_design(source,True)
        if np.linalg.matrix_rank(x.to_numpy())!=x.shape[1]:
            raise ValueError("STAGE87F_COHORT_NOT_FULL_RANK_"+scope)
        for trait,hue,level in OUTCOMES:
            vals=np.asarray(source[trait],float)
            if not np.isfinite(vals).all():
                raise ValueError("STAGE87F_SOURCE_HUE_NOT_MEASURED_FOR_INCLUDED_REGION")
            fitted=sm.OLS(vals,x).fit(cov_type="HC3")
            for term in TERMS:
                out.append({"source_sensitivity_cohort":scope,
                  "original_spatial_TDWG3_region_count":len(source),
                  "hue":hue,"aggregation":level,"term":term,
                  "standardized_region_partial_slope_fraction_points":float(fitted.params[term]),
                  "HC3_exploratory_p":float(fitted.pvalues[term]),
                  "model_r2_descriptive":float(fitted.rsquared),
                  "source_Bombus_10km_richness_is_quality_proxy_not_true_absence":True})
    df=pd.DataFrame(out)
    for (_,_,_),ix in df.groupby(["source_sensitivity_cohort","aggregation","term"]).groups.items():
        df.loc[ix,"BH_q_fixed_11_hue_families"]=multipletests(df.loc[ix,"HC3_exploratory_p"],method="fdr_bh")[1]
    if len(df)!=5*22*3:
        raise ValueError("STAGE87F_SOURCE_FIVE_SCENARIOS_22_HUES_AND_THREE_TERMS_MISSING")
    checks=[]
    for hue,level,term in [
      ("yellow","genus_balanced","log_bombus_richness"),
      ("purple","genus_balanced","log_bombus_richness"),
      ("green","genus_balanced","wind"),
      ("brown","genus_balanced","wind"),
      ("white","genus_balanced","wind_x_bombus"),
      ("white","pooled","wind_x_bombus")]:
        m=df.loc[(df.hue==hue)&(df.aggregation==level)&(df.term==term)]
        checks.append({"hue":hue,"aggregation":level,"term":term,
          "source_scenarios_with_same_positive_direction":int((m.standardized_region_partial_slope_fraction_points>0).sum()),
          "source_scenarios_with_same_negative_direction":int((m.standardized_region_partial_slope_fraction_points<0).sum()),
          "scenarios_with_BH_q_lt_0_05":int((m.BH_q_fixed_11_hue_families<.05).sum()),
          "source_cohort_effects":{r.source_sensitivity_cohort:{
            "source_region_count":int(r.original_spatial_TDWG3_region_count),
            "slope_fraction_points":float(r.standardized_region_partial_slope_fraction_points),
            "source_exploratory_BH_q":float(r.BH_q_fixed_11_hue_families)}
            for r in m.itertuples()}})
    receipt={"schema":"stage87F_real_original_GBIF_Bombus_recording_effort_source_hue_spatial_sensitivity",
      "original_source_11_lexical_hue_families":len(COLORS),
      "original_source_5_independent_definition_sensitivities":list(cases),
      "source_geographic_cohort_counts":{k:len(x) for k,x in cases.items()},
      "source_positive_only_recorded_richness_not_native_or_absent":True,
      "source_pollen_transfer_cognition_odor_landing_wind_not_measured":True,
      "source_spatial_phenotype_generalization_not_proven_by_repeated_regional_flora":True,
      "source_plant_phenotypic_pollination_mode_missing_in_botanical_text":True,
      "source_reporting_effort_proxy_not_causal_debiasing":True,
      "contrasts_to_check_not_selected_from_significant_values":checks}
    return df,receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage87C-global-native-climate-zip",type=Path,required=True)
    p.add_argument("--stage87D-original-GBIF-Bombus-zip",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    joined,global_,bee,support=source_join(a.stage87C_global_native_climate_zip,a.stage87D_original_GBIF_Bombus_zip)
    results,receipt=estimate(bee)
    receipt["original_source_region_gates"]=support
    a.outdir.mkdir(parents=True,exist_ok=True)
    results.to_csv(a.outdir/"stage87F_GBIF_Bombus_source_effort_and_flora_hue_source_sensitivity.csv",index=False)
    (a.outdir/"stage87F_original_5_Bombus_effort_sensitivity_source_receipt.json").write_text(
       json.dumps(receipt,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE87F_ORIGINAL_GLOBAL_REGION_BOMBUS_EFFORT_SPATIAL_SENSITIVITY",json.dumps({
       "regions":receipt["source_geographic_cohort_counts"],
       "source_constraints":receipt["contrasts_to_check_not_selected_from_significant_values"]},sort_keys=True))
if __name__=="__main__":main()
