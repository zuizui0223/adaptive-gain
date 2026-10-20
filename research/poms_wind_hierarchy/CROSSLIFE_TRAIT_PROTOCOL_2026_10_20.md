# Wind × larval trophic ecology × adult hoverfly occurrence: pre-analysis data-join contract

Recorded 2026-10-20 before inspecting the EuPollTrait original files and before fitting the trait interaction. Worktree only, not frozen manuscript. This continues the independently archived UK PoMS wind / species-turnover analyses.

## Central ecological question

Does **wind filter the captured adult hoverfly assemblage differently depending on the species' larval trophic ecology**, and does the station-level presence of an apparently unrelated plant such as `Urtica dioica` modify this relationship? Adult hoverflies may be flower visitors while their larvae eat aphids, decaying matter, or plant tissue; a life-stage connection links plants, herbivores, hoverflies, and their adults without implying a direct adult flower interaction.

**Important**: No aphids, larval diet, larval hosts or direct trophic links are measured by PoMS. Trait categories are independent external species ecology. A site-level association cannot identify an aphid-mediated causal path.

## Locked original input

1. UK PoMS official pan-trap 2017–2023 original sample/insects/flower tables; EIDC DOI 10.5285/5841bfae-471b-498c-af89-c30e5140d6c5. Individual station × site × calendar date grain; per-station 4–8h exposure; strong QC removes disturbed, duplicate site-date, incomplete wind or invalid observations. Explicit accepted member SHA256s are pinned by `wind_hierarchy.py`.
2. **EuPollTrait**, Miličić et al. *Scientific Data* 2026, DOI 10.1038/s41597-026-07513-8, Zenodo 10.5281/zenodo.18032357; 913 hoverfly species and larval feeding/biology categories within a 3,052 species atlas. Download original repository ZIP, verify published MD5 `7a50cc03e2c5a287e663dc5d029f8026` and compute SHA256. Read `input/trait_data_input.csv` or Darwin Core MeasurementOrFact table plus its metadata. **Do not derive larval feeding class from the same PoMS capture outcome**.
3. Use original `taxon_aggregated` names to harmonize sex-identification variants, preserving species complexes as ambiguous; species-only exact binomial matches are the primary taxonomic bridge. Preserve all unassigned specimens; neither default to aphidophagous nor drop silently without a coverage report.

## Hypothesis tests (priority order)

**H1 primary (trait-mediated wind filter):** On identical site-dates and observed stations with known exposure and wind, compare species-resolved *aphid-feeding* versus *non-aphid-feeding* hoverflies. The target estimand is the **difference between within-site-date wind slopes in taxon-conditioned pan-trap capture**, controlling relative station position, vegetation, sun and temperature; use the stage label "larval aphid-feeding" rather than generalist vs specialist. An indicator for true species-level feeding class is required. If the larval trait is multi-category or missing, allow mixed/uncertain as a separate, not force-resolved class. No directional sign is assumed.

**H2 orthogonal plant bridge:** Among site-dates with flower inventories at **all** sampled trap stations, test whether station-level **recording** of `Urtica dioica` (chosen independently from PoMS because it is frequent and often provides non-floral prey habitat) is associated with relative capture of larval aphid-feeding versus other adult hoverflies, after floral-label richness, same-day wind, exposure, station and microhabitat controls. This is not an observed aphid edge, or proof that a plant not in the list was absent. Only use H2 if the trait coverage and event counts provide support; otherwise record NO-GO.

**H3 optional cross-kingdom context:** If H1 and H2 are analyzable, compare measured plants with independent adult/larval traits and optional nonfocal bycatch groups using grouped out-of-site prediction, controlling the same-site-date totals (conditional allocation). Do NOT automatically call residual co-capture a biotic interaction. Direct species-level predator/prey evidence would be needed to promote a true indirect effect.

## Design and data-validity checks

- Keep the 0–5 Beaufort beginning/end wind scores as **ordinal classes**; no unwarranted m/s conversion. Never use the 10-min FIT leaf-movement ordinal scale as the same numerical predictor.
- The analytical unit is station/date, with nested site/year and per-station counts; multiple specimens from one trap are not independent replicates. At minimum cluster uncertainty by site; report coverage and number of discordant station-date comparisons.
- Conditional site×date normalization removes broad regional phenology, seasonal observer choice, and weather common to that date, but does not remove station microhabitat confounding or trap catchability.
- Avoid performance inflation: choose species traits/labels before looking at trait × wind responses; hold entire sites out for prediction if possible; report all declared comparisons and sensitivity to rare taxa, extreme catches, list completion and species-only harmonization.
- Per species trait coverage and observed capture fractions MUST be reported. Genus-only source labels/ambiguous species groups are excluded from primary trait-comparison denominators; no forced taxon propagation from congeners.
- Outcome may be negatively identified or simply underpowered; do not search post-hoc taxon splits to obtain a positive statement.
- Return an independent real-data claim only if measured effect survives reasonable sensitivity and multiplicity controls. Otherwise retain the useful ecological **limit** and prioritize species-resolved flower-use / aphid surveys.

## Intended outputs

Auditable raw-source digest receipt, file and column inventory, taxon matching coverage, per-guild/event support ledger, trait-linked stationary wind screen, station flower inventory support, exact null or cluster uncertainty, primary + sensitivity effects, tests, verified summary. Do not edit V5/V6 manuscripts.
