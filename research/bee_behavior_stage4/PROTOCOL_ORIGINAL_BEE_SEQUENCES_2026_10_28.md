# Stage 4 — direct individual bumblebee history and fixed flower-array data

**Research decision (2026-10-28):** Stop adding post-hoc botanical predictors to the same UK PoMS programme. Switch to an **independent behavioural experiment with tagged individual bees, complete visit timestamps and a known artificial flower array.** Source ingestion and roles must be validated *before* fitting transition/history models.

## Source and scientific grain

Primary source is **Pasquaretta et al. (2019)**, *A spatial network analysis of resource partitioning between bumblebees foraging on artificial flowers in a flight cage*, **Movement Ecology** 7:4, DOI https://doi.org/10.1186/s40462-019-0150-z, CC BY 4.0 article/data. Its publicly published **Additional file 2, dataset S1** is a ~59 kB CSV:
`https://static-content.springer.com/esm/art%3A10.1186%2Fs40462-019-0150-z/MediaObjects/40462_2019_150_MOESM2_ESM.csv`.

The original publication reports **6,205 flower visits and 628 bee-bee encounters** across five monitored days in one controlled colony experiment, with ten artificial flowers at fixed positions, replenished by pumps; individual bees wore identity tags and camera timings were recorded for each flower. These are **publication-reported totals, not audited original raw CSV counts**. The original paper already reported experience-dependent spatial partitioning and avoidance following displacement. Mere confirmation of its stated effect is **not** a novel finding.

**Experimental flower options:** all ten physical artificial flowers were present in the cage and maintained throughout tests, but their **instantaneous sensory detectability differed with geometry and location**; the full ten are not asserted to be a simultaneously visually perceived choice set by a bee. All artificial flower rewards used the same sucrose pump design. This experiment did **not** manipulate wind; it is **not** a second PoMS wind-effect replication.

## Primary (pre-data) data quality gate
1. Download the *exact published original CSV* by its publisher URL, with explicit backup only to the identical publisher supplementary file on PMC when available; preserve source URL, HTTP response, bytes, **SHA-256**. Do not commit raw original visit identifiers or video files to GitHub; CI artifact retains only non-identifying schema/quality/results.
2. Profile **original column names and their actual value formats**, including source delimiters and any date/time/timezone semantics. Count original rows, candidate individual tags, source flowers, dates/bouts, missing values, duplicates, non-monotonic times and impossible intervals. If role identification is ambiguous, stop with a **SCHEMA_GATE** and report the original columns rather than guessing.
3. Identify a **physical sequence order only if supported by a time field**. If multiple visits by one bee have indistinguishable timestamps with no documented tie-break, label sequence ties and exclude affected transitions; **never silently order by CSV row or flower ID**. Flag overlapping records: simultaneous different-flower visits by the same bee are not physical, but may represent different observers/ambiguous video timing. Avoid deleting anomalies without receipts.
4. If raw data are a subset of the publication's reported 6,205 visits (e.g. restricted >20-visit regular bees), reconcile this with source methods and **do not equate source rows with all observation events**.

## Analysis decision if schema gate passes
**P1: Does previous recorded flower identity predict a bee's next observed flower beyond that bee's static flower-use margins, on genuinely later held-out visits?**
- M0: bee-specific empirical distribution across **source-available physical flower IDs** with a fixed Dirichlet/pseudocount for unseen flowers.
- M1: bee-specific first-order transition model, smoothed toward M0 with **a fixed source-independent shrinkage hyperparameter** (to be frozen before inspecting held-out outcomes); do not fit hyperparameters on held-out period.
- Primary held-out split: final monitored day, trained on strictly earlier days. If explicit dates are unavailable but source bouts are grouped, permit chronological final 20% **per bee** as a separately labelled fallback, not falsely called leave-last-day-out.
- Score sequential proper out-of-sample **mean negative log likelihood in nats per transition**, with the **bee** as uncertainty unit; report per-bee Δloss and its distribution. At least five bees with ≥20 training visits and ≥5 held-out evaluable transitions. If fewer, report **NO_GO_TEST_SUPPORT**.
- M1 advantage can be due to spatial continuity or learned flower preference, not uniquely information acquisition. Compare an additional fair source-geometry/static-distance baseline **only** if exact flower coordinates are available in the original supplement and computable without speculative assignments; otherwise a missing coordinate gate is explicit.

**P2: Does a *recent source-recorded social displacement* predict individual return avoidance beyond the previous flower and usual flower preference?** Fit only if original CSV has reliable identity, departure time, flower, and a direct encounter/displacement outcome or reconstruction documented by source event semantics. A merely overlapping occupancy interval is **not itself proof** of displacement. Prespecify outcome as next-bout return to the same physical flower; fail closed if bouts or displacement are not identifiable. The paper already reported avoidance; an empirical contrast must add independent uncertainty control rather than call itself novel.

**No aimless secondary feature search.** Neither model is a proof of the information *order* a bee perceived, nor of `C_A`, `C_F`, nectar fitness, causal competition, adaptive reward improvement, or ecological wind response. A positive sequence predictive gain is a lower-level behavioral observation to connect to routeability theory in future experimental designs.

## Independence, pseudoreplication and stop rules
- The source is **one flight cage / one colony / at most tens of individual marked bees**. Thousands of visits are repeated observations, not independent colonies.
- Temporal train/held-out evaluation must not leak later observations or unseen bee-specific flower margins back into the training model. No random-row cross-validation.
- Report results per bee and guard against missing flower IDs, unequal visit effort, reward refill timing, nest returns and physical interaction-induced preference changes.
- No modifications of the frozen V5/V6 manuscripts or the PoMS Stage 3f/g results. Branch from `main` into a distinct draft PR for this separate experiment. Primary hypothesis/limitations committed *before* inspecting raw experimental records.
