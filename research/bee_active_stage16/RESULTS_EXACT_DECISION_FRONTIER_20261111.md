# Stage16 — When does contingent information acquisition have actual decision value?

**2026-11-11 | exact mathematical finding and independent eight-world Bayesian cross-check. Zero living bees tested; no measured cognitive error or opportunity cost.**

This is a NEW theoretical sensitivity analysis stacked on Stage15 PR #93, but does not change its existing mandatory-first-request experiment or its original source-free QA. The decisive finding is a **boundary** of the Stage15 proposal: the high-cost disappearance of access advantage REQUIRES the subject to be free to skip the first leaf request. Stage15 as presently coded makes its first request mandatory, so these are mathematically different experiments and may not be interchanged.

## One finite Bayesian decision task and two explicit policy sets

The hidden world is iid (R,U,V) uniformly distributed on all eight binary states. The correct target is T=U for R=0, or T=V for R=1. Both access arms receive the same noisy observed root Z, with **root reliability s=P(Z=R)∈[0.5,1]** (independent of U,V). When an animal pays **c units of utility per physically requested leaf**, the U/V bit is observed perfectly. A correct target choice yields 1 unit and a wrong target choice 0. A direct unqueried guess has expected accuracy 1/2. These are **assumptions**, not measured bee accuracies or calibrated milligrams.

Contingent arm may choose first U/V *after* Z; precommit arm chooses and locks first U/V *before* Z, but can request the other one after the first if its root-observed relevance changes. The cost/time of root acquisition is common to both. An optional-skip model additionally allows making **zero** leaf requests in either arm and guessing.

## Exact optimal values when the animal may decline the FIRST leaf

Let L=(1+s)/2. Since the first relevant leaf raises expected correct-choice probability to L, while a fixed arbitrary first leaf gives 3/4 accuracy, and buying the opposite leaf when the fixed first leaf is irrelevant occurs with probability 1/2, exact Bayes-optimal values are:

\[
V_{\rm contingent}^{\rm optional}=\max\left(\frac12,\ \frac{1+s}{2}-c\right).
\]

\[
V_{\rm precommit}^{\rm optional}=\max\left(\frac12,\ \frac34-c,\ \frac{1+s}{2}-\frac32c\right).
\]

The three precommit alternatives are respectively: guess without leaf, purchase only one precommitted leaf and guess as needed, or purchase the second leaf if the first becomes irrelevant to the noisy root signal. The second query's marginal correct-choice benefit is \(s-\frac12\) in a mismatched first-leaf state.

The net access-mode value is \(\Delta_{\rm optional}=V_{\rm contingent}^{\rm optional}-V_{\rm precommit}^{\rm optional}\). It cannot be negative because the contingent arm can mimic any precommitted first request. The benefit is **non-monotonic in c** and vanishes in all three informative edge cases:
- **c=0**: extra queries are free, both can achieve L correct-choice probability; *a difference in query count is not necessarily a reward difference*.
- **s=0.5**: observing Z supplies no routing information; both modes have the same policy frontier.
- **c≥s/2**: the contextual leaf is no longer worth buying and the **optional-skip** policies both guess, receiving 0.5.

**Exact maximum gain over all c≥0**:
\[
\max_c\Delta_{\rm optional}(s,c)=
\begin{cases}
(s-\tfrac12)/2,& \tfrac12\le s\le \tfrac34,\\[2pt]
s/6,& \tfrac34\le s\le 1.
\end{cases}
\]
For \(0.5\le s\le0.75\), the maximum is attained for any \(c\in[s-0.5,\ 0.25]\). For \(0.75\le s\le1\), it is attained at \(c=s/3\). The maximum possible in this restricted world is **1/6** normalized reward units at s=1,c=1/3. These are not empirical effect sizes.

## Distinct exact values for the already written mandatory-first Stage15 protocol

The current Stage15 laboratory specification **requires the first leaf request** in both arms. A subject may stop *before requesting the second* leaf but cannot skip the first. The correct separate envelope is

\[
V_{\rm contingent}^{\rm mandatory}=(1+s)/2-c,\qquad
V_{\rm precommit}^{\rm mandatory}=
\max\{3/4-c,\ (1+s)/2-3c/2\}
\]

and its value difference is
\[
\Delta_{\rm mandatory}=\min\{(s-\tfrac12)/2,\ c/2\}.
\]
This mathematical curve **does not fall back to zero at high cost**, because both forced-first policies still incur a charge even if the rational alternative would be to stop and guess. Their net expected utility can be negative at high cost. A high-cost vanishing advantage **must NOT** be claimed for the presently frozen mandatory protocol.

These are different treatment choice sets. To test the *cost-dependent stop/guess* prediction in real bees requires a separately documented optional **decline-first-leaf** action for BOTH arms, source-verified no-query attempts, otherwise identical query costs, and a new preregistered design; it cannot silently be read into PR #93.

## Inspectable example contrasts

| Root reliability s | Leaf cost c | Optional first: value advantage | Mandatory first: value advantage |
|---:|---:|---:|---:|
| 1.00 | 0.00 | 0.0000 | 0.0000 |
| 1.00 | 0.10 | +0.0500 | +0.0500 |
| 1.00 | 0.20 | +0.1000 | +0.1000 |
| 1.00 | 0.3333 | +0.1667 | +0.1667 |
| 1.00 | 0.40 | +0.1000 | +0.2000 |
| 1.00 | 0.80 | 0.0000 | +0.2500 |
| 0.60 | 0.20 | +0.0500 | +0.0500 |
| 0.60 | 0.40 | 0.0000 | +0.0500 |
| 0.50 | 0.10 | 0.0000 | 0.0000 |

Note: \(c\) is a normalized correctness-reward unit, **not seconds, joules, mg sucrose, or a physiologically measured perceptual cost**. Future real-primary Stage15 intake (mg/30s) does NOT algebraically equal these utility differences. A separate independent pilot must establish whether subjects actually prefer taking no additional information, how accurately they use R and U/V, and how cue request time displaces food intake.

## Verification and submission ceiling

[Exact Stage16 Bayesian workflow #42912930880](https://github.com/zuizui0223/adaptive-gain/actions/runs/42912930880): **SUCCESS, 11 focused tests**. A separate original eight-world Bayes posterior optimizer in the tests independently enumerates the choice to guess, to buy a first U/V leaf, or to buy a second after seeing the first. It reproduces the closed-form optional policy value for 7 root reliability levels × 11 cost values, including zero-cost, root-no-information, high-cost and normalized utility boundary cases. Mandatory-first value identities are separately checked.

The result table \`stage16_exact_query_value_frontier.json\` is saved as a source-free Actions artifact. It holds no animal events. Original prior Stage15 code and original Stage9b–13 real-data evidence are not modified by the Stage16 branch. **Do not present this as measured bees learning with root reliability s or as a demonstrated fitness benefit.**

## What actually moves the research forward

For real experimental feasibility, do **not** assume the mathematical 1/6 maximum or a putative c threshold are observable in a 30s trial. A pilot must first establish (i) the root and leaf cue detection/confusion matrix, (ii) animal-origin optional first/second requests and rejection/guessing, (iii) hardware cue/motor costs including fixed release windows, (iv) original colony independence, and (v) source-verified sucrose intake including real zeroes, instrument missingness and loss blanks. If the experimental goal is strictly the present mandatory Stage15 protocol, **only the mandatory frontier applies**. If the scientific goal is to discover the *decision to stop sampling*, preregister a separate optional-query version. These are alternatives, not post-hoc changes after looking at living animals.
