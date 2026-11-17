# Stage65 — Flowering-annotated iNaturalist photographs: original pixels, source-ID overlap correction and visible corolla marking QC

Date: 2026-11-17 JST. **Status: original annotated-flowering source search, 27 licensed candidate IDs, eight actually downloaded original CC-BY/CC0 photos, one exploratory assistant review of visible petal markings, all source-ID/SHA checks successful. NOT new UV nectar-guide, VOC, wind, pollinator or fitness measurements.**

## Why this study was necessary

Stage60 source-authenticated original `Farré-Armengol 2020 VOC 305 taxa × FCP 4,475 photo species` produces 80 exact species names with original FCP coarse photo opportunities (55 taxa ≥40 coarse-color classifiable photos). Stage64 [original source 8-image QC](https://github.com/zuizui0223/adaptive-gain/actions/runs/44020202688) showed that six of eight licensed original iNaturalist photographs did not provide an adequate view of fresh flower petal markings, including three entirely vegetative frames. A source-photo absence cannot be counted as a flower's biological lack of marks.

Stage65 tests a prospective **image acquisition eligibility filter**, not a treatment on flower biology. Official iNaturalist observation annotated `Flowers and Fruits / Flowers` encoded by `term_id=12&term_value_id=13` (source support: https://help.inaturalist.org/en/support/solutions/articles/151000170738-how-to-use-inaturalist-search-urls). The annotation describes the observation's flowering condition but does **NOT guarantee** that the selected photo itself contains a legible open flower.

### Original botanical taxa fixed before viewing images

- `Dianthus deltoides` — original iNat taxon 76647, Stage60 VOC×FCP source, unconfirmed NHM visible marking textual lead.
- `Dianthus barbatus` — original iNat taxon 60015, same textual lead.
- `Helichrysum stoechas` — original iNat taxon 82641, unlabeled comparison, NOT a verified no-guide species.
- `Antirrhinum majus` — original iNat taxon 48969, unlabeled comparison, NOT a verified no-guide species.

All four belong to original **80-name VOC×FCP image opportunities**. Search is original iNaturalist `/v1/observations`, research-grade, noncaptive, exact taxon ID, up to first 50 observations, at most one selected photo per observation/observer, source open-license gates. The earlier unfiltered Stage64 and new annotated sample come from the **same iNaturalist provider** and are not independently sampled ecological replicates.

## Actual original source metadata, correct ID overlap

Original photographed source CI [Actions 44020931936](https://github.com/zuizui0223/adaptive-gain/actions/runs/44020931936) **SUCCESS**, six mock-only tests including a hard regression against the original API integer photo ID versus prior CSV string ID mismatch. This regression revealed a **critical previously reported bug**: the initial Stage65 output incorrectly showed zero overlap because numerical source API ID `763131994` was not equal to prior string `"763131994"` until canonicalization. That zero-overlap claim was withdrawn and corrected. Original source artifact **14301031564**, ZIP SHA256 `e6674a7af5cefdfc87a999e0ed107e682eff31fe6a110968ff5db1213b51b794`.

| Source taxon | Stage64 previous unfiltered first-50 search accepted metadata | Stage65 newly retrieved flowering-annotated accepted metadata |
|---|---:|---:|
| D. deltoides | 5 | 8 |
| D. barbatus | 4 | 4 |
| H. stoechas | 5 | 7 |
| A. majus | 3 | 8 |
| **Total** | **17** | **27** |

Across the prior 17 and Stage65 27 original **photo IDs**, corrected **5 IDs are reused**, and **22 Stage65 selected IDs were not in the prior 17**. The distinct ID union = `17+27-5=39`, not 44. No effect size for a randomized phenology filter can be inferred from changing source query populations; the age, photographer/license selection and order differ.

## Real independently audited original photo pixels

The Stage64 genuine source image script selected two of the newly accepted annotated source photo IDs per species by a **fixed photo-ID hash before opening pixels**. CC-BY-SA originals remain in the source metadata only; for original 2×4 contact-sheet adaptation only CC-BY/CC0 source files were downloaded with photographer credits. Source [Actions 44020653604](https://github.com/zuizui0223/adaptive-gain/actions/runs/44020653604) and corrected [Actions 44020931936](https://github.com/zuizui0223/adaptive-gain/actions/runs/44020931936) each downloaded exactly **8 actual original medium iNaturalist photos**, **2 per source taxon**, without false botanical labels. Contact sheet and source photo ID/credit/license/SHA256 are in source artifact 14301031564. The original 100 exact photos per FCP study taxon are not reconstructed or claimed to be these new iNat photographs.

**One unblinded assistant review of the eight real pixels** (NOT two independent assessors) was written with original photo ID, observation ID and source SHA; the original-source independent QA [Actions 44021427009](https://github.com/zuizui0223/adaptive-gain/actions/runs/44021427009) **SUCCESS**, four source-free QA tests; result artifact **14300783470** ZIP SHA256 `aceaa2ccd6c556dda5b47532d729a83cbd2173cc37de419c878e30386c1efa29`. Exact photo ID, observer observation ID, open-license attribution, unmodified original medium-image SHA, strict membership in the annotated photo registry and reused IDs in Stage64 were verified.

| Species | Original source photo ID | Original observation ID | Image anatomical eligibility | Conservatively judged RGB visible flower colour marking |
|---|---|---|---|---|
| D. deltoides | 763131994 | 414531756 | Open corolla, petal detail | **Present**: pale radial streaks and spots on magenta/purple petals (also present in Stage64 old original pixel sample) |
| D. deltoides | 730023394 | 397986245 | Pink flowers visible but distant | **Unknown** (not measured negative) |
| D. barbatus | 697709548 | 381318277 | Open corolla, petal detail | **Present**: contrasting light radial markings in magenta petals |
| D. barbatus | 736925000 | 401495210 | Deteriorated/pale floral structure | **Unknown** |
| H. stoechas | 674845341 | 369452631 | Yellow capitula distant, individual petals unresolved | **Unknown** |
| H. stoechas | 714404874 | 389979959 | Dry capitula not resolved | **Unknown** |
| A. majus | 760688061 | 413317984 | White blooms distant, throat region unresolved | **Unknown** (also selected in Stage64 prior pixel sample) |
| A. majus | 743022562 | 404594047 | Open pink/magenta corolla with differentiated throat | **Present**: high-contrast orange/yellow inner throat against magenta corolla |

**Source-pixel QA totals**:
- Eight authentic inspected **source photos**, across four source species.
- **Three visible petal/interior colour markings** (one picture each across **three species**), zero verified within-corolla uniformly coloured petals.
- Five unknown/unscorable (four bloom-but-detail-not-resolved, one dried floral head). No plant of any of the four species is declared a verified 'visual-guide negative'.
- Exactly **two of eight Stage65 pixel IDs were present in the previous Stage64 original 8-image audit**. One of these two reused pixels was already labeled visible-pattern present, so **two of three Stage65 positive images had not been in the previous original image-review sample**. This is *not* two independent ecological replications or a photo-sampling treatment effect.
- Reviewers = one unblinded assistant, not independent double-scored flower segmentation; agreement, false positives and generalization remain unknown.

### Claim boundary and ecological interpretation

A *visible floral marking* is not automatically a nectar/reward guide, a UV pattern, a scent molecule, an experimentally selected trait, actual Bombus visitation, or stigma pollen deposition. Original iNat camera RGB lacks UV, and source species-level published VOC from independent original studies is **not same plant, site or date**. A type of pink with yellow throat may suggest an optical contrast but receptor discrimination and use remain unmeasured.

No inference about that flower's habitat wind, gusts, odour plume, modelled guild-specific color vision, local native Bombus species, fruit/seed fitness or the existing Stage63 Bayesian sensory routing is supported by the eight photographs. A source iNaturalist **flowering annotation is observation-level**, still allowing unreadable image details or dry organs.

**Progress versus prior:** earlier original Stage64 pilot had 2/8 visible-pattern photos, 6/8 unknown; new annotated photo set has 3/8 visible-pattern photos, 5/8 unknown. These are different photo-ID samples, with 2 overlapping records, within the same provider and species. They do **not** form a randomized paired experiment and cannot establish that annotation increases true phenotype ascertainment probability. What is confirmed is operational feasibility of obtaining more original flower-photo cases in multiple species.

## Next strict execution gate (not claimed complete)

1. Recover more original CC-licensed images with prospective flower annotation and *actual* **manual organ visibility** pre-screening, then score marks on a second independently blinded set, including sufficient **visible-mark-negative *open* flowers**. Without measurable true negatives, do not fit a cross-species visible-signal occurrence model.
2. Study botanical floral-type variation in taxa that share independently recorded VOC sources; number of accepted species is not the number of voucher-matched plant phenotype samples. Keep source study and sampling effort independent.
3. After real behavior uses information and actual floral pollen transfer from same experimental animals and source plants, compare **conditional first-cue routing** against the strongest static/noisy Bayesian multisensory control. Prior Lawson 2017 visual backup and Graver 2026 cue timing/scale effects already exist. Stage63 exact four-world model is source-free theory, not this field effect.

Main branch untouched; stacked Draft Stage65; source input/QA scripts in `research/floral_routeability_stage65/`.
