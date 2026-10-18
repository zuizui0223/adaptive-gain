# Macro ecology — stage 0 source audit, not a routeability effect estimate

This is an independent empirically sourced companion to the exact **six-world cue-architecture witness**. It intentionally DOES NOT estimate insect cognition, adaptive sensing, or network rewiring from positive-only flower-visit logs.

**Primary source:** Schwarz et al. (2021), OIK-07303 original 30-study plant–pollinator records, https://doi.org/10.5061/dryad.qz612jmbp, preserved public Zenodo mirror https://zenodo.org/records/4744654. Credit all original studies listed in the original-studies workbook before any derived-publication reuse. Check MD5 reported on Zenodo `7a70c3e2356611b0871c163a2f9aed4a` against the actual bytes before using the results.

## Actual results of this turn (hosted raw-text processing)

The 18,987,400-character source CSV was fetched directly and parsed on October 18 2026, rather than merely described from its abstract. It contains 150,914 row records from 30 studies, 343 study–site labels and 3,270 site-days (all grains). See `../validation/schwarz_stage0_remote_live_20261018.json` for the full observed counts and exploratory statistics, **not a claim that the raw CSV bytes are bundled here**.

Strict day-scale comparisons (adjacent date, 1–30 day gap, ≥20 recorded positive visit rows each date, `freq=1` for both days) yield 479 date pairs in 105 study–site IDs and 16 studies. Mean observed link-set Jaccard dissimilarity = 0.810. Visit-row rarefaction to 20 positive rows per date with deterministic Mulberry32 draws, 80 replicates per comparison, yields 0.851. Rarefaction is NOT an effort/detection adjustment.

An exploratory within-study OLS of raw observed dissimilarity against `log(1+gap_days)` and `log(record_count_ratio)` gave coefficients 0.0568 and 0.0413 with study-clustered SEs 0.0080 and 0.0159. After rarefaction they were 0.0493 and 0.0185 with SEs 0.0062 and 0.0126. The stricter SITE-fixed-effect sensitivity gave a time-gap coefficient 0.0570 (study-clustered SE 0.0103) on raw link sets and 0.0474 (SE 0.00693) after equal-row subsampling; record-count imbalance had a 0.0215 estimate (SE 0.0169) after subsampling. These remain exploratory comparisons across 105 sites and 16 study clusters. All comparisons are **observed incidence**, not latent ecological link occupancy. Standard errors from 16 study clusters are approximate; endpoints overlap within sites and the original study dates may be re-centered. Do not reinterpret link differences as evolution of sensory adaptation.

## Exact reproduction

Download `OIK-07303_database.csv` via Zenodo mirror and verify the MD5. Alternatively the script has a guarded optional `--download` flag. It will never overwrite an existing raw file.

```bash
python -m pip install numpy scipy pytest
python -m pytest -q tests/test_schwarz_stage0.py tests/test_study_cluster_model.py
python stage0/schwarz_stage0.py --csv /path/to/OIK-07303_database.csv \
  --require-md5 --output validation/schwarz_recomputed.json \
  --study-cluster-model
```

The same source rows are kept (including exactly repeated positive visits). The returned JSON contains all 479 pair-level observations and study-stratified means for independent review. Source CSV itself is not repackaged: retrieve the publisher's original instead of trusting a relayed copy.

## Scientific next go/no-go

Stage 0 PASS: original date/plant/pollinator records read; 16 independent studies have prospective repeated positive-visit comparisons.

Stage 1 NOT PASS: no common observation-effort denominator or independent zero-visit frame across these 16 study sources; need each original protocol or UK PoMS FIT zero-preserving count data. Their source sampling intervals, coverage and effort must be reconciled before an inferential publication.

Stage 2 NOT PASS: no measured animal-specific query order, independent resource reward or decision costs; need independent cue calibration plus factorial animal experiment. The six-world witness is a theoretical target, not an observable response in these records.

This file intentionally separates a genuine **real raw macro audit** from a **prospective causal cue-topology hypothesis**.
