"""Original 2016 177-taxon table: invented-row contract tests only."""
import unittest
from extract_nph2016_original_uv_177 import parse_source_rows,summarize

def synthetic_page(study_index):
    # Nine fields: taxon code + 8 actual scalar values, 0 means patterned.
    return "\n".join([
        "Table S2 Floral phenotypes",
        "Species",
        "UV Proportion",
        "UV Pattern",
        "P_examplea",
        "0.45",
        "0",
        "Y",
        "1557",
        "41.5",
        "6.4",
        "617.8",
        "2654.5",
        "P_exampleb",
        "1.00",
        "1",
        "W",
        "2994",
        "40.5",
        "1.0",
        "807.6",
        "3209.0",
    ])
class OriginalUV2016Contracts(unittest.TestCase):
    def test_recover_source_0_present_1_uniform_not_inverted(self):
        rows=parse_source_rows({17:synthetic_page(17)})
        self.assertEqual(len(rows),2)
        self.assertEqual(rows[0]["source_measured_UV_pattern_present"],1)
        self.assertEqual(rows[1]["source_measured_UV_pattern_present"],0)
        self.assertEqual(rows[0]["source_TableS2_UV_pattern_0_present_1_absent"],0)
        self.assertEqual(rows[1]["source_TableS2_UV_pattern_0_present_1_absent"],1)
        self.assertEqual(rows[0]["source_mean_latitude_deg"],41.5)
        self.assertEqual(rows[0]["Bombus_source_model_overlap"],"NOT_COMPUTED")

    def test_rounded_uvp_threshold_disagreement_reported_not_silently_reclassified(self):
        b=synthetic_page(17).replace("0.45\n0\nY","0.45\n1\nY")
        rows=parse_source_rows({17:b})
        self.assertEqual(rows[0]["source_measured_UV_pattern_present"],0)
        self.assertEqual(
            rows[0]["UVP_rounded_threshold_vs_author_discrete_code"],
            "CHECK_SOURCE_ROUNDED_THRESHOLD"
        )

    def test_wrong_species_source_header_not_interpreted_as_taxon(self):
        a=parse_source_rows({17:synthetic_page(17)})
        self.assertEqual({x["original_taxon_code"] for x in a},
                         {"P_examplea","P_exampleb"})

    def test_missing_numeric_source_column_hard_stops(self):
        b=synthetic_page(17).replace("807.6\n3209.0","807.6")
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_TABLE_S2_NON_RECTANGULAR_ROWS"):
            parse_source_rows({17:b})

    def test_source177_denominator_does_not_accept_two_mock_species(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_177_TAXA_NOT_RECOVERED"):
            summarize(parse_source_rows({17:synthetic_page(17)}))

if __name__=="__main__":
    unittest.main()
