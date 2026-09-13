# Aedes state-routing experiment v1

## Purpose

Prospectively test the one biological edge that remains unclosed in the current Aedes qualification:

`gonotrophic-state signal R -> relative use of terminal information sources A versus B`.

This protocol does not assume that the edge is true.  A null result, an asymmetric result, or a pure motor-state result is an admissible terminal outcome.

## Frozen structural roles

- `R`: endogenous gonotrophic-state information processed within the shared decision architecture, with NPF/RYamide dynamics as the leading mechanistic handle.
- `A`: IR8a-dependent acidic host-cue information under a fixed host-cue background.
- `B`: oviposition-site information, with Ir68a-dependent Moist Cell humidity/water-vapor sensing as the primary terminal candidate.

The structural four-world task is already frozen separately.  This experiment tests the causal routing interpretation; it must not redefine worlds, targets or costs after observing the result.

## Why a state intervention is needed

Blood feeding changes many variables simultaneously: nutrient state, egg maturation, endocrine signals, locomotion, circadian program and sensory physiology.  Comparing non-blood-fed with gravid mosquitoes therefore establishes state association but not the causal routing edge.

The test must intervene on candidate state signals while retaining explicit physiological-state controls.

## Core intervention panel

Use matched cohorts with at least the following intervention logic, subject to feasibility and ethical/rearing constraints:

### Previtellogenic side

1. vehicle / sham control;
2. NPF depletion or equivalent loss-of-function manipulation;
3. NPF rescue where the depletion design permits it;
4. RYamide elevation;
5. a selective NPYLR7 agonist as a particularly useful nutrient-independent host-suppression perturbation.

The key question is whether moving the endocrine signal toward the post-blood host-suppressed state changes terminal A use and/or recruits B use without a blood meal.  An NPYLR7 agonist is especially informative here because host-seeking suppression can be induced without using a nutritive blood meal; failure to recruit B under that manipulation would show that host suppression alone is insufficient for the full H-to-O routing switch.

### Post-blood / gravid side

1. matched blood-fed control at preregistered post-blood times;
2. NPF elevation/rescue toward the previtellogenic host-seeking signal;
3. where experimentally justified, RYamide-pathway attenuation.

The key question is whether changing the state signal restores A dependence and/or weakens B dependence while egg-development state is measured rather than assumed.

## Terminal-channel readouts

### A — host acidic-cue channel

Freeze one IR8a-dependent acidic stimulus and background before opening the full experiment.

Measure at least one early sensory readout and one behavioral readout where technically feasible:

- antennal / sensory-neuron response to the frozen acidic cue;
- host-approach or host-cue choice response under the frozen background.

Include Ir8a loss-of-function or an equivalent causal channel perturbation as the terminal-channel validation control.

### B — oviposition-site channel

Freeze a humidity/water-vapor stimulus usable with Ir68a-dependent Moist Cell assays.

Measure:

- Moist Cell response, preferably with the existing genetic-calcium-imaging logic where feasible;
- water-container / humidity-seeking behavior without direct water contact;
- egg-laying competence separately by placing gravid females adjacent to an oviposition substrate, so failure to find the site is not confused with failure to lay eggs.

Include Ir68a loss-of-function as the terminal-channel validation control.

## Dependency rather than raw response is the key endpoint

A change in sensory amplitude alone does not prove adaptive routing.  For each state/intervention, estimate the behavioral consequence of disabling each terminal channel.

Conceptually define:

- `D_A(R)`: loss of target performance when A is disabled at state R;
- `D_B(R)`: loss of target performance when B is disabled at state R.

A strong routing pattern requires a state-dependent change in the *relative dependencies*:

- host-seeking state: A is decision-relevant in the host branch;
- gravid/site-seeking state: B is decision-relevant in the oviposition branch;
- state-signal manipulation shifts these dependencies in the predicted direction.

Do not require branch exclusivity: Ir68a contributes redundantly to blood feeding, so `D_B(host)>0` is compatible with the candidate architecture.  The question is whether the information source is required for the frozen target distinctions and whether its decision weight/dependency is state-modulated.

## Three admissible mechanistic outcomes

### M1 — strong causal routing

State-signal manipulation changes terminal-channel dependency in the predicted direction, with channel-specific perturbations and rescue supporting the causal chain.

This can qualify `state_routing_causality_qualified=True` if all other task/comparator gates pass.

### M2 — sensory reweighting without task routing

State manipulation changes A or B response strength, but both terminal channels remain used similarly enough that the frozen finite-task routing interpretation is unsupported.

Report state-dependent sensory modulation; do not license the positive-gap-with-causal-routing claim.

### M3 — downstream motivational/motor switch

Terminal sensory responses/dependencies remain unchanged while behavioral output changes after state manipulation.

This supports gonotrophic motivational reprogramming but rejects the proposed sensory-routing mechanism for this task.

## Comparator-semantics gate

Before any empirical `g>0` claim, decide prospectively whether R is processed within one shared architecture or is effectively known before policy commitment.

If the appropriate biological comparator is externally pre-indexed by gonotrophic state, use the branch-split control in `adaptive_gain/aedes_context_semantics.py`; both branch-local gaps are zero.

Therefore a positive integrated mathematical fixture is not enough.  The experiment must justify the shared-architecture comparator biologically.

## Major confound controls

Measure or control:

- egg maturation / ovarian state;
- locomotor activity and general arousal;
- circadian time, especially for humidity seeking;
- sugar access and nutritional state;
- blood/protein meal timing and size;
- ability to fly / approach targets;
- ability to lay eggs once adjacent to the substrate;
- terminal-channel integrity under endocrine manipulation.

The longitudinal work on post-biting behavioral reprogramming makes circadian timing especially important because gravid humidity seeking is rhythmic and `cycle`-dependent.

## Decision table

| Frozen task admitted | A/B causal | R changes relative A/B dependency | Claim |
|---|---|---|---|
| no | any | any | no empirical adaptive-gain claim |
| yes | no | any | empirical task only; mechanism unresolved |
| yes | yes | no | positive gap may be structural, but no causal routing claim |
| yes | yes | yes | positive adaptive gap with causal context routing |

Downstream mutational accessibility and population claims remain separately gated by the genotype-policy, mutation-support, mutation-bias, population-process and absolute-rate declarations.

## Literature anchors motivating, not pre-answering, the test

- Dou et al. 2024, PNAS, DOI 10.1073/pnas.2408072121: reciprocal NPF/RYamide regulation of host attraction across the gonotrophic cycle.
- Duvall et al. 2019, Cell, DOI 10.1016/j.cell.2018.12.004: NPYLR7 agonists suppress host seeking, biting and blood feeding, including pharmacological host suppression without a nutritive blood meal.
- Siju et al. 2010, J Insect Physiol, DOI 10.1016/j.jinsphys.2010.02.002: blood-meal-dependent changes in antennal olfactory-neuron sensitivity.
- Tallon et al. 2021, BMC Genomics, DOI 10.1186/s12864-020-07336-w: state-dependent antennal chemosensory/neuromodulatory transcriptome across the first gonotrophic cycle.
- Christ et al. 2017, PLOS ONE, DOI 10.1371/journal.pone.0188243: feeding-induced changes in antennal-lobe sNPF/allatostatin; peptide injections suppress odor-mediated host seeking.
- Tang et al. 2024, PNAS, DOI 10.1073/pnas.2407394121: Ir68a-dependent Moist Cells are required for water-container seeking by gravid females, with egg-laying competence intact when placed at the site.
- post-biting behavioral reprogramming study, PMID 41379618: gravid humidity seeking emerges rhythmically with oviposition-site search and is `cycle`-dependent.

## Stop rule

Do not expand the candidate-system catalog or introduce additional terminal receptors until this causal routing edge is tested or direct existing evidence is found.  The present Aedes system already contains enough mechanistic handles for the next information gain to come from causal discrimination, not broader storytelling.
