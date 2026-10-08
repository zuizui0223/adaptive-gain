# Canonical fitness theorem spine v1

Status: canonical reader path for PR #67. This file selects the smallest theorem
set needed for the biological paper. Results not listed as MAIN should not be
promoted merely because they are mathematically interesting.

## Biological question

When can a finite contingent information architecture generate enough
ecological value to be supported by selection?

The paper answers this at two levels:

1. frequency-free robust value across all represented states;
2. frequency-dependent expected value when some branches are encountered more
   often than others.

The distinction is essential.

## MAIN 1 — exact finite structural frontier

Fix finite deterministic unit-cost tasks with (n) represented worlds, (m)
declared query resources, and maximum query arity (b).

For each feasible adaptive depth (h), define

\[
I_h=\min{m,F_b(n,h)}.
\]

The protected-spine private-pair construction attains

\[
\boxed{(C_A,C_F)=(h,I_h)}
\]

for every feasible depth.

Therefore (hmapsto(h,I_h)) is an exact attainable adaptive/fixed frontier,
not only an upper-bound curve.

Biological interpretation: the finite environment does not provide one scalar
amount of routeability. It provides a menu of attainable architectures trading
adaptive completion depth against fixed simultaneous provisioning burden.

Prior-art boundary: adaptive-tree flattening itself is established. The claim
retained here is the fixed-((n,m,b)) exact frontier with constructive
attainment at every feasible depth.

## MAIN 2 — natural history sharply re-ranks the frontier

Let (U(c)) be any finite nonincreasing biological value of guaranteed
completion at cost (c).

Then

\[
\boxed{
R_{\rm robust,max}
=
\max_h[U(h)-U(I_h)].
}
\]

The same frontier witnesses attain the bound.

Thus natural history does not multiply one structural adaptive-gain score. It
chooses among points on the structural frontier.

If (U(c)=-lambda c), then
(U(C_A)-U(C_F)=lambda(C_F-C_A)). Only in this
constant-marginal-value case is the structural gap alone sufficient.

If (U(c)=vS(c)), with (S(c)) the probability that the ecological opportunity
remains open, then

\[
\boxed{
R_{\rm robust,max}
=
v\max_h[S(h)-S(I_h)].
}
\]

Canonical finite example: for binary (n=10,m=9), the frontier contains
((2,3),(3,7),(4,9)). The structural ratio is maximized at (h=3).
Under exponential opportunity value (U(c)=e^{-mu c}), the robust-value
optimum switches (h^*:4\to3\to2) as urgency increases.

Hence

\[
\boxed{
\text{ratio-optimal architecture}

eq
\text{biologically optimal architecture}.
}
\]

## MAIN 3 — exact inverse evolutionary threshold and global arity no-go

Let contingent control pay additive constitutive cost (Kge0).

At adaptive depth (h), define

\[
J_K(h)
=
\min{jge h:U(h)-U(j)>K}.
\]

Positive robust value at that depth is possible exactly when

\[
\boxed{I_hge J_K(h).}
\]

Thus biology can be inverted back into a minimum finite information
architecture.

Allow world count and query count to grow without bound while keeping cue arity
at most (b). Define

\[
J_b(h)=\frac{b^h-1}{b-1}.
\]

For bounded-below (U),

\[
\boxed{
K_{\rm crit,robust}^{(b)}
=
\max_{h\ge2}[U(h)-U(J_b(h))].
}
\]

If (K>K_{\rm crit,robust}^{(b)}), then no finite task with query arity at most
(b) can guarantee positive net adaptive value in every represented state.
Adding more worlds or more query resources cannot rescue it.

Define

\[
\boxed{
b_{min}^{\rm robust}
=
\min{b\ge2:K<K_{\rm crit,robust}^{(b)}}.
}
\]

For (U(c)=e^{-0.3c}) and (K=0.30),

\[
K_{\rm crit,robust}^{(2)}\approx0.290085,
\qquad
K_{\rm crit,robust}^{(3)}\approx0.386328,
\]

so

\[
\boxed{b_{min}^{\rm robust}=3.}
\]

This is a model-specific information-branching no-go, not a generic statement
that biologically higher-fidelity senses are fitter.

## SUPPORT 1 — encounter frequencies create a distinct expected-value frontier

The robust result requires positive value across all represented states.
Expected selection is different.

For fixed finite (n,m), define

\[
M=\min{m,n-1}.
\]

Across all legal tasks, guaranteed-resolving adaptive policies, and strictly
positive world-frequency distributions,

\[
\boxed{
sup R_{\rm expected}(n,m)
=
U(1)-U(M).
}
\]

The supremum is approached by a binary private-pair tree with one
high-probability one-query branch and rare branches carrying the fixed burden.

Therefore the finite-scope expected ceiling is independent of cue arity
(bge2).

**Scope restriction:** this supremum also permits the *target-class
prevalence* to vary freely. At fixed 50/50 binary-target prevalence, the
minimal four-world, two-query corner instead has a binary supremum
\(\tfrac12[U(1)-U(2)]\) and a ternary supremum \(U(1)-U(2)\).
This conditional arity effect is audited in
`TARGET_PREVALENCE_EXPECTED_CAPACITY.md` and its independent exhaustive test.
It remains supporting interpretation, not another MAIN theorem.

Cue arity constrains robust evolvability, but encounter-frequency concentration
can substitute for cue branching capacity in the expected-value problem.

Globally, for bounded-below (U),

\[
\boxed{sup R_{\rm robust}=U(2)-U_\infty,}
\]

while

\[
\boxed{sup R_{\rm expected}=U(1)-U_\infty.}
\]

Hence

\[
\boxed{
U(2)-U_\infty
le K
<
U(1)-U_\infty
}
\]

is a frequency-assisted evolvability band.

For exponential opportunity value (U(c)=ve^{-mu c}), the band is

\[
\boxed{
ve^{-2\mu}
le K
<
ve^{-\mu}.
}
\]

At (mu=0.3,v=1,K=0.60), robust repayment is impossible for every finite
architecture, but expected repayment is possible with binary cues.

Inside this band, the scalable minimum mass on one-query states is

\[
\boxed{
p_{\rm crit}
=
\frac{
K-[U(2)-U_\infty]
}{
U(1)-U(2)
}.
}
\]

For the example above, (p_{\rm crit}approx0.2666).

This turns encounter frequencies into an explicit evolutionary resource.

### Inverse expected-value resource corner (supporting corollary)

The finite expected ceiling also gives a minimal architecture for **possible**
positive expected value, assuming a sufficiently skewed but strictly positive
encounter distribution.

Define

\[
J_K^{\rm expected}
=
\min\{j\ge2:U(1)-U(j)>K\}.
\]

If finite, the exact componentwise minimum is

\[
\boxed{
(n_{\min},m_{\min})
=
(J_K^{\rm expected}+1,J_K^{\rm expected}),
}
\]

achievable using binary queries at any permitted cue arity \(b\ge2\).

For \(U(c)=e^{-0.3c}\), the cases \(K=0.30\) and \(K=0.60\) require,
respectively, \((n,m)=(4,3)\) and \((8,7)\). At the latter minimum corner,
one-step encounters must exceed approximately \(90.4\%\) to pay \(K=0.60\);
the much smaller \(26.7\%\) threshold applies only to an unbounded scalable
rare-state burden.

These are existence results over possible world frequencies, not predictions
for an empirically fixed species assemblage or a separate main theorem.

### Ecological frequency floor (supporting no-go bound)

RF7 permits encounter frequencies to become arbitrarily concentrated. If each
represented world instead has probability at least \(\eta>0\), an adaptive
policy facing fixed cost \(j\) must leave at least \(j\) worlds unresolved
after the first query. Consequently,

\[
R_{\rm expected}
\le
\max_{2\le j\le M}
\left[
U(1)-U(j)-j\eta\{U(1)-U(2)\}
\right],
\]

with zero included if \(M=1\).

This bound is generally **not sharp** but is a valid no-go when an ecological
frequency floor is known.

At \(n=10,m=9,\ U(c)=e^{-0.3c}\), freely varying frequencies give an exact
expected supremum of \(0.673613\); uniform encounters \(\eta=0.1\) restrict
the expected advantage to at most \(0.500807\).

Thus the earlier \(K=0.60\) expected-rescue example is impossible under
uniform encounters. The model must measure or justify encounter frequencies
before using the arity-independent supremum as biological evidence.

### Novelty status

This section is biologically important but should **not** carry the paper's
theorem-level novelty claim. Prior-weighted expected decision-tree cost and the
ability of skewed distributions to concentrate mass on shallow leaves are
established ideas. In the present paper the exact expected ceiling is used to:

- separate frequency-free robust claims from frequency-dependent expected
  claims;
- prevent robust no-go results from being over-read as universal selection
  impossibility;
- provide a quantitative ecological interpretation of encounter-frequency
  skew.

The exact formula is therefore a model-specific corollary of the structural
framework, not a fourth independent main theorem.

## Biological synthesis

The core process is:

finite information constraints
-> exact adaptive/fixed frontier
-> natural-history completion value U(c)
-> robust recoverable value
-> architecture cost K
-> robust evolvability

When branch frequencies are known:

encounter-frequency distribution
-> early-termination premium
-> expected evolutionary value.

The central distinction is therefore

\[
\boxed{
\text{information architecture}

eq
\text{fitness},
}
\]

but finite architecture places exact limits on which fitness effects are
possible.

## Empirical anchor

Use Chandel et al. Aedes Figure 3a only as a temporal process-shape example.

The aggregate +IR effect after CO2 cessation is strongly late weighted:
half of the first post-pulse signed advantage accumulates after about 46.2 s,
and half of the second after about 46.5 s.

This supports the need for (U(c)) or an ecological value-of-time function.

It does not validate an adaptive/fixed architecture, individual completion-time
distributions, natural opportunity survival, architecture cost, or selection.

## SUPPLEMENT / interpretation only

Keep, but do not headline:

- stochastic opportunity-window formula;
- hazard-curvature identity;
- minimax versus fitness-optimal policy witness;
- urgency-induced policy switching;
- stochastic-dominance interpretation;
- comparator semantics;
- scalable low-urgency noncommuting limits;
- near-maximal-value complexity scaling;
- re-entrant urgency windows.

## Claims explicitly excluded from novelty

Do not claim novelty for sequential value of information, adaptive versus
nonadaptive expected-value gaps, deadline-weighted utility, adaptive-tree
flattening, time-pressure cue switching, worst-case versus expected
decision-tree cost, costly sensory fidelity, or generic sensory/decision
coevolution.

## Recommended headline

> Natural history re-ranks an exact finite frontier of information
> architectures, while encounter frequencies determine whether early branches
> can rescue architectures that are impossible to favor robustly.

Short form:

> Structural adaptive gain is potential; natural history and encounter
> frequencies determine which part of that potential is evolvable.

## Publication rule

The novelty spine contains MAIN 1-3 only. SUPPORT 1 is a biological consequence
and claim firewall, not a fourth novelty theorem.

Do not add another main theorem unless it invalidates or strictly strengthens
one of MAIN 1-3. New consequences belong in corollaries, empirical synthesis or
Supplement.
