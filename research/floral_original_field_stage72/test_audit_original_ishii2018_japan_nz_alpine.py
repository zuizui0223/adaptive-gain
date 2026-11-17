"""Source-free tests for PMC DOI-pinned public original alpine spectra/visits."""
import importlib.util,unittest
from pathlib import Path
p=Path(__file__).with_name("audit_original_ishii2018_japan_nz_alpine.py")
spec=importlib.util.spec_from_file_location("s72d",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class IshiiOriginalSupplementGuards(unittest.TestCase):
    def test_original_geographic_independence(self):
        self.assertEqual(m.PMCID,"PMC6377100")
        self.assertEqual(m.DOI,"10.1093/aob/mcy188")
        self.assertEqual(m.ORIGINAL_PUBLISHED_COUNTS["Japanese_native_spectra_species"],106)
        self.assertEqual(m.ORIGINAL_PUBLISHED_COUNTS["New_Zealand_native_spectra_species"],96)
        self.assertTrue(m.ORIGINAL_PUBLISHED_COUNTS["Mount_Hutt_no_original_pollinator_observation"])
    def test_explicit_only_original_author_OA_and_supplement_urls(self):
        self.assertIn("PMC6377100",m.OA_API)
        self.assertEqual(len(m.SUPPORT),2)
        self.assertTrue(m.SUPPORT["aob-18614-s02.xlsx"].endswith("colour_properties"))
    def test_XML_original_PMCID_mismatch_rejected(self):
        bad=b'<OA><records><record id="PMC0"><link format="tgz" href="ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/x.tar.gz"/></record></records></OA>'
        with self.assertRaisesRegex(ValueError,"ID_MISMATCH"):
            m.oa_original_package_url(bad)
    def test_only_original_national_archive_host_allowed(self):
        self.assertEqual(m.normalize_archive_link("ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/x.tar.gz"),
                         "https://ftp.ncbi.nlm.nih.gov/pub/pmc/x.tar.gz")
        with self.assertRaisesRegex(ValueError,"UNEXPECTED_ORIGINAL_PMC_OA_DOWNLOAD_HOST"):
            m.normalize_archive_link("https://other.invalid/x.tar.gz")
    def test_original_public_oa_valid_metadata(self):
        text=b'<OA><records><record id="PMC6377100" license="CC BY"><link format="tgz" href="ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/a.tar.gz"/></record></records></OA>'
        url,attr=m.oa_original_package_url(text)
        self.assertEqual(url,"https://ftp.ncbi.nlm.nih.gov/pub/pmc/a.tar.gz")
        self.assertEqual(attr["license"],"CC BY")

if __name__=="__main__":unittest.main()
