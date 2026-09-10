# Joint structural-temporal ceiling for evolutionary fluctuation

## Purpose

The statement

> selection amplitude and temporal structure are generated on the same ecological state space

is conceptually useful but, by itself, does not impose a quantitative constraint.
This note supplies the missing inequality.

The result combines two existing ingredients:

1. a finite-sensing ceiling on the state-specific structural gap;
2. the standard spectral representation of reversible Markov-reward variance.

No novelty is claimed for Popoviciu's variance inequality or reversible Markov spectral theory. The repository-specific contribution is the composition with an exact finite information ceiling.

---

## 1. Structural amplitude ceiling

Suppose all recurrent community states belong to a declared finite sensing scope and their structural gaps satisfy

\[
0\le g_i\le g_{\max}.
\]

Under the continuous lift

\[
s_i=\lambda g_i-\kappa,
\]

the constant `kappa` disappears after centering and the reward range has width at most

\[
\lambda g_{\max}.
\]

Therefore

\[
\boxed{
\operatorname{Var}_\pi(s)
\le
\frac{(\lambda g_{\max})^2}{4}.
}
\]

The finite sensing theory supplies `g_max`. At fixed unit-cost scope `(n,m,b,h)` with optional productive-frontier edge cap `E`, one may use

\[
g_{\max}
\le
\min\{m,F_b(n,h),E\}-h,
\]

with the `E` term omitted when no edge cap is declared.

---

## 2. Temporal amplification ceiling

For a finite ergodic reversible community chain, expand the centered reward in nonstationary eigenmodes of the transition operator. Then

\[
\sigma_{\rm eff}^2
=
\sum_r w_r\frac{1+\rho_r}{1-\rho_r},
\]

where

\[
w_r\ge0,
\qquad
\sum_r w_r=\operatorname{Var}_\pi(s).
\]

Let

\[
r_{\max}=\max_r\rho_r<1
\]

be the largest nontrivial algebraic eigenvalue. Since

\[
f(r)=\frac{1+r}{1-r}
\]

is increasing on `(-1,1)`,

\[
\boxed{
\sigma_{\rm eff}^2
\le
\operatorname{Var}_\pi(s)
\frac{1+r_{\max}}{1-r_{\max}}.
}
\]

---

## 3. Joint ceiling

Combining the structural and temporal bounds gives

\[
\boxed{
\sigma_{\rm eff}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}}.
}
\]

This is the quantitative form of the amplitude-timescale coupling used in the paper.

It says that long-run fluctuation strength cannot be chosen independently of the finite information structure once the admissible structural reward range is fixed.

The ceiling separates two multipliers:

```text
finite sensing structure
    -> maximum instantaneous structural variance

community spectral persistence
    -> maximum temporal amplification of that variance
```

but they constrain a single downstream quantity, the asymptotic variance rate of cumulative centered selection.

---

## 4. Corollary: maximum asymptotic delay before directional trend dominates

Suppose stationary mean selection has nonzero magnitude

\[
|\mu|>0.
\]

The existing long-horizon approximation compares directional accumulation

\[
H|\mu|
\]

with fluctuation scale

\[
\sqrt{H\sigma_{\rm eff}^2}.
\]

Their asymptotic crossover proxy is

\[
H_\times^{\rm asy}
=
\frac{\sigma_{\rm eff}^2}{\mu^2}.
\]

Substituting the joint structural-temporal ceiling gives

\[
\boxed{
H_\times^{\rm asy}
\le
\frac{(\lambda g_{\max})^2}{4\mu^2}
\frac{1+r_{\max}}{1-r_{\max}}.
}
\]

Interpretation:

> finite information scope and community persistence bound how long short-term structural fluctuations can asymptotically mask a persistent directional bias of declared magnitude.

This is a bound on the **asymptotic crossover proxy**, not an exact finite-time first-passage or trend-detection theorem.

The dependence is transparent:

- larger structural gap ceiling delays emergence quadratically;
- stronger community persistence delays emergence through `(1+r_max)/(1-r_max)`;
- stronger directional bias shortens the delay as `1/mu^2`.

If `mu=0`, this crossover proxy is infinite and the system remains in the cancellation-stasis side of the exogenous theory rather than entering a persistent directional trend.

---

## 5. Sharpness

The joint variance bound is attained by a symmetric two-state community chain.

Let

\[
P=
\begin{pmatrix}
(1+r)/2 & (1-r)/2\\
(1-r)/2 & (1+r)/2
\end{pmatrix},
\qquad
\pi=(1/2,1/2),
\]

whose only nontrivial eigenvalue is `r`.

Choose endpoint structural rewards

\[
s=(0,\lambda g_{\max}).
\]

Then

\[
\operatorname{Var}_\pi(s)
=
\frac{(\lambda g_{\max})^2}{4},
\]

and all centered reward variance lies on the unique nontrivial mode. Hence

\[
\sigma_{\rm eff}^2
=
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r}{1-r}.
\]

Therefore the variance ceiling is sharp given only the declared reward range and maximal nontrivial eigenvalue. For any separately declared nonzero `|mu|`, the corresponding asymptotic crossover-proxy bound is then sharp with respect to the same variance information.

---

## 6. Why this matters for the paper

The broad fluctuating-selection result that temporal coherence affects long-run accumulation is prior art.

The role of this theorem is different. It puts the original `adaptive-gain` extremal mathematics directly inside temporal statements:

\[
\boxed{
\text{finite sensing ceiling}
\times
\text{community spectral persistence}
\Rightarrow
\text{maximum long-run selection fluctuation}.
}
\]

and, with nonzero directional bias,

\[
\boxed{
\text{finite sensing ceiling}
\times
\text{community persistence}
\times
\text{directional bias}^{-2}
\Rightarrow
\text{maximum asymptotic trend-emergence delay}.
}
\]

Thus Pillar A (common structural origin) and Pillar B (finite structural reachability) are not merely adjacent ideas. They meet in explicit inequalities that constrain long-timescale behavior.

---

## 7. Scope

The theorem assumes:

- a common declared upper bound `g_max` for all recurrent state-specific structural gaps;
- a linear structural lift `s_i=lambda*g_i-kappa`;
- a finite ergodic reversible community Markov chain;
- a known upper bound `r_max<1` on nonstationary eigenvalues.

The trend-emergence corollary additionally assumes a declared nonzero stationary mean-selection magnitude and uses the asymptotic crossover proxy `sigma_eff^2/mu^2`.

It does not claim the bound remains sharp for nonreversible chains, nonlinear structural lifts, heterogeneous scope constraints with no common gap ceiling, nonstationary community processes, or finite-time trend-detection procedures.
