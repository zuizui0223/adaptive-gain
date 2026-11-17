"""Mock-only audits for corrected source flower counts and no false exposure rates."""
import csv,gzip,io,importlib.util,unittest
from pathlib import Path
p=Path(__file__).with_name("audit_original_flowers_sampling_exposure.py")
s=importlib.util.spec_from_file_location("stage71_flower",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class Stage71CountSafetyTests(unittest.TestCase):
    def test_pin_original_corrected_and_flower_count_bytes(self):
        self.assertEqual(m.FLOWER_SIZE,20315455)
        self.assertEqual(m.NETWORK_SIZE,2374060)
        self.assertEqual(m.ORIGINAL_VISIT_ROWS,623476)
        self.assertEqual(len(m.FLOWER_GIT_SHA),40)
        self.assertEqual(len(m.NETWORK_GIT_SHA),40)
    def test_missing_source_count_is_not_zero(self):
        for x in ("","NA","nan","not measured","-1"):
            self.assertIsNone(m.numeric(x))
        self.assertEqual(m.numeric("0"),0)
        self.assertEqual(m.numeric("1.5"),1.5)
    def test_flower_count_unsupported_units_not_merged(self):
        self.assertEqual(m.safe_join_key("S1","flower1"),("S1","flower1"))
        self.assertEqual(m.safe_join_key("S1","NA"),None)
        self.assertEqual(m.safe_join_key("NA","x"),None)
        self.assertNotEqual(m.safe_join_key("S1","x"),m.safe_join_key("S2","x"))
    def test_utf8_and_compressed_csv_preserve_source_row_structure(self):
        b=io.StringIO(newline="")
        w=csv.DictWriter(b,fieldnames=["Study_id","Flower_data_merger","Flower_count","Units"])
        w.writeheader();w.writerow({"Study_id":"X","Flower_data_merger":"foo","Flower_count":"2","Units":"flowers"})
        z=list(m.rows(gzip.compress(b.getvalue().encode()),compressed=True))
        self.assertEqual(len(z),1)
        self.assertEqual(z[0][1]["Flower_count"],"2")
        self.assertEqual(z[0][1]["Units"],"flowers")
    def test_wrong_source_download_rejected_before_network_call(self):
        with self.assertRaisesRegex(ValueError,"UNREGISTERED"):
            m.fetch("flower-photo.csv")

if __name__=="__main__":unittest.main()
