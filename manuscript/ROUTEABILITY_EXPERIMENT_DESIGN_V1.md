# Direct ecological routeability experiment v1

Status: prospective experimental revision/follow-up reserve. This design does **not** modify the frozen Evolution Letters V5 submission surface.

## Goal

Test the core V5 claim by manipulating environmental information architecture directly, rather than inferring routeability from traits or observed interaction links.

The experiment uses the unique minimal strict-gain four-state / three-cue task already proved in the repository and a matched no-gain bypass control.

The critical property is not raw richness or cue frequency. It is whether the cue architecture permits **contingent routing**.

## Exact finite contrast

Both treatments contain:

- four ecological states;
- two accept / reject target states in a 2:2 balance;
- three unit-cost binary cues;
- the same per-cue outcome multiplicities: 1:3, 2:2 and 3:1.

The treatments differ only in how those cue outcomes are assigned across states.

### Routeable task

| state | target | terminal A | context | terminal B |
| --- | ---: | ---: | ---: | ---: |
| w0 | 0 | 0 | 0 | 0 |
| w1 | 0 | 0 | 1 | 1 |
| w2 | 1 | 1 | 1 | 1 |
| w3 | 1 | 0 | 0 | 1 |

Exact costs:

`C_A = 2` and `C_F = 3`.

Optimal contingent rule:

- observe context;
- if context = 0, inspect terminal B;
- if context = 1, inspect terminal A.

### Matched bypass control

| state | target | terminal A | context | terminal B |
| --- | ---: | ---: | ---: | ---: |
| w0 | 0 | 0 | 0 | 1 |
| w1 | 0 | 0 | 1 | 1 |
| w2 | 1 | 0 | 0 | 0 |
| w3 | 1 | 1 | 1 | 1 |

Exact costs:

`C_A = C_F = 2`.

The same context-contingent two-cue schedule can resolve this task, but it is not uniquely valuable because the fixed terminal pair `{A, B}` also resolves every target.

Therefore the control matches cue number, state number, target balance and cue marginals while removing the strict adaptive gain.

### Stronger match: pairwise information is also identical

The executable contrast has a stronger property than marginal matching.

For each of the six named variable pairs among

`{target, terminal A, context, terminal B}`,

the routeable and bypass-control tasks have the same canonical binary 2 x 2 contingency-count profile after ignoring arbitrary 0/1 symbol labels. Consequently they have the same **pairwise mutual information** for every target-cue and cue-cue pair.

This means that neither single-cue informativeness nor any pairwise mutual-information matrix can distinguish the two architectures.

The match is stronger still: the **full three-cue joint distribution** is identical. In both architectures the four cue vectors occur once each under uniform states:

`000, 001, 011, 111`.

Thus the environment-side distribution of cue combinations is exactly matched. What differs is how the same cue-combination surface maps onto the focal target/action structure.

The physical implementation can therefore reuse the same four cue combinations in both architecture groups:

| cue vector | routeable target | bypass target |
| --- | ---: | ---: |
| `000` | 0 | 1 |
| `001` | 1 | 0 |
| `011` | 0 | 0 |
| `111` | 1 | 1 |

Only `000` and `001` change reward / accept–reject assignment. The cue symbols, cue combinations and their frequencies need not change between architecture groups.

This is the cleanest experimental expression of the relational claim: routeability changes while the physical environmental cue surface is held fixed because the focal action map changes.

Yet the exact resolution costs differ:

- routeable: `C_A=2, C_F=3`;
- bypass control: `C_A=C_F=2`.

The contrast therefore isolates a genuinely **higher-order conditional organization** of ecological information. Routeability is not reducible to how informative individual cues are, nor to the strengths of pairwise associations among cues and target.

This statement is deliberately about pairwise information quantities that are invariant to relabeling binary cue symbols. Fixed semantic 0/1 labels are not claimed to have identical signed contingency tables in every target-cue pair.

The higher-order difference is also explicit. Under uniform states, the fixed terminal pair carries `0.5 bit` about the target in the routeable task but `1.0 bit` in the bypass control. Conditional on that terminal pair, the context cue contributes `0.5 bit` in the routeable task and `0 bit` in the control. The route cue is therefore non-bypassable only in the strict-gain architecture.



Executable source:

- `adaptive_gain/ecological_routeability_experiment.py`
- `tests/test_ecological_routeability_experiment.py`

## Primary 2 × 2 manipulation

Factor 1: **task architecture**

- routeable;
- matched bypass control.

Factor 2: **information access**

- contingent;
- fixed.

The main budget is exactly two cue observations.

### Contingent access

Observation 1: context.

Observation 2:

- terminal B after context = 0;
- terminal A after context = 1.

The second cue therefore depends on the first cue's outcome.

### Fixed access

Observation 1 is one terminal cue and observation 2 is the other terminal cue, independent of state.

The first terminal cue remains visible while the second is presented, matching the two-stage timing and cue persistence of contingent access. The A→B versus B→A order is counterbalanced independently of state.

Thus the access manipulation is not sequential versus simultaneous presentation. Both arms receive two sequentially staged observations; they differ in whether the identity of observation 2 depends on the outcome of observation 1.

## Exact information prediction at budget 2

Under a uniform distribution of the four states and optimal classification after the two observed cues:

| architecture | contingent access | fixed terminal access |
| --- | ---: | ---: |
| routeable | 1.00 | 0.75 |
| bypass control | 1.00 | 1.00 |

Thus the exact information-level interaction is:

`(1.00 - 0.75) - (1.00 - 1.00) = 0.25`.

This **25 percentage-point value is an information ceiling contrast**, not a required behavioral effect size. Real animals can make perceptual, learning and motivational errors.

The empirical prediction is only that the contingent-versus-fixed advantage is larger in the routeable architecture than in the bypass control.

## Budget ladder

The main experiment should include or preregister a budget manipulation.

### B = 1 — below adaptive cost

Freeze the one-cue policy prefixes:

- adaptive-policy prefix: context (`q_route`) only;
- fixed-policy prefix: one terminal cue (`q_left`; `q_right` is accuracy-equivalent under the uniform state design).

One cue observation is insufficient to guarantee the target in either architecture. The exact uniform-state ceilings are 0.50 for the adaptive-policy prefix and 0.75 for the fixed-policy prefix in **both** architectures. Therefore the architecture × access interaction is exactly 0 at B=1.

### B = 2 — routeability-sensitive window

For the routeable task:

`C_A <= B < C_F`, i.e. `2 <= 2 < 3`.

Prediction: contingent access has an information advantage over fixed access.

For the bypass control, (C_A=C_F=2), so contingent access has no exact advantage.

### B = 3 — above fixed cost

All three cues are available to both access arms.

Prediction: all four architecture × access cells have exact information ceiling 1.00, so the architecture × access interaction is exactly 0 at B=3.

Thus the exact architecture × access information interaction across the ladder is:

| budget | interaction |
| ---: | ---: |
| B=1 | 0.00 |
| B=2 | 0.25 |
| B=3 | 0.00 |

This budget ladder is the strongest experimental connection to V5 because it localizes the structural advantage to the predicted **window**, rather than merely asking whether animals can learn a contextual rule.

## Biological implementation

Use a laboratory pollinator with established artificial-flower learning protocols. Species choice is operational and should follow local husbandry, ethics and regulatory constraints.

A bumblebee system is a natural first implementation because artificial-flower choice, colour learning and sequential foraging assays are well established.

### Ecological target

Each artificial flower state belongs to one of two response classes:

- target 1: accept / exploit;
- target 0: reject / leave.

Correct acceptance can be reinforced with sucrose reward. Rejection trials should avoid introducing a unique unintended cue before the response is recorded.

### Cue channels

The three cue channels must be independently controllable.

Recommended implementation:

- **context:** a coarse outer collar / patch cue that becomes available before the terminal information and remains visible while the terminal cue is presented;
- **terminal A:** one local cue window;
- **terminal B:** a second local cue window.

The two terminal cue channels should be physically and temporally matched.

Do not literally confound A and B with permanent left/right position. Randomize or rotate physical positions so cue identity is not a side cue.

### Information presentation

A clean implementation uses shutters, cards or other non-flickering displays so that exactly the permitted cue channels are visible on each trial.

For the primary B=2 contrast:

- contingent treatment reveals context first and then the context-selected terminal cue **while the context remains visible**;
- fixed treatment reveals one terminal cue first and then the other terminal cue on the same timing schedule, with the first terminal cue remaining visible during the second;
- total number of informative cue channels, stage durations and cue-persistence rules are matched.

The persistent-context rule is deliberate. Bumblebees can use contextual cues to choose opposite colour targets, but purely sequential priming that disappears before the target can be much harder to learn unless supported by additional spatial structure. The primary implementation therefore tests contingent information without making success depend on fragile delayed-context memory.

The response is recorded only after the allowed cue observations have been presented.


## Behavioral feasibility precedent

The physical implementation is constrained by prior bee-learning work rather than invented from the formal task alone.

- Dale et al. (2005) showed that bumblebees can learn context-dependent colour choices. Concurrent or spatially supported context cues were effective, whereas a weak sequential priming cue presented several seconds before the targets was difficult to use reliably. This motivates the persistent-context implementation above.
- Fauria et al. (2002) showed contextual isolation of opposing visual associations in bumblebees, supporting the feasibility of learning different stimulus-response mappings under different contexts.
- Graver et al. (2026) showed that *Bombus impatiens* changes colour-versus-odor cue weighting with the spatiotemporal scale of cue presentation. Cue timing and persistence must therefore be matched and reported as part of the manipulation, not treated as incidental apparatus details.
- Spaethe et al. (2026) showed that *Bombus terrestris* flexibly changes which visual features it learns as cue discriminability changes. Physical cue symbols should therefore be pretested for discriminability and counterbalanced across context/A/B roles.

These studies establish feasibility of contextual and multicue learning. None tests the matched routeable-versus-bypass architecture defined here.

### Physical-material qualification before Pilot A

The formal cue bits are not themselves a physical stimulus specification. Exact colours, patterns, printed materials, Perspex pieces, displays and viewing distances remain local implementation choices.

A candidate material set must therefore pass a separate **architecture-neutral cue qualification** before any confirmatory treatment allocation.

For each of the three cue identities (context, terminal A, terminal B):

1. test the two physical cue outcomes in a simple differential two-choice task outside the routeable/bypass architecture;
2. require at least **80% correct over the last 20 scored choices** for that cue identity;
3. require the absolute difference between the best and worst of the three final-20 accuracies to be **<= 0.10**.

The 80% criterion follows common operational practice in bumblebee visual-discrimination training; here it is used only to qualify the **apparatus/material set**, not to select confirmatory animals.

If any cue fails, or if one cue is much easier than the others, replace/resize/recalibrate the physical symbols and repeat this architecture-neutral pretest. Do **not** inspect B=2 architecture x access outcomes and then alter the cue set.

This rule addresses a real multicue confound: bumblebees can overweight the most salient or easiest feature and underlearn other elements. A routeability contrast is only interpretable if success is not driven by one trivially dominant visual component.

Additional physical constraints:

- q_route must remain visible during terminal presentation and response;
- q_left and q_right use the same terminal-symbol family, with query identity carried by the inspection window rather than by a permanently easier cue type;
- context and terminal symbol assignments are counterbalanced through the already frozen bit-flip profiles;
- fixed access remains sequential and persistence-matched rather than simultaneous;
- contacted artificial-flower surfaces follow one frozen cleaning protocol to suppress scent-marking cues;
- exact material specifications are hash-frozen after qualification and before confirmatory allocation.

Machine-readable gate:

- `validation/routeability_physical_cue_feasibility_gate_v1.json`.

This qualification does not replace Pilot A. It establishes that the chosen physical cue contrasts are individually learnable and not grossly imbalanced; Pilot A still calibrates response timing, timeouts, side/window bias and apparatus reliability.

## Guided versus autonomous routing

The exact contrast supports two implementation levels.

### Phase 1 — guided contingent presentation

**This is the frozen primary confirmatory implementation for H1 and H2.**

The apparatus reads the context outcome and reveals the correct branch-specific terminal cue. In the contingent arm the animal does not choose which terminal channel to inspect during the confirmatory experiment.

Purpose: isolate the information-architecture contrast with minimal motor or exploration demands, so the primary architecture × access test is not confounded with learning the routing policy or making an additional terminal-window action choice.

This phase tests whether the matched architectures differ when the theoretically sufficient contingent information is actually delivered. It does not by itself show that an animal learns to choose which cue to inspect.

### Phase 2 — autonomous routing

This is a **separate mechanistic follow-up**, not part of the frozen guided H1/H2 dataset unless independently preregistered as a new confirmatory experiment. Autonomous-routing trials must not be pooled with the guided primary analysis.

After the context cue is visible, the animal is given two terminal inspection ports or cue windows but can acquire only one within the two-cue budget.

The frozen routing policy is the **same in both architectures**:

- context = 0 → inspect terminal B;
- context = 1 → inspect terminal A.

The repository verifies that this policy has exact uniform-state target accuracy 1.00 in both the routeable and bypass-control tasks. Reversing the routing rule is insufficient.

Primary autonomous-routing outcomes:

- correct terminal-window choice conditional on context;
- final accept/reject accuracy;
- latency from context exposure to terminal choice.

This phase tests whether the organism can exploit the branch structure rather than receiving the routed terminal cue passively.

The guided phase should remain available as a positive structural calibration. If guided contingent presentation succeeds but autonomous routing fails, the result isolates a policy-learning or action-selection bottleneck rather than invalidating the information architecture itself.

## Primary endpoint

**Correct accept/reject decision within a frozen response window** under the allowed cue budget.

Each initiated test trial is scored:

- 1: correct accept/reject decision within the response window;
- 0: incorrect decision **or no terminal decision before timeout**.

Timeout / abandonment trials therefore remain in the primary denominator. They must not be deleted and the primary analysis must not condition on having produced a response.

The response-window duration is an apparatus/procedural quantity to be frozen from architecture-neutral pilot timing, before the confirmatory treatment contrast is opened.

The primary model tests the interaction:

`task architecture × information access`.

The directional hypothesis is:

> the contingent-minus-fixed success contrast is positive in the routeable task and larger than the corresponding contrast in the bypass control.

Do not require the observed interaction to equal 0.25.

## Secondary endpoints

Allowed secondary outcomes:

- conditional choice accuracy among trials with a terminal response;
- timeout / abandonment probability;
- decision latency after the final allowed cue;
- first inspection / approach error;
- number of revisits when revisits are possible;
- learning slope across trials.

The conditional-accuracy analysis is explicitly secondary because conditioning on response can select different subsets of trials across architectures or access modes.

Secondary outcomes cannot replace the primary success interaction after outcomes are inspected.

## Positive and negative controls

### Full-information positive control

At B=3, expose all three cues.

Purpose: verify that both architectures are learnable when information is not limiting.

### Below-threshold control

At B=1, expose only one cue.

Purpose: verify that the routeability advantage is not a generic preference for one cue symbol.

### Cue-identity counterbalance

Counterbalance the physical symbols assigned to 0/1 outcomes and to context/A/B channels across colonies or independent cohorts.

Purpose: prevent innate colour, pattern or odor preferences from becoming the treatment.

## Training and test separation

Training must not reveal the focal comparison by giving one architecture systematically more experience, and it must not create post-randomization selection.

Preferred primary structure:

1. architecture-neutral familiarization with the apparatus and response port;
2. an architecture-neutral engagement check, completed **before** factorial treatment assignment where operationally possible;
3. random assignment to architecture, access mode and budget;
4. a **fixed amount** of architecture-specific full-information training, identical in dose across randomized cells;
5. main test with the frozen information-access manipulation;
6. optional full-information manipulation check.

Do not require an architecture-specific accuracy threshold for entry into the primary test. An animal that learns slowly is part of the randomized biological response and should not be silently removed because of low training accuracy.

Record architecture-specific training acquisition explicitly:

- training accuracy by block;
- trials or time to a prespecified descriptive criterion;
- non-response / disengagement;
- whether the individual completes the fixed training dose.

If husbandry makes a hard performance criterion unavoidable, criterion attainment becomes a separate treatment-dependent outcome and the test-phase analysis among criterion-reachers is labelled **per-protocol**, not the sole randomized primary analysis.

The between-subject primary design remains preferred. If the same animal receives multiple architecture or access conditions in a separate pilot, use independent cue alphabets and counterbalanced order and do not substitute that pilot for the primary randomized design.

## Randomization

Freeze before data collection:

- state frequency: uniform 1/4 per state in the primary test;
- trial order: randomized within prespecified blocks;
- cue-symbol mapping;
- physical location of cue windows;
- architecture assignment;
- access-mode assignment;
- colony balancing where applicable.

### Machine-generated schedule

The repository now contains a deterministic schedule builder for a clean between-subject implementation:

- architecture is between subjects;
- access mode is between subjects;
- budget is between subjects;
- the full factorial therefore has 12 treatment cells.

Within every individual, each four-trial block contains all four ecological states exactly once. Terminal cue positions are swapped on half of trials, and fixed terminal order is balanced independently of state. At (B=1), fixed access uses terminal A and terminal B equally often across trials rather than permanently privileging one terminal cue. At (B=3), both access arms receive the same complete three-cue surface.

Binary cue symbols are counterbalanced across individuals with four orthogonal flip profiles:

`000, 011, 101, 110`.

Within every treatment cell this balances each cue's symbol mapping and all pairwise combinations of cue-symbol flips.

Executable surface:

- `adaptive_gain/routeability_experiment_schedule.py`;
- `examples/build_routeability_experiment_schedule.py`;
- `validation/routeability_experiment_schedule_gate_v1.json`.

The schedule builder requires the number of individuals per cell to be a multiple of four for exact symbol counterbalancing. Its minimum of four individuals per cell is a **software balance requirement only**. It is not the final powered biological sample size.

### Colony-blocked biological-unit assignment

Once the definitive individuals per cell is frozen, actual foragers are assigned from an **architecture-neutral eligible roster**.

Eligibility is applied before architecture-specific training. The roster contains individual and colony identity only; treatment assignments, architecture-specific learning performance and focal outcomes are forbidden inputs.

The primary allocation uses complete 12-cell blocks **within colony**. Each complete block contains one individual in every architecture × access × budget cell. This keeps the factorial contrast represented within each contributing colony rather than relying on the mixed model to repair avoidable treatment–colony imbalance after the fact.

Machine surface:

- `adaptive_gain/routeability_roster_randomization.py`;
- `examples/randomize_routeability_roster.py`;
- `validation/routeability_roster_randomization_gate_v1.json`.

The exact eligible roster is checksum-frozen before assignment. Excess eligible individuals that are not required for complete blocks are written to a separate unassigned file. They are **not** a treatment-performance-dependent reserve and cannot be added later because one randomized cell learns poorly or produces inconvenient outcomes.

The final randomization seed is frozen before the assignment file is generated. The resulting assignment receipt records colony block capacity, blocks used per colony, treatment-cell counts and cue-symbol counterbalance counts.

Colony remains a biological hierarchical factor in the primary model even under this blocking scheme.

## Exclusion rules

Define before data collection and keep them independent of treatment performance.

Allowed examples:

- failure to initiate the apparatus during architecture-neutral familiarization;
- failure to initiate any test trial after the fixed training dose;
- apparatus malfunction or cue-presentation error;
- loss of individual identity or unavoidable husbandry loss before test.

Not allowed for the randomized primary analysis:

- architecture-specific training accuracy below a threshold;
- low test accuracy;
- slow decisions;
- an inconvenient treatment-specific learning trajectory.

Report all exclusions and their randomized treatment cells. Differential training completion or non-response across architectures is itself diagnostically relevant and must not be hidden by conditioning.

## Manipulation checks

Observed trial logs are validated against the machine-frozen schedule before biological scoring.

The validator checks:

- exact individual/trial key match;
- revealed cue sequence;
- cue-exposure duration tolerance;
- persistent context during terminal presentation when required;
- apparatus-error flags;
- response latency and terminal-decision coding.

Crucially, it separates **protocol invalidity** from **biological failure**. An incorrect decision or timeout on a correctly presented trial is a valid biological outcome scored 0. A cue-presentation mismatch or apparatus error is protocol-invalid and is reported separately rather than silently converted into a behavioral failure.

Executable surface:

- `adaptive_gain/routeability_trial_validation.py`;
- `tests/test_routeability_trial_validation.py`.

Required manipulation checks:

1. cue-exposure durations do not systematically differ between routeable and bypass tasks within access mode;
2. no individual cue alone predicts target above the structure implied by the frozen stimulus table;
3. state frequencies and reward frequencies are balanced;
4. physical cue symbols are counterbalanced;
5. full-information B=3 performance demonstrates that the state-response mapping is learnable.

## Analysis hierarchy

### Confirmatory H1 — architecture × access interaction

Binary correctness as the outcome.

Use an individual-level repeated-measures model if each animal contributes multiple trials, with animal and colony structure handled explicitly.

The confirmatory term is the architecture × access interaction.

### Confirmatory H2 — budget-window localization

When B=1,2,3 are implemented, test the preregistered localization contrast: the architecture × access difference should be larger at B=2 than at the two boundary controls B=1 and B=3.

The exact information-level pattern is 0, 0.25, 0 across B=1,2,3. As with the B=2 ceiling, these are structural information predictions rather than required behavioral accuracies.

The confirmatory contrasts are frozen explicitly as:

`Δ_B = [p(R,C,B) - p(R,F,B)] - [p(K,C,B) - p(K,F,B)]`,

where R is routeable architecture, K is bypass control, C is contingent access and F is fixed access.

- **H1:** `Δ_B2 > 0`.
- **H2:** `Δ_B2 - 0.5 × (Δ_B1 + Δ_B3) > 0`.

Use hierarchical gatekeeping: H1 is primary; H2 retains confirmatory status only if H1 passes the frozen inferential gate. Otherwise H2 is reported descriptively.

The primary trial-level model is a binomial logistic mixed model with the full categorical architecture × access × budget factorial, individual random intercept, and colony random intercept where multiple colonies are used. Trial order is a secondary learning/fatigue sensitivity rather than a model-selection knob for H1.

Machine-readable gate:

- `validation/routeability_experiment_analysis_gate_v1.json`.

### Secondary — latency

Analyze only after H1 is frozen and reported.

A speed-accuracy trade-off must be considered; lower latency is not automatically better if accuracy declines.

## Independent-unit policy

The independent biological unit is the individual forager, with colony treated as a higher-level grouping factor where relevant.

Trials are repeated observations, not independent animals.

Do not report trial count as the biological sample size.

## Pilot and sample size

Do not power the definitive experiment from the theoretical 1.00 versus 0.75 information ceiling.

The procedural pilot is frozen separately in:

- `manuscript/ROUTEABILITY_PROCEDURAL_PILOT_V1.md`;
- `validation/routeability_procedural_pilot_gate_v1.json`.

It has two roles only.

**Pilot A** uses an architecture-neutral calibration task to freeze the response window and quantify timeout, side bias and apparatus failure.

**Pilot B** uses pooled full-information `B=3` trials to estimate nuisance parameters such as:

- baseline full-information success;
- within-animal repeated-trial correlation;
- learning / fatigue across calibration trials;
- colony heterogeneity;
- dropout and non-response rates.

The pilot is not permitted to estimate H1, H2, a routeable-minus-bypass contrast, or any `B=2` architecture × access effect for power planning.

### Three-stage sample-size freeze

Sample-size planning is separated into three explicit stages.

1. **Nuisance receipt.** Freeze Pilot A/B nuisance quantities before opening the focal contrast.
2. **Conservative screening.** Use `adaptive_gain/routeability_experiment_power.py` and `examples/plan_routeability_experiment.py` to obtain a balanced-cell screening calculation. The effect input must be an externally justified probability-scale SESOI, not the theoretical 0.25 information ceiling and not a focal pilot effect.
3. **Nuisance GLMM and robustness expansion.** Fit a pooled full-information `B=3` nuisance-only GLMM that contains no architecture, access, `B=2`, H1 or H2 labels. Freeze the individual and colony random-intercept SDs, then mechanically cross the frozen three baseline profiles with four nuisance profiles (nominal, variance stress, attrition stress, combined stress). The resulting **12 robustness IDs** must be identical at every candidate N. Pilot-anchored probabilities and stress values are never clipped; invalid scenarios fail closed.
4. **Final simulation.** Before confirmatory collection, use the already frozen robustness policy to simulate the frozen binomial mixed model across every multiple-of-four candidate N from the smallest colony-feasible value `4*ceil(colony_count/4)` through a husbandry-defined operational maximum, using the pre-allocation colony count and externally frozen H1/H2 SESOI.

The nuisance-to-robustness machine surface is:

- `examples/fit_routeability_pilot_nuisance_glmm.R`;
- `examples/summarize_routeability_pilot_nuisance_glmm.py`;
- `adaptive_gain/routeability_robustness_grid.py`;
- `examples/build_routeability_robustness_grid.py`;
- `validation/routeability_nuisance_robustness_grid_gate_v1.json`.

The machine-readable firewall is:

- `validation/routeability_experiment_pilot_power_gate_v1.json`;
- `validation/routeability_sesoi_gate_v1.json`;
- `validation/routeability_nuisance_robustness_grid_gate_v1.json`.

The external smallest-effect threshold is now frozen **before pilot/confirmatory treatment contrasts**:

- H1 `Delta_B2` SESOI = **0.10** on the probability scale;
- H2 budget-localization SESOI = **0.10**;
- provenance type = `practical_decision_threshold`;
- freeze ID = `practical_decision_threshold_frozen_2026-09-29`.

The 0.10 threshold means one additional correct decision per ten test trials attributable to the routeability-specific interaction. It is a smallest-worthwhile-effect threshold, not a prediction of the true effect. External bumblebee artificial-flower studies that use 80% learning criteria or report >85% discrimination accuracy provide feasibility context only; their accuracies are not converted into the focal effect estimate.

The screening calculator uses a conservative Bernoulli variance bound and repeated-trial design effect, then rounds randomized individuals per cell upward to the four-profile counterbalance multiple. It is intentionally not labelled the final powered N.

Thus the only legitimate path to the definitive N is:

[
	ext{architecture-neutral / pooled nuisance pilot}
ightarrow
	ext{externally frozen SESOI}
ightarrow
	ext{screening surface}
ightarrow
	ext{final GLMM simulation}.
]

The focal architecture × access effect never feeds backward into its own sample-size target.

## What would falsify the empirical bridge?

The experimental bridge is weakened if:

- the architecture × access interaction is absent or reverses under the preregistered test;
- the predicted B=2 concentration is absent and the same contrast appears equally at B=1 or B=3;
- performance differences disappear after correcting a cue-identity or exposure-duration imbalance;
- the bypass control shows the same contingent advantage as the routeable task.

A failed behavioral experiment does not falsify the exact finite theorem. It would show that the theoretical information advantage is not expressed under the tested animal, cue implementation or ecological cost regime.

## Claim ceiling

A positive experiment would establish that **matched ecological alternatives can differ in behavioral cost because of contingent cue architecture**, under a controlled artificial-flower decision task.

It would not by itself establish that routeability explains natural plant-pollinator network rewiring, niche breadth or community stability.

Those remain separate ecological bridges.


## Experimental feasibility references

- Dale, K., Harland, D. P., Manning-Jones, A. & Collett, T. S. 2005. Weak and strong priming cues in bumblebee contextual learning. *Journal of Experimental Biology* 208:65–74. DOI: 10.1242/jeb.01370.
- Fauria, K., Dale, K., Colborn, M. & Collett, T. S. 2002. Learning speed and contextual isolation in bumblebees. *Journal of Experimental Biology* 205:1009–1018. DOI: 10.1242/jeb.205.7.1009.
- Graver, K., Sommer, J., Rao, V., Tafuri, G. & Sprayberry, J. D. H. 2026. Timing impacts responses to color and odor in a model insect, the bumblebee *Bombus impatiens*. *Journal of Experimental Biology* 229:jeb251126. DOI: 10.1242/jeb.251126.
- Spaethe, J., Hutzenthaler, S., Dietz, A., Gehrig, K., Foster, J. & Stöckl, A. 2026. Bees flexibly adjust decision strategies to information content in a foraging task.
