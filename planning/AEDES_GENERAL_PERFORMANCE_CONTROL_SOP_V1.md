# Aedes Phase 1 general-performance control SOP v1

## Purpose

Provide a host-cue-independent control for gross locomotor impairment in the locked NPYLR7 agonist experiment.

A reduction in Miniport attraction cannot be interpreted as selective host-seeking suppression if the same treatment broadly prevents normal movement or flight.

This SOP is execution readiness only and does not alter the frozen Phase 1 scientific claim or GO/UNRESOLVED/STOP rules.

## Rationale

The published NPYLR7 work already provides important non-behavioral specificity controls:

- active compounds did not reduce meal acceptance / meal size under the screening formulation;
- lethality was explicitly detected and used to exclude a toxic compound in the original screen;
- NPYLR7-null mosquitoes were resistant to behaviorally active agonists in the source system, strongly supporting receptor specificity.

For transfer into an LVP background, receptor-null specificity is not yet available. Therefore add a simple host-cue-independent locomotor assay so that gross motor suppression cannot masquerade as selective loss of host seeking.

Published Aedes video-tracking systems show that spontaneous locomotor activity can be measured reproducibly from infrared/video recordings in the absence of host cues.

## Locked control concept

Run a neutral-arena locomotor test at the same post-meal time used for the Miniport assay.

Treatment groups:

1. saline vehicle;
2. TDI-014188;
3. TDI-014186.

No CO2, human odor, heat target, oviposition cue or blood source is present during the locomotor control.

## Minimal arena

Use a visually uniform, escape-proof observation arena compatible with video recording.

Requirements:

- constant geometry across treatments;
- no host-associated odor source;
- no deliberate humidity or heat gradient;
- stable temperature, humidity and light;
- camera position and gain fixed before confirmatory recording;
- acclimation interval frozen before treatment identities are opened.

An infrared/video-tracking implementation is preferred. FlyBox or an equivalent local video arena is acceptable if it is qualified prospectively.

## Observation unit

Prefer individual females for the general-performance assay, or otherwise use a design that preserves individual tracks without identity mixing.

Primary locomotor metrics should be frozen before confirmatory data:

- distance travelled per unit time;
- fraction of recording time active;
- optionally mean velocity while active.

Do not select whichever metric gives the most favorable treatment result after unblinding.

## Timing

Test at the same biological post-meal interval as Phase 1 Miniport testing, nominally 48 h after saline / compound meal once the source formulation is verified.

Run treatment groups in balanced temporal blocks to avoid confounding with Aedes circadian activity.

## Interpretation gate

The purpose is not to prove zero locomotor effect to arbitrary precision. It is to identify gross general impairment large enough to invalidate a selective host-seeking interpretation.

Before confirmatory work, freeze a practical impairment margin for each primary locomotor metric using vehicle-only baseline variability and biological judgment, not active-treatment pilot effects.

Classify:

- `PASS`: both agonist groups remain within the frozen acceptable general-performance range while Miniport host seeking is evaluated separately;
- `UNRESOLVED`: activity shifts are near the impairment margin, inconsistent across blocks, or video quality is insufficient;
- `FAIL`: treatment produces clear general locomotor impairment beyond the frozen margin.

A `FAIL` prevents Phase 1 `GO`, even if Miniport host seeking is strongly reduced.

## Additional mandatory observations

Record:

- mortality before and after locomotor testing;
- obvious inability to stand/fly;
- malformed or damaged individuals;
- feeding / meal-size receipt from the treatment cohort or matched batch.

Do not retrospectively exclude low-activity animals because they weaken the desired host-seeking result unless the exclusion rule was frozen prospectively.

## Apparatus qualification

Before drug comparison:

1. validate stable tracking of untreated / vehicle LVP females;
2. confirm no persistent spatial blind spot or camera artifact;
3. establish expected within-day / between-block variability;
4. choose and freeze recording duration;
5. freeze circadian test window;
6. freeze impairment margins using only control / qualification data.

## Relationship to NPYLR7 specificity

Passing this assay only excludes gross general performance impairment. It does not prove NPYLR7 receptor specificity in LVP.

Strong mechanistic promotion still benefits from a receptor-specificity test in the common background if such a line becomes available. Until then, the two independent locked agonists plus intake, mortality and locomotor controls constitute a staged pharmacological qualification, not a same-background genetic receptor proof.

## Source anchors

- Duvall et al. 2019, Cell, DOI 10.1016/j.cell.2018.12.004 — meal-size, lethality screening and NPYLR7-mutant resistance controls for active agonists.
- Video-based Aedes locomotor monitoring / FlyBox literature — host-cue-independent spontaneous activity can be quantified from repeated video frames and distance travelled.
