# Stage62 — Original Lawson 2017 wind × sensory backup: colony-F matched odour sensitivity

Date: 2026-11-17 JST. **Source-original observational sensitivity of already published scientific result. This is NOT a new ecological wind-vision/scent interaction or an experimentally validated randomization p-value.**

## Input lineage and independent authenticated source

Original Lawson, Whitney & Rands (2017), DOI `10.1098/rsos.170996`, original source European PMC `PMC5717666`, published supplement `rsos170996supp2.xlsx` original inner SHA256 `b3802f57516c0ebac025f363dd2943796e749ef82b9b32e15fd0deb78c98432c`. Stage61 original 72 bees / four 18-bee treatment arms and authored source of 3 endpoints: visits to learning criterion (smaller better), number of correct decisions after landing (higher better), and number of rewarding flower landings (higher better). Original raw worksheet used only within ephemeral GitHub Actions memory; source bee rows not redistributed.

Stage61 initial source analysis: group A calm scented only, B windy scented only, C windy scented + colour, D windy colour only; original 72-bee averages A/B/C/D learning 19.333/31.722/18.778/18.278. The 2017 author work already identifies sensory backup, so a similar C−B result is NOT new ecology.

Actual original colony labels and scent confounding:
- A: colony A7/F11
- B: colony D8/F10
- C: colony A10/F8
- D: colony EE12/FF6
- Only colony **F** overlaps across A/B/C, and **no** source-colony identifier is shared with D.
- Within F, original reward-scent counts A lav7/mint4; B lav2/mint8; C lav5/mint3. Therefore even original common-colony A/B/C comparisons are confounded by reward-scent treatment composition.
- The exact site, trial start period, original within-F random bee/treatment assignment and cue order remain unverified. Individual bees in different treatment arms are not matched individuals, and one colony does not represent independent replicated colonies.

## New authenticated source computation

Original executable CI [run 44018425376](https://github.com/zuizui0223/adaptive-gain/actions/runs/44018425376) **SUCCESS** after fixing a test-only odor-label corruption that sometimes left the same label unchanged. Five mock-only tests passed; authenticated original 72 bee source re-read. Original derived artifact ID **14299453867**, ZIP SHA256 `ba5c0c1f41ef534cf27c192fa685513cc2208348f23bb4a9c5f02b0b7cbb517b`.

Within F alone compare A→B (n=11→10) and B→C (n=10→8). For each endpoint, compute source original raw mean difference and **within-original-odor-standardized mean**: for lavender and mint separately, calculate right-minus-left and weight both by their **pooled source bee proportion in the two compared groups** (no outcome-based odor weighting).

| F original comparison (right−left) | Endpoint | Raw F-group mean difference | Original lavender-only difference | Original mint-only difference | Original odor-standardized difference |
|---|---|---:|---:|---:|---:|
| B−A: adding wind with scent only | visits to learn | +5.8818 | +1.8571 | +4.3750 | **+3.2959** |
| B−A | correct after landing | −1.8727 | −1.8571 | −2.5000 | **−2.2245** |
| B−A | rewarding flower landings | −0.9091 | +0.1429 | −1.2500 | **−0.6531** |
| C−B: adding colour with wind+scent | visits to learn | −7.5750 | −3.8000 | −5.7917 | **−5.0171** |
| C−B | correct after landing | +5.7250 | +6.8000 | +4.5000 | **+5.3944** |
| C−B | rewarding flower landings | +6.8750 | +8.4000 | +2.9167 | **+5.0491** |

**Genuine source-level finding from reanalysis**: previously published vision backup's descriptive direction in C−B persists within the shared F colony *and* within each source reward-odor label, but shrinks after odor standardization. The B−A wind-only learning disadvantage also attenuates from +5.8818 to +3.2959. This is a sensitivity of an already known result, not new selection, and can also be explained by unobserved bee allocation/time/odor-assignment patterns.

Exact reference enumerations at fixed source odor and colony count (invented randomization mechanisms):
- A/B within F: `choose(9 lav,7 A) * choose(12 mint,4 A)=17,820` possible reassigned label combinations.
- B/C within F: `choose(7 lav,2 B) * choose(11 mint,8 B)=3,465`.
- For C−B visual addition, exact hypothetical fraction of reassignment outcomes as extreme as observed: learning 0.3824, correct landings 0.0150, rewarding landings 0.0303.
- For B−A adding wind, analogous exact hypothetical fractions: 0.5483, 0.1001, 0.5937.
- **NONE OF THESE FRACTIONS IS A VALID RANDOMIZED EXPERIMENTAL P-VALUE**, because original within-colony and odor-stratum exchangeability is not authenticated. Nor are 29 source bees independent evolutionary/colony replicates. No population-level p/95%CI or hypothesis confirmation is reported.

## What this changes for the research hypothesis

The strongest real source support is modest and specific: in an existing published four-treatment 2017 bumblebee experiment, visual availability can offset odor-noise-associated learning/landing performance differences. Even the same-colony/odor check supports only the **sensory-backup prior result**.

An additional **conditional sensory routing** ecological prediction cannot be tested from these rows: no first cue carrying zero direct target information, no record of which second cue each bee chooses under different branches, no explicit sensory acquisition cost, no individual order preference or wind-specific optical use, no pollen deposition or plant fitness. 2017 four published arms leave four of eight full wind×odor×vision cell combinations absent; even a complete factorial of static cues would not itself demonstrate contingent routing.

## Next executable gate

- Matched source 80 original VOC/photo taxa (Stage60) must be reviewed using *actual licensed source photographs* and negative as well as positive within-corolla visual pattern annotations, not just photo classifiability. Visible marks need measured position/geometry; RGB cannot verify UV.
- A Bayesian **noisy-cue conditional-route** model can translate the inherited perfect-information `C_A,C_F` theorem into testable stochastic decision predictions under wind-dependent olfactory/visual reliability **without fitting invented coefficients from cross-species datasets**. The result must be labeled constructed until individual cue-acquisition sequences are measured.
- Future ecological field/lab experiment: same bee/plant within randomized odor ON/OFF × visible/UV guide contrast × wind regime with early-cue identity/order, later cue action, discovery/landing/pollen. A static visual-backup null is mandatory.

Original saved source code: `research/floral_routeability_stage62/colonyF_odor_stratified_lawson2017.py`, five separate mock-only tests and dedicated source CI. `main` unchanged; Draft PR, no causal inference.
