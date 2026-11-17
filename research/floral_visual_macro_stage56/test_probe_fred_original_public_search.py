"""No fabricated spectra or plant coordinates. HTML fixtures only."""
import io
import unittest
from probe_fred_original_public_search import FredFormParser,safe_page

class FakeResponse:
    def __init__(self,body,ctype,url="https://www.reflectance.co.uk/advance.php",status=200):
        self.body=body
        self.headers={"Content-Type":ctype}
        self.url=url
        self.status=status
    def geturl(self):return self.url
    def read(self,n):return self.body[:n]
    def __enter__(self):return self
    def __exit__(self,*args):pass

class FredSourceSiteOriginalSchemaContracts(unittest.TestCase):
    sample=b"""<html><head><title>FReD</title></head><body>
       <form action="search.php" method="post">
         <select name="family"><option value="">all</option><option value="ros">Rose</option></select>
         <input name="lat" type="text"/>
         <input name="nation" type="hidden" value=""/>
         <input name="submit" type="submit" value="go"/>
       </form>
       <a href="tou.php">Terms</a>
    </body></html>"""

    def test_form_action_method_field_names_and_option_counts_not_inferred_species(self):
        p=FredFormParser();p.feed(self.sample.decode())
        self.assertEqual(p.titles,["FReD"])
        self.assertEqual(len(p.forms),1)
        self.assertEqual(p.forms[0]["action"],"search.php")
        self.assertEqual(p.forms[0]["method"],"POST")
        self.assertEqual(p.forms[0]["selects"][0]["n_options"],2)
        self.assertIn("lat",[x["name"] for x in p.forms[0]["fields"]])
        self.assertIn("https://www.reflectance.co.uk/tou.php",p.links)

    def test_live_source_mock_preserves_provenance_not_spectral_or_GPS_claim(self):
        def opener(request,timeout):
            return FakeResponse(self.sample,"text/html; charset=utf-8")
        r=safe_page("/advance.php",opener=opener)
        self.assertTrue(r["source_form_fields_not_spectral_or_spatial_observations"])
        self.assertEqual(r["source_byte_count"],len(self.sample))
        self.assertEqual(len(r["source_html_sha256"]),64)

    def test_non_approved_external_domain_or_pdf_hard_stop(self):
        def evil(req,timeout):
            return FakeResponse(self.sample,"text/html",url="https://not-example.net/p")
        with self.assertRaisesRegex(ValueError,"REDIRECTS_OUTSIDE"):
            safe_page("/advance.php",opener=evil)
        with self.assertRaisesRegex(ValueError,"UNAPPROVED"):
            safe_page("/search.php",opener=evil)
        def pdf(req,timeout):
            return FakeResponse(b"%PDF-1.4","application/pdf")
        with self.assertRaisesRegex(ValueError,"NOT_HTML"):
            safe_page("/advance.php",opener=pdf)

    def test_oversize_source_html_rejected(self):
        from probe_fred_original_public_search import MAX_BYTES
        def huge(req,timeout):
            return FakeResponse(b"<"+b"x"*MAX_BYTES,"text/html")
        with self.assertRaisesRegex(ValueError,"TOO_LARGE"):
            safe_page("/advance.php",opener=huge)

    def test_no_hidden_collector_personal_metadata_written(self):
        p=FredFormParser()
        p.feed("<html><form><input type='password' name='pass' value='SECRET' /></form></html>")
        self.assertEqual(p.forms[0]["fields"][0]["value"],"")
if __name__=="__main__":
    unittest.main()
