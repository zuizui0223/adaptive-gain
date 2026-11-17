"""Mock-only source entry and strict simultaneous island source checks."""
import hashlib,importlib.util,io,unittest
from pathlib import Path
p=Path(__file__).with_name("probe_kent_original_public_dryad_stream.py")
sp=importlib.util.spec_from_file_location("kent_original",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class KentIslandOriginalTests(unittest.TestCase):
    def test_two_different_public_web_stream_ids_exact_source(self):
        self.assertEqual(m.FILES["Floral_Reflectance_Kent_Island_Plants.csv"],4074180)
        self.assertEqual(m.FILES["2019_2023_Kent_Island_Plant_Pollinator_Network.csv"],4074184)
        self.assertEqual(m.PUBLISHED["spectral_plant_species"],90)
        self.assertEqual(m.PUBLISHED["visited_plant_species"],74)
        self.assertEqual(m.PUBLISHED["individual_visitor_observations"],3718)
    def test_source_html_only_exact_public_file_stream(self):
        raw=(b'<a href="/downloads/file_stream/4074180">'
             b'Floral_Reflectance_Kent_Island_Plants.csv</a>'
             b'<a href="/downloads/file_stream/4074184">'
             b'2019_2023_Kent_Island_Plant_Pollinator_Network.csv</a>')
        links=m.author_page_links(raw)
        self.assertEqual(len(links),2)
        self.assertEqual(links[0]["stream_id"],4074180)
        self.assertEqual(links[1]["stream_id"],4074184)
    def test_no_http200_html_as_real_original_CSV(self):
        self.assertFalse(m.is_actual_utf8_csv(b"<html>access denied</html>"))
        self.assertFalse(m.is_actual_utf8_csv(b"\xff\xfe"))
        self.assertTrue(m.is_actual_utf8_csv(b"Wavelength,Aster sp.\n300,0.3\n"))
    def test_real_author_SHA_must_match(self):
        good=b"Wavelength,Aster sp.\n300,0.3\n"
        h=hashlib.sha256(good).hexdigest()
        ok,rec=m.verify_original(good,{"digest":h})
        self.assertTrue(ok)
        self.assertEqual(rec["status"],"ORIGINAL_AUTHOR_SHA256_AND_CSV_VERIFIED")
        bad,rec=m.verify_original(good,{"digest":"0"*64})
        self.assertFalse(bad)
        self.assertEqual(rec["status"],"ORIGINAL_FILE_SHA256_MISMATCH")
    def test_spurious_API_sha_cannot_imply_public_data(self):
        good=b"Wavelength,Aster sp.\n300,0.3\n"
        ok,rec=m.verify_original(good,{"digest":""})
        self.assertFalse(ok)
        self.assertEqual(rec["status"],"OFFICIAL_FILE_SHA256_NOT_DECLARED")
    def test_true_source_sample_grain_without_pseudo_zeros(self):
        original=(
          b"Wavelength,Aster sp.,Solidago sp.,Stimulus paper\n"
          b"300,1.1,3.2,10\n"
          b"310,1.2,3.7,11\n"
        )
        obs=(
          b"Insect_ID,Year,Insect_Species,Taxonomic_Group,Plant\n"
          b"1,2022,Bombus terrestris,bees,Aster sp.\n"
          b"2,2023,Hoverfly sp.,flies,Solidago sp.\n"
        )
        r=m.audit_join(original,obs)
        self.assertEqual(r["strict_literal_plant_overlap"],2)
        self.assertEqual(r["original_visitation_rows"],2)
        self.assertTrue(r["original_measured_spectral_plant_and_field_visitor_same_island"])
        self.assertTrue(r["original_no_visitor_record_not_verified_absence"])
        self.assertFalse(r["spectra_2019_field_visits_temporally_identical"])
    def test_no_external_hosts(self):
        with self.assertRaisesRegex(ValueError,"ONLY_OFFICIAL"):
            m.fetch("https://example.org/file.csv")

if __name__=="__main__":
    unittest.main()
