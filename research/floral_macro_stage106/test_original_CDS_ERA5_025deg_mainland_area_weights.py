"""Stage106 official CDS daily 10fg strict-gust and mainland area-weighting guards."""
import unittest,tempfile,zipfile
from pathlib import Path
import numpy as np
from shapely.geometry import box
from original_CDS_ERA5_025deg_mainland_area_weights import (
    cds_daily_request,gridcell_land_area_weights,index_grid_for_source_bbox,
    gridded_warmmonth_gust_climatology,source_mainland_registry
)

def source_times():
    return np.arange(np.datetime64("1991-01-01"),
                     np.datetime64("2021-01-01"),dtype="datetime64[D]")

def synthetic(warmmonths=(6,7)):
    d=source_times()
    months=d.astype("datetime64[M]").astype(int)%12+1
    warm=np.isin(months,warmmonths)
    n=len(d)
    G=np.zeros((n,1,2),float)+12
    T=np.zeros((n,1,2),float)+273.15
    T[warm,:,:]=273.15+10.
    G[warm,0,0]=16.
    G[warm,0,1]=15.
    return d,G,T,np.array([[2.,1.]])

class OriginalCDSGridSource(unittest.TestCase):
    def test_exact_CDS_variable_separate_max_gust_mean_T(self):
        req=cds_daily_request("10m_wind_gust_since_previous_post_processing",
             "daily_max",1991,1,[42.5,-72,40,-70])
        self.assertEqual(req["frequency"],"1_hourly")
        self.assertEqual(req["daily_statistic"],"daily_max")
        self.assertEqual(req["time_zone"],"utc+00:00")
        self.assertEqual(len(req["day"]),31)
        temp=cds_daily_request("2m_temperature","daily_mean",1991,2,[42.5,-72,40,-70])
        self.assertEqual(temp["daily_statistic"],"daily_mean")
        self.assertEqual(len(temp["day"]),28)
    def test_not_allow_ERA5_gust_max_called_mean_wind(self):
        with self.assertRaises(ValueError):
            cds_daily_request("10m_wind_gust_since_previous_post_processing","daily_mean",1991,1,[42.5,-72,40,-70])
        with self.assertRaises(ValueError):
            cds_daily_request("10m_u_component_of_wind","daily_max",1991,1,[42.5,-72,40,-70])
    def test_not_allow_other_climate_period(self):
        with self.assertRaises(ValueError):
            cds_daily_request("2m_temperature","daily_mean",2021,1,[42,-72,40,-70])
    def test_known_real_ERA5_30yr_days(self):
        self.assertEqual(len(source_times()),10958)
    def test_strict_15_gt_not_gte_and_area_weights(self):
        d,g,t,w=synthetic()
        ans=gridded_warmmonth_gust_climatology(d,g,t,w)
        # First cell above15 for all climatologically warm days, second
        # exactly15 and therefore counts NONE. Weighted area 2:1.
        self.assertAlmostEqual(ans["source_1991_2020_strict_10m_daily_gust_gt_15_fraction_area_weighted"],2/3)
        self.assertEqual(ans["source_cellcount_with_warm_months_and_valid_weather"],2)
        self.assertTrue(ans["source_ERA5_hourly_daily_max_gust_gt_15_strict"])
    def test_climate_temps_exact_5C_not_eligible(self):
        d,g,t,w=synthetic()
        t[:,:,:]=278.15
        ans=gridded_warmmonth_gust_climatology(d,g,t,w)
        self.assertIsNone(ans["source_1991_2020_strict_10m_daily_gust_gt_15_fraction_area_weighted"])
        self.assertEqual(ans["source_flowering_month_eligible_area_fraction"],0)
    def test_missing_day_must_fail(self):
        d,g,t,w=synthetic()
        with self.assertRaises(ValueError):
            gridded_warmmonth_gust_climatology(d[:-1],g[:-1],t[:-1],w)
    def test_unknown_source_units_fail(self):
        d,g,t,w=synthetic()
        with self.assertRaises(ValueError):
            gridded_warmmonth_gust_climatology(d,g,t,w,gust_units="km/h")
        with self.assertRaises(ValueError):
            gridded_warmmonth_gust_climatology(d,g,t,w,temperature_units="C")
    def test_missing_weather_over_5pct_land_area_fails_not_imputed(self):
        d,g,t,w=synthetic()
        g[20,0,0]=np.nan
        with self.assertRaises(ValueError):
            gridded_warmmonth_gust_climatology(d,g,t,w)
    def test_geodesic_grid_cell_fractional_land_area(self):
        region=box(0,0,1,1)
        weights=gridcell_land_area_weights(region,
            np.array([.25,.75]),np.array([.25,.75]),res=.5)
        self.assertEqual(weights.shape,(2,2))
        self.assertTrue(np.all(weights>0))
        self.assertGreater(weights.sum(),12000)
        self.assertLess(weights.sum(),13000)
        self.assertLess(abs(weights[0,0]-weights[0,1]),.02)
    def test_partial_cell_land_edge_weight_zero_outside(self):
        region=box(0,0,.5,.5)
        w=gridcell_land_area_weights(region,
            np.array([.25,.75]),np.array([.25,.75]),res=.5)
        self.assertGreater(w[0,0],0)
        self.assertEqual(w[1,1],0.)
    def test_bad_grid_spacing_or_dateline_refused(self):
        with self.assertRaises(ValueError):
            gridcell_land_area_weights(box(0,0,1,1),np.array([0,.4]),np.array([0,.25]))
        with self.assertRaises(ValueError):
            index_grid_for_source_bbox(box(179.5,20,180,21))
    def test_forged_original_land_registry_checksum_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake","test")
            with self.assertRaises(ValueError):
                source_mainland_registry(p)

if __name__=="__main__":unittest.main()
