"""Stage56 FReD: one specifically delimited, observational search, no bulk scrape.

Only post an exact genus option that exists in the original searchable
public form. A present genus option is not a measured genus/spectral row.
Retain an auditable small HTML read receipt and row/field structure.
No UV nectar-guide from one averaged flower-part reflectance, no photos,
no plant-fitness, no Bombus effects. The original form action is the only
allowed POST destination; never guess hidden service parameters.
"""
from __future__ import annotations
from html.parser import HTMLParser
import hashlib
import http.cookiejar
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import urllib.error

HOST="www.reflectance.co.uk"
ROOT="https://"+HOST
FORM_URL=ROOT+"/advance.php"
SEARCH_TARGET=ROOT+"/munger.php"
MAX_SIZE=2_000_000
SOURCE_CANDIDATES=("Potentilla","Argentina","Ranunculus","Campanula",
                   "Mimulus","Cirsium")

class OptionsParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.current_select=None
        self.current_option=None
        self.selects={}
        self.forms=[]
        self.form=None
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=="form":
            self.form={"action":d.get("action",""),"method":d.get("method","get").upper()}
            self.forms.append(self.form)
        elif tag=="select":
            self.current_select=d.get("name","")
            self.selects.setdefault(self.current_select,[])
        elif tag=="option" and self.current_select is not None:
            self.current_option={"explicit_value":("value" in d),
               "value":d.get("value",""),"label":""}
    def handle_data(self,data):
        if self.current_option is not None:
            self.current_option["label"]+=data
    def handle_endtag(self,tag):
        if tag=="option" and self.current_option is not None:
            self.current_option["label"]=" ".join(self.current_option["label"].split())
            self.selects[self.current_select].append(self.current_option)
            self.current_option=None
        if tag=="select":
            self.current_select=None
        if tag=="form":self.form=None

def pick_genus(selects,priorities=SOURCE_CANDIDATES):
    options=selects.get("genus",[])
    if not options:
        return None
    for genus in priorities:
        exact=[x for x in options if x["label"].casefold()==genus.casefold()]
        if not exact:
            continue
        if len(exact)>1: raise ValueError("NO_GO_AMBIGUOUS_FRED_ORIGINAL_GENUS_OPTION")
        e=exact[0]
        value=e["value"] if e["explicit_value"] else e["label"]
        if not value or len(value)>100 or "<" in value or ">" in value:
            raise ValueError("NO_GO_EMPTY_OR_UNSAFE_FRED_SOURCE_GENUS_OPTION")
        return {"label":genus,"form_value":value,"explicit_value":e["explicit_value"]}
    return None

def read_live_page(openurl,url,data=None):
    if urllib.parse.urlsplit(url).hostname!=HOST or url not in (FORM_URL,SEARCH_TARGET):
        raise ValueError("NO_GO_OUTSIDE_VERIFIED_FRED_PUBLIC_SEARCH_ENDPOINT")
    r=urllib.request.Request(url,data=data,headers={
       "User-Agent":"adaptive-gain-stage56-FReD-single-genus-original-sample-probe/2026",
       "Accept":"text/html,application/xhtml+xml",
       "Referer":FORM_URL,
       "Content-Type":"application/x-www-form-urlencoded"})
    with openurl(r,timeout=45) as h:
        final_url=h.geturl()
        if urllib.parse.urlparse(final_url).hostname not in (HOST,"reflectance.co.uk"):
            raise ValueError("NO_GO_FRED_UNKNOWN_EXTERNAL_REDIRECT")
        if "html" not in h.headers.get("Content-Type","").lower():
            raise ValueError("NO_GO_FRED_SEARCH_RESPONSE_NOT_HTML")
        raw=h.read(MAX_SIZE+1)
        status=h.status
    if len(raw)>MAX_SIZE:
        raise ValueError("NO_GO_FRED_SEARCH_RESPONSE_TOO_LARGE")
    return {"html":raw.decode("utf8",errors="replace"),
            "source_http_status":status,"source_final_url":final_url,
            "source_response_sha256":hashlib.sha256(raw).hexdigest(),
            "source_response_bytes":len(raw)}

class SearchResultParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.seen_headings=[]
        self.in_cell=None
        self.current_row=[]
        self.table_rows=[]
        self.links=[]
        self.text=[]
        self.in_script=False
        self.rowcount=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=="tr":
            self.current_row=[]
            self.rowcount+=1
        if tag in ("th","td"):self.in_cell=[tag,""]
        if tag in ("script","style"):self.in_script=True
        if tag=="a":
            u=d.get("href","")
            if u and len(self.links)<100:
                self.links.append(u[:200])
    def handle_data(self,data):
        if self.in_cell is not None:
            self.in_cell[1]+=data
        if not self.in_script and len(self.text)<250:
            x=" ".join(data.split())
            if x:self.text.append(x[:80])
    def handle_endtag(self,tag):
        if tag in ("th","td") and self.in_cell is not None:
            kind,t=self.in_cell
            t=" ".join(t.split())[:120]
            if kind=="th" and t and len(self.seen_headings)<100:
                self.seen_headings.append(t)
            self.current_row.append(t)
            self.in_cell=None
        if tag=="tr":
            if self.current_row and len(self.table_rows)<12:
                self.table_rows.append(self.current_row[:25])
            self.current_row=[]
        if tag in ("script","style"):self.in_script=False

def run(opener=None):
    if opener is None:
        manager=urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        opener=manager.open
    first=read_live_page(opener,FORM_URL)
    parser=OptionsParser();parser.feed(first["html"])
    choices=parser.selects
    matching_forms=[x for x in parser.forms
                    if urllib.parse.urljoin(FORM_URL,x["action"])==SEARCH_TARGET
                    and x["method"]=="POST"]
    if len(matching_forms)!=1:raise ValueError("NO_GO_FRED_SEARCH_FORM_NOT_UNIQUE_OR_POST")
    selected=pick_genus(choices)
    report={
       "status":"ORIGINAL_FRED_PUBLIC_SOURCE_SINGLE_GENUS_SEARCH_GATE",
       "source_site":"https://www.reflectance.co.uk/",
       "source_database_DOI":"10.1371/journal.pone.0014287",
       "source_advanced_page":{k:v for k,v in first.items() if k!="html"},
       "n_original_genus_form_options":len(choices.get("genus",[])),
       "source_ranked_target_genera":list(SOURCE_CANDIDATES),
       "selected_source_exact_genus_or_unknown":selected["label"] if selected else "",
       "trait_spectrum_guide_and_GPS_not_assumed_from_form":True,
       "no_cross_genus_outcome_driven_search":True,
       "source_response_results":None,
    }
    if selected is None:
        report["status"]="NO_MATCHED_SOURCE_GENUS_OPTION_NO_FALSE_NEGATIVE"
        return report
    # The original form's known input names are from live source; POST only the
    # selected exact genus and search button, no site-wide unbounded scrape.
    payload=urllib.parse.urlencode({"genus":selected["form_value"],
                                    "search1":"Search",
                                    "genusc":"on","speciesc":"on","countryc":"on",
                                    "townc":"on","eastc":"on","southc":"on",
                                    "flowersectc":"on","pollinatorc":"on"}).encode("utf8")
    response=read_live_page(opener,SEARCH_TARGET,data=payload)
    parsed=SearchResultParser();parsed.feed(response["html"])
    report["source_response_results"]={
       **{k:v for k,v in response.items() if k!="html"},
       "html_table_rows_seen":parsed.rowcount,
       "table_first_12_rows_not_confirmed_species_records":parsed.table_rows,
       "table_headers_or_labels":parsed.seen_headings[:80],
       "internal_result_href_examples":parsed.links[:35],
       "visible_text_first_120_tokens":parsed.text[:120],
       "field_presence_not_yet_verified_GPS_geocode_per_spectrum":True,
       "html_row_count_not_certified_distinct_specimens":True,
       "no_spatial_UV_pattern_or_Bombus_ecological_effect_fitted":True,
    }
    return report

def main():
    out=Path("stage56_FReD_original_public_sample_response")
    out.mkdir(exist_ok=True)
    try:
        report=run()
    except (ValueError,urllib.error.URLError,urllib.error.HTTPError,TimeoutError) as e:
        report={"status":"SOURCE_FRED_PUBLIC_SEARCH_UNAVAILABLE_NOT_MISSING_SPECIMENS",
                "error_type":type(e).__name__,
                "error_summary":str(e)[:240],
                "no_unverified_sample_locations_assigned":True}
    (out/"FReD_one_original_source_genus_search_receipt.json").write_text(
        json.dumps(report,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
        encoding="utf8")
    print("STAGE56_REAL_FRED_SINGLE_GENUS_ORIGINAL_PAGE",json.dumps(
        report,sort_keys=True,ensure_ascii=False))
    print("NO_UV_PATTERN_BY_SPECIES_OR_GPS_GUILD_ASSOCIATION_FROM_HTML_ALONE")

if __name__=="__main__":
    main()
