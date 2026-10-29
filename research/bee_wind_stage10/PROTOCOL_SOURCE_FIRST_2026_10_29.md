# Stage10 real wind-exposed bumblebee flight trajectories — source-first scientific gate

**2026-10-29; Stage9b positive transfer already frozen and MUST NOT be reused as causal evidence.** This is an independent original-source access and schema audit, not a positive empirical study.

## Source and immutable provider contract
1. Primary candidate: Chang, Crall & Combes 2016, *Wind alters landing dynamics in bumblebees*, Journal of Experimental Biology, DOI 10.1242/jeb.137976. Authors' original Zenodo record https://zenodo.org/records/60234, file `ChangCrallCombes_WindAltersLandingDynamicsInBumblebeeData.zip`, provider-reported MD5 `22bbc8286fecd2535d3f284679aed87b`; expected size roughly 3.4 MB (NOT a byte-exact size contract). Original study compares still air to wind exposure 3.5 m/s using Bombus impatiens.
2. Independent candidate only if this archive cannot be read or subsequent schema is insufficient: Goyal et al. 2024 original Mendeley Data DOI 10.17632/mww9m8r3dk.1, `landingTracks.mat`, 19,421 recorded landing maneuvers across 6 wind exposures (0, 0.3, 1.0, 1.8, 2.5, 3.4 m/s). Mendeley API may require authorization: NEVER substitute metadata for trajectory bytes.
3. Separate moving-target physiology source (NOT wind intervention): Wang et al. 2026, Dryad DOI 10.5061/dryad.37pvmcvzz, `01_Data_Motion.zip`, 3D bee/flower position/velocity at 500Hz. Even if available, this cannot be relabeled as wind exposure or independent natural foraging partner-choice observations.

## Current stage: source access and native schema ONLY
- Download *original provider* archive, require HTTP 200 or safe equivalent, verify entire source MD5, archive integrity, file names/paths, sizes, data types and native variables. Store source URLs, source checksums and bounded metadata in CI artifact; do NOT commit original position series.
- Fail closed if source unavailable, hash mismatch, corrupted ZIP, ambiguous experimental treatment or missing usable time-stamped trajectories. No inferred zeroes or fabricated timestamps or bee identities.
- Do not begin regression or report an empirical hypothesis result before the true native schema, wind-treatment semantics, replication units and recording-day identifiers are verified. Data collection or statistical post-hoc parameter tuning is not permitted.
- Source first will distinguish original tracked **landing trajectories** from **individual known bees** and from **competing floral choices**: 2016/2024 recordings do not validate adaptive query costs C_A/C_F, behavioral choices between flowers, interspecific interaction or Darwinian fitness.

## Prospective conditional scientific question (only after gate)
Given true measured (not inferred) timestamped positions and experimental wind condition, can **preceding measured travel direction** improve prediction of a later *lateral flight correction* over identical-time-position, velocity, target geometry and wind models, with an explicit no-memory kinematic baseline? Use temporal causality (past windows only), no nested frame pseudo-replication, block by recorded bee/date/session if actually available. Condition on successful landing selection. Do not claim an actual physiological memory mechanism even if a lagged predictor improves.
The raw file schema and units govern whether this estimand is identifiable; if not, record a scientific NO_GO and pivot to genuinely identifiable trajectory-level angular-distribution contrasts, clearly distinguished from the 2016 authors' prior findings.

No changes to frozen V5/V6 manuscripts, Stage9b PR #87, theory results, or original source datasets.
