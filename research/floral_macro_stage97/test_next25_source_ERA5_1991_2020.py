"""Stage97 original second-25 mainland weather-source boundary tests."""
from __future__ import annotations
import unittest,zipfile,tempfile
from pathlib import Path
from next25_source_ERA5_1991_2020 import next25,verified_prior25,START,COUNT

def sample():
    return [
       {"TDWG_L3":f"R{i:03d}",
        "spatial_block_id":f"B{i//5:02d}",
        "shared_split":"holdout" if i%4==0 else "exploration",
        "regional_strict_continent_connected_scope":"mainland",
        "lon":float(i),"lat":35.0,
        "TDWG_source_polygon_SHA256":"a"*64}
       for i in range(125)]

class Stage97Boundary(unittest.TestCase):
    def test_next25_is_exact_unopened_source_range(self):
        full=sample()
        chosen=next25(full,[x["TDWG_L3"] for x in full[:25]])
        self.assertEqual(len(chosen),25)
        self.assertEqual(chosen[0]["TDWG_L3"],"R025")
        self.assertEqual(chosen[-1]["TDWG_L3"],"R049")
        self.assertEqual({x["TDWG_L3"] for x in chosen}&
             {x["TDWG_L3"] for x in full[:25]},set())
        self.assertEqual(START,25);self.assertEqual(COUNT,25)
    def test_previous25_overlap_fails_closed(self):
        full=sample()
        with self.assertRaises(ValueError):
            next25(full,[full[25]["TDWG_L3"]])
    def test_nonmainland_in_second_batch_rejected(self):
        full=sample()
        full[26]["regional_strict_continent_connected_scope"]="mixed"
        with self.assertRaises(ValueError):
            next25(full,[])
    def test_bad_source_universe_cannot_pass(self):
        full=sample()[:124]
        with self.assertRaises(ValueError):
            next25(full,[])
    def test_unfrozen_geographic_partition_fails_closed(self):
        full=sample();full[35]["shared_split"]="some-new-arm"
        with self.assertRaises(ValueError):
            next25(full,[])
    def test_prior_source_zip_requires_actual_sha_not_plausible_fixture(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"previous.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("stage95C_true_source_first25_mainland_site_gust_30yr.json","{}")
            with self.assertRaisesRegex(ValueError,"SOURCE_ARTIFACT_SHA_DRIFT"):
                verified_prior25(p,sample())

if __name__=="__main__":unittest.main()
