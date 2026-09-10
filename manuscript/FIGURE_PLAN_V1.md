# Figure plan v1

## Design principle

Use no more than four main figures. Each figure must carry one theorem-level message and should be understandable before the reader sees the combinatorial proof machinery. The visual sequence should move from biological structure to temporal consequence.

No observation-design figure belongs in the paper.

---

## Figure 1 — One recurrent ecological state space generates both amplitude and recurrence

### Message

Selection amplitude and temporal recurrence are not independent phenomenological inputs in the framework. Both are indexed by the same recurrent community states.

### Suggested layout

Left: a small set of community states `i=1,...,K`.

For one highlighted state, show a schematic finite sensing tree:

`represented alternatives -> cue -> conditional cue -> action distinction`

Under it, label

`C_A(i)`, `C_F(i)`, `g_i=C_F(i)-C_A(i)`.

Right: the same state nodes connected by transition arrows forming `P`.

Bottom convergence:

`g_i -> s_i=lambda*g_i-kappa`

and

`P -> recurrence of the same s_i values`.

### One-sentence takeaway printed on figure

**Finite sensing structure sets state-specific amplitude; recurrence of the same states sets temporal filtering.**

### Optional natural-history inset

A single schematic line only:

`distant cue -> approach -> near cue -> contact -> handling`

Do not turn this into a measurement protocol.

### Do not show

- continuation quotients;
- productive-frontier hypergraphs;
- full test-cover terminology;
- observation design.

---

## Figure 2 — Structural-temporal sharp ceiling

### Message

Finite information amplitude and community persistence jointly cap long-run evolutionary fluctuation.

### Main equation

\[
\boxed{
\sigma_{\rm eff}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}}
}
\]

### Suggested layout

Panel A: amplitude ceiling.

Show structural rewards confined to `[0,g_max]`, with maximum centered variance at endpoint occupancy.

Label:

`structural ceiling = (lambda*g_max)^2/4`.

Panel B: temporal multiplier.

Plot

\[
(1+r)/(1-r)
\]

against `r` for `0<=r<1`.

Panel C: reward-mode alignment.

Use one slow and one fast community mode. Show two reward vectors:

- reward aligned with slow mode -> large temporal amplification;
- reward orthogonal to slow mode -> slow ecological persistence is evolutionarily irrelevant.

Panel D: equality witness.

Two-state symmetric chain, endpoint rewards; mark equality with the theorem bound.

### Takeaway

**Community persistence matters evolutionarily only when structurally generated reward loads onto the persistent mode.**

---

## Figure 3 — Required dynamics imply required finite information complexity

### Message

A requested local dynamical phase imposes a required structural gap, which imposes a minimum or Pareto-minimal sensing structure.

### Top flow

\[
(\alpha,\phi,a,b)
\to G_{\rm osc}
\to q_{\rm osc}
\to \mathcal P_b(q_{\rm osc})
\]

### Panel A: binary exact corner

For binary sensing, show

\[
h_2^*(q)=\min\{h:2^h-1-h\ge q\}
\]

and

\[
(n^*,m^*,E^*)=(h_2^*+q+1,h_2^*+q,h_2^*+q).
\]

Use the canonical example `q=2 -> (6,5,5)` as a small annotation, not the headline.

### Panel B: bounded-arity Pareto frontier

Plot world count `n` on x-axis and query/frontier burden on y-axis.

For `q=3,b=4`, mark both nondominated points:

- `(7,6,6)`;
- `(8,5,5)`.

Show why neither dominates the other.

### Panel C: arity asymmetry

A compact comparison:

`n_min = q + h_2*(q) + 1` — arity-independent

`m_min = E_min = q + h_b*(q)` — improves with arity.

### Takeaway

**Richer cues compress routing burden, but they do not necessarily reduce the ecological alternatives that make the decision difficult.**

---

## Figure 4 — Long-term outcomes and mechanistic status

### Message

Similar long-term net change can arise from different dynamics, and only the oscillatory local regime forces feedback existence inside the generalized model.

### Four side-by-side trajectories

1. **Directional accumulation**
   - persistent mean selection;
   - net displacement grows.

2. **Neutral cancellation stasis**
   - large within-cycle movement;
   - period returns exactly;
   - perturbation remains;
   - label `period multiplier = 1`.

3. **Monotone restoring stasis**
   - perturbation decays monotonically;
   - label `rho(J)<1`;
   - note `G=0 decomposition may exist`.

4. **Oscillatory restoring stasis**
   - damped oscillation to equilibrium;
   - complex eigenpair;
   - highlight `G>0 forced within model class`.

### Bottom algebraic strip

Real nonnegative modes:

\[
\phi=r_1,\ \alpha=r_2\Rightarrow G=0.
\]

Complex modes:

\[
\phi^2-T\phi+D>0\Rightarrow G(\phi)>0.
\]

### Takeaway

**Stasis is not one mechanism; oscillatory restoration has a stronger feedback implication than monotone return.**

---

## Supplementary figures, only if needed

Possible Supplement-only visuals:

- productive-frontier/private-pair witness;
- bounded-arity recurrence geometry;
- critical slowing near lower/upper stability boundaries;
- exact validation / solver audit summary.

None is required for the ecological main narrative.
