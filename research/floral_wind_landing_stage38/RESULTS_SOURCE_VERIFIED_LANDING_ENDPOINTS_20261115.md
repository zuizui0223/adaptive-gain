# Stage38 — independent wind-landing sources: original data and denominator audit

**2026-11-15. Original source authentication plus published-rate comparisons. NOT a pooled causal wind×scent experiment or a new seed-fitness estimate.** Stacked on Stage37 PR #117; main and prior stages unchanged.

## Two independent wind mechanisms cannot be multiplied into plant fitness

Stage37: Crall et al. 2020 (DOI 10.1098/rsbl.2020.0103, Zenodo 10.5281/zenodo.3743898), 70 existing 20-minute male orchid-bee scent-bait sessions, nine sites, 29 dates, 409 collected bees. Within-site wind doubling was associated with 1.3985-fold bait arrivals (site×date two-way approximate IRR interval 1.0966–1.7836). Mean wind values in this source were 0.0206–0.73 m/s. This is not a natural floral pollen-transfer response.

### Chang et al. (2016) original headwind landing records — obtained and authenticated

Paper DOI 10.1242/jeb.137976; dataset https://zenodo.org/records/60234. Exact source filename: ChangCrallCombes_WindAltersLandingDynamicsInBumblebeeData.zip; MD5 22bbc8286fecd2535d3f284679aed87b.

The Stage38 dedicated original-source audit downloaded the REAL publicly archived ZIP and verified the file checksum. The ZIP contains 905 entries, including many Mac OS metadata sidecars, figures, source code and kinematic files. Exactly 157 genuine original xyzpts.csv files have lexical W0 and W1 tokens (56 and 101 files, respectively); there are 28 distinct filename B-label identifiers. Do NOT equate file count with independent bees, the paper's selected comparison N, or an unknown denominator of failed landings. One original source trajectory CSV has 21 columns of 3-D coordinates for seven tracking markers, labeled pt1_X/Y/Z to pt7_X/Y/Z. Further raw kinematic reconstruction requires original frame rate, spatial calibration and physical time mapping; those data have NOT been analyzed here.

The *already published* Chang experiment reported still-air mean speed change between approach and landing −0.171 m/s versus −0.004 m/s in 3.5 m/s headwind, alongside higher landing impact deceleration. These are existing paper figures, not newly reconstructed from archived CSVs. The species is Bombus impatiens, and the source primarily records landing trajectories.

### Goyal et al. (2024) sidewind landing frequency — published benchmark, original MAT unavailable

Paper DOI 10.1242/jeb.245432. Author dataset https://doi.org/10.17632/mww9m8r3dk.1 (Mendeley, CC BY 4.0), describing 19,421 recorded successful landing trajectories under six sidewind conditions 0–3.4 m/s. Of these, 16,374 are from free flight and 3,047 directly after takeoff. **These tracked successful maneuvers lack the denominator of all attempted landings.**

The authors report hourly landing FREQUENCY, NOT conditional landing probability:
- Free flight: calm 280.8 h^-1, high sidewind 112.2 h^-1; ratio 0.39957, **60.04% fewer landings per hour**.
- After takeoff: calm 56.0 h^-1, high sidewind 16.5 h^-1; ratio 0.29464, **70.54% fewer**.

These descriptive effect ratios are independently calculated from PAPER REPORTED MEANS. Published SEMs for each mean do not automatically identify a ratio CI or the effective independent day/colony counts. Original MATLAB data and experiment-specific failed approach counts were NOT independently refit. The public Mendeley API request returned HTTP 401 in the dedicated Stage38 workflow, so there is no claim that the original MAT file was downloaded.

The author analysis code for Goyal is independently available from GitHub kaku289/nimble-bbee-analysis branch landing_steady_winds, commit 1792f8a9c95509fb3aa4783b26e7727a9cb3f871. The code separates wind treatments, landing from free flight vs takeoff and original dates; the source code is not a substitute for the inaccessible MAT original data.

### Independent guild-level field prior art (not yet analyzed from original Dryad ZIP)

Balfour and Ratnieks 2025, paper DOI 10.1093/beheco/araf067; Dryad DOI 10.5061/dryad.4qrfj6qpf (released May 15, 2026). Their published low (<0.5m/s) vs moderate (>2.5m/s) wind field study reports approximately threefold pollinator abundance and double richness under low wind, guild-composition changes, slower bee foraging in wind, but more between-inflorescence movements in wind. The Dryad README specifies 148 survey rows, 329 foraging records and 210 switch records. No original raw Dryad ZIP downloaded, so these remain previously published source results, not new extracted coefficients.

## Scientific distinction and next experiment

**Across independent settings**, scent-bait arrivals can be positively wind-associated while successful bee landing FREQUENCY is negatively wind-associated at much higher wind. These sources involve different genera/species, wind ranges, sensory tasks, and original experimental cohorts; neither data source measures full encounter/detection/landing/pollen-transfer path. No estimate of a wind×natural floral scent ON/OFF interaction, no conditional landing success probability, and no net reproductive benefit or species-wide ranking is available.

The scientifically decisive factorial design is randomized matched intact scented vs experimentally scent-suppressed flowers crossed with multiple measured airflow regimes and marked pollinator identities. Measure source odor plume, true approach opportunities, observed attempted landings, actual successful landings and original stigma deposition / seed siring on the SAME treatment/session cohort. Pair with independently measured learning and motor skill rather than using Bombus/hoverfly taxonomic labels as IQ proxies.

## Implemented verification

- Source-locked landing_original_sources.py audits Zenodo #60234 archive title/author/checksum and original ZIP structure, 3-D trajectory column metadata, Mendeley API status; preserves publication-derived hourly landing ratios with a conspicuous distinction between landing frequency and success probability.
- Synthetic-only test_landing_original_sources.py validates source identity, no fake attempts, biological no-go and extraction rules (10 tests).
- Dedicated floral-stage38-wind-landing.yml downloads original Zenodo ZIP to ephemeral runner memory, saves only aggregate JSON receipt and never authors' raw tracks.
- Original Mendeley MAT and Dryad Balfour files are still unextracted. Whole-repository test matrix must be separately confirmed. Draft only; no merge.
