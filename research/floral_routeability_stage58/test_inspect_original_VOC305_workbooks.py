"""Only mock mini-XLSX bytes, never false original VOC measurements."""
import io,zipfile,hashlib,unittest
from unittest.mock import patch
from openpyxl import Workbook
from inspect_original_VOC305_workbooks import inspect_source_workbooks

def make_xlsx(label):
    book=Workbook();sheet=book.active;sheet.title="Data"
    sheet.append(["species","family","compound",label])
    sheet.append(["Mockus plantus","X",None,123])
    out=io.BytesIO();book.save(out);return out.getvalue()

def make_zip(workbooks):
    bio=io.BytesIO()
    with zipfile.ZipFile(bio,"w") as z:
        for k,v in workbooks.items():z.writestr(k,v)
    return bio.getvalue()

class OriginalFArmegnol305SourceDataContract(unittest.TestCase):
    def test_bound_header_schema_never_infers_missing_flower_scent(self):
        files={f"DataSheet_{i}.xlsx":make_xlsx(f"field{i}") for i in (1,2,3)}
        pins={k:hashlib.sha256(v).hexdigest() for k,v in files.items()}
        with patch("inspect_original_VOC305_workbooks.MEMBERS",pins):
            r=inspect_source_workbooks(make_zip(files))
        self.assertEqual(r["status"],"SOURCE_AUTHENTIC_FARRE_2020_3_VOC_WORKBOOKS_SCHEMA")
        self.assertEqual(len(r["source_authored_workbooks"]),3)
        self.assertTrue(r["no_absent_VOC_phenotype_inferred_from_empty_XLSX_cell"])
        self.assertEqual(r["source_authored_workbooks"]["DataSheet_1.xlsx"]
                         ["worksheets"][0]["first_5_rows_source_schema_only"][1][2],"")

    def test_any_inner_workbook_digest_changed_must_hard_fail(self):
        files={f"DataSheet_{i}.xlsx":make_xlsx(f"field{i}") for i in (1,2,3)}
        pins={k:hashlib.sha256(v).hexdigest() for k,v in files.items()}
        pins["DataSheet_2.xlsx"]="0"*64
        with patch("inspect_original_VOC305_workbooks.MEMBERS",pins):
            with self.assertRaisesRegex(ValueError,"INNER_SHA_CHANGED"):
                inspect_source_workbooks(make_zip(files))

    def test_three_workbooks_required_no_missing_as_trait_zero(self):
        files={f"DataSheet_{i}.xlsx":make_xlsx(f"field{i}") for i in (1,2)}
        pins={k:hashlib.sha256(v).hexdigest() for k,v in files.items()}
        pins["DataSheet_3.xlsx"]="0"*64
        with patch("inspect_original_VOC305_workbooks.MEMBERS",pins):
            with self.assertRaisesRegex(ValueError,"NOT_UNIQUE"):
                inspect_source_workbooks(make_zip(files))

if __name__=="__main__":unittest.main()
