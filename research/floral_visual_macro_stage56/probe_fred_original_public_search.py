"""Stage56: FReD source-native search schema, not an inferred bee signal.

Source: Arnold et al. 2010 Floral Reflectance Database,
doi:10.1371/journal.pone.0014287 and current service
https://www.reflectance.co.uk/. User-facing public terms permit data use
with database citation. Do not treat a location field or a spectrum as
observed locality/petal-guide until the record actually carries it.
Only read two HTML pages; do not crawl/search/speculate about endpoint
parameters. Retain schema/provenance not raw HTML/identifying collectors.
"""
from __future__ import annotations
from html.parser import HTMLParser
import hashlib
import json
import pathlib
import urllib.error
import urllib.parse
import urllib.request

ROOT="https://www.reflectance.co.uk"
PATHS=("/", "/advance.php", "/tou.php")
MAX_BYTES=1_500_000

class FredFormParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms=[]
        self.active=None
        self.select_name=None
        self.links=[]
        self.titles=[]
        self.in_title=False
    def handle_starttag(self,tag,attrs):
        data=dict(attrs)
        if tag=="title":self.in_title=True
        if tag=="form":
            if self.active is not None:
                raise ValueError("NO_GO_NESTED_FRED_SOURCE_FORM")
            self.active={"action":data.get("action",""),"method":data.get("method","GET").upper(),
                         "fields":[],"selects":[]}
        if tag in ("input","textarea") and self.active is not None:
            self.active["fields"].append({
               "type":data.get("type","text") if tag=="input" else "textarea",
               "name":data.get("name",""),
               "value":data.get("value","")[:30] if data.get("type")=="hidden" else "",
            })
        if tag=="select" and self.active is not None:
            self.select_name=data.get("name","")
            self.active["selects"].append({"name":self.select_name,"n_options":0,
                                           "value_examples":[]})
        if tag=="option" and self.active is not None and self.select_name is not None:
            s=self.active["selects"][-1]
            s["n_options"]+=1
            if len(s["value_examples"])<8:
                s["value_examples"].append(data.get("value","")[:50])
        if tag=="a" and "href" in data and len(self.links)<150:
            href=data["href"]
            if href and not href.startswith(("javascript:","mailto:")):
                u=urllib.parse.urljoin(ROOT+"/",href)
                if urllib.parse.urlparse(u).hostname in ("www.reflectance.co.uk","reflectance.co.uk"):
                    self.links.append(u)
    def handle_endtag(self,tag):
        if tag=="form" and self.active:
            self.forms.append(self.active)
            self.active=None
        if tag=="select":self.select_name=None
        if tag=="title":self.in_title=False
    def handle_data(self,data):
        if self.in_title and data.strip():self.titles.append(data.strip())

def safe_page(path,opener=urllib.request.urlopen):
    if path not in PATHS:
        raise ValueError("NO_GO_FRED_UNAPPROVED_SOURCE_PAGE")
    url=ROOT+path
    req=urllib.request.Request(url,headers={
       "User-Agent":"adaptive-gain-floral-stage56-FReD-public-search-audit/2026",
       "Accept":"text/html,application/xhtml+xml"})
    with opener(req,timeout=25) as res:
        mime=res.headers.get("Content-Type","")
        actual=res.geturl()
        if urllib.parse.urlparse(actual).hostname not in ("www.reflectance.co.uk","reflectance.co.uk"):
            raise ValueError("NO_GO_FRED_REDIRECTS_OUTSIDE_SOURCE_HOST")
        blob=res.read(MAX_BYTES+1)
        http_status=res.status
    if len(blob)>MAX_BYTES:
        raise ValueError("NO_GO_FRED_SOURCE_HTML_TOO_LARGE")
    if "html" not in mime.lower() or b"<" not in blob:
        raise ValueError("NO_GO_FRED_NOT_HTML_SOURCE")
    parsed=FredFormParser()
    parsed.feed(blob.decode("utf8",errors="replace"))
    return {
       "status":"FRED_SOURCE_PUBLIC_HTML_READABLE",
       "requested_source_path":path,
       "requested_source_url":url,
       "http_status":http_status,
       "content_type":mime,
       "source_html_sha256":hashlib.sha256(blob).hexdigest(),
       "source_byte_count":len(blob),
       "page_titles":parsed.titles[:4],
       "forms":parsed.forms[:10],
       "internal_source_links":sorted(set(parsed.links))[:30],
       "source_form_fields_not_spectral_or_spatial_observations":True,
    }

def main():
    out=pathlib.Path("stage56_FReD_original_public_search_audit")
    out.mkdir(exist_ok=True)
    report={
      "status":"SOURCE_FIRST_FRED_SITE_SCHEMA_ONLY",
      "source_database_doi":"10.1371/journal.pone.0014287",
      "source_site_root":ROOT,
      "source_claimed_GPS_or_specimen_coordinates_not_yet_audited":True,
      "original_Koski2016_563_UV_specimens_not_joinable_to_genetic_Table_S1_by_species_alone":True,
      "pages":{},
    }
    for path in PATHS:
        try: report["pages"][path]=safe_page(path)
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,ValueError) as exc:
            report["pages"][path]={"status":"UNAVAILABLE_NOT_ABSENCE_OF_FRED_RECORDS",
                "error_type":type(exc).__name__,
                "error_message":str(exc)[:160]}
    (out/"FReD_original_public_site_source_form_receipt.json").write_text(
      json.dumps(report,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("STAGE56_FRED_SITE_SCHEMA_AND_SOURCE_GATES",
      json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("NO_SPECIMEN_GPS_OR_UV_SPATIAL_GUIDE_OR_BOMBUS_EXPOSURE_CLAIM")
if __name__=="__main__":
    main()
