# Relational routeability prior-art audit v1

Status: post-freeze literature boundary for the math–ecology synthesis.

## Question

Which parts of the current synthesis are established in neighboring fields, and what remains specific to the ecological routeability program?

The current exact result constructs two target/action maps on the same physical cue environment such that:
- the full cue matrix is identical;
- target prevalence and entropy are identical;
- total full-vocabulary target information is identical;
- yet adaptive versus fixed acquisition costs differ sharply, with an unbounded asymptotic separation.

The audit asks whether this should be described as:
- new adaptive information acquisition;
- new value-of-information theory;
- new entropy insufficiency;
- or a narrower ecological composition.

---

## 1. Adaptive feature acquisition is prior art

Machine-learning and decision-theory literatures already treat costly feature acquisition as a sequential/adaptive problem.

Examples include:
- Contardo, Denoyer & Artières (2016), adaptive feature acquisition with feature-specific acquisition costs;
- Nan et al. (2017), adaptive classification under a prediction/feature budget;
- later active-feature-acquisition work treating which feature to acquire next as a sequential decision.

Therefore the current program must not claim novelty for:
- acquiring cues sequentially;
- conditioning later observations on earlier values;
- prediction under a feature budget;
- adaptive acquisition reducing average prediction cost.

The ecological contribution is not "animals can benefit from adaptive feature acquisition."

---

## 2. Sequential value of information is prior art

Decision analysis and modern sequential-information-acquisition models already study:
- the value of obtaining information before action;
- costs of information acquisition;
- sequential signal acquisition;
- dynamic stopping or policy choice.

Therefore the current theory must not claim novelty for:
- information having value only relative to a decision;
- information acquisition costs;
- dynamic or sequential information collection.

---

## 3. Entropy is not a complete structural invariant — prior mathematical analogues exist

A particularly close conceptual analogue comes from information theory.

Sun & Jafar (2019), in nonlinear computation broadcast, give instances with the **same entropic structure** — the same entropy for all subsets of the relevant variables — but different capacities. They describe this as the importance of **extra-entropic structure**.

This is not the same problem:
- their object is communication/computation capacity;
- the present object is finite target-resolution acquisition cost;
- their setup is not ecological and does not use the routeability budget window.

But it establishes an important prior-art boundary:

> one must not claim that the present work is the first demonstration that entropy or even a complete entropy vector can fail to determine an operational quantity.

The safe distinction is narrower:

> the current theory identifies an action-conditioned acquisition topology in ecological decision problems, gives exact fixed/adaptive cost consequences, and connects that topology to a biological observation budget.

---

## 4. What remains specific in the current synthesis

The targeted audit has not located an exact predecessor combining all of the following:

1. one fixed finite physical cue environment;
2. two focal action maps on that same environment;
3. matched target prevalence and entropy;
4. matched cue-only distribution;
5. matched total full-vocabulary target information;
6. sharply different adaptive versus fixed exact-resolution cost;
7. an exact common ecological budget \(B\) for which one task lies in
   \[
   C_A\le B<C_F
   \]
   and the matched control does not;
8. an ecological interpretation in terms of resource/host/partner decisions.

The novelty claim should therefore concern the **composition** and the **ecological object**, not the generic component mathematics.

---

## 5. Strongest safe theorem positioning

Use wording close to:

> We formalize a relational property of ecological cue environments: two tasks can share the same physical cue matrix, target prevalence, target entropy and total available target information, yet differ sharply in the cost of resolving the focal action because earlier cue outcomes change which later distinctions remain relevant.

Then:

> Under a shared hard observation budget, this structural difference produces an exact architecture-by-access contrast.

Avoid:

- entropy cannot describe structure;
- mutual information is insufficient in general;
- first theory beyond Shannon information;
- first adaptive information-acquisition theory;
- first value-of-information model with sequence dependence.

---

## 6. Relation to adaptive feature acquisition

The closest operational comparison is adaptive feature acquisition.

That literature typically asks:

> given a predictive task and feature costs, what acquisition policy minimizes expected prediction loss plus cost or respects a budget?

The current deterministic theorem asks a different extremal question:

> holding the physical feature/cue environment fixed, how far can fixed and contingent **guaranteed-resolution** costs diverge solely because the focal action map changes?

This difference matters:
- the current theorem is exact and worst-case;
- the divergence is between two target maps on the same cue environment;
- the ecological interpretation is explicitly task-relative.

The expected-loss extension would move the program closer to adaptive-feature-acquisition theory and must then engage that literature much more deeply.

---

## 7. Implication for the next expected-loss paper

The stochastic extension cannot be positioned as simply "adding noisy cues."

It should explicitly compare against:
- adaptive feature acquisition;
- value-of-information / optimal stopping;
- active feature-value acquisition;
- cost-sensitive classification.

The potentially new question is narrower:

> whether the **quantity/topology separation under matched physical cue distributions and target-information summaries** persists for optimal expected-loss policies.

That is the appropriate novelty target for the next theory paper.

---

## 8. V5 claim boundary

V5 can safely use the deterministic result to establish:

- routeability is relational rather than intrinsic to a habitat/community;
- distributional information summaries do not determine exact acquisition cost;
- a finite ecological budget exposes the difference.

V5 should not make broad priority claims against information theory or machine learning.

## References

- Contardo, G., Denoyer, L. & Artières, T. 2016. Recurrent Neural Networks for Adaptive Feature Acquisition. ICONIP 2016. DOI: 10.1007/978-3-319-46675-0_65.
- Nan, F. et al. 2017. Adaptive Classification for Prediction Under a Budget. NeurIPS 2017.
- Sun, H. & Jafar, S. A. 2019. On the Capacity of Computation Broadcast. arXiv:1903.07597.
- Howard, R. A. 1966. Information Value Theory. IEEE Transactions on Systems Science and Cybernetics.

## Stop rule

Do not broaden the novelty claim.

The strongest defensible statement is the exact ecological composition:

\[
\boxed{
\text{same cue environment}
+
\text{different action-conditioned topology}
+
\text{same budget}
\Rightarrow
\text{different feasible access regime}.
}
\]
