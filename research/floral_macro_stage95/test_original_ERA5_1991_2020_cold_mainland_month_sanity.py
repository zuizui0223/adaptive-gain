"""Stage95B tests high-lat source season gate and fake geography rejection."""
import unittest,zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from original_ERA5_1991_2020_cold_mainland_month_sanity import (
    cold_mainland_sites,LAT_GATE_DEG,N_COLD_SITES
)
from original_ERA5_1991_2020_gust_five_mainland_pilot import climatology,date_range

class Stage95B(unittest.TestCase):
    def test_high_latitudes_are_geographic_not_source_climate_selected(self):
        self.assertEqual(N_COLD_SITES,3)
        self.assertEqual(LAT_GATE_DEG,50.0)
    def test_true_cold_climate_excludes_original_calendar_months(self):
        daily=[]
        for d in date_range(1991,2020):
            m=int(d[5:7]);daily.append((d,16.0,10.0 if 5<=m<=9 else -8.0))
        x=climatology(daily)
        self.assertEqual(x["source_eligible_climatological_months_T2m_strict_above_5C"],[5,6,7,8,9])
        self.assertTrue(0<x["source_eligible_days"]<10958)
        self.assertEqual(x["source_primary_fraction_days_daily_gust_strict_above_15_ms"],1.0)
    def test_source_geographical_sha_required(self):
        with TemporaryDirectory() as td:
            p=Path(td)/"dummy.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake","source")
            with self.assertRaises(ValueError):
                cold_mainland_sites(p,p)

if __name__=="__main__":unittest.main()
