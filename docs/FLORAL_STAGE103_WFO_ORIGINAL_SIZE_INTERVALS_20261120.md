# Stage103 — Recover WFO whole-flower size as intervals rather than invented point diameters

**2026-11-20 JST.** Correct semantic recovery from ORIGINAL source botanical prose, not a confirmed ecological size response or gust signal.

## Motivation: a genuine source interpretation bug

Original Stage100 WFO full-Flora-China/FNA botanical descriptions generated 237 source-labelled *whole flower diameter textual candidates*, 58 corolla-only references, and a deduplicated potential 337 species when combined with 104 independently source-labelled AusTraits flower diameters. Subsequent Stage102 original source audit discovered a major source syntax issue: original botanical prose commonly expresses a measurement as a RANGE such as “8--9 cm in diam”. Earlier grammar could take 9 cm as a point, falsely converting a real range into an invented singleton. Stage102, which independently rechecked the full original archive with an appropriately strict single-number grammar, retained only **34 of 237 (14.3%)** candidates as direct *lexical* singletons; **186** original candidate species contain range/upper-limit parsing risk. The correct interpretation is **not** that all other measurements are irrelevant—ranges and upper limits are real partial information.

## Source-level evidence semantics

- A genuine numerical point statement such as "Flowers 7 mm diam" is represented as an exact lexical source candidate [7, 7] mm. It is **not** a validated hand measurement.
- A genuine original flower-wide range statement such as "Flowers 8--9 cm in diam" is represented as [80, 90] mm, NOT a single value of 90 mm and NOT automatically a midpoint 85 mm.
- A source upper-only statement such as "Flowers to 2 cm in diam" is represented as a left-censored positive floral size (0, 20] mm. The lower endpoint is UNKNOWN (null), not zero observed flower diameter.
- Width of corolla, petal, tube, flower head, inflorescence, fruit, leaf or peduncle is not whole-flower diameter. Distinguish source descriptions of these other organs.
- Multiple source descriptions may report several intervals or points. Their overall envelope is an observed-source morphological VALUE ENVELOPE, **not a statistical confidence interval**, a population sampling confidence bound, or an independently measured species trait mean. Source span exceeding 5-fold is flagged for source review.
- No absent description can be interpreted as flower diameter zero. No original source size range is imputed to a single global value without a declared separate interval-censored model.

## Original source files and fixed species/geo sample

This stage explicitly re-reads, validates and retains SHA/MD5 provenance for:
- Stage100 original verified WFO species candidate ledger ZIP artifact 14541288164 SHA256 06c370061a4c069038aaf11ecd59a423fb00cb051db6ec67632e316ce9d2ebd4, exactly the **237** whole-flower source candidates (the separate 58 corolla-only candidates are excluded).
- Stage98B original geometry-only contact-filtered **72 mainland exploration / 37 unchanged holdout** region split artifact 14537927849 SHA256 8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7.
- Original NHM floral source and Kew WCVP accepted native 55,775 source species/367 TDWG3 regions, original independent file SHA256 checked.
- WFO Flora of China and Flora of North America original DwC-A archives, SHA256 4c0b89280efdcfd0ef8dc753cca5d63566ddf8c34542b0bb4a78cdce799b63a9 and 0757eb55f2e844383d34650ea3aa577d15c2210f3893561b6694559dd9aa02e1 respectively.
- WFO June-2026 original scientific-name taxonID backbone, Zenodo author MD5 0e4486945cd9f7af548ca87eb9a870ed.

Do not invent a new taxonomic matching rule or alter the Stage98B geographic holdout after observing any wind, petal, scent or Bombus outcomes. Recovered size data have the original source provider and accepted species key; the original botanical prose itself is NOT redistributed.

## Empirical source support and claim ceiling

The new outputs distinguish (a) bounded source interval species, (b) only upper-limit source species, (c) single-number lexical source species, and (d) descriptions that cannot be recovered with the declared conservative grammar. The overlap of source ranges and singleton evidence is reported rather than summed as if disjoint. The 37 holdout regions and 72 train regions are recomputed for source *interval availability*, not a wind effect.

The same floristic source species can occur in many TDWG3 regions; this is not independent evolutionary phenotype replication. A future hierarchical interval-censored log-flower-size source model would explicitly integrate the source intervals, clade composition, botanical ascertainment, and 1991–2020 **regional land-area weighted** 10m gust daily >15m/s exposure. Such an analysis is NOT fitted here because original CDS hourly ERA5 10fg vs derivative source semantics and polygon-wide land-cell aggregation are still missing.

The source prose extraction remains automatically annotated and not independently manually validated. The number of bounded intervals recovered is source-availability evidence only; it cannot validate an insect perception signal.

## Implementation

- research/floral_macro_stage103/original_WFO_wholeflower_size_intervals.py
- research/floral_macro_stage103/test_original_WFO_wholeflower_size_intervals.py
- .github/workflows/floral-stage103-original-WFO-size-intervals.yml

**Real interval counts pending source-authenticated execution.** Failure to retrieve official files or verify original byte hashes stops numerical claims; no synthetic fallback.
