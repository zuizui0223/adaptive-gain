"""Offline only: fake DOCX OOXML fixture is NOT original 2025 species data."""
import io,unittest,zipfile
from probe_oliveira_245_original_supplement import (
    inspect_public_archive,inspect_docx_table,TABLE_NAME)

def zipped(files):
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for name,content in files.items():z.writestr(name,content)
    return b.getvalue()

W="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML=f'<w:document xmlns:w="{W}"><w:body><w:tbl>' \
    '<w:tr><w:tc><w:p><w:r><w:t>Species</w:t></w:r></w:p></w:tc>' \
    '<w:tc><w:p><w:r><w:t>UV %</w:t></w:r></w:p></w:tc></w:tr>' \
    '<w:tr><w:tc><w:p><w:r><w:t>Mockus testus</w:t></w:r></w:p></w:tc>' \
    '<w:tc><w:p><w:r><w:t>0.20</w:t></w:r></w:p></w:tc></w:tr>' \
    '</w:tbl></w:body></w:document>'

class OriginalAuthor245SupplementContract(unittest.TestCase):
    def test_inner_DOCX_source_table_shape_not_assumed_to_be_245_data(self):
        member=zipped({"word/document.xml":XML})
        r=inspect_docx_table(member)
        self.assertEqual(r["n_tables_in_original_DOCX"],1)
        self.assertEqual(r["first_15_original_tables"][0]["n_docx_table_rows"],2)
        self.assertTrue(r["no_false_245_distinct_accepted_species_claim"])
        self.assertTrue(r["no_UV_spatial_guide_label_from_average_UV_fraction"])

    def test_original_supplement_member_must_be_exact_not_similarly_named(self):
        wrong=zipped({"fake_table.docx":zipped({"word/document.xml":XML})})
        r=inspect_public_archive(wrong,"application/zip")
        self.assertEqual(r["status"],"AUTHOR_DOCX_TABLE_S1_NOT_FOUND_IN_OA_SUPPLEMENT_ARCHIVE")

    def test_correct_original_filename_is_not_enough_without_Word_document(self):
        outer=zipped({TABLE_NAME:zipped({"fake.xml":XML})})
        with self.assertRaisesRegex(ValueError,"NOT_AN_AUTHOR_ORIGINAL_DOCX"):
            inspect_public_archive(outer,"application/zip")

    def test_exact_member_yields_source_not_species_catalog(self):
        outer=zipped({TABLE_NAME:zipped({"word/document.xml":XML})})
        r=inspect_public_archive(outer,"application/zip")
        self.assertTrue(r["no_spectra_or_species_original_row_reconstruction"])
        self.assertEqual(r["original_primary_table"]["n_tables_in_original_DOCX"],1)
        self.assertEqual(r["archive_members"][0]["name"],TABLE_NAME)

if __name__=="__main__":
    unittest.main()
