# Uehara et al. 2026 binned individual first-probe result

Status: public-source-data secondary analysis for the V6 fitness-frontier programme.

Source:

Uehara, Dong & Duvall (2026), Communications Biology,
"Behavioral heterogeneity in host seeking and post-feeding suppression among
disease vector mosquitoes", DOI 10.1038/s42003-026-09987-z.

Public Supplementary Data 1:

- sheet `Fig2D and S2`;
- one row per included individual;
- separate Flight, Probe and Walk percentages;
- Probe percentages in one-minute bins from -1–0 min and 0–1 through 7–8 min.

## 1. Row identity is independently checkable

The number of individual rows recovered from the Probe block exactly matches the
paper's `Excl_Spp_Cond` timepoint-0 count of individuals inactive before host
cue application:

| species | Fig2D/S2 rows | exclusion-table count |
| --- | ---: | ---: |
| *Aedes aegypti* | 43 | 43 |
| *Aedes albopictus* | 55 | 55 |
| *Anopheles gambiae* | 47 | 47 |
| *Anopheles stephensi* | 43 | 43 |
| *Culex tarsalis* | 30 | 30 |
| *Culex quinquefasciatus* | 15 | 15 |

This makes the Source Data an individual-level dataset, although not a
frame-level dataset.

## 2. Primary onset contract

A positive Probe percentage in the 0–1 min bin is not necessarily a new
post-stimulus onset if that individual was already probing before time zero.

Therefore the primary analysis is restricted to individuals with

[
	ext{Probe}_{-1:0}=0.
]

For each such individual, define the first post-stimulus one-minute bin with

[
	ext{Probe}>0
]

as an interval-censored first-probe onset.

If no post-stimulus bin is positive, the individual is right-censored at
8 min.

This endpoint is written as:

> first observed post-stimulus probing interval among individuals with zero
> probing in the preceding one-minute bin.

It is not called frame-resolved latency.

## 3. Individual completion-profile result

The clean primary cohort contains 112 individuals.

| species | primary n | probe by 1 min | probe by 8 min | median CDF crossing |
| --- | ---: | ---: | ---: | ---: |
| *Ae. aegypti* | 28 | 18/28 = 64.3% | 25/28 = 89.3% | 1 min |
| *Ae. albopictus* | 38 | 10/38 = 26.3% | 23/38 = 60.5% | 4 min |
| *An. gambiae* | 14 | 12/14 = 85.7% | 12/14 = 85.7% | 1 min |
| *An. stephensi* | 18 | 15/18 = 83.3% | 18/18 = 100% | 1 min |
| *Cx. tarsalis* | 10 | 7/10 = 70.0% | 10/10 = 100% | 1 min |
| *Cx. quinquefasciatus* | 4 | 3/4 = 75.0% | 4/4 = 100% | 1 min |

The largest first-minute contrast is between *An. gambiae* and
*Ae. albopictus*:

[
0.857-0.263
=
0.594.
]

The striking feature is not just a mean difference. The empirical discrete
completion profiles have very different early tails and different right-censor
mass.

### *Ae. albopictus*

Its cumulative probability of any first post-stimulus probing is:

[
F(1)=0.263,
]

[
F(2)=0.447,
]

[
F(3)=0.474,
]

[
F(4)=0.500,
]

and

[
F(8)=0.605.
]

Thus the median is not reached until the fourth minute, and 39.5% of the clean
cohort remains without observed probing through 8 min.

### *An. gambiae*

[
F(1)=0.857
]

and remains 0.857 through 8 min: nearly all individuals that probe do so in the
first minute, while two individuals remain right-censored.

This is a distribution-shape difference that would be obscured by a single
mean latency.

## 4. Relation to V6 theory

The V6 expected-value layer uses an empirical object of the form

[
F_j(t)=P(T_jle t).
]

The present analysis provides a coarse, individual-level analog of that object
at one-minute resolution.

It therefore improves the empirical anchor relative to an aggregate activity
trajectory:

- individuals are retained;
- early-tail mass is observable;
- right censoring is explicit;
- completion profiles can be compared without inventing a mean latency.

It still does not identify the biological value function

[
U(t),
]

so it cannot estimate selection by itself.

## 5. Relation to the Chandel anchor

The two public datasets now support different sides of the process story.

Chandel et al. 2024:

- high temporal resolution;
- aggregate population host-seeking effect;
- shows that cue advantage is strongly nonuniform through time.

Uehara et al. 2026 Supplementary Data:

- coarse one-minute resolution;
- individual-level Probe trajectories;
- supplies empirical discrete completion-profile shapes.

Together they justify separating:

[
	ext{when individuals complete an action}
]

from

[
	ext{how ecology values completion at that time}.
]

Neither dataset closes the full adaptive-versus-fixed selection chain.

## 6. Claim ceiling

Do not interpret this secondary analysis as:

- frame-resolved first-probe latency;
- time to successful blood feeding;
- time to a sufficient blood meal;
- reproductive fitness;
- a natural opportunity distribution;
- an adaptive-versus-fixed architecture test;
- evidence that species differences are caused by routeability.

The result is an **individual temporal-process receipt**.

Frame-level XLSX files or videos remain useful for refining the one-minute
intervals, but they are no longer required to demonstrate that individual
completion profiles differ strongly in shape.
