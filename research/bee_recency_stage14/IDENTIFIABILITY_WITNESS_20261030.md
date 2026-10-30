# Stage14 constructive identifiability limit — a positive trial is NOT proof of chosen queries

**2026-10-30 | mathematical witness, NOT a bee simulation calibrated with data.**

Even if Stage14 equalizes the most recent reward/handling cue presentation for both orders, a nonzero randomized order×wind intake contrast could be produced by a **passive learner** that receives every predictive cue automatically and *never decides which one to sample*. Therefore the experimental primary delta, if eventually positive in real bees, does not identify a neural optimized adaptive information-query policy or mathematical C_A<C_F efficiency.

## Minimal constructive model

Suppose the reward cue favors physical flower L, the handling cue favors physical flower R. The animal is forced to see BOTH cue types. Let first/second initial displays have passive scalar memory weights a_W and b_W in wind condition W. The last simultaneous informational refresh adds the **same** extra weight q to reward and handling.

The probability of choosing the high-reward L option follows a logistic score:
- reward-first: P(L) = logistic( (a_W+q) − (b_W+q) ) = logistic(a_W−b_W)
- handling-first: P(L) = logistic( (b_W+q) − (a_W+q) ) = logistic(b_W−a_W)

Thus the within-wind order effect in high-reward choice is exactly tanh[(a_W−b_W)/2], independent of the shared latest refresh weight q. If the hypothetical difference in consumed sucrose rate between the options is dY>0, the experimental interaction is

**Delta = dY{tanh[(a_crosswind−b_crosswind)/2] − tanh[(a_calm−b_calm)/2]}.**

A purely illustrative construction, with NO adaptive cue selection, uses a_calm=b_calm=1, a_crosswind=2 and b_crosswind=1, q=1 and hypothetical high/low intake rates 0.34/0.30 mg/s. It gives:
- calm order effect: 0
- crosswind order effect on high-reward choice: **+0.462117**
- order×wind expected intake contrast: **+0.018484686 mg/s**

This is near the illustrative +0.020 mg/s power assumption, *without* any animal actively choosing information-acquisition order. The numeric similarity is deliberate as a mathematical counterexample, **not** confirmation of the source power assumption or biological feasibility. All parameters are invented for the witness.

The no-adaptive-query construction falsifies the logical implication "a nonzero delta with equal final cue recency necessarily demonstrates active information routing." It does **not** show real bees use passive first-cue primacy, nor rule out adaptive routing. To distinguish mechanisms, an additional experiment must randomize the animal's **option to acquire the next information**, record actual cue requests and their costs, and match opportunity/reward alternatives. Existing PR85 and Stage14 manipulate experimenter-**supplied information order**, not the animal's own endogenous queries.

## Verification

The separate identifiability_witness.py uses closed-form choice probabilities; test_identifiability_witness.py validates the nonzero no-query witness, the zero symmetric-weight counterexample and the independence from shared latest refresh. CI outputs one JSON mathematical receipt. Neither trial schedules nor original animal records are generated here.

**Stop rule:** A future positive Stage14 primary is strictly a causal effect of experimental presentation history conditional on source adherence, NOT a proof of general ecological routeability or Darwinian fitness from optimal information search.