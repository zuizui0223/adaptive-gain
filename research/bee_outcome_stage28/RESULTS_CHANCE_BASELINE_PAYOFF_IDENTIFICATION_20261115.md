# Stage28 — a below-chance unqueried-control anomaly blocks empirical information-payoff identification

**2026-11-15. Source-locked REANALYSIS of existing publicly posted 2026 bumble-bee trial data. No new experimental animals, no empirical claim of evolutionary maladaptation, bee fitness, or Stage24 strategy optimality.** Draft stacked on Stage27 PR #105, all earlier frozen Stage22–27 results, V5/V6 and main unchanged.

## Motivation and provenance

The author-released trial table for He et al. (2026), *Uncertainty-Guided Decision-Making in Bumble Bees*, DOI 10.64898/2026.09.15.751944, publicly resides at https://github.com/Cuixiaojian21/bee_metacognition. Our read-only Stage26 verifier pins:

- author commit 7f886394b4de872ecdb19ca4ea214ec321d5dce9;
- data/4_active_information_seeking_trials.csv;
- actual immutable Git blob SHA1 26259c9071c6d73141d56b9bedd396cab1a04491.

The source table has **19,200 trials, 192 original bee IDs**. Stage28 accepts this table only after Stage26's full original-file identity, row, unique Bee_ID/Trial_ID, treatment and request-semantics checks. The author file is not vendored into adaptive-gain; temporary runner download plus aggregate-only artifact avoids republishing raw records where repository metadata did not declare a reuse license.

Crucially, the author paper separately reports chance-level accuracy in a forced-choice Impossible control. **That is not the same condition** as selectively non-requesting bees in this two-zone information-seeking experiment. We do not claim a direct failure to replicate the forced-choice experiment. The relevant *conditional chance-null* for no-information Impossible trials requires separately verified target-side randomization independently of the bee's request choice.

## Reconstructed source outcomes, not manufactured successes

For Regular trials, "paid" means the bee physically landed on the information platform (and the cue is then provided), while "no cue" means it did not land. For Random_Free_Cue the cue is automatic independently of landing. After-the-cue correctness is available for all Free_Cue trials; it is NOT evidence that the bee paid for a query.

| Difficulty | Regular no cue | Regular paid cue | Auto free cue, NO landing | Auto free cue, landing |
|---|---:|---:|---:|---:|
| Easy | 4,163/5,549 = 75.02% | 555/591 = 93.91% | 555/590 = 94.07% | 906/950 = 95.37% |
| Hard | 1,600/3,242 = 49.35% | 2,662/2,866 = 92.88% | 612/647 = 94.59% | 871/925 = 94.16% |
| Impossible | **183/883 = 20.72%** | 2,073/2,229 = 93.00% | 532/575 = 92.52% | 142/153 = 92.81% |

These figures are descriptive **observed subsets**, not randomized treatment effects of deciding to query. Self-selection, bee-specific difficulty perceptions and hidden final response-side distributions may influence their contrast.

### Missing randomization data: a critical source-quality question

On impossible trials, the task stimuli are described as identical. If the true correct side is an independently randomized and balanced label, and the bee cannot read it from any signal when no cue is provided, success conditional on NOT buying a cue should be near 0.5. The existing author table shows **183/883 = .20725**, not .5, for the Regular/Impossible/no-cue subset.

Per animal, **170/192 Bee_IDs** have below-.5 observed no-cue Impossible accuracy, 12 tie .5 and 10 exceed .5. The equal-bee average is **.20297**. A deterministic 10,000-repeat bootstrap resampling whole original bee IDs gives an illustrative bee-level percentile 95% range of approximately **.182–.233** for the trial-weighted aggregate no-cue success rate. But the CSV contains no independent colony IDs; these are *not* independent-colony population confidence intervals. There is no authority to declare a biological below-chance strategy, deceptive stimuli, or experiment fraud.

The anomaly is persistent when checking trial-number strata:

- trials 1–50: unqueried Impossible 81/442 = 18.33%;
- trials 51–100: unqueried Impossible 102/441 = 23.13%.

The author table **does not contain the randomized true-target side, bee's actual final selected side, or the randomization log**. Those data are needed before estimating a valid chance baseline or using this observational contrast as a cue-acquisition benefit. Selection after uncertain stimuli, an imbalanced target-side process, a coding convention or a previously unreported apparatus cue are alternative explanations that cannot be resolved from this table.

### Conditional benefit is NOT a causal reward effect

The published apparatus describes equal 5 uL volumes of 15% sucrose after a paid correct choice versus 30% sucrose after a nonpaid correct choice; errors are punished with quinine. If one constructs only a *correct-sucrose-concentration proxy* where a correct nonpaid choice has unit payoff and a correct paid choice has half a unit, the action-selected subgroup difference is:

  D(K) = (0.5*p_paid - p_no_cue) + K*(p_paid - p_no_cue)

where K>=0 is the **UNKNOWN** disutility of an error measured in units of the nonpaid-correct sucrose proxy. It is not in the author CSV and cannot be set to zero as if quinine punishment had no cost. Neither concentration nor this toy reward schedule is a measured fitness unit.

| Difficulty | p_paid | p_no_cue | D(0): paid minus no-cue correct sucrose proxy | K threshold for D(K)>0 |
|---|---:|---:|---:|---:|
| Easy | .9391 | .7502 | −.2807 | >1.486 |
| Hard | .9288 | .4935 | −.0291 | >.0669 |
| Impossible | .9300 | .2072 | +.2578 | Positive for any K>=0, **conditional on the currently unverified .2072 no-cue baseline** |

The last row is **especially sensitive** to the source anomaly. If, as a mathematical counterfactual ONLY, one replaced p_no_cue=.2072 with the unobserved chance baseline p_no_cue=.5 while keeping the observed PAID selected rate fixed, the Impossible D(0) would reverse from **+.2578 to −.0350**, and would become positive only for K>~.0814. This is NOT a valid causal adjustment; it is an identification stress test that shows why an unverified no-cue baseline and unmeasured punishment disutility can reverse a biological interpretation.

## Independent QA and audit controls

Stage28 code (research/bee_outcome_stage28/outcome_chance_audit.py):

1. Verifies the immutable public source through the existing Stage26 author-file checker and independently parses outcome branches (0.0/1.0 decimal accuracy indicators).
2. Reconstructs twelve disjoint source/difficulty/actual-landed strata and keeps FreeCue NO-LANDING outcomes separate from voluntary paid requests.
3. Computes source-locked chance-negative-control values, 192 original-bee summaries, 10,000 seeded bee-ID cluster bootstrap intervals, and early/late trial-index controls, always marking colony dependence unknown.
4. Derives *descriptive* reward-proxy penalty sensitivity with explicit unknown K and a labeled UNOBSERVED ideal chance thought experiment.
5. Hard-stops on missing byte identity, source outcome change, missing trial categories, invalid request/correctness branch, missing original bee information, and altered epoch/semantics.

An isolated GitHub workflow runs synthetic-only tests first; downloads the pinned public CSV to a temporary runner file; verifies Git blob SHA; runs source-locked actual analysis; then uploads ONLY derived aggregate receipt and asserts all source-quality and no-biological-inference stop labels. The author's original trial table is not copied into this repository or CI artifacts.

## Real next evidence to request, not an assumed dataset

The **smallest decisive original-source package** is a trial-keyed independent record of (i) randomized correct target side before the bee's first-zone decision, (ii) bee's actual Zone2 chosen side, (iii) first-zone physical landing and cue exposure/flash timing, (iv) target-side randomization schedule/seed, and (v) colony IDs to assess dependence. A blinded external recheck could then test whether impossible unqueried chance really should be .5 or whether conditioning on selection or a source coding issue explains .207. Separately, measured response-time, actual sucrose volume and quinine outcome utilities would be needed to move from this deliberately artificial proxy to net payoff.

**HARD LIMIT:** Stage28 is original-data QA + conditional utility algebra. Neither a Stage24 8D leaf-confusion parameter region nor a causal adaptive-information benefit, interspecies transfer or fitness outcome has been measured here.
