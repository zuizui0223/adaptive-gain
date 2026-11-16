"""No displayed synthetic source counts as real predictions."""
import csv
import tempfile
from pathlib import Path
import unittest

from plot_source_filtered_bombus_hex import read_source_rows

class SourceMapGuard(unittest.TestCase):
    def test_missing_global_cells_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/"test.csv"
            path.write_text(
              "longitude,latitude,n_source_tree_and_pa_cutoff_Bombus_taxa\n"
              "0,1,0\n",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"NO_GO_GLOBAL_HEX_SOURCE_MAP_INCOMPLETE"):
                read_source_rows(path)

if __name__=="__main__":
    unittest.main()
