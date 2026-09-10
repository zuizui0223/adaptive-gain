# Figure plan v1

## Design principle

Use no more than four main figures. The visual sequence should reflect the result hierarchy rather than implying four equal theorem claims: first establish the shared biological state space, then show the principal reachability theorem, then the supporting structural-temporal envelope, and finally the mechanistic/diagnostic distinction among long-time outcomes.

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

## Figure 2 — Principal result: required dynamics imply required finite information complexity

### Message

A requested local dynamical phase imposes a required structural gap, which imposes a minimum or Pareto-minimal sensing structure.

### Top flow

\[
(\alpha,\phi,a,b)
\to G_{\rm osc}
\to q_{\rm osc}
\to \mathcal P_b(q_{\rm osc})
\]

Make this the strongest visual statement in the paper.

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

Show visually why neither dominates the other.

### Panel C: arity asymmetry

A compact comparison:

`n_min = q + h_2*(q) + 1` — arity-independent

`m_min = E_min = q + h_b*(q)` — improves with arity.

### Takeaway

**Richer cues compress routing burden, but they do not necessarily reduce the ecological alternatives that make the decision difficult.**

---

## Figure 3 — Supporting result: structural-temporal extremal envelope and its slack

### Message

Finite information amplitude and community persistence impose an exact upper envelope on long-run evolutionary fluctuation, but realized variance can lie well below that envelope.

### Main equation

\[
\boxed{
\sigma_{\rm eff}^2
\le
\frac{(\lambda g_{\max})^2}{4}
\frac{1+r_{\max}}{1-r_{\max}}
}
\]

Label this explicitly as **extremally sharp**, not as a generic realized-variance prediction.

### Panel A: amplitude ceiling

Show structural rewards confined to `[0,g_max]`, with maximum centered variance at endpoint occupancy.

Label:

`range/variance saturation <= 1`.

### Panel B: temporal multiplier and mode alignment

Plot

\[
(1+r)/(1-r)
\]

against `r` for `0<=r<1`.

Use one slow and one fast community mode. Show two reward vectors:

- reward aligned with slow mode -> large temporal amplification;
- reward weakly aligned with slow mode -> realized fluctuation well below the extremal ceiling.

### Panel C: exact slack decomposition

Show

\[
\frac{\sigma_{\rm eff}^2}{B}
=
\underbrace{\frac{4\operatorname{Var}_\pi(s)}{(\lambda g_{\max})^2}}_{\text{range/variance saturation}}
\times
\underbrace{\frac{\sum_j\widetilde w_j f(r_j)}{f(r_{\max})}}_{\text{reward--slow-mode alignment}},
\]

where `B` is the theorem ceiling and `f(r)=(1+r)/(1-r)`.

### Panel D: equality witness

Two-state symmetric chain, endpoint rewards; mark equality with the theorem bound. Add a contrasting multi-state schematic where one or both slack factors are below one.

### Takeaway

**The ceiling is mathematically sharp because equality is attainable; its realized tightness depends on reward variance and modal alignment.**

---

## Figure 4 — Mechanistic long-time outcomes and diagnostic status

### Message

Similar long-term net change can arise from different dynamics. The cancellation/restoration distinction is interpretive, while only a model-compatible oscillatory local regime forces feedback existence inside the generalized model.

### Four side-by-side trajectories

1. **Directional accumulation**
   - persistent mean selection;
   - net displacement grows.

2. **Neutral cancellation stasis**
   - large within-cycle movement;
   - period returns exactly;
   - perturbation remains;
   - label `period multiplier = 1`;
   - mark as **mechanistic proposition**, not independent theorem novelty.

3. **Monotone restoring stasis**
   - perturbation decays monotonically;
   - label `rho(J)<1`;
   - note `G=0 decomposition may exist`.

4. **Oscillatory restoring stasis**
   - damped oscillation to equilibrium;
   - complex eigenpair;
   - first check `0<=T<2`;
   - highlight `G>0 forced within model class` only after that compatibility check;
   - mark as **diagnostic theorem**.

### Bottom algebraic strip

Stable real nonnegative modes:

\[
\phi=r_1,\ \alpha=r_2\Rightarrow G=0.
\]

Model-compatible complex modes:

\[
0\le T<2,
\qquad
\phi^2-T\phi+D>0
\Rightarrow G(\phi)>0.
\]

Boundary note: `alpha=1` is allowed by the generalized model, while `phi<1`; a neutral unit eigenvalue is therefore model-feasible in a zero-feedback decomposition but is not asymptotically stable return. If a complex transient has `T<0` or `T>=2`, label it **outside model domain**, not `feedback forced`.

### Takeaway

**Stasis is not one mechanism; model-compatible oscillatory restoration has a stronger feedback implication than monotone return.**

---

## Supplementary figures, only if needed

Possible Supplement-only visuals:

- productive-frontier/private-pair witness;
- bounded-arity recurrence geometry;
- critical slowing near lower/upper stability boundaries;
- exact validation / solver audit summary.

None is required for the ecological main narrative.
