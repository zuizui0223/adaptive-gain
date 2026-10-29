"""Source-index parser controls based on native documented example file names."""
import unittest
from inspect_native_schema import PATTERN

class OriginalFileNameSchemaTests(unittest.TestCase):
    def test_original_source_file_accepted(self):
        name="B01_BC6935_F01_S0_P0_T01_W0_C001H001S0001xyzpts.csv"
        m=PATTERN.fullmatch(name)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("bee"),"01")
        self.assertEqual(m.group("tag"),"6935")
        self.assertEqual(m.group("w"),"0")
        self.assertEqual(m.group("s"),"0")
    def test_malformed_file_rejected(self):
        for name in ("B01_BC6935_F01_S0_P0_T01_W0_xyzpts.csv",
                     "B01_BC6935_F01_S0_P0_T01_W0_C001H001S0001xyzpts.csv.exe",
                     "._B01_BC6935_F01_S0_P0_T01_W0_C001H001S0001xyzpts.csv"):
            self.assertIsNone(PATTERN.fullmatch(name))

if __name__=="__main__":unittest.main()
