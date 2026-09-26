# Aedes state-to-terminal routing audit v1

## Question

Does the current Aedes literature close the biological edge

`gonotrophic state -> which terminal information source is used`

strongly enough to instantiate the adaptive-gain routing interpretation?

## Verdict

**No — not yet.**

The literature now strongly supports all of the following separately:

1. a circulating gonotrophic-state signal linked causally to host attraction;
2. state-dependent reprogramming of peripheral chemosensory transcription and physiology after a blood meal;
3. a causal host-associated acidic-odor channel;
4. a causal gravid oviposition-site hygrosensory channel.

But it does **not** yet show that experimentally manipulating the NPF/RYamide state signal causes the organism to switch between the exact terminal information sources used in the frozen Aedes task.  That missing causal edge is the decisive G2/G7 handoff for interpreting the finite task as one endogenous sensing architecture rather than as a laboratory juxtaposition of two behaviors.

## R: internal gonotrophic-state signal

Dou et al. (PNAS 2024; PMID 38950363; DOI 10.1073/pnas.2408072121) show that:

- NPF is high in the previtellogenic state and promotes human attraction / biting;
- blood or protein feeding lowers NPF during the host-seeking refractory phase;
- RYamide secretion increases after protein/blood feeding;
- RYamide injection suppresses host attraction;
- NPF knockdown suppresses host attraction and NPF injection rescues it.

This is strong evidence that NPF/RYamide dynamics encode or participate causally in the reproductive-state switch relevant to host seeking.

The same paper notes RNA-seq evidence that a RYamide receptor (AAEL017005) is expressed in antennae as well as brain, ovaries, abdominal tip, maxillary palp and rostrum.  This makes a peripheral sensory action plausible but does not establish that RYamide directly controls the A or B channel.

Recent receptor deorphanization further confirms two bona fide Aedes RYamide receptors (AAEL017005 and AAEL019786/NPYLR7), but emphasizes rectal/hindgut physiology as a major target.  Therefore endocrine-state signaling is real, but its sensory-routing site remains unresolved.

## State-dependent peripheral sensory reprogramming

The peripheral system is not static across the gonotrophic cycle.

- Siju et al. (J Insect Physiol 2010; PMID 20153749; DOI 10.1016/j.jinsphys.2010.02.002) report blood-meal-dependent changes in antennal olfactory-neuron sensitivity.  Prior work cited there showed down-regulation of lactic-acid-sensitive grooved-peg neurons after blood feeding; the study itself found increased sensitivity to several compounds associated with oviposition sites at 24–72 h post-blood meal.
- Tallon et al. (BMC Genomics 2021; PMID 33478394; DOI 10.1186/s12864-020-07336-w) show age- and state-dependent regulation of the antennal transcriptome throughout the first gonotrophic cycle, including broad changes in chemosensory and neuromodulatory genes.  No simple permanent on/off switch was observed.

These results support biological state-dependent reweighting/reconfiguration of sensory processing, but they do not identify NPF/RYamide as the causal upstream controller of the relevant terminal channels.

## A: host-associated acidic cue

IR8a is a strong causal handle for acidic host volatiles.  Published CRISPR work shows that loss of Ir8a eliminates lactic-acid attraction and reduces attraction to human odor.  This is suitable as a candidate terminal host-information channel, with the important caveat that host seeking is multi-cue and IR8a is not the only host-sensory pathway.

## B: oviposition-site information

Ir68a-dependent Moist Cells are currently the strongest B candidate.

Tang et al. (PNAS 2024; PMID 39159375; DOI 10.1073/pnas.2407394121) show that:

- Ir68a is required for Moist Cell responses to humidity;
- gravid Ir68a mutants are profoundly impaired in finding water-filled containers;
- when placed directly adjacent to water, Ir68a mutants lay eggs normally;
- Ir68a-dependent Moist Cells therefore contribute to locating an oviposition site rather than egg-production or egg-laying capacity itself.

This provides an unusually clean terminal information-source perturbation.  However, Ir68a also contributes redundantly to blood feeding, so it cannot be declared branch-exclusive.

## The decisive missing experiment

The shortest causal test is not another receptor screen.  It is a crossed state-manipulation x terminal-channel experiment.

Prospectively declare two endocrine-state manipulations that move R in opposite directions while holding blood-meal history as controlled as feasible, for example:

- NPF elevation / rescue versus NPF depletion;
- RYamide elevation versus matched control.

Then measure both terminal channels in the same animals or matched cohorts:

### A readout

Use the frozen IR8a-dependent acidic-host-cue stimulus under a fixed CO2/background context.  Measure peripheral or early sensory response plus host-approach output.

### B readout

Use the frozen Ir68a-dependent humidity/water-vapor stimulus.  Measure Moist Cell calcium response or equivalent peripheral activity plus water-container seeking.

### Required causal pattern for strong routing admission

A strong routing result would require the endocrine-state manipulation to change the *relative decision use* of A versus B in the predicted direction, while controls show that this is not explained solely by locomotion, egg maturity, generalized arousal, sensory damage, or motor incapacity.

The strongest version would show one or more of:

1. state manipulation changes terminal sensory responsiveness itself;
2. state manipulation changes whether terminal-channel perturbation affects behavior;
3. rescue of the state signal restores the branch-specific terminal-channel dependence.

A change only in downstream motor choice with unchanged terminal information use is biologically interesting but does not establish the finite-sensing routing interpretation.

## Context-semantics hard stop

The gonotrophic state must not be treated as a free experimenter label.

If `R` is externally known before policy commitment and the fixed comparator is allowed to choose a different bundle in the host and gravid contexts, the task decomposes into two two-world branch tasks:

- host branch: one A query, `C_A=C_F`;
- oviposition branch: one B query, `C_A=C_F`.

Both gaps are exactly zero regardless of positive terminal-query costs.

Therefore the positive integrated Aedes gap is biologically meaningful only if `R` is processed within a shared sensing/decision architecture whose state-dependent routing is itself part of the mechanism being tested.  The executable control is implemented in `adaptive_gain/aedes_context_semantics.py`.

## Claim state after this audit

Allowed now:

- Aedes provides a well-motivated prospective positive-gap task;
- NPF/RYamide is a strong candidate gonotrophic-state signal;
- gonotrophic state reprograms peripheral chemosensory physiology/transcription;
- IR8a and Ir68a provide causal terminal-channel handles.

Not allowed now:

- NPF/RYamide is proven to route IR8a versus Ir68a information use;
- published Aedes data already demonstrate empirical `g>0`;
- gonotrophic state may be inserted as a cost-free context while retaining the same adaptive-vs-fixed comparison;
- receptor knockouts define a natural mutation graph or population occupancy model.

## Next admission gate

Do not broaden candidate-system search before testing or locating direct evidence for the state-to-terminal routing edge.  The Aedes system is now sufficiently specified that the next information gain comes from this causal bridge, not from adding more candidate receptors or more species.
