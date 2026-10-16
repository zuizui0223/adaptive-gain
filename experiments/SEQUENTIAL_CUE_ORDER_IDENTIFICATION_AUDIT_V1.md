# Ordered cue acquisition: the static calibration boundary

**Status:** Supporting assumption audit for adaptive-gain PR #68, not a new theorem family, species-level fitness result, or observation of a pollinator. The pre-existing V5/V6 submission surfaces are untouched.

## Question

PR #68 established that, **if acquisition does not alter the underlying cue readouts**, matching every world-conditioned pairwise observation distribution suffices for optimal decision payoffs when the animal can acquire at most two cues. Does a calibration performed on separately or simultaneously presented cues still suffice when an earlier inspection changes the distribution of a later readout? **No.** Such calibration estimates a different intervention. A serial experiment must identify the ordered observation process.

## Sequential information process and comparison

Let `w` be the fixed ecological state and `h=((j1,z1),...,(jk,zk))` the actor's **ordered history of requested cues and perceived responses**. A sequential sensor has an observation kernel

`kappa_j(z | w, h) = P(perceive z from cue j | latent world w, preceding requested cues/responses h)`.

The actor sees `h` and may either stop and choose a target (or abstain), or request another cue within its resource budget. The fair nonadaptive comparator precommits an **ordered cue schedule** before observing the first response; its final target choice can still depend on the accumulated evidence. Acquisition uses budget but imposes no additional utility penalty, so it is never necessary to force a precommitted schedule to use all possible queries. Comparisons always use the same observation kernel, prior, targets and payoff map. Do not compare an adaptive actor using the true kernel with a fixed actor deliberately kept ignorant of it.

The static sufficient-data proposition holds when all `kappa_j` are induced by one nonreactive world-conditioned joint readout vector; under that assumption path probabilities equal appropriate unordered-subset marginals. Under an *order-dependent* kernel the same inference from passive simultaneous measurements is not licensed.

## Explicit two-world, three-cue experiment

Consider equally likely target worlds `w=0` and `w=1` and three unit-cost cues, with no more than two acquisitions:

- **Context cue A (query 0):** an independent fair binary observation. It contains **zero information about the target**.
- **Target cues B/C (queries 1/2):** when measured alone or first, each reports the correct target with probability `3/4`, independently of the other in a separate passive simultaneous calibration.
- **Stable environment S:** when any cue is acquired second, its readout law remains the corresponding standalone law, regardless of earlier observations.
- **History-reactive environment R:** if A was acquired first and observed `0`, B becomes more accurate and C less accurate; if A was acquired first and observed `1`, C becomes more accurate and B less accurate. Other orders retain their standalone laws.

In a diagnostic extreme, the primed cue is perfect and the other is fair (accuracies `1` and `1/2`). A full-support version uses accuracies `9/10` and `3/5`. Because A is a fair coin, both versions preserve the second cue's **unconditional** positional accuracy: `(9/10 + 3/5)/2 = 3/4`, or `(1 + 1/2)/2 = 3/4`. Every cue's first-position accuracy and the passive simultaneous cue-pair calibration are identical across S and R **by the experimental definition of the passive intervention**. The *actively ordered pair* law differs after the A report.

### Exact optimized rewards (correct=+1, error=-L, abstention=0)

| Scenario | S adaptive | S precommitted | R adaptive | R precommitted |
|---|---:|---:|---:|---:|
| Perfect priming, `L=0` | `3/4` | `3/4` | `1` | `3/4` |
| Perfect priming, `L=3` | `3/8` | `3/8` | `1` | `1/2` |
| Full-support priming (0.9/0.6), `L=0` | `3/4` | `3/4` | `9/10` | `3/4` |
| Full-support priming (0.9/0.6), `L=3` | `3/8` | `3/8` | `3/5` | `3/8` |
| Full-support priming (0.9/0.6), `L=9` | `0` | `0` | `0` | `0` |

The two-query *adaptive access premiums* are therefore 0 under S, but `1/4` with perfect priming and `3/20` with full-support priming at loss zero. At loss three they are respectively `1/2` and `9/40` in R, versus 0 in S.

The policy that obtains the R advantage samples A first, then requests B if the perceived A bit is `0` and C if it is `1`. The precommitted comparator can always choose the best order, but cannot select the **identity of its second cue** after viewing A. When only one cue is affordable, neither environment gives the adaptive class any incremental access advantage. In the full-support variant, the loss `L=9` abstention boundary prevents extrapolation to indefinite high danger; unlike perfect priming it does not produce error-free certification.

An independent Fraction oracle enumerates every two-query acquisition tree and terminal action; it matches the separate production dynamic program across multiple loss settings. The proof does not rely on assumed optimal root choice or an unfair fixed universal bundle.

## Sufficient measurement with order-reactive information

The valid replacement is **ordered path-law sufficiency**. For any two sequential experimental environments, if for every ecological state `w` and each affordable ordered history of cue identities `j1,...,jk`, the environments agree on

`P(Z_j1=z1, ..., Z_jk=zk | W=w, do(request j1, then j2, ...))`,

then each policy leaf has the same state-conditional probability, so every fixed/acquisition-contingent policy has the same expected reward, and its optimum agrees. This remains true with history-dependent sensor reliability as long as the ecological state/target stays fixed within the encounter and the kernel is well-defined. The proof is simply summing identical policy-leaf probabilities. It is **not** a novel general result in sequential decision theory.

**For a two-query budget**, all appropriately **ordered, state-conditional pair distributions** and their prefixes suffice. Three-way co-occurrence is still unnecessary. What fails is using *passive unordered-pair* calibration in place of the **active ordered intervention**. Pooling `(A then B)` with `(B then A)` can conceal the direction-dependent mechanism. A set of separately estimated single-cue accuracies—even broken down by first/second position but averaged over previous outcomes—also fails in the example.

If previous sensing changes the actual target world, reward, spatial location or remaining opportunity, the state must be expanded to include those changes. If perception changes over across-trial learning, the trial index, prior training, individual and relevant history must enter the model. A pre-stored static confusion table cannot substitute for these histories. Where wall-clock time matters, query latency and elapsed time must also be modeled: number of cues alone is not elapsed time.

## Prospective pollinator pilot and anti-circularity gate

A three-cue artificial-flower pilot could use a context signal A plus two discriminable features B/C (e.g. colour and odor, or distinct controlled visual features). To **demonstrate that an actor can exploit externally imposed reliability switching**, the stimulus apparatus may randomize A and alter the reliability of the next cue contingent on the recorded A response; such an apparatus validates the designed experimental *intervention*, not a naturally evolved bee attention process.

To test endogenous attentional effects instead, manipulate the order in which otherwise unchanged features can be sampled; independently measure the correct/incorrect response to each modality with an explicit reporting assay, not just the final flower choice. Counterbalance cue identity, order, lag and stimulus side; analyze bee identity, colony, learning block and within-trial latency. Preserve all no-choice and missing-observation trials. Measure whether `P(next report | world, previous observed cue/outcome, order)` changes after controlling for the physical stimulus and encounter context. **Do not infer an internal cue error from a successful final visit**: the animal could guess, change strategy, or rely on other information.

If order effects disappear after directly matching stimulus presentation, learning stage and inter-cue delay, this preparation supports the static approximation. If order matters but individual cue reports cannot be independently calibrated, treat the mechanism as **unidentified**. If the only result is a shift in correct choices without cue-choice histories, one cannot attribute it uniquely to conditional sensing. A separate reward/no-reward comparison is needed to translate behavioral acquisition into fitness.

## Prior art and novelty ceiling

The ecological motivation is grounded in work demonstrating that bumblebees alter visual attention with learning (Robert, Tarapata & Nityananda 2024, https://doi.org/10.1007/s00265-024-03432-z), use multiple floral cue modalities with speed–accuracy trade-offs (Kulahci, Dornhaus & Papaj 2008, https://doi.org/10.1098/rspb.2007.1176), and switch multicue learning strategies when cue discriminability changes (Spaethe et al. 2026, https://doi.org/10.1126/sciadv.adw9320). **None** of those papers validates the present synthetic history-reactive channel or the exact reward numbers. Value of information, cue order and Bayesian sequential decisions are established ideas; the purpose is to prevent overclaiming the static pairwise-sufficiency result and provide a falsifiable measurement contract.

## Reproduction and change isolation

- `adaptive_gain/ordered_readout.py`: finite exact-state optimization over a declared history-dependent binary observation kernel, with fair precommitted *ordered* comparator and free abstention.
- `tests/test_ordered_readout.py`: 83 focused checks against an independent Fraction policy-tree oracle, standalone/passive versus active/ordered calibration checks, full-support and perfect-channel witnesses, and input guards.
- Local partial reproduction harness: `523 passed, 0 failed` (not the complete PR repository). Baseline PR head `f5693c2d60b8082a53c1ab1cca2442068ea41fe3` had successful CI on Python 3.10/3.11/3.12.
- The new-head full GitHub Actions result remains a separate gate. No existing code or frozen paper was edited.
