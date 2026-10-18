# Stage-0 ecological evidence gates

## What passed on 18 October 2026

- 30-study Schwarz primary event table read directly from the Zenodo-hosted public CSV URL. Exactly 150,914 rows and 10 identified columns. 343 study/site identifiers, 3,270 study-site/date units.
- Prospective dated comparisons: 16 original studies, 105 site identifiers, 479 adjacent pairs meeting **day-grain / <=30 days / >=20 positive records on both dates / freq ==1 in compared rows**.
- Observed link sets measured and row-based 20-draw Monte Carlo rarefaction run with an exact reproduced Mulberry32 seed. Raw mean Jaccard dissimilarity 0.809807; standardized mean 0.850722. Study-FE/CR1 exploratory regressions run and recorded in the receipt.
- 6-state cue-by-target-marginal-matched deterministic pair reproduced independently with exact Fractions and 135 constrained synthetic designs enumerated.

## What has NOT passed

- Raw source file is **NOT** included in the deliverable and its MD5 has not been independently recomputed in the local container. The MD5 listed in the public Zenodo metadata is not itself a raw-byte check. The recipient should use the reproducible `--require-md5` gate before peer review.
- No unified sampling-effort denominator or observed-zero frame across 30 studies. Arbitrarily large duplicate rows may be genuine repeated positive visits; no dedupe.
- No routeability validation: no insect-acquired cue order, independently known resource target/payoff, sensing budget or behavioral control.
- PoMS 2017–23: accessible dataset landing page and ZIP location, **bulk ZIP content not downloaded/analyzed here**. Latty Dryad: file metadata known, anonymous file download HTTP 401 in this session. Kent: schema read, raw file unanalysed.
- No inference of latent interaction loss/rewiring or adaptation/fitness. No pooled meta-effect from papers with incompatible outcome definitions.

## No-go for submission of macro routeability result

Require **both** independently measured reward/decision targets and observed/calibrated sensory cue distributions for focal species/assemblages, and either a randomized conditional-versus-fair-precommitted access experiment or timestamped validated cue-acquisition histories with an identifiable decision model. Without these, macro network models estimate positive visit observations or potential cue architecture only.
