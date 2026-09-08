# Predictive cue usefulness beyond temporal autocorrelation

## Status

This note generalizes the temporal routing result away from the single symmetric parameter `rho`.

The mathematical core is a standard value-of-information/Jensen-gap calculation. The contribution claimed here is therefore **not** a new convexity theorem. The modeling contribution is the ecological identification:

> the relevant temporal quantity for contingent sensing is the predictability of **which future specialist cue will be useful**, not temporal autocorrelation itself.

The exact two-context result remains tied to the repository's original `q_route/q_left/q_right` normal form. A finite-state extension is then stated under an explicit branch-diagnostic specialist abstraction.

---

## 1. Arbitrary binary transition kernel

Let

\[
T\in\{0,1\}
\]

be a fair fitness-relevant target, independent of the current context

\[
C_0\in\{0,1\}.
\]

Write

\[
P(C_0=i)=\pi_i,
\qquad \pi_0+\pi_1=1,
\]

and allow an arbitrary binary transition kernel

\[
K_{ij}=P(C_1=j\mid C_0=i).
\]

The target remains fixed over the short sensing episode.

The original specialist semantics are unchanged:

\[
q_L(T,C_1)=
\begin{cases}
T,&C_1=1,\\
0,&C_1=0,
\end{cases}
\]

and

\[
q_R(T,C_1)=
\begin{cases}
T,&C_1=0,\\
1,&C_1=1.
\end{cases}
\]

The route observation reveals `C0` before the second query is chosen.

---

## 2. Fixed policy ceiling under an arbitrary kernel

Define the future context marginal

\[
\mu_j=P(C_1=j)=\sum_i\pi_iK_{ij}.
\]

A fixed two-query policy cannot change specialist identity after seeing `C0`.

For the best fixed pair, exact Bayes decoding gives

\[
\boxed{
A_F^{(2)}
=
\frac12+rac12\max_j\mu_j.
}
\]

For two branches this includes both route-plus-one-specialist bundles and the two-specialist bundle. The latter has an ambiguous observation whose Bayes-optimal resolution simply chooses the more common future context branch, yielding the same optimum.

---

## 3. Contingent policy under an arbitrary kernel

Conditional on `C0=i`, choosing the specialist matched to future branch `j` gives target accuracy

\[
\frac12+\frac12K_{ij}.
\]

Therefore the optimal contingent policy chooses a row-wise maximizer

\[
a^*(i)\in\arg\max_jK_{ij},
\]

and reaches

\[
\boxed{
A_A^{(2)}
=
\frac12+rac12\sum_i\pi_i\max_jK_{ij}.
}
\]

Hence

\[
\boxed{
G_K
=
A_A^{(2)}-A_F^{(2)}
=
\frac12
\left[
\sum_i\pi_i\max_jK_{ij}
-
\max_j\sum_i\pi_iK_{ij}
\right].
}
\]

This is the exact arbitrary-binary-kernel replacement for the symmetric `rho` formula.

---

## 4. Jensen-gap interpretation

Define

\[
U(i,j)=K_{ij},
\]

the probability that specialist `j` will be the useful specialist at the future sensing step when the current context is `i`.

Then

\[
2G_K
=
E_{C_0}\left[\max_j U(C_0,j)\right]
-
\max_jE_{C_0}[U(C_0,j)].
\]

Thus routing gain is one half of the value of conditioning the specialist decision on current context.

The ecological interpretation is

\[
\boxed{
\text{routing value}
=
\text{predictive value of current state for future cue usefulness}.
}
\]

Autocorrelation is only one way to create this value.

---

## 5. Exact strict-gain condition

Because `max` is convex,

\[
G_K\ge0.
\]

Equality has a sharp decision-theoretic characterization.

Let

\[
M_i=\arg\max_jK_{ij}
\]

for every current context with positive prior mass.

Then

\[
\boxed{
G_K=0
\iff
\bigcap_{i:\pi_i>0}M_i\ne\varnothing.
}
\]

Equivalently,

\[
\boxed{
G_K>0
\iff
\text{no single specialist is optimal in every current context.}
}
\]

This is stronger than saying that `C0` predicts `C1`.

Current context can contain predictive information about future context while having **zero routing value** if that information never changes which specialist should be used.

Example:

\[
K=
\begin{pmatrix}
0.9&0.1\\
0.6&0.4
\end{pmatrix}.
\]

The two rows differ, so current context predicts the future distribution, but specialist 0 remains optimal in both rows. Therefore contingent routing gives no gain.

The relevant quantity is consequently **action-relevant predictability**, not predictive information in the abstract.

---

## 6. Binary closed form

For two future specialists define the signed branch advantage

\[
d_i=K_{i0}-K_{i1}.
\]

Then

\[
\boxed{
G_K
=
\frac14
\left[
\sum_i\pi_i|d_i|
-
\left|\sum_i\pi_id_i\right|
\right].
}
\]

The first term measures how strongly each current context locally favours a specialist. The second subtracts the specialist advantage that a fixed policy can exploit from the marginal future branch bias.

For two positive-prior current contexts, strict gain requires the local advantages to disagree in sign, apart from ties:

\[
d_0d_1<0.
\]

When they do,

\[
G_K
=
\frac12\min\{\pi_0|d_0|,\pi_1|d_1|\}.
\]

So the gain is controlled by the weaker weighted side of the routing conflict.

---

## 7. Recovery of the symmetric temporal theorem

Take

\[
\pi_0=\pi_1=\frac12
\]

and

\[
K=
\begin{pmatrix}
\rho&1-\rho\\
1-\rho&\rho
\end{pmatrix}.
\]

Then

\[
d_0=2\rho-1,
\qquad
d_1=-(2\rho-1),
\]

so

\[
\boxed{
G_K
=
\frac{|2\rho-1|}{4}.
}
\]

Therefore `TEMPORAL_ROUTING_THRESHOLD.md` is the balanced symmetric special case of the general predictive-cue-usefulness theorem.

This clarifies what the earlier result was measuring: not persistence or alternation per se, but disagreement across current contexts about which future specialist will be useful.

---

## 8. Finite-state branch-diagnostic extension

Now let current context take values

\[
i\in\{1,\ldots,n\}
\]

and future specialist identity take values

\[
j\in\{1,\ldots,m\}.
\]

Let `K_ij` be the probability that specialist `j` is the diagnostic specialist at the future step.

Assume explicitly that

- a matched specialist reveals the fair binary target perfectly;
- a mismatched specialist is target-uninformative;
- the route observation identifies the current context before specialist choice.

Under this branch-diagnostic abstraction the same formulas hold:

\[
\boxed{
A_F
=
\frac12+rac12\max_j\sum_i\pi_iK_{ij},
}
\]

\[
\boxed{
A_A
=
\frac12+rac12\sum_i\pi_i\max_jK_{ij},
}
\]

and

\[
\boxed{
G
=
\frac12
\left[
\sum_i\pi_i\max_jK_{ij}
-
\max_j\sum_i\pi_iK_{ij}
\right].
}
\]

The strict-gain condition remains the absence of a common row-wise optimal specialist across all positive-prior current contexts.

This finite-state statement is a modeling extension of the original four-world core, not a claim that every multi-cue sensory system has this likelihood structure.

---

## 9. Selection threshold with routing cost

If one unit of classification accuracy is worth `v>0` fitness units and contingent control costs `k>=0`, then

\[
\Delta W=vG_K-k.
\]

Routing is favoured exactly when

\[
\boxed{
\sum_i\pi_i\max_jK_{ij}
-
\max_j\sum_i\pi_iK_{ij}
>
\frac{2k}{v}.
}
\]

This threshold has a direct natural-history reading: context dependence must change future cue choice often and strongly enough to repay the cost of maintaining contingent control.

---

## 10. Empirical interpretation

The theorem suggests estimating two objects rather than only an environmental autocorrelation coefficient.

### Current-state-conditioned future cue usefulness

Estimate

\[
K_{ij}=P(\text{specialist }j\text{ is useful later}\mid C_0=i).
\]

Examples include

- habitat or microclimate state -> which sensory modality becomes reliable later;
- approach geometry -> which close-range cue becomes diagnostic after contact;
- host or flower state -> which handling cue resolves profitability;
- predator encounter state -> which escape cue becomes informative at the next stage.

### Fixed baseline

Also estimate the marginal

\[
\mu_j=\sum_i\pi_iK_{ij}.
\]

A large `K` dependence is not sufficient by itself. The dependence must alter the identity of the best future cue relative to the fixed marginal choice.

This gives a concrete empirical target:

\[
\boxed{
\text{Does present ecological state predict a change in the identity of the best future cue?}
}
\]

That question is sharper than asking only whether the environment is temporally autocorrelated.

---

## 11. Boundary of the claim

This theorem does **not** yet cover

- noisy observation of a general multi-state current context;
- correlated or asymmetric specialist errors;
- target dynamics during the episode;
- costs that depend on cue identity or context;
- learning of an unknown transition kernel;
- endogenous environmental modification;
- explicit population-genetic dynamics.

The existing symmetric noisy theorem remains the exact noisy special case. The next evolutionary layer should place heritable investments on routing and specialist precision and ask when the positive within-episode complementarity creates multiple optima, thresholds, or bifurcations.
