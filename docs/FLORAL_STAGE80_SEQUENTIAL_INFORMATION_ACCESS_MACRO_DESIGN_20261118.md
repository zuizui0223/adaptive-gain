# Stage80: When does wind reorder floral information acquisition?

2026-11-18. Status: **synthetic finite mathematical example and original-source macro identifiability audit; no new field effect confirmed**.

## One claim

Wind can alter the relative availability and costs of scent, distant visual detection, close-range chromatic/guide discrimination, approach and landing. The ecological payoff of a cue therefore depends not just on its salience, but on **when the receiver must buy and act on it**, what it learned previously, and whether approaching is feasible.

The previously proved repository finite **deterministic guaranteed-resolution** result C_A <= C_F and the adaptive-only budget window C_A <= B < C_F do NOT prove this claim for noisy cues, animals, evolution or real field flower traits. In particular the botanical data contain neither a measured acoustic/scent/visual flight decision tree nor a pollinator reward function.

## Executable illustrative noisy decision model

Source: research/floral_macro_stage80/sequential_floral_cues.py. The insect considers a candidate flower with a probability p of reward. FAR actions: inspect scent, inspect coarse distant visual information, approach or abandon. NEAR actions: inspect a fine-scale visual guide, land or abandon. A binary signal's accuracy is declared explicitly. All signals are conditionally independent conditional on reward in this illustration, not a biological estimate.

Landing utility at posterior p and context w:
L(p,w)=q_land(w) [p V_reward-(1-p) C_empty]-(1-q_land(w)) C_failed.
The near-stage value is max{0, L(p,w), -c_guide + E[max(0,L(p|guide,w))]}.
The far-stage Bellman recursion chooses max among abandoning, approaching (paying c_approach and using the near-stage value), and paying for one of the unmeasured far cues before conditionally choosing again.

Thus the decision uses **net expected reward**, not maximizing mutual information in isolation. Learning is represented here only by the reward prior p; neither learning rate nor receiver capacity is fitted.

The following are synthetic input/output examples, not wind observations:

| Scenario | P(reward) | P(correct scent) | P(correct distant visual) | Landing success | Approach cost | Optimal first action | Net value |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| Calm | 0.45 | 0.90 | 0.68 | 0.96 | 0.08 | inspect scent | 0.231079 |
| Gusty | 0.45 | 0.57 | 0.78 | 0.89 | 0.10 | inspect far visual | 0.107540 |
| Hazardous | 0.45 | 0.52 | 0.80 | 0.30 | 0.55 | abandon | 0 |

All reward and inspection costs are declared in the Python script. Changing the assumed costs, diagnostic accuracy, reward prior or signal-dependence model can change the policy; these outputs do not estimate real wind responses.

## Existing original evidence and limits

- Stage79 corrected original EuPPPollNet, botanical source and matched ERA5: 623,476 original recorded plant–visitor events, 1,864 source network-year units, and **37** within-source floral petal width contrasts informative for recorded strict bee guilds from 15 source study IDs. Only seven study IDs have within-study gust15 exposure variability. A descriptive 15m/s gust interaction score is +1.4384 [-1.1804,+4.0573]; study-equal weighting is +0.7340 [-1.5099,+2.9778]. Both intervals span zero; one study makes 81.07% of initial information. Petal width is a taxon prose proxy, not an experimentally measured distant detectability or airborne wind/plume near the bee.
- Ohashi et al. (2015; DOI 10.1111/1365-2435.12420) already measured distant green-receptor and close chromatic effects on floral colour change (219 screened; 48 bee-visible positives). 28 name-matched measured taxon folders occur in the EuPP field flora, but the 48 source-confirmed positively perceptible taxa must not be guessed from folder overlap. Archive: https://zenodo.org/records/4942515.
- Lawson et al. (2017; dataset DOI 10.5061/dryad.3g591) already experimentally tested wind/odor/vision learning. It does not supply independent cross-region field visitor/landing macro effects.
- Finnell & Koski (2021; DOI 10.1111/nph.17631) original one-species UV illumination and guide experiment has 377 first visits in 27 original array pairs and no physical wind treatment.
- Flower patterns improve foraging efficiency (2023; DOI 10.1111/1365-2435.14262) already demonstrates approach/landing/departure effects, without necessarily faster nectar discovery *after* landing.
- Follow the flower (DOI 10.1242/jeb.249380) reports bumblebee landing control on an artificial flower oscillating at up to 0.65Hz. Flower oscillation frequency cannot be imputed from ERA5 daily gust wind speed.
- Farré-Armengol et al. (2020; DOI 10.3389/fpls.2020.01154) published a 305-plant 851-VOC compiled dataset, but same-site co-measured atmospheric plume, field visitation and vision are missing. A source field named wind means wind POLLINATION, not atmospheric airflow.
- Kantsa et al. (2018; DOI 10.1038/s41467-018-03448-w) supplied true field VOC/visitation network overlap for 40/41 plant species in one Greek community, without same-study atmospheric wind; multi-sensory floral networks are already prior art.

## New machine-audited macro data-availability result

Original-source ledger: research/floral_macro_stage80/source_stage_ledger.csv; audit code: audit_stage_identifiability.py. Ten identified original sources were assessed for far optics, near guide, emitted VOC, discrimination learning, physical wind, flight/landing, source-local visitor outcomes, and fitness. Source-component flags are **co-measurement labels**, not positive effect signs, and 0 does not establish a biologically absent trait. Independently recovered raw bytes are flagged separately.

The audit yields:
- far + near + wind + local field visitors: **0 of 10 source identities**;
- actual emitted VOC + wind + local visitors: **0/10**;
- visual + cognition + local visitors: **1/10 source identities**, BUT **0 recovered raw source instances** within that matched class (Kent Island Jones et al. 2025 source reported, Dryad file stream returned 403);
- wind + measured true guide + actual landing: **0/10**;
- all eight dimensions and fitness: **0/10**.

These are coverage gaps among a targeted list, NOT a published-universe meta-analysis, not evidence of null biological effects and not a fitted SEM. **Resolved study-ID accounting:** original EuPPPollNet explicitly states 52 independent studies and 54 Study IDs because one study was divided into three habitat-specific IDs 23, 24 and 25 (original DOI 10.1111/geb.70000, section 2.3). The corrected study-year database retains those ID labels. Stage79's 15 informative Study_id labels must be checked for these duplicate-publication IDs and publication-level clustering before calling them 15 independent studies.

## Preregistered direction for a real macro test

1. **Freeze flora before bee outcomes.** Use original 300–700nm spectrometer measurements; separate distant achromatic/green contrast, near chromatic contrast and true spatial guides, as well as genuinely measured negative/unchanged colour-change states. Map plant accepted names, genuinely native field region and phylogenetic groups. No image-derived proxy or unmentioned-trait negative.
2. **Record receiving channel and environmental accessibility.** Source species-identified bee/fly/butterfly visits and separately inferred Bombus environmental suitability, with study/effort, flower abundance, canopy, precipitation, irradiation, temperature, gust and measured UV illumination, where available. Model observation effort rather than making visited plants represent the whole flora.
3. **Split descriptive macro patterns from mechanisms.** Observational study/lineage-clustered optical trait × wind × receiver-opportunity guild models can study *recorded composition*; repeated-individual flight, sniff/visual scanning, landing and reward records are needed to assess signal acquisition order and learning. VOC plumes require emission plus actual wind/turbulence transport data; monthly ERA5 gust is not a plume.
4. **Condition on adequate independent source studies.** Show study-ID and clade leave-one-out, within-study atmospheric contrast, true matched negative controls and site-time compatibility before a cross-stage model. Keep 20m/s gust as Stage79 NO-GO (only four varying source studies), not "no effect".
5. **Claim ceiling.** The novel empirical demonstration would be a reproducible cross-guild/clade/context boundary for **cue-order switches** that survives phylogeny, visitor availability, environmental confounding and sampling bias. No source now identifies a complete wind -> scent -> information cost -> landing -> pollination-fitness mediation.

Run locally:
    python research/floral_macro_stage80/sequential_floral_cues.py
    python research/floral_macro_stage80/audit_stage_identifiability.py
    python -m unittest discover -s research/floral_macro_stage80 -p 'test_*.py'
