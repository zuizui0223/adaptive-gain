# Conditional decision topology separates information amount from ecological accessibility

Draft v0.3 — American Naturalist-oriented theoretical synthesis candidate

## Abstract

Environmental heterogeneity has amount, grain and pattern, but ecological decisions also have **conditional topology**: an early cue outcome can change which later distinction matters. We ask whether this topology can alter ecological accessibility when conventional information quantities are held fixed. For a finite decision task, let \(C_A\) be the minimum worst-case cue cost under outcome-contingent acquisition and \(C_F\) the minimum cost of a fixed resolving cue set. For every \(d\ge2\), we construct two target maps on the same states and complete cue-outcome matrix. The paired tasks share cue costs, all cue-only distributions, target prevalence, target entropy and full-vocabulary target information. They differ only in how cue states map to action. In the routeable task, \(C_F\ge2^d\) and \(C_A\le d+1\); in the control, \(C_A=C_F=2\). Under the same budget \(B=d+1\), only the routeable task lies in \(C_A\le B<C_F\). Thus information amount and accessibility are distinct coordinates. The theory yields a measurement protocol and matched behavioral experiments, while leaving noisy cues and expected-loss decisions to a separate stochastic extension.

## Keywords

environmental heterogeneity; ecological information; sequential decision making; adaptive feature acquisition; niche breadth; routeability; information processing; cue acquisition

---

## 1. Introduction

Environmental heterogeneity is a central ecological explanatory variable, but ecology does not reduce it to a single scalar. Classical and modern theory distinguish not only how much variation exists but also its spatial or temporal pattern and grain. Likewise, information ecology and information-fitness theory ask how environmental information changes decisions, growth and selection. The starting point of this paper is therefore not that ecology has ignored structure.

A second established literature makes the acquisition problem explicit. Sequential host-location models propose that organisms can use broad and specific cues in stages, and costly-feature classification formalizes prediction in which different features are acquired for different samples, in different orders, under acquisition costs or budgets. Adaptive feature acquisition is therefore prior art, as is the general value of collecting information before action. Our contribution is not the observation that conditional sampling can be useful. Bernays and Wcislo linked resource specialization to information-processing costs, Silva and Clarke proposed sequential cue use in polyphagous host location, and modern costly-feature methods explicitly choose later measurements from earlier observations (Bernays & Wcislo 1994; Silva & Clarke 2020; Contardo et al. 2016; Janisch et al. 2020; Nan & Saligrama 2017).

The unresolved ecological issue is different. Most empirical summaries of environmental information are **distributional**: richness, frequencies, variance, cue entropy, pairwise association or the total target information available in a cue set. Even when such summaries are rich, they need not answer an operational question:

> after one cue outcome is observed, which distinctions remain necessary before the organism can act?

We call this dependency structure **conditional decision topology**. The term does not mean temporal order alone. A fixed sequence of observations and an outcome-contingent decision tree are different objects: topology concerns which later distinction becomes relevant on each branch. The same physical environment can therefore induce different topologies for different focal actions.

This distinction also has mathematical precedent outside ecology. Information theory contains examples in which two problems share the same entropy for every subset of their variables yet have different operational capacities, showing that entropic structure need not be a complete operational invariant. We therefore do not claim that this paper is the first theory in which entropy misses consequential structure (Sun & Jafar 2019). The ecological question is narrower and constructive: **can environmental states, the complete physical cue matrix, target prevalence, target entropy and total available target information all be held fixed while the acquisition cost of the focal action changes sharply?**

We answer yes. For a declared ecological task, let \(C_A\) denote the minimum worst-case cue cost when later cues may depend on earlier outcomes, and let \(C_F\) denote the minimum cost of a fixed resolving cue set. We construct paired tasks on the same physical cue environment. Only the map from cue-defined states to the focal action changes. Nevertheless, the fixed-to-contingent acquisition geometry separates without bound as the construction grows, whereas the matched control requires only two fixed cues.

The biological coupling is supplied by a separate natural-history quantity: an observation budget \(B\). This budget may represent time before a host departs, handling opportunity, predator exposure, attention or another hard or effectively hard ceiling. Conditional topology changes guaranteed performance precisely when the budget lies between the two structural requirements,

\[
C_A\le B<C_F.
\]

This factorization keeps the mathematics and the ecology distinct. The action-conditioned cue structure determines \((C_A,C_F)\); natural history determines \(B\); their intersection determines whether routeability changes feasible behavior.

We develop four consequences. First, information amount and information accessibility are distinct coordinates. Second, routeability is relational rather than intrinsic to a habitat or community: the same physical environment can be routeable for one focal action and non-routeable for another. Third, several common ecological summaries can be insufficient for routeability-sensitive mechanistic claims even when they are quantitatively strong. Fourth, the theory specifies what must be measured and produces matched experimental designs, rather than asking routeability to be inferred from richness, entropy or network turnover alone.

---

## 2. Finite ecological decision tasks

Let \(W\) be a finite set of ecological alternatives. A world \(w\in W\) may represent a resource, host, partner, habitat condition or other state relevant to a focal decision.

Let

\[
T:W\to\mathcal A
\]

map each alternative to a focal ecological action. Examples include accept/reject, exploit/leave, attack/avoid or court/reject.

A cue \(q\) is a deterministic map from represented states to observable outcomes. Each cue has a positive acquisition cost \(c(q)\). The cue vocabulary is finite.

A **fixed** resolving bundle is chosen before any cue outcome is known and must distinguish all state pairs that require different focal actions. Its minimum cost is \(C_F\).

An **adaptive** policy chooses the next cue conditional on previous outcomes. Every terminal branch must contain only states requiring the same focal action. The minimum worst-case path cost is \(C_A\).

Because any fixed bundle can be queried sequentially while ignoring intermediate outcomes,

\[
C_A\le C_F.
\]

The difference

\[
g=C_F-C_A
\]

measures the structural burden avoided by contingent acquisition.

Neither \(C_A\) nor \(C_F\) is intrinsically fitness. They are exact properties of a declared finite decision problem.

---

## 3. Relational routeability theorem

For every integer \(d\ge2\), set

\[
k=2^d.
\]

Use the existing exactly-balanced binary cue environment with \(2k+2\) represented states and \(d+k\) unit-cost binary cues. Every cue divides the state set exactly in half.

We define two target maps on this **same cue environment**.

### 3.1 Routeable target map

There are \(k\) mixed target pairs \((a_i,b_i)\), with opposite targets inside each pair, plus two target-0 dummy states.

The first \(d\) cues encode the branch index. Each branch has a terminal cue that uniquely separates its mixed pair.

A contingent policy asks the \(d\) routing cues and then only the terminal cue for the realized branch. Hence

\[
C_A(T_R)\le d+1.
\]

Every branch terminal is uniquely required by one cross-target pair, so any fixed resolver must contain at least all \(k\) terminals:

\[
C_F(T_R)\ge k=2^d.
\]

### 3.2 Matched control target map

Keep every represented state and every cue outcome unchanged.

Define the control target using equality of the first two routing bits:

\[
T_K(w)=
\begin{cases}
0,&q_0(w)=q_1(w),\\
1,&q_0(w)\ne q_1(w).
\end{cases}
\]

The first two routing cues resolve this target, so

\[
C_A(T_K)\le2,\qquad C_F(T_K)\le2.
\]

No single cue resolves the target. Every declared cue partitions the \(2k+2\) states into two sets of size \(k+1\), whereas the two control target classes have sizes \(k+2\) and \(k\). Thus

\[
\boxed{
C_A(T_K)=C_F(T_K)=2.
}
\]

### 3.3 Quantities held fixed

The two tasks share exactly:

- represented states and state count;
- cue identities and cue count;
- cue costs;
- the complete state-by-cue outcome matrix;
- all one-cue marginals;
- every cue-only joint distribution of every order.

They also have identical target class multiplicities:

\[
(k+2,k).
\]

Therefore target entropy is identical under a uniform prior on represented states.

Because the full cue vocabulary resolves both targets,

\[
I(T_R;Q_{\mathrm{all}})
=
I(T_K;Q_{\mathrm{all}})
=
H(T).
\]

Thus neither the physical cue environment nor the amount of full-vocabulary target information distinguishes the two tasks.

Yet

\[
\boxed{
\frac{C_F(T_R)}{C_A(T_R)}
-
\frac{C_F(T_K)}{C_A(T_K)}
\ge
\frac{2^d}{d+1}-1
\to\infty.
}
\]

The source of the separation is the action-conditioned arrangement of cue states.

---

## 4. Exact common-budget ecological corollary

The relational theorem becomes ecological when a shared observation budget is imposed.

Set

\[
B=d+1.
\]

For every \(d\ge2\),

\[
2^d>d+1.
\]

Therefore the routeable task satisfies

\[
C_A(T_R)\le B<C_F(T_R),
\]

whereas the control satisfies

\[
C_A(T_K)=C_F(T_K)=2\le B.
\]

Let \(S_{X,Y}\) be the indicator that architecture \(X\in\{R,K\}\) is guaranteed resolvable under access mode \(Y\in\{A,F\}\) at the common budget.

Then

\[
(S_{R,A},S_{R,F},S_{K,A},S_{K,F})
=
(1,0,1,1).
\]

Hence the architecture-by-access contrast is

\[
\boxed{
(S_{R,A}-S_{R,F})
-
(S_{K,A}-S_{K,F})
=
1.
}
\]

This is an exact feasibility contrast, not a claim that real animals will exhibit a one-unit behavioral effect. Its biological role is to localize where topology can matter: under extremely small budgets both strategies may fail; under large budgets both may succeed; the topology-sensitive region lies between the adaptive and fixed requirements.

---

## 5. Stronger finite matching of pairwise information

The asymptotic construction holds the complete cue-only environment fixed, but changing the target map generally changes individual target–cue pairwise associations.

At small registered scopes, stronger controls are available.

For routing depths two and three, we constructed matched target maps with:

- the same physical cue matrix;
- the same target multiplicities;
- the same **multiset** of canonical target–cue \(2\times2\) contingency profiles, up to independent binary relabeling.

This matches the distribution of pairwise target–cue information strengths, although not necessarily cue-name by cue-name.

At depth two the matched control has

\[
C_A=C_F=2.
\]

At depth three it has

\[
C_A=C_F=3.
\]

These examples show that pairwise target–cue informativeness can remain insufficient to identify conditional acquisition structure.

We do not claim an asymptotic family preserving a named pairwise-information matrix.

---

## 6. A sufficiency ladder for ecological summaries

The paired constructions organize ecological summaries by how much structural information they retain.

State count and cue count are insufficient.

All cue marginals are insufficient, even when every binary cue is perfectly balanced.

The complete cue-only joint distribution is insufficient.

Target prevalence and target entropy are insufficient.

Total full-vocabulary target information is insufficient.

At finite scopes, the multiset of pairwise target–cue information strengths can also be insufficient.

By contrast, if one observes the complete action-conditioned table

\[
(w,T(w),q_1(w),\ldots,q_m(w))
\]

together with cue costs, the deterministic finite optimization problem is specified and \(C_A\) and \(C_F\) can in principle be computed.

The theory therefore does not claim that topology is metaphysically hidden or unrecoverable. It identifies which common summaries omit the relevant structure.

---

## 7. Relation to existing ecological principles

### 7.1 Information amount and information accessibility

Information-fitness theory establishes that environmental information can affect fitness and can be quantified relative to environmental states and responses. Our theorem concerns a different operational layer.

Two tasks can contain the same total target information yet differ in how much information must be acquired together before action.

Thus

\[
\boxed{
\text{information amount}
\neq
\text{information accessibility under sequential cost}.
}
\]

This is a complement to, not a rejection of, information-fitness theory.

### 7.2 Specialist-generalist information-processing costs

Information-processing limits have long been proposed as constraints on broad diet breadth.

Routeability sharpens that idea. Equal nominal niche breadth does not imply equal decision burden. A consumer using many resources may need few observations per encounter when early cues route encounters into small branch-specific subproblems. Another consumer with the same number and frequency of usable resources may require many distinctions to remain simultaneously provisioned.

The direct claim concerns processing burden. Predicting evolved niche breadth additionally requires fitness, trade-offs and evolutionary dynamics.

### 7.3 Environmental heterogeneity and niche breadth

Heterogeneity theory already distinguishes amount, grain and spatial/temporal pattern. Conditional decision topology is not a substitute for these dimensions.

It is a relational addition: even when environmental distributions and schedules are matched, different mappings from state to action can produce different decision geometry.

A safe prediction is therefore conditional:

> broad ecological use should be less constrained by information acquisition when relevant alternatives are routeable within the organism's observation budget.

### 7.4 Interaction accessibility

Morphology, phenology and encounter opportunity can define a set of compatible potential interactions. Conditional decision topology can act downstream of those filters.

An interaction can be biologically compatible yet behaviorally inaccessible if its discrimination burden exceeds the available observation budget.

This supplies a direct prediction about **accessibility**, not yet about equilibrium network topology or stability.

### 7.5 Diversity-stability is downstream

The present finite model contains no species abundance dynamics, synchrony process, community Jacobian, resilience metric or ecosystem-function variance.

Therefore no diversity-stability conclusion follows directly.

A future theory would need to map routeability into realized interaction strengths and then into an explicit community dynamical model.

---

## 8. Measurement: recover structure before summarizing it

A routeability analysis must begin with a focal action.

For each represented ecological alternative, measure:

- target/action;
- available cue identities;
- cue outcomes;
- acquisition costs or timing constraints.

Behavioral data should also retain ordered observation paths rather than only cue-use frequencies.

The minimal structural object is

\[
(W,T,Q,c).
\]

From it compute

\[
C_A,\qquad C_F,\qquad g=C_F-C_A.
\]

Then estimate a biologically meaningful observation budget \(B\).

The protocol is therefore:

\[
\boxed{
\text{measure the action-conditioned cue table first; summarize it second}.
}
\]

Natural systems lacking the action map, state-by-cue incidence or defensible acquisition costs should be labeled unevaluable rather than rescued with richness or entropy proxies.

---

## 9. Two direct experiments

### 9.1 Minimal four-state causal experiment

The first experiment uses four physical cue vectors and three cue channels.

Routeable and bypass-control architectures share the cue environment but differ in target mapping.

The budget ladder is designed so that the architecture-by-access contrast is predicted to be absent below and above the routeability-sensitive window and positive only inside it.

This is the preferred first behavioral test because it minimizes training and apparatus burden.

### 9.2 Exact-balanced ten-state stress test

A stronger follow-up uses ten states and six cue channels. Every cue is exactly 5/5 balanced, and routeable/control groups use the identical physical cue matrix.

Exact costs are

\[
(C_A,C_F)_R=(3,4),
\]

\[
(C_A,C_F)_K=(2,2).
\]

At common budget \(B=3\), a routed three-cue schedule reaches exact uniform-state accuracy 1 in both architectures.

The best fixed three-cue ceiling is

\[
4/5
\]

in the routeable architecture and

\[
1
\]

in the control.

Thus the exact deterministic ceiling interaction is

\[
\boxed{
(1-4/5)-(1-1)=1/5.
}
\]

The value \(1/5\) is a task ceiling, not a behavioral effect-size assumption.

---

## 10. Prior-art boundary

Adaptive feature acquisition is established in machine learning: features can be sequentially selected per sample under acquisition costs or budgets.

Sequential value-of-information problems are established in decision analysis.

Uniform separating systems and generic adaptive-versus-non-adaptive search are established in combinatorics.

Information theory also provides examples in which identical entropic structure does not determine an operational quantity; *extra-entropic structure* is therefore prior conceptual territory.

The present contribution is narrower:

> an exact ecological decision construction in which the physical cue environment and strong information summaries are held fixed while the focal action map changes acquisition topology, producing an exact difference in finite-budget feasibility.

This is the claim that should be defended.

---

## 11. Deterministic scope and next theory

The current model assumes:

- finite alternatives;
- deterministic cue outcomes;
- additive positive cue costs;
- worst-case optimization;
- guaranteed exact action resolution.

These assumptions define an idealized structural limit.

They are sufficient to establish the existence and ecological relevance of conditional decision topology.

The next theory should replace exact resolution with stochastic expected loss, for example

\[
J(\pi)
=
\mathbb E[C_\pi]
+
\lambda\mathbb E[L(A,T)].
\]

The key question is not merely whether noisy cue acquisition can be optimized. That is already adjacent to active feature acquisition.

The sharper future question is:

> does the quantity-topology separation persist when physical cue distributions and target-information summaries are matched but decisions are noisy and evaluated by expected loss?

This is a separate paper.

---

## 12. Conclusion

Environmental information has at least two operational aspects.

One is amount: what states, cue variation and target information are present.

The other is conditional decision topology: which distinctions must remain jointly available before action, and which can be deferred until an earlier observation identifies the relevant branch.

These coordinates can be separated exactly. Two tasks can share the same physical cue environment, target prevalence, target entropy and total available target information while having radically different fixed and contingent acquisition costs.

A finite ecological budget converts that structural distinction into a feasibility difference.

The resulting principle is:

\[
\boxed{
\text{Amount describes what information exists; topology describes what must be acquired together before action.}
\]

## Claim boundary

This paper does not claim:
- a new theory of adaptive feature acquisition;
- that entropy or mutual information are generally inadequate;
- that routeability replaces environmental grain or network topology;
- direct diversity-stability consequences;
- quantitative validity under noisy natural cues.

It claims an exact relational ecological axis and a measurement/experimental program for testing its consequences.

## References

- Bernays, E. A. & Wcislo, W. T. 1994. Sensory capabilities, information processing, and resource specialization. *Quarterly Review of Biology* 69:187–204. DOI: 10.1086/418539.
- Bernays, E. A. 2001. Neural limitations in phytophagous insects: implications for diet breadth and evolution of host affiliation. *Annual Review of Entomology* 46:703–727. DOI: 10.1146/annurev.ento.46.1.703.
- Contardo, G., Denoyer, L. & Artières, T. 2016. Recurrent Neural Networks for Adaptive Feature Acquisition. ICONIP 2016. DOI: 10.1007/978-3-319-46675-0_65.
- Donaldson-Matasci, M. C., Bergstrom, C. T. & Lachmann, M. 2010. The fitness value of information. *Oikos* 119:219–230. DOI: 10.1111/j.1600-0706.2009.17781.x.
- Janisch, J., Pevný, T. & Lisý, V. 2020. Classification with Costly Features as a Sequential Decision-Making Problem. *Machine Learning* 109:1587–1615. DOI: 10.1007/s10994-020-05874-8.
- Kassen, R. 2002. The experimental evolution of specialists, generalists, and the maintenance of diversity. *Journal of Evolutionary Biology* 15:173–190. DOI: 10.1046/j.1420-9101.2002.00377.x.
- Nan, F. & Saligrama, V. 2017. Adaptive Classification for Prediction Under a Budget. *Advances in Neural Information Processing Systems* 30.
- Rivoire, O. & Leibler, S. 2011. The Value of Information for Populations in Varying Environments. *Journal of Statistical Physics* 142:1124–1166. DOI: 10.1007/s10955-011-0166-2.
- Silva, R. & Clarke, A. R. 2020. The sequential cues hypothesis: a conceptual model to explain host location and ranking by polyphagous herbivores. *Insect Science* 27:1136–1147. DOI: 10.1111/1744-7917.12719.
- Sun, H. & Jafar, S. A. 2019. On the Capacity of Computation Broadcast. arXiv:1903.07597.
