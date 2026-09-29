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

**Tier C — high-value response/detection test bed, not a routeability pilot.**

Why it remains valuable:

- repeated yearly networks;
- raw public dated visitor records;
- independently measured morphology;
- a large set of shared species and links across years;
- raw records permit focal-response-excluded availability/activity opportunity and 5-min census effort to be reconstructed.

Why it is no longer treated as Tier B:

- the published `phenological_overlap` candidate-gain surface is response-conditioned and is quarantined;
- binary gain/loss is materially effort- and detection-sensitive;
- an effort-standardized census-incidence response leaves only a small, fold-mixed opportunity increment (4/6 dated-core transitions);
- a simple repeated-detection model is identifiable enough for sensitivity analysis in 5/6 transitions, but current opportunity receives latent state-transition support in only 1/6 while a detection/activity component is supported in 4/6;
- availability, activity and morphology still do not establish an independent cue hierarchy or decision-equivalence structure.

A trait- or network-derived class system can only be exploratory unless externally justified by independent behavioral evidence.

### Allowed use

Use Villavicencio for:

- response reconstruction;
- sampling-effort and detection diagnostics;
- focal-response-excluded ecological opportunity/activity associations;
- demonstrating why observed-link turnover cannot automatically be interpreted as latent ecological rewiring.

Do **not** use it as the observational Stage-2 routeability test. The predeclared natural-rewiring bridge fails its general latent-state promotion rule in this system.


## Candidate 1b — Villavicencio 18-subseason response surface

**Source:** Vázquez & Chacoff Dryad dataset, `10.5061/dryad.j6q573n9j`.

This is a second public release from the same Villavicencio plant–pollinator system. It contains:

- 18 bipartite interaction matrices;
- three subseasons per year across 2006–2011;
- 18 directed dependence matrices;
- plant and pollinator identification codes;
- the original 59 plant species, 196 flower-visiting insect species, 28,015 visits and 1,050 interacting pairs.

### Screening decision

**Preferred Stage-1 response grain is now reconstructable from the public raw dated records.**

The Dryad methods define the three subseasons by date, so the public Figshare visitor records can reconstruct an 18-period response without requiring the unavailable RData bytes. The frozen 45 × 135 subset yields 18 non-empty period networks and 12 within-year adjacent transitions. Exact byte-for-byte identity with the RData object is **not** claimed.

The higher temporal resolution improves the feasibility test substantially. Rather than relying only on five year-to-year transitions, the primary Stage-1 response contains 12 within-year adjacent transitions:

[
6\;\text{years}\times(\text{early}\to\text{mid},\;\text{mid}\to\text{late})=12.
]

Year-end to next-year early transitions should be sensitivity analyses rather than part of the primary series because they span a qualitatively different seasonal gap.

The response reconstruction is frozen to the same 45 plant × 135 pollinator subset used by the annual analysis. The published aggregate `phenological_overlap` matrix is **not** reused as a candidate-gain opportunity surface; conventional opportunity must be rebuilt from raw dated records with focal-response exclusion.

The reconstructed Stage-1 response contains **4,581 shared-dyad rows and 853 changed links (422 gains, 431 losses)**, and all **12/12** within-year transitions contain both changed and unchanged shared dyads. Presence is still defined from observed positive links, so the turnover partition remains detection-sensitive rather than true species turnover.

### Date-completeness boundary

Dated raw records recover complete annual positive-link support for 2006–2010. In 2011, **433 of 440** annual links have dated support; seven links occur only in positive rows lacking a date and therefore cannot be assigned to a subseason. The 12-transition response is retained with this limitation explicit, while 2006–2010 provides a dated-complete sensitivity. Exact equality to the inaccessible RData object is not asserted.

A second modeling boundary is also explicit: 2006 mid→late contains one gain and no loss. That transition is valid for the changed-versus-unchanged Stage-1 feasibility audit, but separate endpoint-specific gain/loss models must use a prespecified nondegenerate scope.

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

## Candidate 4 — Villavicencio as a clean non-routeability baseline

The Villavicencio system remains valuable even if it never supplies decision classes, but its baseline must respect the support-leakage audit.

The clean **non-routeability** layer is now:

- focal-response-excluded current-year plant availability;
- pollinator activity on other plants;
- the small incremental focal-excluded weekly-overlap term;
- independently measured plant and pollinator morphology where used with an outcome-independent support definition.

The published aggregate phenological-overlap matrix is retained only as historical/source context, not as the full candidate-dyad gain surface.

This repaired baseline is the appropriate comparator for asking whether a later independent decision-structure term adds information beyond ordinary ecological opportunity.

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

## Best next move — observational stop rule, then direct mechanism test

### Villavicencio observational result — stop here

Villavicencio has now answered the observational feasibility question as far as the public data allow.

**Response reconstruction**
- 18 subseason networks and 12 within-year transitions are reproducible from public raw dated visits;
- the 45 × 135 subset yields 4,581 shared-dyad rows and 853 observed binary changes;
- exact RData byte identity remains an optional source cross-check, not an ecological result.

**Detection boundary**
- 5-min census effort is reconstructable;
- binary turnover is materially effort-sensitive;
- matched-effort rarefaction destabilizes original link-state labels;
- the 853 changes must be called **observed-link turnover**, not identified ecological rewiring.

**Opportunity after effort handling**
- annual gain prediction contains information beyond focal-plant census count;
- at the finer dated-core scale, effort-standardized interaction incidence shows only a small opportunity increment and only **4/6** held-out transitions improve;
- a simple two-season detection model passes its identifiability gate in **5/6** transitions;
- after separating opportunity effects on latent state from opportunity effects on current detection, state-side support appears in only **1/6** transitions versus a frozen **5/6** requirement, whereas detection/activity-side support appears in **4/6**.

Therefore the Villavicencio natural-network routeability bridge is **not promoted**.

The useful empirical conclusion is a failure boundary:

> strong apparent binary rewiring predictors can largely map onto ecological activity/encounter/detectability once repeated detection is modeled.

This is exactly the point at which additional flexible observational modeling should stop.

See:
- `validation/villavicencio_subseason_effort_audit_result_v1.json`
- `validation/villavicencio_census_rate_result_v1.json`
- `validation/villavicencio_two_season_detection_result_v1.json`
- `validation/villavicencio_latent_opportunity_decomposition_result_v1.json`
- `validation/villavicencio_rewiring_claim_resolution_v1.json`

### Next empirical mechanism test

Do **not** proceed by adding a decision-class proxy to the Villavicencio links.

The next routeability evidence must instead come from either:

1. a genuinely independent network dataset with detection-standardized link states **and** an independently measured cue/decision layer; or
2. the controlled routeability experiment already frozen in this PR.

For an observational dataset, decision classes must be frozen before joining them to the network response and must not be inferred from the same links being predicted.

## Preferred direct experiment

Given the Villavicencio detection boundary and the absence of a Tier A public dataset, the controlled plant–pollinator experiment is now the preferred direct mechanism test rather than merely a fallback.

Minimal design:

- keep the same set of floral rewards and partner identities;
- manipulate whether an early cue partitions alternatives into informative branches;
- cross this with removal of a non-final versus final representative of an externally defined decision class;
- record visitation links repeatedly through time;
- test rewiring among the shared partner set.

This directly targets the Level-2 / Level-3 evidence ladder from the prospective-test reserve.

## Stop rules

Villavicencio has reached the observational stop rule because:

- observed binary turnover is materially detection-sensitive;
- the effort-standardized opportunity increment is fold-mixed;
- the repeated-detection sensitivity supports a general opportunity effect on latent state transitions in only 1/6 transitions;
- the same opportunity variable more commonly maps onto current detection/activity;
- an independent decision class is still absent.

Do not add more flexible Villavicencio models to search for a positive rewiring mechanism, and do not label a trait cluster as “decision equivalence” merely because it improves prediction.

For any future observational candidate, stop if true link state cannot be separated defensibly from detection or if decision classes can only be obtained by inspecting the same link outcomes to be predicted.

## Promotion rule

The natural-network routeability extension can be promoted only after one of two gates is met:

1. a Tier A observational dataset is identified with detection-standardized link states and an independent decision layer; or
2. the controlled routeability experiment supplies direct behavioral evidence for the frozen cue architecture contrast.

Villavicencio itself is retained as a response/detection boundary case, not empirical confirmation of V5 routeability.
