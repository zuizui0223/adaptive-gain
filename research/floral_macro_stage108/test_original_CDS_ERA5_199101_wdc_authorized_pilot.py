"""Stage108 source-free CDS original 1991-01 NetCDF scientific integrity tests."""
from __future__ import annotations
import io,json,os,tempfile,unittest,zipfile,hashlib
from pathlib import Path
from unittest.mock import patch
import numpy as np
import xarray as xr
import original_CDS_ERA5_199101_wdc_authorized_pilot as m

def fixture_zip(kind="gust",unit=None,wrong_days=False,drop_wdc_cell=False,with_missing=False):
    times=np.arange(np.datetime64("1991-01-01"),
                    np.datetime64("1991-02-01"),dtype="datetime64[D]")
    if wrong_days:times=times[:-1]
    lat=np.array([39.00,38.75],float)
    lon=np.array([-77.0],float)
    n=len(times)
    if kind=="gust":
        vals=np.zeros((n,2,1))+16.
        vals[:,1,0]=15.
        variable="fg10"
        unit=unit or "m s**-1"
    else:
        vals=np.zeros((n,2,1))+273.15+8.
        variable="t2m"
        unit=unit or "K"
    if with_missing:vals[0,0,0]=np.nan
    if drop_wdc_cell:lat=np.array([39.0],float);vals=vals[:,:1,:]
    ds=xr.Dataset({
       variable:xr.DataArray(vals,dims=("time","latitude","longitude"),
          attrs={"units":unit,"long_name":(
             "10 metre wind gust since previous post-processing" if kind=="gust"
             else "2m temperature")})},
       coords={"time":times,"latitude":lat,"longitude":lon})
    raw=ds.to_netcdf(engine="scipy")
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("orig_cds_source.nc",raw)
    return buf.getvalue()

def source_stage106_fake(tmp):
    d={
     "CDS_official_dataset":m.CDS_DATASET,
     "CDS_original_API_source_request_submitted":False,
     "source_global_125_region_climatology_NOT_obtained":True,
     "source_month_1991_01_CDS_request_specs_NOT_submitted":[]}
    import csv
    rows=[]
    for la,km2 in ((38.75,41.6868537),(39.,142.95504263)):
        rows.append({"TDWG_L3":"WDC",
             "ERA5_atmosphere_source_grid_latitude":str(la),
             "ERA5_atmosphere_source_grid_longitude":"-77.0",
             "source_intersected_original_mainland_land_km2":str(km2)})
    for variable,stat in m.TYPES.values():
        req={"product_type":"reanalysis","frequency":"1_hourly",
            "time_zone":"utc+00:00","year":"1991","month":["01"],
            "day":[f"{x:02d}" for x in range(1,32)],
            "variable":[variable],"daily_statistic":stat}
        d["source_month_1991_01_CDS_request_specs_NOT_submitted"].append({
            "TDWG_L3":"WDC","variable_source":variable,"statistic":stat,
            "one_month_source_probe_request_NOT_SUBMITTED":req})
    p=Path(tmp)/"source.zip"
    with zipfile.ZipFile(p,"w") as z:
        out=io.StringIO();writer=csv.DictWriter(out,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
        z.writestr(m.SOURCE_GRID_MEMBER,out.getvalue())
        z.writestr(m.SOURCE_REQUESTS,json.dumps(d))
    return p,hashlib.sha256(p.read_bytes()).hexdigest()

WEIGHTS={(39.,-77.):142.95504263,(38.75,-77.):41.6868537}

class OriginalCDSPhysicalProof(unittest.TestCase):
    def test_official_variables_independent_aggregation(self):
        self.assertEqual(m.TYPES["gust"][1],"daily_max")
        self.assertEqual(m.TYPES["temperature"][1],"daily_mean")
        self.assertEqual(m.CDS_DATASET,"derived-era5-single-levels-daily-statistics")
        self.assertEqual(m.CDS_URL,"https://cds.climate.copernicus.eu/api")
    def test_actual_netcdf_synthetic_gust_and_temp_valid(self):
        g,meta_g=m.inspect_original_cds_netcdf_bytes(fixture_zip("gust"),"gust",WEIGHTS)
        t,meta_t=m.inspect_original_cds_netcdf_bytes(fixture_zip("temperature"),"temperature",WEIGHTS)
        self.assertEqual(len(g),2)
        self.assertEqual(meta_g["source_native_units"],"m s**-1")
        self.assertEqual(meta_t["source_native_units"],"K")
        summary=m.validate_199101_original_small_pilot(g,t,WEIGHTS)
        expected=142.95504263/(142.95504263+41.6868537)
        self.assertAlmostEqual(summary["source_original_region_CDS_area_weighted_Jan_only_gust15_fraction"],expected)
        self.assertTrue(summary["source_NOT_1991_2020_flowering_month_gust_climatology"])
    def test_strict_gust_above15_not_equal15(self):
        g,_=m.inspect_original_cds_netcdf_bytes(fixture_zip("gust"),"gust",WEIGHTS)
        t,_=m.inspect_original_cds_netcdf_bytes(fixture_zip("temperature"),"temperature",WEIGHTS)
        summary=m.validate_199101_original_small_pilot(g,t,WEIGHTS)
        self.assertEqual([r["original_1991_Jan_daily_max_10fg_above_15_days"] for r in summary["source_two_original_mainland_cell_monthly_summaries"]],[0,31])
    def test_nonoriginal_30_day_source_rejected(self):
        with self.assertRaisesRegex(ValueError,"31_DAILY"):
            m.inspect_original_cds_netcdf_bytes(fixture_zip("gust",wrong_days=True),"gust",WEIGHTS)
    def test_nonoriginal_unit_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"SOURCE_UNIT"):
            m.inspect_original_cds_netcdf_bytes(fixture_zip("gust",unit="km/h"),"gust",WEIGHTS)
        with self.assertRaisesRegex(ValueError,"SOURCE_UNIT"):
            m.inspect_original_cds_netcdf_bytes(fixture_zip("temperature",unit="°C"),"temperature",WEIGHTS)
    def test_absent_true_mainland_area_cell_fails(self):
        with self.assertRaisesRegex(ValueError,"025_CELL_MISSING"):
            m.inspect_original_cds_netcdf_bytes(fixture_zip("gust",drop_wdc_cell=True),"gust",WEIGHTS)
    def test_missing_mainland_cell_day_fails(self):
        with self.assertRaisesRegex(ValueError,"MISSING_CLIMATE"):
            m.inspect_original_cds_netcdf_bytes(fixture_zip("gust",with_missing=True),"gust",WEIGHTS)
    def test_nonzip_unverified_source_fails(self):
        with self.assertRaisesRegex(ValueError,"NETCDF_IN_ZIP"):
            m.inspect_original_cds_netcdf_bytes(b"not zip","gust",WEIGHTS)
    def test_original_stage106_artifact_sha_required(self):
        with tempfile.TemporaryDirectory() as d:
            p,sha=source_stage106_fake(d)
            with self.assertRaisesRegex(ValueError,"AREA_SOURCE_SHA_DRIFT"):
                m.exact_stage106_source(p)
            with patch.object(m,"SOURCE_STAGE106_SHA",sha):
                weights,req=m.exact_stage106_source(p)
                self.assertEqual(set(req),{"gust","temperature"})
                self.assertEqual(len(weights),2)
    def test_no_user_token_does_not_submit_or_claim_source(self):
        with tempfile.TemporaryDirectory() as d:
            p,sha=source_stage106_fake(d)
            with patch.object(m,"SOURCE_STAGE106_SHA",sha):
                with patch.dict(os.environ,{"CDSAPI_KEY":""}):
                    rec=m.run(p,Path(d)/"result",enable_retrieve=True)
            self.assertFalse(rec["actual_official_CDS_download_successful"])
            self.assertEqual(rec["status"],"BLOCKED_NO_EXISTING_CDS_PERSONAL_ACCESS_TOKEN")
            self.assertFalse(rec["original_CDS_dataset_licence_acceptance_checked_by_account"])
    def test_not_asked_to_retrieve_never_contacts_CDS(self):
        with tempfile.TemporaryDirectory() as d:
            p,sha=source_stage106_fake(d)
            with patch.object(m,"SOURCE_STAGE106_SHA",sha):
                with patch.dict(os.environ,{"CDSAPI_KEY":"unverified-test-placeholder"}):
                    rec=m.run(p,Path(d)/"result",enable_retrieve=False)
            self.assertEqual(rec["status"],"SOURCE_CONTRACT_ONLY_NO_REQUEST_SENT")
    def test_safe_auth_failure_category_no_secret(self):
        self.assertEqual(m.category_from_CDS_exception(Exception("403 not accepted licence")),
                         "DATASET_TERMS_NOT_YET_ACCEPTED_OR_LICENCE_REJECTED")
        self.assertEqual(m.category_from_CDS_exception(Exception("429 too many requests")),
                         "CDS_PROVIDER_QUOTA_OR_QUEUE")
        self.assertEqual(m.category_from_CDS_exception(Exception("timeout ssl")),
                         "CDS_TRANSPORT_FAILURE")
if __name__=="__main__":unittest.main()
