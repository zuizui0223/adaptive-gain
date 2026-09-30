# When observed link turnover does not identify ecological rewiring

Status: post-freeze methods-note reserve. This document does **not** modify the
frozen Evolution Letters V5 submission surface.

## One-sentence result

Binary interaction-network turnover can be perfectly well measured and still
fail to identify ecological rewiring, because observed gain/loss is a joint
function of latent link state and observation probability.

The useful contribution is not the generic statement that sampling matters.
It is a compact set of exact identities and an explicit opposite-direction
witness that show precisely **what binary turnover does and does not identify**.

## Existing literature boundary

Interaction-network sampling bias and imperfect detection are established
problems.

Relevant examples include:

- Weinstein & Graham (2017), *Food Webs*,
  DOI: 10.1016/j.fooweb.2017.05.002 — separates interaction process from
  detection.
- Vizentin-Bugoni et al. (2016), *Journal of Animal Ecology*,
  DOI: 10.1111/1365-2656.12459 — shows network inference changes with sampling
  effort.
- Jordano (2016), *Functional Ecology*,
  DOI: 10.1111/1365-2435.12763 — distinguishes missing from forbidden links
  and reviews interaction-network sampling.
- Gómez-Martínez et al. (2024), *Methods in Ecology and Evolution*,
  DOI: 10.1111/2041-210X.14366 — shows turnover-component estimation changes
  strongly with detectability/sampling and proposes improved partitioning.
- Manning et al. (2025), *Oecologia*,
  DOI: 10.1007/s00442-025-05771-8 — directly demonstrates that apparent
  seasonal plant-pollinator interaction turnover and rewiring are sensitive to
  sampling effort.
- MacKenzie & Royle (2005), *Journal of Applied Ecology*,
  DOI: 10.1111/j.1365-2664.2005.01098.x — repeated-survey design for separating
  occupancy from detection.
- Bailey et al. (2014), *Methods in Ecology and Evolution*,
  DOI: 10.1111/2041-210X.12100 — review of occupancy models separating state
  and detection.

No claim is made that imperfect detection or sampling-sensitive rewiring is new.

## Identity 1 — finite-network turnover balance

On a fixed candidate-dyad universe let `A_1(d), A_2(d)` be observed binary
link states.

Let

- `G` = number of observed gains `0 -> 1`;
- `L` = number of observed losses `1 -> 0`;
- `E_t` = number of observed links at time `t`.

Then exactly

```text
G - L = E_2 - E_1.
```

Therefore aggregate excess gain over loss is not independent evidence for an
assembly/disassembly asymmetry. It is the observed edge-count change written in
transition language.


The same statement extends immediately through time. For a fixed dyad universe,

```text
sum_t (G_t-L_t) = E_T-E_1.
```

Hence cumulative net gain-minus-loss over any number of observation periods is
only the endpoint edge-count change. Intermediate transitions add information
through total turnover and which dyads changed, not through the signed net
balance.

There is also a weighted analogue. If an observed dyad weight changes by
`Delta w`, decompose it into positive and negative parts. Then total weight
strengthening minus total weight weakening equals the change in total observed
interaction weight exactly. This is again bookkeeping, not a separate
mechanistic statistic.


## Identity 2 — probability-flow conservation

For any two binary observations `Y_1,Y_2`,

```text
P(0 -> 1) - P(1 -> 0)
= P(Y_2=1) - P(Y_1=1).
```

No independence assumption is needed.

Thus a change in marginal observed-link probability necessarily creates a
gain-minus-loss imbalance.

## Identity 3 — persistent-link detection specialization

Suppose the latent interaction is truly present in both periods and let
`q_1,q_2` be its marginal probabilities of being detected at least once.

Then

```text
P(observed gain) - P(observed loss) = q_2 - q_1.
```

So detection change alone is sufficient to produce directional apparent
turnover with no latent state change.

Under additional conditional independence of period-level detections,

```text
P(G) = (1-q_1) q_2
P(L) = q_1 (1-q_2)
P(G)/P(L) = odds(q_2)/odds(q_1).
```

The observed gain:loss odds are then exactly the detectability odds ratio.

If within-period census detections are conditionally independent with
per-census detection `p`,

```text
q(n) = 1 - (1-p)^n.
```

For fixed `0<p<1`, more censuses therefore bias a persistent interaction
toward observed gain and fewer censuses toward observed loss.

## Exact nonidentifiability witness — even the full 2 x 2 table is insufficient

Under a standard two-season latent-state/detection model, both of the following
latent systems generate exactly the same observed transition table:

```text
P(00) = 3/5
P(01) = 1/5
P(10) = 1/10
P(11) = 1/10
```

### Latent system A

```text
psi_1 = 1/4
gamma = 7/15
epsilon = 0
q_1 = 4/5
q_2 = 1/2

psi_2 = 3/5
Delta psi = +7/20
```

### Latent system B

```text
psi_1 = 11/20
gamma = 1/18
epsilon = 1/2
q_1 = 4/11
q_2 = 1

psi_2 = 3/10
Delta psi = -1/4
```

Observed binary link prevalence increases from `1/5` to `3/10` in both
cases, yet latent link prevalence increases in A and decreases in B.

Therefore the full binary transition table does not identify even the **sign**
of latent network change when detection is unknown.

This is an explicit network-turnover witness for a general occupancy/detection
identification problem, not a claim to have discovered that problem.

## Villavicencio empirical diagnosis

The six-year Villavicencio plant-pollinator record supplies repeated 5-min
censuses, allowing the observation problem to be examined rather than merely
asserted.

### Raw binary response

The raw reconstruction yields:

- 18 subseason networks;
- 12 within-year transitions;
- 4,581 shared-dyad rows;
- 853 observed binary changes: 422 gains + 431 losses.

These are **observed-link turnover**, not identified ecological rewiring.

### Sampling effort

One raw census is a 5-min focal-plant observation period.

Across subseasons:

- identifiable effort ranges from 38 to 424 censuses;
- incidence-Chao2 observed-link completeness is approximately 31–65%;
- focal-plant effort change ranks observed gain over loss at AUC 0.815 in the
  strict dated core;
- effort-only models have held-out AUC approximately 0.697 for gain and 0.670
  for loss;
- matched-effort rarefaction retains original gain/loss labels only around
  0.58–0.60 on average.

### Effort-standardized response

When the response is focal interaction detections per 5-min focal-plant census,
current focal-response-excluded opportunity has only a small pooled increment
over recent interaction history and is positive in 4/6 held-out transitions.

It fails the frozen all-fold reproducibility rule.

### Latent repeated-detection sensitivity

A simple two-season detection model is identifiable under the frozen gate in
5/6 transitions.

A pre-frozen opportunity decomposition gives:

- latent state-side support: 1/6;
- detection/activity-side support: 4/6.

A beta-binomial observation model is preferred over simple binomial detection
in 6/6 transitions and drives at least one latent transition parameter to the
frozen boundary in 6/6.

Hence there is no stable detection-corrected rewiring response under the tested
observation models.

### Exact detection-direction diagnostic

Using transition-specific fitted period detection and actual dyad census counts,
the persistent-link detection score `q_current-q_previous` ranks observed gain
over observed loss at:

- AUC **0.852** across all six transitions;
- AUC **0.837** across the five simple-model identified transitions.

Every individual transition has AUC > 0.73.

This AUC is deliberately not treated as independent prediction because the
detection probabilities come from the same repeated-census data. Its role is
mechanistic: the empirical direction of observed turnover is strongly aligned
with an observation-map asymmetry that exists even when the latent link is
persistent.

## Practical identification ladder for network-turnover studies

### Level 0 — aggregated binary networks only

Allowed:

- observed-link turnover;
- binary network dissimilarity.

Not identified:

- true link gain/loss;
- ecological rewiring;
- direction of latent link-prevalence change.

Minimum reporting:

- fixed candidate-dyad universe;
- edge counts in both periods;
- `G-L = E_2-E_1`;
- sampling effort and completeness.

### Level 1 — effort inventory / rarefaction

Adds evidence about sampling sensitivity.

Still not sufficient for latent rewiring because equal effort does not guarantee
equal detectability.

### Level 2 — effort-standardized interaction incidence

Model detections relative to exposure/census count.

Supports interaction-rate or encounter/detection associations.

Still does not by itself identify latent link states.

### Level 3 — repeated-detection latent-state model

Can separate state and detection under an explicit observation model.

Required diagnostics:

- identifiability;
- sensitivity to detection heterogeneity / overdispersion;
- boundary estimates;
- repeated-survey closure assumptions.

Only promote latent gain/loss if inference is stable to a defensible observation
model.

### Level 4 — independent state or experimental manipulation

Independent information on true interaction state, or controlled manipulation
that separates state from observation, gives the strongest mechanistic
evidence.

## Recommended terminology

Use:

- observed-link turnover;
- detected interaction incidence;
- latent-state estimate under model X;
- detection/activity-side signal.

Reserve **ecological rewiring** for cases where the state-versus-observation
distinction is adequately identified for the intended claim.

## Relation to routeability

This note does not validate or test routeability.

Its role in the adaptive-gain program is to prevent an observational network
response from being promoted into a decision-structure mechanism when the
response itself is not identified.

The direct matched routeability experiment remains the cleaner test of the
decision-structural mechanism.

## Stop rule

Do not add increasingly flexible Villavicencio observation models merely to
search for a positive rewiring result.

Further natural-network mechanism claims require either:

1. an independent network with a defensible detection-standardized state
   process plus an independent decision layer; or
2. an experiment that separates ecological interaction state from
   encounter/detection.

## Claim ceiling

The methods-note reserve supports an explicit identification boundary for
binary network turnover and a worked repeated-detection diagnosis.

It does not claim novelty for imperfect detection, does not identify a corrected
Villavicencio rewiring process, and does not modify or validate the frozen V5
routeability theory.
