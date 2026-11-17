"""Mock-only source-digest and Zenodo archive admission controls."""
import io,hashlib,importlib.util,unittest,zipfile
from pathlib import Path
p=Path(__file__).with_name("audit_original_2021_sensory_drive_Zenodo.py")
sp=importlib.util.spec_from_file_location("z74b",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class Original2021Controls(unittest.TestCase):
    def test_2021_author_publication_not_novel(self):
        self.assertEqual(m.REFERENCE_DOI,"10.5281/zenodo.5110165")
        self.assertEqual(m.PUBLICATION_DOI,"10.1111/nph.17631")
    def test_only_official_Zenodo_source_host(self):
        with self.assertRaisesRegex(ValueError,"ONLY_OFFICIAL"):
            m.get("http://localhost/private")
        with self.assertRaisesRegex(ValueError,"ONLY_OFFICIAL"):
            m.get("https://other.com/file")
    def test_original_MD5_and_SHA256_must_match(self):
        raw=b"field measured guide original"
        good_md5="md5:"+hashlib.md5(raw).hexdigest()
        good_sha="sha256:"+hashlib.sha256(raw).hexdigest()
        self.assertTrue(m.verify_original_author_digest(raw,good_md5)[0])
        self.assertTrue(m.verify_original_author_digest(raw,good_sha)[0])
        self.assertFalse(m.verify_original_author_digest(raw,"md5:"+"0"*32)[0])
        self.assertFalse(m.verify_original_author_digest(raw,"not_specified")[0])
    def test_zip_original_members_are_not_claimed_as_visited_species(self):
        mem=io.BytesIO()
        with zipfile.ZipFile(mem,"w",zipfile.ZIP_DEFLATED) as z:
            z.writestr("field/raw_visits.csv","elevation,visits\nhigh,10\n")
        found=m.source_members(mem.getvalue(),"source.zip")
        self.assertEqual(found["original_zip_non_directory_member_count"],1)
        self.assertTrue(found["original_zip_member_metadata_only_not_extracted"])
        self.assertEqual(found["original_zip_members"][0]["filename"],"field/raw_visits.csv")
    def test_nominal_html_not_counted_as_original_CSV(self):
        self.assertEqual(m.source_members(b"<html>Error</html>","visits.csv")["status"],
                         "HTTP200_NOT_ORIGINAL_CSV")
    def test_real_original_CSV_header_audited(self):
        rec=m.source_members(b"elevation,guide,visits\nhigh,large,4\n","field.csv")
        self.assertEqual(rec["original_source_line_count"],2)
        self.assertEqual(rec["original_csv_first_four_rows"][0],
                         ["elevation","guide","visits"])
if __name__=="__main__":unittest.main()
