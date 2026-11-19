"""Stage98 source-free original TDWG geographic holdout boundary guards."""
from __future__ import annotations
import unittest,tempfile,zipfile
from pathlib import Path
from shapely.geometry import box
from original_TDWG3_shared_holdout_polygon_contact_audit import (
    edge_geodesic_approx_km,diagnose_crossfold_region_boundaries,
    read_locked_mainland_split
)

class OriginalBoundaryGuards(unittest.TestCase):
    def test_exact_shared_border_is_not_spatially_buffered(self):
        a=box(0,0,1,1);b=box(1,0,2,1)
        self.assertAlmostEqual(edge_geodesic_approx_km(a,b),0.0)
        self.assertTrue(a.touches(b))
    def test_exact_overlap_is_contact(self):
        a=box(0,0,2,2);b=box(1,1,3,3)
        self.assertAlmostEqual(edge_geodesic_approx_km(a,b),0)
        self.assertTrue(a.overlaps(b))
    def test_geographic_far_boundary_positive(self):
        self.assertGreater(edge_geodesic_approx_km(box(0,0,1,1),box(4,0,5,1)),200)
    def test_fixed_fold_identity_not_changed(self):
        rows=[
          {"TDWG_L3":"T1","shared_split":"exploration","spatial_block_id":"A"},
          {"TDWG_L3":"T2","shared_split":"exploration","spatial_block_id":"A"},
          {"TDWG_L3":"H1","shared_split":"holdout","spatial_block_id":"B"}]
        polys={"T1":box(0,0,1,1),"T2":box(6,0,7,1),"H1":box(1,0,2,1)}
        result,pairs,summary=diagnose_crossfold_region_boundaries(rows,polys)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]["TDWG_L3"],"H1")
        self.assertTrue(result[0]["source_direct_polygon_contact_or_overlap"])
        self.assertEqual(result[0]["n_source_intersecting_exploration_polygons"],1)
        self.assertEqual(summary["total_train_holdout_region_pairs_evaluated"],2)
        self.assertEqual(summary["holdout_regions_touching_or_intersecting_any_exploration_polygon"],1)
        self.assertEqual(len(pairs),1)
        self.assertEqual(result[0]["full_physical_geodesic_100km_holdout_buffer_certified"],"NO")
    def test_missing_region_geometry_fails(self):
        rows=[{"TDWG_L3":"T1","shared_split":"exploration","spatial_block_id":"A"},
              {"TDWG_L3":"H1","shared_split":"holdout","spatial_block_id":"B"}]
        with self.assertRaises(ValueError):
            diagnose_crossfold_region_boundaries(rows,{"T1":box(0,0,1,1)})
    def test_source_first_requires_frozen_sha(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("stage94_original_mainland_shared_geoblock_split.csv","TDWG_L3\nA\n")
            with self.assertRaisesRegex(ValueError,"SOURCE_ZIP_SHA_CHANGED"):
                read_locked_mainland_split(p)

if __name__=="__main__":unittest.main()
