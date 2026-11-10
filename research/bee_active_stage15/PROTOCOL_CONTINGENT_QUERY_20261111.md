# Stage 15 — randomized contingent information access, not externally imposed cue order

**2026-11-11. Design and exact finite-game mathematics ONLY. NO bees have been tested or recruited.** Stage15 is a separate optional design stacked on Stage14 (PR #92), not a modification of that frozen branch, historical data, or main.

## The one new mechanism question

Can a bee reduce the number of *real source information requests* without sacrificing target-choice accuracy by choosing the next requested cue **AFTER**, rather than **BEFORE**, it sees the outcome of an initial cue?

The treatment is randomized **contingent access opportunity** (decide first follow-up cue after observing R) versus **precommitted access** (bind same first follow-up request before observing R). Both modes keep self-initiated cue requests, identical physical channels, the same world states, eventual available target choices, a neutral/matched pre-R motor control, and the same source timing/effort per real cue reveal. This differs fundamentally from Stage9/14's experimenter-forced presentation order.

## Pre-outcome mathematical benchmark; not an observed biological effect

Three independent uniformly random binary source variables: root R∈{0,1} and optional cue values U,V∈{0,1}. Correct flower target is **U when R=0, V when R=1**. Root R is presented in both arms; animals must learn the mapping in a separate blinded training/pilot BEFORE any real main trial. Each trial's three source bits are drawn **independently with replacement**, keeping the full 8-state distribution uniform in expectation; do NOT enforce equal state quotas within blocks, because a finite deck would make later R values predictable from earlier trials. The two physically accessible target flowers L/R correspond to 0/1, randomized physical sides in additional independent balancing if later added, not implied by cue alphabet.

- Contingent choice: observe R; request U when R=0 or V when R=1. **Exactly one leaf request** yields the target under error-free learning (two total observations including R).
- Noncontingent precommit: choose U or V **BEFORE** R, with the originally chosen request physically locked even after R is shown; if the first leaf is not relevant, a second request is available at identical measured cost. Under independent equiprobable R, **expected 1.5 leaf requests** under the full-information error-free policy (2.5 total observations with root). The difference is **0.5 paid leaf requests per trial** in the specified restricted-comparator game, not a universal sharp bound over all nonadaptive policies.
- A cost c per real leaf reveal (toy units) creates an illustrative normative full-correct payoff advantage 0.5c in favor of contingent access. The value c and reward conversion must NOT be assumed biologically calibrated; do not claim observed sucrose savings.
- Full-alternative success is **not** assumed for actual bees: they can guess, miss cues, decline a second query or use unexpected strategies. Report actual choices and errors from ALL randomized trials without selecting successful animals.

## Factorial assignment and source population

2×2: access mode `contingent`/`precommit` × physically instrumented wind `calm`/`crosswind`; secondary wind interaction, not the target of a significance search. Source worlds (R,U,V) are separately randomized and concealed on each original trial. Demonstration QA only: 24 *synthetic* colonies×12 synthetic bee IDs×64 trials=18,432 simulated assignment records. Each bee has four 16-trial wind blocks in the same balanced ABBA/BAAB structure as Stage14; each block allocates exactly 8 trials per access mode while each trial's R/U/V state is a fresh independent three-bit draw. Across both blocks for a given wind condition, each bee×mode×wind contains 16 trials but no forced state counts. Do not reveal source schedule, real animal seed or future state assignments.

## Physical source-event requirement before animal testing

Every trial must be timestamped with original bee and colony identity, randomized access arm/wind/world, pre-R button act and whether it is binding, actual R exposure and comprehension, post-R request act (contingent selection vs precommit neutral acknowledgment), original cue selector U/V, first leaf reveal, optional second leaf reveal, last feeder-choice / no-choice, synchronization and both target alternatives. Real cue reveal events must be source-verified, not inferred from selected flowers or trial labels. The first leaf request is mandatory in both arms; the second is optional and charged equally. Precommit first-request identity cannot be changed after R, and contingent request cannot be locked before R. Use an identical initial motor/attention task to control action effort but acknowledge it may not fully control the psychological effects of making a commitment before knowing R.

Fixed real observation window (e.g. 30 seconds **from initial R presentation**, not from final feeder access) captures time spent querying. Do not redefine start time based on last cue reveal, which would erase the query-cost opportunity. All apparatus cues must be clearly distinguishable by bees after separate learning verification, no target reward/handling cues should leak from feeder appearance before query, and known cue-value mappings must not be visible at choice unless obtained by actual request.

Record both final target-choice correctness and calibrated, independently blank-corrected sucrose actually consumed within the same original fixed window; valid no-choice/no-feeding is 0, source sensor failure is MISSING (and returns NO_GO), no real individual data currently exist. Physical reveal latency and wind measured per source trial, calibrated in independent pilots. Original ethical approvals, colony access, learning pilot and real allocation secrecy are external prerequisites, not actions taken by this branch.

## Prespecified intended biological inference (requires independent pilot)

- **Primary prospective ITT**: verified total sucrose intake (mg per fixed initial-R–anchored 30s opportunity) comparing contingent versus precommit access, equal bees within original colonies then equal independent colonies, averaged over both assigned wind conditions. No exclusion for making more requests, wrong targets, or no-drink trials. Actual independent-colony Student-t CI/p only if ≥12 real colonies and qualified measurement; no source data, no claim.
- **Locked secondary mechanism checks**: (a) actual original leaf-cue reveals per assigned trial (including all unsuccessful choices), (b) true binary target-choice accuracy/no-choice rates, (c) conditional correctness of first selected U/V given R, (d) the access-mode×wind contrast in intake/query counts. None may replace a null intake primary.
- The normative mathematical 0.5 **expected** saved queries prediction only applies to accurate optimal policies under the independent uniformly sampled 8-world task; realized behavioral gains may be smaller, absent or negative. Query counts are not independent bees; analysis uses colony-level replication.
- The primary causal effect under proper randomization is **access to outcome-contingent querying**, not independently identified animal cognitive optimality, wind-mediated natural selection or generalized evolutionary fitness. An observed difference without actual source-triggered query choice does not support adaptive information access.

## Hard scientific gates / stop conditions

Real experiment only after pilot establishes separate cue comprehension, feasible fixed query and viewing time, nonleaking/identical hardware motor requests, randomized source wind ranges, 3D anemometry, ingestion measurements, and animal-welfare-safe workload. Original source states must be concealed, balanced and auditable. Report every assigned animal regardless of behavior and all missing/instrument failures by arm; do not convert missing data to zero. Precommit actor chooses before root is shown; post-root subject action in contingent arm is actually selected, not programmed by experimenter. Do not optimize wind magnitude, cue threshold, cost, guess penalties, outcome, or responded-bee subsets after effects are observed.

**This is a separate experimental design, not a claim that a living bee has achieved the normative optimum.** PR #85, PR #92, empirical Stage9b–13 results, V5/V6 theory and main remain unchanged.


## Pre-outcome source-independence fix (2026-11-11)
During software review after source-free CI, it became clear that a world-permutation without replacement within each block would leak information about future source R values to a subject learning previous trial outcomes. This violates the independent world assumption in the exact 0.5 EXPECTATION. The original equal-state-per-block assignment was superseded **before any real animal data existed** by independent R/U/V draws with replacement on every trial, while preserving balanced mode × wind allocation. The updated TDD test verifies repeated world states are possible. Therefore the 0.5 value is exact in the generative distribution, NOT required to equal exactly 0.5 in a particular finite generated allocation.
