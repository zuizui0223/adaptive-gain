# Conditional decision topology separates information content from ecological accessibility

Draft v0.4 — information-accessibility synthesis candidate

## Abstract

Ecological information is often summarized by amount, but accessibility depends on how observations reorganize what must be learned next. For a deterministic task, fixed resolution satisfies
\[
C_F=\min_{S:I(T;Q_S)=H(T)} c(S),
\]
whereas adaptive resolution is an outcome-resolved Bellman problem. We construct paired 12-state tasks with identical physical cue matrices and complete Shannon entropy vectors but different costs: \((C_A,C_F)=(4,4)\) versus \((3,4)\). Their \(r\)-fold products preserve entropic equivalence while the adaptive-cost difference grows as \(r\). A separate balanced family gives an unbounded fixed-to-adaptive ratio under weaker matching. Reanalysis of public *Bombus* data shows costly information acquisition increases when unaided decisions are difficult, while secondary cues are recruited when primary cues are insufficient. A finite budget exposes the ecological consequence when \(C_A\le B<C_F\). Routeability therefore separates static information content from sequential accessibility.

## Keywords

environmental heterogeneity; ecological information; sequential decision making; adaptive feature acquisition; niche breadth; routeability; information processing; cue acquisition

---

## 1. Introduction

Environmental heterogeneity is a central ecological explanatory variable, but ecology does not reduce it to a single scalar. Classical and modern theory distinguish not only how much variation exists but also its spatial or temporal pattern and grain. Likewise, information ecology and information-fitness theory ask how environmental information changes decisions, growth and selection. The starting point of this paper is therefore not that ecology has ignored structure.

A second established literature makes the acquisition problem explicit. Sequential host-location models propose that organisms can use broad and specific cues in stages, and costly-feature classification formalizes prediction in which different features are acquired for different samples, in different orders, under acquisition costs or budgets. Adaptive feature acquisition is therefore prior art, as is the general value of collecting information before action. Our contribution is not the observation that conditional sampling can be useful. Bernays and Wcislo linked resource specialization to information-processing costs, Silva and Clarke proposed sequential cue use in polyphagous host location, and modern costly-feature methods explicitly choose later measurements from earlier observations (Bernays & Wcislo 1994; Silva & Clarke 2020; Contardo et al. 2016; Janisch et al. 2020; Nan & Saligrama 2017).

A particularly close recent neighbor makes the information-theoretic overlap explicit. Li, Dhali & Bouma (2026) use partial information decomposition to study when pairwise synergy helps active feature acquisition, combine pairwise joint information with conditional information evaluated at realized feature values, and include controlled fixed-information comparisons. Thus neither synergy-aware acquisition nor outcome-conditioned information scores are novelty claims here. The unresolved issue we isolate is stricter: whether two tasks can be statically indistinguishable to the entire Shannon entropy vector yet differ in the exact optimal cost of adaptive resolution.

The exact-resolution primitives are also classical. Adaptive identification by
binary or multiway decision trees and fixed identification by separating/test
systems have long-standing theories (Garey 1972; Katona 1966; Hyafil & Rivest
1976; Chakaravarthy et al. 2009; Moshkov & Zielosko 2011). We therefore do not
claim novelty for \(C_A\), \(C_F\), optimal decision trees, separating systems,
or generic adaptive-versus-fixed gaps. The new question is what remains
unidentified when these classical operational costs are compared with complete
static information summaries in an ecological task.


The ecological consequence of that mathematical distinction is especially relevant because many empirical summaries of environmental information are **distributional**: richness, frequencies, variance, cue entropy, pairwise association or the total target information available in a cue set. Even when such summaries are rich, they need not answer an operational question:

> after one cue outcome is observed, which distinctions remain necessary before the organism can act?

We call this dependency structure **conditional decision topology**. The term does not mean temporal order alone. A fixed sequence of observations and an outcome-contingent decision tree are different objects: topology concerns which later distinction becomes relevant on each branch. The same physical environment can therefore induce different topologies for different focal actions.

This distinction also has mathematical precedent outside ecology. Information theory contains examples in which two problems share the same entropy for every subset of their variables yet have different operational capacities, showing that entropic structure need not be a complete operational invariant. We therefore do not claim that this paper is the first theory in which entropy misses consequential structure (Sun & Jafar 2019). The ecological question is narrower and constructive: **can environmental states, the complete physical cue matrix, target prevalence, target entropy and total available target information all be held fixed while the acquisition cost of the focal action changes sharply?**

We answer yes. For a declared ecological task, let \(C_A\) denote the minimum worst-case cue cost when later cues may depend on earlier outcomes, and let \(C_F\) denote the minimum cost of a fixed resolving cue set. We construct paired tasks on the same physical cue environment. Only the map from cue-defined states to the focal action changes. Nevertheless, the fixed-to-contingent acquisition geometry separates without bound as the construction grows, whereas the matched control requires only two fixed cues.

The biological coupling is supplied by a separate natural-history quantity: an observation budget \(B\). This budget may represent time before a host departs, handling opportunity, predator exposure, attention or another hard or effectively hard ceiling. Recent bumble-bee experiments also show that animals can voluntarily pay a reward cost to obtain predictive information when uncertain (Yuan et al. 2026), supporting the biological plausibility of treating information acquisition as costly without constituting a test of routeability itself. Conditional topology changes guaranteed performance precisely when the budget lies between the two structural requirements,

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

## 7. Conditional accessibility can bound evolutionary reachability

The structural distinction becomes evolutionarily consequential only after a
biological lift is specified. Let the state-specific routeability gap be

\[
g_i=C_F(i)-C_A(i)\ge0
\]

and consider two ecological states with ordered contrast
\(\Delta g=g_2-g_1\ge0\). Suppose the local selection contribution is
\(s_i=f(g_i)-\kappa\), where \(f\) is nondecreasing and \(L\)-Lipschitz on the
relevant domain. Then

\[
0\le\Delta s\le L\Delta g.
\]

For a local eco-evolutionary feedback with positive conversion scale
\(B_f=-\beta e>0\), distinguished from the ecological observation budget
\(B\), the loop gain therefore satisfies

\[
\boxed{G\le B_fL\Delta g.}
\]

In the generalized two-dimensional local response used here, evolutionary
persistence \(\alpha\) and ecological memory \(\phi\) give the exact
complex-eigenpair threshold

\[
G_{\rm osc}
=
\frac{(\alpha-\phi)^2}{4(1-\phi)}.
\]

Hence a stable oscillatory response is possible only if

\[
\boxed{
\Delta g>
\frac{G_{\rm osc}}{B_fL}.
}
\]

More strongly, if an entire architecture class satisfies \(0\le g_i\le
q_{\max}\) and \(B_fLq_{\max}\le G_{\rm osc}\), oscillatory feedback is
unreachable for that class. This is a **no-go theorem**, not a sufficiency
claim: crossing the structural threshold does not guarantee oscillation, and
\(B_f,L,\alpha,\phi\) are not estimated from the public bee data. Its role is to
show that information accessibility can delimit an evolutionary possibility
space once a state-dependent ecological feedback is specified.

---

## 8. Ecological scope

The immediate ecological consequence concerns **processing burden and
accessibility**, not evolved niche breadth by itself. Equal nominal niche
breadth can impose different information costs when early cues route encounters
into small branch-specific problems. Thus broader resource use should be less
constrained by information acquisition when relevant alternatives are routeable
within the organism's observation budget. Morphology, phenology and encounter
opportunity still define upstream compatibility; routeability can act as an
additional filter on which compatible interactions are behaviorally accessible.

This framework complements rather than replaces established heterogeneity
dimensions such as amount, grain and spatial or temporal pattern (Kassen
2002). Predicting evolved specialist/generalist outcomes still requires
fitness trade-offs and evolutionary dynamics; the no-go result above supplies
one explicit bridge when such dynamics are specified. Diversity-stability,
community resilience and ecosystem-function stability remain downstream:
the present model contains no abundance dynamics or community stability
functional from which those conclusions could follow.

---

## 9. Measurement: recover structure before summarizing it

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

## 10. Bombus as a single-system empirical anchor

The deterministic theorem is intentionally stronger than any one public
behavioural dataset located so far. We therefore use *Bombus* not as an
anecdotal example, but as a single-system empirical anchor. The primary
published anchor is the cue-allocation experiment of Spaethe et al. (2026);
the recent Yuan et al. (2026) preprint supplies a separate, provisional test
of costly active acquisition. Across these and other experiments in the same
genus, the evidence tests distinct operational ingredients rather than the
full theorem.

### 10.1 Secondary cues are recruited when primary information is insufficient

Spaethe et al. (2026) trained *B. terrestris* on combined colour and
pattern/shape cues and then used cue-conflict tests to separate their
contributions. We prospectively defined a secondary-cue recruitment index

\[
R=1-p_{\rm colour}.
\]

Using the individual values in the authors' public analysis repository,
secondary-cue recruitment was approximately

\[
R_{\rm easy}=0.026
\]

when the primary colour discrimination was easy, but

\[
R_{\rm hard}=0.374
\]

when the colour discrimination was difficult, a difference of about 0.349.
Pattern and shape experiments showed the same direction independently.

This result directly supports the narrower prediction that the same nominal
cue vocabulary need not impose the same acquired information burden: bees
largely ignore a secondary attribute when the primary cue is sufficient and
recruit it when primary information is insufficient. The attributes were
simultaneously available, however, so this is not a within-encounter
branch-specific next-cue policy.

### 10.2 Costly contingent acquisition

The bioRxiv preprint by Yuan et al. (2026) gave *Bombus terrestris* a two-stage task in which bees
could voluntarily land on an information-request platform before a mandatory
discrimination. A correct choice without requesting information earned 30%
sucrose, whereas a correct post-request choice earned only 15%, so information
acquisition carried an explicit reward cost.

We independently reaggregated all 19,200 public trial records from 192 bees.
On Regular trials, the probability of requesting information increased from

\[
0.096
\]

on Easy trials to

\[
0.469
\]

on Hard trials and

\[
0.716
\]

on Impossible trials. The gradient was also within-individual: all 192 bees
requested more information on Hard than Easy trials, and 181/192 increased
again from Hard to Impossible. Post-request accuracy remained near \(0.93\) at all three difficulty levels.
The public CSV also reports non-request accuracy of \(0.750\), \(0.494\) and
\(0.207\) from Easy to Impossible. We do not use the final value as biological
evidence: the 0.207 Impossible value is unexpectedly below chance for a binary
choice and is not presently reconciled with the task description. The robust
bridge used here is therefore the difficulty-dependent decision to pay for
information, not an inferred 0.207-to-0.93 accuracy rescue.

The experiment also contains Random Free-Cue trials in which the predictive
cue is supplied independently of platform landing. This produces a strong
access-mode interaction. Across the same 192 bees, the Easy-to-Impossible
increase in landing probability on Regular trials is reversed when information
is supplied freely; the within-bee difference-in-differences is 1.018 on
average and is positive for 191/192 bees (exact one-sided sign test
\(p=3.1\times10^{-56}\)). Thus the Regular-trial difficulty gradient is not
a generic motor response to difficulty: it appears specifically when landing
is required to obtain information. Because Yuan et al. (2026) is a bioRxiv preprint, we treat this result as a
reproducible but provisional component test. The dataset directly supports
**need-dependent costly information acquisition**, although only one optional
predictive cue is available and the experiment does not identify the exact
\(C_A<C_F\) theorem.

### 10.3 Sequential sensory access is biologically real

MaBouDi et al. (2025) provide public high-speed trajectories showing that
bumblebees inspect restricted diagnostic regions of visual patterns before
accepting or rejecting them. The scanned regions differ between patterns,
demonstrating selective sequential sensory sampling rather than mandatory
parallel access to the whole stimulus. The pattern-specific scanning strategy
also persists when reward and punishment valence are reversed, providing a
useful negative control: a simple relabelling of outcomes does not by itself
force a new acquisition architecture.

Public match-to-sample data provide the relational action-map component:
in Chow et al. (2022), platform/sample colour determines which subsequently
available ball is the rewarding action. Essenberg et al. (2015) provide the
closest biological precedent for branch-specific cue relevance: flower size
predicts reward in one flower-type branch but is uninformative in another, and
bees learn to use size only where it carries value.

Together these studies let one biological system carry the theory from
abstraction to mechanism: bumblebees can pay for information, recruit
additional cues according to information need, sample sensory information
sequentially, and switch later actions according to earlier context. They do
**not** constitute a single direct test of the exact relational theorem.
Instead, they show that every major biological operation required by the
theory already exists within *Bombus*. The remaining experiment is therefore
a narrow composition test rather than a leap from mathematics to biology.

---

## 11. Prospective direct test

The remaining causal test is narrow: hold one physical cue matrix fixed, alter
the focal action map so that different early outcomes make different later cues
relevant, impose costly cue acquisition under a shared finite budget, and test
the predicted architecture-by-access interaction. The preregisterable
four-state design and the stronger exact-balanced ten-state stress test are
specified in the Supplement.

---

## 12. Prior-art boundary

### 12.1 Decision trees and separating systems

The finite identification problem itself is established theory. Katona (1966)
developed separating systems for fixed collections of tests. Garey (1972)
formulated binary identification with test costs and gave a dynamic-programming
solution for minimum expected testing cost; Hyafil & Rivest (1976) established
NP-completeness for constructing an expected-test-optimal binary decision tree.
Chakaravarthy et al. (2009) likewise studied entity identification from an
attribute table under an average-test objective, while Moshkov & Zielosko
(2011) develop a broader framework of tests, decision rules and trees,
including complexity bounds. These works are direct prior art for fixed
separating systems and adaptive decision trees, but their objectives are not
identical to our minimum worst-case exact-resolution costs. Our claim is not a
new decision-tree problem. It is the non-identification result that even the
complete Shannon entropy vector can determine the fixed exact-resolution
burden while failing to determine the adaptive worst-case burden, together
with the ecological interpretation through an action-conditioned cue map.

### 12.2 Static entropy profiles

The complete static subset-information function is not itself a new object.
Forré (1990) defined an entropy profile for Boolean functions using the
conditional entropy of a function output given subsets of its input variables.
With fixed target entropy, that family is equivalent to scanning
\(I(T;Q_S)\) across cue subsets. Youssef & Tavares (2004) subsequently studied
decision-tree complexity of cryptographic Boolean functions while also
considering Boolean-function entropy profiles.

Our claim therefore begins **after** those objects are fixed. The matched twins
show that even the complete Shannon entropy vector over target and cues does
not identify optimal adaptive worst-case resolution cost; the direct-product
construction makes that adaptive-cost difference arbitrarily large.

### 12.3 Partial information decomposition and synergy

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

### 12.4 Active feature acquisition

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

Under the strongest matching condition, direct products make the adaptive-cost
difference grow without bound additively. A separate exactly balanced routing
family gives the stronger unbounded multiplicative (C_F/C_A) separation
under weaker information matching.

---

## 13. Deterministic scope and next theory

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

## 14. Conclusion

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
- Garey, M. R. 1972. Optimal Binary Identification Procedures. *SIAM Journal on Applied Mathematics* 23:173–186. DOI: 10.1137/0123019.
- Hyafil, L. & Rivest, R. L. 1976. Constructing optimal binary decision trees is NP-complete. *Information Processing Letters* 5:15–17. DOI: 10.1016/0020-0190(76)90095-8.
- Katona, G. O. H. 1966. On separating systems of a finite set. *Journal of Combinatorial Theory* 1:174–194. DOI: 10.1016/S0021-9800(66)80024-8.
- Chakaravarthy, V. T., Pandit, V., Roy, S. & Sabharwal, Y. 2009. Approximating Decision Trees with Multiway Branches. In *Automata, Languages and Programming*, Part I, LNCS 5555:210–221. DOI: 10.1007/978-3-642-02927-1_19.
- Moshkov, M. & Zielosko, B. 2011. *Combinatorial Machine Learning: A Rough Set Approach*. Springer. DOI: 10.1007/978-3-642-20995-6.
- Li, J., Dhali, M. A. & Bouma, H. R. 2026. When Does Synergy Help Active Feature Acquisition? A PID-Based Study. arXiv:2609.32301.
- Kassen, R. 2002. The experimental evolution of specialists, generalists, and the maintenance of diversity. *Journal of Evolutionary Biology* 15:173–190. DOI: 10.1046/j.1420-9101.2002.00377.x.
- Ma, C., Tschiatschek, S., Palla, K., Hernandez-Lobato, J. M., Nowozin, S. & Zhang, C. 2019. EDDI: Efficient Dynamic Discovery of High-Value Information with Partial VAE. *Proceedings of Machine Learning Research* 97:4234–4243.
- Nan, F. & Saligrama, V. 2017. Adaptive Classification for Prediction Under a Budget. *Advances in Neural Information Processing Systems* 30.
- Norcliffe, A. L. I., Lee, C., Imrie, F., van der Schaar, M. & Lio, P. 2025. Stochastic Encodings for Active Feature Acquisition. *Proceedings of Machine Learning Research* 267:46784–46814.
- Rivoire, O. & Leibler, S. 2011. The Value of Information for Populations in Varying Environments. *Journal of Statistical Physics* 142:1124–1166. DOI: 10.1007/s10955-011-0166-2.
- Silva, R. & Clarke, A. R. 2020. The sequential cues hypothesis: a conceptual model to explain host location and ranking by polyphagous herbivores. *Insect Science* 27:1136–1147. DOI: 10.1111/1744-7917.12719.
- Sun, H. & Jafar, S. A. 2019. On the Capacity of Computation Broadcast. arXiv:1903.07597.
- Forré, R. 1990. Methods and instruments for designing S-boxes. *Journal of Cryptology* 2:115–130. DOI: 10.1007/BF00190799.
- Youssef, A. M. & Tavares, S. E. 2004. Decision trees of cryptographic Boolean functions. *Canadian Conference on Electrical and Computer Engineering* 1:401–404. DOI: 10.1109/CCECE.2004.1345040.
- Yuan, L., He, Y., Ye, Q., Lin, L., Yuan, R., Wang, Q. & Chen, S. 2026. Uncertainty-Guided Decision-Making in Bumble Bees. bioRxiv. DOI: 10.64898/2026.09.15.751944.
- Spaethe, J. et al. 2026. Bees flexibly adjust decision strategies to information content in a foraging task. *Science Advances*. DOI: 10.1126/sciadv.adw9320.
- MaBouDi, H., Richter, J., Guiraud, M.-G., Roper, M., Marshall, J. A. R. & Chittka, L. 2025. Active vision of bees in a simple pattern discrimination task. *eLife* 14:e106332. DOI: 10.7554/eLife.106332.
- Chow, P. K. Y., Lehtonen, T. K., Näreaho, V. & Loukola, O. J. 2022. Prior associations affect bumblebees' generalization performance in a tool-selection task. *iScience* 25:105466. DOI: 10.1016/j.isci.2022.105466.
- Essenberg, C. J. et al. 2015. The value of information in floral cues: bumblebee learning of floral size cues. *Behavioral Ecology* 26:1335–1344. DOI: 10.1093/beheco/arv061.
- Williams, P. L. & Beer, R. D. 2010. Nonnegative Decomposition of Multivariate Information. arXiv:1004.2515.
