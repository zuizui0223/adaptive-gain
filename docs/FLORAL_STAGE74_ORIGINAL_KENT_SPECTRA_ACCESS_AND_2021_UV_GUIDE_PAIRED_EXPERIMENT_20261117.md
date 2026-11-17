# Stage74 | Same-island measured flower spectra and genuine environmental UV-guide manipulation: original-data admission and paired reanalysis

2026-11-17 JST. Stacks on Stage73 Draft PR #152. **Main remains untouched**. This is a source-authenticated retrieval, an explicit access-failure audit and a source-original reproduction of a **published 2021 single-plant experimental study**, not a new multispecies macroecological association, adaptive-gain theorem test or claimed first evidence for environmental visual cue dependence.

## Scientific decision before the analysis

Stage71 saw an observational, source-species-constant German botanical garden UV-reflectance proxy for Euro field visits shift from positive (`+0.8468` null-local score in 93 conservative informative networks) to approximately zero (`−0.0179` in 186 original repaired-GIS informative networks). A simple "more UV means more *Bombus*" claim is **not robust**. Next, we sought genuinely coincident measured wild flower spectrometer traits and observed visitation, and actual prior environmental UV-background manipulations; we must not backfill wild phenotypes using photo-derived colours or infer nectar guides from mean petal UV.

## 1. NEW original same-island spectra×visitor source candidate: Jones et al., Kent Island, Canada (2025)

Article original DOI [10.1098/rsbl.2025.0044](https://doi.org/10.1098/rsbl.2025.0044), archived source DOI [10.5061/dryad.9p8cz8wtm](https://doi.org/10.5061/dryad.9p8cz8wtm). Real official Dryad v2 source version **365076** includes nine original files; author reports 90 field flower spectral plant species, 74 species with visitor events, 3,718 visitation observations and 145 original visitor taxonomic types. **The reported counts were not independently recomputed because original numeric files could not be downloaded.**

- `Floral_Reflectance_Kent_Island_Plants.csv`: source v2 file ID **4074180**, **248,453 bytes**, original publisher SHA256 **`bd78bdfc810b3330a3a2ae2fe9ed0af297e1626141fb513f6675d25d73e22fd0`**.
- `2019_2023_Kent_Island_Plant_Pollinator_Network.csv`: source file ID **4074184**, **405,961 bytes**, official original SHA256 **`67b8585c07b525ab5c4b3207944ea0d1b027d4fc6b4a2f6eb7d7087801cc6135`**.
- Both original public WEB HTML anchors are independently observed on the Dryad dataset page (`/downloads/file_stream/4074180`, `/downloads/file_stream/4074184`), but BOTH stream downloads returned **HTTP403**. The file identity, published research design and site provenance are validated; the **real original numeric CSV bytes have NOT been acquired or analysed**.
- Other original author files on that same archive include flowering phenology, experimentally assessed pollinator learning, source analytical script and processed colour distances. These are source metadata records, NOT evidence we have reanalyzed the author's learning effects.
- Spectral flowers sampled from the same island as field bee/fly visits do NOT establish source-same individual flowers or even same calendar year (network spans 2019/2022/2023 and field reflectance originates 2022/2023). No photo-derived traits, true UV spatial-guide negative or plant reproductive fitness should be inferred.
- This paper itself already tested floral signals and pollinator cognition, so "floral colour and bee networks interact" is not a new novel claim.

Original source [Actions 44102174065](https://github.com/zuizui0223/adaptive-gain/actions/runs/44102174065) **SUCCESS**, 7 source-free integrity controls and original source metadata/public HTML admission, artifact **14335379034**, SHA256 **`2f1437a1512c033c431f654a171e9436b6100a2f33161a4f59dd804bca0be2f8`**. A prior mock-only test failure was corrected by using real binomial species names rather than genus-`sp.` proxies; final stage passed. Unavailable original CSV source was **not fabricated**.

## 2. Major primary-source addition: Finnell & Koski 2021 environment×UV-guide×visitor behavior (previously published)

Source original article DOI [10.1111/nph.17631](https://doi.org/10.1111/nph.17631), official Zenodo original source [10.5281/zenodo.5110165](https://doi.org/10.5281/zenodo.5110165). Prior published field UV sensory-drive experiment on ONE flowering species, *Argentina anserina*, high/low alpine elevation, ambient/reduced UV-light conditions, original large/small floral UV-guide stimuli and separate bare/foliage background manipulation, observed bee/fly visitors. **This is existing mechanistic prior art, not independently novel evidence or a global replicated macro signal.**

All **five original author files** were retrieved through official Zenodo public API and source-author checksum-verified (the Zenodo original metadata source is also SHA256 logged):

| Original file | Verified bytes | Independently calculated SHA256 |
|---|---:|---|
| `FinnKosk_PollData_Final.xlsx` (real first visits) | **67,593** | `d66d12f3dbfc83b3fe6e854b69f9e5f768a1c3f973c0db5368176e17264ace59` |
| `ColorContrastData.xlsx` (real chromatic/achromatic visual contrast) | **16,068** | `68d000362b9840a752f8e82cab005406eb81eaa4ab48f1e1ca8814829757ddd7` |
| `Spectra Used for Vismodels.zip` (flower/irradiance/background 77 source files) | **826,745** | `1e849dd5374de206abeb192d543b14cea07dc0a385cf616fbe713de2bd7fea87` |
| `SAS_modelcode.R` | **2,743** | `1e8f2d8508b83fa5dae0b0d9be2a3b5424e0fbf465ed473974ec57eb88fe2126` |
| `vismod_Code.R` | **4,740** | `3550524979eb71db6d08d801fbdd90f7ef456b6d1e7d4f80a2361f0706ab254a` |

Original source archive contains 77 entries, including macOS archive metadata and non-independent spectrum samples; do NOT call all 77 distinct measured plant species. Independent study species count: **one**. Original `ColorContrastData.xlsx` has sheets `Chromatic Floral Contrast`, `Background Chromatic Contrast`, `Background Achromatic Contrast` and its author headers; no inferred analogue of site meteorological wind.

Source retrieval/access CI [44102819892](https://github.com/zuizui0223/adaptive-gain/actions/runs/44102819892) **SUCCESS**, original artifact **14335279990**, SHA256 `8c05e4be86aefdb893ee07f90fce54b29b083e59826ac85d3a841fe6ea331e56`. Workbook field and spectral archive source structure [44103458903](https://github.com/zuizui0223/adaptive-gain/actions/runs/44103458903) **SUCCESS** after fixing source workbook helper import.

## 3. Independently reconstructed original 2021 first-visit experimental evidence

The original `FinnKosk_PollData_Final.xlsx` `UVLightArrays` worksheet has **648 rows** because observations are arranged as experimental array × source flower number × bee/fly taxon group, **NOT 648 independent treatments**:

- **54** distinct source experimental arrays;
- **27** matched altitude×population×date×array-pair keys, one original source `AMBIENT_UV` and one `REDUCED_UV` treatment each;
- **377 source integer `FirstVisits`**, exactly reproducing the originally published UV experiment first visit count; **448 rows** contain actual original numeric zero recorded for that flower×guild cell. The distinction between a source-observed zero **within an actual observed experimental array** and an absence at an unobserved geographic sampling site remains essential;
- Genuine source `FlwType` codes `L` large and `S` small; original `Poll` bee/fly. The 377 observed events split as:

| Elevation | UV illumination | Large-guide first visits | Small-guide first visits | Total | Original arrays |
|---|---|---:|---:|---:|---:|
| High | Ambient UV | **48** | **28** | **76** | 15 |
| High | Reduced UV | **14** | **21** | **35** | 15 |
| Low | Ambient UV | **69** | **91** | **160** | 12 |
| Low | Reduced UV | **45** | **61** | **106** | 12 |

At high elevation the raw event-weighted large-guide fraction is **63.16% ambient vs 40.00% reduced**; low elevation **43.13% ambient vs 42.45% reduced**. These raw percentages are **not equivalent to a paired treatment-specific statistical effect**: individual arrays have different visit intensities and some array arms have no first visits.

For a deliberately **descriptive, matched-pair** summary, restrict to original pairs where BOTH treatment arms have at least one observed first visit and calculate the within-pair difference of large-guide visit fractions (ambient minus reduced) averaged across pairs:

| Elevation | Original paired array keys | Pairs with both arms observed | Mean of within-pair large-guide fraction differences | Seed-fixed 5,000-resample paired-block 95% percentile range |
|---|---:|---:|---:|---:|
| High | 15 | **11** | **+0.0730** | **−0.1725 to +0.3365** |
| Low | 12 | **12** | **−0.1103** | **−0.2956 to +0.0553** |

The high-minus-low difference of the **descriptive paired mean differences** is **+0.1833** (18.3 percentage points); independent elevation-specific paired resampling percentile range **−0.1171 to +0.4985**. These are **not original author's SAS-model estimates**, and **not confirmatory p-values or causal fitness effects**. One high-altitude original pair's reduced or ambient treatment had zero first visits (four such pairs total), so the mean conditions on 11 informative pairs. Selection into having both arms visited can itself affect interpretation. Uncertainty is broad and includes zero; the original reported mechanistic response cannot be described as newly statistically confirmed by this one-step bootstrap.

Original source-recount / paired-descriptive CI run [44104769150](https://github.com/zuizui0223/adaptive-gain/actions/runs/44104769150) **SUCCESS**, independent original SHA validation, original paired counts and fixed-seed bootstrap. Latest branch source workflow additionally explicitly asserts fractional/background handling; its final updated CI digest is to be verified after the final patch.

### Separate background experiment: **source raw-data semantics remain unresolved**

The original `BackgroundArrays` worksheet has 312 flower×pollinator rows, 26 original array IDs and 14 original pair keys. Of 312 source `FirstVisits` cells, **10 contain non-integer values** (five `0.75`, five `1.5`); integer-only cells sum to 249 and fractional cells sum to **11.25**, combined numeric sum **260.25**. These noninteger cells cannot literally denote a count of individual first insect visits without further weighting/author semantics. **We do not round them, call 249 a complete original background visit count, or estimate bare-versus-foliage discrete first-visit preference with those incomplete values.** The source manuscript's background-contrast findings are acknowledged as published prior art, not re-estimated under invented count semantics.

## 4. What this does and does not test for macroecology

**Real biological inference that is appropriate:** This field experimental literature directly demonstrates why ambient UV transmission, visual backgrounds and receiver-specific response matter when assigning ecological usefulness to floral information; original source data now independently available for transparent computational audit. The experiment provides a strong mechanistic *reference*, not a new general macroecological test. Different receiver guilds and habitat contexts need not value the same source optical cue.

**Not demonstrated:** A replicated across-species macro UV guide×Bombus richness coefficient; local evolution of species-specific guide loss; conditional first-request adaptive routing; co-located wind×VOC×UV effects; pollen transfer or fruit/seed fitness. Original 2021 source contains one species; 54 arrays are treatment replicates, not 54 independent plant evolutionary radiations. The original source's background fractional response cells, original manuscript model specification and the source Kent Island binary-access barrier are not solved by accumulating visits.

The original independent-public-literature bridge at present is:
- **Kent Island**: real same-island original spectral+visit source identified, source metadata SHA verified, **raw downloads HTTP403**; cannot re-estimate numeric coefficients.
- **Finnell/Koski alpine experiment**: original source all 5 files and 377 field UV first visits verified; **one species and already published experimental sensory-drive evidence**.
- **Lesvos Kantsa 2018**: original 40 exact-taxon VOC × 41×168 visitor network same-region source; no original wavelength-resolved colour file in those two 2018 sheets.
- **Wisconsin**: real author field wind Beaufort + literature-categorical visible color + visitation; wind constant at site×date and original Excel-year mismatch; cannot infer causal wind and does not measure UV.

A publishable macro test needs independently observed **same-field** floral UV guide geometry / spectral receptor contrast, true visitor guild opportunities, floral abundance/exposure and defensible geographic/climate context in **multiple independent regions/species**. Do not claim missing download binary means biological absence. Existing 2021/2025 papers already own any single-species UV UV-light experimental or cognition discovery.

## 5. Reproduction and status

Source/original code (no flower photographs used):
- `research/floral_original_field_stage74/probe_kent_original_public_dryad_stream.py` and 7 source-free tests.
- `research/floral_original_field_stage74/audit_original_2021_sensory_drive_Zenodo.py` and 6 source-free tests.
- `research/floral_original_field_stage74/inspect_original_2021_UVguide_field_workbook.py` and 5 source-free tests.
- `research/floral_original_field_stage74/recount_original_UVguide_first_choice_by_array_pair.py` and 5 source-free guards after fractional-value fix.
- `research/floral_original_field_stage74/compare_original_2021_UVguide_pair_contrasts.py` and 6 source-free tests.
- GitHub Actions workflows `.github/workflows/floral-stage74-Kent-original-public-Dryad-spectra.yml`, `floral-stage74b-original-UV-guide-Zenodo.yml`, `floral-stage74c-real-source-UV-guide-factor.yml`, `floral-stage74d-original-UV-array-pair-recount.yml`.

**Numerical source claim ceiling:** Verified real source first visits 377 at 54 array units; descriptive high-minus-low paired contrast with broad uncertainty, not a new confirmatory experimental or global macro result. The next source acquisition gate is independent site-native source field optical traits + independently observed visitor groups with original bytes and temporal/site validation.
