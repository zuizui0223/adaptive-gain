# Stage 4 empirical result — individual bee route order predicts next flower beyond static flower use

**Date:** 2026-10-28. **Status: ORIGINAL-DATA TEST COMPLETE, POSITIVE HELD-OUT SEQUENCE PREDICTION, causal routeability NOT established.** Validated dedicated CI [GitHub Actions run 40536545147](https://github.com/zuizui0223/adaptive-gain/actions/runs/40536545147) **SUCCESS, all 35 focused tests passed** with publisher retrieval, original source schema and original-data behavioral prediction all completed. Frozen V5/V6 manuscripts untouched.

## Source and byte-for-byte provenance

Pasquaretta, C., Jeanson, R., Pansanel, J., Raine, N. E., Chittka, L. & Lihoreau, M. (2019). *A spatial network analysis of resource partitioning between bumblebees foraging on artificial flowers in a flight cage.* Movement Ecology, 7, 4. DOI **https://doi.org/10.1186/s40462-019-0150-z**. The exact original open-access supplementary **Dataset S1** was fetched directly from:
`https://static-content.springer.com/esm/art%3A10.1186%2Fs40462-019-0150-z/MediaObjects/40462_2019_150_MOESM2_ESM.csv`.

- Direct publisher HTTP 200, source original bytes **61,316**, SHA-256 **`0d30b0957c4b18602beebf60a915e03bee26142a8593f252badd77881b5e9dfe`**. CI enforces the exact digest before fitting. Public article has CC BY 4.0 and data CC0 waiver unless otherwise marked. Data themselves remain in the ephemeral runner, not committed to the repository.
- Exactly **881** original source rows = **881 individual tagged-bee foraging bouts**. Source uses six named columns `day, bee, foraging bout, start_time, end_time, duration` and **35 unnamed, left-to-right visit-order slots**. It is **not** a one-row-per-visit dataset; filling or sorting these anonymous fields as if generic categories would destroy the observed sequence.
- Across 10 bee tags, 5 experimental days, 10 native flower labels in the physically fixed array: **6,205 individual recorded flower visits** (exactly the publication-reported number). Under source bout boundaries, there are exactly **5,324 consecutive *within-bout* flower-to-flower transitions**. Day 5 has **214 bouts, 1,764 visits and 1,550 within-bout transitions**; days 1–4 provide **667 bouts, 4,441 visits and 3,774 within-bout transitions**.
- **0** exact duplicate source rows, **0** empty original flower-visitation bouts, **0** source bout duration differences >1 s, **0** temporally overlapping source bouts for the same individual and **0** duplicate same-bee/day start times. All 881 rows have 41 source CSV fields. Median **6** visits per bout, maximum 35.
- Original start/end numerical time stamps reach >86,400 on later days and refer to the **experiment-wide numeric clock**. They were **never** treated as local 24-hour clock times, reset at midnight or interpolated to infer individual flower landing times. Original source fields lack explicitly identified individual encounter/displacement outcomes, despite those being discussed in the original paper.

### Original publication versus new analysis

Pasquaretta et al. already reported bee-flower network modularity, experience-dependent resource use and avoidance after social displacements. **Do not present these published biological observations as newly discovered.** This Stage 4 branch evaluates a distinct, specified *out-of-sample conditional predictive contrast* of flower-order history versus static flower-use margins, with a separate bout-multiset preserving negative-control randomization. It does not turn a single previous paper into a cross-study macro-analysis or a new causal discovery.

## Before-outcome model definitions and strict chronological separation

Exact source role and source-format gate were completed before scoring the full original data. The follow-up model design and hyperparameters were recorded *before* inspecting held-out Stage 4 scores; see `PROTOCOL_ORIGINAL_BEE_SEQUENCES_2026_10_28.md`.

- Every experimental bee had ten **physically present** artificial flowers available in the cage. This is not proof that all ten were *simultaneously visible* to a bee at any given landing.
- **M0 — static bee-specific preference:** `P(f | bee)` from each bee's earlier four days of visits, with predeclared additive **α=0.5 per physical flower**, ensuring positive probability for flower identities absent in that bee's training record.
- **M1 — static preference + previous physical flower:** `P(f_next | bee, f_previous)`, computed only from that bee's earlier days' within-bout transition table and shrunk toward its own M0 with **β=5** equivalent pseudoobservations. Both smoothing values were fixed before inspecting Stage 4 outcome scores.
- Test set is only **day 5**, held out in full. Predictions can see an earlier observed flower on day 5 because it was known **before** the predicted next flower; day 5 labels never train or tune the transition model. **Reset at every original bout boundary**, no fabricated nest-to-flower or overnight links. All 10 bees pass ≥20 early training visits, ≥5 last-day transitions, and ≥5 evaluable bee tags.

The proper scoring rule is **negative log likelihood (nats per next-flower transition)**. Primary unit is one marked bee. A 5,324-transition total is **not** 5,324 independent experimental animals.

## Held-out empirical result: predictive sequence information is present

| Individually tagged bee | Day-5 within-bout transitions | M0 NLL (nats/transition) | M1 NLL | M0−M1 gain |
|---|---:|---:|---:|---:|
| w25 | 340 | 2.2987 | 1.8665 | **+0.4322** |
| w37 | 399 | 2.2340 | 1.7908 | **+0.4431** |
| w58 | 296 | 2.0793 | 1.9017 | **+0.1777** |
| y35 | 76 | 2.0232 | 1.6865 | **+0.3367** |
| y39 | 30 | 2.0732 | 1.8991 | **+0.1741** |
| y45 | 74 | 2.1889 | 2.3199 | **−0.1310** |
| y62 | 119 | 2.1382 | 1.7988 | **+0.3394** |
| y63 | 100 | 1.7436 | 1.6825 | **+0.0610** |
| y64 | 59 | 2.1323 | 2.0273 | **+0.1051** |
| y67 | 57 | 2.2174 | 2.0904 | **+0.1270** |

**9/10 bees** show *positive prospective* predictive improvement from previous-flower identity; one bee (y45) has a negative gain. **Mean per bee = +0.2065275 nats per transition**, median per bee = +0.1758606 nats. Totals: **1,550** strictly later day-5 within-bout transitions. The descriptive transition-count-weighted gain is +0.29509 nats, **not** the main independent-unit estimate.

Exact within-colony sign-flip test of the 10 bee-specific gains: **two-sided p = 0.009765625**. Since all 10 bees belong to a *single colony and a single cage array*, this is a **within-colony directional diagnostic**, not inference to ten independent colonies or a global species/region-level effect.

**Supported point:** bee-specific flower visitation margins do not exhaust the predictive information in the individual's observed ordered foraging routes. Under this fixed held-out test, the previous recorded flower improves forecasting on a genuinely later observation day.

## Additional conditional null: preserve everything except within-bout order

A secondary analysis, committed before the empirical result, uses **199 source-preserving shuffles**, fixed RNG seed **20261028**. It permutes **only within-day-5, within-bout ordering of visits**. Each bee's day-5 bout count, bout size, and multiset of visited flowers (including repeated visits to the same flower) remain *exactly* preserved. Earlier-day training observations, both trained predictive models, the physical 10-flower labels and each bee's eligibility remain unchanged.

| Statistic (M0−M1 gain, nats/transition, bee-mean) | Value |
|---|---:|
| **Real visit order**, genuine day 5 | **+0.2065275** |
| **Within-bout shuffled order**, mean of 199 controls | **−0.2916815** |
| Shuffled null distribution, 5–95% empirical percentile | −0.33549 to −0.25638 |
| **Observed minus shuffled mean** | **+0.4982090** |
| Positive-tail Monte Carlo p | **0.005 (1/200 minimum)** |

The original visit order is larger than all 199 shuffled scores. This supports **non-exchangeable within-bout visit order beyond the per-bout visited-flower multiset**. It does not show that the bee consciously queried sensory cues in a particular order: **physical flower geometry, learned circuits, flight-path continuity, within-bout state persistence and natural movement constraints** can also produce that ordering. This null is a negative control on sequence structure, **not** a randomized cognitive experiment.

## What is not established; next true mechanism gate

- **Not a wind experiment.** No wind direction or controlled wind levels were included in these original bout records; do not pretend this directly replicates the earlier PoMS wind association.
- **Not interspecific network structure.** The source is a single bee species and ten physically fixed sucrose flowers, not a natural plant community. It does not test abundance or niche partition of plant taxa, indirect interspecific competition, or plant-derived visual/scent cue accessibility.
- **Not source-known competition outcome:** there are no explicit tagged-bee displacement variables in the published S1 bout CSV, despite the parent study describing social competition elsewhere. P2 social-displacement-to-future-return analysis is **NO_GO_WITH_THIS_ORIGINAL_TABLE**.
- **Not adaptive routeability / fitness:** last-flower predictive value is not proof of sensory observation order, query/access cost `C_A/C_F`, perceived option sets or reproductive fitness payoff. The array's full ten artificial flowers were not necessarily simultaneously visually detectable; geometric accessibility is a major alternative explanation.
- **Not independent population replication:** all tagged bees came from one colony and one cage across five consecutive days. Individual tag replicates do not make the experimental setup independent. Training/held-out proper scoring and within-bout permutations help against overfitting and marginal-preference nulls but cannot substitute experimental replication.

**Decision:** retain positive Stage 4 as an **empirical behavioral bridge** between static interaction structure and ordered decision histories, independently sourced from the observational PoMS dataset. The next decisive test is randomized variation in **when/which cue or flower location becomes observable** with individual bee tracking and measured reward/fitness or controlled geometry; independent colonies and flower layouts are needed for generalization. Do not promote the single-colony prediction result to a general routeability theorem or change frozen manuscript claims.
