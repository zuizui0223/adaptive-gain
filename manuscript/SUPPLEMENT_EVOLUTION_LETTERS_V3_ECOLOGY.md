# Supplementary Information — ecological interpretation and mathematical support

## Purpose

This Supplement supports the ecology-first manuscript **“Ecological structure and deadlines govern the evolutionary value of contingent sensing.”** The main text asks when contingent cue acquisition becomes selectively exposed by natural-history constraints. The Supplement has two roles:

1. make the mapping from natural history to the finite decision model explicit enough to guide empirical tests; and
2. retain the exact mathematical statements and validation boundaries needed to support the main claims.

The ecological examples below are illustrative mappings, not fitted empirical case studies.

---

## S1. From natural history to a finite sensing problem

### S1.1 Define one decision episode

The basic empirical unit should be a decision episode with a clear stopping point: attack/escape, accept/reject, choose/leave, mate/reject, oviposit/reject, or another action that can be scored.

The model then distinguishes six objects.

| Ecological object | Model object | Empirical question |
| --- | --- | --- |
| situations that may require different actions | represented worlds | Which encounter types must the organism distinguish? |
| action-relevant grouping of situations | decision target | Which distinctions actually change behavior? |
| sensory observations or sampling acts | cues/queries | What can the organism inspect, and in what order? |
| time, energy, exposure or opportunity spent sampling | acquisition cost | What is lost by obtaining another cue? |
| deadline/resource ceiling | ecological budget \(B\) | When does the opportunity close? |
| season, habitat, community or repeated context | ecological state | Does the same decision have different cue structure in different contexts? |

The represented worlds should not be “everything that differs in nature.” They are the alternatives that remain relevant to the declared decision. This is important because raw environmental complexity can greatly exceed decision-relevant complexity.

### S1.2 Define the target before measuring complexity

A cue can distinguish two situations that nevertheless lead to the same action. Such discrimination is not required for the focal target. All quantities in the theory are therefore target-specific.

For example, two plant individuals may differ chemically but belong to the same accept/reject class for an herbivore. Conversely, two visually similar flowers may require different handling actions. The theory counts only distinctions required to guarantee the focal action.

### S1.3 Record cue order, not only cue presence

A standard cue inventory records which signals are available. The present theory additionally requires the **conditional transition structure**:

- Which cue is sampled first?
- Which outcomes terminate the decision?
- Which outcomes trigger another cue?
- Which later cues are sampled only after specific earlier outcomes?

This transition structure is the empirical analogue of a contingent decision tree.

### S1.4 Define costs and budgets independently

The model does not decide what \(B\) means biologically. A focal study must justify the mapping. Candidate currencies include:

- elapsed decision time;
- energetic sampling cost;
- exposure to a predator or competitor;
- handling opportunity lost while sampling;
- duration before a host, prey item or mate becomes unavailable;
- developmental or phenological opportunity windows.

If different cue costs cannot be expressed on a common scale, the simple additive model is not yet appropriate.

---

## S2. Ecological predictions

### S2.1 Intermediate ecological constraint

For a fixed ecological decision,

\[
C_A\le C_F,
\]

where \(C_A\) is the minimum worst-case cost of contingent cue acquisition and \(C_F\) is the minimum cost of a precommitted resolving cue set.

The unique performance window for contingent sensing is

\[
\boxed{C_A\le B<C_F.}
\]

This predicts a three-region ecological response:

1. **severe constraint:** \(B<C_A\); neither architecture guarantees the decision;
2. **intermediate constraint:** \(C_A\le B<C_F\); only contingent sensing guarantees it;
3. **weak constraint:** \(B\ge C_F\); both architectures guarantee it.

Therefore the performance advantage of contingent sensing is non-monotonic with ecological constraint.

### S2.2 Conditional cue dependence

The structural advantage is

\[
g=C_F-C_A.
\]

Large \(g\) requires branch-specific obligations: different situations make different later cues relevant. Merely increasing cue number or marginal cue balance need not increase \(g\).

Empirical prediction:

> systems with stronger conditional cue dependence should show a larger performance gap between contingent and exhaustive/precommitted sampling, even when one-cue frequencies are similar.

### S2.3 Decision-relevant environmental heterogeneity

Across ecological states,

\[
\Delta g=g_2-g_1
\]

is the contrast relevant to the feedback model.

Environmental variables are therefore indirect predictors. A habitat difference matters only if it changes the decision target, cue-transition structure, cue costs, or whether the ecological budget satisfies \(C_A\le B\) and \(B<C_F\).

### S2.4 Persistence × payoff alignment

Environmental persistence matters when the persistent states also differ in contingent-sensing payoff. The recurrence result predicts an interaction between:

- state persistence; and
- state-specific selection generated by the sensing problem.

A persistent environment whose states all have similar \(g\) or similar budget-gated payoff should have weak long-run evolutionary effects through this mechanism.

### S2.5 Generalism and sensory focusing

Broad resource use can increase the number of situations and potential cues an organism encounters. The theory yields two qualitatively different cases.

**Routeable generalism:** cheap early cues separate situations into branches, and expensive terminal cues are needed only within particular branches. Contingent sensing can keep realized acquisition cost shallow.

**Non-routeable generalism:** many terminal cues remain necessary across most branches. Fixed and contingent costs converge or both become high.

This is a conditional mechanism linking natural-history breadth to decision architecture. It is not a general theory of ecological specialization.

---

## S3. Illustrative natural-history mappings

### S3.1 Predator assessment

**Represented situations:** predator classes, approach directions, distances or attack trajectories.

**Target:** escape now / monitor / ignore, or another declared action partition.

**Possible early cue:** broad risk class, movement direction or alarm cue.

**Possible terminal cue:** identity-, distance- or trajectory-specific information required only in a subset of branches.

**Budget:** time until interception, safe refuge closes, or exposure becomes unacceptable.

**Prediction:** contingent assessment should be most valuable when a broad early cue cheaply eliminates many response branches but fine assessment remains necessary for a subset.

### S3.2 Herbivore host choice or oviposition

**Represented situations:** candidate host taxa, plant states or resource-quality classes.

**Target:** accept/reject or a graded target discretized before analysis.

**Possible early cue:** habitat, plant identity, gross morphology or volatile class.

**Possible terminal cue:** surface chemistry, contact chemical cue or fine quality measure.

**Budget:** handling time, enemy exposure, movement of the host, or opportunity cost.

This mapping is motivated by longstanding work linking host breadth and sensory/information-processing complexity to decision time and exposure risk. It is also directly compatible with the sequential-cues hypothesis for polyphagous herbivores, in which broadly shared host cues first place the insect in host habitat and more specific cues then guide continued search and ranking (Silva & Clarke 2020). A focal empirical test should therefore score not only which cues are used, but whether common cues terminate some decisions while specific cues are sampled only after particular early outcomes. The finite model becomes informative only after those conditional transitions and their costs are measured.

### S3.3 Pollinator flower choice

**Represented situations:** flower species or reward classes.

**Target:** visit/skip, handling mode or another focal action.

**Possible early cue:** spatial position, gross color category or flower shape.

**Possible terminal cue:** fine color discrimination, odor or contact information.

**Budget:** foraging time or opportunity cost.

Bumblebee speed–accuracy trade-offs provide an empirical precedent for time-sensitive flower discrimination, but the present \(C_A/C_F\) structure has not been estimated from those experiments.

---

## S4. Empirical workflow

### S4.1 Observe natural cue sequences

Video, high-speed recording, gaze/antenna/orientation tracking, controlled cue removal or staged encounters can be used to infer:

- order of sampling;
- branch-specific continuation;
- stopping rules;
- decision latency.

The key datum is conditionality, not only response to individual cues.

### S4.2 Reconstruct a target-relevant decision tree

For each encounter type, record the target action and observed cue outcomes. A proposed tree should be checked against all represented situations.

The empirical \(C_A\) is not simply mean decision time. It is the minimum cost of a strategy that guarantees the declared target under the modeled cue repertoire. Observed behavior can be compared with this optimum but need not equal it.

### S4.3 Build a fixed counterfactual

\(C_F\) represents the cheapest cue set that would guarantee the same decision without conditioning acquisition on earlier outcomes.

This is a counterfactual architecture, not necessarily a naturally observed phenotype. It asks how much resource provisioning would be required if every potentially relevant cue had to be available before branch identity was known.

### S4.4 Manipulate the ecological budget

The most direct test varies \(B\) while holding the target and cue repertoire as stable as possible.

Predicted response:

\[
\text{advantage of contingent sensing}
=
0
\rightarrow
\text{positive}
\rightarrow
0
\]

as the budget moves from below \(C_A\), through the region where \(C_A\le B\) and \(B<C_F\), to above \(C_F\).

### S4.5 Compare ecological states

Repeat the task across seasons, habitats or community contexts. Estimate whether changes alter:

- the represented target-relevant alternatives;
- cue costs;
- branch-specific cue requirements;
- \(C_A\), \(C_F\), or \(g\).

This separates raw environmental change from decision-relevant ecological change.

### S4.6 Link to recurrence

For recurrent states, estimate an ecological transition matrix and state-specific sensing payoff. The long-run theory then asks whether payoff variation loads onto slow ecological modes.

---

## S5. Exact finite adaptive gain

Let \(\mathcal W\) be a finite represented-world set, \(T\) a declared target, and \(\mathcal Q\) a finite cue vocabulary with positive additive acquisition costs.

The minimum fixed resolving-bundle cost is

\[
C_F
=
\min_{F\text{ resolves}}
\sum_{q\in F}c(q).
\]

For unresolved represented-world set \(S\) and remaining cues \(R\), the adaptive Bellman value is

\[
C_A(S,R)=\min_{q\in R}\{c(q)+\max_y C_A(S_{q,y},R\setminus\{q\})\}.
\]

where the maximum is over reachable outcomes \(y\), and \(C_A=0\) once the target is constant on the active state.

Every fixed resolver is a feasible contingent policy that ignores intermediate outcomes, therefore

\[
\boxed{C_A\le C_F.}
\]

The adaptive-only ecological budget region follows immediately:

\[
\boxed{C_A\le B<C_F.}
\]

**Primary source:** \`theory/ADAPTIVE_GAIN_THEOREM.md\`.

---

## S6. Exact target-relevant reduction

Raw natural-history descriptions can contain distinctions irrelevant to the focal decision.

### S6.1 Query-side dominance

At active state \(A\), let \(S_A(q)\) be the identity-indexed cross-target pairs separated by cue \(q\). If

\[
S_A(q)\supseteq S_A(r)
\]

and

\[
c(q)\le c(r),
\]

then \(r\) is safely dominated at that state.

### S6.2 World-side quotient

Same-target represented worlds with identical remaining cross-target separation profiles can be quotient-collapsed without changing adaptive continuation value.

### S6.3 Two-sided kernel

Recursive composition of world quotienting and query dominance preserves the adaptive optimum:

\[
\boxed{
C_A^{\rm kernel}=C_A^{\rm direct}.
}
\]

Ecological interpretation: descriptive differences are not automatically distinct decision states. The reduction is target-specific and applies only to the deterministic exact-resolution objective.

**Sources:**

- \`theory/ADAPTIVE_SAFE_QUERY_COMPRESSION.md\`
- \`theory/ADAPTIVE_WORLD_TWIN_QUOTIENT.md\`
- \`theory/ADAPTIVE_TWO_SIDED_KERNEL.md\`

---

## S7. Finite structural requirements and branch exclusivity

### S7.1 Binary exact corner

If a state-specific task must support integer structural gap \(q\ge1\), define

\[
h_2^{\ast}(q)
=
\min\{h\ge1:2^h-1-h\ge q\}.
\]

The first componentwise binary unit-cost corner capable of gap \(q\) is

\[
\boxed{
(n^{\ast},m^{\ast},E^{\ast})
=
(h_2^{\ast}+q+1,\;
h_2^{\ast}+q,\;
h_2^{\ast}+q).
}
\]

These exact finite counts are proof support for the ecological statement that increasingly large contingent advantages require increasingly rich branch-specific structure.

### S7.2 Bounded cue arity

For maximum cue arity \(b\ge2\),

\[
h_b^{\ast}(q)
=
\min
\left\{
h\ge1:
\frac{b^h-1}{b-1}-h\ge q
\right\}.
\]

The exact joint requirement is generally Pareto-valued for \(b>2\); there is not one scalar sensory-complexity minimum.

### S7.3 Globally balanced cues can still produce unbounded gain

For routing depth \(d\), we construct finite deterministic binary unit-cost tasks in which every cue is exactly 50/50 balanced over represented worlds, while

\[
C_F\ge2^d,
\qquad
C_A\le d+1.
\]

Hence

\[
\boxed{
\frac{C_F}{C_A}
\ge
\frac{2^d}{d+1}
\longrightarrow\infty.
}
\]

This is a family-level existence result, not a fixed-size optimum.

Ecological interpretation: marginal cue balance does not bound contingent value because the critical structure is branch-specific terminal demand.

**Sources:**

- \`theory/GENERAL_BINARY_DYNAMIC_SCOPE_THRESHOLD.md\`
- \`theory/ARITY_GAP_PARETO.md\`
- \`theory/DYNAMIC_ARITY_PARETO.md\`
- \`theory/BALANCED_BINARY_UNBOUNDED_ADAPTIVE_GAIN.md\`

---

## S8. Hard-budget evolutionary selection

For ecological state \(X\), define guaranteed-resolution indicators

\[
S_A(X,B)=\mathbf 1\{C_A(X)\le B\},
\qquad
S_F(X,B)=\mathbf 1\{C_F(X)\le B\}.
\]

Let baseline fitness be \(w_0>0\), the benefit of resolving the target before the opportunity closes be \(v\ge0\), and log maintenance cost of contingent control be \(\kappa\ge0\):

\[
W_A
=
e^{-\kappa}
[w_0+vS_A(X,B)],
\]

\[
W_F
=
w_0+vS_F(X,B).
\]

The log fitness contrast is

\[
s_B(X)
=
\log\frac{W_A}{W_F}.
\]

The three budget regions are:

- if \(B<C_A\), both architectures fail to guarantee resolution and \(s_B=-\kappa\);
- if \(C_A\le B\) and \(B<C_F\), only contingent sensing guarantees resolution and
  \[
  s_B=\log\frac{w_0+v}{w_0}-\kappa;
  \]
- if \(B\ge C_F\), both architectures guarantee resolution and \(s_B=-\kappa\).

Thus contingent architecture is favored in the adaptive-only region when

\[
\kappa
<
\log\frac{w_0+v}{w_0}.
\]

The non-monotonic ecological prediction follows from this three-region structure.

**Source:** \`theory/BUDGET_GATED_EVOLUTIONARY_SELECTION.md\`.

---

## S9. Nonlinear structural no-go for feedback

For ecological states with

\[
g_i=C_F(i)-C_A(i)\ge0
\]

and ordered contrast

\[
\Delta g=g_2-g_1\ge0,
\]

let selection satisfy

\[
s_i=f(g_i)-\kappa
\]

for nondecreasing \(f\) with bounded marginal effect

\[
0
\le
f(g_2)-f(g_1)
\le
L\Delta g.
\]

With feedback-per-selection scale \(B_f>0\),

\[
0\le G\le B_fL\Delta g.
\]

For local evolutionary persistence \(\alpha\) and ecological persistence \(\phi\), the complex-return threshold is

\[
G_{\rm osc}
=
\frac{(\alpha-\phi)^2}
{4(1-\phi)}.
\]

A necessary condition for oscillatory return is therefore

\[
\boxed{
\Delta g
>
\frac{G_{\rm osc}}{B_fL}.
}
\]

If an admissible architecture class has maximum contrast \(\Delta g_{\max}\) satisfying

\[
B_fL\Delta g_{\max}
\le
G_{\rm osc},
\]

then the requested oscillatory regime is impossible for every sensing-to-selection lift in the declared class.

Crossing the bound is necessary, not sufficient.

**Sources:**

- \`theory/NONLINEAR_LIFT_NO_GO_V2.md\`
- \`adaptive_gain/nonlinear_feedback_reachability.py\`
- \`tests/test_nonlinear_feedback_reachability.py\`
- \`validation/nonlinear_lipschitz_no_go_v2.json\`

---

## S10. Ecological recurrence and reward-mode alignment

Let ecological states form a finite ergodic reversible Markov chain with stationary distribution \(\pi\). For centered state-specific selection reward,

\[
\sigma_{\rm eff}^2
=
\sum_r
w_r
\frac{1+r_r}{1-r_r}.
\]

Here \(r_r\) is a nonstationary ecological eigenvalue and \(w_r\) is the squared loading of the selection/reward vector on that mode.

This decomposition separates two ecological properties:

1. **persistence:** amplification factor \((1+r_r)/(1-r_r)\);
2. **alignment:** whether sensing-generated selection actually projects onto that persistent mode.

In the linear special case with \(0\le g_i\le g_{\max}\),

\[
\sigma_{\rm eff}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}}.
\]

The bound is extremally sharp but is not a generic prediction of realized variance.

**Sources:**

- \`theory/STRUCTURAL_SPECTRAL_JOINT_BOUND.md\`
- \`theory/STRUCTURAL_REWARD_MODE_ALIGNMENT.md\`

---

## S11. Feedback existence and identifiability boundary

Within the declared local persistence domain,

\[
0\le\alpha\le1,
\qquad
0\le\phi<1,
\]

a model-compatible complex conjugate eigenpair excludes every zero-feedback decomposition, so every compatible decomposition has

\[
G>0.
\]

This can diagnose feedback existence within the model but does not identify:

- feedback magnitude;
- separate ecological and evolutionary persistence;
- the fraction of feedback caused by sensing architecture.

The main text does not require this diagnostic as a headline result; it is retained here as an interpretive boundary.

**Sources:**

- \`theory/FEEDBACK_EXISTENCE_FROM_OSCILLATION.md\`
- \`theory/GENERAL_RESPONSE_IDENTIFIABILITY.md\`

---

## S12. Scope and reproducibility

### Scope

The exact finite results assume deterministic cue outcomes, positive additive cue costs and guaranteed target resolution. The theory does not yet include:

- noisy likelihoods;
- Bayesian belief updating;
- graded accuracy;
- expected-loss objectives;
- continuous sampling time;
- heterogeneous individual budgets;
- mutation, migration or drift;
- demographic stochasticity;
- multivariate genetics;
- global nonlinear bifurcation analysis.

### Reproducibility

Code and theorem documents are organized in the public \`zuizui0223/adaptive-gain\` repository. The Supplement retains the exact finite results, validation boundaries and reproducibility pointers supporting the ecological claims in the main text.

### Empirical interpretation boundary

Natural-history examples in S3 are illustrative. They show how to instantiate the model, not that contingent \(C_A/C_F\) gaps have already been measured in those systems.


## S13. Ecological references for interpretation

- Silva, R. & Clarke, A. R. 2020. The “sequential cues hypothesis”: a conceptual model to explain host location and ranking by polyphagous herbivores. *Insect Science* 27:1136–1147. https://doi.org/10.1111/1744-7917.12719.
- Stephens, D. W. 2008. Decision ecology: foraging and the ecology of animal decision making. *Cognitive, Affective, & Behavioral Neuroscience* 8:475–484. https://doi.org/10.3758/CABN.8.4.475.
