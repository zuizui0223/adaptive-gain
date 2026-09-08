# Structural reward mode alignment from existing adaptive-gain tasks

## Status

This note makes the community spectral result repository-native.

The spectral identities themselves are standard.  The point here is that the
reward vectors aligned with slow and fast community modes can be generated from
**existing exact adaptive-gain tasks**, rather than introduced as arbitrary
numbers.

---

## 1. Existing tasks provide structural gaps 0, 1, and 2

Use three already-registered task classes.

### Gap 0

`routing_bypass_control()` has

\[
(C_A,C_F)=(2,2),
\]

so

\[
g=C_F-C_A=0.
\]

### Gap 1

`payoff_routing_task()` has

\[
(C_A,C_F)=(2,3),
\]

so

\[
g=1.
\]

### Gap 2

`extremal_routing_task(3)` has

\[
(C_A,C_F)=(2,4),
\]

so

\[
g=2.
\]

No new sensing witness is invented for this spectral construction.

---

## 2. One common three-state community chain

Use the symmetric transition matrix

\[
P=
\begin{pmatrix}
0.7&0&0.3\\
0&0.7&0.3\\
0.3&0.3&0.4
\end{pmatrix}
\]

with stationary distribution

\[
\pi=(1/3,1/3,1/3).
\]

Its nonstationary relaxation eigenvalues are

\[
\lambda_{slow}=0.7,
\qquad
\lambda_{fast}=0.1.
\]

The slow contrast is proportional to

\[
(1,-1,0),
\]

while the fast contrast is proportional to

\[
(1,1,-2).
\]

The **community dynamics are held fixed** throughout the comparison.

---

## 3. Existing structural gaps can be aligned with the slow mode

Place the gap-2, gap-0, and gap-1 tasks on the three community states in that
order.

Under

\[
s_i=\lambda g_i-\kappa
\]

choose

\[
\lambda=\kappa=\sqrt{3/2}.
\]

Then the structural reward vector is

\[
\boxed{
s_{slow}
=\sqrt{3/2}(1,-1,0).
}
\]

It has stationary mean zero and stationary variance one.

Because it lies entirely in the `0.7` mode,

\[
\boxed{
\sigma_{eff,slow}^2
=\frac{1+0.7}{1-0.7}
=\frac{17}{3}.
}
\]

---

## 4. Existing structural gaps can also be aligned with the fast mode

Now place the gap-2 task on the first two community states and the gap-0 task on
the third.

Choose

\[
\lambda=\frac{3}{2\sqrt2},
\qquad
\kappa=\sqrt2.
\]

Then

\[
\boxed{
s_{fast}
=\left(\frac1{\sqrt2},\frac1{\sqrt2},-\sqrt2\right),
}
\]

which also has stationary mean zero and stationary variance one.

It lies entirely in the `0.1` mode, so

\[
\boxed{
\sigma_{eff,fast}^2
=\frac{1+0.1}{1-0.1}
=\frac{11}{9}.
}
\]

---

## 5. Same ecology, same reward variance, different evolutionary time

The ratio is

\[
\boxed{
\frac{\sigma_{eff,slow}^2}{\sigma_{eff,fast}^2}
=\frac{51}{11}
\approx4.64.
}
\]

Everything listed below is held fixed:

- number of community states;
- transition matrix;
- stationary distribution;
- stationary mean selection (=0);
- stationary selection variance (=1).

What changes is only **which community-state contrast carries the repository's
structural adaptive advantage**.

Therefore raw community persistence and marginal selection variance do not
determine the long evolutionary timescale.

The missing object is the alignment

\[
\boxed{
\text{structural reward geometry}
\times
\text{community relaxation geometry}.
}
\]

---

## 6. Ecological interpretation

Suppose three recurring community states correspond, for example, to different
pollinator assemblages, predator regimes, or host/resource stages.

Two systems could have the same state frequencies and the same transition
matrix.  They could also have the same overall variance in selection on a
contingent sensory architecture.

Yet if the adaptive-only sensing advantage distinguishes states along a slowly
switching community contrast in one system and a rapidly relaxing contrast in
the other, short-term evolutionary bursts will persist for very different
lengths of time.

This sharpens the statement

```text
community temporal structure
!=
evolutionarily experienced temporal structure.
```

The evolutionary timescale depends on **which ecological contrast changes the
information problem faced by individuals**.

---

## 7. Prior-art boundary

No novelty is claimed for eigenmode decompositions of Markov chains or for the
factor `(1+lambda)/(1-lambda)`.

The repository-specific result is that already-proved structural sensing tasks
with exact `(C_A,C_F)` values can be assigned to the same community dynamics and
produce distinct reward-mode alignments with more than fourfold different
long-run fluctuation scales.
