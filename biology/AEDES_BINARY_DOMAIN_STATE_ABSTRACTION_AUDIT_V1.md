# Aedes binary-domain and state-abstraction audit v1

## Main correction

The prospective four-world q=1 Aedes task must **not** be described as a complete model of the gonotrophic cycle.

The natural cycle contains more than two behaviorally relevant phases.  At minimum the literature distinguishes:

1. a previtellogenic host-seeking phase;
2. an early/intermediate post-blood host-seeking refractory phase during egg development;
3. a mature-gravid oviposition-site-search phase with strong circadian timing;
4. return to host seeking after oviposition.

Host suppression begins well before the mature-gravid humidity-seeking program.  Therefore one binary molecular switch cannot be assumed to generate the whole H-to-O transition.

## Admissible domain for the q=1 task

The current four-world task is prospectively restricted to two endpoint windows only:

### H endpoint

A preregistered previtellogenic window in which females are competent for host seeking.

### O endpoint

A preregistered mature-gravid window, at a circadian time when oviposition-site/humidity seeking is behaviorally expressed.

Intermediate post-blood times and post-oviposition recovery are **outside the task domain**.  They may be measured as mechanistic controls but must not be silently folded into the binary R outcome.

Any manuscript or receipt using this task must say explicitly that it is an endpoint-restricted finite decision problem, not a full-cycle state model.

## R is currently an abstraction, not one established molecule

NPF/RYamide signaling is the strongest current mechanistic handle for the host-attraction side of R:

- NPF promotes host attraction in the previtellogenic state;
- blood/protein feeding lowers NPF;
- circulating RYamide rises after feeding and suppresses host attraction;
- NPYLR7 agonists can suppress host seeking even without a nutritive blood meal.

However, mature-gravid B behavior has additional gates:

- humidity seeking appears only after egg maturation rather than immediately after host seeking is suppressed;
- humidity/site seeking is strongly circadian;
- `cycle` mutants disrupt the timing of gravid humidity-seeking behavior.

Thus the current biological R is best regarded as a **candidate composite internal decision-state readout** whose mechanistic components are unresolved.  It must not be equated with NPF, RYamide, NPYLR7, egg maturity or circadian phase individually without a causal test.

## Strong falsification experiment for single-signal R

NPYLR7 agonists provide a useful dissociation because they suppress host-seeking in non-nutritive conditions.

In previtellogenic females, apply a selective NPYLR7 agonist and ask:

1. does A-dependent host information use fall as expected?
2. does B-dependent humidity/site-seeking information use emerge?

Possible outcomes:

### A down, B up

Supports sufficiency of the manipulated state pathway for a broader branch switch and strengthens the case for a low-dimensional R.

### A down, B unchanged

Shows that the pathway controls host suppression but is not sufficient for the H-to-O information-routing switch.  NPF/RYamide/NPYLR7 cannot by itself instantiate R.

### neither changes at the sensory-dependency level

Supports a downstream motivational/motor effect rather than the proposed sensing-route mechanism.

The experiment must also monitor reproductive state and locomotion because NPYLR7 has reproductive physiological functions.

## Two allowed futures

If no single common state signal coordinates both terminal channels, there are only two defensible options.

### Option 1 — retain R as a composite biological state readout

This requires prospective evidence that the organism integrates the relevant endocrine/reproductive/circadian information before selecting terminal sensory resources.  The comparator semantics must still be shared-architecture rather than externally pre-indexed.

### Option 2 — expand the finite task

Declare separate internal state queries (for example nutritional/reproductive and circadian/egg-maturity components) **before** opening the decisive data, then recompute exact `C_A` and `C_F` from the expanded task.

Do not add extra state queries post hoc merely to preserve positive gain.

## Relation to the context-preindexing control

Endpoint restriction does not solve the comparator problem.  Even if H and O windows are cleanly defined, positive integrated adaptive gain disappears if the organism's state is effectively available before policy commitment and fixed strategies are allowed to be separately indexed by that state.

Therefore two independent gates remain:

1. **domain gate:** are the H and O endpoint windows prospectively defined and biologically coherent?
2. **comparator gate:** is state information processed within one shared architecture rather than used to pre-index separate fixed policies?

Both must pass before interpreting the integrated q=1 fixture as empirical adaptive gain.

## Literature anchors

- Dou et al. 2024, PNAS, DOI 10.1073/pnas.2408072121 — NPF/RYamide reciprocal regulation of host attraction.
- Duvall et al. 2019, Cell, DOI 10.1016/j.cell.2018.12.004 — NPYLR7 agonists and mutants establish a manipulable host-seeking suppression pathway.
- post-biting behavioral reprogramming study, PMID 41379618 — mature-gravid nocturnal humidity seeking and `cycle` dependence.
- Tang et al. 2024, PNAS, DOI 10.1073/pnas.2407394121 — Ir68a-dependent Moist Cells required for water-container seeking by gravid females.

## Current claim boundary

The Aedes system remains the strongest prospective positive-gap candidate in this repository, but the state variable R is now explicitly classified as **mechanistically unresolved/composite** until the state-to-terminal causal experiment closes or rejects the common-routing hypothesis.
