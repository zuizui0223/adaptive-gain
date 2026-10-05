# Conditional decision topology separates ecological diversity from decision complexity

Draft v0.4 — information-accessibility synthesis candidate

## Abstract

Generalist animals face resources, yet sequential decisions can avoid simultaneous comparison. What determines decision complexity? For a deterministic choice, let \(C_F\) be the minimum cost of a fixed resolving cue set and \(C_A\) the minimum worst-case cost when later cues may depend on earlier outcomes. We construct paired 12-state tasks with identical physical cue matrices and complete Shannon entropy vectors but different costs: \((C_A,C_F)=(4,4)\) versus \((3,4)\). Thus resource diversity, cue diversity and complete static information do not determine sequential decision burden. A finite observation budget makes this difference ecological when \(C_A\le B<C_F\). In a temporal extension, a cue with no direct target information gains value when it predicts which later cue will be useful; the gain vanishes at temporal independence. Staged information use occurs across pollination, host finding, predator avoidance and patch foraging. Conditional decision topology separates ecological diversity from effective decision complexity.

## Keywords

environmental heterogeneity; ecological information; sequential decision making; adaptive feature acquisition; niche breadth; routeability; information processing; cue acquisition

---

---

## 1. Introduction

A long-standing problem in behavioural ecology is how animals make effective
choices when many resources, hosts or patches are available. This problem is
especially acute for generalists. The neural-constraints hypothesis predicts
that broad diet breadth can slow or degrade choice because more potential
resources must be discriminated in limited time (Bernays & Wcislo 1994;
Bernays 2001); specialist aphids, for example, make host-associated decisions
faster than closely related generalists (Bernays & Funk 1999). Yet natural foraging is rarely a single
simultaneous comparison among all alternatives. Decision ecology instead
emphasizes sequential and hierarchical choices, from habitat and patch
selection to the acceptance or rejection of particular resources (Stephens
2008).

This creates a basic unresolved question: **when does ecological diversity
actually become decision complexity?** If early observations eliminate most
alternatives or determine which cue matters next, a generalist need not
distinguish every resource and every attribute at once. The sequential-cues
hypothesis makes this idea explicit for polyphagous herbivores: broad cues can
first locate a host habitat, after which more specific cues rank a much smaller
set of candidates (Silva & Clarke 2020). Comparable staged information use is
widespread. Parasitoids commonly locate host habitat before host and host
suitability (Quilici & Rousse 2012), and multi-stage escape in fiddler crabs
acquires qualitatively different information about predation risk at successive
stages (Hemmi & Pfeil 2010). Sequential ecological decisions are therefore not
a special property of one taxon or sensory modality.

These examples point to a distinction between the number of alternatives in a
choice set and the comparisons an animal must actually make before acting. We
call the dependency among those comparisons **conditional decision topology**.
For a declared ecological action, let \(C_F\) be the minimum cost of a fixed
cue bundle that resolves the action in every represented state, and let
\(C_A\) be the minimum worst-case cost when later cues may depend on earlier
outcomes. Their difference
\[
g=C_F-C_A
\]
is the processing burden that contingent acquisition can avoid. The underlying
decision-tree and separating-system primitives are classical; the ecological
question is whether familiar descriptions of the choice environment determine
this burden.

We first ask whether two ecological decision problems can contain the same
static information but differ in adaptive cost. They can. Two tasks on one
identical physical cue matrix can have the same complete Shannon entropy vector
and the same fixed resolution cost, yet different adaptive costs. Cartesian
products amplify that additive difference, while a separate exactly balanced
family gives an unbounded fixed-to-adaptive ratio under weaker information
matching. Resource diversity, cue diversity and even complete static Shannon
information therefore do not determine sequential decision burden.

A finite natural-history budget \(B\)—time before a host departs, exposure to
predation, handling opportunity or another hard constraint—makes the
difference consequential. When
\[
C_A\le B<C_F,
\]
contingent sensing can guarantee a resolved action when fixed acquisition
cannot. We then ask the same question through time. In the minimal temporal
model, current context is useful when it predicts which later cue will be
useful, and routing value disappears at temporal independence. Published animal
systems show that the staged decisions assumed by these models occur in nature,
without serving as direct tests of the exact theorem.

---

## 2. Material and methods

---

### 2.1 Finite ecological decision tasks

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

---

### 2.2 Minimal temporal routing extension

To ask whether routing value survives beyond static exact resolution, we use the
repository's minimal four-world strict-gain core as a two-step decision problem.
A binary context \(C_t\) determines which of two specialist cues is diagnostic
for the target at the next step. In the symmetric temporal model,

\[
P(C_1=C_0)=\rho.
\]

The early routing cue reports the current context but has zero direct mutual
information with the final target. Policies are compared under a two-query
budget by exact Bayes accuracy. A noisy extension gives the routing cue
reliability \(a\ge1/2\) and each specialist cue reliability \(b\ge1/2\).
All temporal and noisy expressions are checked both by closed form and direct
latent-state enumeration.

### 2.3 Biological evidence synthesis

We used published animal-behaviour studies only to ask whether the operations
assumed by the theory occur in real ecological decisions. Evidence was grouped
by operation rather than taxon: sequential or hierarchical sampling,
conditional cue relevance, context-conditioned action, and costly information
acquisition. Bumblebees, parasitoids, fiddler crabs and patch-foraging animals
provide examples from pollination, host finding, predator avoidance and
resource exploitation. None of these studies estimates \(C_A\) or \(C_F\).

---

## 3. Results

---

### 3.1 Relational routeability theorem

For every integer \(d\ge2\), set

\[
k=2^d.
\]

Use the existing exactly-balanced binary cue environment with \(2k+2\) represented states and \(d+k\) unit-cost binary cues. Every cue divides the state set exactly in half.

We define two target maps on this **same cue environment**.

#### 3.1.1 Routeable target map

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

#### 3.1.2 Matched control target map

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

#### 3.1.3 Quantities held fixed

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

---

### 3.2 Exact common-budget ecological corollary

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

This is an exact feasibility contrast, not a claim that real animals will exhibit a one-unit behavioral effect (Fig. 2a). Its biological role is to localize where topology can matter: under extremely small budgets both strategies may fail; under large budgets both may succeed; the topology-sensitive region lies between the adaptive and fixed requirements.

---

---

### 3.3 Complete static information can miss adaptive accessibility

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

The finite separation amplifies. This amplification uses the composite target
\(\mathbf T=(T_1,\ldots,T_r)\), so it establishes an unbounded additive
separation under complete entropic equivalence as the action alphabet grows;
it does not establish an unbounded separation for a fixed binary action
alphabet. Take \(r\) independent coordinate copies,
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

The matched finite witness, continuation trees and direct-product amplification
are summarized in Fig. 1.

---

### 3.4 Fixed and adaptive information are different mathematical objects

#### 3.4.1 Fixed resolution is exactly a static subset-information optimization

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

#### 3.4.2 Adaptive resolution requires realized outcomes

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

#### 3.4.3 Raw ecological diversity can contain exact decision redundancy

The finite theory also gives an exact sense in which descriptively different
states or cues need not add decision complexity. At any unresolved state
\(A\), let \(S_A(q)\) be the set of remaining cross-target world pairs
separated by cue \(q\). If

\[
S_A(q)\supseteq S_A(r)
\qquad\text{and}\qquad
c(q)\le c(r),
\]

then \(q\) safely dominates \(r\): removing \(r\) at that state leaves the
optimal adaptive cost unchanged. On the world side, same-target worlds with
identical separation profiles against every remaining opposite-target world
can likewise be quotient-collapsed without changing \(C_A\) or \(C_F\).

Thus raw state richness and raw cue richness can strictly exceed
**decision-relevant richness** for the focal action. This is an exact
deterministic reduction, not a claim that taxonomically or phenotypically
distinct resources are generally interchangeable. It says only that
differences which never change a remaining target-relevant distinction are
irrelevant to the declared decision problem.

#### 3.4.4 Corrected sufficiency ladder

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

---

### 3.5 Routing value can come from predicting which cue will matter next

The deterministic results show that a cue can be useful by routing later
acquisition even when it does not itself resolve the target. The minimal
temporal model makes that distinction quantitative.

At a two-query budget, every fixed cue pair has optimal accuracy

\[
A_F^{(2)}=\frac34.
\]

If the first observation is used to choose which specialist cue to acquire
next, optimal contingent accuracy is

\[
A_A^{(2)}
=
\frac34+\frac{|2\rho-1|}{4}.
\]

Therefore the temporal routing advantage is

\[
\boxed{
G_{\rm time}
=
A_A^{(2)}-A_F^{(2)}
=
\frac{|2\rho-1|}{4}.
}
\]

The gain vanishes exactly at temporal independence, \(\rho=1/2\). Predictable
persistence and predictable alternation both create routing value; they simply
require opposite continuation rules (Fig. 2b). The relevant quantity is
therefore not persistence itself, but whether present information predicts
**which later cue will be useful**.

With symmetric observation noise, the same result factorizes exactly. If the
routing cue has reliability \(a\) and the specialist cues have reliability
\(b\),

\[
\boxed{
G_{\rm noisy}
=
\frac{|2\rho-1|(2a-1)(2b-1)}{4}.
}
\]

Temporal predictability, usable routing information and usable downstream
specialist information are thus multiplicative gates in this minimal model.
This is an expected-accuracy extension of the deterministic theory, not an
equivalence theorem for arbitrary noisy decision problems. Under a general
binary transition kernel, temporal dependence alone is also insufficient:
routing value is zero whenever the same specialist cue remains optimal after
every current context.

---


## 4. Discussion

---

### 4.1 From ecological diversity to effective decision complexity

The immediate ecological prediction is that **resource diversity and decision
complexity need not covary**. A broad diet can be cheap to manage when early
cues route encounters into small branch-specific problems, whereas a much
smaller resource set can remain costly if several distinctions must be
maintained simultaneously. Routeability therefore refines, rather than rejects,
the information-processing hypothesis of ecological specialization: the burden
relevant to generalism is not niche breadth itself but the structure of the
choice problem imposed by that breadth.

This distinction also changes how behavioural specialization should be read.
Flower constancy, host fidelity or repeated patch use can reduce processing
cost, but switching between nominal resource categories need not be costly when
the same decision route can be reused. Conversely, alternatives that look
similar in richness or Shannon diversity can impose different burdens when
their cue relevance is arranged differently across outcomes. The theory thus
predicts that behavioural costs should track route changes more closely than
taxonomic switches or option counts alone.

Morphology, phenology, encounter opportunity and physiological compatibility
still determine which interactions are possible upstream. Routeability acts
only after those constraints, by filtering which compatible alternatives are
behaviourally accessible within the available observation budget. Predicting
evolved niche breadth still requires fitness trade-offs and evolutionary
dynamics.

---

### 4.2 Measurement: recover structure before summarizing it

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

Without an action map, state-by-cue incidence or defensible acquisition costs,
a natural system cannot support a direct routeability estimate; richness or
entropy alone should not be substituted for the missing decision structure.

---

This action-first measurement pipeline is summarized in Fig. 2d.

---

### 4.3 Examples across ecological decision systems

Natural histories in several systems already have the staged form represented
by the model. None of the following systems directly measures \(C_A<C_F\);
they show instead that early observations can change which distinctions matter
later.

In bumblebees, Spaethe et al. (2026) found that *B. terrestris* relied almost
entirely on colour when colour discrimination was easy but recruited pattern or
shape when colour became difficult; in public individual-level values, the
predefined secondary-cue index \(R=1-p_{\rm colour}\) increased from 0.026
to 0.374. MaBouDi et al. (2025) showed selective sequential scanning of
diagnostic pattern regions; Essenberg et al. (2015) showed that the same size
cue could be informative in one flower context and ignored in another; and
Lotto & Chittka (2005) and Dale et al. (2005) showed context-conditioned later
choices. These results make *Bombus* one well-resolved example of a flexible
generalist in which cue relevance and information use depend on decision
state. At the broader foraging scale, flower constancy responds to multi-trait
variation and *B. impatiens* can switch among cue-regulated pollen-collection
routines across diverse floral resources (Gegear & Laverty 2005; Russell et
al. 2017). Comparable staged structure occurs outside pollination. Fruit-fly parasitoids
first locate host habitat and only then localize and assess hosts, using
different cues at successive stages (Quilici & Rousse 2012). Fiddler crabs
acquire qualitatively different information about predation risk during
successive stages of escape (Hemmi & Pfeil 2010). Patch foraging is naturally
formulated as repeated stay-or-leave decisions rather than a simultaneous
comparison among all future patches (Stephens 2008). Together, these systems
show that hierarchical information acquisition is not specific to one taxon,
sensory modality or ecological interaction.

These examples motivate a direct causal test: hold the physical cue matrix
fixed, change only the action-conditioned branch structure, and manipulate
costly cue access under a shared budget (Fig. 2c). The test is applicable
wherever early observations or actions determine which later distinctions
remain relevant.

---

### 4.4 Prior-art boundary

#### 4.4.1 Decision trees and separating systems

Fixed separating systems and adaptive identification trees are established
theory (Katona 1966; Garey 1972; Hyafil & Rivest 1976; Chakaravarthy et al. 2009;
Moshkov & Zielosko 2011). These works are direct prior art for the
operational primitives. Our claim is instead that complete static Shannon
information can determine the fixed burden while failing to determine the
adaptive worst-case burden in the same ecological cue environment.

#### 4.4.2 Static entropy profiles

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

#### 4.4.3 Partial information decomposition and synergy

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

#### 4.4.4 Active feature acquisition

Costly sequential feature acquisition, conditional information gain,
value-of-information policies and generic adaptive-versus-fixed search are all
prior art (Contardo et al. 2016; Nan & Saligrama 2017; Ma et al. 2019; Janisch
et al. 2020; Norcliffe et al. 2025). The present contribution is narrower:
one physical ecological cue environment can retain the same complete Shannon
entropy vector while different action maps produce different optimal
worst-case adaptive accessibility. Direct products make that difference
unbounded additively; the separate exact-balanced family gives an unbounded
multiplicative \(C_F/C_A\) ratio under weaker information matching.

---

---

### 4.5 Deterministic scope and next theory

The model is a structural limit: alternatives and cue outcomes are finite and
deterministic, cue costs are positive and additive, and the objective is
worst-case exact resolution. Extending the quantity-topology separation to
noisy cues and expected loss is a distinct problem closely adjacent to active
feature acquisition; we do not claim that extension here.

---

### 4.6 Conclusion

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
feasibility prediction. The temporal extension then shows that an early cue
need not predict the final target directly: it can be valuable because it
predicts which later cue will be useful. Published examples from pollination,
host finding, predator avoidance and patch foraging show that staged
information use is biologically widespread, while leaving the exact
routeability contrasts for direct future tests.

The resulting principle is:

\[
\boxed{
\text{Static information tells us what can be known together; routeability tells us what must be learned together.}
\]

---

The claim is therefore deliberately narrow: routeability is an exact
relational ecological axis for deterministic resolution, not a replacement
for entropy, environmental grain, network topology or stochastic
value-of-information theory.

---

## References

- Bernays, E. A. & Funk, D. J. 1999. Specialists make faster decisions than generalists: experiments with aphids. *Proceedings of the Royal Society B* 266:151–156. DOI: 10.1098/rspb.1999.0615.
- Stephens, D. W. 2008. Decision ecology: foraging and the ecology of animal decision making. *Cognitive, Affective, & Behavioral Neuroscience* 8:475–484. DOI: 10.3758/CABN.8.4.475.
- Gegear, R. J. & Laverty, T. M. 2005. Flower constancy in bumblebees: a test of the trait variability hypothesis. *Animal Behaviour* 69:939–949. DOI: 10.1016/j.anbehav.2004.06.029.
- Russell, A. L., Buchmann, S. L. & Papaj, D. R. 2017. How a generalist bee achieves high efficiency of pollen collection on diverse floral resources. *Behavioral Ecology* 28:991–1003. DOI: 10.1093/beheco/arx058.
- Quilici, S. & Rousse, P. 2012. Location of host and host habitat by fruit fly parasitoids. *Insects* 3:1220–1235. DOI: 10.3390/insects3041220.
- Hemmi, J. M. & Pfeil, A. 2010. A multi-stage anti-predator response increases information on predation risk. *Journal of Experimental Biology* 213:1484–1489. DOI: 10.1242/jeb.039925.

- Bernays, E. A. & Wcislo, W. T. 1994. Sensory capabilities, information processing, and resource specialization. *Quarterly Review of Biology* 69:187–204. DOI: 10.1086/418539.
- Bernays, E. A. 2001. Neural limitations in phytophagous insects: implications for diet breadth and evolution of host affiliation. *Annual Review of Entomology* 46:703–727. DOI: 10.1146/annurev.ento.46.1.703.
- Chakaravarthy, V. T., Pandit, V., Roy, S. & Sabharwal, Y. 2009. Approximating Decision Trees with Multiway Branches. In *Automata, Languages and Programming*, Part I, LNCS 5555:210–221. DOI: 10.1007/978-3-642-02927-1_19.
- Contardo, G., Denoyer, L. & Artières, T. 2016. Recurrent Neural Networks for Adaptive Feature Acquisition. ICONIP 2016. DOI: 10.1007/978-3-319-46675-0_65.
- Essenberg, C. J., Easter, R. A., Simmons, R. A. & Papaj, D. R. 2015. The value of information in floral cues: bumblebee learning of floral size cues. *Behavioral Ecology* 26:1335–1344. DOI: 10.1093/beheco/arv061.
- Lotto, R. B. & Chittka, L. 2005. Seeing the light: illumination as a contextual cue to color choice behavior in bumblebees. *Proceedings of the National Academy of Sciences USA* 102:3852–3856. DOI: 10.1073/pnas.0500681102.
- Dale, K., Harland, D. P., Manning-Jones, A. & Collett, T. S. 2005. Weak and strong priming cues in bumblebee contextual learning. *Journal of Experimental Biology* 208:65–74. DOI: 10.1242/jeb.01370.
- Forré, R. 1990. Methods and instruments for designing S-boxes. *Journal of Cryptology* 2:115–130. DOI: 10.1007/BF00190799.
- Garey, M. R. 1972. Optimal Binary Identification Procedures. *SIAM Journal on Applied Mathematics* 23:173–186. DOI: 10.1137/0123019.
- Hyafil, L. & Rivest, R. L. 1976. Constructing optimal binary decision trees is NP-complete. *Information Processing Letters* 5:15–17. DOI: 10.1016/0020-0190(76)90095-8.
- Janisch, J., Pevný, T. & Lisý, V. 2020. Classification with Costly Features as a Sequential Decision-Making Problem. *Machine Learning* 109:1587–1615. DOI: 10.1007/s10994-020-05874-8.
- Katona, G. O. H. 1966. On separating systems of a finite set. *Journal of Combinatorial Theory* 1:174–194. DOI: 10.1016/S0021-9800(66)80024-8.
- Li, J., Dhali, M. A. & Bouma, H. R. 2026. When Does Synergy Help Active Feature Acquisition? A PID-Based Study. arXiv:2609.32301.
- Ma, C., Tschiatschek, S., Palla, K., Hernandez-Lobato, J. M., Nowozin, S. & Zhang, C. 2019. EDDI: Efficient Dynamic Discovery of High-Value Information with Partial VAE. *Proceedings of Machine Learning Research* 97:4234–4243.
- MaBouDi, H., Richter, J., Guiraud, M.-G., Roper, M., Marshall, J. A. R. & Chittka, L. 2025. Active vision of bees in a simple pattern discrimination task. *eLife* 14:e106332. DOI: 10.7554/eLife.106332.
- Moshkov, M. & Zielosko, B. 2011. *Combinatorial Machine Learning: A Rough Set Approach*. Springer. DOI: 10.1007/978-3-642-20995-6.
- Nan, F. & Saligrama, V. 2017. Adaptive Classification for Prediction Under a Budget. *Advances in Neural Information Processing Systems* 30.
- Norcliffe, A. L. I., Lee, C., Imrie, F., van der Schaar, M. & Lio, P. 2025. Stochastic Encodings for Active Feature Acquisition. *Proceedings of Machine Learning Research* 267:46784–46814.
- Silva, R. & Clarke, A. R. 2020. The sequential cues hypothesis: a conceptual model to explain host location and ranking by polyphagous herbivores. *Insect Science* 27:1136–1147. DOI: 10.1111/1744-7917.12719.
- Spaethe, J. et al. 2026. Bees flexibly adjust decision strategies to information content in a foraging task. *Science Advances*. DOI: 10.1126/sciadv.adw9320.
- Sun, H. & Jafar, S. A. 2019. On the Capacity of Computation Broadcast. arXiv:1903.07597.
- Williams, P. L. & Beer, R. D. 2010. Nonnegative Decomposition of Multivariate Information. arXiv:1004.2515.
- Youssef, A. M. & Tavares, S. E. 2004. Decision trees of cryptographic Boolean functions. *Canadian Conference on Electrical and Computer Engineering* 1:401–404. DOI: 10.1109/CCECE.2004.1345040.
