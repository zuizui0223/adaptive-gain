"""No real species or spectral observations are synthesized in tests."""
import unittest
import urllib.parse
from probe_fred_single_real_genus_sample import OptionsParser,pick_genus,run

SAMPLE="""<html><form method="POST" action="munger.php">
<select name="genus"><option>All</option><option>Potentilla</option>
<option>Campanula</option></select>
<input type="submit" name="search1"/>
</form></html>"""

class Response:
    def __init__(self,html,url):
        self.b=html.encode()
        self.u=url
        self.status=200
        self.headers={"Content-Type":"text/html; charset=UTF-8"}
    def read(self,n):return self.b[:n]
    def geturl(self):return self.u
    def __enter__(self):return self
    def __exit__(self,*a):pass

class OriginalFReDGenusSearchContract(unittest.TestCase):
    def test_priority_is_declared_before_guild_trait_outcome(self):
        p=OptionsParser();p.feed(SAMPLE)
        x=pick_genus(p.selects)
        self.assertEqual(x["label"],"Potentilla")
        self.assertEqual(x["form_value"],"Potentilla")
        self.assertFalse(x["explicit_value"])

    def test_explicit_empty_option_no_false_wildcard_request(self):
        p=OptionsParser();p.feed('<select name="genus"><option value="">Potentilla</option></select>')
        with self.assertRaisesRegex(ValueError,"EMPTY_OR_UNSAFE"):
            pick_genus(p.selects)

    def test_mock_source_post_uses_exact_genus_then_retains_html_ambiguity(self):
        seen=[]
        def opener(request,timeout):
            u=request.full_url;seen.append((u,request.data))
            if len(seen)==1:
                return Response(SAMPLE,"https://www.reflectance.co.uk/advance.php")
            return Response("<html><table><tr><th>Genus</th><th>GPS east</th><th>GPS south</th></tr>"
                            "<tr><td>Potentilla</td><td></td><td></td></tr></table></html>",
                            "https://www.reflectance.co.uk/munger.php")
        r=run(opener=opener)
        self.assertEqual(len(seen),2)
        self.assertIn(b"genus=Potentilla",seen[1][1])
        self.assertEqual(r["source_response_results"]["html_table_rows_seen"],2)
        self.assertTrue(r["source_response_results"][
            "field_presence_not_yet_verified_GPS_geocode_per_spectrum"])
        self.assertEqual(r["source_response_results"][
            "table_first_12_rows_not_confirmed_species_records"][1][1],"")

    def test_unknown_genera_prevent_broad_search(self):
        def opener(request,timeout):
            return Response("<html><form method='POST' action='munger.php'>"
                            "<select name='genus'><option>Only Unknownus</option>"
                            "</select></form></html>",
                            "https://www.reflectance.co.uk/advance.php")
        r=run(opener=opener)
        self.assertEqual(r["status"],"NO_MATCHED_SOURCE_GENUS_OPTION_NO_FALSE_NEGATIVE")
        self.assertIsNone(r["source_response_results"])

    def test_invalid_form_action_does_not_post(self):
        def opener(request,timeout):
            return Response("<html><form action='admin.php' method='POST'>"
                            "<select name='genus'><option>Potentilla</option></select>"
                            "</form></html>",
                            "https://www.reflectance.co.uk/advance.php")
        with self.assertRaisesRegex(ValueError,"NOT_UNIQUE_OR_POST"):
            run(opener=opener)

if __name__=="__main__":
    unittest.main()
