# Stage99 — Exact plant species recurrence across mainland training and holdout regions

**2026-11-19 JST.** Scientific task: audit whether the original Stage98B geographical validation groups also represent novel floral taxa. It is a **source-based identity diagnostic**, not a floral cue × wind association or a model of independent evolution.

## Frozen region groups

The independently source-verified Stage94 mainland original consists of 125 strict mainland TDWG3 regions (island 120, mixed 122 excluded). Stage98A found 22 source-original train/holdout geometry contacts (20 overlaps and 2 touches). Stage98B excluded only the 16 contacting exploration regions, retaining **72 noncontact exploration regions and 37 original holdout regions unchanged** (independent source artifact 14537927849, SHA256 `8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7`). The 100-km physical buffer and plant-phylogeny independence have NOT been established.

## Original source identity audit

Rather than extrapolating from regional counts or reusing hue association outcomes, Stage99 reads actual source species names:
- Original NHM 59,369 botanical descriptions, source CSV SHA256 `b81ab96a2883e2b2e7f254a9e7ab62a34afaa0dfe62f0062d1677ba852dc686a`.
- Kew WCVP accepted native species × original 367 TDWG3 regional distributions, archive SHA256 `d32ea2b3a85e489b14e83bcc9eae7274532e1d113753f7be290d4b2dfde573fa`.
- GIFT independently qualified v3.2 animal- versus wind-pollination modes, source ZIP SHA256 `074a52323ba835201043a3a5980cc2b2d0ff79878e83bc9be19511ae83a1c0e8`.
- AusTraits 7.0.0 original authored flower_diameter measurements, archive SHA256 `2995fb9e5eebf9271f9241b5a6c2e2cbb7b45e8eda5ce4db43c14c68f95e2f3f`, strict 104 WCVP native species.
- WFO original Flora of China/North America botanical description extracted and accepted-name-verified source, 27,899 taxa, 420 positive fragrance lexical reports/105 explicit negative reports, source ZIP SHA256 `eb32786c6464a6edecd7ff0d12e61762cdb107f3082124066aadcc03292dd88e`.

For each trait (all native species, positive *lexical* floral markings, source-labelled flower diameter, fragrance lexical positive, fragrance lexical negative, and independently source-qualified animal/wind pollination mode), count **distinct source species** in contact-free training and unchanged holdout. Identify exact species shared between folds and holdout-exclusive species. Distinguish a novel species within a previously present genus from a genuinely new source genus.

Because a WCVP source species often occupies numerous TDWG3 regions, a holdout region may be geographically new but contain an already observed species with an unchanged original trait statement. This is not proof of a recurrent evolutionary transition nor an independent validation of species-level signal change. Source name novelty does not establish a phylogenetic transition; a new genus is not a direct measure of evolutionary independence.

## No unsupported biological claims

The source positive marking lexicon has **no verified negative reference set**. Fragrance positive and explicit negative are unreviewed source phrases rather than measured VOC emission states, and no matched-source plant has proven local nocturnal pollination, bee plume tracking or learning. The flower_diameter source label is not necessarily an optically visible display diameter at bee-view distance. None of the Stage99 results contains a causal wind effect or an ERA5 area-weighted source regional exposure. Original Stage95/97 results remain limited to 50 regional *point* samples.

A nonzero source reuse fraction is a warning about apparent biogeographic validation, not evidence that every ecological pattern is invalid. A future wind×signal model could report both geographically blocked extrapolation and taxon-heldout extrapolation if original cross-family, independently measured trait data become available. These require separate eligibility and pre-outcome splits; never retroactively select results by coefficient sign.

## Code and execution

- `research/floral_macro_stage99/original_three_cue_species_holdout_source_leakage.py`
- `research/floral_macro_stage99/test_original_three_cue_species_holdout_source_leakage.py`
- `.github/workflows/floral-stage99-original-mainland-three-cue-species-holdout.yml`

Actual counts pending original SHA-verified source CI. Keep Draft and main unchanged.