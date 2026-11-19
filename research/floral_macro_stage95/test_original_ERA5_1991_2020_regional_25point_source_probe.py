"""Stage95C original time-series source: regional expansion is source-only."""
import csv,hashlib,io,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
from shapely.geometry import box
import original_ERA5_1991_2020_regional_25point_source_probe as m
class RegionSource25Tests(unittest.TestCase):
    def test_25_source_regions_in_five_requests(self):
        self.assertEqual(m.FIRST_SOURCE_REGIONS,25)
        self.assertEqual(m.SITES_PER_REQUEST,5)
    def test_corrupt_source_region_artifact_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake","no")
            with self.assertRaises(ValueError):m.source_mainland_regions(p,p)
    def test_global_mainland125_split_88_37_invariant(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"synthetic.zip"
            rows=[]
            for i in range(125):
                rows.append({"TDWG_L3":f"T{i:03d}",
                    "shared_split":"exploration" if i<88 else "holdout",
                    "spatial_block_id":str(i//5),
                    "polygon_sha256":"a"*64})
            text=io.StringIO()
            wr=csv.DictWriter(text,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
            with zipfile.ZipFile(p,"w") as z:z.writestr(m.STAGE94_CSV_MEMBER,text.getvalue())
            from types import SimpleNamespace
            polygons={r["TDWG_L3"]:box(30+i,40,30.2+i,40.2) for i,r in enumerate(rows)}
            with patch.object(m,"STAGE94_ARTIFACT_SHA",m.sha256(p)):
                with patch.object(m,"source_polygons",return_value=(polygons,set(),{})):
                    regions=m.source_mainland_regions(p,p)
            self.assertEqual(len(regions),125)
            self.assertEqual(regions[0]["TDWG_L3"],"T000")
            self.assertEqual(regions[87]["shared_split"],"exploration")
            self.assertEqual(regions[88]["shared_split"],"holdout")
    def test_outcome_not_in_geo_source_selector(self):
        import inspect
        s=inspect.getsource(m.source_mainland_regions)
        self.assertNotIn("fragrance",s)
        self.assertNotIn("Bombus",s)
        self.assertNotIn("hue_",s)
    def test_five_multiple_required(self):
        with self.assertRaises(ValueError):
            m.run(Path("dummy"),Path("dummy"),Path("dummy"),max_sites=3)
if __name__=="__main__":unittest.main()
