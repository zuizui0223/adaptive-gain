# Stage22: Four separate paid-leaf confusion probabilities

**14 November 2026 | EXACT MATHEMATICS and mock source-record validation ONLY, not a new bee experiment.** This is a separate Draft PR stacked on the source-verified Stage21 PR99. No change to previous scientific results, prior authors' data, main or frozen manuscripts.

## One question
Stage21 assumed the same bit-reading accuracy for true bit0 and true bit1 of a requested leaf cue. Real organisms often have response biases; one overall U/V hit rate is not enough. Stage22 allows:
- aU0=P(U observed 0 | U true 0), aU1=P(U observed 1 | U true 1)
- aV0=P(V observed 0 | V true 0), aV1=P(V observed 1 | V true 1).
Use a class-specific ROOT confusion s0=P(Z=0|R=0), s1=P(Z=1|R=1) as Stage20–21. All six rates are *mathematical inputs*, each in [.5,1] so labels are not inverted.
The 8 hidden worlds R~Bern(.5), U~Bern(q), V~Bern(.5) are sampled independently each trial with replacement; correct target is U if R0 else V. One source leaf may be acquired ONCE and a different second leaf optionally; both treatment arms can SKIP the first source. Cost c per actual requested leaf, correct reward1 / wrong0, normalized decision utility not measured sucrose or fitness.

## Exact theorem to test, before biological outcomes
For q=1/5, c=1/4 (the exact Stage21 special case), the best precommitted first request is SKIP, value 13/20. The optimally contingent first action after observing Z0 is also SKIP. V alone may be bought after Z1, giving a positive gain iff the true-bit class confusion meets

\[
\boxed{\Delta=\max\{0,\;\frac{s_1}{4}(a_{V0}+a_{V1}-\tfrac32)
+(1-s_0)(\tfrac3{20}a_{V0}-\tfrac3{20}a_{V1}-\tfrac{11}{40})\}.}
\]

The average U accuracy and even the two separate U true-bit accuracies do not influence the optimal access value IN THIS high-cost q/c game; buying U is dominated. Do not generalize this to lower c or other ecology.

At s0=.8,s1=.6 this reduces to \(\Delta=\max\{0,0.18a_{V0}+0.12a_{V1}-0.28\}\). Two V channels with identical mean .95, (.9,1) vs (1,.9), yield advantages .002 vs .008. Thus more accurate recognition of true V0 matters more than true V1 in this particular biased-target decision, and a single average V hit rate does not predict the optimal value. For aV0=aV1=aV this reduces exactly to Stage21's threshold \(a_V>14/15\).

## Concrete source-of-measurement gate
An independently approved pilot would need per-original-bee and per-independent-colony 2×2 confusion for **U and V** separately, blind true bit and reported bit, correct chronological presentation/response/feedback, verified no other information and no feeder reward/odor/visual leakage. Sampling both true bit0 and bit1 is essential: biased U~Bern(.2) could make an always-0 responder appear 80% accurate. Do not infer P(observed 0 | true 0) and P(observed 1 | true 1) from a single weighted overall percentage.
Do not require *exact equality* of class errors in an actual finite pilot; the point of Stage22 is to measure the asymmetry. Record uncertainty by bee/colony, not 1000 image frames as 1000 independent animals. Also measure trained root branch prior, real reward-cost and source voluntary SKIP/U/V actions. No real bee/classification or payoff data have been collected here.

## Hard claim ceiling
The above values follow a finite invented Bayesian game and do not imply bee perception, sensory bias, Darwinian fitness or a universal macroecological principle. The positive benefit is conditional on the fixed q,c and source channel assumptions. Future conclusions require an actually approved prospective study with independent colonies, verified rewards and query events. Do not tune cost or prior after biological outcomes to rescue the result.
