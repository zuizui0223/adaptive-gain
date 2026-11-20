# Stage102 — Original WFO floral diameter extraction quality gate, not a wind result

**2026-11-20 JST.** This is a stricter independent syntactic recheck of the source-original full botanical prose. It is NOT manual trait validation, organismal sensory response, regional wind association, or a mechanism.

## Why and fixed source sample

The authenticated Stage100 original Flora of China/Flora of North America plant treatments yielded 237 WFO textual **whole-flower diameter candidates** plus 58 **corolla-only width** candidates, across 27,899 species with botanical prose. Stage101 exact-match union with AusTraits v7 measured-source flower diameter (104 accepted native species) found only FOUR shared species; the resulting 337 source-available species are not all measured. In the 37 geographically unchanged mainland holdout regions, 20 regions have at least 10 source-available mixed-grade size species, but manual quality validation is still absent.

This task freezes the original inputs, before examining any associated gust or floral effects:
- Original Stage100 complete 295 WFO candidate species ledger ZIP, source SHA256 **06c370061a4c069038aaf11ecd59a423fb00cb051db6ec67632e316ce9d2ebd4** and artifact 14541288164.
- Original Stage98B 72 mainland contact-free training and 37 original holdout geography ZIP, SHA256 **8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7**.
- Original full WFO eFloras China and North America DwC-A archives SHA256 **4c0b89280efdcfd0ef8dc753cca5d63566ddf8c34542b0bb4a78cdce799b63a9** and **0757eb55f2e844383d34650ea3aa577d15c2210f3893561b6694559dd9aa02e1**.
- Official WFO Plant List June 2026 taxonID-to-exact accepted species names release, Zenodo author original MD5 **0e4486945cd9f7af548ca87eb9a870ed**.
- NHM 59,369 source trait records and Kew WCVP original 55,775 strict accepted-native species and 367 source TDWG3 floristic regions; these include islands in the global original source but Stage98B's strict mainland eligibility remains fixed.

## Independent source specificity grammar

Stage100's original lexical grammar is replayed unchanged against full source descriptions and MUST reproduce the 237 whole-flower/58 corolla-only candidates, or the workflow fails. A SECOND, more conservative grammar then uses:
- explicit whole-flower subject and diameter/across/width dimension within 40 characters of that subject;
- no intervening reference to corolla tubes, petals, sepals, bracts, capitula, heads, clusters, leaf/fruit, peduncle, or inflorescence;
- unambiguous numeric mm or cm value, not an interval/range, negative or implausible measurement;
- same original species no more than 1.5-fold disagreement between strict-source descriptions.

The result is **syntax retention sensitivity**, not independently estimated precision. Values from corolla-only passages are never promoted to whole-flower display diameter. Missing/unmentioned values are NEVER small or zero flowers. More stringent filters can reject true positive floral dimensions, so neither loss nor retention directly proves correctness.

A deterministic, prelabelled-by-grammar 15-species review queue is selected by original species name SHA and fixed salt, stratified over six strict, six original-only/flagged, and three corolla-only candidates where available. Original source full treatment text is NOT redistributed. The GitHub Actions source-read step prints at most 15 minimal snippets of up to 62 characters to aid a later manual source review, with review flags remaining explicitly NOT_YET_DONE. Hashes and source identity, but not raw prose, are archived. An independent, botanical-domain human review is required to estimate positive predictive value of the original 237-source parser; the current algorithm's own replay is not a gold standard.

## Genuine first source audit found an unhandled interval encoding — corrected

In original source-verified Actions #44660691765, the preselected short original flora phrases included botanical intervals written with two ASCII hyphens (example: "8--9 cm in diam.") and phrases that designate an upper limit ("to 2 cm in diam."). Stage100's original detector, and the first Stage102 stricter grammar, could silently take the upper endpoint as a singleton measurement. This contaminates the interpretation of some source size candidates even where the botanical organ is correctly identified.

**Fix before accepting empirical result:** the stricter parser now detects double hyphen, regular hyphen, en dash, em dash, tilde, "to", and explicit upper-limit expressions as bounded measurements, NOT single point diameter. A size interval may later be retained as [minimum, maximum] original evidence in a different interval-censored model; its maximum must not be treated as a species median. The new tests reproduce the observed double-hyphen issue and require proper rejection without losing genuine one-number diameter evidence.

The initial strict candidate count from the pre-fix Actions run is NOT a validated final figure. The original Stage100 237-source candidate ledger is retained for provenance rather than silently rewritten. Re-run original authentic WFO and freeze corrected support counts without reading any wind-cue regression.

## Scientific decision gate

The two legitimate outputs are (1) the proportion of original WFO whole-flower textual *candidates* surviving this new strict parser and (2) mainland 72/37 source coverage and heldout-only species count under that filter. Do not describe either as a corrected biological rate or evidence that strong wind changes long-distance floral signal allocation.

Even after this source audit, broader regional climate inference requires the 1991–2020 opening-month gust exposure area-integrated over the true mainland TDWG3 land portion, not just the Stage95/97 50 point samples, and independent CDS 10fg clock/source checks. Differences in floral description detail and plant phylogeny remain confounders, and actual nectar guides, volatile plume dispersion, bee training/learning and landing success are not recorded.

Source code: research/floral_macro_stage102/authentic_WFO_diameter_strict_quality_audit.py and its unit tests; GitHub workflow floral-stage102-WFO-wholeflower-size-quality.yml.

**Status:** Actual result unknown until original GitHub Actions source validation succeeds.
