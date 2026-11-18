# Routeability procedural pilot v1

Status: prospective nuisance-parameter pilot. This pilot is intentionally separated from the confirmatory architecture × access test and does not modify the frozen Evolution Letters V5 submission surface.

## Purpose

The direct routeability experiment is now structurally specified, randomized, and analysis-gated. The remaining quantities needed before freezing the definitive biological sample size are procedural nuisance parameters rather than the focal routeability effect.

The pilot therefore estimates only:

- a defensible response-window duration;
- baseline non-response / timeout frequency;
- baseline perceptual / response error under full information;
- within-individual repeatability / overdispersion relevant to repeated trials;
- colony-to-colony heterogeneity where multiple colonies are available;
- procedural dropout and apparatus-failure rates;
- learning / fatigue over repeated calibration trials.

It must **not** estimate the confirmatory architecture × access interaction for power planning.

## Two-stage pilot

### Pilot A — architecture-neutral apparatus calibration

Use a simple calibration discrimination that does not instantiate either the routeable or bypass architecture.

Goals:

1. establish that the animal initiates the apparatus reliably;
2. measure latency from the final visible cue to a terminal accept/reject response;
3. quantify timeout / abandonment under an easy full-information task;
4. detect side biases, cue-window approach biases, or handling artifacts;
5. choose the response-window duration before confirmatory treatment assignment.

The calibration cues should be physically comparable to the planned experiment but use an independent cue alphabet.

### Response-window freeze

Do not choose the response window to maximize treatment accuracy.

Freeze it from Pilot A using the following deterministic rule:

> response window = the smallest prespecified candidate window that contains at least 95% of terminal decisions among successfully engaged calibration trials, subject to a fixed upper safety/handling bound declared before the pilot.

The candidate-window grid and the upper bound must be written into the pilot run sheet before collecting Pilot A.

If no candidate reaches 95%, enlarge or redesign the apparatus and rerun the procedural pilot. Do not carry an unstable response window into the confirmatory experiment.

## Pilot B — pooled B=3 full-information calibration

After apparatus calibration, use the actual physical cue channels under full information only.

All three cues are visible. There is no contingent-versus-fixed restriction at B=3.

Routeable and bypass state tables may both be represented so that nuisance estimates cover the intended physical stimuli, but the pilot extraction is **pooled across architecture**.

Allowed nuisance summaries:

- pooled correct-response probability within the frozen response window;
- pooled timeout probability;
- individual-level response variance / repeatability;
- colony-level variation;
- block-wise learning or fatigue slope;
- apparatus-error rate.

Forbidden before definitive sample-size freeze:

- architecture-specific accuracy;
- routeable-minus-bypass contrast;
- any architecture × access contrast;
- any B=2 data;
- any estimate of H1 or H2;
- choosing exclusions, response windows, or trial counts because one architecture looks better.

Architecture labels should be masked in the nuisance-summary output wherever practical.

## Pilot sample size

The pilot itself is not powered for the focal routeability hypothesis.

Pilot size should be chosen for stable nuisance estimation and operational feasibility, with multiple individuals and preferably multiple colonies. The exact pilot N remains a husbandry/logistics quantity until the available animal/colony surface is known.

Do not report pilot trial count as if it were the biological sample size.

## Nuisance receipt

The pilot should produce one machine-readable receipt containing:

- response-window candidate grid and selected window;
- number of individuals and colonies;
- initiated calibration trials;
- valid terminal decisions;
- timeouts;
- pooled full-information correctness;
- within-individual repeated-trial variance or ICC-compatible summary;
- colony-level variance estimate or a conservative bound when estimable;
- dropout / exclusion counts with reasons;
- block-wise latency and success summaries;
- a statement that no focal architecture × access effect was opened.

## Definitive sample-size step

After the nuisance receipt is frozen, generate a **design operating-characteristic surface** rather than selecting N from a favorable pilot treatment effect.

The sample-size analysis should vary:

- individuals per randomized cell;
- trials per individual;
- plausible baseline correctness;
- timeout probability;
- individual heterogeneity;
- colony heterogeneity;
- a grid of scientifically relevant architecture × access effects.

The theoretical 0.25 information ceiling is not the assumed behavioral effect size.

The focal treatment effect from a pilot, if accidentally visible, is not used as the power target.

Prefer reporting power / precision curves over a range of effect sizes. Final N can then be frozen from a predeclared precision or minimally relevant-effect criterion without using the confirmatory data.

## Promotion gate

The confirmatory experiment is ready to freeze its final response window and sample-size plan only when:

1. Pilot A yields a stable response window;
2. Pilot B shows that full-information performance is operationally measurable without catastrophic non-response;
3. nuisance summaries can be estimated without opening H1/H2;
4. the schedule remains feasible under the available colony/individual supply;
5. a sample-size operating-characteristic analysis is frozen before confirmatory allocation.

## Failure modes

Redesign the apparatus before confirmatory testing if:

- Pilot A cannot produce a stable response window;
- side / window bias is large despite counterbalancing;
- B=3 full-information performance is near chance or dominated by timeouts;
- apparatus errors are common;
- training cannot be delivered at a fixed dose without severe differential non-response.

These are procedural failures, not evidence against routeability.

## Claim boundary

A successful pilot establishes only that the direct experiment is operationally measurable and that nuisance parameters can be frozen without using the focal routeability contrast.

It is not an empirical test of environmental routeability.
