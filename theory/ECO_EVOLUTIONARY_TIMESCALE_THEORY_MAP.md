# Eco-evolutionary timescale theory map

## Purpose

This map fixes the main theoretical hierarchy after removing observation-design work from scope.
The paper-level line is:

```text
finite individual information structure
    -> state-specific structural selection
    -> community-state temporal geometry
    -> short-term evolutionary amplitude
    -> long-term retention / cancellation / restoring dynamics
    -> reachable dynamical phases
```

The generalized nonidentifiability result is retained only as a **limit on interpreting time**. It is not an observation-design program.

---

## 0. Static structural core

For each finite sensing task,

\[
C_A=\text{minimum adaptive worst-path cost},
\qquad
C_F=\text{minimum fixed resolving cost},
\]

with structural advantage

\[
\boxed{g=C_F-C_A.}
\]

The static layer contains:

- continuation structure for adaptive resolution;
- productive-frontier / hitting-set structure for fixed resolution;
- exact decomposition of the adaptive-fixed gap;
- sharp bounded-arity and frontier-edge extremal bounds;
- adaptive-only budget windows.

The dynamic paper does **not** need every static object downstream. The part that carries decisive weight is the exact extremal ceiling

\[
\boxed{
\Delta g\le \Delta g_{\max}(n,m,b,h,E).
}
\]

Natural history defines the feasible cue/state structure; the finite theory constrains how much structural selection contrast that state can generate.

---

## 1. Exogenous temporal filtering: cancellation stasis

Branch lineage: `theory/evolutionary-timescale-filter` / PR #2.

Each recurrent community state `i` carries a structurally generated selection reward `s_i`, while the community transition process `P` is exogenous.

For stationary finite-state dynamics,

\[
\bar s=\sum_i\pi_i s_i,
\]

\[
\gamma(k)
=\sum_i\pi_i(s_i-\bar s)[P^k(s-\bar s)]_i.
\]

The key nonstandard composition is that `s` and `P` live on the **same ecological state space**. Selection amplitude and temporal recurrence are therefore not introduced as unrelated free parameters.

For reversible community dynamics,

\[
\sigma_{\rm eff}^2
=\sum_r w_r\frac{1+\lambda_r}{1-\lambda_r},
\]

where `w_r` is the projection of the structurally generated reward onto community relaxation mode `r`.

Hence

\[
\boxed{
\text{slow community modes matter only when structural selection projects onto them.}
}
\]

For zero-mean finite-correlation selection, short-term activity can remain large while the retained fraction scales as

\[
O(H^{-1/2}).
\]

This is **cancellation stasis**, not restoring feedback.

---

## 2. Endogenous eco-evolutionary feedback: restoring stasis

Branch lineage: `theory/endogenous-community-feedback` / PR #3.

Evolution now changes the community state that generates its future selection.
For the parent haploid/logit model, define

\[
L=-\eta\Delta s\,p^*(1-p^*).
\]

The exact local stability interval is

\[
\boxed{0<L<1.}
\]

Stable nonoscillatory return occurs for

\[
0<L\le(1-\phi)/4,
\]

and stable damped oscillation for

\[
(1-\phi)/4<L<1.
\]

Under

\[
\Delta s=\lambda\Delta g,
\]

the static structural gap becomes dynamical loop gain:

\[
\boxed{
L=(-\eta)\lambda\Delta g\,p^*(1-p^*).
}
\]

This is the first exact bridge from finite sensing structure to endogenous dynamics.

---

## 3. General evolutionary response

Branch lineage: `theory/general-evolutionary-response` / PR #5.

Let

\[
x_{t+1}=F(x_t,s(q_t)),
\qquad
q_{t+1}=\phi q_t+(1-\phi)Q(x_t).
\]

At an interior equilibrium define

\[
\alpha=\partial_xF,
\quad
\beta=\partial_sF,
\quad
e=Q'(x^*),
\]

and generalized loop gain

\[
\boxed{G=-\beta\Delta s\,e.}
\]

The Jacobian is

\[
J=
\begin{pmatrix}
\alpha & \beta\Delta s\\
(1-\phi)e & \phi
\end{pmatrix}.
\]

For `0<=alpha<=1` and `0<=phi<1`, stability is exactly

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

Thus intrinsic evolutionary persistence, community memory, and feedback gain jointly determine transient form and duration.

The parent model is the exact special case `alpha=beta=1` and `G=L`.

---

## 4. Static extremal theory as a dynamical reachability ceiling

This is the main reason the original combinatorics stays on the paper's central line.

If

\[
\Delta g\le\Delta g_{\max}(n,m,b,h,E)
\]

and

\[
G=(-\beta e)\lambda\Delta g,
\]

then

\[
\boxed{
G\le(-\beta e)\lambda\Delta g_{\max}.
}
\]

Therefore finite cue repertoire, arity, depth, and productive-frontier size impose a ceiling on attainable selection contrast and closed-loop gain.

Consequences include exact one-sided exclusions such as

\[
G_{\max}\le G_{osc}
\Rightarrow
\text{stable damped oscillation is structurally unreachable},
\]

and

\[
G_{\max}<G_+
\Rightarrow
\text{upper feedback instability is structurally unreachable}.
\]

The novelty target is not the extremal formula itself, but its use as a **dynamical reachability constraint**.

---

## 5. Two origins of stasis are dynamically inequivalent

See `TWO_ORIGINS_OF_STASIS.md`.

### Cancellation stasis

In the additive weak-selection coordinate

\[
z_{t+1}=z_t+E\beta_t,
\]

a periodic zero-sum cycle has

\[
\boxed{F_P(z)=z}
\]

and period multiplier exactly

\[
\boxed{1}.
\]

Short-term activity can be arbitrarily large while perturbations survive unchanged after every complete cycle. This is neutral stasis generated by temporal cancellation.

### Restoring stasis

For an endogenous fixed point with Jacobian `J`,

\[
\boxed{\rho(J)<1}
\]

implies local attraction. Perturbations decay.

Thus the same observation of little long-run net change can arise from

```text
cancellation stasis
    zero period drift + neutral return map

restoring stasis
    zero equilibrium drift + attractive local map
```

These mechanisms must not be collapsed into one category.

---

## 6. Oscillation creates a feedback-existence window

Branch lineage: `theory/general-response-identifiability` / PR #6.

The generalized local invariants are

\[
T=\alpha+\phi,
\qquad
D=\alpha\phi+(1-\phi)G.
\]

For any admissible candidate `phi<1`,

\[
G(\phi)=\frac{\phi^2-T\phi+D}{1-\phi}.
\]

The numerator is the characteristic polynomial evaluated at `phi`.

### Stable real nonnegative eigenvalues

If

\[
0\le r_1,r_2<1,
\]

then choosing `phi=r_1` and `alpha=r_2` gives

\[
\boxed{G=0.}
\]

Therefore monotone stable return does not, by itself, establish feedback existence in this model class.

### Complex eigenvalues

If the eigenvalues form a non-real conjugate pair, the characteristic polynomial is strictly positive for every real `phi`; with `phi<1`,

\[
\boxed{G(\phi)>0}
\]

for every compatible decomposition.

Therefore oscillatory local dynamics force feedback existence within the generalized model, although feedback magnitude remains unidentified.

This is retained as a **mechanism-identification theorem**, not as an observation-design program.

---

## 7. Time-interpretation limit

Even if local characteristic invariants `(T,D)` are known, they generally do not identify

\[
(\alpha,\phi,G).
\]

Indeed,

\[
\alpha(\phi)=T-\phi,
\qquad
G(\phi)=\frac{D-T\phi+\phi^2}{1-\phi}
\]

produce the same characteristic polynomial over the compatible ridge.

Hence an observed evolutionary timescale cannot generally be assigned uniquely to

- intrinsic evolutionary persistence `alpha`;
- community memory `phi`;
- feedback coupling `G`.

This nonidentifiability is retained only as a limit on interpreting temporal dynamics. The paper does not propose an observation or perturbation design program.

---

## 8. Four-pillar paper structure

### Pillar A — common structural origin

Selection amplitude and temporal recurrence are generated on the same ecological state space rather than chosen independently.

### Pillar B — finite structural reachability

Exact finite sensing ceilings bound attainable selection contrast and reachable dynamical phases.

### Pillar C — two origins of stasis

Cancellation is neutral across the forcing cycle; endogenous restoration is attractive around a fixed point.

### Pillar D — oscillation as a feedback-existence window

Monotone stable return may admit a zero-feedback decomposition, whereas a complex local eigenpair forces positive feedback within the generalized model.

---

## 9. Natural history in the retained main line

Natural history has two roles here.

### 9.1 It defines the feasible individual information structure

Examples such as

```text
long-range cue
    -> approach
    -> contact cue
    -> handling / reward / host assessment
```

define biologically possible queries and continuations, hence constrain `C_A`, `C_F`, and `Delta_g`.

### 9.2 It determines how information-mediated behavior rewires future community states

This supplies the ecological feedback sign and strength represented by `eta` in the parent model or `e=Q'(x*)` in the generalized model.

No observation-design role is claimed here.

---

## 10. What is not the novelty claim

Do not lead with:

- rapid short-term evolution can fail to accumulate;
- fluctuating selection can generate stasis;
- temporal autocorrelation matters;
- generic feedback can generate oscillation;
- Jury stability or characteristic-polynomial algebra;
- identity period maps or spectral-radius stability;
- generic nonidentifiability.

The candidate novelty is the composition

\[
\boxed{
\text{finite information structure}
\to
\text{structural selection}
\to
\text{community-mode alignment}
\to
\text{bounded reachable evolutionary timescales and phases}.
}
\]

That is the main line to preserve.
