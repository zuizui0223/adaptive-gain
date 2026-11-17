# Stage58 — Wind, scent, optical cues and conditional information-access topology in floral communication

Date 2026-11-17 JST. **Scope: existing source-backed empirical evidence + existing exact finite routing theorem + NEW explicitly falsifiable cross-system hypothesis/design. Not a fitted joint ecological wind×VOC×UV effect.**

## Central evolutionary/ecological hypothesis

**Receiver-specific floral communication is governed not solely by the number or measured strength of flower signals, but by whether early sensory/environmental cues let the receiver select usable later channels under the prevailing wind, light and floral-motion regime.** An environmental disturbance can change *cue relevance, cost, and sometimes whether an action-relevant distinction is available at all*; thus trait presence and receiver richness do not identify realized signal use.

This is an ecological specialization of the established `adaptive-gain` routeability theorem, **not a new theorem or evidence of actual floral evolution**. A signal can also be biologically noninformative about reward and still organize which later cue is economical; this requires sequence-specific behavior, not a mere co-occurrence of odor and pigment.

Do NOT claim the general concept of cue hierarchy, sensory drive or visual–olfactory synergy is novel: Finnell & Koski (2021, 10.1111/nph.17631) manipulate UV light and floral background and find context-dependent guide-size preference; Pritchard's multi-cue plant-animal literature describes hierarchical cue use; 2024 bumblebee work (10.1016/j.isci.2023.108587) reports noisy multimodal cue benefit; 2025 Eristalis hoverfly work (10.1007/s00114-025-01965-5) reports joint odor+vision flower identification. Exact new claim must be a **conditional access/decision topology × wind/receiver guild × stage-specific contact** pattern that cannot be replaced by additive concentration/contrast or single-cue effects.

## Distinct original verified source results: not one combined treatment

| Evidence | Source and original granularity | Observed supported result | Missing and prohibited inferential claim |
|---|---|---|---|
| Crall et al. 2020 orchid bees and scent | 10.1098/rsbl.2020.0103; 70 actual 20-min sessions in 9 sites/29 dates; all scent-baited; original Zenodo 3743898; Stage37 PR #117 | Within-site wind doubling IRR 1.39852 for bait arrivals, date+site 2-way approximate interval 1.09658–1.78359. Between-site wind–visitation sign differs | No no-odor control; all male orchid-bee fragrance foraging, not wild floral pollen visits, not petal UV, not scent/wind manipulation or complete stage chain |
| Chang, Crall & Combes 2016 Bombus | 10.1242/jeb.137976; 157 archived successful tracks, 28 B IDs; matched 23 B labels; Stage40–44 | W1-W0 near-flower ground speed +0.121429 m/s; six preprocessing methods +.12047–+.12168; within-bee selection sharp minima positive (weakest +.092544 m/s), conditional on archived tracks | Successful landings only; no failed-approach probability; author 112 selected cohort not reconstructed; no odor, visual guide manipulation or pollen |
| Baird et al. 2021 Apis | 10.1098/rspb.2020.3051; visual tunnel texture × head/tail wind | Original manipulated longitudinal/transverse optic-flow cues alter speed/height control | Arena optic-flow texture, not UV floral petals, no flower visit, pollen |
| Haverkamp et al. 2016 Manduca | 10.7554/eLife.15039; floral volatile suppression and proboscis sensation in wind-tunnel/tent | Natural scent may influence within-flower foraging and plant success, not only long-range attraction | Not Crall wind speed treatments; different animal and flower; cannot combine endpoints quantitatively |
| Stage57 UV x Bombus x climate | Stage57 PR #136; Koski & Ashman original 159 UV-status species, 106 sufficient modern GBIF model coverage | Published E=(UV-B,T,P) explains modeled Bombus/all-bee fraction R²=.18288; environment→trait+guild observational confounding; quasi-separation under genus dummy | Modern bee model and plant index-point are not original UV phenotyped sites; no exposed wind or scent data on these plants |
| Stage57 visual atlas | Source union 817 GBIF accepted taxa; 230 directly measured UV pattern; 243 source mean UV fraction; 207 age spectra archives; 124 reviewed color-change taxa | Quantitative UV mean by bee/bird source only weakly separated; only **2 accepted taxa overlap original binary UV pattern and continuous UV mean** | 817 are not 817 visually guided species. No VOC columns; no measured cross-modality covariance |

**Never multiply** the Crall wind×bait association by the Chang speed effect to obtain plant visit or seed outcomes. All outcomes have different species, time, wind, settings and denominators.

## Existing exact theory reused and mechanically audited

Use *existing* `adaptive_gain.extremal_routing_family.extremal_routing_task(2)` with four constructed worlds `(a0,b0,a1,b1)` and targets `(0,1,0,1)`:

- One coarse cue routes the encounter into two equally target-mixed branches (so under uniform worlds the coarse cue has **zero direct bits about target**).
- One terminal cue would distinguish a target in the first branch only (conceptual visual or UV guide), while another terminal cue distinguishes the second branch (conceptual close-range chemical cue).
- An actual flower has NOT been demonstrated to instantiate these outcomes. These are labels for a mathematical witness, not a biological result.

For positive integer acquisition costs `(r,v,o)`, the existing exact k=2 solver returns:

```
C_A = r + max(v, o)          (worst-case contingent policy)
C_F = r + v + o              (cheapest fixed complete cue bundle)
g = C_F - C_A = min(v, o)
Only when C_A <= B < C_F is an adaptive-only route feasible under budget B.
```

This is the **exact weighted special case of an existing theorem**, independently checked for 64 cost tuples (4×4×4) by existing finite-task exhaustive solvers in Stage58 unit tests; not newly proven for flowers. Here `B` means receiver's constrained sampling/decision time/energy/risk budget; the flower does not literally charge the bee a cue fee.

With **hypothetical equal budget B=4 cost units**, exact computed results:

| Assumption-only sensory context | r,v,o | C_A | C_F | Adaptive-only within budget? |
|---|---|---:|---:|---|
| All modalities accessible | 1,2,2 | 3 | 5 | YES |
| Moderate context: chemical easier but visual harder | 1,3,1 | 4 | 5 | YES |
| Visual-motor bottleneck | 1,5,1 | 6 | 7 | NO, neither strategy succeeds |
| Coarse routing cue becomes a constant/uninformative observation | 1,3,1, collapsed R | Unresolvable | Unresolvable | NO |

The last case is stronger than a simple cue cost penalty: a formerly identifiable target becomes **unidentifiable** from the remaining cue partition, even with unlimited receiver budget, in this specific constructed task. Conversely, a positive gap g in the third case does **not** imply realized success when B<C_A. Cue quantity and successful information access differ.

These toy costs are NOT fitted as functions of wind (m/s) or taxon/group. In particular Crall wind `0.0206–0.73 m/s` should not calibrate Chang `3.5 m/s` headwind. The root outcome partition remains an assumption unless measured in the same animals under changed airflow.

## Pollen-return gate (separate existing Stage33/34 exact identity)

For an opportunity: `D = P(discovery)`, `L = P(landing | discovery)`, `T = P(pollen deposit | landing)`. Then `P(pollen) = D*L*T`, **only if** the stages are measured under the same study population, treatment and opportunity denominator.

In an existing illustrative exact-counterexample, calm `D=.4,L=.8,T=.75` gives .24; windy odor detection `D=.6,L=.5,T=.75` yields .225 (decrease .015 despite better discovery). Wind with assumed visual-motor compensation `D=.6,L=.75,T=.75` yields .3375. The break-even conditional landing rate if pollen transfer per landing unchanged is `L_w >= (D_c*L_c)/D_w=8/15≈.5333`. These are **theoretical numbers chosen by hand**, not observations from Crall/Chang/Baird. Stage58 preserves exact Fraction arithmetic and provenance.

Do not call cross-study convergence a real mechanistic link. It only justifies measuring the *complete* opportunity→discovery→landing→contact→pollen event chain.

## Macroecological source data and limits

- Current source-accepted atlas: **817 distinct taxa**, but only 230 UV spatial binary and 243 mean UV reflection source accepted; across these modalities only **2** taxa overlap. DO NOT combine them into a single zero/one visual-guide trait or fit a 817-species cross-modal joint covariance.
- Database candidate for **actual floral scent**: Farré-Armengol et al. 2020 (10.3389/fpls.2020.01154), a **secondary review** compiling **305 species, 851 VOCs, 58 underlying papers**, original source location/climate and pollinator guild indicators. Existing authors already analyzed guild, climate and scent/phylogenetic covariation, so showing VOC~climate or VOC~guild alone is **not novel**. The Stage58 original source probe searches official Europe PMC supplement; the 305 taxa must not be labelled no-VOC if unseen, and taxonomy overlap with 817 must be determined from original rows.
- Experimental cross-signal candidates: `Argentina anserina` measured UV guide × light/background (Finnell & Koski 2021); noisy multisensory Bombus experiment (iScience 2024); `Eristalis aeneus` visual/odor trials (2025); `Nicotiana attenuata` odor genetic silencing and real pollen/seed work (Haverkamp 2016). These constitute prior art/test-bed links, NOT observations from a unified flora × wind intervention.
- Global future guild availability: original Laborieux et al bee model 133 Bombus + other bee names at eligible source HEX; broaden to Diptera, Lepidoptera, birds/moths when separately original-mapped. No universal 'Bombus absence means signal absence'.

## The one nontrivial falsifiable hypothesis (three-layer study; no spurious mediated SEM)

**Conditional-channel bottleneck hypothesis:**
`H1` At constant source UV/odor intensity and initial target prior, changing environment (airflow/turbulence, flower-motion, irradiance/background) changes *which signal is action relevant in the realized encounter*, so first-cue-dependent receiver continuation improves stage-specific accuracy/time under intermediate constraints beyond a noncontingent cue set. **Null**: after conditioning on absolute cue contrast, VOC intensity, attractiveness and source-cluster effects, observing the first cue does not change the optimal continuation / there is no reproducible order- or branch-specific gain.

**H2** The same physical wind condition may improve scent-source encounter while reducing, not changing or improving actual pollen return depending on receiver visual control, flower motion and organism. This is an endpoint-specific sign criterion, not a general prediction that wind universally favours odor.

**H3** Across lineages/geographic communities, a signal's association with guild availability survives after UV-B, temperature, rain, elevation, phylogeny, sun/background and VOC emissions only when its matching receiver stage and locally measured wind/light context afford information access. Estimate alternative receiver guilds; do not make the result Bombus-specific by construction.

Source-specific tests and model grain:

| Data layer | Primary dependent variable | Actual needed inputs | Comparison/negative |
|---|---|---|---|
| Macro floral trait | within-flower UV guide vs source uniform; separate continuous UV mean; VOC richness/composition | source-vouchered plant/part, climate, light/background, long-run wind regime, plant tree, native receiver guild, source-study controls | within clade native source area/spatial holdout; common study vs different study; direct E effects; no unlabeled negatives |
| Animal field or lab | measured route choice and decision time with **first cue information**, order, branch, odor, local UV/visible, wind vs calm | same receiver/flower, original opportunity denominators, continuous airflow gust/plume, flower sway, learning, randomized cue-order and channel suppression | cue order randomized; fixed-bundle control; random first cue; separate negative plume no signal |
| Plant success | observed pollen transfer / fruit / seed / outcross in same randomized arm | actual legitimate contact, deposition and matched flower individual | odor on/off × guide on/off × wind, without inventing independent cross-studies |

## Minimal prospective model formulas

At plant/species x native location `(i,s)`, modeling costs or conditional information use is **separate** from plant trait presence:

```text
B_{guild,s}   ~ f(climate_s, native accessibility_s, wind_s, phylo_bee)
V_{i,s}       ~ f(UVB_s, climate_s, local irradiance_s, B_{guild,s},
                  wind_s, B*wind, plant phylo, source study, image sampling)
VOC_{i,s}     ~ f(temp_s, drought_s, plant phylo, receiver guild, VOC source)
D_{i,s,t}     ~ odor * local plume(wind,shelter) + display contrast(light,background)
L | D         ~ local guide * receptor acuity + flower sway*wind + cue order
T | L         ~ physical contact + pollen deposition geometry + handling
```

`D×L×T` and a `W×scent×vision` interaction are identified as **causal** only within a real intervention/cohort design and after checking no missing plant/animal selection gates. Observational path/SEM alone cannot infer plant fitness or evolutionary selection. Prefer multi-scale model comparisons and spatial/phylogeny held-outs to fitting one very large nonidentified SEM.

**Conditional feedback theory:** the existing eco-evolutionary no-go `G ≤ B_f L Δg` can be referenced only after measured between-environment routeability gaps and a justified signal→selection response lift. Stage58 computes no feedback gain `G`, predicts no oscillation and does not convert the source wind effects into `Δg`.

## Stop rules / completed scope

Stage58 exact context simulator and offline test model, original wind evidence ledger, and bounded authentic original 305 VOC source scan; original source workflows are independent. **No full wind×odor×UV original factorial data collected or discovered**, and no measured source flower/bee/local pollen routeability coefficients identified. Keep PR Draft and main unchanged. Next actual empirical gate is accepted-species VOC overlap and experimental stage-specific source data; do not claim completed manuscript from this theory-only combination.
