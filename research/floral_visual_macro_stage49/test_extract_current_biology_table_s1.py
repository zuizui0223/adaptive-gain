"""Offline tests for PDF Table S1 text-to-record conversion."""
import unittest
from extract_current_biology_table_s1 import (
    parse_table_s1_text,evaluate,_record
)

AUSTRALIA=["Australia","Dilleniaceae","Hibbertia","cuneiformis",
    "E","p","o","11","-0.341","0.280","0.209","1947","1993","46"]
AMERICA=["N. America","Zygophyllaceae","Tribulus","cistoides",
    "E","p","o","19","0.328","-0.059","0.207","1954","1993","39"]

class OriginalS1StrictRows(unittest.TestCase):
    def test_continent_taxon_source_row_parses_without_guide_imputation(self):
        row=_record(AUSTRALIA)
        self.assertEqual(row["taxon_binomial_as_published"],"Hibbertia cuneiformis")
        self.assertEqual(row["original_herbarium_samples"],11)
        self.assertEqual(row["uv_nectar_guide_presence"],
                         "NOT_MEASURED_OR_NOT_REPORTED_IN_S1")
        self.assertEqual(row["standardized_UVP_slope_per_year"],-.341)

    def test_original_header_footer_not_reinterpreted_as_species(self):
        start="Continent\nFamily\nGenus\nSpecies\nYear\nRange\n"
        end="\nTable S1: Taxa included in study testing for temporal\n"
        d=parse_table_s1_text({
          13:start+"\n".join(AUSTRALIA)+"\n",
          14:"\n".join(AMERICA)+end
        })
        self.assertEqual(len(d),2)
        self.assertEqual(evaluate(d)["source_herbarium_samples_sum"],30)

    def test_anther_shape_invalid_in_original_data_is_no_go(self):
        b=list(AUSTRALIA)
        b[4]="U"
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_PUBLISHED_EXPOSURE"):
            _record(b)

    def test_wrong_source_row_length_hard_stop(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_S1_ROW_ARITY"):
            _record(AUSTRALIA[:13])

    def test_unknown_pdf_extra_line_hard_stop(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_S1_TABLE_LINES_NOT_MULTIPLE"):
            parse_table_s1_text({
                13:"Year\nRange\n"+"not a row\n",
                14:"\n".join(AMERICA)+"\nTable S1: Taxa included\n",
            })

if __name__=="__main__":
    unittest.main()
