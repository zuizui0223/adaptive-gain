# Stage13 — Social-cue flower visits need not cluster in time

**2026-10-30 | Original publisher-verified Smolla et al. 2016 visit-order reanalysis | Frozen one-sided positive-cue-state-persistence hypothesis NOT SUPPORTED**

## Main result and inferential limit

On the author-original independent-source tagged bumblebee data, actual visitation orders have **no positive cue-state persistence beyond the exact original flower-use marginals and first-choice condition** under the frozen null. They have slightly *less* cue-state persistence than the source-conditional shuffle mean, but that contrast is **not a prespecified test of negative anti-persistence**.

| Frozen endpoint, original source 2016 | Value |
| --- | ---: |
| Test-stage source-verified individuals | 57 |
| Source-original test flower visits | 1,308 |
| Genuine between-distinct-flower switches | 1,233 |
| Distinct original colonies, equal-weighted | 3 (a=4, b=35, c=18 individuals) |
| Original cue-state (cued/cueless) persistence among switches | **0.4838662979909009** |
| First-choice fixed, original flower-use counts retained null mean | **0.5096104660789736** |
| Actual minus null mean | **−0.025744168088072727** |
| Frozen null 5–95% empirical Monte Carlo range | [0.47912337073786393,0.5403116215195489] |
| Fixed one-sided conditional p for **greater** cue-state persistence | **0.918** |
| Source-null permutations | **999** (seed 20261030) |

All three source colony differences actual−null are negative: `a: −0.05552526342990327`, `b: −0.013400571673337858`, `c: −0.008306669160974112`. These descriptive signs do not establish an independent biological-population effect with only 3 colonies, one represented by just 4 bees. The full original test sample was eligible; **zero excluded animals** from this Stage13 outcome. Original `test_easy` 29 tagged bees, 725 visits; `test_diff` 28 tagged bees, 583 visits. The original 57 `dummy_last` training observations with 498 visits were used to verify pairing but never pooled into the test-order outcome.

## Biological question and comparison

Smolla, Alem, Chittka & Shultz (2016), Biology Letters, DOI 10.1098/rsbl.2016.0188, experimentally studied social flower cues under variable reward environments. The source authors' reward-dependent copying effect, particularly initial choices, **is previously published and is not claimed as our novel result**.

Here a distinct, limited question was frozen **before running any Stage13 test outcome**: Does an animal's source visit sequence retain an excess tendency to move from a cued flower to another cued flower, or from an uncued flower to another uncued flower, after preserving which original flowers the animal visited and its first choice?

For every original test bee, classify each of 12 source flower IDs as cued (4 original positions) or uncued (8 positions). Count **only original consecutive transitions to a different physical flower**. Calculate per-bee `A = same_cue_state_switches / all_real_switched_flower_pairs`. Original 57 bee scores are averaged with **equal weight per bee within each source colony, then equal weight for each of the three colonies**, not weighted by visit-event count.

For 999 permutations, **the first original flower visit is held fixed**, and the remaining original visit identities are shuffled within **the same tagged bee**. This preserves exact original flower-use frequencies, source cues, source group labels, actual first-choice preference, bee counts, and source colony identities; the ordering of later visits is the only perturbed object. One-sided fixed null `p=(1+number(null>=actual))/1000`. No group, flower, animal subset or shuffle strategy was selected after seeing the result. Every shuffled sequence remains a **statistical surrogate, not a physically possible randomized flight path**.

## Provenance and the source-grade audit

Original archived Dryad DOI https://doi.org/10.5061/dryad.3jb68, legacy provider version 19480. Original `beeLandings.csv` 9,462 bytes, MD5 `35a9d6c258e001f7c8222d90c84dfee6`, SHA256 `248b8257ac4a756a16704eaedbabd3909f24be1d8bd6d4a64e6bcbb100ee8e65`. Original author statistical R script archived alongside it, MD5 `9d7bc353b2890c61f10626db42d219b7`. All compare exactly with the original provider metadata.

The early source-gate attempt returned HTTP401 for individual-file legacy API; after diagnosis, a provider-authored version ZIP was fetched, and **each original member was verified against original file hashes**. No arbitrary alternate file was used.

Native source includes 114 rows with one `dummy_last` phase and one `test_easy`/`test_diff` per bee, and source `landed` contains full integer ordered flower IDs; `cue` is source flower-index list of four locations out of twelve. The native original `reward` for all test rows is `na na`, not observed individual test reward; all 57 source bees have a unique matched test sequence. Original `firstLanding` and `lastLanding` have unresolved time unit/format inconsistency (one `5:47` value); **NO time/latency/energy measurement is imputed or used here**.

No individual original visits, landing sequences, cues, or source original data rows are committed to Git. Derived aggregate colony/statistic receipts live in GitHub Actions and machine-readable report.

## Scope

**Defensible:** in one historical laboratory social-cue experimental source, the full test visit *order* does not exhibit an excess of cue-state-same transitions above what would follow from the source's individual flower preferences and first choice. Previously published first-choice copying need not entail new *serial route ordering* evidence; such routes can be consistent with the same visit-frequency margins.

**NOT established:** a universal absence of social copying, an anti-social or alternating sequence tendency, a motor or memory mechanism, ecological wind effects, sensory cue acquisition timing, benefits in fitness, `C_A<C_F` or general decision-topology laws. Spatial flower geometry is not independently randomized by this permutation; it may itself explain serial transitions. The source provides 3 colonies, not a population-level repeated field study.

### Frozen source/code receipts

- [Original historical source+real 999-shuffle execution CI #41037702916](https://github.com/zuizui0223/adaptive-gain/actions/runs/41037702916), **SUCCESS**, 15 source+method tests, original source hashes, 57-bee training/test QA and original real test-order result.
- [Original source order protocol](https://github.com/zuizui0223/adaptive-gain/blob/analysis/bee-social-cue-sequences-20261030/research/bee_social_stage13/PROTOCOL_FROZEN_SEQUENCE_TEST_20261030.md).
- No retuning of permutations, first visits, species/cue types, visit cutoff, repeat-visit handling, colony weights, or selection after seeing the result.

**Research decision:** Stop retrospective cue-order searching in this source. The 2016 authors' social copying and our conditional route-order test measure different endpoints. To establish causal information-query chronology or evolutionary payoff, use the independently specified prospective experimental **cue order × physical wind × measured sucrose** protocol in [adaptive-gain PR #85](https://github.com/zuizui0223/adaptive-gain/pull/85). No animal tests in that PR have occurred. Original Stage9b/10/11/12 and frozen V5/V6/main remain unchanged.
