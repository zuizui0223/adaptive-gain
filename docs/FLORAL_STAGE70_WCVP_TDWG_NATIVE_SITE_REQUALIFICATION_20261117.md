# Stage70 | Source-pinned regional nativeness of original floral optical × EuPPollNet comparisons

**Status 2026-11-17 JST:** source-authenticated real GitHub Actions [44061625101](https://github.com/zuizui0223/adaptive-gain/actions/runs/44061625101) SUCCESS for conservative WCVP×TDWG native-region filter; source-authenticated follow-up [44061979834](https://github.com/zuizui0223/adaptive-gain/actions/runs/44061979834) SUCCESS with strictly separate historic geometry repair sensitivity. Draft stacked on Stage69 PR #148, `main` not modified. No biological-effect p-value, causal SEM or evolutionary fitness effect estimated.

## Source chain and checks

1. Prior fixed source: corrected [EuPPollNet v1.3.0](https://github.com/joseblanuza/EuPPollNet/tree/v1.3.0), 623,476 genuinely observed records, 1,864 study×network×year cells, source [Stage69B 156 networks](https://github.com/zuizui0223/adaptive-gain/actions/runs/44057077625). The frozen selection is different measured-petal species from different genera, ≥3 visits per plant, both *Bombus* and other guilds in network, UV mean petal reflectance difference ≥1 percentage point. It is a *design filter*, not a significant ecological effect.
2. [Natural History Museum botanical descriptive TEXT](https://github.com/NaturalHistoryMuseum/plant-traits), original 59,369 accepted literal plant labels, from Stage68; no image-derived flower colours.
3. [Shrestha et al. original 73 botanical garden petal spectra](https://doi.org/10.6084/m9.figshare.21081025.v2), 26 actual spectral plant names represented in Stage69B 156 source networks. Raw 300–399nm percent mean petal reflectance is **not spatial UV nectar-guide geometry**. Original spectrometer measurements are at a German botanical garden; EuPPollNet visits are on independently surveyed field plants.
4. Original official [Kew WCVP](https://sftp.kew.org/pub/data-repositories/WCVP/wcvp.zip), SHA256 `d32ea2b3a85e489b14e83bcc9eae7274532e1d113753f7be290d4b2dfde573fa` (same historical pin previously verified in `zuizui0223/island`). Parse exact `wcvp_names.csv` species rank+accepted status and `wcvp_distribution.csv` TDWG-L3 `area_code_l3` with non-extinct, non-doubtful, introduced=0 for a **regional compatible** native record. An unlisted L3 is UNKNOWN, never confirmed nonnative or species absent.
5. Original [TDWG WGSRPD Level3 geojson](https://github.com/tdwg/wgsrpd/blob/master/geojson/level3.geojson), Git blob SHA1 `91104e5159e31f88154833a51d3b0d1c9271083f`. Author original field points are mapped within a unique polygon, not to the nearest polygon; no field site selected when a network has multiple source coordinates, or in source-border 0.02° angular sensitivity. The polygon geometry is historical, not a survey coordinate error or modern high-resolution coastline.

## Verified primary Stage70 outcomes

From the exact **156** design-eligible original source networks, **26** independently measured optical botanical species:

- Kew WCVP accepted exact species labels: **25/26**; `Calystegia sepium` did not pass exact accepted name. This does not mean that species is biologically absent or always nonnative; taxonomic reconciliation remains unresolved.
- TDWG originally supplies **369** polygons, **350** valid and **19** topologically invalid. Conservatively ignoring 19 source-invalid polygons (no automatic geometry edits), the original 156 source networks were classified as **85** uniquely within non-border polygons, **3** close to boundaries, **68** outside/ambiguous relative to the valid-only set.
- **73** of the 156 networks meet original source-region compatible WCVP nativeness and conservative edge controls for >=2 eligible real-spectra plants, among **20 distinct source study IDs** and **20 plant names**.
- Original eligible source plant×network units: **485**; WCVP native L3 compatible **276** before border sensitivity, introduced L3 recorded **6**, WCVP unlisted area **2**, WCVP species not exact accepted **5**, source site L3 unassigned **196**. These are units repeated across networks, NOT 485 species. Original local introduced records include `Borago officinalis`, `Geranium pratense`, `Solidago canadensis`, `Veronica filiformis`; unlisted `Tropaeolum majus`. These labels do not establish field introduction origin of each observed individual.
- Of all 1,864 original source network-year keys, six have multiple distinct source coordinates. These are refused automatic single-site assignment.

## Critical geography-source sensitivity — NOT a replacement primary

The separately registered diagnostic [Stage70B Actions 44061979834](https://github.com/zuizui0223/adaptive-gain/actions/runs/44061979834) uses `shapely.make_valid` *only* on the 19 historically invalid geometries while leaving 350 originally valid polygons unchanged, and recomputes area membership rather than changing source row identities.

- All **19** previously invalid source polygons are repairable geometrically. They include **Germany**, Greece and Norway and 16 other source-level botanical regions; these are historical topology problems, not evidence of biological occurrence absence.
- Of **68** previously unlocated Stage70 networks, **65** receive exactly one Level3 area under repaired topology, **3** remain geometrically unresolved.
- In this additional geometry-only sensitivity, **62** further networks (mostly Germany source surveys) also pass WCVP native compatibility and the original field-guild/spectrometer comparison criteria.
- Hence **135/156 networks in 26 studies** pass the **repair-sensitivity** version. The original conservative primary **73 networks in 20 studies** remains unchanged. No originally primary-qualified network loses that status in the repaired-geometry sensitivity.

The sensitivity is **not** a newly measured plant-native field-site source or evidence of genuine same-individual floral optical adaptation. For interpretation, retain **73 primary / 135 repaired-geometry sensitivity / 3 still unlocated**, not “135 proven native phenotypes”. Although geometry repair may be an appropriate future primary GIS preprocessing step after an independently audited spatial pipeline, Stage70 does not silently promote this post hoc choice.

## What remains unidentified

- No original co-measured optical phenotype from the **field** plant individuals observed by EuPPollNet: 2024 original spectra are from a German botanical garden. Species means may vary geographically, so garden spectral traits cannot be assumed invariant across all 156 field networks.
- Field visitor count is observation-effort contingent, not a validated visitation per flower or pollen transfer rate; no record for a guild is not a surveyed biological absence. Different source studies have different sampling methods.
- European survey scope lacks bird guild, and *Bombus* vs non-*Bombus* is an observational subset; no global bird/bee comparative syndrome estimate.
- Matched source site meteorological wind, true species-specific emitted VOC, field light/UV-B, direct sensory routing and plant reproductive fitness not collected together.
- Cross-study causal path/mediation SEM, selective adaptation, and global prediction slopes are not established.

## Executable and next gate

`research/floral_literature_macro_stage70/official_wcvp_native_tdwg_original_field_network.py` reconstructs original source native regional matches. `research/floral_literature_macro_stage70/historic_tdwg_invalid_geometry_diagnostic.py` separately recomputes the old polygon repair sensitivity without altering main classification. Nine synthetic-only tests cover false absences and topology; both scripts rerun in the standalone [Stage70 workflow](../.github/workflows/floral-stage70-original-wcvp-tdwg-native.yml).

**Next science decision:** first verify field-local flower phenotype transfer or identify *actual site-collected spectral* sources for several independent EuPPollNet studies. With that (or with explicitly labelled garden-species proxy exploratory status), prospectively compare per-network *Bombus* vs competing guild visitation as a composition conditional on source effort, floral abundance and study identity, with held-out study IDs; include native-border sensitivity and species/phylogeny controls. Do not present a phylogenetic causal effect until source-site phenotype and independent study information support it.

Result artifact from [Stage70B successful run](https://github.com/zuizui0223/adaptive-gain/actions/runs/44061979834): artifact ID **14318313234**, ZIP sha256 `6bf6ce8aef58b3561f15c43a54fa2985f073cc71ec64903d71262a02d5091444`. Derived network×species and area code tables only; original full WCVP/TDWG source bytes not redistributed.
