# Summary sufficiency ladder for ecological routeability

Status: post-freeze synthesis, revised after complete static-information matching.

The question is:

> how rich must an ecological information summary be before it determines fixed
> and adaptive routeability costs?

The answer is now sharper than a simple "summaries versus full table" divide.

---

## Level 0 — raw ecological counts

Matched:
- represented-state count;
- cue count;
- cue costs.

Not sufficient for \(C_F\) or \(C_A\).

---

## Level 1 — all one-cue marginals

Matched:
- Level 0;
- every cue outcome frequency.

The exact-balanced families make every binary cue exactly 50/50.

Not sufficient.

---

## Level 2 — complete cue-only joint distribution

Matched:
- the entire physical state-by-cue matrix;
- therefore every cue-only marginal and every cue-only joint distribution of
  every order.

Not sufficient.

Changing only the target/action map can change \((C_A,C_F)\).

---

## Level 3 — target amount

Additionally matched:
- target multiplicities;
- target entropy under the uniform world prior.

Not sufficient.

---

## Level 4 — total full-vocabulary target information

Additionally matched:

\[
I(T;Q_{\rm all})=H(T).
\]

Still not sufficient.

The asymptotic relational family has an unbounded fixed-to-adaptive ratio
separation under Levels 0–4.

---

## Level 5 — pairwise target-cue information profile

At finite registered scopes, the repository additionally matches the multiset of
canonical target-query \(2\times2\) profiles.

Still not sufficient.

These controls are finite and the pairwise match is a multiset match rather
than a name-by-name match.

---

## Level 6 — complete named static subset-information function

Define

\[
F(S)=I(T;Q_S),
\qquad
S\subseteq Q.
\]

The new 12-state, four-cue twins match:
- the same physical cue matrix;
- exact 6/6 balance of every cue;
- target multiplicities \((8,4)\);
- **every named value** \(F(S)\) for all \(2^4=16\) cue subsets.

They also match the stronger object

\[
\boxed{
H_A(U)=H_B(U)
\qquad
\forall U\subseteq\{T,q_0,q_1,q_2,q_3\}.
}
\]

Thus the complete Shannon entropy vector of the target and all four cues is
identical. Cue-only entropies match because the physical cue matrix is common;
target-containing entropies match because

\[
H(T,Q_S)=H(Q_S)+H(T\mid Q_S)
\]

and the conditional-entropy fingerprints match exactly.

Yet

\[
(C_A,C_F)_A=(4,4),
\qquad
(C_A,C_F)_B=(3,4).
\]

Therefore

\[
\boxed{
F(\cdot)\not\Rightarrow C_A.
}
\]

The separation is not bounded in absolute size. Taking \(r\) independent
coordinate copies preserves the complete Shannon entropy vector but gives

\[
(C_A,C_F)_A=(4r,4r),
\qquad
(C_A,C_F)_B=(3r,4r).
\]

Thus the adaptive-cost difference and the routeability-gap difference both
equal \(r\) and grow without bound. The matched construction does **not**
currently give an unbounded multiplicative \(C_F/C_A\) ratio; that stronger
ratio result uses the separate asymptotic family under weaker information
matching.

However, Level 6 has a new positive result.

For deterministic finite exact resolution under any strictly positive
full-support prior,

\[
S\text{ resolves }T
\iff
I(T;Q_S)=H(T).
\]

Hence

\[
\boxed{
C_F=
\min_{S:F(S)=H(T)}
c(S).
}
\]

So the complete static subset-information function is:

- **sufficient for \(C_F\)**;
- **insufficient for \(C_A\)**.

This is the key boundary that was missing from the previous ladder.

Executable witness:

- \`adaptive_gain/static_information_adaptive_separation.py\`
- \`tests/test_static_information_adaptive_separation.py\`

Formal statement:

- \`theory/STATIC_INFORMATION_ADAPTIVE_ACCESS_THEOREM.md\`

---

## Level 7 — outcome-resolved conditional continuation geometry

A static subset average does not retain which particular result occurred.

For a realized history

\[
h=(q_1=a_1,\ldots,q_r=a_r),
\]

the adaptive value obeys

\[
V(h)=0
\quad\text{if}\quad
H(T\mid h)=0,
\]

and otherwise

\[
V(h)
=
\min_{q\notin h}
\left[
c(q)+
\max_{a:P(q=a\mid h)>0}
V(h,q=a)
\right].
\]

The relevant information object is therefore outcome-resolved: each child
history is retained separately.

Conditional mutual information

\[
I(T;q\mid h)
\]

is an average immediate entropy reduction. A single CMI scalar does not retain
the worst child or which later cue becomes relevant there.

The MROD witness gives the simplest example:

\[
I(T;\mathrm{context})=0,
\]

but after context outcome 0,

\[
I(T;\mathrm{assay0}\mid \mathrm{context}=0)=1,
\qquad
I(T;\mathrm{assay1}\mid \mathrm{context}=0)=0,
\]

whereas after context outcome 1 the two values reverse.

Thus the routing observation can reveal no target information directly while
revealing **which later observation contains the target information**.

---

## Level 8 — complete action-conditioned cue table

Observed:
- world/state identity;
- target/action \(T(w)\);
- every cue outcome \(q_j(w)\);
- cue costs.

This representation directly specifies the deterministic finite problem and
therefore both \(C_A\) and \(C_F\).

The theory does not claim topology is fundamentally hidden.

It identifies the exact point at which static averaging remains insufficient.

---

## Identification ladder

\[
\begin{array}{rcl}
\text{counts} &\not\Rightarrow& (C_A,C_F)\\
\text{cue marginals} &\not\Rightarrow& (C_A,C_F)\\
\text{cue-only joint distribution} &\not\Rightarrow& (C_A,C_F)\\
H(T),I(T;Q_{\rm all}) &\not\Rightarrow& (C_A,C_F)\\
\text{pairwise target-cue profile} &\not\Rightarrow& (C_A,C_F)\\
F(S)=I(T;Q_S)\ \forall S
&\Rightarrow& C_F\\
F(S)=I(T;Q_S)\ \forall S
&\not\Rightarrow& C_A\\
\text{outcome-resolved continuation geometry}
&\Rightarrow& C_A\text{ by Bellman recursion.}
\end{array}
\]

---

## Relation to synergy and PID

Partial information decomposition asks how multiple sources contribute unique,
redundant and synergistic information to a target. That literature is relevant
and must be acknowledged.

But routeability is not defined as synergy.

An XOR/XNOR target provides the canonical case in which two cues jointly carry
information absent from either cue alone, yet if both cues are always required,

\[
C_A=C_F=2.
\]

The new Level-6 theorem goes further than pairwise synergy language: even the
complete Shannon entropy vector of the target and all cues can be identical
while adaptive cost differs.

This does **not** prove that every PID construction is identical for the matched
twins. PID measures can depend on structure not fixed by an entropy vector, and
multivariate PID definitions are not unique.

A 2026 active-feature-acquisition study by Li, Dhali & Bouma is direct prior
art for combining pairwise PID, realized-value conditional information and
budgeted sequential acquisition. The novelty boundary is therefore not
"synergy becomes useful sequentially"; it is the exact entropic-equivalence
counterexample and its ecological action-map interpretation.

Safe statement:

> static multivariate information content and sequential accessibility are
> distinct operational objects.

---

## Ecological consequence

The measurement question becomes:

1. What target/action is being resolved?
2. Which fixed cue subsets contain enough information to resolve it?
3. After each **realized** cue outcome, which distinctions remain?
4. Which later cue becomes relevant on that branch?
5. What does acquiring that cue cost relative to the ecological budget?

Richness, entropy and even a complete static subset-information scan answer
questions 1–2 incompletely and question 3 not at all.

---

## Experimental implication

The strongest direct empirical test should manipulate:
- one common physical cue environment;
- target/action mapping or decision topology;
- contingent versus fixed access;
- a finite ecological budget.

Existing public datasets with staged cue use can provide concordant biological
signatures, but they should not be called direct validation unless they identify
the branchwise acquisition object.

See:

- \`manuscript/PUBLIC_DATA_ROUTEABILITY_ELIGIBILITY_AUDIT_V1.md\`

---

## Current claim boundary

Established:
- static subset information exactly characterizes \(C_F\);
- complete static subset information can fail to identify \(C_A\);
- exact cue balance does not remove that failure;
- weaker information matching permits an unbounded adaptive/fixed separation.

Not established:
- unbounded \(C_A\) separation under a fully matched static subset-information
  function;
- equivalence or non-equivalence to every possible PID definition;
- noisy expected-loss analogues.

## One-line result

\[
\boxed{
\text{Static information identifies what must be available together; realized outcomes identify what must be acquired next.}
\]
