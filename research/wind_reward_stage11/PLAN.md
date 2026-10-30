# Stage11 independent wind-resource bridge — source first

2026-10-30. Continue the empirical research without re-tuning the negative Stage10 endpoint. Stage9b and Stage10 stay frozen.

Goal: examine whether wind's association with observed flower-probing rate varies with independently sampled floral reward. Candidate original source: Harris et al. 2026, Functional Ecology DOI 10.1111/1365-2435.70429; Dryad DOI 10.5061/dryad.9kd51c608. The source authors already reported seasonal energetic patterns; no new discovery is claimed for them.

1. Fetch native provider metadata and actual bytes, verify provider file checksums and sizes, record version and URLs. Inspect schemas and original analysis script, not just the abstract. No biological model at this stage.
2. Validate survey-level keys and joining of forage, nectar, weather and insect surveys. Keep within-survey records distinct from independent weather exposures. Never silently create a many-to-many join, impute nectar missingness, or label an observation row a persistently identified bee.
3. After schema and units are established, freeze one primary wind×independent floral reward interaction on observed probes per 60 seconds. Do not predict derived energetic profit from variables used to construct it. Any scientific analysis requires a separately recorded pre-outcome specification.
4. Execute with survey/date replication, report actual exclusions, effect and uncertainty. Retain positive, null or negative results without changing choices after scoring.

Alternatives: Stage10 re-tuning rejected; artificial-flower wind manipulation is relevant but its exact original dataset was not yet located; this independent 2026 dataset was selected for its joint survey-level measurements, not its statistical outcome.

Limits: nectar availability is not actual ingestion or fitness; wind is observational; no simultaneous full flower-choice set; no randomized sensory cues; only two cities, not multiple independent colony replicates; original patches were selected where honeybees made up at least about one quarter of observed flower visitors. No competition claim from co-occurrence.

Implementation: source_gate.py uses standard-library provider API + version ZIP, tests enforce checksum validation, row-grain preservation and archive ambiguity rejection. Dedicated CI retains only source audit receipts and derived profiles, not original animal event rows in Git. Python source tests were first run against stubs (4 failures), then implementation (4 passes). Full repo CI is a separate gate.
