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

[
C_A=2,qquad C_F=3.
]

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

[
C_A=C_F=2.
]

The same context-contingent two-cue schedule can resolve this task, but it is not uniquely valuable because the fixed terminal pair ({	ext{A},	ext{B}}) also resolves every target.

Therefore the control matches cue number, state number, target balance and cue marginals while removing the strict adaptive gain.

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

Observation 1 and 2 are always terminal A and terminal B, independent of state.

The order of A and B should be counterbalanced, but the same pair is provisioned on every trial.

## Exact information prediction at budget 2

Under a uniform distribution of the four states and optimal classification after the two observed cues:

| architecture | contingent access | fixed terminal access |
| --- | ---: | ---: |
| routeable | 1.00 | 0.75 |
| bypass control | 1.00 | 1.00 |

Thus the exact information-level interaction is:

[
(1.00-0.75)-(1.00-1.00)=0.25.
]

This **25 percentage-point value is an information ceiling contrast**, not a required behavioral effect size. Real animals can make perceptual, learning and motivational errors.

The empirical prediction is only that the contingent-versus-fixed advantage is larger in the routeable architecture than in the bypass control.

## Budget ladder

The main experiment should include or preregister a budget manipulation.

### B = 1 — below adaptive cost

One cue observation is insufficient to guarantee the target in either architecture.

Prediction: no condition has exact guaranteed resolution.

### B = 2 — routeability-sensitive window

For the routeable task:

[
C_Ale B<C_F
quadLongleftrightarrowquad
2le2<3.
]

Prediction: contingent access has an information advantage over fixed access.

For the bypass control, (C_A=C_F=2), so contingent access has no exact advantage.

### B = 3 — above fixed cost

All three cues are available.

Prediction: both access classes can resolve the routeable target and the unique routeability advantage disappears.

This budget ladder is the strongest experimental connection to V5 because it tests the predicted **window**, not merely whether animals can learn a contextual rule.

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

- **context:** a coarse outer collar / patch cue visible before the terminal information;
- **terminal A:** one local cue window;
- **terminal B:** a second local cue window.

The two terminal cue channels should be physically and temporally matched.

Do not literally confound A and B with permanent left/right position. Randomize or rotate physical positions so cue identity is not a side cue.

### Information presentation

A clean implementation uses shutters, cards or other non-flickering displays so that exactly the permitted cue channels are visible on each trial.

For the primary B=2 contrast:

- contingent treatment shows context, then the context-selected terminal cue;
- fixed treatment shows terminal A and terminal B;
- total cue-exposure count and nominal exposure duration are matched.

The response is recorded only after the allowed cue observations have been presented.

## Primary endpoint

**Correct accept/reject response** under the frozen two-cue budget.

The primary model tests the interaction:

[
	ext{task architecture}	imes	ext{information access}.
]

The directional hypothesis is:

> the contingent-minus-fixed accuracy contrast is positive in the routeable task and larger than the corresponding contrast in the bypass control.

Do not require the observed interaction to equal 0.25.

## Secondary endpoints

Allowed secondary outcomes:

- decision latency after the final allowed cue;
- first inspection / approach error;
- number of revisits when revisits are possible;
- abandonment probability;
- learning slope across trials.

Secondary outcomes cannot replace the primary accuracy interaction after outcomes are inspected.

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

Training must not reveal the focal comparison by giving one architecture systematically more experience.

Preferred structure:

1. familiarization with apparatus and response port;
2. balanced training on state-response associations using full information;
3. criterion check defined before the main test;
4. main test with the frozen information-access manipulation;
5. optional B=3 positive-control block.

If the same animal receives multiple architecture or access conditions, use independent cue alphabets and counterbalanced order. A between-subject primary design is cleaner if enough colonies / individuals are available.

## Randomization

Freeze before data collection:

- state frequency: uniform 1/4 per state in the primary test;
- trial order: randomized within prespecified blocks;
- cue-symbol mapping;
- physical location of cue windows;
- architecture assignment;
- access-mode assignment;
- colony balancing where applicable.

## Exclusion rules

Define before data collection.

Examples:

- failure to meet a prespecified training criterion;
- failure to initiate a minimum number of test trials;
- apparatus malfunction or cue presentation error;
- loss of individual identity.

Do not exclude an individual because its test accuracy is low.

## Manipulation checks

Required:

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

### Confirmatory H2 — budget-window interaction

When B=1,2,3 are implemented, test whether the architecture × access difference is concentrated at B=2 rather than being a monotonic treatment difference across all budgets.

### Secondary — latency

Analyze only after H1 is frozen and reported.

A speed-accuracy trade-off must be considered; lower latency is not automatically better if accuracy declines.

## Independent-unit policy

The independent biological unit is the individual forager, with colony treated as a higher-level grouping factor where relevant.

Trials are repeated observations, not independent animals.

Do not report trial count as the biological sample size.

## Pilot and sample size

Do not power the definitive experiment from the theoretical 1.00 versus 0.75 information ceiling.

First run a procedural pilot to estimate:

- baseline perceptual error under B=3;
- within-animal correlation;
- learning / fatigue across trials;
- colony heterogeneity;
- dropout and non-response rates.

Freeze the final sample-size simulation from those nuisance parameters without using the focal architecture × access interaction estimate from the confirmatory test.

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
