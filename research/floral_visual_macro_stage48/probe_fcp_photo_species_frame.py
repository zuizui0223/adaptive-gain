"""Stage48 original FCP species-photo opportunity schema audit, not a pattern classifier.

Source source is user's own original FCP image measurement project, 4,475
species and 447,500 photographed flower attempts (not all classifiable).
The immutable species-level ledger is audit input only; all true UV/petal
pattern states remain UNKNOWN until inspected in real original images.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
import urllib.request

REPO_COMMIT="c45a95420a96abfb3fdb8e9ad1a37c75288c63fb"
SOURCE_GIT_BLOB_SHA1="95ec1140a622ae11c816bcfbd1d3b33150ec104a"
SOURCE_PATH="results/fcp_np_all4475_unified_species_ledger_20261021.csv"
URL="https://raw.githubusercontent.com/zuizui0223/fcp/"+REPO_COMMIT+"/"+SOURCE_PATH
MAX_BYTES=8_000_000
EXPECTED_SPECIES_ROWS=4475

def _sha1_blob(data):
    return hashlib.sha1(
        b"blob "+str(len(data)).encode()+b"\x00"+data
    ).hexdigest()

def get_original_fcp_ledger():
    request=urllib.request.Request(URL,headers={
        "User-Agent":"adaptive-gain-stage48-FCP-pinned-4475-species-probe/2026",
        "Accept":"text/csv,application/octet-stream"
    })
    with urllib.request.urlopen(request,timeout=60) as response:
        blob=response.read(MAX_BYTES+1)
    if len(blob)>MAX_BYTES or _sha1_blob(blob)!=SOURCE_GIT_BLOB_SHA1:
        raise ValueError("NO_GO_FCP_ORIGINAL_4475_SPECIES_LEDGER_SOURCE_DRIFT")
    return blob

def profile(blob,expected_rows=EXPECTED_SPECIES_ROWS):
    if not isinstance(blob,bytes):
        raise ValueError("NO_GO_NOT_FCP_SOURCE_BYTES")
    reader=csv.DictReader(io.StringIO(blob.decode("utf-8-sig"),newline=""))
    fields=reader.fieldnames or []
    if not fields or len(set(fields))!=len(fields):
        raise ValueError("NO_GO_FCP_SOURCE_FIELD_SCHEMA_DUPLICATE")
    rows=list(reader)
    if len(rows)!=expected_rows:
        raise ValueError("NO_GO_FCP_SPECIES_COUNT_CHANGED")
    names=[x for x in fields if any(tag in x.lower() for tag in
       ("species","taxon","scientific","photo","classif","roi","source","image","cohort"))]
    present={f:sum(bool((x.get(f) or "").strip()) for x in rows) for f in names}
    return {
      "status":"SOURCE_VERIFIED_FCP_4475_SPECIES_LEDGER_SCHEMA_ONLY",
      "source_repo_commit":REPO_COMMIT,
      "source_file":SOURCE_PATH,
      "source_Git_blob_sha1_verified":_sha1_blob(blob),
      "source_full_CSV_SHA256":hashlib.sha256(blob).hexdigest(),
      "species_ledger_rows":len(rows),
      "n_fields":len(fields),
      "all_column_names":fields,
      "candidate_species_and_photo_fields":names,
      "nonblank_counts_in_candidate_fields":present,
      "first_three_records_selected_field_previews":[
        {f:(x.get(f) or "")[:120] for f in names[:12]}
        for x in rows[:3]],
      "not_measured_uv_or_visible_guide_presence":True,
      "not_a_Bombus_or_plant_trait_geographic_association":True
    }

def main():
    x=profile(get_original_fcp_ledger())
    d=Path("stage48_source_probe")
    d.mkdir(exist_ok=True)
    (d/"fcp_4475_species_photo_opportunity_source_schema.json").write_text(
        json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+"\n",
        encoding="utf8")
    print("STAGE48_ORIGINAL_FCP_GLOBAL_PHOTO_SPECIES_FRAME",json.dumps(x,sort_keys=True))

if __name__=="__main__":
    main()
