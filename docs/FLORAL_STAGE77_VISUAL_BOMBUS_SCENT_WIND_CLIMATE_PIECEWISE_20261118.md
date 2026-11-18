# Stage77 | MACRO floral visual information × Bombus: wind and climate adjustment, original VOC identifiability

**Status 2026-11-18 JST:** four distinct original-source tests have SUCCEEDED. This is the corrected research **mainline** the user requested: **NO islands**, no WCVP/island flora layer and no repeated single-species experimental workflow. The branch stacks directly on Stage75 continental field network evidence. The estimand is initially an **observational conditional association**, not an evolutionary causal SEM.

## Central hypothesis: visual cue usability, not simple hue-syndrome matching

Does the relation between *independently documented* floral visual characteristics and the **realized recorded Bombus component of the bee visitor community** change with atmospheric/environmental context, especially wind and temperature, after accounting for study composition and insect observation? If same-site measurements become available, evaluate whether VOC emission/olfactory accessibility modifies or mediates the visual-guild relation. Wind may mask odor plumes as well as alter insect flight, phenology and botanical assemblage, so a coefficient on wind must not be automatically interpreted as a sensory signal.

The conditioning question is **not an island hypothesis**. Continental study, species/genus, site/year and environmental covariation matter. Previous *visual×scent×wind* mechanisms have been studied experimentally (e.g. Lawson et al. 2017) and floral VOC×climate×pollinators have already been analysed (Farré-Armengol et al. 2020). A generic multimodal association is therefore not itself a novel finding. The macroscale claim would need independent receiver-accessibility differences and study/lineage holdouts.

## Stage77A: original wind and environment at real field network coordinates

Original corrected [EuPPollNet v1.3.0](https://github.com/joseblanuza/EuPPollNet/tree/v1.3.0), 623,476 actually observed original plant–visitor records, 54 original independent study IDs, 1,864 study×network×year keys. Source coordinates unique for **1,858** networks; **six** source networks have multiple distinct original coordinates and receive **NO fabricated single representative location**. All source visit dates parsed directly as year-first, so original observed calendar months are available for the rest.

Original [WorldClim 2.1](https://www.worldclim.org/data/worldclim21.html) 1970–2000 10-arcminute (~18km latitude) monthly GeoTIFF rasters were **downloaded from the official UC Davis host** and SHA256-authenticated at each ZIP; 12 original EPSG4326 source monthly rasters each for wind (m/s), Tavg (°C), precipitation (mm/month), vapor pressure (kPa), solar irradiance (kJ/m²/day). No nearest-land extrapolation, reanalysis invented from study year, or default zero missing values. Exact **1,858/1,864** unique-coordinate study networks have annual and observed-month five-variable real climatological attributes. These are **1970–2000 climate means, not instantaneous wind at a visit, not measured odor plume and not source measured insect flight conditions**.

[WorldClim source/run 44205235512](https://github.com/zuizui0223/adaptive-gain/actions/runs/44205235512) **SUCCESS**, 9 synthetic date/geometry/climate tests; source artifact **14383900449**, digest `sha256:63c877a6993fd6afb2ce6566482fa9661307cb01d361002b7596cb97d4d28439`.

Original source ZIP SHA256 individually frozen:
- `wc2.1_10m_wind.zip`: `489660bd6ab3bf5ddf4c1a3d29d8ddd96babe413a97bb3bde9bb60575e680c5c`
- `wc2.1_10m_tavg.zip`: `5e567dcfe94379b94229492849ce91078b1c6e5210aaf435fba449fae6b95405`
- `wc2.1_10m_prec.zip`: `1090f578f6402672a2b6438e252156f6cf867a25002a8ad6ffcbfa19e516ddc6`
- `wc2.1_10m_vapr.zip`: `0501b5b5cbbc6e2fc2a3801efa9a126a5f9669f0f9a00642d2519c2324ce726d`
- `wc2.1_10m_srad.zip`: `c72ee7f4f9a0eb4b5f6cd7a003eddc05bda22a2e5666d968ed4e817fd36b9026`.

## Stage77B: explicit two-equation observational piecewise path-screen

Original authenticated NHM botanical prose contains 59,369 source species/labels. In original EuPPollNet, 1,408 plant species occur in visited field records, 963 exact NHM botanical text matches, and **233** have one lexically explicit reported hue family (NOT actual flower colour measurement or UV nectar-guide negative). After source visitor-based plant group assembly, **424** study×network×year units across **43** studies have ≥2 distinct original positive hue families. 422 original source monthly WorldClim complete and **421** record at least one strictly identified bee visitor, across **42** distinct original original study IDs. No site is selected according to the presence of *Bombus* before building the visual frame.

Define two *network-level* variables with a 0.5 finite-logit continuity adjustment:
- \(V_k=\log[(N_{\mathrm{yellow},k}+0.5)/(N_{\mathrm{other\,explicit\,hue},k}+0.5)]\). A **prose-reported species composition conditional on already observed visiting plants**, not actual optical-UV pattern or colour signal measured at the field.
- \(B_k=\log[(n_{\mathrm{observed\,Bombus},k}+0.5)/(n_{\mathrm{observed\,other\,bee},k}+0.5)]\). A **realized species-rank visitor record composition**, not source field pollination effectiveness, all-bee abundance, independent *Bombus* SDM suitability or verified guild absence.

The directed *associational* screen, not a causal SEM, is

\[
V_k = a_WW_k+a_TT_k+a_PP_k+u_{\mathrm{study}(k)}+\varepsilon_k,
\]

\[
B_k = b_VV_k+b_WW_k+b_{VW}(V_kW_k)+b_TT_k+b_PP_k
  +v_{\mathrm{study}(k)}+\eta_k,
\]

where original WorldClim seasonal wind/T/precipitation are centred and SD-standardized over the **visual frame before any guild outcome is opened**, and study intercepts are fixed effects with study-cluster-robust descriptive uncertainty. Secondary replaces T/P by actual source vapor pressure/solar irradiance to diagnose different correlated environment axes. Both equations are ordinary equal-network-weight OLS approximations to compositional transformed records, not a fitted binomial likelihood, phenotypic selection coefficient, experimental cue experiment or validated full phylogeny.

[Full original source path run 44206960082](https://github.com/zuizui0223/adaptive-gain/actions/runs/44206960082) **SUCCESS**, 8 mock path-structure/collinearity/date/cluster controls, 421 real field network units, source artifact **14382874793**, SHA256 `5116ab6bb18a8e1c62be70be9e5a47630d49b3c50767815525fb3cf32f1f9b8a`.

| Observational path, one SD change for climate normals | Estimate | Study-cluster 95% sampling interval (descriptive, NOT causal) |
|---|---:|---|
| \(V \to B\): positively documented hue composition vs actual Bombus share | **+0.0194** | **−0.2286 to +0.2675** |
| \(W\times V \to B\): climate wind normal modifies hue–Bombus relation | **+0.1016** | **−0.1228 to +0.3261** |
| \(W\to B\): climate wind normal vs realized Bombus share | **+0.1639** | **−0.6401 to +0.9680** |
| \(W\to V\): climate wind normal vs source-recorded hue composition | **−0.1166** | **−0.3044 to +0.0712** |
| \(T\to B\) | +0.3430 | −0.2227 to +0.9087 |
| \(P\to B\) | +0.3034 | −0.0771 to +0.6840 |

Sensitivity replacing T/P with original water vapor pressure/solar irradiance: wind×V **+0.0806 [−0.1366,+0.2978]**. Main wind×V interval crosses 0; **no supported wind moderation**, despite its point direction staying positive in single-study-out diagnostics. The V→B sign changes in **5/42** study deletions. Of 43 pre-outcome original studies, 31 have within-study variation in 1970–2000 climatological wind greater than 0.05 of the frame-wide SD. Median within-study wind SD ~0.108 m/s versus between-study mean SD ~0.815 m/s; wind is strongly study/spatial-structured, and within-study contrasts can be small. Reported climate normals are correlated (T with vapor pressure, wind with temperature, etc.), so no unadjusted wind coefficient should be described as a "wind sensory effect".

**Fundamental observation conditioning:** The floral trait distribution is measured only among positive visited plants, not an independently censused flowering source community; both V and B arise from a conditioned network sample. Taxon-level V itself is source species constant and can correlate with plant evolutionary lineage and observation study method. Study fixed effects alone do not remove species/phylogeny and network sampling bias. This is an **exploratory macro evidence audit**, not a genuine cause-specific ecological mediation result.

## Stage77C/D: newly retrieved *original floral scent* multispecies chemical tables

2020 [Farré-Armengol et al.](https://doi.org/10.3389/fpls.2020.01154) *Deciphering the Biotic and Climatic Factors That Influence Floral Scents*, PMCID `PMC7412988`. Author paper reported **305** source plant species, **66** families, **851** floral VOCs compiled from 58 previous source studies. Their publication **already** related plant scent to climate and pollination. **Novelty cannot be simply "climate × floral VOC".**

[Original data retrieval CI 44207723647](https://github.com/zuizui0223/adaptive-gain/actions/runs/44207723647) **SUCCESS** verified the Europe PMC authoritative `PMC7412988/supplementaryFiles` ZIP and 3 original genuine Excel source workbooks among **24** source archive members; original outer archive 8,428,937 bytes, first packaged ZIP SHA256 `44b9f0b8ee0a41be3958a18552e84afb518ecca57e34b573e4a7d800ae1dfb88`. Europe PMC *dynamically repackages ZIP* with potentially changing SHA256, despite stable original member data. Stage77D checks the actual original member sizes, exact semantic `Species` column and independently re-fetches the authority URL **twice** to confirm stable original member SHA rather than silently repinning wrapper ZIP, and checks OOXML structure. Real original 3 workbook source SHA256:
- `DataSheet_1.xlsx`, original `PRESENCE` (reported VOC presence): **1,582,240 bytes**, SHA256 `918ebcf51db693eb14ae8dec5eca1cb19fd48513cc345af050070d24e88ffe45`
- `DataSheet_2.xlsx`, `PERCENT %` source chemical composition: **1,023,324 bytes**, SHA256 `bc3c788793dfd6c26f489d240328882a0adb3025d1afd5ddfe49d2ec1b221e79`
- `DataSheet_3.xlsx`, `EM. RATE` chemical emission: **1,542,488 bytes**, SHA256 `1b25abdad31a2ede3032b654eac7b452ccfa60784cc3e44cc41a626f2e16a17a`

The genuine original workbook headers contain:
`Source article`, `Species`, `APG III synonims`, `wind`, `animal`, `insect`, `lepidoptera`, `coleoptera`, `diptera`, `hymenoptera`, `bat`, `bird`, author compiled temperature and precipitation, source total floral VOC emission rate units **μg/h/flower**, **μg/h/inflorescence**, **μg/h/gDW**, **μg/h/gFW**, then named compounds across ~850 columns. In the original 2020 table, **`wind` is a wind-*pollination mode flag*, NOT atmospheric wind speed**. Likewise the source compilation's ecological guild flags are authors' pollination-mode coding, not independent raw observed *Bombus* visits at EuPPollNet site times. Original compound zeros/missing are not assumed emitted source site negative across all sources.

Original source `DataSheet_1` has **306 data plant rows** (307 including source first row), the other two **305 data rows** (306 with header). Stage77D source strict "Genus species" semantic taxon label extraction yields **291** candidate Latin binomial names, fewer than reported 305 (other source original labels include unresolved names/taxon authorship): compare **47** exact lexical names with the **1,408** observed EuPPollNet species, **43** with exact NHM botanical text, and only **5** with the source **233** explicit single-hue botanical lexical species. *These counts are names, not co-measured same-location field scent+visual+visitation records*.

**Independently authenticated DIRECT 2024 petal-spectrometer × 2020 scent × recorded EuPPollNet intersection:** The source Stage68 original 73 measured species from the original 2024 true petal 300–399nm reflectance study (original spectral source crosswalk SHA256 e574fb9b58bc8b9e5fe620852d0e138c1f7f7f5c544f98e14a2673a85202a6f8) yielded 73 distinct plant names; 36 of these appear in actual corrected EuPPollNet visitor records. Of the 73, **just ONE species, *Knautia arvensis*, also occurs in the authenticated original author 2020 floral VOC tables**, and that species also occurs in the genuine EuPPollNet field-visitor plant names. Thus **1/73 spectral species; 1/36 spectral species with real visitor records; and one cross-source biological taxon** for the three modalities; this is NOT one field-local, cotemporaneous source of measured floral spectrum, chemical emission and visitor response. In particular, do not fit or claim a wind × measured UV × VOC scent-mediated Bombus path or 1 independent evolutionary replicate from these non-coincident datasets. This is an empirical data-identifiability finding, not evidence that floral scent has no ecological function.

[Original member actual-source CI 44209990991](https://github.com/zuizui0223/adaptive-gain/actions/runs/44209990991) **SUCCESS** with 8 original botanical-taxon/spectrometer-source safeguards and all three authentic VOC XLSX member SHA256 independently confirmed across two original source downloads. Derived result artifact **14384229987**, ZIP SHA256 **4d0e8fe0d19f134c30a787a7fa83a058d0ab9df93c5c934ade335de96cfe80bb**.

### Why **real causal scent-mediated path** must remain closed

The 2020 305-species data are an independent published chemical compilation and have same-species **different studies/sites/times** relative to original EuPPollNet observed insects. There is no valid source row for **same-site 1970–2000 climatological wind normal → contemporaneous measured emitted floral scent at that original EuPPollNet flower → insect olfactory reception → choice → fitness**. Matching 5 original species does not supply 5 independent valid *same site* multisensory path triples. Therefore:

\[
W_{\mathrm{actual}} \to \mathrm{odor\ plume}_{\mathrm{coincident}} \to
B_{\mathrm{recorded}}
\]

and

\[
(V_\mathrm{measured\ in\ wild},S_\mathrm{measured\ in\ wild}) \times
W_\mathrm{actual}
\to B_\mathrm{field}
\]

are **NOT IDENTIFIED**. In particular do **not** put `source wind pollination=1` into any atmospheric wind model, impute unobserved VOC as 0, treat taxon-level source chemical signals as site-autonomous behavior, or use compiled guild codes to independently "validate" realized EuPP visitor effect.

## Clear next real macro-science gate, not more single-species examples or island work

The current earned outcome is a completed **original-source continental macro wind–flower visual–real Bombus encounter analysis** with an exploratory four-path adjustment screen, plus authentic independent 305-species floral VOC original database with limited 5-taxon strict visual-hue overlap. The four path intervals include zero, so this run does not support an environmental wind moderation general rule; it does document an observational study design and co-measurement insufficiency. No global fit, causal mediation, species-level phylogenetic effect, direct wild spectral guides or bee receptor color contrast yet.

Next steps for the MACRO hypothesis are **dataset-building**, not further relaxing a preferred beta:
1. Build a broader independent source-based floral visual optical signal atlas (true 300–700nm spectra and spatial UV guide separate) beyond only 233 lexical hue species, and a broader multi-study original floral scent emission coverage. Use exact accepted plant labels and identify source site/year for both. The 2020 305-species original table contains only 47 source EuPPollNet overlap plants.
2. Obtain a true *Bombus* receiver opportunity predictor across EuPP field survey sites that is **independent of the original recorded visitation dataset**; joint habitat/climate/effort modeling must distinguish suitable, detected, inadequately observed and structurally unavailable. Only positively observed visitors can be used as an actual realized-visit response.
3. Prospectively test **visual modality × environmental noise × true receiver opportunity**, with study/source and clade controls, not generic yellow–purple association. If scent is not common-site measured, include it only as a separate literature-level trait meta-analysis or a future measured predictor, **not a mediated link**.
4. Treat local meteorological wind observations, canopy/background and source sampling effort as important requirements for causal interpretation. Climate normals only describe broad background. Preserve studies and taxon lineages as independent sampling/grain structures.

## Reproducibility and branch instructions

Source-specified research:
- `research/floral_macro_stage77/assemble_source_worldclim_wind_climate_sites.py` + **9** tests
- `research/floral_macro_stage77/source_observational_visual_wind_climate_Bombus_piecewise.py` + **8** tests
- `research/floral_macro_stage77/audit_original_multispecies_floral_VOC_sources.py` + **6** tests
- `research/floral_macro_stage77/reconstruct_original_multispecies_VOC_XLSX_species_overlap.py` + **8** tests
- Four corresponding source-verified GitHub workflows `.github/workflows/floral-stage77-real-worldclim-wind-bombus-path.yml`, `floral-stage77b-visual-wind-piecewise-macro.yml`, `floral-stage77c-source-VOC-macro-access.yml`, `floral-stage77d-source-VOC-species-extract.yml`.

All **31 mock unit tests PASS** across the four workflows, and each workflow re-reads real, independently checksum-verified scientific source data. Source full original chemistry binary not redistributed via GitHub artifacts; only source computed audit receipts and source hash/metadata.

The branch is **not** merged to `main`; review as separate Draft stacked directly above the main Stage75 continental macro PR #154. Do NOT reintroduce island floras, reclassified island Bombus absences, or assume the already published one-species UV guide experiment is a global macro result.
