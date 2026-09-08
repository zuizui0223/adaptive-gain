# Prior-art boundary: eco-evolutionary timescales and fluctuating selection

## Purpose

This note prevents the evolutionary-timescale branch from claiming novelty for established ideas.

The branch does **not** claim as new:

- eco-evolutionary feedbacks;
- rapid or contemporary evolution;
- fluctuating selection;
- temporal reversals in directional selection;
- the possibility that rapid short-term changes coexist with long-term stasis;
- individual behavior or information use affecting ecological interactions and community dynamics;
- the standard haploid log-odds selection recurrence;
- partial-sum autocovariance identities;
- the general warning that evolutionary rate divided by elapsed time is difficult to interpret.

The proposed contribution is narrower: use the repository's exact finite sensing structures to specify a mechanistic, state-dependent source of selection on sensory architecture and then trace how temporal cancellation filters that selection across generations.

---

## 1. Fluctuating selection and stasis are established

Bell (2010) explicitly argued that strong natural selection can fluctuate in intensity and direction and that repeated reversals can reconcile rapid adaptation with limited long-term directional change.

**Reference**

Bell, G. (2010). Fluctuating selection: the perpetual renewal of adaptation in variable environments. *Philosophical Transactions of the Royal Society B*, 365, 87–97. https://doi.org/10.1098/rstb.2009.0150

Messer, Ellner & Hairston (2016) likewise highlighted the contrast between rapid heritable phenotypic change observed over a few generations and longer-term trajectories that can remain bounded when selection changes direction.

**Reference**

Messer, P. W., Ellner, S. P., & Hairston, N. G. Jr. (2016). Can Population Genetics Adapt to Rapid Evolution? *Trends in Genetics*, 32(7), 408–418. https://doi.org/10.1016/j.tig.2016.04.005

Recent syntheses of long-term field studies also emphasize that opposing episodes of directional selection can combine to yield long-term stasis even when within-generation stabilizing selection is uncommon.

Therefore the statement

```text
strong short-term selection + directional reversals -> little long-term net change
```

is prior art.

---

## 2. Eco-evolutionary feedbacks are established

Post & Palkovacs (2009) defined eco-evolutionary feedbacks as reciprocal interactions in which ecological change alters evolution and evolved organismal differences feed back to ecological interactions, communities, or ecosystems.

**Reference**

Post, D. M., & Palkovacs, E. P. (2009). Eco-evolutionary feedbacks in community and ecosystem ecology: interactions between the ecological theatre and the evolutionary play. *Philosophical Transactions of the Royal Society B*, 364, 1629–1640. https://doi.org/10.1098/rstb.2009.0012

Govaert et al. (2019) reviewed theoretical eco-evolutionary feedback models across populations, communities, abiotic environments, and spatial scales, stressing that such feedback theory has a long history and can be represented by coupled ecological and evolutionary formalisms.

**Reference**

Govaert, L., Fronhofer, E. A., Lion, S., et al. (2019). Eco-evolutionary feedbacks—Theoretical models and perspectives. *Functional Ecology*, 33(1), 13–30. https://doi.org/10.1111/1365-2435.13241

Therefore the generic loop

```text
ecology -> evolution -> ecology
```

is not a repository novelty.

---

## 3. Individual behavior and information can scale up to communities

The step from individual phenotype or behavior to altered ecological interactions is also established.

Werner & Peacor (2003) reviewed trait-mediated indirect interactions in ecological communities. Their core point is that a species' phenotypic or behavioral response to another species can alter its per-capita effects on other species, changing population density or fitness and thereby restructuring community interactions.

**Reference**

Werner, E. E., & Peacor, S. D. (2003). A review of trait-mediated indirect interactions in ecological communities. *Ecology*, 84(5), 1083–1100. https://doi.org/10.1890/0012-9658(2003)084[1083:AROTII]2.0.CO;2

Gil et al. (2018) explicitly synthesized how social information use can link individual behavior to population and community dynamics, including changes in density dependence, competition, species interactions, and extinction risk.

**Reference**

Gil, M. A., Hein, A. M., Spiegel, O., Baskett, M. L., & Sih, A. (2018). Social Information Links Individual Behavior to Population and Community Dynamics. *Trends in Ecology & Evolution*, 33(7), 535–548. https://doi.org/10.1016/j.tree.2018.04.010

Therefore the generic statement

```text
individual information/behavior -> interaction changes -> community consequences
```

is prior art.

The present branch must make a narrower claim: the repository's exact continuation/frontier mathematics can distinguish **which higher-order cue structures change the structural advantage of contingent sensing**, and therefore can supply a specific state-dependent selection mechanism inside that already-established individual-to-community framework.

---

## 4. Rate-time scaling should not be the main observable

De Lisle & Svensson (2026) revisited evolutionary rate–time relationships and showed that much negative rate–time scaling follows from the mathematical dependence created by dividing evolutionary change by elapsed time. Their reanalysis found that over 99% of variation in rate–time relationships across six datasets was explained by time variation alone. They recommend focusing more directly on how evolutionary change accumulates with time.

**Reference**

De Lisle, S. P., & Svensson, E. I. (2026). Revisiting evolutionary rate–time relationships. *Evolution*, 80(1), 28–39. https://doi.org/10.1093/evolut/qpaf222

This is directly relevant to the current branch.

The branch therefore does **not** use

\[
\text{evolutionary rate}=\frac{\text{change}}{\text{time}}
\]

as its central cross-timescale quantity.

Instead it tracks

- total absolute evolutionary selection activity;
- signed cumulative log-odds change;
- retained displacement;
- retention ratio across increasing windows.

This aligns the model with accumulated change rather than a denominator-confounded rate-time plot.

---

## 5. What the repository adds to this literature

The new bridge starts one mechanistic layer earlier than standard fluctuating-selection models.

A community state `X` is mapped to a finite sensing task

\[
\mathcal T(X).
\]

Existing repository theorems then give

\[
C_A(X)=V_A(\operatorname{Type}(X))
\]

and

\[
C_F(X)=\tau_c(\mathcal H_{\min}(X)).
\]

Under the deliberately minimal sensing-cost fitness model,

\[
\boxed{
s(X)
=\lambda[C_F(X)-C_A(X)]-\kappa.
}
\]

Thus the ecological state affects evolution through two already-proved structural summaries:

```text
adaptive continuation structure
+
productive-frontier structure.
```

The branch then reuses the repository's exact decomposition

\[
C_F-C_A
=(U-C_A)-(C_U-C_F)-(U-C_U)
\]

to separate selection on contingent sensing into

```text
branch-exclusive opportunity
- external shortcut discount
- internal union redundancy.
```

Across community states the same mathematics gives

\[
\boxed{
\Delta s
=\lambda\Delta C_F
-\lambda\Delta C_A
-\Delta\kappa,
}
\]

which separates productive-frontier rewiring from adaptive-continuation rewiring and a separately modeled control-cost channel.

The registered `resource_role_profile_collision()` sharpens this point: two tasks can have the same adaptive continuation root type and the same multiset of per-resource role profiles while `C_F` differs. Under the minimal fitness map this can reverse selection with `Delta C_A=0`, isolating a purely fixed/frontier-side structural effect.

This mapping from finite sensing structure to a state-dependent evolutionary selection coefficient is the proposed modeling contribution.

---

## 6. Cross-scale result that is specific to the combined construction

The temporal-routing branch and evolutionary-timescale branch use temporal predictability differently.

In the symmetric within-individual routing model,

\[
G_{route}\propto|\phi|.
\]

Both persistence (`phi>0`) and predictable alternation (`phi<0`) can make the next useful cue predictable.

By contrast, long-term directional evolutionary retention depends on **signed** coherence of the selection sequence. Perfect alternation can therefore maximize within-individual predictability while cancelling long-horizon evolutionary displacement exactly over even windows.

The combined statement is

\[
\boxed{
\text{predictability useful for individual contingent behavior}
\ne
\text{temporal coherence required for directional evolutionary accumulation}.
}
\]

Neither the existence of fluctuating selection nor the population-genetic cancellation identity is claimed as new. The possible novelty is the explicit structural route from community-dependent cue obligations to the sign and magnitude of that selection.

---

## 7. What still must be shown before a strong biological claim

The branch remains theoretical until at least one natural system supplies evidence for the full chain

```text
community state
-> feasible cue graph / productive obligations
-> different contingent-vs-fixed structural gap
-> measurable fitness difference among sensory architectures
-> altered interaction edges
-> feedback to community state
-> temporally varying selection.
```

Without those links, the repository supports a structural possibility theorem and evolutionary hypothesis, not a demonstrated natural eco-evolutionary mechanism.
