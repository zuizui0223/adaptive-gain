"""Native source archive integrity tests on synthetic only; NOT bee empirical results."""
import io
import hashlib
import unittest
import zipfile
from source_audit import safe_manifest,EXPECTED_MD5,RECORD,FILENAME

class Stage10SourceIntegrityTests(unittest.TestCase):
    @staticmethod
    def sample(name="some_original_test.csv",data=b"time,x,y,z\\n0,0,1,2\\n"):
        mem=io.BytesIO()
        with zipfile.ZipFile(mem,"w",zipfile.ZIP_DEFLATED) as z:
            z.writestr(name,data)
        return mem.getvalue()
    def test_archive_metadata_contract(self):
        self.assertEqual(RECORD,"60234")
        self.assertEqual(len(EXPECTED_MD5),32)
        self.assertIn("ChangCrallCombes",FILENAME)
    def test_bounded_native_header(self):
        got=safe_manifest(self.sample())
        self.assertEqual(len(got),1)
        self.assertEqual(got[0]["prefix_type"],"TEXT")
        self.assertIn("time,x,y,z",got[0]["source_header_excerpt"])
    def test_matlab5_detected(self):
        got=safe_manifest(self.sample(name="raw.mat",data=b"MATLAB 5.0 MAT-file" + b"\\x00"*200))
        self.assertEqual(got[0]["prefix_type"],"MATLAB5")
    def test_bad_zip_fails(self):
        with self.assertRaisesRegex(ValueError,"NOT_ZIP"):
            safe_manifest(b"fake")
    def test_zip_slip_fails(self):
        with self.assertRaisesRegex(ValueError,"UNSAFE"):
            safe_manifest(self.sample(name="../escape.csv"))

if __name__=="__main__":unittest.main()
