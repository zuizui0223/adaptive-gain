# Open problems

The finite deterministic guaranteed-resolution layer now has several closed components:

```text
exact adaptive optimum C_A
exact fixed optimum C_F
fixed-cost certificate ladder
exact bypass decomposition
full identity-indexed target-pair incidence sufficiency for C_A and C_F
state-local target-relevant query-class compression preserving C_A
two-sided fixed-cover kernelization
exact proof DAG / isomorphism / transport / symmetry pruning
unique minimal 4-world / 3-query strict-gain normal form
complete 4-world / 4-query extension classification
unique deletion-minimal 5-world / 2+3-target / 3-query strict-gain normal form
```

The key representation boundary is now explicit:

\[
\boxed{
\text{full target-pair incidence is sufficient for deterministic }(C_A,C_F),
}
\]

while an inclusion-minimal fixed-cover kernel is not sufficient to preserve adaptive routing geometry.

The first adaptive-specific safe compression is also closed: at each Bellman state, queries with the same exact family of target-mixed children are continuation-equivalent, so one cheapest representative is sufficient.

The next questions therefore concern **stronger adaptive-safe quotients**, cheaper symmetry certification, larger finite normal forms, and extensions beyond deterministic exact resolution.

## 1. Characterize the coarsest adaptive-safe quotient of full pair incidence

At a current world set `A`, define

\[
\mathcal M_A(q)
\]

as the family of target-mixed outcome cells induced by query `q`.  `adaptive_safe_compression.py` now proves and implements

\[
\boxed{
\mathcal M_A(q)=\mathcal M_A(r)
\Longrightarrow
\text{one cheapest representative is sufficient at }A.
}
\]

All target-pure cells have continuation cost zero, and every unresolved common mixed child is an outcome cell of both queries, so the rest of the equivalence class becomes constant there.

This exact equality quotient is useful but may not be maximal.

Open questions:

- Can different mixed-child families still be Bellman-equivalent because their child states have equal continuation values under every remaining query budget?
- Is there a recursively defined bisimulation on `(world subset, remaining query vocabulary)` that gives the coarsest exact quotient for `C_A`?
- Can that quotient be computed without already solving the complete Bellman recursion?
- Can one prove safe **dominance** from refinement or inclusion relations between mixed-child families, rather than exact equality only?
- Which within-target world distinctions can be merged before any query is chosen?
- Is there a static quotient of full identity-indexed pair incidence that is strictly smaller yet still determines `C_A` for every positive cost vector?

The fail-closed rule remains: inability to certify a quotient means `compression_incomplete`, never assumed equivalence.

## 2. Develop joint fixed/adaptive kernel bounds

The four-world and five-world deletion-minimal strict-gain cores both reduce to the same minimal fixed separator antichain

\[
(1,2,4),
\]

while their adaptive normal forms differ.

So the repository now has two distinct kernel ideas:

```text
fixed kernel:
  preserve weighted target-pair cover

adaptive kernel:
  preserve target-mixed continuation structure and Bellman value
```

Open questions:

- What size bounds exist for the adaptive state-local quotient?
- Can pair-side Sperner bounds be combined with target-mixed child counts?
- Is there a bound parameterized by `C_A`, strict gain `C_F-C_A`, or adaptive-tree depth rather than raw query count?
- Can fixed and adaptive kernels share one compact residual representation without losing either proof obligation or routing geometry?

## 3. Certify automorphism generators without enumerating the full stable-color permutation family

The proof-compression side is exact for small states:

```text
color refinement
-> individualization-refinement
-> exact automorphism audit
-> stabilizer-orbit pruning
-> explicit transported proof DAG
-> parent-automorphism branch-orbit pruning
```

But `automorphism.py` still certifies the complete group by enumerating every stable-color-preserving query permutation up to a hard cap.

Open questions:

- Can a small generator set and its completeness be certified without enumerating the whole candidate family?
- Can a stabilizer chain be built incrementally during individualization and reused by proof search?
- Can canonicalization traces provide a compact independently checkable symmetry certificate?
- Can global proof size be bounded directly in certified orbit counts?

## 4. Classify the next finite normal forms

Three nearby scopes are closed:

1. `4 worlds / 2+2 targets / 3 queries`: one strict symmetry orbit `(3,5,9)`.
2. `4 worlds / 2+2 targets / 4 queries`: no new irreducible mechanism; only one-query extensions of the minimal core.
3. `5 worlds / 2+3 targets / 3 queries`: five strict signature classes and one new world/query deletion-minimal orbit `(7,28,42)`.

Next questions:

- What new irreducible forms appear first with five worlds and four queries?
- What is the next deletion-minimal core at six worlds?
- At what smallest scope can `C_F/C_A` exceed `3/2`?
- What is the smallest deletion-minimal core with nonzero internal or external bypass?
- Do larger deletion-minimal cores reuse the same fixed antichain while introducing new adaptive routing geometries?
- How many normal forms remain after exact world/query/outcome symmetry quotienting?

## 5. Characterize external fixed bypass locally

The exact decomposition is

\[
U-C_A=(C_F-C_A)+(C_U-C_F)+(U-C_U).
\]

`C_U-C_F` is the external shortcut discount.

Open questions:

- Can an outside query be certified irrelevant from a restricted incidence signature?
- Is there a cut-style certificate that every external shortcut must cross?
- Can external shortcut discount be bounded without solving the full fixed cover?
- Which query-vocabulary operations monotonically create or destroy external bypass?

## 6. Information-valued adaptive gain

For MROD-like tasks the utility need not be binary exact target resolution:

\[
G(B)
=\max_{\pi:c(\pi)\le B}I(T;H_\pi)
-\max_{F:c(F)\le B}I(T;Q_F).
\]

Open questions:

- What are the information analogues of internal redundancy and external shortcut discount?
- What replaces exact mixed-child equivalence when observations carry partial information?
- Under what assumptions is the objective submodular or adaptively submodular?
- Can positive adaptive-information windows have multiple disconnected budget intervals?
- Is there an information-valued version of branch-orbit compression for equivalent continuation experiments?

## 7. Continuous compatible sets

PAYOFF's scientific uncertainty is continuous.  A desired extension has

\[
\Theta_{t+1}=\Theta_t\cap C(q_t,y_t)
\]

with target map `T(theta)` without unjustified finite discretization.

Open questions include convex/semi-algebraic separation certificates, interval branch-and-bound, and finite witness reductions whose completeness is proved rather than assumed.

## 8. Calibration actions versus target actions

MROD, PAYOFF, and BALANCE all expose the resource tradeoff

```text
measure the scientific target
vs
improve the measurement model itself.
```

A calibration action can change the future query system, so the state must carry both scientific uncertainty and calibration uncertainty.  The current static deterministic query-cover model is insufficient for that extension.

## 9. Stochastic branch-invariance and scenario robustness

BALANCE's current no-routing theorem is deterministic/minimax.  Under stochastic errors, equal deterministic support need not imply equal continuation distributions.

A probabilistic analogue likely requires equality of continuation-value kernels rather than raw state summaries.  Randomized policies under multiple calibration scenarios are a separate objective and should not be imported into deterministic guaranteed resolution by default.

## 10. Empirical identification of routing value

A natural-data routing claim needs more than a low-information first observation.  The finite theory now establishes that:

- zero direct root information is neither necessary nor sufficient;
- deletion-minimal strict gain can have a positive-information root;
- fixed bypass may be internal or external;
- lower-bound relaxations may miss integer fixed-cost gaps;
- full target-pair incidence preserves deterministic `C_A`, but aggressive fixed-side kernelization may destroy adaptive geometry;
- state-local mixed-continuation equivalence gives one exact adaptive-safe compression;
- symmetric proof branches may be mathematically redundant even when measurements remain distinct named actions.

An empirical claim therefore needs evidence that the first result changes the useful continuation, the branch-specific plan has a real resource advantage, plausible fixed bypasses are bounded, and the measurement/calibration relationships transport to deployment.

The source repositories currently provide synthetic/conditional witnesses, not that natural-data demonstration.
