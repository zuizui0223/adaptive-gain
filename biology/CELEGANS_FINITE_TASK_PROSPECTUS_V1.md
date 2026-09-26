# C. elegans finite-task prospectus v1

## Purpose

The qualification screen identifies C. elegans AWA state-dependent chemosensation as a plausible genotype-policy bridge. This note asks the stricter question required by adaptive-gain:

> Can the existing biology already instantiate a finite sensing task with a verified adaptive/fixed gap `g=C_F-C_A>0`?

Current answer: **not yet**.

## Minimal q=1 architecture we would like to test

The simplest exact adaptive-gain witness has four represented alternatives and three binary cues:

- coarse context cue `R`;
- branch-A terminal cue `A`;
- branch-B terminal cue `B`.

The desired outcome pattern is

| World | R | A | B | target |
|---|---:|---:|---:|---|
| w1 | 0 | 0 | * | A0 |
| w2 | 0 | 1 | * | A1 |
| w3 | 1 | * | 0 | B0 |
| w4 | 1 | * | 1 | B1 |

where `*` means that the terminal cue is irrelevant/non-discriminating for the declared target in the other branch.

Then an adaptive policy asks `R` and only the relevant terminal cue, so `C_A=2`; every fixed cue set must contain `R,A,B`, so `C_F=3`; hence `g=1`.

## Tempting biological mapping

A first-pass mapping is:

- `R`: feeding / food-sensory context;
- `A`: ODR-10 / diacetyl channel;
- `B`: STR-44 / butyl- or propyl-acetate channel.

This is attractive because both receptors are in the AWA sensory system and both have direct sensory/behavioral evidence.

## Why the mapping is not yet licensed

### 1. STR-44 is not an exclusive terminal channel

Fasting strongly upregulates `str-44` and potentiates AWA responses to butyl and propyl acetate, but fed animals can still detect these odors when STR-44 expression is low. Published work explicitly notes that multiple chemoreceptors likely contribute. Therefore the off-branch outcome cannot currently be coded as `*` or constant without additional perturbation evidence.

### 2. ODR-10 state dependence is sex/development dependent

`odr-10` is a clean diacetyl receptor-to-behavior link, but its state regulation is not a universal binary fed/fasted switch. In adult males, food deprivation strongly induces `odr-10`; in hermaphrodites and other developmental states the baseline differs. A prospective task must therefore fix sex, stage and history before defining worlds.

### 3. A regulatory state signal is not automatically a unit-cost cue

Food history can regulate receptor expression through distributed sensory, endocrine and circuit pathways. The adaptive-gain theorem counts declared cue acquisitions. Treating an internal regulatory state as one unit-cost query requires an explicit biological measurement convention; it cannot be assumed from pathway diagrams.

### 4. Receptor abundance is not query cost

A receptor being expressed or absent does not itself tell us `C_A` or `C_F`. Those quantities are properties of the declared finite discrimination task and cue outcome table. Expression data may help define availability, but costs must be stated prospectively.

### 5. Behavioral target partition must be predeclared

The four worlds must map to predeclared actions/targets. It is not enough to observe four response patterns and then choose a partition that produces a gap.

## Prospective experiment that would close the gap

### Stage A — freeze the task before genotype manipulation

1. Fix one sex and developmental stage.
2. Choose exactly four ecological/odor alternatives.
3. Declare one coarse context measurement and two candidate terminal receptor channels.
4. Declare the target action for each world.
5. Freeze the cue cost convention before inspecting `C_A-C_F`.

### Stage B — establish the cue outcome matrix

For every world, independently measure:

- coarse-context signal;
- receptor/channel-A response;
- receptor/channel-B response;
- target behavior.

Use endogenous reporters and calcium/behavioral assays where possible.

The task is admitted only if the empirical matrix has the required separation structure without post-hoc recoding.

### Stage C — establish branch specificity

Use receptor knockout / endogenous regulatory perturbation to show that:

- channel A is necessary/sufficient for the declared within-branch-A distinction under the chosen conditions;
- channel B is necessary/sufficient for the declared within-branch-B distinction;
- each terminal perturbation is non-disruptive to the other branch except where explicitly encoded as a coupled mutation.

For STR-44, the known redundant detection of butyl/propyl acetate is presently the main hard stop. Either remove/identify the alternative receptor contribution prospectively or choose a cleaner terminal receptor-ligand channel.

### Stage D — compute C_A and C_F from the frozen matrix

Only after the biological matrix is frozen should the repository's exact finite-task solver calculate adaptive and fixed minima. Admission requires `g>0` prospectively; a failed or zero-gap task is a valid negative result and should not be redesigned post hoc.

### Stage E — genotype-policy perturbation

After a real positive gap is established, introduce a small endogenous regulatory edit and repeat the full matrix across all worlds. The edit is allowed to define one local mutation edge only if its cross-context effects are measured and compatible with that edge.

## Strongest near-term design

The most defensible first experiment is **not** to claim that the published ODR-10/STR-44 system already has `g=1`.

Instead:

1. use the existing literature to define the prospective context and receptor candidates;
2. identify or engineer two terminal channels whose off-branch outcomes are experimentally constant under the frozen task;
3. pre-register the four-world target partition;
4. open the outcome matrix once;
5. compute `C_A` and `C_F` without redesign.

This turns the current literature from retrospective analogy into a genuine qualification experiment.

## Current verdict

C. elegans remains the best candidate found so far for the biological genotype-policy bridge, but **no published evidence located in this screen yet licenses a nonzero empirical adaptive-gain value**.

The immediate research question is now sharp:

> Can one predeclared four-world AWA chemosensory task produce a prospective `C_A=2, C_F=3` witness while surviving receptor redundancy and cross-context perturbation tests?

Until the answer is yes, do not connect C. elegans to the downstream mutation/population stack.