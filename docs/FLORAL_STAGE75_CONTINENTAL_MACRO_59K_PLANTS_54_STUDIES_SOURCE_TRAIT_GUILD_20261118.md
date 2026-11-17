# Stage75 | Continental floral visual *source TEXT* × independently observed guild networks — macroscale line restored

2026-11-18 JST. **This is the macroecology primary line, not another single-species UV/light experiment.** Stacks directly on Stage71 PR #150, deliberately **does NOT depend on Stages72–74** source-case branches, whose UV manipulation and scent experiments remain independent mechanistic background. `main` untouched, Draft/unmerged.

Verified original datasets and reproducible source execution [GitHub Actions 44117438149](https://github.com/zuizui0223/adaptive-gain/actions/runs/44117438149) **SUCCESS**, source artifact **14344346006** SHA256 `895f6f14e500dc5efd2e1a730ada3cc02995aaaae7754f3ddae67accbf919f8a`, **10 synthetic trait/group tests + 5 genus/context controls**, 54 real studies.

## Actual sample sizes and independent measurement grain

Original NHM text `NaturalHistoryMuseum/plant-traits` (CC-BY original BHL/eFloras/Ecoflora botanical prose): original pinned `combined.csv` SHA-pinned in Stage68. The actual derived source compact **11,119,044 bytes**, SHA256 `b81ab96a2883e2b2e7f254a9e7ab62a34afaa0dfe62f0062d1677ba852dc686a`, contains **59,369 taxon labels**, **31,773** with flower/petal/corolla visible-colour text, and **925** with positively reported flower/petal/corolla `spot` or `spotted` tokens. These are text extraction labels, NOT spectrometer measurements or observed UV nectar guides. A nonreported spot or hue is **UNKNOWN**, not a confirmed source flower without marking.

Original independently observed EuPPollNet author-corrected `v1.3.0` (2025 Lanuza et al., DOI 10.1111/geb.70000, correction DOI 10.1111/geb.70054, source DOI 10.5281/zenodo.15183272): **623,476** original observed plant–visitor records from **54** original study IDs across **1,864** study×network×year units in **23** European country labels and **7** source Bioregions. Stage69 source-derived network×plant compact **18,798** rows, SHA256 `475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617`. The original 623,476 source rows are **not** 623,476 independent plant species or sites; original 1,864 networks are **not** 1,864 independently evolved floral phenotypes.

Original exactly name-matched **963 species** across botanical textual traits and *recorded-visitation* EuPPollNet. Of these, **809 species** have any colour text, **233 species** have exactly one distinctly identifiable lexically reported colour family after distinguishing `yellowish` as yellow; **625 networks** have >=2 such species, of which **424 networks across 43 distinct original studies** have >=2 genuinely different source-recorded hue families. Earlier provisional **245 single-hue / 434 contrasting networks** was incorrect because an exploratory parser failed to classify source `yellowish` as part of the yellow family. The final corrected parser and CI now **fix 233/625/424/43**.

The original 963 source-matched plants also include only **31** with positively reported `spot`/`spotted` wording; original global corpus includes **925** taxon labels with positive textual spot mentions. These **are not 31 confirmed UV nectar-guide positive species**. Importantly, all other source plants lack a verified negative marking state; no defensible binary `has_guide=0` can be assigned from this text alone. Therefore, **no macro UV nectar-guide presence/absence selection coefficient has been estimated**.

## Prespecified actual guild comparisons after sample selection

To avoid the Stage69B bias that preselected study networks by observed guilds, Stage75 freezes each original network on **positive text lexical flora colour alone**, then reads actual original independent pollinator taxa (never guilds inferred from floral colour) and quantifies observed *Bombus* vs other scientifically identified bees. Further filtering for statistical informativeness (two positive hue groups actually visited by bees and both bee channels observed) is assessed **after the base frame is fixed**.

Source lexical phenotype groups are strictly flowers with just one recorded colour FAMILY across `flower colour`, `petal colour`, `corolla colour`; this does NOT mean individuals are biologically monochromatic, a hue is biologically absent, or an actual receiver perceives that colour as the same chromatic signal. Source text variants such as `whitish`, `yellowish`, `violet`, `lilac` are encoded with version-controlled parsing rules, and multi-family textual variants are excluded from this narrow comparison rather than assigned invented phenotypic dominance.

Source original insect observations must satisfy the recorded pollinator taxon `Pollinator_rank=SPECIES`, nonaffirmative `Pollinator_unsure_id`, `Pollinator_order=Hymenoptera` and source family/genus `Bombus` vs recognized other bee families. An original no-record does NOT prove bee biological absence; study methods can sample only selected pollinator groups. Site/study/bioregion information is from **actual original source `Country`, `Bioregion`, `EuPPollNet_habitat` and source sampling method**, not inferred from a photo or a species' colour.

Prespecified null-local descriptive score against a study×network×year intercept is the source-exact observed bee composition score / expected Fisher information ratio `ΣU_k / ΣI_k` at coefficient=0. It is **NOT fitted maximum-likelihood logit beta, odds ratio, phylogenetically corrected contrast, p-value, fixed-effect standard error, or causal selection evidence**. Study-block bootstrap (2,000 seed-fixed study resamples) ranges are **descriptive sensitivity bands** and do not supply an independent species-level evolutionary confidence interval.

| Comparison | Original pre-guild networks with both recorded hue states | Original source studies at entry | Strict-bee informative networks | Strict-bee informative studies | Null-local score/information ratio | Descriptive study-block percentile range |
|---|---:|---:|---:|---:|---:|---|
| **Yellow lexical-only vs white lexical-only** | **345** | **42** | **84** | **21** | **+0.0763** | **−0.731 to +1.316** |
| **Yellow lexical-only vs purple lexical-only** | **65** | **21** | **25** | **13** | **−1.3703** | **−3.245 to −0.341** |

These are **recorded conditional visitation categories**, not directly measured causal receiver preferences.

**Yellow versus white:** Essentially no stable overall association. Negative and positive original study-specific scores compete; 3 leave-one-study-out operations and 3 leave-one-genus-out operations change the pooled null-local score sign. The four source Bioregion strata with informative original data give score ratios:
- Continental: 51 networks/12 studies, **+1.1148**;
- Atlantic: 24/6, **−0.0855**;
- Mediterranean: 2/2, **−0.9197**;
- Alpine: 7/3, **−0.0199**.

This is an **observational research-region difference**, not a direct effect of climate or a biological demonstration that colour itself causes visitation preference. Mediterranean coverage is only 2 informative networks and high relative sampling information from certain recorded plants.

**Yellow versus purple:** Exploratory negative score in the sample; it does not change sign under exclusion of any one of the 13 informative study IDs or any one of 65 genus labels in this source. Its study-block descriptive interval is negative, but that **cannot be promoted into confirmatory biological evidence** because the label is extracted from heterogeneous botanical prose, plant source population colour and genuine insect receptor contrast are unmeasured, original host plants are observed and not guaranteed native, and **true within-genus, same-network comparisons are extremely restricted**. The four source bioregion strata are:
- Continental 11 networks/5 studies: −2.3219;
- Atlantic 8/4: −0.7256;
- Alpine 3/3: −4.1821;
- Mediterranean 3/2: −1.5286.

The apparent region-wide direction may simply reflect lineage, actual flora traits correlated with species or source study methods, not a universal bee response to "yellow vs purple".

## Critical independent genus/phylogeny admissions

Genus controls use real source species names. Genus is **not a rooted genus-level or species-level phylogeny** and genus omission is not an equivalent substitute for a phylogenetic hierarchical regression.

| Source hue pair | Total distinct genera in source frame | Same-genus networks with both source hues | Same-genus networks with informative strict bee composition | Genuinely distinct informative genus comparisons |
|---|---:|---:|---:|---:|
| Yellow/white | 100 | 12 | **4** | **1 genus: Melilotus** |
| Yellow/purple | 65 | 4 | **4** | **1 genus: Teucrium** |

The within-genus score ratio is +2.114 (yellow vs white) and −1.279 (yellow vs purple), but these are **single-genus observational case comparisons, not phylogenetically replicated macro evolutionary effects**. They must never be described as 4 independent clade origins or as proof that nectar guides are adapted to *Bombus*. The macro dataset still lacks independent color-state variation across sufficiently many well-measured clades; a species fixed effect would absorb a species-constant NLP colour label.

## Spatial, environmental and observation confounding

- 1,864 source networks span **7** bioregions (Alpine, Atlantic, Boreal, Continental, Mediterranean, Pannonian, Steppic) and **23** country labels, but the informative yellow/white and yellow/purple subsets occupy only **4** bioregions each. In original 1,864 source network-year units, **6** have more than one source latitude and **11** have multiple habitat labels. They are flagged rather than arbitrarily assigned.
- Conditioning on original network reduces **shared measured site/source study/time** differences, but cannot identify measured wind, UV illumination intensity, canopy background, floral VOC, site-specific native flora status or the abundance/visitation sampling effort per flower.
- Both species phenotype and pollinator guild are cross-sectionally observed; no validated *Bombus* presence–absence or accessible pollinator niche probability is attached. A missing guild recording cannot be treated as pollinator exclusion. Source original guild composition is observational, not proven pollen deposition.
- Existing Stage71 full original floral census check established original mixed units (percent cover, flowers/m², inflorescences) and cannot standardize all visits per flower. Reusing species with repeated network records without clade controls can generate pseudoreplication.
- **This is continental, not yet a genuine global plant/bee origin analysis**. The 59k global textual source by itself has no true same-site guild opportunity, and it cannot be combined with global bee absence simply from unobserved GBIF data.

## Interpretation and next MACRO task (not more individual case studies)

The defensible observational macro result is: a **reported colour-token × recorded insect-guild association is heterogeneous by region and taxonomic origin**, with yellow–white not directionally stable, and yellow–purple exploratory negative but underidentified phylogenetic replication. This shows why a crude scalar flower-colour-versus-Bombus regression or a "floral information complexity" index is unsuited as a general mechanism.

**Next required truly macro-scale work:**
1. Add independent GBIF/WCVP validated species native distributions and existing source-authenticated modelled *Bombus* receiver opportunity (only modeled-eligible hex cells, NOT unknown cells as absence). Retain location/time/coarse climate/bioregion terms, and genuine plant visual modality distinct from text lexical hue.
2. Expand the **global source-presence visual trait evidence** beyond prose colour categories: original measured UV spatial guides, spectral receptor contrast, direct flower age change, nectar guide pattern and scent where independently measured. Treat source missingness as missing, keep separate evidence types. Source origin, taxon concept, site/year, study version and receiver guild all traceable.
3. Fit a prospective hierarchical macro association with source geographical study effects, separate clade dependence, climate and sampling-effort guardrails. Test whether environmental receiver-channel loss predicts *variation in the payoff of measured modalities*, not merely hue richness.
4. If independent sources cannot support the mechanism, restrict a paper to dataset coverage/observation bias or an explicitly descriptive continental guild association. Do not use a single 2021 UV experiment as a substitute for the macro dataset.

**NO new global causal SEM, wind×VOC mediation, phylogenetically validated general pollination syndrome, or selection/adaptation effect is established in Stage75.**

## Source-executable evidence and controls

- `research/floral_macro_stage75/authentic_continental_text_signal_guild_macro.py`: original full NHM59k + actual corrected EuPPollNet 623,476 source bytes, strictly lexical hues, 963 real species source-matched, and observational source within-network strict bee-guild contrasts.
- `research/floral_macro_stage75/source_macro_genus_bioregion_sensitivity.py`: source-pinned original derived macro artifact SHA, source-genus deletion, within-genus contrasts and original bioregion/habitat strata.
- `research/floral_macro_stage75/test_authentic_continental_text_signal_guild_macro.py` and `test_source_macro_genus_bioregion_sensitivity.py`: **15 synthetic/mocked source invariant tests PASS**.
- `.github/workflows/floral-stage75-original-continental-source-macro.yml`: full real original dataset ingestion via author-verified source artifacts from [Stage68](https://github.com/zuizui0223/adaptive-gain/actions/runs/44051561567) and [Stage69](https://github.com/zuizui0223/adaptive-gain/actions/runs/44057077625), SHA checks, all source trait/guild/country/bioregion counts, independent study/genus sensitivity and downloadable source derived matrices.
- Final **SUCCESS** [44117438149](https://github.com/zuizui0223/adaptive-gain/actions/runs/44117438149), artifact **14344346006**, ZIP SHA256 `895f6f14e500dc5efd2e1a730ada3cc02995aaaae7754f3ddae67accbf919f8a`.

This is a **completed large-scale quantitative data audit and exploratory observational macro test** with explicit inference ceilings, not a polished causal evolution result or a proposal that has not been executed.
