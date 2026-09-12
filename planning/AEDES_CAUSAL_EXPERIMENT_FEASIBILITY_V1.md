# Aedes causal experiment feasibility v1

## Status

Execution planning only. This file is downstream of the immutable pre-data scientific freeze at `freeze/aedes-pre-data-admission-v1` and does not modify the frozen v1 worlds, targets, comparator semantics, endpoint domain, or success criteria.

## Executive conclusion

The frozen Aedes causal program is experimentally plausible, but the available literature argues against treating any single known neuropeptide axis as a reversible binary switch for the full H-to-O task.

The most efficient path is therefore staged:

1. verify state-signal manipulation and the A terminal channel in a strain-compatible system;
2. verify the B terminal channel and site-seeking assay separately;
3. test whether state-signal manipulation changes *relative A/B dependency*;
4. only if step 3 is positive attempt a fully integrated biological finite-task admission.

Do not begin by building a large genotype-by-state factorial experiment.

## 1. Existing components are unusually strong

### State-signal manipulation

NPYLR7 has both genetic and pharmacological handles. Duvall et al. (2019; Cell, DOI 10.1016/j.cell.2018.12.004) showed that NPYLR7 agonists suppress host seeking and that NPYLR7 null mutants are resistant to the drugs. A later SAR study identified three compounds active at 1 micromolar when delivered in non-nutritive saline 48 h before testing (Zeledon et al. 2024; DOI 10.1186/s13071-024-06347-w).

This is a particularly useful intervention because host suppression can be induced without blood nutrients.

### A terminal channel

Ir8a mutants provide a causal acidic-host-cue perturbation. Raji et al. (2019; Current Biology, DOI 10.1016/j.cub.2019.02.045) used a CO2 + lactic-acid uniport olfactometer and showed loss of lactic-acid attraction and acidic-odor responses in Ir8a mutants.

### B terminal channel

Ir68a-dependent Moist Cells provide the cleanest current oviposition-site handle. Tang et al. (2024; PNAS, DOI 10.1073/pnas.2407394121) used a wet-versus-dry container assay with approximately 70 gravid females, 72 h after blood feeding, and showed profound Ir68a-dependent failure to locate the wet container. Direct placement next to water restored normal egg-laying output, separating site finding from egg-laying competence.

## 2. Important strain/background constraint

The published components are not all in one laboratory background.

- next-generation NPYLR7 agonist work: Orlando strain;
- Ir8a host-cue work: Orlando strain;
- Ir68a humidity/oviposition work: LVP background;
- NPF/RYamide endocrine work: UGAL strain.

Therefore published effect sizes cannot be concatenated as if they came from one causal system.

The first integration decision should be whether to:

A. validate the pharmacological state manipulation in LVP and use the existing Ir68a lines; or
B. recreate/backcross the B-channel perturbation into the host-cue/state-manipulation background.

Option A is likely the shorter first experiment because the state intervention is pharmacological, but NPYLR7 specificity must be independently checked in the chosen background before mechanistic interpretation.

## 3. Existing data already reject a simple reversible NPF switch

Dou et al. (2024; PNAS, DOI 10.1073/pnas.2408072121) provide a useful hard constraint.

- midgut NPF knockdown reduces host attraction in previtellogenic females;
- synthetic NPF rescues that loss;
- RYamide injection suppresses host attraction in previtellogenic females;
- however, NPF injected after blood feeding does not restore host attraction while mature eggs remain in the ovaries.

Thus NPF is causal for host attraction but is insufficient to reverse the mature-gravid state.

Interpretation for adaptive-gain:

`R` should remain composite/unresolved. NPF/RYamide can perturb one coordinate of internal state, but they cannot currently be treated as the complete upstream router.

Do not spend the first experiment trying to prove a binary NPF-only H-to-O switch that published data already make unlikely.

## 4. Recommended minimal experimental sequence

### Phase 1 — reproduce the state manipulation cleanly

Use two preselected validated NPYLR7 agonists in non-nutritive saline with prospectively fixed dose and timing. The 2024 study demonstrates multiple active compounds at 1 micromolar with testing 48 h after feeding.

Measure:

- host-seeking in the established miniport/uniport logic;
- meal consumption/weight to exclude intake differences;
- locomotor/activity control;
- if possible, NPYLR7-null resistance or another receptor-specificity control in the same genetic background.

A single active-compound result is not enough. Use the `GO / UNRESOLVED / STOP` logic frozen in `AEDES_PHASE1_2_CONFIRMATORY_DECISION_RULES_V1.md`.

### Phase 2 — validate the B assay independently

Use the Tang et al. container-seeking geometry or a close preregistered replication:

- mature gravid females at a fixed post-blood time and circadian phase;
- wet versus dry container;
- mesh geometry minimizing accidental contact;
- two independent Ir68a alleles where available;
- direct-placement egg-laying competence control.

B is qualified only if the site-finding deficit replicates causally while direct egg-laying competence remains within the prospectively frozen control rule.

### Phase 3 — test state-signal sufficiency for terminal-channel reweighting

This is the highest-information experiment available before building an integrated genotype stack.

In a common validated background, compare vehicle versus nutrient-independent NPYLR7 activation in previtellogenic females.

Measure both terminal channels:

- A: acidic-host-cue sensory response and host-cue behavioral dependency;
- B: Moist-Cell/humidity sensory response, plus an age/state-appropriate humidity-orientation readout if one can be defined without pretending that previtellogenic females are already performing oviposition.

Interpretation:

- `A down, B unchanged`: host suppression is not sufficient for full H-to-O routing; strong negative for a single upstream state router;
- `A down, B sensory up but no O target behavior`: sensory reweighting, not yet finite-task routing;
- NPYLR7/NPF controls A while egg maturity / `cycle` independently controls B without a shared organism-level state representation: reject single-query R v1;
- coordinated shift in A/B dependency through a shared state representation: strongest justification to advance to the integrated endpoint experiment.

Do not score lack of egg laying in previtellogenic females as a B-channel failure; that would confound sensory routing with reproductive competence.

### Phase 4 — endpoint comparison under the frozen task

Only after Phases 1-3 pass, run the frozen H and O endpoint windows with the prospectively fixed A/B stimuli and target definitions.

At this stage the question is whether the biological comparator really behaves like one shared architecture or like externally pre-indexed branch policies.

The pre-indexed control remains mandatory: if context-specific fixed policies are the biologically correct comparator, branch-local gaps are zero even though the integrated mathematical fixture is positive.

## 5. Confirmatory discipline

Component qualification uses explicit `GO / UNRESOLVED / STOP` receipts.

- decision rules: `AEDES_PHASE1_2_CONFIRMATORY_DECISION_RULES_V1.md`;
- machine-readable receipt schema: `AEDES_PHASE_RECEIPT_SCHEMA_V1.json`;
- sample-size freezing rule: `AEDES_CONFIRMATORY_SAMPLE_SIZE_RULE_V1.md`.

Confirmatory n is computed before treatment/genotype effects are opened. Sequentially adding replicates until a threshold is crossed is prohibited.

Pilot data may establish assay variance, attrition, block structure and control ranges, but active-treatment pilot effects may not be used to choose `delta_min` or select the strongest compound.

## 6. What not to do

- do not combine published effect sizes from Orlando, LVP and UGAL as one empirical matrix;
- do not infer B recruitment merely because host seeking is suppressed;
- do not use NPF restoration in mature-gravid females as the central reverse-switch test; published evidence already shows it is insufficient while eggs are retained;
- do not treat receptor expression or response amplitude alone as decision dependency;
- do not add another receptor if Ir8a or Ir68a gives an inconvenient result;
- do not alter the four targets or comparator semantics after data are opened;
- do not infer genotype accessibility, stationary occupancy or waiting time from a positive finite-task result.

## 7. Practical bottlenecks ranked by information value

1. **Common-background validation of the state intervention** — highest priority. The pharmacological NPYLR7 route makes this tractable.
2. **Cross-state A/B dependency assay** — scientific bottleneck; closes G2/state-routing causality.
3. **Comparator-semantics justification** — conceptual bottleneck; positive integrated g is meaningless if state pre-indexes separate fixed policies.
4. **Background harmonization of Ir8a and Ir68a perturbations** — necessary for strong causal integration but should follow a positive Phase 3 signal.
5. **Genotype-policy mutation map** — later. Do not build this before the biological finite task is admitted.

## 8. Current go/no-go verdict

**GO for a staged causal feasibility experiment.**

**NO-GO for claiming empirical adaptive gain now.**

The shortest information-bearing next experiment is not a full gonotrophic-cycle model. It is a nutrient-independent state perturbation followed by direct measurement of both terminal-channel dependencies under the already frozen semantics.

## Literature anchors

- Duvall LB et al. 2019. Cell 176:687-701.e5. DOI 10.1016/j.cell.2018.12.004.
- Zeledon EV et al. 2024. Parasites & Vectors. DOI 10.1186/s13071-024-06347-w.
- Raji JI et al. 2019. Current Biology 29:1253-1262.e7. DOI 10.1016/j.cub.2019.02.045.
- Tang R et al. 2024. PNAS 121:e2407394121. DOI 10.1073/pnas.2407394121.
- Dou X et al. 2024. PNAS 121:e2408072121. DOI 10.1073/pnas.2408072121.
