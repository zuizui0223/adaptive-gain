# Stage52 — original 2016 UV species × source-modelled Bombus guild geography

**2026-11-16 JST. Status: authentic source geospatial pilot + descriptive guild analysis completed. NO causal/adjusted UV×Bombus effect.** Branch stacked on Stage51, which corrected source-region GBIF sampling. Source original study: Koski & Ashman, New Phytologist (2016), [doi:10.1111/nph.13921](https://doi.org/10.1111/nph.13921); source-authenticated Table S2 with direct UV petal phenotypes.

## Current state and what actually ran

Source original Table S2 has **177 UV-phototyped plant taxon rows**. After resolving accepted names and infraspecific duplication: **159 unique accepted GBIF species**, **81 original UV-uniform** and **78 original UV-patterned**, 164 mapped source taxon rows. All 159 species have source-paper average latitude, UV-B irradiance, annual temperature and precipitation.

The paper explicitly states the species averages range from **21.07°N to 76.49°N** with overall mean c.43.04°N; the automated initial Stage52 source receipt's caution that original signedness was still unverified was superseded by the manual journal-text verification. The southern GBIF source search is a **negative-control** for occurrence/source overlap, not an equally plausible reconstruction of the paper's stated northern source means.

| Actual original 2016 source means (159 accepted species) | UV uniform (81) | UV patterned (78) |
| --- | ---: | ---: |
| Original mean latitude, degrees N | 43.79 | 42.53 |
| Original mean temperature °C | 3.90 | 5.59 |
| Original mean UV-B J m^-2 d^-1 | 2984.16 | 3037.88 |

**Precommitted spatial probe:** independent source-latitude-ranked terciles in each UV class, 10 hashed species per tercile×UV status → **60 species, 30+30**. Original source latitude ±4° GBIF search, one bounded first 100 indexed plant occurrence records per species in the **northern study latitude**, and a *separate* southern negative-control; same taxonKey, 2000–2026, coordinate uncertainty <=10km, explicitly introduced/managed excluded. Source bee geographical predictions: original Laborieux 2026 3,370-model-taxon filter, 133 source Bombus names, exact original author HEX polygon/CRS, 2,695 eligible bee model cells out of 10,242 source HEX.

**Original source CI** [Actions 43872982408](https://github.com/zuizui0223/adaptive-gain/actions/runs/43872982408) **SUCCESS**: 45/60 species have >=5 coordinate-validated, source-bee-model-eligible original northern GBIF records; 0 corresponding southern negative-control species reach >=5 original-source-eligible records; **44** northern species reach the prespecified stricter analysis grain >=5 original-source-eligible records in >=2 modeled HEX.

## Primary exploratory descriptive outputs (NOT a significance test)

Each original plant species is weighted equally. Within each species, the original source modelled taxon richness is averaged over eligible bee-model cells reached by the bounded plant GBIF record page. The **Bombus fraction proxy** is each species' mean modelled Bombus taxon count divided by its mean modelled all-bee taxon count; it is then averaged equally over plants. This is emphatically **not** an abundance ratio, native pollinator availability or visitation mechanism.

| Original 2016 plant UV status | Viable plant species | Mean modelled Bombus species names | Mean modelled all-bee names | Species-equal mean Bombus/all-bee ratio |
|---|---:|---:|---:|---:|
| UV uniform | 24 | 4.198 | 189.540 | 0.08444 |
| UV spatially patterned | 20 | 6.347 | 137.732 | 0.13248 |
| Pattern minus uniform | — | **+2.149** | **−51.808** | **+0.04804** |

**Source sensitivity:** all 44 single-species deletions retain the direction in each of these three metrics. For Bombus relative share, deletion-min/max difference is [+0.02679,+0.06694]. Under a stricter >=10 GBIF quality records and >=3 eligible bee HEX cells the original subset has **33 species** (uniform 19 / patterned 14) and the descriptive Bombus fraction difference remains **+0.02520**. Within original *Potentilla* genus only, **38 species** (uniform 19 / patterned 19) have a positive proxy fraction difference **+0.04105**.

But the three **source latitude terciles are heterogeneous**: pattern-minus-uniform share differences **+0.07186**, **+0.05791**, **−0.01902**. Thus the descriptive positive pooled sign is **not universal across original geographical/climatic source strata**.

Critically, Stage50's *global* GBIF first-page pilot of 2016 flora showed the opposite absolute Bombus difference (uniform 6.26 versus patterned 4.11 modelled names). Source-latitude bounding reversed it (uniform 4.20 versus patterned 6.35), directly illustrating **GBIF sampling frame / geographic source-domain sensitivity**, not discovery of adaptive UV signals.

The original 2016 paper itself reported significant phylogenetic signal for binary UV pattern and ecological associations with UV-B/temperature in its phylogenetic analysis; the descriptive observed bee-model signal therefore remains strongly confounded by lineage, habitat, source original climate and spatial opportunity. Published source means are NOT precise individual UV-phototyped locations; subsequent GBIF plant coordinates cannot be presumed to carry the same measured within-population UV phenotype. Source bee HEX estimates are predicted species-name richness from heterogeneous SDM/polygon input, NOT actual visiting native bees, species abundance, neural information use or plant seed fitness.

## Reproducibility / next gate

- Stage52 source original 159 accepted species latitude/UVB audit [Actions 43872051254](https://github.com/zuizui0223/adaptive-gain/actions/runs/43872051254), derived source artifact 14228751117 (sha256 `65067a852b05c9bed9e0e9974fdf3cbed6a9db71c7393bb32ea0480bd38c2dd5`).
- True first-page original-source HEX point-in-polygon pilot [Actions 43872982408](https://github.com/zuizui0223/adaptive-gain/actions/runs/43872982408), derived source artifact 14228532831 (sha256 `582eb86a23f954e05622301e5411d587b91003d23fbdc2e500cd7f56537aca79`).
- Descriptive Bombus/allbee-ratio robustness [Actions 43874230221](https://github.com/zuizui0223/adaptive-gain/actions/runs/43874230221), artifact 14229800187 (sha256 `0d0d641f07ffe48b9a0faafd6e11aa5011629b15dd0a4a42956a646fe3c7d27f`).
- An additional **post hoc** same-genus, original latitude/UVB/temperature matched-pair analysis is implemented separately. It must be evaluated on real original data and is not preregistered or a causal climate control. Report its outcome whether it supports or reverses the initial sign.

**Next biological evidence gate:** reconstruct the actual native/measurement geography of each source-taxonomically accepted species (original herbarium locality and voucher metadata where possible), build true regional source conditional bee species-composition models, and fit prespecified phylogenetic + climate + spatial + observation-process controls with region held-out validation. The current 44 source species and raw relative fractions do **not** identify a population effect.

Keep Draft/unmerged, main unchanged; do not combine with unrelated wind mechanics or falsely claim a real nectar-guide function.
