# Community spectral timescale for structurally generated selection

## Status

This note generalizes the two-state `m, phi` timescale formulas to arbitrary
finite community-state Markov dynamics.

The Markov-reward and Poisson-equation identities used here are standard.  The
repository does **not** claim new probability theory.  The modeling contribution
is the upstream link from each ecological state to a structurally generated
selection reward through the repository's exact adaptive/fixed sensing theory.

The central ecological message is:

> community persistence matters for evolution only through the dynamical modes
> onto which state-specific structural selection actually projects.

Thus a slow ecological mode need not be a slow evolutionary mode.

---

## 1. Finite community states carry structural selection rewards

Let community state be

\[
X_t\in\{1,\ldots,K\}
\]

with stationary distribution `pi` and transition matrix `P`.

Each state `i` supplies a finite sensing task and therefore a state-specific
selection value `s_i`.  For example, under the continuous structural lift,

\[
s_i
=\lambda[C_F(i)-C_A(i)]-\kappa,
\]

while a hard-budget lift can assign rewards from whether the common ecological
budget lies inside the adaptive-only window

\[
C_A(i)\le B<C_F(i).
\]

The finite-state Markov layer itself does not care which valid biological lift
created `s`; it receives the reward vector

\[
s=(s_1,\ldots,s_K).
\]

---

## 2. Long-run direction comes from occupancy-weighted reward

The stationary mean selection is

\[
\boxed{
\bar s=\sum_i\pi_i s_i.
}
\]

Expected cumulative selection after `H` generations is

\[
\boxed{
E[S_H]=H\bar s.
}
\]

Therefore the existence of a long-run directional evolutionary trend depends
on the occupancy-weighted reward imbalance, not on community switching speed by
itself.

If

\[
\bar s\ne0,
\]

the mean directional component is `O(H)`.

If

\[
\bar s=0,
\]

there is no linear directional mean even if selection is strong in every state.

---

## 3. Community switching generates reward autocovariance

Define centered reward

\[
c=s-\bar s\mathbf 1.
\]

Then

\[
\boxed{
\gamma(k)
=\operatorname{Cov}(s_t,s_{t+k})
=\sum_i\pi_i c_i(P^k c)_i.
}
\]

The exact finite-horizon cumulative variance is

\[
\boxed{
\operatorname{Var}(S_H)
=H\gamma(0)
+2\sum_{k=1}^{H-1}(H-k)\gamma(k).
}
\]

This already shows why community-state autocorrelation alone is insufficient:
`P` acts on the centered **selection reward**, not on a generic ecological state
label.

---

## 4. Poisson equation gives the general long-timescale coefficient

Let `Pi` denote the matrix with every row equal to `pi`.

Solve

\[
\boxed{
(I-P+\Pi)h=c.
}
\]

For an irreducible finite chain this system is nonsingular.  The effective
long-run variance per generation is

\[
\boxed{
\sigma_{\rm eff}^2
=2\langle c,h\rangle_\pi
-\langle c,c\rangle_\pi.
}
\]

When the covariance series is summable this equals

\[
\boxed{
\sigma_{\rm eff}^2
=\gamma(0)+2\sum_{k\ge1}\gamma(k).
}
\]

Hence

\[
\operatorname{Var}(S_H)
\sim H\sigma_{\rm eff}^2.
\]

This `sigma_eff^2` is the general finite-community replacement for the
single two-state factor involving `phi`.

---

## 5. Zero-mean selection: general H^{-1/2} retention law

Let

\[
a=E_\pi|s|
=\sum_i\pi_i|s_i|.
\]

If

\[
\bar s=0
\]

and `a>0`, expected total absolute selection activity is

\[
A_H=Ha.
\]

Meanwhile

\[
R_H^{\rm RMS}
\sim\sqrt{H}\,\sigma_{\rm eff}.
\]

Therefore

\[
\boxed{
\frac{R_H^{\rm RMS}}{A_H}
\sim
\frac{\sigma_{\rm eff}}{a}H^{-1/2}.
}
\]

The exponent `-1/2` is therefore not restricted to the two-state model.  What
changes across community systems is the prefactor

\[
\boxed{
K_{\rm eco}=\frac{\sigma_{\rm eff}}{E_\pi|s|}.
}
\]

The community dynamics determine how large the finite-time residue is before
that fraction decays.

---

## 6. Nonzero mean: general trend-emergence horizon

If

\[
\bar s\ne0,
\]

then

\[
|E[S_H]|=H|\bar s|
\]

while the correlated fluctuation standard deviation is asymptotically

\[
\sqrt{H}\,\sigma_{\rm eff}.
\]

Equating the two gives the general crossover scale

\[
\boxed{
H_\times
\approx
\frac{\sigma_{\rm eff}^2}{\bar s^2}.
}
\]

Interpretation:

- larger stationary directional bias shortens the time until a long-run trend is
  visible;
- stronger reward-weighted community persistence increases `sigma_eff^2` and can
  hide a weak long-run trend behind long short-term runs;
- fast ecological modes that do not affect `s` do not enlarge this timescale.

---

## 7. Reversible-chain spectral interpretation

For a reversible community chain, expand the centered reward in orthogonal
community relaxation modes.  Let `lambda_r` be a nonstationary eigenvalue and
`w_r>=0` the reward variance carried by that mode.

Then

\[
\boxed{
\sigma_{\rm eff}^2
=
\sum_r
w_r\frac{1+\lambda_r}{1-\lambda_r}.
}
\]

This formula sharpens the ecological interpretation.

A slow mode with

\[
\lambda_r\approx1
\]

creates a long evolutionary memory only if

\[
w_r>0.
\]

If the structural selection reward is orthogonal to that mode, the mode is
almost invisible to evolution even though it dominates raw community relaxation.

Therefore

\[
\boxed{
\text{community mixing time}
\not\Rightarrow
\text{evolutionary selection timescale}.
}
\]

The correct object is **reward-weighted community relaxation**.

---

## 8. Exact three-state mode-alignment counterexample

The executable tests register one symmetric three-state chain with stationary
mass `1/3` and nonstationary eigenvalues

\[
0.7,\qquad0.1.
\]

Two centered reward vectors are chosen with identical stationary variance one.

One reward aligns entirely with the slow `0.7` mode, giving

\[
\sigma_{\rm eff,slow}^2
=
\frac{1+0.7}{1-0.7}
=
\frac{17}{3}.
\]

The other aligns with the fast `0.1` mode, giving

\[
\sigma_{\rm eff,fast}^2
=
\frac{1+0.1}{1-0.1}
=
\frac{11}{9}.
\]

Thus the **same community transition matrix** and the **same stationary reward
variance** produce more than a fourfold difference in long-run selection
variance solely because the structural reward points along a different community
mode.

This is the finite-community version of the distinction

```text
environmental temporal structure
!=
evolutionarily experienced temporal structure.
```

---

## 9. Recovery of the two-state formulas

For the two-state community chain

\[
P=
\begin{pmatrix}
1-a&a\\
b&1-b
\end{pmatrix},
\]

the unique nonstationary eigenvalue is

\[
\phi=1-a-b.
\]

For reward magnitude `delta` and stationary sign bias `m`,

\[
\sigma_{\rm eff}^2
=
\delta^2(1-m^2)
\frac{1+\phi}{1-\phi}.
\]

Therefore

\[
H_\times
=
\frac{\sigma_{\rm eff}^2}{(\delta m)^2}
=
\frac{1-m^2}{m^2}
\frac{1+\phi}{1-\phi},
\]

recovering the previously derived two-state crossover formula exactly.

So the earlier `phi` model is not discarded; it is the one-mode special case of
the finite-community theory.

---

## 10. Relation to the repository's structural mathematics

The Markov chain does not generate the reward values on its own.

The repository supplies the upstream state map

\[
X_i
\longmapsto
\bigl(
\operatorname{ContinuationType}_i,
\mathcal H_{\min,i}
\bigr)
\longmapsto
(C_A(i),C_F(i))
\longmapsto
s_i.
\]

Hence the full cross-scale object is

\[
\boxed{
\text{structural reward geometry}
+
\text{community transition geometry}.
}
\]

Neither part alone determines evolutionary timescale.

This is especially important because the repository already proves that weaker
resource summaries can fail to determine `C_F`.  Therefore two communities that
look similar under marginal cue summaries can induce different reward vectors and
consequently different projections onto the same ecological dynamical modes.

---

## 11. Natural-history interpretation

Natural history enters twice.

### Structural side

It defines which cue sequences are physically feasible:

```text
distant detection
-> approach
-> contact
-> handling
```

and therefore which continuation/frontier task a community state induces.

### Dynamical side

It defines how community states switch or persist:

- seasonal replacement;
- pollinator turnover;
- predator regime shifts;
- host-stage succession;
- resource pulses;
- disturbance/recovery states.

The theory predicts that a long-lived ecological mode affects evolutionary
retention only when the associated state contrast also changes the structural
selection reward.

---

## 12. Prior-art boundary

The following are standard and are not claimed as new:

- Markov reward processes;
- Poisson equations for additive functionals of Markov chains;
- asymptotic variance and integrated autocovariance;
- reversible-chain spectral decompositions;
- central-limit scaling of cumulative rewards.

The proposed contribution remains the structural ecological bridge:

```text
community state
-> exact finite sensing structure
-> state-specific selection reward
-> reward-weighted community modes
-> evolutionary retention / crossover time.
```

No empirical claim is made until natural data support both the state-specific
sensing tasks and the community transition process.
