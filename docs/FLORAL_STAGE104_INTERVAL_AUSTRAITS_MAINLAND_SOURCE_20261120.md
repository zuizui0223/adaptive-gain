# Stage104 — Original AusTraits measured floral diameter vs WFO 2026 botanical size intervals

**2026-11-20 JST.** Genuine species-level source availability and correctness gate, **not an estimated gust effect**. Draft stacked onto Stage103 #182; main unchanged.

## Why the source union must be recomputed

Original AusTraits v7.0.0 supplied 104 actual source-labelled flower_diameter species, matched strictly to original WCVP native taxa. Original WFO eFloras full botanical treatments supplied 237 whole-flower size *textual* candidate taxa; naive Stage101 availability union was 337 distinct taxa after 4 exact species overlaps. However the Stage102 independent grammar uncovered a real botanical source expression bug: double hyphens encode source size intervals (e.g. 8--9 cm) and upper-bound-only expressions are not singleton measurements.

Verified Stage103 genuine WFO original source yielded **124** accepted native species with source-bounded two-sided intervals, **57** upper-only species, **34** species with exact textual singleton clauses, and **212** distinct source species with at least one recovered numerical size bound. A further 25 of the 237 source candidates lack an eligible source expression under the frozen Stage103 parser. Some categories overlap and cannot be summed.

**This project now recomputes the accurate source-available size opportunity from independent original AusTraits 104 and recovered WFO 212, minus actual exact matching species**. The previous 337 source-available WFO unreviewed size candidate count must NOT be described as a 337 species numerical measurement dataset.

## Source and morphological grade rules

- **A — measured-source label**: original AusTraits 7.0.0 explicitly published flower_diameter (unit-normalised mm), 104 accepted WCVP native taxa, SHA 2995fb9e5eebf9271f9241b5a6c2e2cbb7b45e8eda5ce4db43c14c68f95e2f3f. Source value itself need not correspond to bee viewing geometry or exact source floral developmental stage.
- **B — unreviewed botanical original size bound**: 212 accepted WFO species with a valid numerical dimension in source text, where two-sided intervals [lower,upper], exact singleton [value,value], and upper-only bounds (unknown lower, upper] stay distinct. **NEVER** treat a botanical interval upper endpoint or midpoint as directly observed, nor impute a lower limit of zero as a measured trait.
- **B2 — two-sided source interval**: 124 distinct accepted species with at least one actual source range.
- **B3 — upper-bound only**: 57 distinct accepted species with no source lower bound.
- **B4 — exact textual singleton candidate**: 34 distinct accepted species with one or more original grammatical point phrases. Includes source report, not independent manual verified measuring.
- **C — corolla width only**: original 58 WFO corolla-only width species remain excluded from the A-or-B full-flower diameter union.

The prior Stage103 source artifact has *237* rows (also includes 25 with no eligible source bound), and is SHA-locked to the independently successful Actions #44662510103, derived ZIP artifact 14595854235 SHA256 95fb60fa049ed4e79673e1f1dc12aaddb97f5fadd1dc27f905d31dd25b8cfe90.

## Geographic cohort, source lineage and disagreement

Keep independently source-frozen Stage98B **72** original continental contact-free exploration and **37** unchanged holdout TDWG3 regions, artifact 14537927849 SHA256 8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7. Restore original WCVP+NHM source of 55,775 accepted native plants and repeat exact species identity joins. Identical species across regions cannot count as independent evolutionary transitions. A measured AusTraits source report and WFO source interval for one exact taxon may cover different populations, methods or developmental stages; agreement is descriptive, not manual quality validation.

For each source grade and original geographic fold report: number of distinct globally accepted source taxa, distinct taxa in train and holdout, taxa new in holdout, truly new genera, and number of mainland regions with ≥10 source species. Source reporting, lineage, optical signal detectability and original exact ERA5-CDS hourly 10fg area-weighted exposure remain separate prerequisites. Two original Acaena source-wide >5-fold WFO range envelopes are flagged; preserve measured-source A even if a WFO interval is excluded as suspicious.

The 37 heldout regions are not yet shown to be phylogenetically independent; Stage99 found AusTraits size records have 64.8% exact species reuse across train/holdout. Native TDWG3 botanical flora are author lists, not field measurements of within-region flower sizes.

## Output and claim ceiling

GitHub Actions independently restores and SHA-checks WFO Stage103, WCVP native species, NHM source, original AusTraits v7, and Stage98B geo. It writes only derived source grade counts, source-overlap consistency diagnostics and mainland 109-region data-availability table. No botanical copyrighted full text redistribution. No model fitting of gust and floral size, no actual scent flux, visual receptor detectability, bee learning, landing or fitness inference.

**Empirical source-union values beyond the already verified A=104/B=212 have not been declared until genuine original Stage104 workflow success.**

Code: research/floral_macro_stage104/graded_Austraits_and_WFO_interval_mainland_source.py and tests, workflow .github/workflows/floral-stage104-original-size-interval-Austraits-mainland.yml.
