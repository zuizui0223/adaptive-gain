# Stage44 — Sharp original-archive within-bee flight-path selection envelopes

**2026-11-16. Original experimental archive reanalysis, not a newly designed bee experiment or a reproduction of the journal's selected 112-track cohort.**

## Verified source and inference target

- Chang, Crall & Combes (2016), *Journal of Experimental Biology*, DOI [10.1242/jeb.137976](https://doi.org/10.1242/jeb.137976), [original Zenodo 60234](https://zenodo.org/records/60234).
- The authenticated ZIP SHA256 is \`9a2881e5aaf4d7bb9556c9118c45d2e2ed6a2a8b22b80d4d762a5626fdd918ec\`. Original analysis MATLAB source semantics are verified from the original file's pinned SHA.
- The archive contains **157 original xyzpts trajectories**, W0=56 / W1=101, across 28 filename B codes. The Stage41 approach/near-flower physical-window rule yields 142 eligible tracks. The present **paired comparison uses 23 matched B codes, 37 eligible matched B×S×P cells and 83 appearances of eligible original source files within those matched cells**. Among these 37 matched cells, only **five** have multiple eligible original tracks on at least one wind side. Fifteen B codes allow alternative original cell and/or trial choices.
- Sign/estimator: source **W1−W0** near-flower 3-D ground speed (m/s), after one static flower coordinate reference, 1000 fps, 5–7 cm approach and 1.5–3 cm final-near-flower windows.
- Original Stage43 result +0.121429363389 m/s from 100 Hz/three-tag with averaged eligible trials, equal B and equal matched cells.

## Two different sharp envelopes, not statistical confidence intervals

**Regime A, fixed B and matched S/P cell set:** In each matched (B,S,P) cell, select any ONE archived eligible W0 and any ONE archived eligible W1 trajectory, then average cell differences within B and B differences equally. Its exact lower bound is the equal-B/cell average of \`min(windy trajectory speed)−max(calm trajectory speed)\`; the exact upper switches min/max. Since each cell term enters linearly with positive fixed weight and selections are independent across cells, each endpoint is attainable by those finite archived files.

**Regime B, fixed B but one S/P cell per bee:** Allow selecting exactly ONE of the observed eligible matched S/P cells per original B code and ONE W0 and W1 trajectory in that selected cell. Then each bee's lower/upper are its minimum/maximum among cell-level extrema; average equally across the **same original B codes**. This is deliberately a MORE PERMISSIVE observed-file bound and is not guaranteed to match the 2016 paper's fixed experimental design.

| Cutoff and speed definition | Original all-eligible mean (m/s) | Regime A exact [lower,upper] (m/s) | Regime B exact [lower,upper] (m/s) |
|---|---:|---:|---:|
| 50 Hz / three markers | +0.121675 | [+0.114894,+0.129241] | [+0.094200,+0.147160] |
| 50 Hz / central marker | +0.120860 | [+0.113947,+0.128505] | [+0.092917,+0.146615] |
| 100 Hz / three markers | **+0.121429** | **[+0.114666,+0.128986]** | **[+0.093954,+0.146800]** |
| 100 Hz / central marker | +0.120633 | [+0.113735,+0.128272] | [+0.092664,+0.146299] |
| 150 Hz / three markers | +0.121227 | [+0.114483,+0.128770] | [+0.093824,+0.146507] |
| 150 Hz / central marker | +0.120473 | [+0.113591,+0.128097] | [+0.092544,+0.146081] |

**Conclusion specific to this frozen observed archive and this fixed 23-B matched cohort:** every Regime A and even Regime B admissible selection produces a **positive equal-B mean near-flower ground-speed difference** across all six separately specified signal-processing methods. The weakest observed finite-file bound is **+0.092544 m/s** (150 Hz, central marker, Regime B).

At 100 Hz/three markers, 22/23 B codes have a strictly positive *worst*-case Regime A per-B contrast; under Regime B, 21/23 have positive worst-case B contrasts. These facts describe fixed observed source B labels, not population support.

### Sensitivity outcome

Landing-minus-approach *speed-change* is a distinct endpoint and likewise retains positive mean under both selection regimes: at 100 Hz/three-marker, Regime A [+0.126845,+0.147365] m/s; Regime B [+0.080086,+0.202339] m/s. This does not independently measure impact force, failed landing events or pollen delivery.

At 100 Hz/three markers:
- S0 Regime B lower +0.128710 m/s (19 matched B);
- S1 lower +0.066387 (10 matched B);
- P0 lower +0.106432 (20 matched B);
- P1 lower +0.118151 (17 matched B);
- S1/P0 lower +0.046594 (4 matched B), with **zero** alternative eligible tracks in its matched four source cells. This fragile subgroup remains vulnerable to *whole-B deletion* (Stage43) despite having no within-cell track-selection uncertainty.

All subsets overlap in original B identifiers and are NOT independent replications.

## Critical source-selection ceiling

- Stage44 does **NOT** prove the original 112 publication-selected trajectories are recoverable. In the published Results vs archive counts, four P1/W0 primary-condition trajectories cannot be matched under a strict one-to-one filename correspondence; the original paper's results, Fig. 1 caption and paired t-test denominators also require careful reconciliation (Stage43).
- The Regime A/B envelopes are conditional on **keeping the same 23 archive-matched B codes**, their current eligible source trajectories and the registered 5–7/1.5–3cm inclusion windows. They do **not** protect against original-author selection of different study animals, other unarchived trials, a different primary-condition roster, source B misidentification, arbitrary nonmatched cells, or changing the trajectory eligibility rule.
- Regime B is an outer sensitivity design, not a statistical confidence/credible interval. Extreme selection is not a randomized biological intervention and does not yield a population p-value or colony-independent inference.
- There is **no** actual conditional landing success (the original archive contains only successful tracked landings), randomized floral odor on/off comparison, natural flower community, per-visit pollen deposition, seeds or plant reproductive fitness. Do **not** multiply Crall scent-bait low-speed visitation with Chang headwind motor speeds as a measured net pollination effect.

## Source/CI reproducibility

- Implementation: \`within_bee_trial_selection.py\`, with independent exact finite-choice optimizer and existing source-locked 3D trajectory parser.
- Ten unit tests on wholly invented numerical rows, including an **independent exhaustive enumeration oracle** of the finite within-B/S/P choices and source-safety STOP.
- Original-source CI [run 43828238773](https://github.com/zuizui0223/adaptive-gain/actions/runs/43828238773) **SUCCESS**, source aggregate artifact ID **14207153862**, checksum **sha256:775b02a3716b95a8b7dd32f5451e3e6872c4c2b78640de336c060fb89bd9791d**. Original raw ZIP and exact XYZ rows remain ephemeral in Actions; only aggregate JSON is archived.
- Check final branch-head full Python 3.10/3.11/3.12 test matrix separately before asserting final software acceptance. Keep Draft PR, do not merge into main.

**Scientific transition:** the known archived Bombus headwind-speed effect is robust to several specified algorithmic, whole-bee deletion and within-bee experimental-file selection decisions. The limiting factor for a genuinely new ecological claim is no longer this motor-speed sign, but the absence of paired *discovery → approach → successful landing → pollen transfer* measurements in the same animals, flowers, wind conditions and treatment assignments.
