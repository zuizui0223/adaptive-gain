"""Mock-only nested source files, no invented published species labels."""
import io,zipfile,unittest
from inspect_nested_visual_trait_tables import _body_docx
from xml.etree import ElementTree as ET

def docx():
    x=b'''<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>
      <w:tbl><w:tr><w:tc><w:p><w:r><w:t>Species</w:t></w:r></w:p></w:tc>
      <w:tc><w:p><w:r><w:t>Colour change</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
      </w:body></w:document>'''
    raw=io.BytesIO()
    with zipfile.ZipFile(raw,"w") as z:
        z.writestr("word/document.xml",x)
    return raw.getvalue()
class NestedTableSourceSafe(unittest.TestCase):
    def test_docx_original_table_headers_only(self):
        r=_body_docx(docx())
        self.assertEqual(r["format"],"DOCX")
        self.assertEqual(r["n_tables"],1)
        self.assertEqual(r["table_schemas"][0]["first_two_rows_as_schema"][0],
                         ["Species","Colour change"])

    def test_do_not_confuse_random_zip_with_docx_source(self):
        self.assertEqual(_body_docx(b"this isn't word")["format"],"NOT_DOCX")


if __name__=="__main__":
    unittest.main()
