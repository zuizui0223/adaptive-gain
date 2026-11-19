"""Fail closed on any unaudited/mixed/island TDWG3 mainland split."""
import unittest
from freeze_mainland_region_frame import split_regions

D="a"*64
def audit():
    return [
       {"TDWG_L3":f"R{i}", "land_scope":"mainland" if i<5 else "island",
        "spatial_block_id":f"block{i}" if i<5 else "island0",
        "polygon_sha256":D,"geometry_source":"source polygon validated"}
       for i in range(6)]

class MainlandSplit(unittest.TestCase):
    def test_shared_blocks_and_no_islands(self):
        frame,receipt=split_regions([f"R{i}" for i in range(6)],audit())
        self.assertEqual(len(frame),5)
        self.assertEqual({x["land_scope"] for x in frame},{"mainland"})
        self.assertEqual({x["shared_split"] for x in frame},{"exploration","holdout"})
        self.assertEqual(receipt["island_regions_excluded"],1)
        self.assertFalse(receipt["wind_or_cue_values_used_to_define_split"])
        self.assertFalse(receipt["spatial_separation_buffer_verified"])
    def test_same_assignment_independent_of_input_order(self):
        f,_=split_regions([f"R{i}" for i in range(6)],audit())
        g,_=split_regions([f"R{i}" for i in reversed(range(6))],list(reversed(audit())))
        self.assertEqual(f,g)
    def test_mixed_regions_are_excluded(self):
        a=audit();a[-1]["land_scope"]="mixed"
        f,r=split_regions([f"R{i}" for i in range(6)],a)
        self.assertEqual(len(f),5)
        self.assertEqual(r["mixed_regions_excluded"],1)
    def test_missing_geometry_fails(self):
        with self.assertRaises(ValueError):
            split_regions([f"R{i}" for i in range(6)],audit()[:-1])
    def test_polygon_sha_not_a_dummy(self):
        a=audit();a[1]["polygon_sha256"]=""
        with self.assertRaises(ValueError):
            split_regions([f"R{i}" for i in range(6)],a)
    def test_no_inference_from_doubtful_land_scope(self):
        a=audit();a[0]["land_scope"]="assumed_mainland"
        with self.assertRaises(ValueError):
            split_regions([f"R{i}" for i in range(6)],a)
    def test_single_effective_block_fails(self):
        a=audit()
        for row in a[:5]: row["spatial_block_id"]="all mainland same"
        with self.assertRaises(ValueError):
            split_regions([f"R{i}" for i in range(6)],a)

if __name__=="__main__":unittest.main()
