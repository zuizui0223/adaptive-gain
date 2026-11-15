# Stage33 — pollinator learning × wind-mediated scent transport × landing control

**2026-11-15. NEW exact source-free stage decomposition and a source-backed study/data ledger. NO observed wind-specific cognition effect, pooled meta result or experimental plant fitness estimate is claimed.** This study branch builds on Stage32 PR #111. All earlier stages, authors' raw data, V5/V6 and main remain unchanged.

## Main ecological hypothesis: dual wind pathways and conditional compensation

Airflow can enlarge, shape and transport an odor plume; modest advection may improve odor encounters and search. Wind also changes plume intermittency, dilution and chemical composition, so discovery can become less reliable at high/turbulent wind or for chemically degraded blends. Simultaneously airflow destabilizes pollinator trajectories, changes the flower's motion, raises energy/motor demands and can reduce landing frequency, with sensory-motor learning/skill partially compensating.

**Core falsifiable prediction:** the net wind effect on a flower is NOT generally monotone. It depends on where wind acts in a sequential encounter process, on whether vision supplements an unreliable odor signal, on the receiver's learned/innate response and motor compensation, and on the plant's pollen deposition after each successful encounter. Being "smart", learning colors quickly, and being an efficient pollinator are THREE different, separately measured things. No hoverfly, moth, solitary bee or butterfly is assigned "random behavior" merely by order; Kandori et al. 2021 DOI 10.1111/1440-1703.12249 found that ALL eight tested taxa learned color-reward associations. The authors used different flower colors/arena sizes and odor/reward conditions across groups; the rankings are task-specific, not IQ labels.

## Three-stage mechanism

For an ORIGINAL shared encounter opportunity define:
- D(w) = probability of discovering a plant/flower/scent source given wind state w, source display and guild;
- L(w) = probability of successful landing given that discovery, including approach and wind-driven flower sway;
- T(w) = probability of true plant pollen transfer given landing (not mere pollen reward collection).

Then, for a matched cohort only, expected successful transfer per opportunity V(w) = D(w)*L(w)*T(w). The *exact ordered decomposition* for two wind states (0 calm, 1 wind) is

    V1 - V0
      = (D1 - D0)*L0*T0                [remote scent/visible discovery]
      + D1*(L1 - L0)*T0                [mechanical landing]
      + D1*L1*(T1 - T0).               [transfer quality after landing]

This is a chain-rule identity, not a fitted causal mediator model. The first term also includes other discoverability changes unless the original experimental treatment isolates scent. The second is a conditional movement effect, not a measure of cognitive ability. The third allows more between-plant outcross visits even if total visits decline; such a hypothesis requires original pollen/deposition records, not flower-switch observations alone.

### Hypothetical constructive results, NOT insect observations

Set calm D0=.30, L0=.80, T0=.75; thus V0=.18.

| Hypothetical state | D | L | T | V | V−V0 |
|---|---:|---:|---:|---:|---:|
| Calm | .30 | .80 | .75 | .1800 | 0 |
| Moderate wind, stronger scent reach | .60 | .50 | .75 | .2250 | +.0450 |
| Strong wind, landing loss | .70 | .20 | .75 | .1050 | −.0750 |
| Same strong wind, better sensorimotor compensation | .70 | .70 | .75 | .3675 | +.1875 |

For the moderate-wind synthetic example, the remote discovery component is +.18 and mechanical landing component −.135; net +.045. The example is a nontrivial proof that positive attraction and negative landing can coexist and that the net sign can change. It does NOT predict a windspeed threshold or establish relative real-world Bombus vs hoverfly advantage.

If per-landing transfer T does not change, a necessary break-even for increased expected transfer is L1 > D0*L0/D1. In the moderate example this is L1 > .40. **Every factor requires matched original experimental denominators and wind exposure information**; different papers' source-visit and landing outcomes cannot be multiplied as if measured on the same individuals.

## Existing empirical evidence, with distinct ecological and causal limits

1. **Wind may improve odor-source arrivals:** Crall et al. 2020 DOI 10.1098/rsbl.2020.0103, male orchid bee *Euglossini* visits at *artificial scent-collection stations* rose with within-site wind speed/turbulence. Original published Zenodo 10.5281/zenodo.3675327 (two data tables + R). This is source-location behavior, NOT pollen transfer to naturally scented flowers.
2. **Wind can alter landing mechanics:** Chang et al. 2016 DOI 10.1242/jeb.137976 (raw landing trajectories on Zenodo 10.5281/zenodo.60234) and Goyal et al. 2024 DOI 10.1242/jeb.245432 (Mendeley Data 10.17632/mww9m8r3dk.1, 19,421 recorded landing maneuvers). The 2024 experiment found landing frequency lower at high sidewinds while bumblebees compensated hover/approach behavior. The flight paths are repeat measures; do not count 19,421 approaches as independent bees.
3. **Wind-driven flower movement matters but can be compensated:** 2025 DOI 10.1242/jeb.249380, original Dryad 10.5061/dryad.qbzkh18tj, moving artificial flower: Bombus terrestris landing success dropped at 0.65 Hz but not below 0.53 Hz for this setup. Motion frequency is NOT wind speed; do not convert to a field airflow threshold.
4. **Wind is also a guild/community filter:** Balfour & Ratnieks 2025 DOI 10.1093/beheco/araf067, original Dryad 10.5061/dryad.4qrfj6qpf published 2026. The field study finds ~2.94-fold more pollinators and ~2.5-fold more taxa under weak vs moderately strong wind, flower visit rate ~15% faster in lower wind, but greater between-inflorescence moves at higher wind. Fly, butterfly and bee compositions shift, so a guild-level "flower visits" effect is not one cognition score. The Dryad README lists 148 census rows, 329 foraging observations and 210 switches; the paper text mentions 330 and 211 for its respective observation sets. These different counts require a SOURCE/EXCLUSION reconciliation before any new raw-data effect extraction; not currently evidence of an error.
5. **Wind can change odor information quality:** Lawson et al. 2017 DOI 10.1098/rsos.170996 shows flower color can back up an unreliable scent under olfactory noise in Bombus. A wind-tunnel VOC × ozone experiment DOI 10.1016/j.envpol.2023.122336 finds honeybee recognition of center-plume VOC mixtures 52% at 6 m vs 38% at 12 m, edge-plume 32% vs 10%, in those experimental conditions. Do NOT extrapolate these numbers to clean natural air or all species.
6. **Near-surface plume physics is contextual:** Houle & van Breugel 2023 DOI 10.1063/5.0147945, wind-direction variability depends on local vegetation/surface complexity and temporal scale; chemical plume presence, mean speed and turbulence are not interchangeable. Botanical visual and odor signal associations need measured source-specific conditions.

## Next multi-source meta-analysis: prespecified estimands, no fabricated pooled coefficients

A. In **scent source attraction experiments**, estimate log relative source encounters per observer-hour or trap-hour and confidence interval based on independent site/collection-session replicates, wind mean/direction/turbulence and odor controls; separate original orchid-bee perfume collection from nectar-foraging flowers.

B. In **flower landing experiments**, estimate conditional landing odds / landing rate ratios by original bee ID and session, versus wind exposure and flower motion. Keep sidewind, headwind, plume turbulence, and oscillating flower treatments as distinct moderators. Add individual experience and visual/scent-guide availability where experimental, and measured body size/load rather than order-level "intelligence".

C. In **pollen transfer / plant reproduction**, estimate stigma deposition and seeds/siring only from original plant source records. **Between-inflorescence switching is a hypothesis for improved outcrossing, not direct fitness evidence**.

D. In **wind×signal factorial experiments**, preregister within-original-experiment interaction for odor intensity or blend × airflow, scent × visual guide under airflow/noise, and structural display × sway. Multiple cue combinations and guild-level groups require multilevel repeated-subject effects, not one row per photo/frame.

E. For **macroecological effect modification**, join measured site × date/hour wind to floral original traits (display area, UV-vis spectral contrast, VOC blend/flux, flower stiffness/height), pollinator morphology and empirically measured learning/motor control and guild occupancy. Keep missing modalities explicit; population-by-region/bird/bat comparisons follow source QA. Treat weather station speed and wind-gust proxy separately from flower-height plume turbulence and local leeward microclimates. Control land use, temperature, flower abundance, reward and observation effort in matching/causal models.

**Meta-analysis likelihood:** different stage-specific families (count rate, Bernoulli landing, measured pollen deposition and seed fitness) with separate sampling variances, within-study and within-bee covariance, plant/pollinator taxa and source random effects. The cross-stage transportability hypothesis is TESTED only where two stages share same source grains. There is no global pooled signed wind effect in this branch.

## Implemented and remaining work

- KANDORI_2021_EIGHT_TAXA_TASK_ATLAS.csv: eight taxa from the primary color-learning paper; records NO quantitative learning rate or same-animal pollen transfer, and warns all tested visitors learned.
- COMPARATIVE_RECEIVER_EVIDENCE_LEDGER.csv: cognitive/behavior vs pollen efficiency prior art, not joined individual outcomes.
- receiver_cognition_route_value.py: exact hypothetical counterexamples proving cue-use and per-landing transfer efficiency need not rank together and that the plant can benefit while the receiver pays a cost.
- WIND_DUAL_PATH_EVIDENCE_LEDGER.csv: ten source-linked observations across different stages, with original data DOI candidates.
- wind_dual_path.py: exact multi-stage wind decomposition, break-even diagnostic, microenvironment original-event contract, null/missingness propagation and source ledger QA; numerical scenarios are exclusively source-free.
- Focused Python unit tests and an isolated GitHub CI gate, plus general Python 3.10–3.12 repository test matrix as a separate check.

**Scientific STOP:** zero NEW independently reconstructed original wind experiment effect sizes/variances in Stage33, zero observed same-individual learning×landing×pollen pathway, zero verified universal guild cognitive ranking and no measured causal flower fitness benefit. Pending raw-data analysis: 2020 Zenodo orchid-bee scent sessions, 2026 Dryad Balfour wind field records, 2024 Mendeley bumblebee landing data, and available open scent quality/factorial experiments. The preceding Stage32 Dryad UV manipulation workbook automatic API download returned HTTP 401, so UV effects are still not extracted.
