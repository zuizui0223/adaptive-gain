# Eco-evolutionary timescale theory map

## Purpose

This map fixes the logical hierarchy of the repository's ecological/evolutionary extension.
It distinguishes:

1. exact finite sensing structure;
2. exogenous temporal filtering;
3. endogenous eco-evolutionary feedback;
4. a special haploid-logit inverse;
5. a generalized evolutionary response;
6. generalized observability and identifiability limits.

The point is not that every layer is equally general.  Each stronger layer either adds a
mechanism or relaxes an assumption from the layer below it.

---

## 0. Static structural core: finite sensing tasks

For a finite deterministic sensing task, the repository defines

\[
C_A=\text{minimum worst-path adaptive resolution cost},
\]

\[
C_F=\text{minimum fixed resolving-bundle cost}.
\]

The static adaptive advantage is

\[
\boxed{g=C_F-C_A.}
\]

This layer contains the repository's exact structural mathematics:

- continuation structure for the adaptive side;
- productive-frontier / hitting-set structure for the fixed side;
- the decomposition

  \[
  C_F-C_A
  =(U-C_A)-(C_U-C_F)-(U-C_U);
  \]

- exact finite classifications;
- sharp bounded-arity / edge-cap extremal bounds;
- adaptive-only budget windows

  \[
  C_A\le B<C_F.
  \]

Ecological interpretation:

> natural history supplies the feasible cue graph; the static theory computes how much
> conditional routing can save relative to a fixed sensing repertoire.

This is the upstream structural source used by every later layer.

---

## 1. Exogenous community timescales

Branch / PR lineage: `theory/evolutionary-timescale-filter` / PR #2.

Each recurrent community state `i` carries a structural selection reward `s_i` generated
from its finite sensing task, while the community transition process is treated as
exogenous.

For finite-state Markov community dynamics with transition matrix `P`, stationary
probability `pi`, and reward vector `s`,

\[
\bar s=\sum_i\pi_i s_i
\]

is the long-run directional component and

\[
\gamma(k)=\sum_i\pi_i(s_i-\bar s)[P^k(s-\bar s)]_i
\]

is the selection autocovariance.

The finite-horizon accumulated selection variance is

\[
\operatorname{Var}(S_H)
=H\gamma(0)+2\sum_{k=1}^{H-1}(H-k)\gamma(k).
\]

For zero-mean selection, evolutionary activity can remain large while the retained
fraction decays like `H^-1/2`.

This layer separates three quantities:

```text
instantaneous magnitude
    how hard evolution moves in one generation

temporal coherence
    how long selection keeps the same dynamical direction

long-run directional bias
    whether one direction wins after temporal averaging
```

Important conclusion:

\[
\boxed{
\text{rapid short-term evolution does not imply large long-term accumulated change.}
}
\]

The spectral extension replaces a single two-state autocorrelation coefficient by
reward-weighted community relaxation modes.  Hence

\[
\boxed{
\text{community persistence}\ne\text{evolutionarily experienced persistence}.
}
\]

A slow community mode matters only if structural selection projects onto that mode.

---

## 2. Endogenous eco-evolutionary feedback

Branch / PR lineage: `theory/endogenous-community-feedback` / PR #3.

Now evolution changes the future community state that generates its own selection.

Let

\[
p_t=\text{frequency of the contingent sensing architecture},
\]

\[
q_t=\text{occupancy of the high-opportunity community state}.
\]

The parent closed loop is

\[
q_{t+1}=\phi q_t+(1-\phi)q_{target}(p_t),
\]

\[
\operatorname{logit}(p_{t+1})
=\operatorname{logit}(p_t)+s_-+(s_+-s_-)q_t.
\]

At an interior equilibrium the Jacobian in `(z=logit p,q)` coordinates is

\[
J=
\begin{pmatrix}
1 & \Delta s\\
(1-\phi)\eta p^*(1-p^*) & \phi
\end{pmatrix}.
\]

Define

\[
\boxed{L=-\eta\Delta s\,p^*(1-p^*).}
\]

Then local stability is exactly

\[
\boxed{0<L<1.}
\]

The local phase split is

\[
0<L\le(1-\phi)/4
\]

for stable nonoscillatory return and

\[
(1-\phi)/4<L<1
\]

for stable damped oscillation.

At `L=1`, a conjugate eigenvalue pair reaches the unit circle.

Under the continuous structural lift

\[
\Delta s=\lambda\Delta g,
\]

so

\[
\boxed{L=(-\eta)\lambda\Delta g\,p^*(1-p^*).}
\]

This is the first exact bridge from the static structural gap to a dynamical
closed-loop gain.

The inherited bounded-arity theory gives one-sided phase-exclusion certificates and,
using integer unit-cost gaps, finite ceilings on stable damping time and oscillation
period.

Status of this layer:

- deterministic;
- two community states;
- haploid/logit evolutionary coordinate;
- exact local theory and validated executable witnesses.

---

## 3. Special inverse under the haploid-logit response law

Branch / PR lineage: `theory/feedback-inverse-diagnostics` / PR #4.

This inverse is **conditional on the parent response law**.

For the parent Jacobian,

\[
T=1+\phi,
\qquad
D=\phi+(1-\phi)L.
\]

Thus an ideal local trajectory that identifies `(T,D)` gives

\[
\boxed{\phi=T-1}
\]

and

\[
\boxed{L=\frac{D-\phi}{1-\phi}.}
\]

Equivalent routes use

- the local eigenvalue pair;
- damping time + principal period;
- phenotype-logit AR(2) coefficients.

The empirical factorization is deliberately staged:

```text
transient
    -> phi, L
    -> independently measured eta and p*
    -> inferred selection contrast Delta_s
    -> direct state-specific fitness test
    -> natural-history finite sensing tasks
    -> Delta_g
    -> continuous-lift calibration or rejection
```

This branch also shows that inverse conditioning worsens as `phi -> 1`.

Crucial scope statement:

\[
\boxed{
\text{the time-series-only }(\phi,L)\text{ inverse is not generic.}
}
\]

It survives only because this branch fixes intrinsic evolutionary persistence to the
parent value `alpha=1`.

---

## 4. General evolutionary response

Branch / PR lineage: `theory/general-evolutionary-response` / PR #5.

Replace the specific haploid-logit update by a differentiable local evolutionary map

\[
x_{t+1}=F(x_t,s(q_t)),
\]

\[
q_{t+1}=\phi q_t+(1-\phi)Q(x_t).
\]

At equilibrium define

\[
\alpha=\partial_xF,
\qquad
\beta=\partial_sF,
\qquad
e=Q'(x^*).
\]

The local Jacobian is

\[
J=
\begin{pmatrix}
\alpha & \beta\Delta s\\
(1-\phi)e & \phi
\end{pmatrix}.
\]

Define generalized loop gain

\[
\boxed{G=-\beta\Delta s\,e.}
\]

For

\[
0\le\alpha\le1,
\qquad
0\le\phi<1,
\]

stability is exactly

\[
\boxed{
G_-:=\alpha-1
<G<
G_+:=\frac{1-\alpha\phi}{1-\phi}.
}
\]

The complex-eigenvalue threshold is

\[
\boxed{
G_{osc}=\frac{(\alpha-\phi)^2}{4(1-\phi)}.
}
\]

Hence

```text
G_- < G <= G_osc
    stable nonoscillatory return

G_osc < G < G_+
    stable damped oscillation
```

The parent model is recovered exactly with

\[
\alpha=1,
\quad\beta=1,
\quad e=\eta p^*(1-p^*),
\quad G=L.
\]

A qualitative parent conclusion does **not** survive:

\[
\alpha<1
\]

allows a finite stable interval with reinforcing ecological feedback,

\[
\boxed{\alpha-1<G<0.}
\]

Thus intrinsic evolutionary damping can buffer weak positive feedback.

There are two distinct critical-slowing boundaries:

### Lower weak-restoring boundary

\[
\boxed{
\tau_{lower}
\sim
\frac{2-\alpha-\phi}
{(1-\phi)(G-G_-)}.
}
\]

This is slow nonoscillatory return.

### Upper strong-feedback boundary

\[
\boxed{
\tau_{upper}
\sim
\frac{2}{(1-\phi)(G_+-G)}.
}
\]

This is slow damped oscillation near the unit-circle boundary.

The finite sensing theory still acts upstream through

\[
G=-\beta\lambda\Delta g\,e.
\]

Therefore natural-history structure constrains the available gain ladder, but response
geometry sets the dynamical phase boundaries.

---

## 5. General observability and identifiability

Branch / PR lineage: `theory/general-response-identifiability` / PR #6.

Once `alpha` is free, the earlier time-series-only inverse no longer identifies
biological timescales.

The generalized characteristic invariants are

\[
\boxed{T=\alpha+\phi}
\]

and

\[
\boxed{D=\alpha\phi+(1-\phi)G.}
\]

The scalar evolutionary coordinate obeys

\[
x_{t+2}=T x_{t+1}-D x_t.
\]

But inversion has **two distinct gates**.

### Gate 1: scalar mode observability

Four noiseless scalar observations recover `(T,D)` only when

\[
\boxed{R=x_0x_2-x_1^2\ne0.}
\]

Then

\[
\boxed{
T=\frac{x_0x_3-x_1x_2}{R},
\qquad
D=\frac{x_1x_3-x_2^2}{R}.
}
\]

For a two-real-mode trajectory

\[
x_t=c_1r_1^t+c_2r_2^t,
\]

\[
\boxed{R=c_1c_2(r_1-r_2)^2.}
\]

Therefore a long time series is not enough.  The perturbation/observable must expose
both local modes.

### Gate 2: biological decomposition

Even when `(T,D)` are known, every feasible candidate memory `phi` generates

\[
\boxed{\alpha(\phi)=T-\phi}
\]

and

\[
\boxed{
G(\phi)=\frac{D-T\phi+\phi^2}{1-\phi}
}
\]

with exactly the same scalar transient.

Thus

\[
\boxed{
(T,D)\text{ do not jointly identify }(\alpha,\phi,G).
}
\]

Either one independent persistence measurement is locally sufficient:

```text
independent alpha
    -> phi=T-alpha
    -> recover G

independent phi
    -> alpha=T-phi
    -> recover G
```

The parent inverse is the exact special case obtained by fixing `alpha=1`.

A stronger nonidentifiability result holds for stable high-trace trajectories:

\[
\boxed{
T\ge1
\Rightarrow
G(\phi)\to+\infty
\text{ as }\phi\to1^-.
}
\]

So the free transient alone may not even provide a finite upper bound on generalized
feedback gain or on the structural sensing mechanism that would be required to
produce it.

---

## 6. What "evolutionary time" means in the full hierarchy

The repository now distinguishes at least five clocks / timescale generators.

### 6.1 Within-individual information time

Cue acquisition and routing occur sequentially within an encounter or decision episode.
This is the original adaptive-observation logic.

### 6.2 Community-state residence / memory

`phi` or, in the finite-state Markov layer, reward-weighted relaxation modes determine how
long ecological conditions persist.

### 6.3 Intrinsic evolutionary persistence

`alpha` determines how strongly the evolutionary state carries itself into the next step
in the generalized local response.

### 6.4 Feedback gain

`G` couples the structural selection contrast back through ecological response and
selection responsiveness.

### 6.5 Long-run directional bias

The stationary mean selection determines whether short-term movement accumulates into a
long-term directional trend or cancels.

Hence there is no single scalar "evolutionary timescale" that can be read from a
phenotype trajectory without a model and independent measurements.

A compact summary is

\[
\boxed{
\text{observed trajectory geometry}
=\text{evolutionary persistence}
\oplus\text{community persistence}
\oplus\text{feedback coupling}
\oplus\text{directional bias}.
}
\]

The symbol `oplus` is conceptual, not an algebraic direct sum.

---

## 7. Natural history in the hierarchy

Natural history enters at three nonredundant points.

### 7.1 It defines the feasible sensing graph

Examples:

```text
long-range detection
    -> approach
    -> contact
    -> handling
    -> reward / host / mate assessment
```

This determines which finite queries and continuations are biologically possible and
therefore constrains `C_A`, `C_F`, and `Delta_g`.

### 7.2 It determines eco-evolutionary feedback sign and magnitude

The same sensory architecture can deplete, reinforce, or otherwise rewire the future
community state.  This enters through `eta` in the parent model or `e=Q'(x*)` in the
general response.

### 7.3 It determines what perturbation reveals the hidden modes

The scalar-observability gate shows that merely watching a system is insufficient.
A perturbation must project onto both local dynamical modes if both timescales are to be
recovered.

Thus natural history is not decoration or post-hoc interpretation.  It supplies both the
forward structural model and the interventions needed for inverse identification.

---

## 8. Claim hierarchy

### Exact structural claims

Supported directly by the finite sensing theory:

- `C_A`, `C_F`, strict adaptive gain, decomposition;
- productive-frontier / continuation sufficiency;
- sharp bounded-arity and edge-cap bounds;
- adaptive-only budget windows.

### Exact local dynamical claims

Supported by the deterministic feedback layers:

- parent loop-gain phase diagram;
- generalized response phase diagram;
- critical-slowing laws;
- finite structural phase-exclusion and transient-time ceilings.

### Exact local inverse / noninverse claims

Supported by the identifiability layers:

- parent inverse under `alpha=1`;
- scalar mode-observability determinant;
- generalized `(alpha,phi,G)` equivalence ridge;
- high-trace unbounded-gain nonidentifiability.

### Not yet claimed

- noisy statistical consistency from finite empirical time series;
- process-noise / measurement-noise identifiability;
- multivariate quantitative genetics;
- explicit diploid genotype dynamics;
- mutation, migration, drift;
- globally nonlinear bifurcation classification;
- empirical confirmation in a real natural-history system;
- novelty of generic feedback, AR(2), Jury stability, critical slowing, or trace/determinant inversion.

---

## 9. Recommended conceptual paper spine

The strongest unified ecological/evolutionary statement is not

> adaptive measurement is useful.

It is closer to

> ecological structure determines which information pathways are available and how much
> conditional sensing can gain; community dynamics and evolutionary response determine
> whether that structural opportunity appears as a short burst, reversible fluctuation,
> long transient, instability, or long-term trend; observed evolutionary time alone does
> not identify which clock generated it.

A compact mathematical spine is

\[
\boxed{
\text{natural-history cue structure}
\to(C_A,C_F)
\to\Delta g
\to\Delta s
\to G
\to\text{phase / timescale}
}
\]

for the forward direction, and

\[
\boxed{
\text{trajectory}
\to\text{mode observability}
\to(T,D)
\to\text{persistence measurement}
\to G
\to\text{structural compatibility / falsification}
}
\]

for the inverse direction.

The two arrows meet only when natural history and independent ecological/evolutionary
measurements supply the factors that the time series itself cannot identify.
