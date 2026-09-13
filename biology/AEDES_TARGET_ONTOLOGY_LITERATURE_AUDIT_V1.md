# Aedes target-ontology literature audit v1

## Question

The positive-gap four-world prospectus treats the host-seeking and oviposition branches as different target programs:

- H0: continue host search;
- H1: approach / accept host;
- O0: continue oviposition-site search;
- O1: accept site / oviposit.

This note asks whether that four-action ontology has independent biological support, rather than being a post-hoc relabeling chosen because it yields `g>0`.

## Evidence for distinct gonotrophic behavioral programs

### Longitudinal post-biting reprogramming

Recent longitudinal work on female *Aedes aegypti* reports a sequence in which:

1. non-blood-fed females show strong host-seeking drive and responsiveness to human-associated cues;
2. blood feeding is followed by days of suppressed locomotion and host-cue responsiveness while eggs mature;
3. by approximately the third day after feeding, gravid females enter a hyperactive state associated with active search for egg-laying sites;
4. this gravid program includes a shift in circadian timing, nocturnal humidity seeking and egg laying;
5. disruption of the circadian clock gene `cycle` disrupts the timing of oviposition-related behavior and reduces reproductive performance when active site search is required;
6. the behavioral state reverses after successful oviposition.

This is strong evidence that gravid oviposition search is a distinct behavioral program rather than generic approach behavior renamed by physiological state.

### Host-cue to oviposition-cue responsiveness switch

Recent work on the NPYLR7 system summarizes the gonotrophic transition as a behavioral shift in responsiveness from host-associated to oviposition-associated chemosensory cues: females suppress attraction to humans and begin seeking standing water for egg laying.

Older experimental and review literature independently describes host seeking and pre-oviposition as two essential reproductive behavioral sequences. Host seeking is inhibited after a replete blood meal while egg development proceeds, and pre-oviposition behavior predominates when mature females receive oviposition-site stimuli.

### Sensory and motor distinctions

The two branches also differ at the level of sensory ecology and action:

- host seeking uses human CO2, odor, heat and other host-associated signals to locate and blood-feed from a vertebrate;
- gravid site search uses humidity, aquatic/oviposition odors, visual and contact cues to locate and evaluate egg-laying substrate;
- egg laying is a different terminal motor output from host approach/blood feeding;
- gravid search has distinct locomotor and circadian organization from non-blood-fed host-seeking behavior.

These differences support treating the branches as different decision programs when the target ontology is frozen prospectively.

## Qualification status

The literature raises the four-target ontology from a purely hypothetical encoding to **biologically supported / prospectively testable**.

It does not by itself freeze the exact target labels for an adaptive-gain experiment. The experiment must still define quantitative scoring rules before opening the cue matrix.

Recommended operational targets are:

- `continue_host_search`: absence of terminal host acceptance while retaining the pre-blood host-search state;
- `approach_host`: predeclared host-oriented approach / landing / blood-feeding endpoint;
- `continue_oviposition_search`: gravid search/humidity-seeking without site acceptance or egg deposition;
- `accept_oviposition_site`: predeclared site-acceptance / egg-laying endpoint.

The exact assay may choose different labels, but their biological distinction must be declared independently of the solver result.

## Falsification remains active

If a prospective experiment cannot reliably distinguish H0 from O0 as different behavioral programs, the task must be coarsened. The executable coarsened control then applies; under unit costs it has `g=0`.

Thus literature support makes the four-target design plausible but does not override the empirical target-validation gate.

## Literature anchors

- *Post-biting behavioral reprogramming underlies reproductive efficiency in Aedes aegypti mosquitoes*. Cell Reports (2025), PMID 41379618. Reports the transition from post-blood-meal inactivity to gravid hyperactivity, humidity seeking, active oviposition-site search and egg laying, with `cycle` required for correct timing.
- Frank K. et al. 2026. *A signaling hub in the mosquito rectum coordinates reproductive investment after blood feeding*. Current Biology. DOI 10.1016/j.cub.2026.02.042. Describes the switch from attraction to humans toward oviposition-related chemosensory cues during the gonotrophic cycle.
- Klowden M.J. 1990. *The endogenous regulation of mosquito reproductive behavior*. Experientia 46:660-670. DOI 10.1007/BF01939928. Distinguishes host-seeking and pre-oviposition as two essential reproductive behavioral sequences.

## Verdict

The four-action target partition is no longer the weakest part of the Aedes prospectus. It has independent natural-history and experimental support.

The remaining central empirical bottlenecks are instead:

1. operationalizing the gonotrophic-state information source and its acquisition cost;
2. measuring both terminal sensory channels across both gonotrophic branches;
3. preserving prospective off-branch baselines;
4. qualifying genetic perturbations without pretending broad endocrine/co-receptor changes are branch-local mutations.