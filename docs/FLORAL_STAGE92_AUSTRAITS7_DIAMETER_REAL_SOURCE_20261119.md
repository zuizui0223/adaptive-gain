# Stage92 — Original AusTraits v7.0.0 flower diameter source audit

**Date: 2026-11-19 JST. Status: original-source opportunity, NOT a fitted wind effect.** Stacked on Stage91 Draft PR #170; main untouched.

## Scope

Stage91 original NHM compact extraction supplies no source flower diameter, no validated floral fragrance and 906 positive lexical marking candidates among 55,775 globally native source plants. Missing source fields are not biological zeroes.

Original independent AusTraits 7.0.0 public archive has dataset DOI 10.5281/zenodo.15718081, versioned ZIP, SHA256 2995fb9e5eebf9271f9241b5a6c2e2cbb7b45e8eda5ce4db43c14c68f95e2f3f. The original eFLOWER_Dun_2022 dataset reports flower_diameter, unlike the distinct NHM petal width. This is a valid discovery target, pending original byte and codebook verification.

## Pre-source extraction contract

1. Verify byte SHA256 of complete source ZIP and its CSV long-format column schema, including source unit and source dataset when present.
2. Admit only original exact flower_diameter numeric measurements with explicit mm/cm/m units. Reject/inventory unspecified units, vague ranges, implausible values and zeroes; do NOT derive diameter from length or petal width.
3. Match source species exactly to the pinned NHM–Kew WCVP native species baseline 55,775 species across 367 TDWG3 regions. Repeated records within a dataset are summarized to a median; dataset-level medians are then summarized to a species-level median. Repeated species across regions are not independent evolutionary evidence.
4. Record unique source-matched species, genus and WCVP family support, native-region coverage, source-unit breakdown and GIFT animal/wind/unknown pollination modes. No missing species is assigned zero diameter or a missing pollen mode inferred from other traits.
5. Derived-only receipt and regional count tables will include islands for coverage *only*. Mainland eligibility and common holdout must be established by separately verified regional geometry before regressions.

A source field labelled flower_diameter does NOT automatically measure display diameter as perceived in a particular bee view, optical detection distance, flower opening stage or attraction. The codebook and source type need review before a future far-distance signalling association. AusTraits is Australian-biased, so global region source gaps are expected and must be reported.

## Frozen non-inferences

No floral scent data, actual bee choice/learning, wind plume, landing, evolutionary origin, causal mediation or 1991–2020 ERA5 10m gust period is measured here. The planned wind variable remains fraction of daily maximum gust **strictly >15m/s** across months where climatological 2m temperature **strictly >5°C**. Difference from Stage78 source-month weather and WorldClim mean wind must be retained.

## Source code and tests

- research/floral_macro_stage92/austraits7_flower_diameter_source_audit.py
- research/floral_macro_stage92/test_austraits7_flower_diameter_source_audit.py
- .github/workflows/floral-stage92-original-Austraits7-diameter.yml

**Empirical n / coverage:** PENDING ORIGINAL CI; do not insert counts until a successful logged source run.
