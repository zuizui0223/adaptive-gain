# Aedes pre-data admission freeze v1

## Status

**SCIENTIFIC SURFACE FROZEN PENDING CI.**

This receipt freezes the prospective Aedes empirical-admission package before any decisive state-routing outcome matrix is opened.  It does not claim that empirical adaptive gain has been observed.

Source branch:

`biology/aedes-gonotrophic-finite-task`

Scientific freeze parent at the time this receipt was initiated:

`c2bb023f1cb6500ccb0cc5ae88a8fb98da5aafa7`

The current PR is #35.  CI completion is a separate technical gate.  After this receipt, changes to the scientific task, targets, comparator semantics, endpoint domain, primary terminal channels, or success criteria require an explicit new version rather than silent editing.

## 1. Frozen finite-task structure

The prospective integrated task has four represented endpoint worlds:

- `H0=(R,A,B)=(0,0,0)`;
- `H1=(0,1,0)`;
- `O0=(1,0,0)`;
- `O1=(1,0,1)`.

The four target programs are prospectively distinct:

- `H0`: continue host search;
- `H1`: approach host;
- `O0`: continue oviposition-site search;
- `O1`: accept oviposition site.

The structural query roles are:

- `R`: internal gonotrophic-state information used within a shared decision architecture;
- `A`: acidic host-cue information, with IR8a as the primary causal handle;
- `B`: oviposition-site information, with Ir68a-dependent humidity/water-vapor sensing as the primary causal handle.

The exact solver verifies for positive integer costs `(r,a,b)`:

`C_A = r + max(a,b)`

`C_F = r + a + b`

`g = min(a,b) > 0`.

This is a mathematical property of the frozen prospective task, not an empirical result.

## 2. Frozen endpoint domain

The binary task is not a model of the full gonotrophic cycle.

Only two endpoint windows are admitted prospectively:

- `H`: a preregistered previtellogenic host-seeking window;
- `O`: a preregistered mature-gravid window at a circadian phase in which oviposition-site/humidity seeking is expressed.

Intermediate post-blood states and post-oviposition recovery are outside the finite-task domain.  They may be used as mechanistic controls but cannot be silently recoded into R after the data are seen.

## 3. Frozen interpretation of R

R is **mechanistically unresolved/composite**.

NPF/RYamide/NPYLR7 provide strong candidate components for host-seeking suppression, but mature-gravid B behavior also depends on egg maturity and circadian state.  No single peptide, receptor, egg-maturity marker or clock state is currently equated with R.

If future evidence shows that multiple internal information sources are required, an expanded task must be declared prospectively as a new version and its exact costs recomputed.  Extra state queries cannot be added post hoc to preserve positive gain.

## 4. Frozen comparator-semantics control

The integrated positive gap is admissible only if R is processed inside one shared sensing/decision architecture.

If gonotrophic context is externally known before policy commitment and fixed policies are allowed to be separately indexed by context, the problem decomposes into two branch tasks:

- host branch: `C_A=C_F=a`;
- oviposition branch: `C_A=C_F=b`.

Both gaps are exactly zero.

Therefore `comparator_semantics_qualified` is an independent admission gate.  A laboratory label such as “pre-blood” or “gravid” cannot by itself supply R while retaining the integrated comparator.

## 5. Frozen target-coarsening control

If the four target programs are collapsed to generic `accept` versus `reject`, then

`C_F = a+b`

`C_A = min(a+b, r+max(a,b))`

`g = max(0, min(a,b)-r)`.

At unit costs the coarsened gap is exactly zero.  Hence target ontology must be justified independently and prospectively; it cannot be refined after observing the desired structural gap.

## 6. Frozen causal question

The decisive missing biological edge is:

`R -> relative decision use/dependency of A versus B`.

Current literature supports the components separately:

- gonotrophic-state neuropeptide signaling causally changes host attraction;
- peripheral chemosensory physiology and transcription change with gonotrophic state;
- IR8a is a causal handle on acidic host cues;
- Ir68a-dependent Moist Cells are a causal handle on locating water-filled oviposition sites.

The literature does not yet show that manipulating the candidate state signal switches the relative decision dependence on the exact A and B channels.

## 7. Frozen causal experiment

The state-routing experiment is defined in `biology/AEDES_STATE_ROUTING_EXPERIMENT_V1.md`.

It must:

1. manipulate candidate state signaling independently of the full blood-meal package where possible, including a selective NPYLR7 agonist as a nutrient-independent host-suppression perturbation;
2. assay A and B at sensory and behavioral levels;
3. measure dependency on each terminal channel, not merely response amplitude;
4. distinguish strong causal routing from sensory reweighting and from a downstream motivational/motor switch;
5. control egg maturity, circadian phase, locomotion/arousal, nutritional state and terminal-channel integrity;
6. retain null and asymmetric results without redefining the finite task.

## 8. Frozen empirical claim ladder

The generic claim gate is implemented in `adaptive_gain/empirical_claim_gates.py`.

A mathematical positive gap does not license an empirical positive-gap claim.

Empirical task admission requires at least:

- task semantics;
- comparator semantics;
- measurement resolution;
- target ontology;
- cost semantics.

Causal routing additionally requires:

- terminal-channel causality;
- state-routing causality.

Downstream evolutionary claims remain separately gated:

- accessibility: admitted task + genotype-policy map + mutation support + start state;
- stationary occupancy: admitted task + genotype-policy map + support + relative mutation bias/neutral measure + population process;
- biological waiting time: accessibility + population process + absolute rate scale.

These gates implement the downstream nonidentifiability ceiling rather than assuming that q or g determines population dynamics.

## 9. Admissible terminal outcomes

The future data need not produce a positive result.

Allowed terminal receipts include:

- task rejected by measurement or semantic admission;
- zero structural gap;
- positive structural gap without causal routing;
- state-dependent sensory modulation without routing;
- downstream motivational/motor state change without terminal-channel reallocation;
- strong positive gap with causal state-dependent terminal-information use.

No failed outcome licenses redesign of worlds, targets, costs, comparator semantics or endpoint windows within v1.

## 10. Stop rule

Until the frozen state-to-terminal causal test is performed or direct existing evidence closes the same edge:

- do not add more candidate species;
- do not add more receptor candidates merely to preserve the architecture;
- do not extend the abstract mutation/population side theory;
- do not modify the frozen Theoretical Ecology flagship manuscript with this prospective biology;
- do not promote PR #35 from prospective qualification to empirical evidence.

## 11. CI gate

The scientific surface may be called **pre-data frozen** once the exact current branch head passes the repository's full CI matrix and audit scripts.  If CI exposes an implementation error, only the minimal technical repair needed to make the frozen semantics executable is allowed under v1.  Any scientific-semantic change requires v2.
