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
- raw public dated visitor records;
- independently measured morphology;
- a large set of shared species and links across years;
- raw records permit focal-response-excluded availability/activity opportunity to be reconstructed rather than inferred from the focal link itself.

Important repair boundary:

- the published `phenological_overlap` matrix is **not** a valid full candidate-dyad gain predictor for this project because its non-zero support is nested inside dyads realized as links at least once;
- the historical published-overlap gain model is therefore quarantined for ecological interpretation;
- the repaired raw-record opportunity surface has broad support among never-realized dyads and is the valid conventional ecological baseline.

Why it is **not Tier A**:

- availability, activity and morphology do not establish the cue hierarchy or contingent decision problem of a pollinator;
- defining decision-equivalence classes directly from the same network links would be circular;
- a trait- or network-derived class system can only be exploratory unless externally justified by independent behavioral evidence.

### Allowed pilot use

The annual fallback now answers a clean narrower question:

> Does focal-response-excluded current ecological opportunity discriminate link gain and loss, and how much residual structure remains for a later independently defined decision-class test?

The repaired answer is yes for current-year opportunity, while the one-year-lagged negative control does not recover the same signal. Do **not** call this routeability or strict forecasting.


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

## Best next move — two-stage empirical program

### Stage 1 — Villavicencio ecological baseline

Stage 1 now has two complementary green surfaces.

**Response surface:** public raw dated records reconstruct the documented 18-period grain, giving 12 within-year transitions with 4,581 shared-dyad rows and 853 changed links. This removes the earlier dependence on unavailable RData bytes for response feasibility, while retaining an explicit 2011 missing-date limitation.

**Ecological baseline:** the annual focal-response-excluded opportunity repair remains the cleaner current-state predictor analysis.

Current annual result:
- focal-response-excluded current-year availability/activity discriminates both gain and loss across held-out annual response transitions;
- the signal is stronger for gains;
- pair-specific weekly overlap is only a small, sensitivity-dependent increment beyond the marginal opportunity terms;
- the same opportunity construction measured one year earlier does not recover the current-state signal.

The 18-subseason response is therefore no longer blocked on RData materialization. What remains unavailable is only a byte-for-byte cross-check against that published object. Any predictor analysis at the subseason grain must still rebuild opportunity from raw dated records or another independently defined support surface. Do **not** reuse the published aggregate overlap matrix as though it covered all candidate dyads independently of realized interactions.

**Stage-1 success does not validate routeability.** It supplies the clean ecological baseline against which an independent decision layer must compete.

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
