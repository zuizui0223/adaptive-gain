"""Source-free Stage90B paired geographic block and regional hue reweight tests."""
from __future__ import annotations
import tempfile,unittest,zipfile
from pathlib import Path
import numpy as np,pandas as pd
from source_reweighted_GIFT_hue_wind_Bombus_spatial_pairs import (
  input_range_table,adjusted_mode_outcomes,paired_geo_bootstrap,
  HUES_SEQUENCE if False else input_range_table
)
