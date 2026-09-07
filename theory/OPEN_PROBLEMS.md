# Open problems

The finite deterministic guaranteed-resolution layer now has the following closed components:

```text
exact adaptive optimum C_A
exact fixed optimum C_F
exact gain/bypass decomposition
cost-only continuation quotient preserving C_A
productive-frontier hypergraph preserving C_F
cost-only continuation + productive frontier preserving (C_A,C_F)
productive-frontier / minimal pair-separator equivalence
Sperner/LYM bounds for the fixed frontier
productive-frontier form of gain / external bypass / internal redundancy
resource-labelled transition structure for richer named wiring
joint-safe global world-twin/query-refinement kernel
fixed-side certificate ladder and proof compression
minimal 4-world strict-gain normal form
complete 4-world / 4-query extension classification
unique deletion-minimal 5-world strict-gain normal form
first unit-cost scope with C_F/C_A > 3/2
unbounded unit-cost adaptive advantage
unbounded binary-observation unit-cost adaptive advantage
sharp productive-tree internal-node bound M(n,h)
sharp unit-cost fixed-(world count, query count) ratio for unrestricted query arity
```

The central scalar-cost boundary is now especially compact:

\[
\boxed{
\text{adaptive continuation structure}\Longrightarrow C_A,
}
\]

and

\[
\boxed{
\mathcal H_{\min}=\min_{\subseteq}\{P_s:s\text{ reachable mixed}\}
+\text{query costs}
\Longrightarrow C_F.
}
\]

Thus

\[
\boxed{
\text{adaptive continuation}+\mathcal H_{\min}
\Longrightarrow(C_A,C_F).
}
\]

The productive frontier is the minimum-edge antichain after inclusion reduction; consumed-query history and fixed-side child wiring are not needed for scalar `C_F`.

## 1. Find the coarsest joint scalar-cost quotient

The product

```text
cost-only continuation quotient
+
productive frontier
```

is sufficient for `(C_A,C_F)` but is not claimed to be the coarsest joint representation.

Open questions:

- Can adaptive continuation classes and frontier edges share one canonical quotient instead of being stored separately?
- Which continuation distinctions are already implied by the productive frontier?
- Which frontier distinctions are irrelevant once continuation type is known?
- Can the gap `C_F-C_A` be computed from an object strictly smaller than those needed to recover the two optima separately?
- Is there a canonical joint bisimulation/hypergraph quotient preserving the entire budget profile rather than only the two minima?

## 2. Generate the productive frontier without full reachable-state enumeration

The fixed statistic is now conceptually minimal under inclusion, but the current builder still discovers reachable mixed states before taking productive sets.

Open questions:

- Can the minimal productive frontier be generated directly from target-pair incidence or another static representation?
- Can frontier edges be output-sensitive, with complexity parameterized by the number of minimal edges rather than the number of reachable states?
- Can incremental query addition/deletion update the frontier without rebuilding the full state space?
- Can frontier generation exploit query automorphisms and world symmetries with independently checkable certificates?
- What parameterized complexity bounds are possible in query count, `C_F`, frontier rank, or transversal number?

## 3. Extremal adaptive advantage under additional structural constraints

Without extra restrictions, both additive gain and `C_F/C_A` are unbounded even for binary deterministic observations with unit costs:

\[
C_A=d+1,\qquad C_F=2^d.
\]

For **unit costs with unrestricted deterministic query arity**, the fixed-`(n,m)` problem is now closed exactly:

\[
\boxed{
\max\frac{C_F}{C_A}
=
\max\!\left(
1,
\frac{\min\{m,1+\lfloor n/2\rfloor\}}{2}
\right).
}
\]

The exact productive-tree internal-node bound used in that proof is

\[
\boxed{
M(n,h)
=
n+1-
\max\!\left(
2,
\left\lceil\frac{n}{2^{h-1}}\right\rceil
\right).
}
\]

So the remaining extremal questions require additional restrictions beyond just `n,m` in the unrestricted-arity unit-cost model.

Open questions:

- What is the sharp fixed-`(n,m)` ratio when **all queries are binary**?
- What is the sharp ratio at fixed observation-tree depth together with bounded query arity?
- What bounds follow from limiting productive-frontier rank, edge count, or transversal number?
- What is the sharp ratio bound when every query has balanced binary outcomes?
- What changes if each query may be used at most once globally, versus once per branch as in the current resource model?
- Under unequal positive costs, what is the sharp fixed-`(n,m)` ratio and what are the smallest scopes exceeding a given threshold?

## 4. Next finite irreducible normal forms

Closed nearby scopes:

1. `4 worlds / 2+2 targets / 3 queries`: one strict orbit `(3,5,9)`.
2. `4 worlds / 2+2 targets / 4 queries`: only one-query extensions of that core.
3. `5 worlds / 2+3 targets / 3 queries`: one new deletion-minimal orbit `(7,28,42)`.
4. Unit-cost ratio `>3/2`: impossible with at most five worlds; attained with six worlds/four queries.

Next questions:

- What irreducible forms first appear with five worlds and four queries?
- What is the next deletion-minimal core at six worlds after quotienting the explicit extremal family?
- What is the smallest deletion-minimal core with nonzero internal or external bypass?
- Which larger cores share one adaptive continuation type but have distinct productive frontiers?
- Can normal forms be classified directly by `(continuation type, productive frontier)` rather than raw world/query tables?

## 5. Localize external and internal bypass on the productive frontier

For selected adaptive query union `S`,

\[
c(S)-C_A
=
[\tau_c(\mathcal H)-C_A]
+
[\tau_c(\mathcal H;S)-\tau_c(\mathcal H)]
+
[c(S)-\tau_c(\mathcal H;S)].
\]

The scalar decomposition is closed, but structural certificates for its two discount terms can be sharper.

Open questions:

- Can external shortcut discount be bounded from frontier edges intersecting `Q\\S` without solving the full hitting set?
- Is there a local cut certificate proving that no outside resource can improve `C_U`?
- Can internal redundancy be characterized by minimal transversals entirely inside `S`?
- Which vocabulary operations monotonically increase/decrease the two discount channels?
- Can one certify the decomposition terms from a small subset of frontier edges?

## 6. Resource-labelled structure beyond scalar costs

The productive frontier is enough for scalar `C_F`, but richer outputs still need more structure.

Open questions:

- What is minimally necessary to recover **all** optimal fixed bundles, not just their minimum cost?
- What is minimally necessary to replay a named adaptive policy after quotienting?
- Can explicit resource-transition isomorphism be certified without factorial permutation enumeration?
- Which scientific objectives depend on child wiring even though scalar fixed resolution does not?

## 7. Information-valued adaptive gain

For MROD-like tasks,

\[
G(B)=\max_{\pi:c(\pi)\le B}I(T;H_\pi)
-\max_{F:c(F)\le B}I(T;Q_F).
\]

Open questions:

- What replaces deterministic productive-frontier edges when observations have likelihoods?
- Is there a probabilistic fixed-failure or fixed-sufficiency certificate analogous to hitting every productive set?
- What are the information analogues of internal redundancy and external shortcut discount?
- Under what assumptions is the objective submodular or adaptively submodular?
- Can information-valued adaptive gain also be unbounded under bounded binary observations and normalized cost?

## 8. Continuous compatible sets

PAYOFF's scientific uncertainty is continuous. A desired extension has

\[
\Theta_{t+1}=\Theta_t\cap C(q_t,y_t)
\]

without unjustified finite discretization. Open directions include interval/semi-algebraic separation certificates, continuum hitting-set analogues, and complete finite witness reductions.

## 9. Calibration actions versus target actions

A calibration action changes later observation laws, so a static productive frontier is no longer enough. The state must carry both scientific uncertainty and measurement-model uncertainty, and resources may change their own future transition law.

## 10. Empirical identification of routing value

The source repositories currently provide synthetic/conditional structural witnesses. A natural-data routing claim still needs evidence that branch outcomes change useful continuation, that the physical measurement vocabulary really has the declared productive frontier, that plausible fixed bypasses are bounded, and that measurement/calibration relationships transport to deployment.
