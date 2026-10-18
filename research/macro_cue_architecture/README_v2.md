# Adaptive-gain empirical macro stage 0 — directly audited source, 2026-10-18

This package advances the earlier theoretical 6-state matched-cue result and source registry to an *actual, live-processed* 30-study raw plant–pollinator record audit. No real sensory routeability estimate is claimed.

Start with `stage0/README.md`, `validation/schwarz_stage0_remote_live_20261018.json` and `stage0/REPRODUCTION_GATES.md`.

To rerun the source analysis on a network-connected machine, download the exact original source from https://zenodo.org/records/4744654 (Schwarz et al. 2021, https://doi.org/10.5061/dryad.qz612jmbp) and verify its MD5. Then:

```
python -m pytest -q tests
python stage0/schwarz_stage0.py --csv OIK-07303_database.csv --require-md5 --study-cluster-model --output validation/schwarz_local_recomputed.json
python verify_matched_cues.py
```

Source time and sampling grain can be modified by the compiling authors for seasonal alignment. Observation denominators/zeros must be reacquired from each original study before fitting detection-corrected turnover. Never report row-rarity standardization as observer effort standardization. See source registry for other 15 datasets and explicit unresolved download status.
