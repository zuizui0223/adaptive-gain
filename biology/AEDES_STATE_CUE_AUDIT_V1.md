# Aedes gonotrophic-state cue audit v1

## Question

The prospective four-world task requires a coarse state information source `R` that routes the decision toward a host-related terminal cue `A` or an oviposition-site terminal cue `B`.

What biological signal could instantiate `R`?

## Important distinction

`R` should not be equated automatically with:

- experimenter-assigned days after blood feeding;
- the label `gravid`;
- NPYLR7 receptor genotype;
- abdominal distension alone.

Those may define/manipulate physiological state, but the adaptive-gain task needs an organism-level information source that could in principle be read by the decision architecture.

## Current strongest candidate: NPF / RYamide endocrine state

Recent work gives a coherent gonotrophic endocrine contrast.

### Previtellogenic state

Posterior-midgut enteroendocrine cells produce neuropeptide F (`NPF`). Circulating NPF is associated with the previtellogenic phase and promotes attraction to human hosts / biting-related behavior.

### Post-protein / post-blood state

Protein digestion after a blood meal reduces NPF production/titer while RYamide secretion increases. RYamide-producing neurons innervate the gut/rectal region and circulating RYamide rises after a protein meal.

Exogenous RYamide suppresses host attraction in previtellogenic females, providing causal evidence that the endocrine signal can change behavioral priority rather than merely correlate with egg development.

### NPYLR7 link

NPYLR7 is required for normal sustained host-seeking suppression after blood feeding. Pharmacological agonists suppress human attraction and biting, and CRISPR null mutants fail to maintain normal long-term suppression.

More recent work identifies NPYLR7-expressing rectal-pad cells that respond to RYamide and amino acids and communicate with the nervous system / reproductive physiology. This provides a plausible peripheral nutrient-state sensing hub, although NPYLR7 is pleiotropic and is not a clean single routing switch.

## Candidate operational definition of R

A prospective experiment could define a two-state endocrine readout such as

- `R=0`: preregistered previtellogenic endocrine range — high NPF / low post-meal RYamide signature;
- `R=1`: preregistered post-blood/gravid endocrine range — reduced NPF / elevated RYamide signature.

The exact biomarker threshold must be frozen before the full A/B outcome matrix is opened.

This is stronger than using `hours post blood meal` alone because it ties the state label to an organismal signaling channel.

## What is still missing

### 1. R-to-routing causality

Existing evidence strongly links NPF/RYamide/NPYLR7 signaling to host-attraction suppression. It does not yet show that this same endocrine state causally switches sensory allocation from `A` to `B`.

The decisive prospective test should therefore manipulate the R pathway and measure both terminal channels in the same animal/state design:

- host-associated acidic-cue response (`A`);
- oviposition-site cue response (`B`, primary candidate Ir68a-dependent humidity);
- host-search target behavior;
- oviposition-site-search target behavior.

A valid routing result would require the R perturbation to change the relative use/value of the terminal channels in the predeclared direction, not merely suppress locomotion or one terminal behavior.

### 2. Acquisition-cost semantics

Hormonal state may be continuously available rather than actively sampled. Therefore no claim should be made that its physiological cost equals one terminal sensory acquisition.

The four-target mathematical witness does not require equal costs: for positive `(r,a,b)`, `g=min(a,b)>0`. But the current exact framework still assumes positive acquisition costs. A biological realization must either:

- define a positive organism-level readout/resource cost for `R`; or
- explicitly report that a cost-free/pre-known context would be a different model contract and is outside the present flagship theorem's positive-cost task class.

Do not silently treat a continuously available internal state as a unit-cost query.

### 3. Pleiotropy

NPF/RYamide/NPYLR7 signaling affects feeding/reproductive physiology as well as host attraction. Any genetic or pharmacological perturbation may therefore change motivation, egg maturation or general physiology in addition to information routing.

Cross-branch controls are mandatory.

## Proposed R qualification experiment

Before measuring adaptive gain:

1. define the endocrine R assay and thresholds;
2. manipulate NPF/RYamide/NPYLR7 signaling prospectively;
3. measure A and B sensory responses under both R states;
4. measure the four target programs;
5. assay locomotion, egg maturation and general reproductive state as pleiotropy controls;
6. only then decide whether R qualifies as a causal routing information source.

If endocrine manipulation changes host motivation but not terminal sensory allocation, classify the result as **state-dependent action gating**, not as demonstrated adaptive cue routing.

## Literature anchors

- Duvall L.B. et al. 2019. *Small-Molecule Agonists of Ae. aegypti Neuropeptide Y Receptor Block Mosquito Biting*. Cell 176:687-701.e5. NPYLR7 agonism suppresses human attraction and biting; NPYLR7 null mutants fail to maintain normal post-blood-meal suppression.
- *Reciprocal interactions between neuropeptide F and RYamide regulate host attraction in the mosquito Aedes aegypti*. 2024. NPF promotes host attraction in the previtellogenic state; protein feeding lowers NPF and increases RYamide secretion; RYamide suppresses host attraction.
- Frank K. et al. 2026. *A signaling hub in the mosquito rectum coordinates reproductive investment after blood feeding*. Current Biology. NPYLR7-expressing rectal cells respond to RYamide/amino acids and participate in post-blood-meal nutrient/reproductive signaling.

## Verdict

Promote the NPF/RYamide endocrine axis to the primary biological candidate for `R`, while retaining `R` as **not yet qualified** for adaptive cue routing.

The central missing link is now explicit:

`endocrine gonotrophic state -> differential terminal information use (A versus B)`.

That is a prospective experiment, not an inference to extract from existing behavioral literature.