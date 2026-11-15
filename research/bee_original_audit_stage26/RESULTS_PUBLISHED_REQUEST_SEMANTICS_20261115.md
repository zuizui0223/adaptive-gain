# Stage26 — re-auditing actual information access versus animal-initiated requests in published bee trials

**2026-11-15. Read-only reanalysis of an existing public author trial CSV, not new bees or a Stage24 biological test.** This Draft is stacked on Stage25 PR #103 and does not change previous Stage22–25 frozen results, V5/V6 or main.

## Source provenance and scope

He et al., 2026, *Uncertainty-Guided Decision-Making in Bumble Bees* (bioRxiv 10.64898/2026.09.15.751944) reports an uncertainty-guided, sucrose-costly information-request experiment with Bombus terrestris. The author-linked public repository is:

https://github.com/Cuixiaojian21/bee_metacognition

The public author repository lists trial-level data in data/4_active_information_seeking_trials.csv, and the requested dataset consists of 192 bee labels and 19,200 trial records. To make the reproduction independent of mutable main, Stage26 pins author commit 7f886394b4de872ecdb19ca4ea214ec321d5dce9 and verifies the CSV's Git blob SHA1 26259c9071c6d73141d56b9bedd396cab1a04491 before reading any rows. The pinned URL is:

https://raw.githubusercontent.com/Cuixiaojian21/bee_metacognition/7f886394b4de872ecdb19ca4ea214ec321d5dce9/data/4_active_information_seeking_trials.csv

The source repository did not advertise a GitHub license when checked. Stage26 NEVER vendors this full author data into adaptive-gain or republishes the raw trials, and only emits derived audit summaries. Matching bytes verifies **public file identity**, not first-hand experimental instrumentation or the conditions in which original animal responses were collected.

## Core QA finding: source flag and actual voluntary request are different observables

There are two treatments. In Regular trials, landing on the Information Request platform triggers an informative cue and a reward discount. In Random_Free_Cue trials, the visual cue is supplied automatically; the bee may or may not land on the platform but this landing cannot be identified with paying to acquire information when the cue has already been supplied.

The public table includes both Info_Requested and Actually_Landed_On_Platform. Crucially, their semantics differ by treatment:

| Trial group | Trials | Info_Requested=1 | Actual platform landings | Info flagged but NO landing |
|---|---:|---:|---:|---:|
| Regular, Easy | 6,140 | 591 | 591 | 0 |
| Regular, Hard | 6,108 | 2,866 | 2,866 | 0 |
| Regular, Impossible | 3,112 | 2,229 | 2,229 | 0 |
| Random_Free_Cue, Easy | 1,540 | 1,540 | 950 | 590 |
| Random_Free_Cue, Hard | 1,572 | 1,572 | 925 | 647 |
| Random_Free_Cue, Impossible | 728 | 728 | 153 | 575 |
| TOTAL | 19,200 | 9,526 | 7,714 | 1,812 |

Every one of 3,840 Random_Free_Cue records has Info_Requested=1, but 1,812 (47.19%) show NO physical landing. Across all treatments, treating this flag as a genuine animal-initiated request would thus count 9,526 apparent requests when there were 7,714 actual platform landings; the treatment-specific inconsistency is exactly 1,812 records. **Even the 2,028 platform landings under Random_Free_Cue cannot be counted as PAID self-initiated information queries, because information was automatically provided.**

Operational rule frozen before further empirical calculations:

- Strict paid animal-initiated information requests: Regular AND Actually_Landed_On_Platform=1, **N=5,686**.
- Random_Free_Cue trial Info_Requested indicates experimental information exposure/availability in this public CSV. It is **not** a general self-request behavior outcome; all 3,840 such trials must be excluded from strict paid-query counts. Trial_Type and actual landing must be retained together.

These are observational coding facts, NOT a contradiction of the published experiment's reported uncertainty-related request behavior. The paper separately discusses automatic free-cue controls.

## Behavioral sanity check: landing rates reverse in the impossible control

| Difficulty | Regular landing fraction | Random_Free_Cue landing fraction | Equal-bee mean within-bee free-minus-regular landing difference |
|---|---:|---:|---:|
| Easy | 591/6140 = 9.63% | 950/1540 = 61.69% | +0.51970 (192 paired bees) |
| Hard | 2866/6108 = 46.92% | 925/1572 = 58.84% | +0.12403 (192 paired bees) |
| Impossible | 2229/3112 = 71.63% | 153/728 = 21.02% | −0.49868 (192 paired bees) |

The source-provided Random_Free_Cue control shows much less platform landing in Impossible trials, consistent with the paper's qualitative interpretation of a task-dependent information benefit. These are DESCRIPTIVE reanalyses of the published author data, NOT newly observed animals, independently randomized treatment estimates, or proof of subjective metacognition.

All 192 bee identifiers have both conditions in all three difficulty groups; bee-level means are reported to avoid treating individual trials as independent experimental animals. The source CSV contains NO independent colony IDs. Consequently, no colony-robust population p-value or causal ecology/fitness inference is claimed here.

## Relation to Stages22–25 and hard scientific inference limit

This author CSV offers genuine *treatment-specific source evidence* that the voluntary platform landing and automatic cue exposure must be distinguished. That is directly relevant to the Stage15–25 animal-origin SKIP/request source gate. It does NOT supply independently measured six class-conditional Z/U/V true0/true1 confusion rates, a learned branch prior q, a calibrated matching normalized paid-information cost c, or a randomized test comparing the Stage24 precommit and contingent *first-source* policy classes.

Thus the following is rigorously forbidden: plugging the published 19,200 records into Stage24 and calling its 8D +0.01008 lower bound empirically supported. No forced reinterpretation of Random_Free_Cue as voluntary paid requests. No claim that an externally published behavior result is a new experiment conducted in this project.

## Exact software receipt and reproducibility

Stage26 source-free unit tests use ONLY invented local toy CSV data, verify fail-closed missing source or changed blob digests, duplicate trial/bee-session handling, mutually exclusive outcome columns and source-specific treatment semantics. The dedicated GitHub Actions job downloads the pinned author CSV into a temporary runner path, checks its Git blob SHA1, runs the read-only audit and uploads **only a compact numeric summary**. Nothing from the author raw CSV is checked into adaptive-gain or uploaded as an artifact.

Command (a prior manual download of the pinned author CSV is required):

    cd research/bee_original_audit_stage26
    python -m unittest test_audit_author_request_semantics -v
    python audit_author_request_semantics.py --input /path/to/4_active_information_seeking_trials.csv --out stage26_author_source_receipts

A missing local CSV returns NO_GO_PUBLIC_AUTHOR_CSV_NOT_PROVIDED. The output receipt explicitly records that all behavior was observed in previously published work, original instrumentation cannot be independently authenticated from a CSV, colony IDs and six class channels are missing, and **Stage25 eight-parameter empirical confidence validation remains NO_GO**.

**Next genuine empirical step:** per-original-bee and independent-colony blinded true-class cue trials with learned-prior and paid-cost calibration, followed by observed source choice and randomized realized-payoff comparison. The present public data do not fill that gap.
