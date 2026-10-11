# Topology × opportunity-budget experiment: mechanism screen v1

**Status:** prospective, deterministic benchmark and preregistration-ready protocol. There are no biological observations in this note. It does not empirically validate adaptive-gain V5/V6.

## Ecological question and contrasts

Can opportunity-window changes select differently among decision architectures even when species composition and cue partitions are unchanged? Can an experiment tell that **value-layer** effect apart from an actual change in target-conditioned cue partitions?

Keep separate:

1. ecological state/target composition;
2. query-outcome partitions and branch topology;
3. ecological deadline, state frequency, reward and maintenance cost;
4. observation/detection of what the actor did.

Changing only (3) is **not** decision-structural turnover. Network rewiring or taxonomic turnover is not inferred from either benchmark.

## Exact matched topology witness

Five states have the same targets `(0,1,1,0,0)`. Three binary unit-cost queries are available in both cases, and all states are presented equally often for the primary contrast.

Topology A — routeable:

```text
       w0 w1 w2 w3 w4
root    0  0  1  1  0
left    0  1  0  0  0
right   0  0  0  1  0
```

Topology B — sequential:

```text
         w0 w1 w2 w3 w4
first     1  0  0  0  0
second    0  0  0  1  0
third     1  1  1  1  0
```

Every query in both systems has a private opposite-target pair requiring it in the fixed universal bundle. Hence both have `C_F=3`. In A, an adaptive route resolves every state in two queries, `C_A=2`. In B, the guarantee remains `C_A=3`.

### Exact outcomes, not empirical effect sizes

Let `M_z(B)` be the **optimal encounter-weighted mass of states with certain correct target identification** before budget `B`, when query choices can be conditioned on outcomes. Unresolved target-mixed branches score zero, even if a guess might be right. The fixed comparator purchases a universal resolving bundle; it may not stop after partly informative fixed queries.

| Budget | Optimal adaptive A | Optimal adaptive B | Universal fixed A | Universal fixed B | D(B) |
|---|---:|---:|---:|---:|---:|
| 1 | 0.2 | 0.2 | 0 | 0 | 0 |
| 2 | 1.0 | 0.4 | 0 | 0 | 0.6 |
| 3 | 1.0 | 1.0 | 1 | 1 | 0 |

Here `D(B)=(M_A(B)-F_A(B))-(M_B(B)-F_B(B))`; the values are computed under equal world probabilities, error-free deterministic cues, unit time per query, and deadline-specific optimal policies. The guarantee-only analysis is distinct: at B=2 the A minimax controller guarantees all worlds, while B cannot.

### A fairer ecological nonadaptive comparator

The theoretical `C_F=3` requires a **universally resolving** precommitted bundle. A real organism need not wait for that bundle to finish: it may use a shorter outcome-independent fixed subset and then make a decision, or simply report no certain identification. Denying the nonadaptive organism the ability to use incomplete information would artificially magnify adaptivity.

Use a separate *budget-matched nonadaptive* policy class: select the cue subset before seeing any outcomes, subject to the same total acquisition budget; after the fixed cues are acquired, use the joint observed outcomes either to certify a target or to make the Bayesian best guess. Only the **choice of which cues to acquire** is prohibited from depending on preceding outcomes.

Its exact balanced-prior envelope is:

| Budget | Nonadaptive certified A | Nonadaptive certified B | Nonadaptive best-guess A | Nonadaptive best-guess B |
|---|---:|---:|---:|---:|
| 0 | 0 | 0 | 0.6 | 0.6 |
| 1 | 0.2 | 0.2 | 0.8 | 0.6 |
| 2 | 0.6 | 0.4 | 0.8 | 0.8 |
| 3 | 1.0 | 1.0 | 1.0 | 1.0 |

Against this **fair nonadaptive baseline**, the true added value of conditional cue choice at budget 2 is:
- certified resolution: **0.4 in topology A**, **0 in topology B**;
- guess-permitting correct choice: **0.2 in topology A**, **0 in topology B**.

At budgets 1 and 3, both adaptive-minus-nonadaptive advantages are zero in these matched examples. Consequently, the discriminating deadline is still B=2, but the honest adaptivity gap is smaller than the initial universal-bundle contrast. Report both estimands; the universal-bundle cost and the fair partial-subset decision performance must never be labeled as the same `fixed` comparator.

### Critical endpoint distinction: an unobserved guess can be correct

The preceding table counts only *certain* target resolution. A realistic actor can guess a target before the cue history uniquely identifies it. If any target guess is allowed and maximizes correctness under the known prior, the Bayes-optimal **correct-choice** probabilities under exactly the same balanced conditions are:

| Budget | Guess-permitting choice A | Guess-permitting choice B |
|---|---:|---:|
| 0 | 0.6 | 0.6 |
| 1 | 0.8 | 0.6 |
| 2 | 1.0 | 0.8 |
| 3 | 1.0 | 1.0 |

In particular, the no-cue majority-target guess is already 0.6 accurate because three of the five states share target 0. A cue that does not completely resolve a branch can nevertheless improve expected classification. Hence **observed correct flower choice is not a valid direct estimator of certain resolution**. This is the main observation-versus-theorem ambiguity in this experiment.

The two envelopes ask different biological questions: cue-history certification tests actual exploitation of a sufficient information route, whereas correct-choice accuracy tests behavior under imperfect information and includes guesses. No positive accuracy contrast alone identifies adaptive routeability.

**Independent check:** a separate state-subset exhaustive enumerator (not importing the repository solver) gives the same 0.2/1.0/1.0 and 0.2/0.4/1.0 certain-resolution sequences, and 0.6/0.8/1.0/1.0 and 0.6/0.6/0.8/1.0 correct-choice sequences.

## Encounter distribution sensitivity

With prior `p=(0.5,0.125,0.125,0.125,0.125)`, while keeping both topologies and targets unchanged:

| Budget | Adaptive A | Adaptive B | A minus B |
|---|---:|---:|---:|
| 1 | 0.125 | 0.5 | -0.375 |
| 2 | 1.0 | 0.625 | 0.375 |
| 3 | 1.0 | 1.0 | 0 |

Thus the direction of a short-deadline **certified-resolution** contrast can reverse with encounter frequencies alone. Balanced experimental assignment identifies the structural capacity contrast; natural encounter frequencies must be measured before extrapolation to expected selection.

### New endpoint-ranking reversal at the same fixed prior

With this same skew prior and one-query deadline, the **certified-resolution** criterion favors B over A: `0.50 > 0.125`. But the **guess-permitting correct-choice** criterion favors A over B: `0.875 > 0.75`.

This is a strict reversal of the ranking of the two topologies **without changing states, target labels, probabilities, cue inventories or deadline**; only the scientific endpoint differs. Both results are attained by explicitly optimized contingent policies. Consequently, a high observed visit accuracy cannot be taken as evidence that an architecture certifies more states before the deadline, and routeability capacity cannot be promoted to a universal predictor of observed choice accuracy.

The model's different policies are allowed to optimize different stated goals. If behavior is assessed with a *fixed, pre-trained policy* rather than a separately re-optimized policy for each endpoint, policy transport and transfer costs are additional empirical requirements.

## Proposed randomized 2 × 3 × 2 controlled experiment

Cross topology A/B, deadline 1/2/3 cue-acquisitions, and strategy availability:
- **Contingent:** participant may choose the next cue based on earlier cue outcomes;
- **Nonadaptive partial:** participant precommits a subset and/or acquisition order before seeing outcomes, may make a guess within the same deadline, but may not choose the next cue conditionally.

The **universal fixed bundle** is a separate, deliberately stricter theoretical comparator used to audit the worst-case `C_F` requirement, not the causal comparison arm for observed accuracy. If a fixed subset is presented as an experimental control, it must be precommitted before the trial and the analysis must verify the selected cues do not change after observing outcomes.

The participant may be a human pilot, trained animal, or a physical/artificial agent. Use a human or simulator pilot first to confirm trial implementation and payoffs. Only move to a pollinator/consumer preparation if separate training can establish the target labels and cue discriminability. These abstract bit patterns are **not** asserted to be biologically natural flower signals.

Present trial-by-trial target state in randomized balanced blocks; independently randomize the deadline and topology, and counterbalance cue labeling/stimulus identity/order. Record all requests, their outcomes, the actor's explicit target decision, response latency, training stage and trial failures. Do not substitute clock time for counted acquisitions unless each query's latency distribution has been calibrated. The experiment compares **policy access**, not compulsory adoption of the theoretical optimal policy.

### Primary and diagnostic endpoints

1. **Primary behavioral endpoint:** probability of verified correct target action within deadline. Incorrect, absent, and timeout actions are separately reported. Because correct guesses are possible, benchmark this against the guess-permitting Bayes-optimal rather than the certified-resolution envelope.
2. **Mechanistic diagnostic endpoint:** probability of *certified certain resolution* based on the observed cue history, with an unresolved-mixed branch assigned zero. This matches the theorem but is not equivalent to biological success; a participant may guess correctly without certainty.
3. **Process endpoints:** chosen cue order, conditional change in query choice after each outcome, total queries, elapsed time and reaction latency.
4. **Error/detection diagnostics:** cue-recognition accuracy, unobserved/missed actions, dropout, observer agreement, and state-specific detection probability.

Fit both intention-to-treat and compliant-policy analyses; do not promote the latter to an unbiased randomized causal estimand. Fit a hierarchical binomial model with participant/block effects and topology × deadline × strategy interaction, supplemented by directly standardized marginal means and cluster-bootstrap intervals. Report the five-state frequencies and performance by state, not just pooled success.

### Precommitted theory-facing contrasts

- **Universal-bundle structural benchmark** at balanced priors: `D(1)=0, D(2)=0.6, D(3)=0`. This is a distinct idealized comparator, not the preferred ecological accuracy control.
- **Primary fair-policy benchmark** at balanced priors: adaptive minus budget-matched precommitted-partial advantage at deadline 2 equals 0.4 (A) versus 0 (B) for certified resolution, and 0.2 (A) versus 0 (B) for guess-permitting correct choice. Both contrasts vanish at deadlines 1 and 3. These are deterministic optimal-policy ceilings, **not mandatory empirical effects**.
- The interaction of topology and deadline on the certified-resolution endpoint is the key mechanistic contrast. A topology effect at B=2 but not at B=3 is compatible with the finite structure; absence at B=2 despite demonstrated cue mastery falsifies the claim that actors exploit the available conditional route in this preparation.
- If correct actions differ while the certified-resolution endpoint and cue structure do not, do **not** interpret that as evidence of routeability; use guesses, payoffs, strategies, or errors as candidate explanations.
- Preregister minimum meaningful observed effect, power, exclusion policy, clustering unit and familywise multiplicity before collecting confirmatory trials. The theoretical 0.6 is not a justified empirical effect-size assumption.

### Value-layer-only subexperiment

Hold topology A and its state frequencies constant; independently change the hard deadline B between 1, 2 and 3 while keeping cue cost and target reward fixed. With a controller maintenance debit `K=0.2` and guaranteed-success payoff 1, the **guarantee-level** adaptive-minus-fixed net value at these budgets is `(-0.2,+0.8,-0.2)`. This uses a different, worst-case performance endpoint from the encounter-weighted masses above.

The two reversals are an algebraic construct, not an observation of natural selection. An evolutionary test additionally needs realized reward and maintenance-cost measures, heritable alternative architectures, and their frequency or invasion dynamics; a one-session behavioral test alone cannot demonstrate evolutionary maintenance.

## Anti-circularity and stop rules

1. Set target, cue partitions, deadlines and data-quality standards before trial outcomes; do not infer topology from observed successful choices.
2. Verify cue perception/accuracy in independent calibration trials. Probabilistic cue errors require a stochastic model; they are not an established deterministic topology change.
3. Distinguish exact simulator success (expected) from behavioral success (unknown), and certify no apparent interaction outcome is simply a detection-effort contrast.
4. A nonadaptive *precommitted partial* cue subset is distinct from the universal fixed resolving bundle, even if it permits early decisions or guessing. Outcome-contingent choice of the next cue is adaptive and invalidates that nonadaptive comparator.
5. If a topology intervention changes cue salience, access cost or reward simultaneously, the structural causal claim is not identified.
6. If deadlines change encounter probabilities or prey/flower behavior, report the joint intervention rather than assigning the effect to opportunity alone.
7. If state-specific detection is unidentified, do not assert a latent ecological-rewiring mechanism from apparent gain/loss.

## Experimental prior art and novelty boundary

Artificial-flower learning, multimodal discrimination and cue-based decision strategy changes are **not new by themselves**:

- Spaethe et al. (2026), *Science Advances*, DOI: [10.1126/sciadv.adw9320](https://doi.org/10.1126/sciadv.adw9320), experimentally examined flexible decision strategies as cue information content and perceptual discriminability varied.
- Lawson et al. (2018), *Proceedings of the Royal Society B*, DOI: [10.1098/rspb.2018.0661](https://doi.org/10.1098/rspb.2018.0661), showed learning of floral scent patterns and cross-modal transfer to corresponding visual patterns.
- *The value of information in floral cues: bumblebee learning of floral size cues* (2015), *Behavioral Ecology*, DOI: [10.1093/beheco/arv061](https://doi.org/10.1093/beheco/arv061), showed learned cue informativeness need not produce a preference for the informative flower type.

The distinctive proposed empirical contrast is **not** that animals use multiple cues, learn flexible strategies, or save time. It is a preregistered crossed intervention on **target-conditioned cue partitions versus opportunity budget**, with identical world/target marginals and separate certain-resolution, guess-permitting accuracy, and observed-activity estimands. Priority for this particular experimental design remains to be audited; this protocol does not assert novelty by absence of a found antecedent.

## Repository reproducibility

- `adaptive_gain/deadline_factorial.py` computes exact contingent certain-resolution and guess-permitting correct-choice envelopes, plus budget-matched nonadaptive partial-query subset envelopes; the three comparator semantics are declared explicitly.
- `tests/test_deadline_factorial.py` checks topology costs, deadline profiles, prior shift and input guards.
- `tests/test_deadline_factorial_oracle.py` independently enumerates all finite policy trees and terminal actions to verify both endpoint envelopes.
- `tests/test_ecological_topology_opportunity_separation.py` separately checks that deadlines can reverse net value with fixed topology.

No freeze/ manuscript, V6 theorem spine, or natural-network identification ledger is modified. Treat this as mechanism-design support, not an extra paper-level theorem.
