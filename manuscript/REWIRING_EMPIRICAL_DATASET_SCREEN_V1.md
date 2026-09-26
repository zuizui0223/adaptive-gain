# Rewiring empirical dataset screen v1

Status: post-freeze feasibility ledger for the decision-structural rewiring reserve. This file does **not** modify the frozen Evolution Letters V5 submission surface.

## Screening question

The prospective rewiring test requires repeated interaction networks **and** a way to define decision-equivalence structure independently of the observed rewiring response.

A dataset is confirmatory-ready only if it supports all of the following:

1. repeated networks with link-level or dyad-level information;
2. explicit separation of species turnover from rewiring among shared species;
3. partner availability / phenology / morphology or other compatibility filters;
4. decision-relevant cue or choice information measured independently of the rewiring outcome;
5. enough repeated transitions to compare boundary-crossing and within-class turnover.

The screen below intentionally distinguishes a good network dataset from a good decision-structure dataset. They are not the same thing.

## Admission tiers

- **Tier A — confirmatory-ready:** independent decision classes + repeated network response + opportunity controls.
- **Tier B — strong pilot:** repeated network response and strong conventional controls, but decision classes are only indirectly measurable.
- **Tier C — response-only / aggregate:** useful for benchmarking turnover, but insufficient for the prospective decision-structure test.
- **Reject:** the focal response or independent exposure cannot be reconstructed.

## Candidate 1 — Villavicencio six-year plant–pollinator network

**Source:** Chacoff, Vázquez & Lomáscolo Dryad dataset supporting Peralta et al. 2020, *Ecology Letters*.

- Dataset DOI: `10.5061/dryad.8cz8w9gm1`
- Study period: 2006–2011.
- Public asset: `plant_pollinator_data.xlsx`.
- Reported network subset: 45 plant species and 135 flower-visiting species with morphological data.
- Original interaction dataset: 59 plant species, 196 flower visitors, 28,015 visits and 1,050 interacting pairs.
- Public dataset includes yearly plant–pollinator matrices for six consecutive years, flower abundance, phenological overlap, plant traits, pollinator traits and pollination-success information.
- Plant traits include corolla length, corolla aperture and flower height.
- Insect traits include body dimensions and proboscis length/width.

### Screening decision

**Tier B — strongest current public pilot candidate.**

Why it is strong:

- repeated yearly networks;
- independently measured morphology;
- phenological overlap;
- abundance;
- a large set of shared species and links across years;
- conventional compatibility filters can be modelled explicitly rather than absorbed into the routeability term.

Why it is **not Tier A**:

- morphology and phenology describe compatibility and accessibility constraints, but they do not by themselves establish the cue hierarchy or contingent decision problem of a pollinator;
- defining decision-equivalence classes directly from the same network links would be circular;
- therefore a morphology-derived class system can only be an exploratory proxy unless it is externally justified by independent behavioral evidence.

### Allowed pilot use

Use the dataset to answer a narrower feasibility question:

> After controlling for abundance, phenology and morphology, is there enough repeated link turnover and shared-partner structure to support a later independently defined decision-class test?

Do **not** call a morphology clustering result an exact empirical decision-equivalence test.

## Candidate 2 — Catalan butterfly–plant long-term network

**Source:** Colom et al. 2026, *Ecology Letters*, “Three Decades of Butterfly–Plant Interaction Turnover Explained by Climate and Species Loss.”

- Article DOI: `10.1111/ele.70361`.
- Public processed-data / code archive: Zenodo `10.5281/zenodo.18668204`.
- Long-term butterfly–plant interaction monitoring.
- Published analysis partitions interaction turnover and rewiring, includes butterfly traits, abundance / phenological change and climate covariates.
- The paper reports that rewiring became more intense in years with stronger temperature fluctuations, while the relative importance of rewiring declined as species loss reduced the pool of shared partners.

### Screening decision

**Tier B-minus — high-value external validation candidate, not yet confirmatory-ready.**

Strengths:

- long temporal extent;
- an already established rewiring response;
- climate variation;
- trait and phenological covariates;
- direct relevance to the V5 low-turnover / environmental-change regime.

Limitations:

- the public archive is described as processed data plus annotated scripts; raw butterfly–plant interaction data are available from the authors on request;
- independent decision-relevant cue structure is not supplied as part of the published network analysis;
- therefore the current public surface does not yet support the frozen decision-equivalence exposure.

### Allowed use

Use only after verifying that the processed archive retains the link-level transition information needed for the shared-species contrast. If not, this candidate requires author-supplied raw data.

## Candidate 3 — RMBL weekly plant–pollinator turnover

**Source:** CaraDonna et al. 2017, *Ecology Letters*.

- Article DOI: `10.1111/ele.12740`.
- Dryad DOI: `10.5061/dryad.s91p4`.
- Weekly censuses over three years.
- Published result: interaction turnover was high and dominated by rewiring; phenology and relative abundance constrained turnover and rewiring.
- Public Dryad files are turnover summaries and simulation outputs.

### Screening decision

**Tier C for the present test.**

The temporal resolution is excellent, but the public Dryad surface is not the right unit for the prospective dyad-level decision-boundary test. It remains useful for benchmarking the expected magnitude and temporal structure of rewiring.

## Candidate 4 — six-year trait-matching study as conventional-filter reference

The Villavicencio dataset is also valuable even if it never supplies decision classes.

Its strongest role may be to freeze the **non-routeability** part of the model:

- phenological overlap;
- floral abundance;
- corolla length / aperture;
- insect proboscis dimensions;
- body size.

These are exactly the filters that the V5 claim says routeability does **not** replace.

That makes this dataset useful for testing whether a later decision-structure term adds information after strong conventional compatibility models are already present.

## Candidate 5 — habitat-loss seasonal rewiring network

**Source:** Lázaro & Gómez-Martínez, Dryad `10.5061/dryad.1ns1rn8x3`.

The public dataset supports seasonal plant–pollinator rewiring across a habitat-loss gradient.

### Screening decision

**Tier B-minus / reserve.**

It may supply repeated rewiring response and community context, but the current screen has not identified an independent decision-cue surface comparable to the Villavicencio morphology / phenology bundle.

Do not advance it ahead of Candidate 1 without a clear independent exposure.

## Current empirical conclusion

**No Tier A public dataset has yet been identified.**

That is a useful result, not a failure.

The current data landscape separates into:

- datasets with strong repeated network responses; and
- datasets with traits / compatibility information;

but the formal V5 extension requires a third ingredient: **independent information about the contingent decision problem itself**.

This is precisely why the prospective reserve forbids deriving decision classes from observed rewiring.

## Best next move — two-stage empirical program

### Stage 1 — feasibility reanalysis on Villavicencio

Goal: determine whether the network response has enough structure to justify collecting or importing independent decision data.

Freeze before analysis:

- annual interaction matrices;
- shared species / shared partner sets;
- abundance;
- phenological overlap;
- morphology compatibility;
- one prespecified rewiring outcome.

Outputs:

1. annual species-turnover and rewiring components;
2. distribution of shared-partner opportunity;
3. number of repeated dyads;
4. how much rewiring remains after morphology, phenology and abundance;
5. power / estimability of a future independent decision-class exposure.

**Stage-1 success does not validate routeability.** It only shows that the response surface is usable.

### Stage 2 — independent decision-structure layer

Only after Stage 1 passes.

Acceptable routes:

1. published or newly collected pollinator cue-choice assays;
2. independent flower-choice experiments;
3. externally trained cue-response models;
4. a new experiment that manipulates cue hierarchy while holding partner composition approximately constant.

Then freeze decision classes before joining them to the network response.

## Preferred experimental fallback

If no public dataset supplies independent decision structure, a controlled plant–pollinator experiment is cleaner than inventing trait-proxy classes.

Minimal design:

- keep the same set of floral rewards and partner identities;
- manipulate whether an early cue partitions alternatives into informative branches;
- cross this with removal of a non-final versus final representative of an externally defined decision class;
- record visitation links repeatedly through time;
- test rewiring among the shared partner set.

This directly targets the Level-2 / Level-3 evidence ladder from the prospective-test reserve.

## Stop rules

Do not proceed from Stage 1 to Stage 2 if:

- too few species persist across adjacent networks to define rewiring independently of species turnover;
- morphology / phenology / abundance already explain nearly all observable link change, leaving no estimable residual contrast;
- the network has too few repeated transitions for matched (D=1) versus (D=0) comparisons;
- decision classes can only be obtained by inspecting the same link outcomes to be predicted.

Do not label a trait cluster as “decision equivalence” merely because it improves prediction.

## Promotion rule

The dataset screen can enter a follow-up manuscript only after one of two gates is met:

1. a Tier A observational dataset is identified; or
2. an independent experimental decision-structure layer is added to a Tier B network response.

Until then, the public-data work is feasibility analysis, not empirical confirmation of V5 routeability.
