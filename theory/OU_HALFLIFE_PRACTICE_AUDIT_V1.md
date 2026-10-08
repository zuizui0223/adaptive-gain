# Practice audit v1: OU half-life as a mechanistic adaptation speed

## Purpose

This is a **seed audit**, not a systematic review. Its job is to test whether the exact half-life identified-set result targets an actual and recurring inferential practice rather than one unusually strong paper.

Audit question:

> Is \(t_{1/2}=\log(2)/\alpha\) presented as a biologically interpretable rate/time of adaptation toward an optimum, rather than merely as a descriptive autocorrelation timescale conditional on the OU model?

The second-paper claim is potentially consequential only if this interpretation is widespread enough to matter and if the new congruence theorem changes what the data alone can support.

## Initial direct positives

### 1. Voje, Saito-Kato & Spanbauer (2024), Journal of Evolutionary Biology

**Evolution in fossil time series reconciles observations in micro- and macroevolution.**

- Defines \(\alpha\) as the rate of adaptation and half-life as \(\log(2)/\alpha\).
- For *Cyclostephanos andinus*, reports a best half-life estimate of about **12 years**.
- Interprets the fitted dynamics as rapid trait adaptation to a quickly and randomly moving optimum and states that deterministic tracking of the moving optimum dominates the dynamics.
- This is the highest-value direct witness because the model is exactly the evoTS OUBM likelihood for which the congruence theorem has been derived.

**Audit class:** direct target; exact theorem applies to the fitted trait-only OUBM class.

### 2. Hansen et al. tradition / adaptation-inertia framework

The adaptation-inertia literature routinely interprets \(\alpha\) as adaptation rate and \(t_{1/2}=\log(2)/\alpha\) as the expected time for a trait mean to move halfway toward a primary optimum. Recent framework papers retain this interpretation and extend it to multivariate predictors and changing adaptive landscapes.

**Audit class:** conceptual source of the practice; theorem relevance depends on what is observed and on latent/predictor assumptions.

### 3. Ingram & Mahler (2013), Methods in Ecology and Evolution — SURFACE

**SURFACE: detecting convergent evolution from comparative data by fitting Ornstein-Uhlenbeck models with stepwise AIC.**

- Presents \(\alpha\) as the rate of adaptive evolution toward optimum \(\theta\).
- Presents phylogenetic half-life \(\log(2)/\alpha\) as the expected time for a lineage to evolve halfway toward \(\theta\).

**Audit class:** broad phylogenetic-practice witness; current nonstationary time-series theorem does not automatically transfer to a tree likelihood.

### 4. Khabbazian et al. (2016), Methods in Ecology and Evolution

**Fast and accurate detection of evolutionary shifts in Ornstein-Uhlenbeck models.**

- Explicitly calls \(\alpha\) the rate of adaptation.
- Uses half-life \(\log(2)/\alpha\) as the time for the expected trait value to reach halfway to the optimum.

**Audit class:** broad-practice witness; needs a separate phylogenetic/tree congruence argument before being counted as invalidated.

### 5. Grabowski et al. (2017), Nature Communications

**Evidence of a chimpanzee-sized ancestor of humans but a gibbon-sized ancestor of apes.**

- States that a main goal of the OU analysis is to quantify the rate of adaptation by phylogenetic half-life.
- Interprets half-life as the average time required to evolve half the distance to a new optimum and as a metric of phylogenetic inertia / slowness of adaptation.

**Audit class:** high-visibility practice witness; not yet an exact theorem target because the likelihood geometry differs from evoTS OUBM.

### 6. Rein et al. (2019), Nature Communications

**Early anthropoid femora reveal divergent adaptive trajectories in catarrhine hind-limb evolution.**

- Uses Hansen half-time / phylogenetic half-life explicitly as a proxy for rate of adaptation.

**Audit class:** high-visibility practice witness; separate tree extension required.

### 7. Gearty et al. (2018), PNAS

**Energetic tradeoffs control the size distribution of aquatic mammals.**

- Uses \(\log(2)/\alpha\) as phylogenetic half-life, the time to evolve halfway toward an optimum.
- Uses combinations of optimum, half-life and stationary variance to discriminate biological scenarios.

**Audit class:** broad-practice witness; separate tree extension required.

### 8. Recent methodological/review literature (2022–2026)

Recent Systematic Biology and Evolution papers continue to recommend or interpret half-life as a biologically intuitive adaptation timescale. Examples include:

- Bayesian OU interpretation papers emphasizing half-life as the time to cover half the distance to the optimum;
- the 2023 Systematic Biology response to Cooper et al., which explicitly interprets shorter half-life as faster adaptation and longer half-life as stronger inertia;
- 2026 within-lineage adaptation-inertia work, which again defines \(\alpha\) as adaptation rate and half-life as expected time to traverse half the distance to a primary optimum.

**Audit class:** evidence that the interpretation is current, not historical.

## Important negative / cautionary precedent

The practice is **not uncriticized**. Some OU literature already warns that a fitted \(\alpha\) need not uniquely represent stabilizing selection or adaptation. For example, POUMM documentation explicitly notes a dual interpretation of \(\alpha\) as adaptation/selection versus phenotypic decorrelation, and cautions against treating a positive \(\alpha\) as evidence of stabilizing selection without additional evidence.

This means the second paper cannot claim to be the first warning that OU \(\alpha\) may be biologically overinterpreted.

The candidate advance must instead be sharper:

\[
\boxed{
\text{for the actual trait-only moving-optimum likelihood,}
\quad H_{\rm direct}\in[H_{\rm OU},\infty)
}
\]

under an explicitly characterized observationally congruent causal class, together with the exact hidden-noise assumption that collapses this set to the one-way interpretation.

## Current inference from the seed audit

The practice-level target **exists and is widespread enough to justify a systematic audit**. However, only the Voje/evoTS moving-optimum class is currently covered by the exact nonstationary theorem. The macroevolutionary/phylogenetic examples establish field relevance but cannot yet be counted as overturned results.

Therefore the correct next order is:

1. finish prior-art audit for the exact evoTS causal gauge;
2. reproduce the Voje fossil-series fit and attach exact congruent half-life witnesses;
3. build a preregistered/systematic literature ledger of mechanistic half-life claims;
4. only then decide whether a tree/phylogenetic extension is needed for field-level scope.

## Working impact gate

- **One evoTS example + exact theorem:** strong conceptual/methods paper.
- **Several independent time-series applications with the same affected inference:** plausible broad ecology/evolution methods or conceptual paper.
- **Systematic audit showing a widespread class of published adaptation-speed claims is assumption-supported rather than data-identified, plus an actionable replacement diagnostic:** reevaluate Nature Ecology & Evolution.
- **Do not invoke Nature proper** unless the result demonstrably crosses subfields (fossil time series + phylogenetic comparative inference + causal SDE practice) without relying on an unproved tree generalization.
