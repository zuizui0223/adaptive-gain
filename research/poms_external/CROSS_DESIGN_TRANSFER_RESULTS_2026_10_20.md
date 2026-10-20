# PoMS cross-design transfer — 2026-10-20

**Completed original-data analysis: 120 paired comparisons / 240 fitted models.** This is a new between-design test, not another within-design holdout. No universal or causal routeability finding is promoted.

## Main result

After matching observed flower/month support, the previously shortlisted bumblebees, hoverflies and beetles do not show positive increments in both transfer directions under every declared flower-exposure/penalty variant. Bumblebee gains are asymmetric, mainly monitoring-to-public. The broad `insects_small` category has positive mean increments under all 12 direction/exposure/penalty combinations, but all four primary conditional site-bootstrap intervals cross zero. These data do not establish a precisely resolved, generally portable seasonal flower-use mechanism.

## Source recovery and execution

Official UK Pollinator Monitoring Scheme (2026), Flower-Insect Timed Count data 2017–2023, EIDC DOI `10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618`.

- Original public source recovered through https://github.com/zuizui0223/adaptive-gain/actions/runs/39370955234; artifact `12240349865`.
- Recovery artifact SHA256: `b3ae1c5d3ed9fb1b5bcd82eb744f17b7b70ec878ece99fc04d5c24aa2a45c356`.
- Monitoring CSV SHA256: `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`.
- Public CSV SHA256: `bcd2ef780d3208a5a4aba5c191178900ccef705e5b569dc0160b27d00652dc3c`.
- Recovered source-model commit: `395422122d14346de267bfce9b0a4458c99e4e07`; model file SHA256: `7448ddf7369356071d4c501beb28549b6dca004599519e91e90837091f0f5b37`.
- Transfer fitting ran locally on the recovered originals, NOT in the recovery workflow. Python 3.11.8, NumPy 2.3.5, pandas 2.2.3, SciPy 1.17.0, scikit-learn 1.8.0. The exact Python version is recorded in the machine-readable result; do not use the recovery runner version as the fitting version.

## Matched population and leakage controls

Both designs: May–August 2017–2023; seven named flower categories; the same 20 flower-month combinations. Keep performed-survey zero counts and positive measured floral-unit counts. Exclude unspecified Other flowers; never create zeros for unobserved flowers. Support thresholds: >=12 surveys/4 monitoring locations and >=30 surveys/10 public grid cells per combination, with >=2 shared months per flower. Selection uses exposure/covariates, not insect counts.

The complete sources have 18 shared coordinate-system-specific grid labels. The eligible May–August public subset includes 16 of them. Assign monitoring grids to monitoring only and remove 38 eligible public observations using the FULL original monitoring grid set. There are no shared original sample IDs or final geographic grid cells across the two designs.

Final populations: monitoring **1,463 surveys / 89 monitoring locations** (91 recorded grid cells); public **4,447 surveys / 1,276 grid cells**. Matching flower/month categories does not balance habitat, observer, country, weather, floral amounts or sample size.

## Frozen model contrast

Fit on all eligible public observations and test on monitoring without target-outcome calibration; then reverse the roles. Baseline includes plant/month/year/country/recorder experience/habitat/flower context, cover and units/weather. Add a plant-month block projected off the FULL baseline using training data only. Main count-scale alpha=0.25; sensitivities 0.025 and 2.5. Two flower models: fitted log1p amount and proportional offset, with weighted-rate alpha divided by mean training exposure. No tuning against transfer outcomes.

Below: percentage reduction in target-site-equal Poisson negative log likelihood. Positive means better count prediction, NOT higher insect numbers, preference, accuracy, variance explained or fitness. Six variants per direction = two exposure models × three penalties.

| Group | Public→monitor fitted flowers | Public→monitor offset | Monitor→public fitted flowers | Monitor→public offset | Positive variants public→monitor; monitor→public |
|---|---:|---:|---:|---:|---:|
| bumblebees | +0.0181% | -0.0175% | +0.3588% | +0.2605% | 1/6; 6/6 |
| honeybees | -0.0816% | -0.4130% | -0.1184% | -0.0227% | 0/6; 1/6 |
| solitary_bees | +0.0661% | +0.0496% | -0.0026% | +0.0915% | 6/6; 4/6 |
| wasps | +0.1573% | +0.1014% | +0.0340% | -0.0236% | 6/6; 2/6 |
| hoverflies | -0.2222% | -0.2466% | -0.2347% | -0.3396% | 2/6; 1/6 |
| other_flies | -0.0176% | -0.0130% | +0.0945% | -0.4071% | 2/6; 2/6 |
| butterflies_moths | +0.2383% | +0.1757% | -0.0782% | +0.0219% | 5/6; 2/6 |
| beetles | +0.2205% | +0.2754% | +0.1954% | +0.3659% | 4/6; 5/6 |
| insects_small | +1.1080% | +1.2568% | +0.5588% | +0.7366% | 6/6; 6/6 |
| insects_other | -0.0539% | -0.0628% | +0.0513% | -0.0546% | 0/6; 3/6 |

## Uncertainty, influence and transfer limits

Primary small-insect absolute site-average delta intervals (fixed-prediction site bootstrap): public→monitor fitted [-0.01569,+0.16454], offset [-0.03136,+0.23116]; monitor→public fitted [-0.00536,+0.05844], offset [-0.01628,+0.08932]. All include zero. These are conditional diagnostics, not full training-refit/spatial/multiplicity-adjusted confidence intervals.

Removing the single most favorable target site leaves each primary small-insect mean positive. Removing the top 1% most favorable public target cells makes both reverse-direction means negative. This is an outcome-selected influence diagnostic, not an unbiased alternative estimate and not evidence that the favorable records are errors.

Unseen target flower-month cells=0 in both directions. Public→monitor has no unseen baseline category levels. Monitor→public has new country levels in 15 observations, habitat in one, floral-unit in 15, cloud category in five, and five flower counts outside the training range (these counts can overlap). Encoders ignore new categories; common flower/month support is not complete multivariable common support.

Prediction is observational, and FIT does not measure every available floral alternative, individual insects, nectar profitability, sensory sequences, latent rewiring or fitness. Asymmetric transfer cannot by itself establish biological differences between survey populations. This does not negate the earlier Schwarz temporal-partitioning pattern: the estimands and sampled populations differ.

## Verification and saved state

All 16 focused tests passed: eight new transfer tests plus eight inherited model tests. All 240 fits converged (maximum 149 iterations). Independent reaggregation of all 120 site-score CSVs reproduced site means, survey-weighted means and relative improvement; maximum discrepancy 1.81e-15. Full result JSON SHA256: `5eea6f60afe1923be599984ff52a05d1359acf1ef01a84d45c4ed947f8c37125`.

The delivered `poms_cross_design_transfer_20261020.zip` contains the actual original archive, source/model receipt, executable transfer code, tests, pre-result protocol, full 120-comparison summary, 120 hashed-site score CSVs, support ledger, influence diagnostics and independent verification. Package SHA256: `9c3457161c3a70d1431263b67cc9cab0bcb59f41c322bdc1fcf0274799980eb1`. Repository-wide CI was not rerun locally and is not claimed green. Frozen manuscripts and main are unchanged.

Stop rule: do not search further variants merely to make monitoring transfer favorable. The present result supports at most group- and context-dependent seasonal predictive structure. A mechanistic explanation requires independently measured resource availability or individual/species-resolved behavior.

Data use is under the Open Government Licence. Publications must cite the original EIDC release and include the mandatory UK PoMS partnership, funder and volunteer acknowledgement; the unchanged source readme and metadata are retained in the package.
