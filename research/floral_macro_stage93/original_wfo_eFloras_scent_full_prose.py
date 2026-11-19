#!/usr/bin/env python3
"""Stage93 original World Flora Online eFloras full-description source preflight.

Read ORIGINAL Flora of China/Flora of North America Darwin Core Archives (DwC-A).
Do not pretend NHM ADEPT's absent scent field implies no floral fragrance.
Strict original text phrases -> positive / explicit negative / unknown; unresolved
mentions and contradictory texts are not forced to binary 0/1.
Original WFO source is not an unbiased native-plant observation campaign.
No wind coefficient, no behavioural plume or bee information use.
"""
from __future__ import annotations
import argparse,csv,hashlib,html,io,json,re,statistics,sys,xml.etree.ElementTree as ET,zipfile
from collections import Counter,defaultdict
from html.parser import HTMLParser
from pathlib import Path,PurePosixPath

BASE=Path(__file__).resolve().parents[1]
for m in ("floral_macro_stage87","floral_macro_stage89"):
    sys.path.insert(0,str(BASE/m))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions,strict_name
from gift32_independent_pollen_mode_global_native_coverage import original_gift_species

ORIGINAL={
 "Flora_of_China":"https://files.worldfloraonline.org/files/eFloras/Flora_Of_China/Flora_Of_China.zip",
 "Flora_of_North_America":"https://files.worldfloraonline.org/files/eFloras/FNA/FNA.zip",
}
# First genuine source ZIP download verified in Actions 44518683985:
SOURCE_SHA256={
 "Flora_of_China":"4c0b89280efdcfd0ef8dc753cca5d63566ddf8c34542b0bb4a78cdce799b63a9",
 "Flora_of_North_America":"0757eb55f2e844383d34650ea3aa577d15c2210f3893561b6694559dd9aa02e1",
}
COLLAPSE=re.compile(r"\s+")
FLOWER=r"(?:flowers?|blooms?|corollas?|petals?|tepals?|inflorescences?)"
POSITIVE=r"(?:fragrant|sweet(?:ly)?[ -]scented|scented|sweet[ -]smelling|perfumed)"
NEGATIVE=r"(?:scentless|odorless|odourless|unscented|not[ -]fragrant|without\s+(?:any\s+)?(?:scent|fragrance|odor|odour)|no\s+(?:detectable\s+)?(?:scent|fragrance|odor|odour))"
P1=re.compile(r"\b"+FLOWER+r"\b[^.;:]{0,75}?\b"+POSITIVE+r"\b",re.I)
P2=re.compile(r"\b"+POSITIVE+r"\b[^.;:]{0,50}?\b"+FLOWER+r"\b",re.I)
N1=re.compile(r"\b"+FLOWER+r"\b[^.;:]{0,75}?\b"+NEGATIVE+r"\b",re.I)
N2=re.compile(r"\b"+NEGATIVE+r"\b[^.;:]{0,50}?\b"+FLOWER+r"\b",re.I)
UNCERTAIN=re.compile(r"\b(?:probably|possibly|perhaps|reportedly|apparently|may|might)\b",re.I)
POLLEN=re.compile(r"\b(?:pollen|anther|stamen|seed|fruit|leaf|leaves|foliage|stem)\b",re.I)
SPECIES_TEXT=re.compile(r"^[A-Z][a-zA-Z-]+ [a-z][a-zA-Z-]+(?:$|\s)")

class HTMLText(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,data):self.parts.append(data)
    def get(self):return " ".join(self.parts)

def cleaned(raw):
    x=html.unescape(str(raw or ""))
    if "<" in x and ">" in x:
        h=HTMLText();h.feed(x);x=h.get()
    return COLLAPSE.sub(" ",x).strip()

def locality(el):return el.tag.rsplit("}",1)[-1]

def termname(term):return str(term or "").rsplit("/",1)[-1].rsplit("#",1)[-1].casefold()

def _escape_decoder(value,default):
    if value is None:return default
    v=str(value)
    return {"\\t":"\t","\\n":"\n","\\r":"\r","\\\"":'"',"\\'":"'","":""}.get(v,v)

def parse_meta(archive):
    names=archive.namelist()
    metas=[m for m in names if m.endswith("meta.xml")]
    if len(metas)!=1:raise ValueError("WFO_ORIGINAL_DWCA_UNIQUE_META_XML_MISSING")
    prefix=str(PurePosixPath(metas[0]).parent)
    root=ET.fromstring(archive.read(metas[0]))
    out=[]
    for element in root:
        if locality(element) not in ("core","extension"):continue
        fields={};index=None;linkkey=None;fileloc=None
        for child in element:
            tag=locality(child)
            if tag=="files":
                for loc in child:
                    if locality(loc)=="location":fileloc=(loc.text or "").strip();break
            elif tag=="field":
                term=termname(child.attrib.get("term",""))
                if term:fields[term]=int(child.attrib["index"])
            elif tag=="id":index=int(child.attrib["index"])
            elif tag=="coreid":linkkey=int(child.attrib["index"])
        if not fileloc:raise ValueError("WFO_DWCA_ROWTYPE_WITHOUT_FILE")
        candidate=str(PurePosixPath(prefix)/fileloc) if prefix!="." else fileloc
        if candidate not in names:
            if fileloc in names:candidate=fileloc
            else:raise ValueError("WFO_DWCA_META_REFERENCES_MISSING_FILE")
        out.append({"type":locality(element),"row_type":element.attrib.get("rowType",""),
              "file":candidate,"id":index,"coreid":linkkey,"fields":fields,
              "delimiter":_escape_decoder(element.attrib.get("fieldsTerminatedBy"),"\t"),
              "quotechar":_escape_decoder(element.attrib.get("fieldsEnclosedBy"),'"'),
              "headers":int(element.attrib.get("ignoreHeaderLines","0")),
              "encoding":element.attrib.get("encoding","UTF-8")})
    if len([x for x in out if x["type"]=="core"])!=1:
        raise ValueError("WFO_DWCA_PRIMARY_CORE_MISSING")
    return out

def iter_rows(archive,desc):
    if len(desc["delimiter"])!=1:raise ValueError("WFO_DWCA_UNSUPPORTED_FIELD_SEPARATOR")
    quote=desc["quotechar"]
    if len(quote)!=1:quote='"'
    with io.TextIOWrapper(archive.open(desc["file"]),encoding=desc["encoding"],errors="replace",newline="") as f:
        rd=csv.reader(f,delimiter=desc["delimiter"],quotechar=quote)
        for _ in range(desc["headers"]):next(rd,None)
        for row in rd:yield row

def field(row,fields,key):
    i=fields.get(key)
    return row[i] if i is not None and i<len(row) else ""

def canon_source_binomial(name,rank):
    s=cleaned(name)
    if not SPECIES_TEXT.match(s):return None
    words=s.split()
    if len(words)<2 or "×" in s or words[1].casefold() in {"sp","spp","cf","aff","hybrid"}:return None
    if rank and str(rank).strip().casefold() not in {"species","sp.","specie"}:return None
    if len(words)>2 and words[2].casefold() in {"var.","var","subsp","subsp.","ssp","ssp.","f.","forma"}:return None
    return strict_name(words[0]+" "+words[1])

def scent_class(text):
    txt=cleaned(text)
    if not txt:return "empty_description"
    positive=[];negative=[]
    for m in list(P1.finditer(txt))+list(P2.finditer(txt)):
        frag=m.group(0)
        if re.search(NEGATIVE,frag,re.I):continue
        if UNCERTAIN.search(frag):continue
        if POLLEN.search(frag) and "nectar" in frag.casefold():continue
        positive.append((m.start(),m.end()))
    for m in list(N1.finditer(txt))+list(N2.finditer(txt)):
        frag=m.group(0)
        if UNCERTAIN.search(frag):continue
        negative.append((m.start(),m.end()))
    return "positive_candidate" if positive and not negative else (
        "explicit_negative_candidate" if negative and not positive else
        "conflict_positive_negative" if positive and negative else "unmentioned_or_uncertain")

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

WFO_BACKBONE_202606_MD5="0e4486945cd9f7af548ca87eb9a870ed"
WFO_BACKBONE_URL="https://zenodo.org/records/20782718/files/_DwC_backbone_R.zip?download=1"
WFO_ID=re.compile(r"wfo-[0-9]{10}",re.I)

def stable_wfo_name_id(value):
    match=WFO_ID.search(str(value or "").casefold())
    return match.group(0) if match else None

def source_legacy_wfo_ids(path):
    """Original taxonID core IDs, without guessing that the name is known."""
    ids=set();count=Counter()
    with zipfile.ZipFile(path) as z:
        meta=parse_meta(z)
        core=next(x for x in meta if x["type"]=="core")
        for row in iter_rows(z,core):
            count["source_core_rows"]+=1
            key=field(row,core["fields"],"taxonid")
            if not key and core["id"] is not None and core["id"]<len(row):
                key=row[core["id"]]
            x=stable_wfo_name_id(key)
            if x:ids.add(x)
            else:count["source_non_WFO_id_rows"]+=1
    if count["source_core_rows"]<100:
        raise ValueError("ORIGINAL_WFO_ELFORAS_CORE_ID_SCAN_TOO_SMALL")
    return ids,dict(count)

def WFO_backbone_202606_crosswalk(archive_path,wanted_ids,approved):
    """Original Zenodo WFO 2026-06 data, exact WFO stable ID -> accepted species.

    No synonym or infraspecific-to-species promotion; unknown IDs stay unknown.
    """
    h=hashlib.md5()
    with Path(archive_path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):h.update(block)
    if h.hexdigest()!=WFO_BACKBONE_202606_MD5:
        raise ValueError("WFO_202606_AUTHOR_ZENODO_BACKBONE_MD5_MISMATCH")
    matches={};ambiguous=set();counts=Counter()
    with zipfile.ZipFile(archive_path) as z:
        meta=parse_meta(z)
        core=next(x for x in meta if x["type"]=="core")
        print("STAGE93_WFO_202606_BACKBONE_AUTHENTIC_META",json.dumps({
            "row_type":core["row_type"],"file":core["file"],"fields":sorted(core["fields"]),
            "original_core_id_index":core["id"],"archive_sha256":sha256(archive_path)
        },sort_keys=True),flush=True)
        fields=core["fields"]
        if "scientificname" not in fields:
            raise ValueError("WFO_202606_BACKBONE_DOES_NOT_HAVE_SCIENTIFICNAME_FIELD")
        if "taxonid" not in fields and core["id"] is None:
            raise ValueError("WFO_202606_BACKBONE_DOES_NOT_HAVE_TAXONID_FIELD")
        for row in iter_rows(z,core):
            counts["original_backbone_core_rows"]+=1
            key=field(row,fields,"taxonid")
            if not key and core["id"] is not None and core["id"]<len(row):
                key=row[core["id"]]
            wfo=stable_wfo_name_id(key)
            if not wfo or wfo not in wanted_ids:continue
            counts["original_backbone_target_ID_rows"]+=1
            sp=canon_source_binomial(field(row,fields,"scientificname"),field(row,fields,"taxonrank"))
            if not sp or sp not in approved:continue
            status=field(row,fields,"taxonomicstatus").casefold().strip()
            if status and status not in {"accepted","valid"}:
                counts["backbone_nonaccepted_usage_excluded"]+=1
                continue
            if wfo in matches and matches[wfo]!=sp:
                ambiguous.add(wfo)
            else:matches[wfo]=sp
    for key in ambiguous:matches.pop(key,None)
    if counts["original_backbone_core_rows"]<100000:
        raise ValueError("WFO_202606_BACKBONE_SOURCE_NOT_FULL_ARCHIVE")
    return matches,{
      "original_WFO_taxonomic_release":"2026-06",
      "original_WFO_backbone_DOI":"10.5281/zenodo.20782718",
      "original_backbone_Zenodo_md5":WFO_BACKBONE_202606_MD5,
      "original_backbone_ZIP_sha256":sha256(archive_path),
      "source_counts":dict(counts),
      "WFO_source_taxonIDs_requested":len(wanted_ids),
      "backbone_accepted_native_exact_matches":len(matches),
      "ambiguous_202606_name_usage_IDs_excluded":len(ambiguous),
      "no_synonym_or_fuzzy_matching_performed":True,
      "source_versioned_names_may_differ_from_regional_original_flora_year":True,
    }

def source_raw_flora(path,approved,crosswalk=None):
    # First original retrieval establishes SHA. The next (heldout) use
    # MUST pin the emitted digest before any wind model and compare it.
    count=Counter();datasets=defaultdict(set);desclens=defaultdict(list)
    with zipfile.ZipFile(path) as archive:
        meta=parse_meta(archive)
        core=next(x for x in meta if x["type"]=="core")
        taxcol=core["fields"]
        print("STAGE93_REAL_ORIGINAL_WFO_DWCA_META_SCHEMA",json.dumps([
            {"type":m["type"],"row_type":m["row_type"],"file":m["file"],
             "id":m["id"],"coreid":m["coreid"],"field_names":sorted(m["fields"])}
            for m in meta],sort_keys=True),flush=True)
        if ("scientificname" not in taxcol and not crosswalk) or core["id"] is None:
            # Source core often contains only a stable WFO taxonID; without
            # the independently versioned WFO backbone the floral text is
            # genuinely UNJOINABLE (not evidence of a scent-negative species).
            return {},{
              "archive_sha256_first_source_fingerprint":sha256(path),
              "original_rows":{"original_core_rows":0},
              "source_taxonomy_join_admissible":False,
              "source_taxonomy_join_blocker":"NO_SCIENTIFICNAME_CORE_ONLY_TAXONID",
              "matched_species_with_full_descriptions":None,
              "original_meta_schema":[{k:v for k,v in d.items() if k!="fields"}
                       |{"field_names":sorted(d["fields"])} for d in meta],
              "source_text_not_a_structured_negative_database":True,
              "not_evaluated_not_zero_scent_species":True,
            }
        taxa={}
        for row in iter_rows(archive,core):
            count["original_core_rows"]+=1
            rawname=field(row,taxcol,"scientificname")
            if rawname:
                sp=canon_source_binomial(rawname,field(row,taxcol,"taxonrank"))
            else:
                key=field(row,taxcol,"taxonid")
                if not key and core["id"]<len(row):key=row[core["id"]]
                wfo=stable_wfo_name_id(key)
                sp=crosswalk.get(wfo) if wfo and crosswalk else None
                count["source_ID_no_validated_name_crosswalk"]+=(sp is None)
            if not sp or sp not in approved:continue
            status=field(row,taxcol,"taxonomicstatus").casefold().strip()
            if status and status not in {"accepted","valid"}:
                count["original_nonaccepted_taxa_ignored"]+=1
                continue
            link=row[core["id"]]
            if link in taxa and taxa[link]!=sp:raise ValueError("SOURCE_CORE_ID_COLLISION")
            taxa[link]=sp
        count["original_core_native_matched_taxon_ids"]=len(taxa)
        descs=[x for x in meta if "description" in x["row_type"].casefold()
               or "description" in x["fields"]]
        if not descs:raise ValueError("WFO_ORIGINAL_DWCA_DESCRIPTION_EXTENSION_NOT_FOUND")
        for desc in descs:
            if desc["coreid"] is None:continue
            textcol=next((k for k in ("description","text","abstract") if k in desc["fields"]),None)
            if textcol is None:
                count["description_extension_without_plain_text_column"]+=1;continue
            for row in iter_rows(archive,desc):
                count["original_description_rows"]+=1
                if desc["coreid"]>=len(row):continue
                sp=taxa.get(row[desc["coreid"]])
                if sp is None:continue
                text=cleaned(field(row,desc["fields"],textcol))
                if not text:continue
                digest=hashlib.sha256(text.encode()).hexdigest()
                state=scent_class(text)
                datasets[sp].add((digest,state))
                desclens[sp].append(len(text))
                count["original_matched_nonempty_descriptions"]+=1
        if count["original_core_rows"]<100 or count["original_description_rows"]<1:
            raise ValueError("WFO_ORIGINAL_ARCHIVE_NOT_AUTHENTIC_DESCRIPTION_COVERAGE")
    values={}
    for sp,entries in datasets.items():
        states={state for _,state in entries}
        if "conflict_positive_negative" in states or ({"positive_candidate","explicit_negative_candidate"}<=states):
            final="conflicting_prose"
        elif "positive_candidate" in states:final="positive_candidate"
        elif "explicit_negative_candidate" in states:final="explicit_negative_candidate"
        else:final="unmentioned_or_uncertain"
        values[sp]={"scent":final,"description_n":len(entries),
                    "description_chars_median":statistics.median(desclens[sp])}
    return values,{"archive_sha256_first_source_fingerprint":sha256(path),
        "original_rows":dict(count),
        "description_extension_count":len(descs),
        "matched_species_with_full_descriptions":len(values),
        "original_meta_schema":[{k:v for k,v in d.items() if k!="fields"}
                                |{"field_names":sorted(d["fields"])} for d in meta],
        "source_text_not_a_structured_negative_database":True}

def run(nhm,wcvp,gift,flora_sources,out,wfo_backbone=None):
    traits,_=load_nhm(nhm);native,_=wcvp_regions(wcvp,traits)
    modes,_=original_gift_species(gift)
    unique=set().union(*native.values())
    if len(unique)!=55775 or len(native)!=367:
        raise ValueError("STAGE93_WCVP_NATIVE_SOURCE_COHORT_CHANGED")
    allinfo={};states=defaultdict(set);details=defaultdict(list)
    wfo_names={};crosswalk_meta={"source_absent":True}
    if wfo_backbone is not None:
        requested=set();original_id_counts={}
        for label,path in flora_sources:
            ids,sourcecounts=source_legacy_wfo_ids(path)
            requested.update(ids);original_id_counts[label]=sourcecounts
        wfo_names,crosswalk_meta=WFO_backbone_202606_crosswalk(
            wfo_backbone,requested,unique)
        crosswalk_meta["original_elfloras_taxonID_scans"]=original_id_counts
        if not wfo_names:
            raise ValueError("STAGE93_NO_ACCEPTED_NATIVE_WFO_ID_TO_SPECIES_CROSSWALK")
    for label,path in flora_sources:
        if label not in ORIGINAL:raise ValueError("WFO_UNREGISTERED_ORIGINAL_SOURCE")
        if sha256(path)!=SOURCE_SHA256[label]:
            raise ValueError("WFO_ORIGINAL_FIRST_RETRIEVED_SOURCE_ZIP_SHA_CHANGED_"+label)
        data,manifest=source_raw_flora(path,unique,wfo_names)
        allinfo[label]={"url":ORIGINAL[label],**manifest}
        for sp,entry in data.items():
            states[sp].add(entry["scent"])
            details[sp].append(entry["description_chars_median"])
    flora={}
    for sp,st in states.items():
        if "conflicting_prose" in st or ({"positive_candidate","explicit_negative_candidate"}<=st):
            c="conflicting_prose"
        elif "positive_candidate" in st:c="positive_candidate"
        elif "explicit_negative_candidate" in st:c="explicit_negative_candidate"
        else:c="unmentioned_or_uncertain"
        flora[sp]={"state":c,"median_characters":statistics.median(details[sp])}
    rows=[]
    for code,plants in sorted(native.items()):
        present=[s for s in plants if s in flora]
        counted=Counter(flora[s]["state"] for s in present)
        modes_pos=Counter(modes.get(s,"unknown") for s in present if flora[s]["state"]=="positive_candidate")
        rows.append({"TDWG_L3":code,"n_native":len(plants),"n_full_original_flora_descriptions":len(present),
            "n_flora_scent_positive_SOURCE_CANDIDATE":counted["positive_candidate"],
            "n_flora_scent_explicit_negative_SOURCE_CANDIDATE":counted["explicit_negative_candidate"],
            "n_flora_scent_conflict":counted["conflicting_prose"],
            "n_flora_scent_unmentioned_NOT_negative":counted["unmentioned_or_uncertain"],
            "n_source_scent_positive_GIFT_animal":modes_pos["animal"],
            "n_source_scent_positive_GIFT_wind":modes_pos["wind"],
            "n_source_scent_positive_GIFT_unknown":modes_pos["unknown"],
            "n_scent_positive_distinct_genera":len({s.split()[0] for s in present if flora[s]["state"]=="positive_candidate"}),
            "mainland_scope":"NOT_AUDITED_INCLUDES_ISLANDS",
            "ecological_wind_scent_effect_admissible":"NO"})
    summary=Counter(v["state"] for v in flora.values())
    output={
      "schema":"stage93_original_WFO_eFloras_full_prose_scent_SOURCE_CANDIDATES_only",
      "native_species":len(unique),"global_TDWG3_regions_INCLUDING_islands":len(native),
      "source_fingerprint_first_retrieval_not_frozen_for_future_wind_model":False,
      "source_archive_sha_frozen_before_future_climate_cue_fit":True,
      "WFO_backbone_202606_exact_ID_join":crosswalk_meta,
      "source_flora_files":allinfo,"unique_native_source_description_species":len(flora),
      "scent_lexical_species_states":dict(summary),
      "positive_candidate_species_GIFT_mode":dict(Counter(modes.get(s,"unknown") for s,v in flora.items() if v["state"]=="positive_candidate")),
      "cannot_treat_unmentioned_as_scent_absent":True,
      "does_not_measure_actual_VOC_emission_or_pollinator_airflow":True,
      "not_a_fitted_wind_signal":True,"mainland_only":False}
    out.mkdir(parents=True,exist_ok=True)
    with (out/"stage93_original_WFO_flora_scent_source_367_region_counts_INCLUDES_ISLANDS.csv").open("w",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    (out/"stage93_WFO_original_flora_source_scent_coverage.json").write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
    print("STAGE93_ORIGINAL_FLORA_FULL_TEXT_SOURCE_SCENT",json.dumps({
      "native_species":len(unique),"flora_species":len(flora),"states":dict(summary),
      "source_urls":list(ORIGINAL)}),flush=True)
    return output

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-NHM",type=Path,required=True)
    p.add_argument("--original-WCVP",type=Path,required=True)
    p.add_argument("--original-GIFT",type=Path,required=True)
    p.add_argument("--original-WFO-202606-backbone-ZIP",type=Path)
    p.add_argument("--original-Flora-of-China-ZIP",type=Path,required=True)
    p.add_argument("--original-Flora-of-North-America-ZIP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    run(a.original_NHM,a.original_WCVP,a.original_GIFT,
      [("Flora_of_China",a.original_Flora_of_China_ZIP),
       ("Flora_of_North_America",a.original_Flora_of_North_America_ZIP)],a.outdir,
       wfo_backbone=a.original_WFO_202606_backbone_ZIP)
