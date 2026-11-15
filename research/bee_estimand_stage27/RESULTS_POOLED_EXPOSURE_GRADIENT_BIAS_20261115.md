# Stage27 — outcome meaning changes the apparent uncertainty-response gradient

**15 November 2026. New reanalysis of an existing PUBLIC 2026 author trial CSV, not new animals. Source-free QA and independently sampled existing bee identifiers, NOT independent colony replication.** Stage27 is stacked on Stage26 PR #104 and leaves all previous frozen Stages22–26, manuscripts and main untouched.

## What is being estimated — distinguish the two estimands

He et al., *Uncertainty-Guided Decision-Making in Bumble Bees* (2026 bioRxiv preprint; DOI 10.64898/2026.09.15.751944), experimentally interleaved Regular trials (one **paid, voluntary** information-platform landing for a cue, lower sucrose for correct choice) with Random_Free_Cue trials (cue **automatically** flashed before the decision regardless of landing). Its author-public source is Cuixiaojian21/bee_metacognition, pinned commit 7f886394b4de872ecdb19ca4ea214ec321d5dce9, CSV data/4_active_information_seeking_trials.csv, Git blob SHA1 26259c9071c6d73141d56b9bedd396cab1a04491. We do NOT copy author raw CSV into the adaptive-gain git history or CI artifacts.

The published source repository contains distinct analysis scripts:
- c_6_1_active_info_seeking_glmm.R fits **Info_Requested ~ Difficulty + (1|Bee_ID)** to all trial types without filtering Trial_Type, and therefore estimates a mixture of voluntary paid action and automatically presented access;
- c_6_3_Regular_info_seeking_glmm.R **correctly** restricts to Regular trials and models voluntary information requests;
- c_6_5_Random_Free_Cue_info_seeking_glmm.R explicitly models actual platform landing with Difficulty × Trial_Type.

This research does NOT claim that all of the authors' analyses are erroneous. It estimates the quantitative consequence **of interpreting the pooled Info_Requested GLMM and pooled descriptive means as if they represented paid voluntary information requests**, an estimand mismatch.

## Reproduced empirical counts

| Difficulty | Regular paid landing | All-trial Info_Requested flag | Auto free-cue landing |
|---|---:|---:|---:|
| Easy | 591/6,140 = 9.63% | 2,131/7,680 = 27.75% | 950/1,540 = 61.69% |
| Hard | 2,866/6,108 = 46.92% | 4,438/7,680 = 57.79% | 925/1,572 = 58.84% |
| Impossible | 2,229/3,112 = 71.63% | 2,957/3,840 = 77.01% | 153/728 = 21.02% |

Across all difficulties there are exactly 15,360 Regular trials with **5,686 actual voluntary paid requests**, plus 3,840 Random_Free_Cue trials whose Info_Requested flag is always 1 even though the cue was delivered automatically. A naive sum reports **9,526 flags**, of which **3,840=40.31%** belong to automatic-cue conditions and must NOT be interpreted as paid animal-initiated information acquisition. This count is separate from the Stage26 observation that **1,812** free-cue trials have Info_Requested=1 despite NO platform landing; even those free-cue bees that landed did NOT need to request a cue to receive it.

**Main pooled-estimand contamination:**

- True Regular Easy→Impossible gradient: 2,229/3,112 minus 591/6,140 = **+0.620005568** (62.00 percentage points).
- Naive all-trial flag gradient: 2,957/3,840 minus 2,131/7,680 = **+0.492578125** (49.26 points).
- Gradient bias when interpreting the latter as the former: **−0.127427443**, or **20.55% attenuation** relative to the Regular gradient, on a trial-weighted descriptive scale. This is an estimand-bias calculation, not a fitted causal treatment effect or a refutation of the valid Regular-only analysis.

## Independent bee-unit sensitivity, not trial pseudoreplication

All 192 original Bee_IDs have both treatments and all three difficulty categories. Compute each bee's own (Impossible−Easy) gradient for Regular paid landing, its own invalid pooled Info_Requested gradient, and their difference, then give each bee equal weight. The reconstructed means from the public source are:

- Equal-bee Regular paid gradient: **+0.61840526**.
- Equal-bee naive pooled-flag gradient: **+0.492578125**.
- Equal-bee contamination difference: **+0.12582714**, positive in **186 of 192** bees.
- Equal-bee negative-control platform-landing interaction, (Regular Impossible−Easy) minus (Free_Cue Impossible−Easy): **+1.01837559**, positive in **191/192** bees. A difference-in-differences of two probability gradients may legitimately exceed 1; it is NOT a measured fitness multiplier.

A prespecified deterministic **10,000-replicate bee-ID cluster bootstrap** resamples the 192 bee identifiers, with all each individual's trial outcomes intact, reporting percentile 95% intervals of the equal-bee means and the naive/regular gradient retention ratio. This avoids pretending that 19,200 trials are 19,200 independent biological replicates. **Independent colonies cannot be identified in the author CSV**, so the intervals are sample-bee-level descriptive sensitivity intervals conditional on the bee-as-unit assumption. They are NOT colony-level independent biological population confidence intervals.

Additional deterministic checks: disjoint early (trial number ≤50) versus late (>50) trial windows, where both estimates are recomputed from actual trial strata; and leave-one-bee-out ranges for each equal-bee contrast. Trials with automatic free information always remain separate even if the bee happened to land.

## Mechanism of the contamination

For difficulty d, write w_d for the proportion of automatic Free_Cue trials. Their Info_Requested is coded as 1 regardless of behavior. In the same author table:

P(Info_Requested=1 | d, all) = (1−w_d) × P(paid landing=1 | d, Regular) + w_d × 1.

The factor w_d is approximately 20% across difficulty categories, and Free_Cue stimuli were randomized in the author's reported methods. This is why the pooled flag gradient is mechanically flattened: it measures *experimental cue exposure plus behavior*, not self-initiated paid information use. The equation holds at the sample-stratum level without requiring any cognitive theory. It also clarifies why an alternative pooled landing GLMM with trial-type interaction is a different, correctly defined estimand.

## Relation to adaptive-gain's mathematical stages

This dataset does demonstrate previously published, difficulty-conditioned paid-cue acquisition and a useful randomized free-cue control. It does **not** contain the six class-specific Stage22–25 Z/U/V recognition confusion rates, source-specific information selection, learned q, independently identified normalized cost c, or the Stage24 randomized contingent-first-query-versus-precommit-first-query comparison. It would be a serious category mistake to feed the 19,200 source trials into the Stage24 8D rectangle and assert an empirical +0.01008 optimal-information reward. No observed fitness or pollination-rate changes are measured.

## Software design and proof receipts

Code: research/bee_estimand_stage27/estimand_contamination.py. It first calls the frozen Stage26 source-byte-and-semantics auditor. Then independently reconstructs each difficulty/treatment, equal-bee contrast, deterministic XorShift32 resampling, per-bee leave-one-out ranges and early/late sensitivity. All outputs are derived aggregates and source hashes; the original author CSV stays in a temporary runner input directory only.

Tests: research/bee_estimand_stage27/test_estimand_contamination.py — invented local CSV fixtures only, no source attribution to fake bees. The dedicated GitHub Actions job pins, downloads and exact-Git-SHA-checks the author's public CSV before producing and validating aggregate JSON. The three-version whole-repo matrix is an independent CI gate. No PR is merged.

**Biological STOP:** This reanalysis changes how a published variable should be interpreted. It does not estimate cognition, physiological net payoff, reproductive fitness or the optimality of Stage24's eight-world Bayes policy. A primary experiment would still require independent original colonies and blind source-class sensory responses with measured costs and actual conditional versus precommit source requests.
