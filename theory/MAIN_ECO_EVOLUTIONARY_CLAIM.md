# Main eco-evolutionary claim: coupled amplitude and temporal structure

## Why the question must be narrower than "fast short-term evolution versus long-term stasis"

The broad statement

> strong short-term evolution need not accumulate into large long-term change

is already standard in fluctuating-selection and quantitative-genetic theory. Directionally coherent selection accumulates; temporally varying selection can cancel.

That statement is therefore **not** the main novelty target of this repository.

The narrower claim is:

\[
\boxed{
\text{selection amplitude and temporal structure need not be independent free parameters.}
}
\]

In this framework they are generated on the **same ecological state space**. Each recurrent community state `i` carries a finite sensing task that determines

\[
C_A(i),\qquad C_F(i),\qquad g_i=C_F(i)-C_A(i),
\]

while the transition process `P` on those same states determines how the structurally generated rewards recur through time.

Thus the dynamic input is not an arbitrary pair

```text
selection amplitude
+ independently chosen temporal autocorrelation
```

but rather

```text
community-dependent information structure
    -> state-specific structural reward

community-state transition geometry
    -> recurrence of those same structural rewards
```

---

## 1. The main difference from standard fluctuating-selection framing

Let `s_i` denote the selection reward associated with community state `i` and let `P` be the community transition matrix. Temporal covariance is

\[
\gamma(k)
=
\sum_i\pi_i(s_i-\bar s)[P^k(s-\bar s)]_i.
\]

For reversible community dynamics,

\[
\sigma_{\rm eff}^2
=
\sum_r w_r\frac{1+\lambda_r}{1-\lambda_r},
\]

where the weights `w_r` depend on projection of the **structurally generated reward vector** onto community relaxation modes.

Hence

\[
\boxed{
\text{slow community dynamics matter evolutionarily only when structural selection aligns with those slow modes.}
}
\]

This is the useful coupling between short-term amplitude and long-term retention.

---

## 2. Why the static combinatorics must survive downstream

A danger in the dynamic extension is to compress every community state to the single scalar

\[
g_i=C_F(i)-C_A(i)
\]

and thereby relegate productive frontiers, continuation quotients, and sharp extremal structure to an appendix. The static theory survives downstream in three direct roles.

### 2.1 Finite structural ceilings restrict reachable dynamics

Suppose the structural lift is

\[
\Delta s=\lambda\Delta g.
\]

For the generalized local response,

\[
G=(-\beta e)\lambda\Delta g.
\]

The finite sensing theory supplies bounds

\[
\Delta g\le\Delta g_{\max}(n,m,b,h,E),
\]

where `E=|H_min|` is an optional productive-frontier edge cap. Therefore

\[
\boxed{
G\le(-\beta e)\lambda\Delta g_{\max}.
}
\]

If this ceiling lies below a dynamical phase threshold, that entire phase is structurally unreachable for the declared information scope.

### 2.2 Structural and temporal ceilings combine in one long-run bound

If all recurrent states satisfy

\[
0\le g_i\le g_{\max},
\]

and the community process is a finite ergodic reversible chain whose largest nontrivial algebraic eigenvalue is `r_max<1`, then

\[
\boxed{
\sigma_{\rm eff}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}}.
}
\]

A symmetric two-state chain with endpoint rewards attains equality. For nonzero stationary mean-selection magnitude `|mu|`, the asymptotic mean-versus-fluctuation crossover proxy obeys

\[
H_{\times}^{\rm asy}
\le
\frac{(\lambda g_{\max})^2}{4\mu^2}
\frac{1+r_{\max}}{1-r_{\max}}.
\]

This is a proxy ceiling, not an exact finite-time hitting-time theorem.

### 2.3 Required dynamical gain determines minimum or Pareto-minimal information complexity

Suppose a downstream dynamical regime requires integer structural gap

\[
q\ge1.
\]

#### Binary exact corner

For binary unit-cost sensing define

\[
\boxed{
h_2^*(q)=\min\{h\ge1:2^h-1-h\ge q\}.}
\]

Then the componentwise first binary corner capable of gap `q` is

\[
\boxed{
n^*=h_2^*+q+1,\qquad
m^*=h_2^*+q,\qquad
E^*=h_2^*+q.}
\]

Here `E*=|H_min|` is the minimum productive-frontier obligation count. The private-pair tree construction attains this corner. Moreover,

\[
h_2^*(q)=\log_2 q+O(1),
\]

so fixed-mandatory information obligations grow essentially linearly with the required gap while binary adaptive routing depth grows only logarithmically.

#### Bounded-arity generalization

For maximum query arity `b>=2`, define

\[
\boxed{
h_b^*(q)=\min\left\{h\ge1:\frac{b^h-1}{b-1}-h\ge q\right\}.}
\]

Then

\[
\boxed{m_{\min}(q,b)=E_{\min}(q,b)=q+h_b^*(q),}
\]

while the minimum world count is arity-independent,

\[
\boxed{n_{\min}(q)=q+h_2^*(q)+1.}
\]

At fixed depth `h`, let

\[
n_b(q,h)=\min\{n:F_b(n,h)\ge h+q\}.
\]

The exact joint information requirement is generally the nondominated set

\[
\boxed{
\mathcal P_b(q)
=
\operatorname{Pareto}\{(n_b(q,h),\ h+q,\ h+q)\}.
}
\]

Binary sensing is the special case in which this Pareto set collapses to one exact componentwise corner. For `b>2`, world minimization and query/frontier minimization can be incompatible. For example,

\[
q=3,\ b=4
\]

gives the two Pareto points

\[
(8,5,5),\qquad(7,6,6).
\]

Thus higher arity can lower query/frontier burden without lowering the absolute minimum world burden, exposing a genuine tradeoff rather than uniformly reducing all notions of complexity.

For generalized feedback

\[
G=a\Delta g,
\]

the strict complex-eigenvalue threshold supplies a required integer gap `q_osc`, so the general reachability map is

\[
\boxed{
(\alpha,\phi,a,b)
\longrightarrow
q_{\rm osc}
\longrightarrow
\mathcal P_b(q_{\rm osc}).
}
\]

If the integer gap ladder jumps directly beyond the upper stability threshold, the stable-oscillation Pareto set is empty.

The canonical binary case

\[
(\alpha,\phi,a)=(1,1/2,1/8)
\]

gives `q_osc=2` and

\[
\mathcal P_2(2)=\{(6,5,5)\}.
\]

No novelty is claimed for binary/bounded-arity tree counting, hitting-set inequalities, or generic Pareto optimization. The candidate contribution is their exact composition with adaptive/fixed structural gaps and evolutionary feedback thresholds.

---

## 3. Two distinct origins of stasis must remain separate

The framework contains two mathematically different mechanisms that can both look like long-term stasis.

### 3.1 Exogenous cancellation stasis

For additive periodic weak selection with zero sum over one cycle, the one-cycle map is exactly the identity and its multiplier is one. Short-term evolutionary activity can be arbitrarily large while retained period drift is zero.

Mechanism:

\[
\boxed{
\text{large movement + temporal sign cancellation + neutral period map.}
}
\]

### 3.2 Endogenous restoring stasis

Evolution changes the community state that generates future selection. If the local Jacobian has

\[
\rho(J)<1,
\]

small perturbations decay toward an interior equilibrium. Stable complex eigenvalues give oscillatory restoring dynamics.

Mechanism:

\[
\boxed{
\text{feedback-generated restoring attraction.}
}
\]

Thus

```text
cancellation stasis
    zero period drift + neutral return map

restoring stasis
    zero equilibrium drift + attractive local map
```

are not two descriptions of one mechanism.

---

## 4. Oscillation creates a qualitative identification window

The generalized local response has

\[
T=\alpha+\phi,
\qquad
D=\alpha\phi+(1-\phi)G.
\]

For any candidate community memory `phi<1`,

\[
G(\phi)=\frac{\phi^2-T\phi+D}{1-\phi}.
\]

The numerator is the characteristic polynomial evaluated at `phi`.

If the two local eigenvalues satisfy

\[
0\le r_1,r_2<1,
\]

choosing `phi=r_1` and `alpha=r_2` gives

\[
\boxed{G=0.}
\]

Therefore a stable monotone transient cannot by itself establish feedback existence within this model class.

If the eigenvalues form a non-real conjugate pair, the characteristic polynomial is strictly positive for every real `phi`; since `phi<1`,

\[
\boxed{G(\phi)>0}
\]

for every compatible decomposition. Thus oscillatory local dynamics force feedback existence, although feedback magnitude remains unidentified.

---

## 5. The four-pillar structure of the paper

### Pillar A — common structural origin
Short-term selection amplitude and long-term temporal filtering are generated on the same community-state space rather than chosen independently.

### Pillar B — finite structural reachability
Finite sensing structure bounds reachable dynamics and, conversely, maps a required structural/dynamical gap to an exact binary minimum or a bounded-arity Pareto-minimal information requirement.

### Pillar C — two origins of stasis
Exogenous cancellation is neutral over a full cycle; endogenous restoring feedback is attractive around an equilibrium.

### Pillar D — oscillation as a feedback-existence window
Stable monotone return may admit a no-feedback decomposition, whereas a complex local eigenpair forces positive feedback within the generalized model.

---

## 6. What not to make the headline

Do not lead with any of the following as the claimed novelty:

- strong short-term evolution need not imply large long-term change;
- fluctuating selection can generate apparent stasis;
- temporal autocorrelation matters;
- generic eco-evolutionary feedback can create oscillation;
- Jury stability or characteristic-polynomial algebra;
- binary or bounded-arity tree counting;
- hitting-set bounds or generic Pareto optimization;
- AR(2) inversion or generic nonidentifiability.

Those are prior-art or standard mathematical components.

The candidate novelty lies in the composition

\[
\boxed{
\text{required dynamical gain}
\to
\text{required structural gap}
\to
\text{minimum/Pareto-minimal finite information complexity}
\to
\text{reachable evolutionary timescales and phases}.
}
\]

That is the main line to preserve.
