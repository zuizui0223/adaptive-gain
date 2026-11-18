# Stage83 | Does genuine bee-perceived far/near flower-age information predict Bombus visitation across plants?

2026-11-18 JST. Primary decision: **NOT established as a macroscale species-generalizable effect**.

This document reports one new original-source reanalysis, not four new ecological mechanisms. The original original-code Stage81D has now succeeded after its R system-library repair: genuine archived Ohashi et al. (2015) raw flower-part spectra are read, converted to Apis mellifera receptor excitation under D65 light with a green-foliage background and von Kries adaptation using the real pavo R package. The empirical receptors are a **declared honeybee model**; measured flight detection distance or real Bombus receptor physiology is not available. The algorithm is a mathematical implementation of known bee optical physiology, not a new discovery that flowers change colour.

## Original source and denominators

Ohashi et al. original Zenodo accession https://zenodo.org/records/4942515 (DOI 10.1111/1365-2435.12420); original ZIP 285,933,377 bytes, MD5 d98ddd3b93fb79fdbaaa5eec5818c187, SHA256 860ad9ef71d99efdda441fae00090ddb1dad0145f5c54a04b581b09490e718b7. Stage81D authentic extracted source produces 1,360 spectra from 28 exact-name taxa overlapping the corrected EuPP plant roster and 53 early/late part comparisons, in the R pavo 2.10.0 visual system. Receptor result artifact ID **14409142056**, ZIP SHA256 **9139935f10fbd94a8fb888d807af872c9e5289422249d138fb8a61ac799a0b2a**; real successful job https://github.com/zuizui0223/adaptive-gain/actions/runs/44259368414.

- Of the 28 source taxa, **5** have ≥1 flower part exceeding a hexagon distance 0.09 with the independent per-part permutation test adjusted over 53 parts (BH q < 0.05). These are **not** the 5 positive species in the original 219-species author's own list; exact matching to the author's full classification remains outstanding. The other 23 are not verified genetically colour-invariant species.
- Species-median late-minus-early *green receptor foliage contrast* is negative for **13/28** and species-median late-minus-early *hexagon chromatic foliage contrast* is negative for **18/28**. **12/28** have a nonnegative far-green contrast change and negative near-chromatic change. Some changes are very small and not perceptually significant; the 12 are an unthresholded **descriptive sign phenotype**, NOT functional nectar-guide positives.
- Corrected EuPPollNet source file SHA256 475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617: original 18,798 accepted plant×network-year records, 1,408 accepted source species. Exactly 1,921 plant-network records from the 28 source taxa in 1,040 networks. The eligibility frame has 537 source networks with at least two genuine independent source spectrometer taxa, **selected before** viewing the bee guild outcome. After real species-ranked bee-guild information, 194 within-source networks from **30 original publications** have positive null Fisher information for three continuous traits. Only **23 of the 28** taxa have identified bee observations in these 194 networks. Their repeated appearances across 194 networks are not 194 independent plant evolution origins.

## Four preregistered source descriptors and their sign contrasts

1. FAR (green achromatic receptor): species-median change of absolute green-channel background contrast (late - early).
2. NEAR (chromatic contrast to foliage): species-median change of radial hexagon distance from green-adapted achromatic center.
3. AGE CHROMATIC SHIFT: species-median early-to-late distance between hexagon coordinates, a nonnegative magnitude.
4. DISCORDANCE: purely descriptive 0/1 for green nondecrease plus near chroma decrease, a 12/28 sign flag with no proof that the signal changed enough to be perceptible.

The three continuous descriptors are standardized across the **28 measured source species before any visitor outcome**; the fourth is an unscaled binary flag. Within each observed network, the source zero-effect Bombus vs other bee binomial null-score ratio U/I is calculated from recorded guild counts by species, conditional on original network guild mix. Study-level bootstrap samples original 30 **publications** rather than 31 Study IDs (EuPP habitat-split IDs 23/24/25 are one study). It is NOT an actual fitted binomial effect or a preference for postchange flowers.

| Source optical descriptor | Local U/I score | Publication-bootstrap 95% descriptive interval | Effective original publications by Fisher information | Largest source publication info share | 28-species-vector shuffle 9,999: 2-sided tail | Four-signal maxT familywise diagnostic tail |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| FAR green signed late-minus-early | **-0.1774** | **[-1.3462,-0.0501]** | **1.417** | **83.55%** | **0.7751** | **0.9945** |
| NEAR chromatic signed late-minus-early | **+0.4651** | **[+0.1160,+0.8019]** | **4.799** | **28.75%** | **0.5905** | **0.9316** |
| Chromatic colour-shift magnitude | **-0.8710** | **[-1.2183,-0.6431]** | **4.570** | **38.70%** | **0.3169** | **0.7072** |
| FAR-maintained / NEAR-reduced sign flag | **-1.0671** | **[-2.9323,-0.5666]** | **2.082** | **67.32%** | **0.5485** | **0.9123** |

The source original publication bootstrap intervals, even when excluding zero, do not establish taxon-generalizable effects because source species are repeatedly used across the source publications. The taxon shuffle permutes the WHOLE four-component source-species receptor trait vector among the 28 plant taxon labels, while retaining all real observer-recorded network counts. The maxT diagnostic accounts for having searched four related visual channels. The **species-vector shuffle is not a valid phylogenetic null**: it breaks ancestral covariance and is presented as a *falsification sensitivity* only, not a formal p-value of evolutionary selection. The four observed statistics are not extreme relative to their empirical repeated-taxon placement in those tests, even without phylogenetic clustering.

The full study-native 194-networks score is not a 194-replicate phylogenetic design. For source taxa, the key unit of trait replication is 23 visitor-informative species, with fewer independent genus and clade contrasts. The null-score ratio cannot convert visitor counts into pollinator cognitive learning or physical field-landing behavior.

## Taxonomic robustness

The executable program recomputes the original per-network Bombus fraction after deleting each source genus or plant species; it does not subtract scores with a now-invalid baseline.

- Excluding original *Taraxacum* genus changes the positive near chromatic local ratio **+0.4651** to **-0.0408**; 170 informative source networks remain. This is one-of-26 genus leave-outs, and the far/age associations also shift in magnitude.
- Excluding *Trifolium* reduces the informative network count to only **39** from 12 original publications; this does not add independent plant origins to the remaining data.
- FAR green has only **1.417 effective independent publications** by null Fisher information despite 30 nominal source papers. These are empirical information concentration findings.

## Theory, wind and what is NOT shown

The existing finite deterministic adaptive-gain theorem states the optimal adaptive guaranteed-resolution cost is at most fixed-bundle cost, under declared deterministic observation and cost semantics. It does not imply that real bees perform optimal cue routing. Stage80's noisy payoff example shows that decisions *could* switch when scent reliability, learned prior and landing cost vary; it does not estimate any behavioral mechanism.

Stage82 independently joined Stage79I's weather-eligible width-first frame and Stage81C's raw age-RMS score: 36 actual overlapping weather×age×bee networks from 16 publications with effective publication information count **1.387**. Those strong-wind interactions were unsupported and cannot be recycled as if Stage83's new green/hexagon source traits were measured with true visitor-hour winds.

Wind can improve the distance odor plumes reach under some conditions, while turbulent intermittency and floral motion can degrade recognition and landing. Genuine separate original same-site / time channels are needed to distinguish these directions, not a hypothetical SEM fit using 151 study-month gust exposures and the 28 Japan spectrometer species.

## Next scientific priority / stopping rule

A macroecological signal-ordering claim is NOT currently supported by the four optical associations. The identified observational risk is a sparse **original receptor phenotyping × independent field pollinator guild** intersection, not a lack of variation in spectrometer raw data. Do not mine more arbitrary colour cutoffs for a positive sign.

The next useful scientific step is **new independent source-region recruitment**, preferably field receptor spectra + verified age-positive AND age-negative source phenotypes, *repeated floral census/visit effort*, and independent bee/fly/butterfly guilds; match the real wind / odor / landing modalities at their true original scales. Extend taxon coverage beyond the 28 cross-source exact-name pairs and replicate phylogenetic sister-lineage comparisons before claiming any adaptive signal order. A descriptive source metadata retrieval is not equivalent to a reproducible independent study effect.
