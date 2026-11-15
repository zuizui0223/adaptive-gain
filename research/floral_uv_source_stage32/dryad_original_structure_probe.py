"""Stage32: original Dryad UV-bullseye workbook *STRUCTURE* and provenance.

No biological effect estimates are generated; independent sample units,
treatment denominators and covariance need original column-level semantics.
This audit reads ZIP container metadata and workbook sheet-name metadata,
not workbook cells or numerical sheet statistics.
Raw Dryad Excel original is never committed or redistributed in artifacts.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import zipfile

DOI='10.5061/dryad.bm558'
API_DOWNLOAD='https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.bm558/download'
EXPECTED_ORIGINAL='FEKoskiSF2.xlsx'
MAX_BYTES=1_500_000
MAX_WORKBOOK_BYTES=500_000
MAIN='http://schemas.openxmlformats.org/spreadsheetml/2006/main'


def _hash(raw):
    return hashlib.sha256(raw).hexdigest()


def inspect_archive(package_raw):
    if not isinstance(package_raw,bytes) or not package_raw.startswith(b'PK'):
        raise ValueError('NO_GO_NOT_DRYAD_ZIP')
    if len(package_raw)>MAX_BYTES:
        raise ValueError('NO_GO_DRYAD_PACKAGE_OVERSIZE')
    try:
        with zipfile.ZipFile(io.BytesIO(package_raw)) as f:
            names=[z.filename for z in f.infolist() if not z.is_dir()]
            match=[n for n in names if Path(n).name==EXPECTED_ORIGINAL]
            if len(match)!=1:
                raise ValueError('NO_GO_ORIGINAL_WORKBOOK_MISSING_OR_DUPLICATE')
            entry=f.getinfo(match[0])
            if entry.file_size>MAX_WORKBOOK_BYTES:
                raise ValueError('NO_GO_ORIGINAL_WORKBOOK_TOO_LARGE')
            raw=f.read(match[0])
    except (zipfile.BadZipFile,RuntimeError) as err:
        raise ValueError('NO_GO_INVALID_DRYAD_ARCHIVE') from err
    return {'status':'ORIGINAL_DRYAD_ARCHIVE_AND_WORKBOOK_STRUCTURALLY_PRESENT',
            'doi':DOI,'api_download_endpoint':API_DOWNLOAD,
            'package_sha256':_hash(package_raw),
            'package_bytes':len(package_raw),
            'source_package_filenames':names,
            'original_workbook_name':EXPECTED_ORIGINAL,
            'original_workbook_sha256':_hash(raw),
            'original_workbook_bytes':len(raw),
            'original_workbook_structure':_inspect_workbook_shell(raw),
            'experimental_effects_extracted':0,
            'independent_array_count_inferred_from_sheet_rows':False,
            'source_variances_extracted':False,
            'original_excel_redistributed':False,
            'not_biological_meta_result':True}


def _inspect_workbook_shell(raw):
    """Sheet NAME/relationship metadata only; no worksheet cells read."""
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as f:
            names=set(f.namelist())
            if 'xl/workbook.xml' not in names:
                raise ValueError('NO_GO_NOT_AN_OOXML_XLSX')
            root=ET.fromstring(f.read('xl/workbook.xml'))
            sheets=root.findall('.//{%s}sheets/{%s}sheet'%(MAIN,MAIN))
            result=[s.attrib.get('name','') for s in sheets]
            if not result or not all(result) or len(set(result))!=len(result):
                raise ValueError('NO_GO_SHEET_NAMES_INVALID')
            return {'sheet_count':len(result),'sheet_names':result,
                    'is_OOXML_xlsx':True,
                    'cell_values_or_headers_examined':False,
                    'independent_experimental_unit_NOT_ESTABLISHED':True}
    except (zipfile.BadZipFile,ET.ParseError) as err:
        raise ValueError('NO_GO_INVALID_ORIGINAL_WORKBOOK_CONTAINER') from err


def fetch_original_archive():
    r=urllib.request.Request(API_DOWNLOAD,headers={
        'User-Agent':'adaptive-gain-floral-source-audit/20261115',
        'Accept':'application/zip,application/octet-stream'
    })
    with urllib.request.urlopen(r,timeout=30) as response:
        status=response.status
        data=response.read(MAX_BYTES+1)
        final_url=response.url
    if status!=200:
        raise ValueError('NO_GO_UPSTREAM_HTTP_STATUS')
    if not final_url.startswith('https://'):
        raise ValueError('NO_GO_UNEXPECTED_UNENCRYPTED_REDIRECT')
    return data


def run(archive_bytes=None):
    if archive_bytes is None:
        try:
            archive_bytes=fetch_original_archive()
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,
                ConnectionError,OSError) as err:
            return {'status':'NO_GO_DRYAD_UPSTREAM_DOWNLOAD_UNAVAILABLE',
                    'source_doi':DOI,
                    'failure_type':type(err).__name__,
                    'original_workbook_acquired':False,
                    'experimental_effects_extracted':0,
                    'no_biological_claim':True,
                    'not_an_inference_from_fake_source':True}
    return inspect_archive(archive_bytes)


def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--input-archive',default=None)
    ap.add_argument('--out',default='stage32_original_source_receipts')
    args=ap.parse_args(argv)
    if args.input_archive:
        result=run(Path(args.input_archive).read_bytes())
    else:
        result=run()
    directory=Path(args.out);directory.mkdir(parents=True,exist_ok=True)
    (directory/'stage32_dryad_bm558_workbook_structure.json').write_text(
        json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],
                      'workbook_acquired':result['status'].startswith('ORIGINAL_DRYAD_'),
                      'sheet_names':result.get('original_workbook_structure',{}).get('sheet_names'),
                      'experimental_effects_extracted':0},sort_keys=True))


if __name__=='__main__':
    main()
