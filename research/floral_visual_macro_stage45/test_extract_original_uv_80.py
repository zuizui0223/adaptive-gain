"""Source-free PDF categorical extraction safety checks. No fake UV ecology."""
import unittest
from extract_original_uv_80 import (
    parse_table_pages,evaluate,EXPECTED_COUNTS
)

class FakeTable:
    def __init__(self,rows):self.rows=rows
    def extract(self):return self.rows
class FakeFound:
    def __init__(self,tables):self.tables=[FakeTable(x) for x in tables]
class FakePage:
    def __init__(self,rows):self.rows=rows
    def find_tables(self,**kwargs):return FakeFound([self.rows])
class FakePdf:
    def __init__(self,rows):self.pages=[FakePage([]),FakePage(rows)]
    def __len__(self):return len(self.pages)
    def __getitem__(self,n):return self.pages[n]

def r(name,uv,nonuv="Absent"):
    return ["",name,uv,"Melittophilous","N","Flower",nonuv]

class OriginalUVTableContracts(unittest.TestCase):
    def test_category_mapping_and_pollination_uncertainty(self):
        rows=[["Species","","UV-categories","Pollination system","Floral resources",
               "Attraction unit","Non-UV pattern"],
              ["Lamiaceae","","","","","",""],
              r("Salvia mockiana","CM","Present"),
              r("Mockus patternless","A"),
              r("Mockus uncertain sp.","BE")]
        d=parse_table_pages(FakePdf(rows))
        self.assertEqual(len(d),3)
        self.assertEqual(d[0]["source_family_name"],"Lamiaceae")
        self.assertEqual(d[0]["uv_pattern_present"],1)
        self.assertEqual(d[0]["non_uv_pattern_present"],1)
        self.assertEqual(d[1]["uv_pattern_present"],0)
        self.assertEqual(d[2]["species_level_binomial_candidate"],0)
        for x in d:
            self.assertEqual(x["pollination_evidence_basis"],
                             "source_literature_or_syndrome_inference_mixed")

    def test_hard_stop_on_invalid_category_and_visible_pattern(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_UV_CATEGORY"):
            parse_table_pages(FakePdf([r("Mockus a","UNKNOWN")]))
        with self.assertRaisesRegex(ValueError,"NO_GO_UNKNOWN_VISIBLE"):
            parse_table_pages(FakePdf([r("Mockus a","BE","Maybe")]))

    def test_80_rows_and_five_author_categories_exact(self):
        rows=[]
        for cat,n in EXPECTED_COUNTS.items():
            for i in range(n):
                rows.append({
                    "taxon_as_published":f"Mockus {cat}{i}",
                    "uv_category":cat,
                    "uv_pattern_present":int(cat in ("BE","CM","CR")),
                    "non_uv_pattern_present":0,
                    "species_level_binomial_candidate":1,
                })
        obj=evaluate(rows)
        self.assertEqual(obj["n_original_taxon_rows"],80)
        self.assertEqual(obj["n_patterned_author_categories"],27)
        self.assertEqual(obj["n_uniform_A_R_author_categories"],53)
        self.assertTrue(obj["source_pollination_labels_NOT_direct_Bombus_observations"])
        with self.assertRaisesRegex(ValueError,"NO_GO_NOT_SOURCE_VERIFIED"):
            evaluate(rows[:-1])

    def test_repeated_taxon_hard_stop(self):
        rows=[]
        for cat,n in EXPECTED_COUNTS.items():
            rows.extend({"taxon_as_published":"same" if i<2 else f"{cat}-{i}",
                         "uv_category":cat,
                         "uv_pattern_present":int(cat in ("BE","CM","CR")),
                         "non_uv_pattern_present":0,
                         "species_level_binomial_candidate":1}
                        for i in range(n))
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_PDF_DUPLICATED"):
            evaluate(rows)


if __name__=="__main__":
    unittest.main()
