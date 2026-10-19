import unittest
import tempfile
from pathlib import Path
import numpy as np
from temporal import entropy_parts, permutation_null, read_source_csv

class TemporalTests(unittest.TestCase):
    def test_independence(self):
        r=entropy_parts(np.array([[5,5],[5,5]])); self.assertAlmostEqual(r['I'],0);self.assertAlmostEqual(r['Dpool'],2)
    def test_complete_segregation(self):
        r=entropy_parts(np.array([[10,0],[0,10]]));self.assertAlmostEqual(r['I'],np.log(2));self.assertAlmostEqual(r['Dwithin'],1)
    def test_relabeling(self):
        a=np.array([[4,0,3],[0,6,2]]);self.assertAlmostEqual(entropy_parts(a)['I'],entropy_parts(a[::-1,::-1])['I'])
    def test_one_day(self):
        self.assertAlmostEqual(entropy_parts(np.array([[3,5,8]]))['I'],0)
    def test_one_plant(self):
        self.assertAlmostEqual(entropy_parts(np.array([[3],[5],[8]]))['I'],0)
    def test_bad_counts(self):
        for a in (np.array([[1,-1]]),np.array([[1,.5]]),np.zeros((2,2))):
            with self.assertRaises(ValueError): entropy_parts(a)
    def test_seeded_permutation(self):
        a=np.array([[20,0],[0,20]]);x=permutation_null(a,29,2);y=permutation_null(a,29,2)
        np.testing.assert_array_equal(x,y);self.assertLess(x.mean(),entropy_parts(a)['I'])
    def test_local_blocks_preserve_between_block_segregation(self):
        a=np.array([[10,0],[10,0],[0,10],[0,10]])
        z=permutation_null(a,19,8,np.array([0,0,1,1]));np.testing.assert_allclose(z,np.log(2))
    def test_singleton_blocks_are_identical(self):
        a=np.array([[2,3],[8,1]]);z=permutation_null(a,9,8,np.array([0,1]));np.testing.assert_allclose(z,entropy_parts(a)['I'])

    def test_verified_source_text_reading_preserves_legacy_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "legacy.csv"
            source.write_bytes(b"name,value\nT\xccst,3\n")
            data, codec = read_source_csv(source)
            self.assertEqual(codec, "latin-1")
            self.assertEqual(len(data), 1)
            self.assertEqual(data.loc[0, "name"].encode("latin-1"), b"T\xccst")
            self.assertEqual(int(data.loc[0, "value"]), 3)

    def test_verified_source_text_prefers_strict_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "utf8.csv"
            source.write_bytes("name,value\n東京,4\n".encode("utf-8"))
            data, codec = read_source_csv(source)
            self.assertEqual(codec, "utf-8")
            self.assertEqual(data.loc[0, "name"], "東京")

if __name__=='__main__':unittest.main()
