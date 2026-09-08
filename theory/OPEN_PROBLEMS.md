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
static minimal frontier generation from cross-target pair incidence
Sperner/LYM bounds for the fixed frontier
productive-frontier form of gain / external bypass / internal redundancy
minimal-transversal characterization of internal and external bypass
set-valued local replacement certificate for zero external shortcut
sharp bypass-channel query minima: internal >=3, external >=4
deterministic exact guarantee budget profile from (C_A,C_F)
all optimal fixed bundles from the productive frontier
resource-labelled transition structure for richer named wiring
joint-safe global world-twin/query-refinement kernel
fixed-side certificate ladder and proof compression
minimal 4-world strict-gain normal form
complete 4-world / 4-query extension classification
unique deletion-minimal 5-world strict-gain normal form
first unit-cost scope with C_F/C_A > 3/2
unbounded unit-cost adaptive advantage
unbounded binary-observation unit-cost adaptive advantage
unbounded balanced-binary unit-cost adaptive advantage
sharp productive-tree internal-node bound M(n,h)
sharp unit-cost fixed-(world count, query count) ratio for unrestricted query arity
sharp unit-cost fixed-(world count, query count) ratio for binary query arity
sharp unit-cost fixed-(world count, query count, max query arity b) ratio
sharp unit-cost ratio with an upper bound on productive-frontier edge count
productive-frontier rank upper cap is extremally vacuous for every positive cap
global-label-once syntax: pointwise containment failure + unchanged feasible-class extremal maximum
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

For deterministic exact guarantee, the entire binary budget profile is already determined by the two minima:

\[
A(B)=\mathbf 1[B\ge C_A],\qquad
F(B)=\mathbf 1[B\ge C_F].
\]

The productive frontier also determines the complete set of minimum-cost fixed bundles, not only scalar `C_F`.

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
- Is there a canonical joint quotient preserving richer budget-indexed utilities (information, expected loss), not merely deterministic exact feasibility?

## 2. Generate and update the productive frontier efficiently

The minimal productive frontier can now be generated **statically** from identity-indexed cross-target pair incidence, so reachable-state enumeration is not required for fixed scalar resolution.

The remaining questions are computational/structural rather than representational:

- Can minimal frontier edges be generated output-sensitively, parameterized by the number of minimal edges rather than all cross-target pairs?
- Can incremental query addition/deletion update the frontier without rebuilding pair incidence from scratch?
- Can frontier generation exploit query automorphisms and world symmetries with independently checkable certificates?
- What parameterized complexity bounds are possible in query count, `C_F`, frontier rank, or transversal number?
- Can minimal transversals be generated output-sensitively without the small-state subset enumeration used by the current structural verifier?

## 3. Extremal adaptive advantage under additional structural constraints

Without extra restrictions, both additive gain and `C_F/C_A` are unbounded even for binary deterministic observations with unit costs.

The fixed-world / fixed-query unit-cost extremal problem is now closed for **every finite maximum query arity**.

### Bounded query arity `b>=2`

Let `F_b(n,h)` be the exact maximum number of internal-node occurrences in a productive tree with at most `n` leaves, depth at most `h`, and at most `b` children at each internal node. Then

\[
\boxed{
F_b(n,h)
=
1+
\max_{2\le r\le\min(b,n)}
\max_{\substack{n_1+\cdots+n_r\le n\\n_i\ge1}}
\sum_i F_b(n_i,h-1)
}
\]

with `F_b(1,h)=F_b(n,0)=0`.

For unit costs,

\[
\boxed{
R_b(n,m)
=
\max_{1\le h\le n-1}
\frac{\min\{m,F_b(n,h)\}}{h}
}
\]

is the exact maximum `C_F/C_A` among tasks with `n` represented worlds, `m` declared queries, and query arity at most `b`.

### Productive-frontier edge cap

If additionally

\[
|\mathcal H_{\min}|\le E,
\]

then the exact maximum becomes

\[
\boxed{
R_{b,E}(n,m)
=
\max_{1\le h\le n-1}
\frac{\min\{m,E,F_b(n,h)\}}{h}.
}
\]

### Productive-frontier rank cap

If `rank(H_min)` means maximum cardinality of a minimal frontier edge, then any positive upper cap is extremally vacuous:

\[
\boxed{
R_{b,\,\operatorname{rank}\le r}(n,m)=R_b(n,m)
\qquad(r\ge1).
}
\]

The sharp bounded-arity witness already has only singleton frontier edges. Thus `rank=1` can realize the full worst-case ratio; small edge size by itself does not make fixed resolution easy.

### Balanced binary outcomes

Global marginal balance also does **not** bound the ratio as problem size grows. There is an explicit family in which every binary query satisfies

\[
|\#0-\#1|\le1,
\]

while

\[
C_F\ge2^d,
\qquad
C_A\le d+1,
\]

so

\[
\boxed{C_F/C_A\ge2^d/(d+1)\to\infty.}
\]

What remains open is the **sharp fixed-`(n,m)` extremal formula inside the balanced-binary subclass**. Balancedness does not give a uniform constant bound, but it may change the finite-size optimum relative to unrestricted binary queries.

### Global-label-once policy syntax

The ordinary model already uses each query at most once on every **realized path**. A stronger syntax that allows each query label at only one node in the entire counterfactual tree is a different model.

Pointwise class containment fails under that syntax: a registered two-query task has ordinary `C_A=C_F=2` but no globally label-unique resolving tree. Nevertheless, if one restricts attention to tasks that are global-label-once resolvable, their sharp unit-cost extremal maximum remains `R_b(n,m)`, because the bounded-arity sharp construction already uses a distinct query at every internal node.

Remaining extremal questions therefore need constraints stronger or different than positive rank caps, marginal balance, or global-label uniqueness:

- What is the sharp fixed-`(n,m)` ratio in the balanced-binary subclass?
- What changes under a genuine operational inventory constraint shared across multiple simultaneously realized subjects or repeated experimental rounds?
- Under unequal positive costs, what is the sharp fixed-`(n,m,b)` ratio and what are the smallest scopes exceeding a given threshold?
- Can the bounded-arity recurrence be simplified to useful closed forms for fixed small `b=3,4`?
- What sharp bounds follow from a **lower** bound on frontier edge size, resource-frequency limits, or specified edge-intersection geometry?

## 4. Next finite irreducible normal forms

Closed nearby scopes:

1. `4 worlds / 2+2 targets / 3 queries`: one strict orbit `(3,5,9)`.
2. `4 worlds / 2+2 targets / 4 queries`: only one-query extensions of that core.
3. `5 worlds / 2+3 targets / 3 queries`: one new deletion-minimal orbit `(7,28,42)`.
4. Unit-cost ratio `>3/2`: impossible with at most five worlds; attained with six worlds/four queries for unrestricted arity and six worlds/five queries for binary-only observations.
5. Positive internal bypass requires at least three declared queries; positive external bypass requires at least four, and both bounds are attained.

Next questions:

- What irreducible forms first appear with five worlds and four queries?
- What is the next deletion-minimal core at six worlds after quotienting the explicit extremal families?
- What are the minimum **world counts** for deletion-minimal internal and external bypass cores?
- What is the smallest strict-gain core with positive internal bypass? With positive external bypass?
- Which larger cores share one adaptive continuation type but have distinct productive frontiers?
- Can normal forms be classified directly by `(continuation type, productive frontier)` rather than raw world/query tables?

## 5. Short certificates for bypass channels

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

The scalar and minimal-transversal structure is now closed:

\[
U-C_U=0
\iff
S\in\operatorname{Tr}(\mathcal H)
\iff
\forall q\in S\;\exists E:\ E\cap S=\{q\},
\]

and

\[
C_U-C_F>0
\iff
\exists T\in\operatorname{Tr}(\mathcal H):
T\not\subseteq S,\ c(T)<C_U.
\]

There is also a local sufficient no-external certificate: every outside resource may be replaced by a no-more-expensive inside **set** covering all frontier edges that used the outside resource.

Open questions:

- Can zero external shortcut be certified **necessarily and sufficiently** from a small edge subset without enumerating all minimal transversals?
- Can positive external discount be lower-bounded from local outside-resource coverage geometry?
- Which query-vocabulary operations monotonically increase/decrease internal and external discount?
- Can internal redundancy magnitude, not only its zero/nonzero status, be certified from private-edge defects?
- What parameterized complexity is possible for minimal-transversal bypass certificates in `C_U`, frontier rank, or edge count?

## 6. Resource-labelled structure beyond fixed bundle optimization

The productive frontier already recovers scalar `C_F` **and all minimum-cost fixed bundles**. Richer transition structure is still needed for other outputs.

Open questions:

- What is minimally necessary to replay a named adaptive policy after quotienting?
- Can explicit resource-transition isomorphism be certified without factorial permutation enumeration?
- Which scientific objectives depend on child wiring even though fixed resolution and its optimal bundles do not?
- What compact object preserves branch-specific provenance or measurement semantics in addition to decision cost?

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
