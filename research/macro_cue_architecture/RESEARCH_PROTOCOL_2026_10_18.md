# Adaptive-gain: from finite decision topology to a global ecological test

**Study design v0.1 — 2026-10-18.** A prospective plan, not a claim of empirical validation. Core code inspected: `adaptive_gain/core.py`, `productive_frontier.py`, `bounded_arity_extremal_bounds.py`, the V5 manuscript/prior-art audit on `main`; PR #67, #65, and #68 descriptions and selected corresponding code. This is a targeted architectural/methodological review, **not** a line-by-line audit of every repository module. No live animal data were newly analysed in preparing this plan. The attached six-world certificate has been independently reimplemented with exact Fractions.

## Executive decision

The most interesting ecological question is **whether the conditional topology of available cues predicts which profitable interactions remain behaviorally accessible during a short decision opportunity, beyond richness, entropy and each cue's target informativeness**. The direct test is a factorial experiment; the macro data are contextual/predictive and a detection-correction test; an individual-trial meta-analysis assesses transportability. Do NOT call an inferred floral-cue matrix a behavioral observation of routeability.

### Four distinct claim layers

1. **Mathematically exact:** for an error-free finite target task, optimal adaptive minimax cost `C_A` versus precommitted fixed resolving-set cost `C_F`; sharp extremal bounds with fixed world count `n`, cue count `m`, and arity `b`; unbounded gap in a binary-observation construction; productive-frontier hitting-set representation. Generic decision trees, test cover, and value of information are old ideas; broad priority is NOT established.
2. **Conditional evolutionary lift:** PR #67's `U(C_A)-U(C_F)` optimization and robust architecture cost thresholds require a stipulated completion-value function U and biological maintenance cost K. These are not estimated natural fitnesses.
3. **Finite payoff robustness:** PR #68 establishes illustrative effects of deadline, abstention, noisy and correlated cues, and acquisition order. These examples establish possibility, not the frequency of the phenomenon in natural systems.
4. **Empirical limitation:** PR #65's Villavicencio records show observed link gain/loss is strongly affected by effort and detection, and that the existing analyses do not identify natural latent network rewiring. Network binary turnover may not be promoted to ecological rewiring.

## New independently checked task-matched witness (pre-data)

Six equiprobable worlds, target `T = [0,0,0,1,1,1]`, and three unit-cost binary cues. Q0 and Q1 are the same across both environments; only Q2 differs. Every world has a distinct **full** three-cue signature in both environments. For each named cue, its *entire two-by-two joint contingency table with the true target* is identical between the environments — stronger than equal cue entropy or equal marginal outcome frequencies.

```
      W0 W1 W2 W3 W4 W5       T: 0 0 0 1 1 1
Q0 :   1  1  0  0  0  0        (both)
Q1 :   1  0  1  1  0  0        (both)
Q2-X:  0  1  1  0  1  0        (nonrouteable)
Q2-Y:  1  0  1  0  1  0        (routeable)
```

`X: (C_A,C_F)=(3,3)`; `Y: (2,3)`. With budget B=2, best-guess accuracy under *fair*, partial, precommitted cue sets is 5/6 for BOTH, while adaptive accuracy is 5/6 for X and 1 for Y. Certified target resolution at B=2 is 2/3 for X (both access classes), and 1 adaptive versus 2/3 fixed for Y. Both have zero true acquisition adaptivity premium at B=1 and B=3. The exact verification script independently enumerates policy trees and fixes all probability arithmetic with `fractions.Fraction`.

Exhausting a declared 135-member labeled matched-contingency synthetic family gives 99 duplicated full cue-signature tasks, 18 distinct-state X-like `(3,3)` cases, and 18 distinct-state Y-like `(2,3)` cases. **This is a combinatorial enumeration, not the prevalence of these environments in nature.** The witness makes a clean experimentally realizable cue architecture contrast, but it is not a new generalized decision-tree theorem.

## Central testable hypotheses and independent endpoints

**H1 — topology × deadline × access, preregistered primary:** With six resource states, identical target prevalences and per-cue target contingency tables, the *incremental behavioral advantage* of contingent over precommitted cue access is higher in a routeable than nonrouteable mapping at the **intermediate** 2-cue budget; no extra *structural* contingent advantage exists at one cue or at full three-cue access in the error-free optimal benchmark.

Define `Delta(topology,B)=Pr(correct final action by deadline | contingent access)-Pr(correct final action by deadline | precommitted access)` under randomized experimental assignment. The principal interaction `H1 = [Delta(Y,2)-Delta(X,2)] - 1/2*[Delta(Y,1)-Delta(X,1)+Delta(Y,3)-Delta(X,3)]`. The exact ideal benchmark for the B=2 bracket alone is `1/6`; this is **not** a prior estimate of actual insect behavior. A zero/negative animal contrast remains entirely possible even when theoretical access is improved.

**H2 — behavioral calibration:** Animals with higher independently measured cue discrimination and successful sequence learning show larger experimental H1, with non-monotonic changes after time/energy cost and sensory noise are introduced. This is a preregisterable effect modifier; do not infer heritable fitness.

**H3 — macro-scale ecological opportunity, different outcome:** Conditional on floral abundance, weather, taxonomic composition, seasonal co-occurrence, and detection effort, there is variation in observed partner visitation not explained by species richness or temporal overlap alone. This can be studied at scale but **does not itself identify cue acquisition or prove H1**. A putative structural-cue proxy is admissible only where cues and reward/compatibility classes were independently measured prior to looking at actual partner visits.

**H4 — observation mechanism:** Correcting for sampling effort and detection substantially attenuates at least some apparent plant–pollinator link gains/losses. The falsifiable competing hypothesis is that latent interaction change survives rigorous observation correction. This may be a **separate macro paper**, not a proof of routeability.

## Empirical programme: three non-interchangeable tracks

### Track I. Original multisystem randomized cue-access experiment: identifies H1

Taxa in feasibility order: captive **Bombus** spp. or **Apis mellifera** first (individual repeated learning + handling achievable); add a second eusocial bee and wild hoverflies only after a calibrated independent-cue reporting/response task works. Use the same abstract six-world target/cue matrix but **species-calibrated** visual/olfactory/tactile stimuli. Avoid insisting that human blue/yellow or odor intensity means equally informative cues to bees, flies, and butterflies.

Factorial protocol: 2 cue architectures (X/Y) × 3 budgets (1/2/3) × 2 access classes (response-contingent next query versus preregistered fixed schedule). Randomize bee, session/order, target state and physical cue-to-bit mapping; block by colony, session and spatial apparatus. An actor's **final target choice may depend on all observations in BOTH access arms**. The fixed arm may abstain or use incomplete information and must not be forced to obtain a universal bundle. The number of access opportunities and physical exposure deadlines must match. Record independent per-cue reports, order, latency, final correct/wrong/no-action/technically unobserved, age/training block and colony. At most one acquisition per physical cue on a trial. Archive planned fixed schedules before trial exposure and audit trace fidelity separately from the ITT effect.

Primary estimand: all enrolled animal/trial slots, correct choice by fixed deadline, with confirmed no-choice scored as failure and technical observation missing explicitly bounded. Secondary estimands: wrong choice, no-choice, acquisition time, number of acquisitions, separately validated sensitivity/specificity per cue and branch selection following each report. A bee/colony-blocked hierarchical logistic model with preregistered contrasts plus randomized assignment tests, bee as experimental unit; never treat 100 repeated trials as 100 independent animals. Pilot must determine physically achievable cue-readout fidelity, carryover, dropout, colony interference and minimum biologically important effect, **then** power a confirmatory sample. Do not choose N from the ideal +1/6 contrast alone.

Falsification: if physical access and cue readouts are calibrated and the experiment yields no H1 interaction with sufficient precision, the biological **exploitation** hypothesis fails even though the finite theorem remains correct. If cue mappings generate different one-cue confusion matrices between X and Y, the decisive matched-information contrast has failed: return to calibration rather than interpretting a positive effect.

### Track II. Original macro-analysis of temporal pollinator observations: tests H3/H4, not H1 directly

Unit of inclusion is the original **observation event** (site×date×survey×plant×pollinator), not a published network metric or a paper-level p-value. Build a systematic retrieval ledger and harmonized event schema with true zeros/effort whenever possible. Seed the frame with: (a) the 30-study, 9-country event-level Schwarz et al. archive (Dryad DOI `10.5061/dryad.qz612jmbp`, `OIK-07303_database.csv`); (b) UK Pollinator Monitoring Scheme 10-minute Flower-Insect Timed Counts 2017–2023 (EIDC DOI `10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618`), with explicit positive AND zero counts, flower number, weather and survey method; (c) additional original multiple-year and repeated-sampling flower/network datasets from Dryad, Zenodo, EIDC, GloBI provenance links, and primary raw surveys (see registry). Do NOT treat the Schwarz collection's 30 original studies as 30 independent papers to meta-analyze again without original unit/metadata checks; deduplicate by source DOI, study period, site and event fingerprints. Use its original-studies workbook to retrieve primary effort metadata. UK PoMS records broader insect groups than species-resolved networks; analyze them in a separate guild-level stratum.

**Model M0 (opportunity):** pooled count-level negative-binomial/hurdle model for detections per fixed unit of effort, with log observation time/flower exposure as offset where documented. Predictors measured independently of the focal dyad: focal plant flowering abundance, site×date environmental conditions, contemporaneous pollinator activity estimated on other plant observations, spatiotemporal flower availability, observer/method and site/year random effects. No response leakage from including the focal link in its own predictor. Temporal cross-validation leaves out whole sites/years/studies, never randomly samples linked dyad rows from the same period into both train and test.

**Model M1 (detectability):** only for sources with repeated visits or explicit survey zero records. Latent interaction occurrence `z_{ij,st}` and detection `y_{ij,str} ~ Bernoulli(z * p_{ij,str})`, where `p` depends on method, effort, weather and observer; fit hierarchical repeated-detection occupancy / count models and check closure over the chosen time window. No repeated detection = **no claim to estimate latent turnover**. Decompose observed gain/loss into latent persistence/transition and changing detection; compare to effort-only negative controls and within-site matched-effort rarefaction.

**Model M2 (independent potential routeability, feasibility-gated):** only in site×date assemblages with independently measured decision target (e.g., measured nectar profitability / host compatibility / pollen contact outcome), a full relevant cue table (e.g., actual insect-vision reflectance, morphology, independently identified scent where available), available alternatives, and a biologically calibrated acquisition cost/time. Precompute cue→target rules blind to realized visitation; derive `C_A,C_F`, conditional expected reward and a null distribution generated by within-target-class cue rearrangements that **preserve every named cue×target contingency table**, richness and opportunity. Compare its prospective predictions for new site/date/insect observations to simpler entropy, richness, phenological overlap and one-cue mutual information models. If cue coverage/reward is absent, restrict interpretation to environmental opportunity; **do not label network nestedness, d-prime or visitation diversity as measured routeability**.

Reporting layers: quantitative analyses of visitation counts use known effort; binary link analyses require detection calibration or are explicitly named observed-link turnover; all datasets are version-locked with original DOIs and SHA-256; metadata completeness and climatic/taxonomic coverage tables are published. Research sample size cannot be declared from the number of raw rows: independent units are sites, original studies, years, bees or colonies as warranted.

### Track III. Systematically harvested individual-participant/trial meta-analysis: tests transportability, with a hard eligibility gate

Search **all** relevant Dryad, Zenodo, Figshare, OSF, DataCite/OpenAlex-linked repositories and references up to a locked extraction date rather than selecting 3–5 supportive papers. Candidate taxa: Hymenoptera (honeybees, bumblebees, solitary bees, wasps), Diptera (hoverflies, mosquitoes), Lepidoptera and other invertebrates with individual trial records. Search combinations of `multimodal / sequential / conditional / information / flower / foraging / host seeking / odour / visual / learning / cue order / decision` and synonyms; retrieve full available datasets and data dictionaries; retain rejected studies with reasons in a public flow diagram. Treat duplicates (publication/repository version/secondary compilation) as one underlying experiment.

**Stratum A — primary causal pooled effect:** individual known reward target, randomized access **contingent versus fair precommitted** with equal budgets, true recorded cue identities/order, correct/wrong/no-response, timestamps, animal IDs, site/colony and randomization propensity. Estimate study-specific `Delta` and the architecture×deadline interaction where available; pool via hierarchical study/taxon/signal-system model with study-level heterogeneity (not by treating all participant trials from one paper as independent experiments). If fewer than ~5 genuinely independent experiments with arm randomization and records pass the eligibility gate, do NOT produce a headline causal meta-estimate: report a systematic evidence-availability audit and conduct Track I.

**Stratum B — ecological cognition / cue interaction:** randomized or observational single-cue learning / full factorial multimodal tasks without contingent access. Estimate learning curves, cue performance and synergy controlling for animal/colony, not a fictional `Delta` effect. The Kent Island Dryad `Learning_Experiment.csv` supplies individual choice trial numbers and correct targets for six Hymenoptera species plus independent flower reflectance, phenology and natural plant-pollinator records. The Latty artificial-flower archive supplies factorial appearance, odour and approach/land/feed responses but not true sequential cue routes. The Chandel mosquito CO2/odour/IR videos/source data support stimulus-integration timing but do not alone identify a choice between contingent and precommitted sensing.

**Stratum C — timed natural foraging sequences:** bee flight-cage raw flower visitation sequences and observational patch-choice trials (visitor IDs, colony, patches, timestamps). Estimate sequential transitions, encounter-dependent switching and detection/availability bias. Without randomized cue access or independent readout histories, these are **behavioral process associations**, not direct routeability effects. Never merge its transition odds ratio with Stratum A's randomized accuracy contrast as though they were the same estimand.

Meta model example for Stratum A: response ~ architecture × access × B + cue-confusion + controls + (1|individual) + (1|colony) + (1|experiment) with study-level partial pooling, nonlinearity in B, and a preregistered policy for absent abstention records. Estimate study and taxon heterogeneity with leave-one-study-out checks and inverse-variance estimates only after harmonizing genuine independent units. Missing actions trigger preregistered worst/best and sensitivity analyses; no-choice is an observed action, not a missing camera record. Evidence quality and availability are explicit outputs.

## Data gaps that could falsify feasibility

1. Time-stamped plant–pollinator **visits** are not direct observations of cue identities, internal percepts or available alternate resources. They cannot by themselves establish `C_A`, a conditional next-cue policy, or neural acquisition cost. UK FIT 10-minute **observer effort is NOT a 10-minute animal decision deadline**.
2. A plant resource's *observed visit label* cannot be used as the target of the same task whose visitation is predicted; this leaks the response. Independent nectar/pollen/morphological compatibility or experimentally assigned reward is essential.
3. GloBI/DoPI and some compiled network matrices contain many positive interaction reports without zeros or comparable effort. Those records support co-occurrence mapping, not latent occupancy/no-go conclusions, unless original sampling denominators can be reconstructed.
4. FloRes includes many taxa but only 27 with all eight listed floral resource traits; do not impute a complete global nectar×pollen matrix and call it observed. Use measured subset traits and preregister overlap/missingness audits. FReD reflectance is in insect-visible wavelength spectra, but taxon-specific receptor and ambient background calibration remain necessary.
5. A task-specific finite optimality result does not imply an evolved or used animal strategy. Need observed query traces and an intervention or demonstrated transportability of the learned strategy.

## Go/no-go and deliverables

**Stage 0 — source inventory (deliverable: unit-of-observation/effort matrix):** index primary archives, inspect native CSV/Excel column names, methods, provenance, licenses, sampling design, known zero observations, taxonomic units, times and the extent of overlapping records. Keep all primary files unmodified with hashes. Stage 0 fails for a direct macro routeability claim if no sites combine independent reward labels with ≥2–3 observable cues and independently calibrated costs.

**Stage 1 — analytic negative controls (deliverable: detection/effort paper or supporting result):** replicate date/effort event construction in Villavicencio; test PoMS survey effort and repeated observations; re-run Schwarz at its original event resolution, separating datasets that document denominator time and those that don't. Model observed-link changes under persistent-latent-link null with fitted detection variation; leave studies out. Publication is warranted only if robust across independent surveys, not because a single dataset gives high AUC.

**Stage 2 — ecological cue calibration (deliverable: candidate state×cue×reward matrices):** measure or source spectral reflectance, morphology and reward independently; compare state counts, target classes and cue conditional tables. Calculate theoretical conditional/access values on observed available-resource assemblages and on within-target-margin-preserving null arrangements. Pre-register realistic time and noise sensitivity with independent sensory measurements. This yields **potential**, not realized behavior.

**Stage 3 — new multisystem randomized experiment + IPD meta (deliverable: causal H1 test):** use the exact six-state matched-information witness to randomize physical cue mappings, topology and budget within an insect species. Require clear animal-level ID and learning/observation windows; calibrate counterfactual fixed control. Preregister the H1 interaction, zero/no-response accounting, randomization unit, exclusion rules and biological effect size after a feasibility pilot. Harvest existing trial-level records in parallel; only synthesize randomized access contrasts if the inclusion criteria are actually met.

**Stage 4 — synthesis:** ask if controlled H1 survives at multiple taxa, and separately whether predicted potential routeability has incremental held-out explanatory value for macro visitation after opportunity/detection controls. Do NOT promote M0/M1 results alone into proof of H1.

## References / starting open sources

- Main finite theorem repository: https://github.com/zuizui0223/adaptive-gain ; PR67 for the assumed-utility evolutionary lift; PR65 for the negative detection result; PR68 for stochastic/order and experimental guardrails.
- Schwarz et al. (30 source studies, 9 countries, original event-level archive): https://doi.org/10.5061/dryad.qz612jmbp
- UK PoMS FIT 2017–2023: https://doi.org/10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618
- Kent Island cognition + phenology + network + reflectance: https://doi.org/10.5061/dryad.9p8cz8wtm
- Artificial multimodal floral traits, wild insects: https://doi.org/10.5061/dryad.jsxksn0h5
- Western Ghats repeated plant flowering and colour-linked networks: https://doi.org/10.5061/dryad.h9w0vt4w0
- Dryland gradient weekly phenology and network cooccurrence, *interaction abundances redacted*: https://doi.org/10.5061/dryad.j0zpc86s2
- Camera vs human detection and explicit observation interval: https://doi.org/10.5061/dryad.q573n5v02
- Bee individual visitation sequence in flight cages: https://pmc.ncbi.nlm.nih.gov/articles/PMC6383269/
- Floral resource traits, high missingness: https://zenodo.org/records/6963646
- FReD spectral reflectance: https://doi.org/10.1371/journal.pone.0014287
- Plant interactions DB broad discovery only: https://www.globalbioticinteractions.org/data
- Aedes CO2/odour/IR multi-sensory responses, raw video link in article: https://doi.org/10.1038/s41586-024-07848-5

Additional prior-art / falsification boundaries: sequential use of general and specific host cues was proposed explicitly for polyphagous herbivores by Silva & Clarke (2020), DOI `10.1111/1744-7917.12719`. A 2025 eight-year meadow analysis found that inferred seasonal interaction turnover changes markedly with sampling effort, DOI `10.1007/s00442-025-05771-8`. Neither sequential cue use nor sampling-effort bias is a new general discovery of this project. The experimental contribution needs the carefully matched cue×target contingency and proper randomized control; the macro contribution needs a new estimand or demonstrably better detection-aware synthesis, not rediscovery of these effects.

All source availability/field granularity must be rechecked programmatically at Stage 0 before asserting dataset-level sample sizes. The attached registry labels which sources are suitable for which estimand.
