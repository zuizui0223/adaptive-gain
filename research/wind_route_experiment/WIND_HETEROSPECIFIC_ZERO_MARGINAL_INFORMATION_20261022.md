# Wind can make an apparently uninformative other-species cue valuable by routing floral information

**22 October 2026 — exact constructed ecological-decision example, not an empirical finding.** This is a counterfactual bridge from the repository's existing finite adaptive-versus-fixed cue theory to a testable controlled wind×species experiment. It is **not** a new general information-theoretic theorem, not a demonstration of predation or social learning, and not an estimate of animal fitness. The existing four-world, three-query exact core is reused; finite-cost Bayes/noisy-cue calculations are a separate new extension.

## Main result and ecological relevance

An indicator of **another species' habitat/branch context** can carry **zero marginal information** about whether a resource is profitable yet increase accuracy from **75% to 95%** in an assumed windy two-cue budget when that other-species indicator guides *which of two branch-specific floral cues to inspect*. This occurs **only if the alternative indicator is actually more reliable than the weather-degraded native branch cue and if the two floral cues do not already suffice as a fixed set**. A sequence matters without any direct species→resource-profit correlation.

### Exact four equally likely worlds

A hidden ecological branch B and profitable-target action T are independent fair bits. Four worlds (B,T)=(0,0),(0,1),(1,0),(1,1); T is the focal accept/reject decision. Cues:

| B,T | Native/heterospecific *branch* cue when available | floral cue F0 | floral cue F1 | expensive direct assay |
|---|---:|---:|---:|---:|
| 0,0 | 0 | 0 | 1 | 0 |
| 0,1 | 0 | 1 | 1 | 1 |
| 1,0 | 1 | 0 | 0 | 0 |
| 1,1 | 1 | 0 | 1 | 1 |

Each branch cue costs 1 and reports B if available. F0 costs 1 and determines T only for B=0; F1 costs 1 and determines T only for B=1. The *off-branch* outputs are respectively 0 and 1 (not invented observational flower behaviors, but a declared **structural condition**). A direct perfect assay costs 3. World set, target frequencies and floral outcomes are identical across all four counterfactual weather×species contexts.

Conditional wind masking: still W=0 native branch cue reveals B; windy W=1 masks it (outputs a constant). In the species-indicator-present Z=1 treatment, a heterospecific cue independently reveals B, even when the native cue is masked. Z=0 masks the species cue. The Z cue conveys habitat/functional branch **not prey identification, pollen reward or true observed enemy contact**.

### Exact deterministic repository solver

Using the unchanged `adaptive_gain.core.adaptive_gain_receipt` on all four contexts:

| Wind | other-species branch cue | adaptive worst-path cost C_A | fixed resolving cost C_F | C_F − C_A |
|---|---|---:|---:|---:|
| still | absent | 2 | 3 | 1 |
| still | present | 2 | 3 | 1 |
| windy | absent | 3 | 3 | 0 |
| windy | present | 2 | 3 | 1 |

Proof sketch: if branch B is known, query precisely its relevant floral cue; two unit queries suffice. Any precommitted two unit-query subset fails: (branch,F0) cannot distinguish T within branch1; (branch,F1) cannot distinguish T in branch0; (F0,F1) identifies **(0,0) and (1,1)** as the *same* observed signature (0,1). Two branch queries provide no direct T information. Thus C_F>=3, and the cost-3 direct assay resolves the entire task. Under windy Z=0 neither branch indicator is available, so F0,F1 still cannot resolve the cross-target collision: C_A=C_F=3. With windy Z=1 branch routing is restored: 2 vs 3.

**Structural falsifier (implemented as an exact negative-control test):** If inactive F1 outputs 0 (not 1), then observing F0 and F1 together resolves the target in two queries. Under all W×Z contexts **C_A=C_F=2**, and the other-species indicator has **no routing value**. A real experiment must first verify the source-specific floral cue structure; branch-indicator usefulness cannot be inferred simply from the presence of a second species.

### Noisy cue and bounded-decision extension

Set a branch-indicator measurement error rate e, independently of B and T, 0<=e<=1/2. Errors are *synthetic assumptions*, not measured in any of the previously analyzed field datasets. For budget **two** unit observations, the exact rational-probability dynamic program allows cue order/second cue to depend on first outcome. A separate exhaustive fixed-subset Bayesian calculation does not.

For this task, verified by exhaustive policy DP:

`P_correct_adaptive(2,e) = 1 − e/2`,
`P_correct_fixed(2,e) = 3/4`.

The only way a wrong branch choice leads to target error is when the mistaken branch's irrelevant floral output coincides with the misleading target; under the uniform world prior this occurs with total probability e/2. Any first floral query, even followed by a perfect branch observation, cannot beat 3/4; two branch observations alone contain zero target information. The fixed two-query set F0+F1 reaches 3/4. Note that `C_A` is the **deterministic guaranteed-resolution** criterion, whereas these Bayesian accuracies explicitly **allow an incorrect decision**.

With two independently noisy branch-source cues of errors e_native and e_other, the exact optimum is

`P_correct_adaptive(2,e_native,e_other)=1−min(e_native,e_other)/2`.

Thus the species-cue rescue in a given weather state is the **sharp threshold**

`Delta_species_accuracy = max(0, (e_native − e_other)/2)`.

The best fixed budget-two success remains 3/4 even when both branch indicators are observable. **The cue's marginal mutual information with T is EXACTLY zero for every error rate 0<=e<=1/2** because B is independent of T. Its value is exclusively conditional: branch cue→choose F0 or F1→resolve T.

### One illustrative 2×2 weather×species prediction (not data)

Set still-native e0=.05; wind-native cue unavailable (equivalently completely uninformative e_w=.5 for decision success); other-species cue e_h=.1. These values are **not fit** to the wind flight studies, UK PoMS or Andrews LTER.

| Context | adaptive P_correct at B=2 | fixed P_correct at B=2 |
|---|---:|---:|
| Still, species absent | 0.975 | 0.750 |
| Still, species present | 0.975 | 0.750 |
| Wind, species absent | 0.750 | 0.750 |
| Wind, species present | 0.950 | 0.750 |

The between-weather difference-in-differences attributable to adding the branch-indicator cue is **+0.200**. At B=1 the best correct-decision probability is 0.75 regardless of the other-species cue, while at B=3 an available perfect direct assay yields 1.0 in all contexts. Hence this constructed species-cue rescue is **restricted to the intermediate information budget**; it cannot be inferred from flight speed.

## Explicit net-payoff and fitness identification ceiling

An improvement in target-choice accuracy is **not itself** an improvement in ecological fitness. Let \(\Delta R\) be the *measured* reward difference between a correct and an incorrect resource choice, and let \(k\) be any extra time/energy/exposure cost of obtaining the heterospecific cue rather than following the baseline two-query route. In the same assumed model, expected net payoff improvement is algebraically

\[
\Delta \Pi = \tfrac12\max(0,e_w-e_h)\,\Delta R - k.
\]

Thus the conditional routing cue can improve decision correctness and **still lower expected net benefit** when acquiring the cue is sufficiently costly. Neither \(\Delta R\) nor \(k\) is available from the cited PoMS, Andrews or honeybee flight datasets. Avoid converting model accuracy into measured pollen delivery, energetic efficiency, demographic growth or selection coefficients.

## Empirical falsification experiment: wind × other-species indicator × cue order × deadline

Primary experimental target: demonstrate a *measured* **other-species branch indicator**, not just an insect community correlation. A credible controlled assay should (1) randomly assign wind condition, (2) independently manipulate species indicator present versus sham/absent, (3) preserve four independently randomized B×T resource states with the same 50% target prevalence in every cell, and (4) measure the cue's conditional reliability e_h separately from any flower reward outcome. Don't import the illustrative 5%/10% errors as expected field parameters.

1. **Confirm sensing/cue architecture before outcomes.** Train individually tracked bees or other consumers to distinguish two habitat/resource branches. Make flower cue F0 informative only within B0 and F1 informative only within B1; independently demonstrate that their two fixed outcomes DO NOT resolve all opposite-target worlds (otherwise the structural-ablation result predicts no benefit). Train/calibrate an alternative visually/olfactorily observed heterospecific indicator that predicts B, but is **independent of T**, with sham-indicator positions randomized against B. Use the same actual rewards/available plants in all weather×species conditions.
2. **Cross controlled wind with source visibility/reliability.** Use randomized still versus calibrated wind, balanced within individual, with a separate cue-detection check to establish `e_w > e_h`. Wind alone could change speed without masking source cues—under that null **no information-topology rescue is predicted**. Species-indicator presence must be randomized and sham controls visual object attraction.
3. **Cross fixed/conditional acquisition with hard budgets.** At B=2, compare exactly TWO observations: fixed F0+F1 versus branch indicator first, followed by the single F_B selected according to that observation. Equalize exposure time, travel distance and reward frequency. Include B=1 and B=3 boundary controls if the apparatus can deliver an unambiguous third-stage assay. First use forced observation protocols to identify feasibility; only voluntary free-order querying supports the *behavioral* claim that animals adaptively acquire cues.
4. **Independent outcomes and falsifiers.** Primary: correct profitable-resource decision before a time deadline. Measure sequence, times, speed, energy and visit counts **separately**; do not equate increased speed with information access. Predeclare a wind×real-vs-sham species×conditional-vs-fixed interaction at B=2 and no such difference when the species cue is made unrelated to B, or when F0+F1 jointly resolves T. Randomize cue presentations and order within bee, block by individual/colony/date and estimate uncertainty at the independent subject level, not number of films.
5. **Natural ecological confirmation (later).** Once the controlled cue effect is reproducible, substitute **identified real heterospecific activity** for the artificial indicator and concurrently measure floral alternatives, predator/competitor/host interactions and actual use of their cues. A natural wind×species×flower association is not causal evidence unless the species cue and wind manipulation are separated.

## Claim ceiling and original-source contrast

- UK PoMS same-guild other-trap catches predict focal captures but parasitoid/spider bycatch plus wind interactions lacked robust cross-site added prediction. A 86-site hoverfly larval-diet wind signal was substantially genus/lineage-confounded. These data **do not estimate cue error e or prove a species routing interaction**.
- Andrews LTER 11-year minute visits allow observational wind×floral partner tests, but meadow-independent flower partner changes and bee-enemy lag associations did not resolve. These also lack a demonstrated other-species branch cue.
- Burnett et al. (2022) wind-tunnel honeybee flight experiment (Dryad DOI `10.25338/B8Z34Q`) changed speed/lateral motion without a clearly resolved increase in high-route occupancy; a subsequent speed decomposition is explicitly *post-route association*, not evidence weather masks a floral cue.
- The mathematical zero-MI conditional relevance phenomenon is a form of **information synergy** and an ecological *constructive example of the repository's existing routeability theory*, not a discovery that species with zero raw information generally improve fitness.
- `C_A,C_F` here concern **guaranteed exact target resolution**, while noisy-Bayes percentages concern **expected decision accuracy**. Neither equals pollen delivery, energy efficiency, realized network rewiring or animal fitness without additional biological measurement and a validated payoff map.

## Executable code and validation

`adaptive_gain/weather_species_routeability.py`: exact four-world task via existing `adaptive_gain.core`, separate Fraction-exact Bayesian adaptive DP and independently enumerated fixed subsets, zero target mutual-information check and weather×species 2×2 result. `tests/test_weather_species_routeability.py`: original 0..0.5 noise grid, **121** pairwise two-router threshold combinations, four deterministic context exact costs and four structural negative-control contexts plus invalid inputs, with `tests/test_core.py` as integration guard. CI workflow `.github/workflows/wind-heterospecific-routing-exact.yml` runs all checks and archives exact machine receipt. No preexisting manuscript or main is changed.

**Stop condition:** do not present the constructed +20pp as an observation in any population. Field progress requires measuring alternative-species signal reliability and the actual branch-specific cue confusion signature, or demonstrating directly manipulated source cue acquisition.
