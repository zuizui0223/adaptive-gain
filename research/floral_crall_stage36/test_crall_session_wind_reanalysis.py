"""Stage36: source-free mathematical checks, never fictional raw bees as empirical."""
from __future__ import annotations
import io
import math
import unittest
import zipfile

from crall_session_wind_reanalysis import (
 _rows,extract_source_tables,prepare_sessions,slope_site_demeaned,
 slope_between_site_means,slope_partial_turbulence,slope_site_and_date_fixed_effects,cluster_bootstrap_sites,
 permutation_within_sites,analyze_original_archive
)


def mock_rows():
    # A's sessions have lower WIND but larger count than B:
    # between-site gradient negative, within-site gradient positive.
    d=[]
    for site,offset,n in (("MOCK_A",0.1,12),("MOCK_B",0.8,3),("MOCK_C",1.3,1)):
        for i in range(5):
            count=n+i
            d.append({
              "site":site,"date":f"2099-01-{i+1:02d}",
              "scent":"MOCK_PERFUME",
              "wind.mean":str(offset+0.04*i),
              "rel.wind.KE":str(.001*(i%2)),
              "count":str(count)
            })
    return d


def faux_zip():
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("Zenodo/collectionMetadata.csv",
                   ',site,date,start.time,scent,count,wind.mean,rel.wind.KE\n'
                   + '\n'.join(
                      f'{i},{r["site"]},{r["date"]},07:00,{r["scent"]},'
                      f'{r["count"]},{r["wind.mean"]},{r["rel.wind.KE"]}'
                      for i,r in enumerate(mock_rows(),1))+'\n')
        z.writestr("Zenodo/integratedSpatialWindData.csv",
                   ',site,wind.mean,count,keep\n1,MOCK_A,0.1,12,TRUE\n')
        z.writestr("Zenodo/beedata.csv",
                   'number,date,site,time,scent,genus,species\n'
                   '1,2099-01-01,MOCK_A,07:00,MOCK,Euglossa,mock_bee\n')
        z.writestr("Zenodo/GenerateFiguresAndAnalyses_CrallEtAl_OrchidBeeWindEcology.R",
                   'model<-glmer(count ~ wind.mean+(1|site))\n')
    return stream.getvalue()


class Stage36CrallTests(unittest.TestCase):
    def test_original_R_row_index_not_an_eco_variable(self):
        rows=_rows(b',site,count\n1,MOCK_A,2\n2,MOCK_B,3\n')
        self.assertEqual(rows[0]["_original_R_row_index"],"1")
        self.assertEqual(rows[1]["count"],"3")
        self.assertEqual(len(rows),2)

    def test_legacy_latin1_notes_do_not_change_original_numeric_fields(self):
        rows=_rows("site,note,count\nMOCK_SITE,café,3\n".encode("latin-1"))
        self.assertEqual(rows[0]["note"],"café")
        self.assertEqual(rows[0]["count"],"3")

    def test_fake_zip_extracts_input_tables_no_real_claim(self):
        x=extract_source_tables(faux_zip())
        self.assertEqual(len(x["sessions"]),15)
        self.assertEqual(len(x["integrated"]),1)
        self.assertEqual(len(x["bees"]),1)
        self.assertTrue(x["original_R_full_content_not_redistributed"])
        self.assertTrue(x["original_R_model_tokens_detected"][r"glmer\s*\("])

    def test_separate_within_positive_between_negative(self):
        rows,_=prepare_sessions(mock_rows(),require_70=False)
        within=slope_site_demeaned(rows)
        between=slope_between_site_means(rows)
        self.assertGreater(within["slope_for_0p1_m_s"],0)
        self.assertLess(between["between_site_pearson_r"],0)
        self.assertEqual(within["original_distinct_sites"],3)

    def test_turbulence_adjusted_sensitivity(self):
        rows,_=prepare_sessions(mock_rows(),require_70=False)
        s=slope_partial_turbulence(rows)
        self.assertEqual(s["status"],"WITHIN_SITE_LOG1P_SLOPE_CONTROLLING_TURBULENCE")
        self.assertGreater(s["wind_beta_per_0p1_m_s"],0)
        self.assertEqual(s["n_source_sessions"],15)

    def test_two_way_site_date_FE_detects_collinear_wind(self):
        rows,_=prepare_sessions(mock_rows(),require_70=False)
        x=slope_site_and_date_fixed_effects(rows)
        self.assertEqual(x['status'],'NO_GO_WIND_COLLINEAR_WITH_SITE_AND_DATE')
        self.assertEqual(x['date_groups'],5)

    def test_two_way_site_date_FE_can_identify_site_by_date_wind_variation(self):
        arr=mock_rows()
        # Add a within-site-by-date wind perturbation not explained
        # by additive site and date intercepts.
        arr[0]['wind.mean']='0.21'
        rows,_=prepare_sessions(arr,require_70=False)
        x=slope_site_and_date_fixed_effects(rows)
        self.assertEqual(x['status'],'SITE_AND_DATE_FIXED_EFFECT_LOG1P_ASSOCIATION')
        self.assertEqual(x['n_sessions'],15)
        self.assertTrue(math.isfinite(x['slope_per_0p1_m_s']))
        self.assertTrue(x['not_causal'])

    def test_repeatability_of_site_cluster_resampling(self):
        rows,_=prepare_sessions(mock_rows(),require_70=False)
        a=cluster_bootstrap_sites(rows,100,seed=2222)
        b=cluster_bootstrap_sites(rows,100,seed=2222)
        self.assertEqual(a,b)
        self.assertEqual(a["bootstrap_site_count"],3)
        self.assertTrue(a["not_an_assigned_wind_causal_CI"])

    def test_site_permutation_preserves_original_site_groups(self):
        rows,_=prepare_sessions(mock_rows(),require_70=False)
        p=permutation_within_sites(rows,100,seed=2222)
        self.assertGreaterEqual(p["two_sided_permutation_fraction"],0)
        self.assertLessEqual(p["two_sided_permutation_fraction"],1)
        self.assertTrue(p["assumption_of_exchangeable_wind_within_site_unverified"])

    def test_no_pseudoreplication_of_beedata_rows(self):
        rows,_=prepare_sessions(mock_rows(),require_70=False)
        slope=slope_site_demeaned(rows)
        self.assertEqual(slope["raw_source_session_rows_used"],15)
        self.assertTrue(slope["log1p_count_NOT_original_Poisson_effect"])

    def test_invalid_original_metadata_missingness_fails(self):
        missing=mock_rows()
        missing[0]["wind.mean"]=""
        rows,skipped=prepare_sessions(missing,require_70=False)
        self.assertEqual(len(rows),14)
        self.assertEqual(skipped["missing_wind_or_count"],1)
        corrupted=mock_rows()
        corrupted[0]["count"]="-1"
        with self.assertRaisesRegex(ValueError,"NEGATIVE_COUNT_OR_WIND"):
            prepare_sessions(corrupted,require_70=False)

    def test_not_declare_an_unverified_70_row_source(self):
        with self.assertRaisesRegex(ValueError,"ORIGINAL_SESSION_GRAIN"):
            prepare_sessions(mock_rows(),require_70=True)

    def test_author_zip_needs_all_files(self):
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,"w") as z:
            z.writestr("Zenodo/collectionMetadata.csv","site,count\nMOCK,1\n")
        with self.assertRaisesRegex(ValueError,"MISSING_AUTHOR_INPUTS"):
            extract_source_tables(stream.getvalue())


if __name__=="__main__":
    unittest.main()
