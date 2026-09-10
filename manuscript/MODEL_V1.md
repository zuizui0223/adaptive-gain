# Model v1

## 1. Ecological states and finite sensing tasks

We consider a finite set of recurrent ecological or community states indexed by `i=1,...,K`. A state summarizes the ecological context that is relevant to an organism's decision problem at a given time: for example the currently available resource assemblage, predator regime, pollinator context, host community, or other finite configuration that changes which distinctions must be resolved before a state-contingent action can be taken.

Within state `i`, the organism faces a finite sensing task. We describe that task by four biological ingredients.

1. **Represented alternatives (`worlds`)**. These are the finite ecological alternatives that remain behaviorally distinct before sensing. A world need not be a literal physical world; it is one state of the organism-relevant uncertainty set.
2. **Declared cues (`queries`)**. A query is one available source of deterministic information. Asking a query partitions the represented alternatives according to its possible outcomes.
3. **Outcome arity (`b`)**. Query arity is the maximum number of distinct outcomes available from one cue. It is a constraint on how many alternatives can be separated in one acquisition step, not on how many ecological items are contained in a cue category.
4. **Required distinctions**. Not every pair of represented alternatives must necessarily lead to different actions. The declared target relation specifies which alternatives must be distinguished for guaranteed state-contingent resolution.

This abstraction is intended to represent finite natural-history structure rather than a universal model of perception. The relevant alternatives and cue repertoire are declared by the biological application. The current theory assumes deterministic cue outcomes and guaranteed resolution; noisy likelihoods and probabilistic stopping rules are outside the present scope.

## 2. Adaptive and fixed information requirements

Let `C_A(i)` be the minimum worst-case number of unit-cost cue acquisitions required to resolve the declared target adaptively in community state `i`. An adaptive policy may choose the next query conditionally on previous outcomes and is represented by a decision tree.

Let `C_F(i)` be the minimum number of declared cue resources that must be acquired as a fixed set before outcomes are known in order to guarantee the same target resolution.

The structural adaptive gap is

\[
\boxed{g_i=C_F(i)-C_A(i).}
\]

The gap is a property of the declared finite sensing task. It is not itself a fitness value. It measures how much fixed information burden can be avoided when cue acquisition is allowed to branch conditionally on earlier outcomes.

The static combinatorial problem is classical in spirit: the fixed side overlaps separating systems / minimum test set / test cover, while the adaptive side overlaps optimal decision trees. We use these quantities as upstream ecological structural coordinates and make no novelty claim for the underlying identification machinery.

## 3. Productive information obligations

For the fixed problem, only distinctions that remain irreducible after redundant cue structure is removed contribute to the minimal fixed burden. We denote the resulting family of minimal productive obligations by `H_min` and its edge count by

\[
E_i=|H_{\min}(i)|.
\]

`Productive frontier` is repository terminology for this retained obligation family. Biologically, an edge represents one required distinction that cannot be discharged by redundancy elsewhere in the declared cue repertoire. We do not interpret the frontier as an independently measurable biological trait. Its role is structural: capping the number of irreducible obligations caps `C_F`, and hence caps the adaptive gap available to downstream selection or feedback.

A key asymmetry is that a cap on frontier edge count constrains the gap, whereas a cap on frontier rank alone does not. Sharp witnesses can already have rank one while retaining large fixed information burden. For the main paper, only the edge-count consequence is needed; the quotient and proof machinery remain supplementary.

## 4. Structural lift to selection

To connect finite sensing structure to evolutionary dynamics, we declare an ecological lift. In the continuous state-reward formulation,

\[
\boxed{s_i=\lambda g_i-\kappa,}
\]

where `lambda>0` converts one unit of structural gap into a state-dependent selection contribution and `kappa` is a state-independent maintenance cost of the adaptive architecture.

This mapping is an explicit model assumption. The theory does not claim that `C_F-C_A` is intrinsically fitness. The role of the structural results is conditional: once a lift is declared, finite sensing complexity places exact ceilings on the selection contrast that can be generated.

The centered temporal geometry is unaffected by a state-independent `kappa`. If

\[
\bar s=\sum_i\pi_i s_i,
\]

then

\[
s_i-\bar s
=\lambda\left(g_i-\bar g\right),
\qquad
\bar g=\sum_i\pi_i g_i.
\]

Thus maintenance cost shifts long-run mean selection but does not alter which community modes carry the state-dependent structural fluctuations.

## 5. Recurrent community dynamics

Let community states evolve as a finite ergodic Markov chain with transition matrix `P` and stationary distribution `pi`. The same state index `i` now carries two roles:

- the finite sensing task associated with state `i` generates structural reward `g_i` and selection `s_i`;
- the transition matrix `P` determines when that same state-indexed reward recurs.

This common indexing is the central structural coupling of the model. The amplitude of selection and its temporal recurrence are not assigned to separate arbitrary processes.

For centered reward vector

\[
c=s-\bar s\mathbf 1,
\]

define the lag covariance

\[
\gamma(k)
=
\sum_i\pi_i c_i[P^k c]_i.
\]

For cumulative centered selection over horizon `H`,

\[
S_H=\sum_{t=1}^{H}(s_{X_t}-\bar s),
\]

we have

\[
\operatorname{Var}(S_H)
=
H\gamma(0)
+2\sum_{k=1}^{H-1}(H-k)\gamma(k).
\]

When the chain is reversible, the asymptotic variance rate can be decomposed over nontrivial community relaxation modes,

\[
\boxed{
\sigma_{\rm eff}^2
=
\sum_r w_r\frac{1+r_r}{1-r_r},
}
\]

where `r_r` is a nontrivial eigenvalue and `w_r` is the squared projection of centered structural selection onto that mode. Slow community modes contribute strongly only when the structural reward aligns with them.

## 6. Local endogenous eco-evolutionary feedback

The exogenous community process above describes recurrence of state-dependent rewards. To represent endogenous feedback, we use a generalized local two-coordinate response around an interior equilibrium. Let `x_t` denote a local evolutionary coordinate and `q_t` a local ecological/community coordinate. The linearized response is summarized by three quantities:

- `alpha`: intrinsic persistence of the evolutionary coordinate;
- `phi`: persistence of the ecological/community coordinate;
- `G`: net eco-evolutionary feedback gain.

The local invariants are

\[
\boxed{T=\alpha+\phi,}
\]

and

\[
\boxed{D=\alpha\phi+(1-\phi)G.}
\]

A convenient mechanistic factorization is

\[
G=-\beta\,\Delta s\,e,
\]

where `beta` is local evolutionary responsiveness to selection, `Delta s` is the selection contrast between ecological states, and `e` is the slope by which the evolutionary coordinate changes the ecological target. For restoring negative ecological feedback, `e<0` and hence `G>0` when `beta Delta s>0`.

Under the structural lift `Delta s=lambda Delta g`,

\[
\boxed{G=a\Delta g,}
\]

with

\[
a=(-\beta e)\lambda>0.
\]

This provides the bridge used in the reachability theorem: a dynamical regime requiring minimum `G` also requires minimum structural gap `Delta g`, which in turn requires a minimum or Pareto-minimal finite sensing structure.

## 7. Local phase boundaries

For `0<=alpha<=1` and `0<=phi<1`, local stability is equivalent to

\[
\boxed{
\alpha-1<G<\frac{1-\alpha\phi}{1-\phi}.
}
\]

The boundary between real and complex eigenvalues is

\[
\boxed{
G_{\rm osc}
=
\frac{(\alpha-\phi)^2}{4(1-\phi)}.
}
\]

Hence a stable oscillatory response requires

\[
G_{\rm osc}<G<G_+,
\qquad
G_+=\frac{1-\alpha\phi}{1-\phi}.
\]

Because structural gaps are integer under the unit-cost finite sensing model, the first reachable oscillatory gap is the smallest integer `q` satisfying

\[
a q>G_{\rm osc}
\]

while remaining below the upper stability boundary. This integer requirement is what the finite-information extremal theory translates into a minimum or Pareto-minimal information structure.

## 8. Information-complexity bounds

For unit-cost sensing with at most `b` outcomes per query, let

\[
F_b(n,h)
\]

be the maximum number of internal-node occurrences in a productive rooted decision tree with at most `n` represented worlds, depth at most `h`, and out-degree at most `b`. We use this rooted-tree extremal quantity only as supporting combinatorial machinery.

A task with adaptive optimum `C_A=h` obeys

\[
\boxed{
C_F\le \min\{m,E,F_b(n,h)\}.
}
\]

Thus a required structural gap `q=C_F-C_A` is possible only if

\[
\min\{m,E,F_b(n,h)\}\ge h+q.
\]

For binary sensing this yields one exact first corner. For `b>2`, the minimum world count and minimum query/frontier count need not be attained by the same task, so the exact requirement is generally a Pareto frontier over `(n,m,E)`.

The sharp constructions and recurrences supporting these bounds are placed in the Supplement. The ecological model uses only their consequences: finite sensing structure bounds state-dependent selection and determines whether specified local feedback phases are structurally reachable.

## 9. Two forms of long-term stasis

We use two minimal dynamical models to distinguish stasis mechanisms.

For exogenous periodic weak selection,

\[
z_{t+1}=z_t+E\beta_t,
\]

zero summed selection over a period produces an identity period map and therefore neutral cancellation stasis.

For endogenous feedback, an equilibrium with spectral radius

\[
\rho(J)<1
\]

is attractive and produces restoring stasis. These constructions deliberately isolate mechanism rather than attempt one universal model of stasis.

## 10. Time-interpretation limit

The local trajectory identifies the characteristic invariants `T` and `D`, but in the generalized response they do not uniquely identify `alpha`, `phi`, and `G`. For any candidate `phi<1`,

\[
\alpha(\phi)=T-\phi,
\]

and

\[
G(\phi)
=
\frac{D-T\phi+\phi^2}{1-\phi}
\]

produce the same characteristic polynomial whenever the parameters remain admissible.

We retain this result only as a limitation on interpreting evolutionary time. The paper does not develop an observation-design or finite-sample inference program.

## 11. Scope

The current model assumes finite deterministic sensing, unit acquisition costs for the sharp information-complexity theorems, a declared linear structural lift, finite community-state dynamics, reversibility for the sharp spectral ceiling, and local deterministic endogenous feedback. The results do not cover noisy cue likelihoods, continuous compatible sets, mutation, migration, drift, multivariate quantitative genetics, demographic stochasticity, or global nonlinear bifurcation structure.
