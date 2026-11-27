"""Source admission of Filipiak et al. 2022 Ecology dataset, 10.5281/zenodo.5862277.
The source contains repeated measurements and mixed units; no numeric trait
aggregation until the original column definitions and citation semantics are checked.
"""
import argparse,csv,hashlib,json,re,sys
from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'floral_macro_stage119'))
from budgeted_reward import members,read_table,HASHES,species
MD5='22c3c9ed5da88307a34fb7c213ae4fe9'
def run(source,author):
    raw=source.read_bytes()
    if hashlib.md5(raw).hexdigest()!=MD5:raise ValueError('Zenodo published file MD5 drift')
    for enc in ['utf-8-sig','cp1252']:
        try:text=raw.decode(enc);break
        except UnicodeDecodeError:continue
    else:raise ValueError('source encoding unknown')
    sep=csv.Sniffer().sniff(text[:16000],delimiters=',;\t').delimiter
    d=pd.read_csv(source,sep=sep,encoding=enc,low_memory=False,dtype=str)
    exact=members(author)
    if any(hashlib.sha256(exact[k]).hexdigest()!=HASHES[k] for k in HASHES):raise ValueError('author morphology/reward source SHA drift')
    m,_=read_table(exact['morphology'],'morphology');n,_=read_table(exact['nectar'],'nectar');p,_=read_table(exact['pollen'],'pollen')
    norm=lambda x:' '.join(re.sub(r'[^a-z0-9]+',' ',x.lower()).split())
    candidates=[k for k in d.columns if norm(k) in {'species','species name','plant species','scientific name','taxon','taxon name','latin name','plant name','species scientific name','species latin name','scientific species name','species accepted name'}]
    co={}
    for k in candidates:
        names=set(d[k].map(species).dropna())
        co[k]={'strict_unique_species':len(names),'with_original_morphology':len(names&set(m.species)),'with_original_positive_nectar':len(names&set(n.species)),'with_original_pollen':len(names&set(p.species)),'with_morphology_new_to_both_reward_tables':len(names&set(m.species)-set(n.species)-set(p.species))}
    cols=[{'name':k,'nonmissing_rows':int(d[k].notna().sum()),'distinct_nonmissing_values':int(d[k].nunique()),'source_value_examples':d[k].dropna().drop_duplicates().head(5).tolist() if re.search('unit|ref|source|species|country|site|year|latitude|longitude|pollen|nectar|sugar',k,re.I) else []} for k in d.columns]
    return {'doi':'10.5281/zenodo.5862277','published_md5_verified':True,'sha256':hashlib.sha256(raw).hexdigest(),'source_rows':len(d),'source_columns':len(d.columns),'encoding':enc,'delimiter':sep,'explicit_species_candidate_headers':co,'columns':cols,'no_claim_of_independent_studies_or_species_until_reference_overlap_audit':True,'no_reward_value_model_before_unit_provenance_review':True}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    r=run(a.source,a.author);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=False)+'\n');print('STAGE122_NEW_REWARD_SOURCE',json.dumps(r,ensure_ascii=False,sort_keys=True))
