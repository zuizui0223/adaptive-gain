# Supplementary Information — environmental routeability and exact mathematical support

## Purpose

The main text argues that ecological heterogeneity has different effective costs depending on how environmental alternatives are organized for a focal ecological interaction. This Supplement separates that ecological interpretation from the exact finite mathematics.

The first four sections develop the environmental concepts used in the main text:

1. raw versus decision-relevant heterogeneity;
2. environmental routeability;
3. decision-equivalence classes;
4. ecological consequences for niche breadth, realized interaction networks and temporal heterogeneity.

The later sections retain the exact optimization, reduction, structural, selection, feedback and recurrence results. No new theorem family is introduced.

---

## S1. Environmental routeability

### S1.1 Raw heterogeneity versus decision-relevant heterogeneity

Ecological heterogeneity can be described in many ways: species richness, resource richness, habitat number, environmental variance, trait dispersion or the number of interaction states. These quantities describe the environment but do not by themselves specify how many distinctions matter for a focal ecological action.

For the finite model, the relevant objects are:

| Ecological object | Model object | Interpretation |
| --- | --- | --- |
| resource, host, predator, habitat or interaction states | represented worlds | ecological alternatives potentially encountered |
| action-relevant grouping | target | distinctions that actually change the focal action |
| observations that separate alternatives | cues/queries | information available to navigate the environment |
| time, energy, exposure or opportunity cost | cue cost | ecological price of acquiring information |
| deadline/resource ceiling | budget \(B\) | maximum cost that can be paid before the interaction closes |

A species-rich community can therefore be decision-simple if many species lead to the same action and have the same future discrimination requirements. A species-poor community can be decision-difficult if each state demands a distinct terminal cue.

### S1.2 Routeability is relational

For a declared target, let

\[
C_A
\]

be the minimum worst-case cost when later information can depend on earlier observations, and let

\[
C_F
\]

be the minimum cost of a precommitted resolving cue set.

Because every fixed cue set is also a feasible contingent policy,

\[
C_A\le C_F.
\]

We use the pair \((C_A,C_F)\) rather than a single universal complexity score.

- \(C_A\) measures the cost of navigating the environment while exploiting its branch structure.
- \(C_F\) measures the cost when every potentially relevant cue must be provisioned before branch identity is known.
- \(g=C_F-C_A\) is the task-specific routeability advantage.

Environmental routeability is therefore not a taxon-independent property of a site. It is a relationship among ecological alternatives, the focal action, the cue repertoire and cue costs.

### S1.3 Routeable and non-routeable heterogeneity

A heterogeneous environment is strongly routeable for a focal task when early cues remove large sets of alternatives and make different later cues relevant on different branches.

A heterogeneous environment is weakly routeable when many cues remain jointly relevant after early observations.

This distinction can occur even when:

- species richness is identical;
- the number of cues is identical;
- every binary cue has exactly 50/50 outcomes;
- the final target has the same number of action classes.

The exact balanced family in S7.3 shows that fixed-to-contingent cost ratios can nevertheless grow without bound.

---

## S2. Decision-equivalence classes

### S2.1 Ecological states can be distinct but decision-equivalent

The target-relevant world reduction identifies represented states that have:

1. the same focal target; and
2. identical remaining cross-target separation requirements.

Such states can be collapsed without changing contingent continuation value.

We call the resulting groups **decision-equivalence classes**.

This gives a precise ecological distinction between:

- **raw richness** — how many states or species are represented; and
- **interaction-relevant richness** — how many distinct decision obligations remain for the focal interaction.

### S2.2 Adding species need not add complexity

Suppose a consumer already treats several hosts identically for the focal decision. Adding another host with the same target and the same remaining discrimination profile increases host richness but does not increase \(C_A\).

By contrast, adding one host that creates a new branch-specific requirement can increase decision complexity even if total richness changes only slightly.

The theory therefore predicts no necessary monotonic relationship between species richness and task-specific information burden.

### S2.3 Decision equivalence is task-specific

Two species can be equivalent for one interaction and distinct for another.

For example:

- two flowers may be equivalent for visit/skip but distinct for handling technique;
- two hosts may be equivalent for acceptance but distinct for oviposition investment;
- two predators may be equivalent for escape initiation but distinct for escape direction.

Decision-equivalence classes therefore do not replace taxonomic or functional diversity. They describe the subset of diversity that is relevant to a declared ecological action.

### S2.4 Relation to functional redundancy

Functional redundancy groups species by similarity in ecological functions or contributions. Decision equivalence is different.

Two species can be functionally distinct at the ecosystem level yet decision-equivalent for one focal consumer if they require the same action and the same remaining discrimination structure. Conversely, functionally similar species can be decision-distinct if the focal interaction requires different cues or responses.

Thus:

[
	ext{taxonomic identity}

eq
	ext{functional identity}

eq
	ext{decision equivalence}.
]

The distinction matters because routeability concerns the information structure of a focal interaction rather than functional redundancy of the community as a whole.

---

## S3. Ecological consequences

### S3.1 Niche breadth and generalism

Environmental heterogeneity is often associated with broader ecological niches, but the relationship is variable across systems.

Routeability provides a structural modifier.

**Routeable generalism:** many resources are encountered, but cheap early cues partition them into smaller groups so that only a small branch-specific repertoire is needed on each encounter.

**Non-routeable generalism:** many resource-specific distinctions remain jointly relevant, so increasing resource richness translates more directly into information burden.

The prediction is not that routeability alone determines niche breadth. It is that information acquisition should constrain broad resource use less strongly in routeable resource environments than in equally heterogeneous but non-routeable environments.

### S3.2 Potential versus behaviorally accessible interactions

Let the potential interaction network contain links allowed by spatial encounter, morphology, physiology and energetic compatibility.

A link can still fail to be behaviorally accessible if the information required to identify, rank or handle the partner cannot be acquired within the ecological budget.

This is different from a **forbidden link** in ecological-network terminology. A forbidden link is prevented by a biological incompatibility such as morphology, phenology or other life-history constraints. A behaviorally inaccessible link in the present sense can remain morphologically and energetically possible but fail because the required ecological discrimination cannot be completed within the available information budget.

Routeability can expand the accessible subset because early observations remove irrelevant alternatives.

This yields a distinction:

\[
\text{potential interactions}
\supseteq
\text{behaviorally accessible interactions}
\supseteq
\text{realized interactions}.
\]

The second inclusion can be strict because of information costs. The third can be strict because competition, demography, spatial structure and other ecological processes remain important.

### S3.3 Intermediate ecological constraint

Environmental routeability changes realized performance only when

\[
C_A\le B
\]

and

\[
B<C_F.
\]

Thus the ecological effect of routeability is strongest neither under unlimited opportunity nor under impossibly severe constraint.

This applies to any common cost scale for which a hard or effectively hard budget is defensible, including time, energetic sampling capacity, exposure or opportunity loss.

### S3.4 Temporal heterogeneity

Persistent environmental change matters through decision-relevant differences among recurrent states.

Two environmental sequences can have the same autocorrelation but different evolutionary effects if one repeatedly switches among states with different routeability payoffs while the other switches among decision-equivalent states.

The relevant temporal object is therefore persistence of **decision-relevant heterogeneity**, not persistence alone.

### S3.5 Eco-evolutionary feedback

Routeability can contribute to eco-evolutionary feedback when information use changes ecological interactions and those altered interactions change future decision structure.

Examples include:

- host-choice rules changing host attack or oviposition distributions;
- adaptive resource choice changing interaction strengths;
- pollinator discrimination changing visitation and reward depletion.

The no-go result in S9 asks whether the available contrast in routeability is large enough for a proposed sensing-mediated feedback to reach a specified local oscillatory regime. It does not establish that routeability is the only or dominant feedback mechanism.

---

## S4. Natural-history mappings and empirical use

The ecological conclusions above do not require that \(C_A\) and \(C_F\) already have been measured in a natural system. The mappings below show what the theory means in concrete settings and how it could later be tested.

### S4.1 Polyphagous host use

The sequential-cues hypothesis proposes that broadly shared host cues first place a generalist herbivore within host habitat and more specific cues then guide continued search and ranking.

In routeability terms:

- host richness is raw heterogeneity;
- common cues provide early routing;
- preferred-host cues are branch-specific terminal information;
- the resulting \(C_A/C_F\) contrast determines the information cost of broad host use.

### S4.2 Adaptive foraging in food webs

Adaptive-foraging theory shows that behavioral changes can alter interaction strengths and food-web structure.

In routeability terms, a consumer's behaviorally accessible resource set can be smaller than its potential resource set when the information needed to resolve all possible partners exceeds the ecological budget.

### S4.3 Predator assessment and habitat choice

Predator classes, habitat states or risk contexts can be decision-equivalent for a coarse action but distinct for a finer response. Routeability therefore depends on the behavioral resolution being modeled.

### S4.4 Optional empirical reconstruction

A focal study can estimate routeability by:

1. declaring the focal action;
2. identifying ecological alternatives relevant to that action;
3. recording which cues separate those alternatives;
4. estimating cue-acquisition costs on a common scale;
5. reconstructing contingent and precommitted resolution costs.

These steps are a route to empirical application, not a premise required for the theoretical conclusions.

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

For unresolved represented-world set \(S\) and remaining cues \(R\), write \(R-q\) for the remaining cue set after cue \(q\) has been used. The adaptive Bellman value is

\[
C_A(S,R)=\min_q(c(q)+\max_y C_A(S_{q,y},R-q)),
\]

where the minimum is over \(q\in R\), the maximum is over reachable outcomes \(y\), and \(C_A=0\) once the target is constant on the active state.

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
h_{2,\mathrm{thr}}(q)
=
\min\{h\ge1:2^h-1-h\ge q\}.
\]

The first componentwise binary unit-cost corner capable of gap \(q\) is

\[
\boxed{
(n_{\mathrm{min}},m_{\mathrm{min}},E_{\mathrm{min}})
=
(h_{2,\mathrm{thr}}(q)+q+1,\;
h_{2,\mathrm{thr}}(q)+q,\;
h_{2,\mathrm{thr}}(q)+q).
}
\]

These exact finite counts are proof support for the ecological statement that increasingly large contingent advantages require increasingly rich branch-specific structure.

### S7.2 Bounded cue arity

For maximum cue arity \(b\ge2\),

\[
h_{b,\mathrm{thr}}(q)
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
- if \(C_A\le B\) and \(B<C_F\), only contingent sensing guarantees resolution and \(s_B=\log[(w_0+v)/w_0]-\kappa\);
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

- Beckerman, A. P., Petchey, O. L. & Warren, P. H. 2010. Adaptive foragers and community ecology: linking individuals to communities and ecosystems. *Functional Ecology* 24:1–4.
- Biggs, C. R. et al. 2020. Does functional redundancy affect ecological stability and resilience? A review and meta-analysis. *Ecosphere* 11:e03184. https://doi.org/10.1002/ecs2.3184.
- Kassen, R. 2002. The experimental evolution of specialists, generalists, and the maintenance of diversity. *Journal of Evolutionary Biology* 15:173–190. https://doi.org/10.1046/j.1420-9101.2002.00377.x.
- Jordano, P. 2016. Sampling networks of ecological interactions. *Functional Ecology* 30:1883–1893. https://doi.org/10.1111/1365-2435.12763.
- Loeuille, N. 2010. Consequences of adaptive foraging in diverse communities. *Functional Ecology* 24:18–27. https://doi.org/10.1111/j.1365-2435.2009.01617.x.
- Poisot, T., Stouffer, D. B. & Gravel, D. 2015. Beyond species: why ecological interaction networks vary through space and time. *Oikos* 124:243–251. https://doi.org/10.1111/oik.01719.
- Ricotta, C. & Pavoine, S. 2025. What do functional diversity, redundancy, rarity, and originality actually measure? A theoretical guide for ecologists and conservationists. *Ecological Complexity* 61:101116. https://doi.org/10.1016/j.ecocom.2025.101116.
- Silva, R. & Clarke, A. R. 2020. The “sequential cues hypothesis”: a conceptual model to explain host location and ranking by polyphagous herbivores. *Insect Science* 27:1136–1147. https://doi.org/10.1111/1744-7917.12719.
- Stephens, D. W. 2008. Decision ecology: foraging and the ecology of animal decision making. *Cognitive, Affective, & Behavioral Neuroscience* 8:475–484. https://doi.org/10.3758/CABN.8.4.475.
