# Conditional decision topology separates information content from ecological accessibility

Draft v0.4 — information-accessibility synthesis candidate

## Abstract

Environmental heterogeneity has amount, grain and pattern, but ecological decisions also have **conditional topology**: the result of an early observation can change which later distinction matters. We separate two operational objects. For a finite deterministic task, the minimum fixed cue cost satisfies exactly
\[
C_F=\min_{S:I(T;Q_S)=H(T)} c(S),
\]
so fixed resolution is a static subset-information problem. Adaptive resolution is instead an outcome-resolved Bellman problem. We construct two target maps on the same 12-state, four-cue physical environment in which every binary cue is exactly 50/50 balanced. The tasks have identical target prevalence and, more strongly, the same complete Shannon entropy vector over the target and all four cues; equivalently, every named cue subset has identical mutual information \(I(T;Q_S)\). Both have \(C_F=4\), yet one has \(C_A=4\) and the other \(C_A=3\). Their \(r\)-fold products preserve complete Shannon entropic equivalence while giving \(C_F=4r\) in both tasks and \(C_A=4r\) versus \(3r\), so the adaptive-cost difference grows without bound. A separate exactly balanced family shows that the fixed-to-adaptive cost ratio itself can grow without bound when weaker information summaries are matched. A finite ecological budget \(B\) converts these structural differences into predicted feasibility differences when \(C_A\le B<C_F\). Routeability is therefore relational: information content describes what can be known jointly, whereas conditional decision topology determines what must be learned jointly before action.

## Keywords

environmental heterogeneity; ecological information; sequential decision making; adaptive feature acquisition; niche breadth; routeability; information processing; cue acquisition

---

## 1. Introduction

Environmental heterogeneity is a central ecological explanatory variable, but ecology does not reduce it to a single scalar. Classical and modern theory distinguish not only how much variation exists but also its spatial or temporal pattern and grain. Likewise, information ecology and information-fitness theory ask how environmental information changes decisions, growth and selection. The starting point of this paper is therefore not that ecology has ignored structure.

A second established literature makes the acquisition problem explicit. Sequential host-location models propose that organisms can use broad and specific cues in stages, and costly-feature classification formalizes prediction in which different features are acquired for different samples, in different orders, under acquisition costs or budgets. Adaptive feature acquisition is therefore prior art, as is the general value of collecting information before action. Our contribution is not the observation that conditional sampling can be useful. Bernays and Wcislo linked resource specialization to information-processing costs, Silva and Clarke proposed sequential cue use in polyphagous host location, and modern costly-feature methods explicitly choose later measurements from earlier observations (Bernays & Wcislo 1994; Silva & Clarke 2020; Contardo et al. 2016; Janisch et al. 2020; Nan & Saligrama 2017).

A particularly close recent neighbor makes the information-theoretic overlap explicit. Li, Dhali & Bouma (2026) use partial information decomposition to study when pairwise synergy helps active feature acquisition, combine pairwise joint information with conditional information evaluated at realized feature values, and include controlled fixed-information comparisons. Thus neither synergy-aware acquisition nor outcome-conditioned information scores are novelty claims here. The unresolved issue we isolate is stricter: whether two tasks can be statically indistinguishable to the entire Shannon entropy vector yet differ in the exact optimal cost of adaptive resolution.

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

## 5. Complete static subset information can still miss adaptive accessibility

The asymptotic construction proves an unbounded routeability separation while
holding the physical cue environment, target prevalence, target entropy and
full-vocabulary target information fixed. A stronger finite construction can
hold **every named static subset mutual information** fixed as well.

Consider one common 12-state environment with four unit-cost binary cues.
Every cue is exactly 6/6 balanced. Define two target maps \(T_A\) and \(T_B\)
on the same states and cue-outcome matrix. Both have target multiplicities
\((8,4)\), hence the same target entropy.

Under the uniform world prior, for every one of the \(2^4\) named cue subsets,

\[
\boxed{
I(T_A;Q_S)=I(T_B;Q_S)
\qquad
\forall S\subseteq\{q_0,q_1,q_2,q_3\}.
}
\]

The equality is exact. It is certified by expressing
\(12H(T\mid Q_S)\) as an integer linear combination of prime logarithms for
each subset, rather than by matching rounded floating-point values.

The common profile has

\[
H(T)=0.9182958\ldots \text{ bits},
\]

no three-cue subset reaches \(H(T)\), and the full four-cue set does.
Consequently,

\[
C_F(T_A)=C_F(T_B)=4.
\]

Yet exact adaptive optimization gives

\[
\boxed{
C_A(T_A)=4,
\qquad
C_A(T_B)=3.
}
\]

For \(T_A\), every possible first cue leaves at least one branch with residual
adaptive depth three. For \(T_B\), either \(q_2\) or \(q_3\) leaves residual
depth two after both outcomes.

Therefore

\[
\boxed{
\{I(T;Q_S):S\subseteq Q\}
\not\Rightarrow C_A.
}
\]

Because the physical cue matrix is identical, every cue-only entropy \(H(Q_S)\)
also matches. Combining that fact with the exact equality of
\(H(T\mid Q_S)\) gives

\[
H_A(T,Q_S)=H_B(T,Q_S)
\qquad
\forall S\subseteq Q.
\]

Every subset of \((T,q_0,q_1,q_2,q_3)\) is either cue-only or has the form
\((T,Q_S)\). Therefore the stronger equality holds:

\[
\boxed{
H_A(U)=H_B(U)
\qquad
\forall U\subseteq\{T,q_0,q_1,q_2,q_3\}.
}
\]

The twins are thus **Shannon-entropically equivalent** across all 32 variable
subsets but adaptively inequivalent.

This result sharpens the paper's information claim. The distinction is not
merely between low-order information and higher-order information. The complete Shannon entropy vector is enough to recover the static subset
information and therefore the fixed burden, but it can still average over the
outcome-specific arrangement that determines adaptive burden.

The earlier depth-two and depth-three controls matching pairwise
target-cue information remain useful finite stress tests, but they are now
supporting results rather than the strongest information-matching theorem.

The finite separation amplifies. Take \(r\) independent coordinate copies,
use the \(r\)-tuple of coordinate targets as the focal action, and retain
coordinate-local cue sets. Entropies factor across coordinates, so the complete
Shannon entropy vector remains identical between the two product tasks.
Worst-case exact fixed and adaptive costs are additive under this Cartesian
product, giving

\[
(C_A,C_F)_{A^{\otimes r}}=(4r,4r),
\qquad
(C_A,C_F)_{B^{\otimes r}}=(3r,4r).
\]

Therefore the adaptive-cost difference and the routeability-gap difference both
grow as \(r\). This is an unbounded **additive** separation under complete
entropic equivalence. It is distinct from the separate asymptotic routing
family, which yields an unbounded **multiplicative** \(C_F/C_A\) ratio under
weaker information matching.

---

## 6. Fixed information and adaptive information are different mathematical objects

### 6.1 Fixed resolution is exactly a static subset-information optimization

Give every represented world strictly positive probability. For any fixed cue
bundle \(S\),

\[
S\text{ resolves }T
\iff
H(T\mid Q_S)=0
\iff
I(T;Q_S)=H(T).
\]

Hence

\[
\boxed{
C_F=
\min_{S\subseteq Q}
\left\{
c(S):
I(T;Q_S)=H(T)
\right\}.
}
\]

This equivalence is structural. If a bundle fails to resolve the target, at
least two positive-probability worlds with different targets share a cue
signature, forcing positive conditional entropy. Conversely a resolving bundle
has target-pure signatures.

Thus the complete named subset-information function is sufficient for
\(C_F\).

### 6.2 Adaptive resolution requires realized outcomes

Let

\[
h=(q_1=a_1,\ldots,q_r=a_r)
\]

be one realized observation history and let \(V(h)\) be the minimum remaining
worst-case cost. Then

\[
V(h)=0
\quad\text{when}\quad
H(T\mid h)=0,
\]

and otherwise

\[
\boxed{
V(h)=
\min_{q\notin h}
\left[
c(q)+
\max_{a:P(q=a\mid h)>0}
V(h,q=a)
\right].
}
\]

Therefore

\[
C_A=V(\varnothing).
\]

Conditional mutual information

\[
I(T;q\mid h)
=
H(T\mid h)
-
\sum_a P(a\mid h)H(T\mid h,q=a)
\]

is an average immediate entropy reduction. The exact worst-case adaptive
problem additionally retains each realized child separately, because different
outcomes can change which future cue is relevant.

The existing routing witness makes this explicit. A context cue can satisfy

\[
I(T;\mathrm{context})=0
\]

while its two outcomes reverse the informational role of the later assays:

\[
I(T;\mathrm{assay0}\mid \mathrm{context}=0)=1,
\qquad
I(T;\mathrm{assay1}\mid \mathrm{context}=0)=0,
\]

and

\[
I(T;\mathrm{assay0}\mid \mathrm{context}=1)=0,
\qquad
I(T;\mathrm{assay1}\mid \mathrm{context}=1)=1.
\]

The routing cue need not reveal the target directly. It can reveal **where the
target information is**.

### 6.3 Corrected sufficiency ladder

The new construction fills the previous gap between pairwise information and
the complete action-conditioned table.

1. State and cue counts are insufficient.
2. Cue marginals and the complete cue-only distribution are insufficient.
3. Target prevalence, target entropy and full-vocabulary target information are
   insufficient.
4. Pairwise target-cue information profiles can be insufficient.
5. The complete named static subset-information function
   \[
   F(S)=I(T;Q_S)
   \]
   is sufficient for \(C_F\), but insufficient for \(C_A\). The matched
   twins satisfy the stronger condition that the complete Shannon entropy
   vector over target and cues is identical.
6. Outcome-resolved conditional continuation geometry retains the realized
   histories needed for the Bellman recursion for \(C_A\).
7. The complete table
   \[
   (w,T(w),q_1(w),\ldots,q_m(w))
   \]
   plus cue costs directly specifies the deterministic finite task.

The theory therefore does not claim that topology is hidden in principle. It
identifies exactly where averaging across unrealized branches loses an
operational property.

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

### 10.1 Partial information decomposition and synergy

Multivariate information theory already distinguishes unique, redundant and
synergistic information. Williams and Beer (2010) introduced partial
information decomposition, with XOR as the canonical case in which neither
source alone contains target information but the pair does.

Li, Dhali & Bouma (2026) directly connect this language to active feature
acquisition. Their state-dependent SynAFA policy uses pairwise joint
information and conditional information evaluated at realized feature values,
and their synthetic analyses include a fixed-total-pair-information control.
Accordingly, this manuscript does not claim that PID, synergy or
realized-value conditioning are new ingredients in sequential acquisition.

Routeability is not a synonym for synergy.

A two-cue XOR/XNOR task can contain purely joint target information while still
requiring exactly the same two observations adaptively and non-adaptively:

\[
C_A=C_F=2.
\]

Conversely, the all-subset matched theorem above shows that two tasks can have
the same complete static Shannon subset-information function and still differ
in adaptive cost.

This does not claim that every possible PID construction is identical for the
matched twins. PID measures can use finer distributional information, and
multivariate PID definitions remain non-unique. The defensible distinction is:

> PID and related decompositions describe how target information is distributed
> among sources; routeability asks how realized source outcomes reorganize the
> future acquisition problem under cost.

### 10.2 Active feature acquisition

Adaptive feature acquisition is established in machine learning. EDDI, for
example, selects additional measurements using expected information gain
(Ma et al. 2019). Recent work explicitly describes active feature acquisition
as instance-wise sequential measurement and identifies greedy conditional
mutual information as an established, but potentially myopic, acquisition rule
(Norcliffe et al. 2025).

Sequential value-of-information problems are likewise established in decision
analysis. Uniform separating systems and generic adaptive-versus-non-adaptive
search are established in combinatorics.

The manuscript therefore does **not** claim novelty for:
- sequentially selecting observations;
- conditional mutual information;
- costly feature acquisition;
- adaptive versus fixed search;
- synergy or multivariate information decomposition.

The present contribution is narrower:

> an exact ecological decision construction in which the physical cue
> environment is held fixed, every cue can be perfectly balanced, and the
> complete Shannon entropy vector over target and cues can be held fixed while
> the focal action map changes optimal worst-case adaptive accessibility.

The separate asymptotic construction then shows that the ecological consequence
can grow without bound under weaker information matching.

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

Environmental information has two operational layers that are easy to
conflate.

The first is **static content**: which fixed sets of cues jointly contain the
target information. In the deterministic exact-resolution model this layer is
completely characterized by the subset-information function, because

\[
C_F=
\min_{S:I(T;Q_S)=H(T)}c(S).
\]

The second is **adaptive accessibility**: after one particular outcome occurs,
which distinction remains necessary next. This is an outcome-resolved Bellman
object.

The two layers are not equivalent. We constructed two tasks with the same
physical cue matrix, exact balance of every cue, the same target prevalence and
the same complete Shannon entropy vector, yet different adaptive costs. A separate family shows that routeability advantages can become
arbitrarily large.

A finite ecological budget converts this structural distinction into a
feasibility prediction.

The resulting principle is:

\[
\boxed{
\text{Static information tells us what can be known together; routeability tells us what must be learned together.}
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
- Li, J., Dhali, M. A. & Bouma, H. R. 2026. When Does Synergy Help Active Feature Acquisition? A PID-Based Study. arXiv:2609.32301.
- Kassen, R. 2002. The experimental evolution of specialists, generalists, and the maintenance of diversity. *Journal of Evolutionary Biology* 15:173–190. DOI: 10.1046/j.1420-9101.2002.00377.x.
- Ma, C., Tschiatschek, S., Palla, K., Hernandez-Lobato, J. M., Nowozin, S. & Zhang, C. 2019. EDDI: Efficient Dynamic Discovery of High-Value Information with Partial VAE. *Proceedings of Machine Learning Research* 97:4234–4243.
- Nan, F. & Saligrama, V. 2017. Adaptive Classification for Prediction Under a Budget. *Advances in Neural Information Processing Systems* 30.
- Norcliffe, A. L. I., Lee, C., Imrie, F., van der Schaar, M. & Lio, P. 2025. Stochastic Encodings for Active Feature Acquisition. *Proceedings of Machine Learning Research* 267:46784–46814.
- Rivoire, O. & Leibler, S. 2011. The Value of Information for Populations in Varying Environments. *Journal of Statistical Physics* 142:1124–1166. DOI: 10.1007/s10955-011-0166-2.
- Silva, R. & Clarke, A. R. 2020. The sequential cues hypothesis: a conceptual model to explain host location and ranking by polyphagous herbivores. *Insect Science* 27:1136–1147. DOI: 10.1111/1744-7917.12719.
- Sun, H. & Jafar, S. A. 2019. On the Capacity of Computation Broadcast. arXiv:1903.07597.
- Williams, P. L. & Beer, R. D. 2010. Nonnegative Decomposition of Multivariate Information. arXiv:1004.2515.
