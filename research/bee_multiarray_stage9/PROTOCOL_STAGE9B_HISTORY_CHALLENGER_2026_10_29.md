# Stage 9b: A source-heldout first-order route-history challenger to transferred direction

**Protocol fixed 2026-10-29, after PR #84's positive external-direction result but BEFORE this Stage 9b source outcome.** This is a **post hoc robustness/falsification test**, not a fresh independent confirmatory discovery. Never revise controls after scoring. The parent study's original data, published coordinates, trained λ, heldout bouts and external κ stay fixed.

## Scientific question and estimand
Does the **2019-frozen incoming-chord direction coefficient κ=1.0** still improve 2017 next-*different*-flower predictions after accounting for a bee's **earlier learned first-order physical flower transitions B→C**? A positive answer tests predictive information beyond an individual route-transition baseline, not sensory-order causality or observed flight heading. A nonpositive result bounds the earlier PR #84 claim: external direction may be proxying learned B→C structure.

## Exact original study / population
Klein et al. (2017), DOI 10.1038/s41598-017-04919-8, original publisher S1/S2 SHA256 and original Figure1 JPEG hash identical to PR #84. Exactly **29 tagged bees, two colonies, three sequential four-flower arrays, 20 original bouts per bee×array**, source structural exclusions **16 incomplete external nest boundaries + 4 internal nest cases**, never interpolated. Train only original numbered bouts **1–15**, test **16–20**, no replenishment of excluded bouts. Test ONLY actual within-bout triplets A→B→C with A≠B and B≠C. Parent fixed test totals: 608 / 687 / 663 by source arrays 1 / 2 / 3. No synthetic source events or alternate flowers.

## Frozen models and fair contrasts
All models use four source flower identities and **only three real alternatives C≠B** at each prediction; all probs normalized on identical alternatives; α=0.5, original geometric λ chosen **from earlier source bouts only** using the *unchanged parent PR #84 implementation* (λ per array 0.50/0.25/0.25 per metre). Original Figure1 digitization ±10cm is explicitly approximate.

- **Mgeo**: original bee's earlier visit-frequency prior × exp(−λ distance(B,C)).
- **Mturn**: normalized Mgeo × exp(κ cosine(A,B,C)), where **κ=1.0 from independent Pasquaretta 2019**.
- **Mhistory**: shrink per-bee original training *switched* transition counts N(B,C) toward **Mgeo** by **β=5 pseudocounts**, i.e. P(C|B, switch)=[N(B,C)+5 Mgeo(C|B)]/[sum_(D≠B)N(B,D)+5]. This β is the frozen historical-source Stage5 β, **not selected on 2017 test outcomes**. This model has NO incoming A.
- **Mhistory+turn**: normalized Mhistory × exp(κ cosine(A,B,C)), same externally frozen κ.

Primary: heldout **Mhistory NLL − (Mhistory+turn) NLL**, weighted equally **by individual bee within colony, then by the two original colonies**, reported separately for each array. Also report previous Mgeo vs Mturn, Mgeo vs Mhistory, and Mturn vs Mhistory+turn, 29 source bees per layout, source triplet totals, and all six colony×array contrasts. Exact parent Mgeo/Mturn NLLs must reconcile numerically to existing source receipts within 1e-9 before Stage 9b claims.

## Frozen challenge and null
199 seed=20261029 outcome-preserving incoming-A permutations *within bee×current flower B×source array*, retaining all genuine B→C outcomes, original bouts, trained counts, λ, and κ. Report actual-primary gain, shuffled mean, actual-minus-shuffle and (1+#null≥actual)/200 for each array. First verify ≥100 exchangeable true triplets and ≥10 original bees with ≥5 exchangeable entries, following PR #84. These are **observational conditional label permutations, not feasible altered animal flights, nor independent experimental replications**. Repeated bees across the three arrays and two source colonies restrict inference.

The **descriptive transfer gate** is positive primary gain in **all three arrays AND each of six colony×array means**. Report any failures explicitly; do not replace with pooled or cherry-picked subset. The conditional null is an additional diagnostic, not a substitute for this gate. All endpoints are fixed here before new source scoring; this is still a post-hoc challenger chosen after the direction signal was observed.

## Strong safeguards
- No original test destination C contributes to prior, Markov counts, geometry λ selection, κ selection, β selection or exclusion choices. Refit histories only on earlier genuine switched pairs, never source test.
- Source quality failure, changed original totals, new sample exclusions, mismatched parent score, invalid plotting hash, data access failure, nonpositive probabilities or inadequate source support => fail closed with NO_GO.
- Use source-backed CI to download original publisher files in ephemeral runner; no individual raw bee trajectories in Git.
- A persistent directional prediction is **not** proof of directional inertia, learning, wind use, cue acquisition chronology, interspecific information use, ecological competition or fitness. Changed landmark layouts have fixed order 1→2→3; only two independent colonies.
- Freeze the outcome on first source-verifiable execution; do not retune β, κ, lambda grid, subset, permutation units or exclusions after seeing the result. No edits to main or V5/V6 manuscript.

Expected artifact: source-hashed derived summaries and per-bee scores, separate from parent PR #84; dedicated source-read-only CI and focused tests.
