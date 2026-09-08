# Evolutionary activity can stay fast while retained change vanishes proportionally

## Status

The probability identities in this note are standard results for partial sums of
stationary correlated processes. The repository does **not** claim the covariance
algebra as new.

The contribution of this branch is to place that temporal filter downstream of
the repository's exact structural opportunity generator:

\[
\text{community/cue structure}
\to
(C_A,C_F)
\to
\text{state-specific selection}
\to
\text{temporal retention}.
\]

The main conceptual result is that rapid short-term evolution and large long-term
evolution are controlled by different mathematical objects.

---

## 1. Symmetric fluctuating selection

Let selection have fixed magnitude `delta>0` but a temporally varying sign:

\[
s_t=\delta X_t,
\qquad X_t\in\{-1,+1\}.
\]

Assume a stationary symmetric sign process with

\[
E[X_t]=0,
\qquad
\operatorname{Corr}(X_t,X_{t+k})=\phi^k,
\]

where

\[
-1\le\phi\le1.
\]

A symmetric two-state Markov environment with probability `rho` of keeping the
same selection sign has

\[
\phi=2\rho-1.
\]

---

## 2. Short-term evolutionary activity does not slow down

Define cumulative absolute selection activity across `H` generations by

\[
A_H=\sum_{t=1}^H|s_t|.
\]

Because every generation has magnitude `delta`,

\[
\boxed{A_H=\delta H.}
\]

Thus evolutionary activity grows linearly with elapsed generations regardless of
whether the sign is persistent, independent, or alternating.

This formalizes one sense in which evolution can remain 'fast' at short temporal
resolution: every generation can experience equally strong selection.

---

## 3. Retained directional change follows a different scaling

Let

\[
S_H=\sum_{t=1}^Hs_t.
\]

Then

\[
E[S_H]=0
\]

and the standard covariance identity gives

\[
E[S_H^2]
=\delta^2 F_H(\phi),
\]

where

\[
\boxed{
F_H(\phi)
=H+2\sum_{k=1}^{H-1}(H-k)\phi^k.
}
\]

For `phi!=1` this has the exact closed form

\[
\boxed{
F_H(\phi)
=
H\frac{1+\phi}{1-\phi}
-
\frac{2\phi(1-\phi^H)}{(1-\phi)^2}.
}
\]

At perfect persistence,

\[
F_H(1)=H^2.
\]

The RMS retained directional displacement is therefore

\[
\boxed{
R_H^{\rm RMS}
=\sqrt{E[S_H^2]}
=\delta\sqrt{F_H(\phi)}.
}
\]

---

## 4. The retention fraction decays as H^{-1/2}

Normalize retained change by total short-term activity:

\[
\mathcal R_H^{\rm RMS}
=
\frac{R_H^{\rm RMS}}{A_H}
=
\frac{\sqrt{F_H(\phi)}}{H}.
\]

For every fixed

\[
-1<\phi<1,
\]

the long-horizon coherence factor is

\[
F_H(\phi)
\sim
H\frac{1+\phi}{1-\phi}.
\]

Hence

\[
\boxed{
\mathcal R_H^{\rm RMS}
\sim
\sqrt{\frac{1+\phi}{1-\phi}}
\;H^{-1/2}.
}
\]

This gives the key timescale distinction:

```text
short-term evolutionary activity  ~ H
RMS retained directional change   ~ sqrt(H)
retained fraction                  ~ H^(-1/2)
```

under zero-mean fluctuating selection with finite correlation time.

So evolution can remain strong generation after generation while the fraction of
that activity visible as long-term directional displacement shrinks toward zero.

Time acts here as a **retention filter**, not as a reduction in instantaneous
selection magnitude.

---

## 5. Three limiting regimes

### Perfect persistence: phi=1

The sign never changes within a realization.

\[
F_H(1)=H^2,
\qquad
\mathcal R_H^{\rm RMS}=1.
\]

All short-term activity is retained directionally.

### Temporal independence: phi=0

\[
F_H(0)=H,
\]

so

\[
\boxed{
\mathcal R_H^{\rm RMS}=H^{-1/2}.
}
\]

Activity remains linear in `H`, while the directional residue grows only as a
random walk.

### Perfect alternation: phi=-1

For every even `H`,

\[
F_H(-1)=0,
\]

and therefore

\[
\boxed{
R_H^{\rm RMS}=0.
}
\]

Every generation can have strong selection, but the long-term directional change
cancels exactly over each complete two-generation cycle.

This is the exact mathematical form of 'rapid reversible evolution plus long-term
stasis' used by the branch's structural collision witnesses.

---

## 6. Why this is different from the within-individual temporal result

The temporal-routing branch found that within an individual's sensing episode,
contingent information acquisition can benefit from temporal predictability
proportional to

\[
|\phi|.
\]

Both persistent and predictably alternating environments can tell an organism
which future cue will be useful.

Long-term directional evolution instead depends on **signed** selection
coherence.

Thus

\[
\boxed{
\text{predictable alternation can be good for individual routing}
}
\]

while simultaneously

\[
\boxed{
\text{predictable alternation can erase long-term directional evolution}.
}
\]

This cross-scale sign asymmetry is central to the proposed theory.

---

## 7. Coupling to the repository's structural opportunity

The upstream structural layer defines

\[
\Omega(X)
=\frac{C_F(X)-C_A(X)}{C_A(X)}.
\]

Existing sharp theorems determine how large `Omega(X)` can be at fixed finite
complexity.

A biological fitness map then turns state `X_t` into selection `s_t`. The temporal
filter described here determines whether those strong state-specific episodes are
retained.

The organizing decomposition is therefore

\[
\boxed{
\text{long-term evolutionary outcome}
=
\text{instantaneous structural opportunity}
\times
\text{state-specific biological fitness map}
\times
\text{temporal retention filter},
}
\]

where the multiplication sign is conceptual rather than a claim that every model
factorizes algebraically into three independent scalars.

The distinction matters:

- high `Omega` is neither necessary nor sufficient for long-term directional
  evolution if selection changes sign;
- high temporal persistence cannot create selection where structural opportunity
  and biological fitness differences are absent;
- moderate structural opportunity can accumulate strongly when the selection
  direction remains coherent.

---

## 8. Empirical implications

The theory suggests measuring at least three separate objects instead of one
'evolutionary rate'.

### Instantaneous activity

How much phenotypic/genetic response or selection occurs over short intervals?

### Structural opportunity

Does the current community/natural-history state create a large adaptive-only
window or a large `C_F-C_A` gap?

### Retention/coherence

Does the direction of selection persist across generations, or does it reverse?

A system with large first and second quantities but low signed coherence should
show rapid contemporary evolution with weak long-term directional accumulation.

A system with moderate instantaneous opportunity but high coherence can show the
opposite pattern.

---

## 9. Scope boundary

This note concerns a zero-mean stationary symmetric sign process as a minimal
analytical timescale model. It does not yet cover

- nonzero mean selection;
- evolving selection magnitude;
- trait-dependent environmental transition rates;
- demographic eco-evolutionary feedbacks;
- drift, mutation, migration, or diploidy;
- lineage birth/death or speciation;
- nonstationary geological or climatic trends.

Those extensions can change long-term scaling. The current theorem isolates the
minimal mechanism by which strong short-term evolutionary activity need not
accumulate proportionally over long time.
