# Wind × hoverfly larval trophic trait: evidence and identification boundary

**2026-10-20 — completed exploratory original-data quantitative analysis.** This is not a causal predation/aphid/flower-pollinator result or an estimated routeability effect. The original data are sourced directly, not from publication-level summary statistics. Frozen V5/V6 and main are untouched.

## Exact sources, analytical units

- UK PoMS pan traps original (2017–2023): DOI `10.5285/5841bfae-471b-498c-af89-c30e5140d6c5`; original samples/insect/flower CSV SHA256: `70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277`, `2423bc370f388a0dafd05c4bd3a7af7491909311ffe6bf4d6607a3697213dcb9`, `53daa167282092b7081190de00e020b4e2635fa5e7d4fc63d3454f7c338951ba`.
- Independent **EuPollTrait**: Miličić et al. 2026, `Scientific Data`, DOI `10.1038/s41597-026-07513-8` / Zenodo `10.5281/zenodo.18032357` (3052 total species, 913 hoverflies), original download MD5 **`7a50cc03e2c5a287e663dc5d029f8026`** confirmed through [successful GitHub source recovery](https://github.com/zuizui0223/adaptive-gain/actions/runs/39401254269).
- PoMS QC: 5506 eligible original trap-station rows, 1139 site/dates, 92 sites, within-day >=0.5 Beaufort grade difference. Same-site/day 4–8-hour trap exposure, undisturbed, minimum 3 stations; mismatched species/sample day excluded at the full day grain. Beaufort start/end category average is ordinal, not measured meter-per-second continuous wind.
- Exact-binomial larval-feeding match for **8921 / 9699 (91.98%)** eligible captured hoverfly specimens (99 taxon names); unrecognized source species/complexes never assigned arbitrary larval traits. Trait categories **zoophagous, saprophagous, saproxylic, phytophagous**; zoophagous is NOT an independently observed aphid-specific diet.

## H1: Wind-associated capture differs by larval life-history class

Primary contrast: difference in the capture wind slope for zoophagous-larva hoverfly adults versus other known larval diets. Conditional count model fixes site-date-by-trophic-group capture totals, uses original hours as offsets, controls physical station index, vegetation height, sun and temperature, allows group-specific nuisance responses and site-cluster sandwich SE.

**86 sites × 413 dates × 2013 station records; 3479 zoophagous +3535 other-diet specimens.**

`beta=0.481357`, `RR=exp(beta)=1.61827` relative capture ratio /+1 Beaufort, exploratory site-cluster 95% CI **[1.37242, 1.90816]**, two-sided nominal p~`1.0e-8`. **Relative conditional catch**, not an absolute population density change or wind causation.

| Declared sensitivity | sites | site/dates | relative RR (exploratory 95% CI) |
|---|---:|---:|---:|
| Primary | 86 | 413 | **1.618 [1.372,1.908]** |
| Source species trait coverage >=95% | 84 | 301 | 1.698 [1.403,2.055] |
| All pantrap stations have plant lists | 52 | 135 | 1.647 [1.317,2.060] |
| Remove extreme capture days | 86 | 384 | 1.381 [1.144,1.666] |
| Remove abundant `Episyrphus balteatus` | 86 | 388 | 1.670 [1.419,1.966] |
| Zoophagous versus saprophagous alone | 84 | 416 | 1.526 [1.281,1.817] |

**Method and observer independent checks:** Statsmodels ConditionalPoisson `beta=0.481825` versus production custom exact conditional likelihood beta `0.481357`, difference `0.000468` (one optimization warning; not identical machine precision). A separate weighted zoophagous catch *fraction*, with site/day and permanent site/station two-way fixed effects, yields **+7.84 percentage points / Beaufort** [3.16,12.52] using 1466 nonzero-catch station records. This is a distinct estimand. Both are observational.

## Critical evolutionary/functional attribution audit

**Do NOT claim a larval-diet causal adaptation to wind.** Of 41 matched source genera, only one (`Volucella`) has any within-genus mixed larval feeding classification, representing 63/8921 (0.71%) of matched specimens. Larval nutrition is nearly perfectly collinear with genus/phylogeny and other shared flight morphology/behavior.

For 15 relatively common genera (>=80 captures, >=20 sites, >=35 days), independent per-genus estimates show an equal-genus zoophagous/nonzoophagous log-slope difference `0.3302` with approximate genus-label randomization **p=0.0812** (20k Monte Carlo), independently checked with **full exact enumeration: 419/5005 = p=0.0837**. Exact genus-label assignment conditional on adult flight traits: **26/168 = p=0.1548**. This corrects an earlier unverified p=0.1845 report; both tests remain unresolved and neither is a phylogenetic randomization. Hence no statistically resolved diet-specific effect at the genus-unit level.

Declared/diagnostic site-level robustness: leaving out one of the five highest-count genera keeps primary RR 1.609–1.670; all unrecognized taxon specimens adversarially forced to either diet group gives primary RR 1.534–1.646. Adult trait stratification still has positive estimates (migratory species RR1.778 [1.433,2.206], strong fliers RR1.553 [1.061,2.272]) but cannot deconfound genus. Splitting sites into five disjoint sets gives RR1.474, 2.036, 1.830, **0.877**, 1.388: effect not uniform across regions.

## H2: Independent, apparently unrelated floral resource

The predeclared `Urtica dioica` recorded-plant × larval-diet contrast reaches **19 sites /39 discordant dates**, below the locked 20-site minimum: **NO-GO; no effect estimated**. `Trifolium repens` flower inventory recorded/not recorded reaches 27 sites and 46 dates, relative RR **1.257 [0.718,2.203]** (p=.423), inconclusive. Unrecorded flower is NOT absent: 2-m plots are incomplete relative to animal range. No aphid/larval host counts exist. As such there is **NO demonstrated plant→aphid→larval hoverfly→adult visit mechanistic mediation or direct trophic network edge.**

## Scientific interpretation, manuscript promotion rule

New observational insight: **an adult hoverfly assemblage's relative capture/wind association aligns with a trait of its larval life stage**, a pattern missed by broad adult visitor guild aggregates. Natural history and taxon ancestry are plausible common drivers, not yet disentangled. Putative direct wind-sensitive other-species network correlations, direct aphid predation and adult cue-routing remain unproven.

This should be described as **"cross-life-stage ecological trait and wind-associated community filtering"** rather than a universal indirect-interaction network law. A real hierarchical test requires species-resolved adult flower visits, prey/larval observation, floral availability and randomized shelter/windbreak perturbations in the same microhabitats.

## Reproduction and verification

Primary `crosslife_analysis.py`; independent optimizer `independent_validation.py`; permanent-station FE `independent_two_way_check.py`; functional/adult trait subsets `trait_structure_sensitivity.py`; equal-genus randomization `genus_level_audit.py` plus exact checks `genus_exact_permutation.py`; independent report and original output JSON. `python -m unittest -v test_crosslife` passed 5/5 locally on 2026-10-20, plus independent method checks above. Full repository test workflow is **NOT** claimed to pass; isolated calculations are a research draft. Complete scripts, machine-readable provenance and calculated evidence are preserved in a separately supplied conversation ZIP; original trait data must be acquired from cited Zenodo and original PoMS source from EIDC.

UKCEH PoMS source uses Open Government Licence and requires PoMS/UKCEH/JNCC/funder/volunteer acknowledgement; EuPollTrait should cite authors and Zenodo version. No rights over original trait files are asserted.
