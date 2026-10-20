"""Detect the actual independent wind/interspecific interaction unit of observation.

Weschler 2024/2025 Zenodo original. No animal interaction effects are fitted
unless true partner identity, weather replication and outcome exposure exist.
"""
import argparse,hashlib,io,json
from pathlib import Path
import pandas as pd

MD5="9bcab4765c4fe5a9edaaf096867caf5b"
def audit(filename):
    raw=Path(filename).read_bytes()
    if hashlib.md5(raw).hexdigest()!=MD5:raise ValueError("SOURCE_MD5_MISMATCH")
    d=pd.read_csv(io.BytesIO(raw),encoding="utf-8-sig")
    cols={"Site","Date","WindSpeed","DistanceTurbine_m",
          "DifferentSpeciesInteraction","SameSpeciesInteraction"}
    if not cols<=set(d):raise ValueError("MISSING_REQUIRED_FIELDS")
    block=d.groupby(["Site","Date"],dropna=False)
    winds=block.WindSpeed.nunique()
    if d.WindSpeed.isna().any():raise ValueError("UNRECORDED_WIND")
    event_count=int(pd.to_numeric(d.DifferentSpeciesInteraction).sum())
    return {"source":"10.5281/zenodo.15447016",
      "original_md5":MD5,"sha256":hashlib.sha256(raw).hexdigest(),
      "behavior_rows":len(d),"site_count":int(d.Site.nunique()),
      "independent_weather_site_dates":int(len(winds)),
      "within_site_date_wind_variation":int((winds>1).sum()),
      "interspecific_flag_rows":event_count,
      "conspecific_flag_rows":int(pd.to_numeric(d.SameSpeciesInteraction).sum()),
      "turbine_distance_is_site_invariant":bool((d.groupby("Site").DistanceTurbine_m.nunique()==1).all()),
      "interspecific_partner_names_measured":False,
      "gate":"NO_GO_INTERSPECIFIC_WIND_MEDIATION",
      "reason":"only five interspecific flags, no identified partners; wind repeated at site-date level"}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--source",required=True);p.add_argument("--out",default="weschler_no_go.json")
    a=p.parse_args();r=audit(a.source)
    Path(a.out).parent.mkdir(exist_ok=True,parents=True)
    Path(a.out).write_text(json.dumps(r,indent=2))
    print("WESCHLER_DIRECT_INTERSPECIFIC_GATE",json.dumps(r))
