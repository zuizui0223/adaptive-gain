# Ecology Letters routeability submission metadata v2

Date: 2026-10-02  
Status: integrated text and figures ready; author metadata, permanent archive DOI and final rendered preflight remain.

## Target

**Journal:** Ecology Letters  
**Article type:** Letter

Current journal limits verified on 2026-10-02:
- abstract: maximum 150 words;
- main text: maximum 5,000 words, excluding abstract, acknowledgements,
  references and figure/table/box legends;
- maximum 6 figures, tables or text boxes combined.

## Title

**Conditional decision topology separates ecological diversity from decision complexity**

## Running title

**Conditional decision topology**

(<45 characters including spaces.)

## Counts

Using the same repository counter as the submission-surface test:

- abstract: **150 words**
- main text: **4,428 words**
- references: **29**
- main figures: **2**
- main tables: **0**
- text boxes: **0**

Canonical manuscript:

\`manuscript/MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_4_INFORMATION_ACCESS.md\`

## Keywords

1. behavioural ecology
2. decision ecology
3. generalism
4. sequential decision making
5. information processing
6. foraging
7. cue acquisition
8. routeability

## One-sentence contribution

Ecological diversity does not determine decision complexity: two tasks can
share one physical cue environment and the same complete Shannon entropy vector
yet have different optimal adaptive resolution costs, and a finite observation
budget exposes that difference behaviorally.

## Main theorem spine

### Static fixed resolution

For deterministic exact resolution under any full-support prior,

\[
C_F=
\min_{S:I(T;Q_S)=H(T)} c(S).
\]

### Complete entropic equivalence does not identify adaptive accessibility

The matched 12-state twins have the same physical cue matrix and the same
complete Shannon entropy vector but

\[
(C_A,C_F)_A=(4,4),
\qquad
(C_A,C_F)_B=(3,4).
\]

Their \(r\)-fold products preserve complete entropic equivalence and give

\[
(4r,4r)
\qquad\text{versus}\qquad
(3r,4r),
\]

so the adaptive-cost difference is unbounded additively as the composite action
alphabet grows.

A separate exactly-balanced family gives an unbounded multiplicative
\(C_F/C_A\) separation under weaker information matching.

### Ecological budget

Conditional accessibility changes guaranteed feasibility in the intermediate
window

\[
C_A\le B<C_F.
\]

### Temporal predictive routing

For the minimal two-step routing model with

\[
P(C_1=C_0)=\rho,
\]

the best fixed two-query policy has

\[
A_F^{(2)}=\frac34,
\]

while the best contingent policy has

\[
A_A^{(2)}=
\frac34+\frac{|2\rho-1|}{4}.
\]

Hence

\[
G_{\rm time}=\frac{|2\rho-1|}{4},
\]

with zero routing value exactly at temporal independence. Under symmetric cue
noise,

\[
G_{\rm noisy}
=
\frac{|2\rho-1|(2a-1)(2b-1)}{4}.
\]

Canonical assets:
- \`adaptive_gain/temporal_routing.py\`;
- \`adaptive_gain/noisy_temporal_routing.py\`;
- \`tests/test_temporal_routing.py\`;
- \`tests/test_noisy_temporal_routing.py\`;
- \`validation/temporal_routing_threshold_v1.json\`;
- \`validation/noisy_temporal_routing_factorization_v1.json\`.

## Independent theorem verification

The strongest Section-5 claim is verified twice:

1. by the canonical finite-task/information implementation; and
2. by an independent audit that does not import the repository's main solver,
   information helpers or static-information witness.

Independent assets:

- \`adaptive_gain/independent_section5_audit.py\`
- \`tests/test_independent_section5_audit.py\`
- \`validation/independent_section5_audit_v1.json\`

The independent implementation reproduces:

- one-copy complete entropy-vector equality,
  \(C_F=(4,4)\), \(C_A=(4,3)\);
- two-copy 144-world equality,
  \(C_F=(8,8)\), \(C_A=(8,6)\).

## Cross-system biological examples

Canonical receipts:

- \`validation/bombus_public_data_component_receipt_v1.json\`
- \`validation/bombus_empirical_convergence_panel_v1.json\`

### Supplementary provisional costly-information component

Yuan et al. (2026) is retained only in the Supplement. Its public reaggregation
is not plotted in the main figure and is not used as direct evidence for the
routeability theorem. Provenance remains frozen in
`validation/bombus_public_data_component_receipt_v1.json` and
`validation/yuan_free_cue_acquisition_interaction_v1.json`.

### Bumblebee conditional cue recruitment

Public analysis repository:
\`stoeckl-lab/Spaethe_et_al_2024_beeDecisions\`.

Prospectively defined secondary-cue recruitment:

\[
R_{\rm easy}=0.026,
\qquad
R_{\rm hard}=0.374,
\]

difference 0.349; pooled Cliff's \(\delta=0.980\).

### Other staged decision systems and mechanisms

- MaBouDi et al. 2025 and Essenberg et al. 2015: sequential sampling and conditional cue relevance in bumblebees;
- Quilici & Rousse 2012: staged parasitoid host finding;
- Hemmi & Pfeil 2010: multi-stage predator-risk information;
- Stephens 2008: hierarchical and repeated patch-foraging decisions.

Claim ceiling:
these studies document biological operations relevant to conditional decision structure; they are not direct validation or estimation of the exact deterministic \(C_A<C_F\) theorem.

## Main figures

### Figure 1

**Entropic equivalence does not imply adaptive equivalence**

Panels:
- common 12-state/four-cue environment and two target maps;
- all 32 Shannon entropies exactly matched;
- \(C_F=4\) in both, \(C_A=4\) versus 3;
- direct-product additive amplification.

### Figure 2

**When information accessibility becomes ecological**

Panels:
- ecological budget window \(C_A\le B<C_F\);
- temporal predictive routing, one peer-reviewed *Bombus* quantitative example, and cross-system staged-decision scope;
- prospective matched causal test;
- measurement pipeline.

Canonical plan:

\`manuscript/RELATIONAL_ROUTEABILITY_FIGURE_PLAN_V1.md\`

## Supplement

Canonical integrated supplement:

\`manuscript/SUPPLEMENT_RELATIONAL_ROUTEABILITY_PROOFS_V1.md\`

It contains:
- formal relational proofs;
- static-information theorem and complete-entropy matched twins;
- outcome-resolved Bellman recursion;
- nonlinear eco-evolutionary no-go retained as additional mathematical theory, not a main-text result;
- temporal and noisy routing derivations;
- exact-balanced stress tests;
- prospective direct experiment designs;
- temporal recurrence/spectral filtering as supporting theory;
- identifiability limits;
- exact-balanced extremal geometry from the mathematical companion.

The mathematical companion is therefore a supplementary proof reservoir for
the initial submission, not a separate simultaneous manuscript.

## Portfolio rule

**Do not submit frozen V5 separately.**

V5 is retained only as provenance/revision reserve. Its routeability and
budget-window content is incorporated into the main manuscript, while its
nonlinear no-go is retained in the integrated Supplement. A separate V5
submission would therefore create substantial theorem/claim overlap.

Villavicencio rewiring remains a separate project because its
sampling/detection-effort issue is unresolved and should not be imported into
this manuscript.

## Data accessibility

Canonical draft:

\`manuscript/DATA_ACCESSIBILITY_ECOLOGY_LETTERS_ROUTEABILITY_V1.md\`

Before submission:
1. archive the exact submitted repository state in a permanent repository;
2. insert the permanent DOI;
3. record the submitted Git commit SHA.

Do not claim ownership of external public datasets.

## Novelty firewall

Do not claim novelty for:
- decision trees or separating systems;
- all-subset entropy profiles;
- entropy-vector insufficiency as a generic information-theory phenomenon;
- adaptive feature acquisition;
- conditional mutual information;
- PID/synergy;
- sequential value of information;
- generic adaptive-versus-fixed search.

The manuscript-specific contribution is:

> complete Shannon entropic equivalence can coexist with different optimal
> adaptive worst-case ecological resolution costs on one physical cue
> environment; finite budgets make that difference behaviorally consequential,
> and temporal predictability can give a target-uninformative cue value by
> identifying which later cue should be sampled.

## Author-controlled title-page fields — unresolved

Verify deliberately before upload:
- author list and order;
- publication spelling of names;
- affiliations;
- corresponding author;
- complete correspondence address/e-mail/telephone;
- ORCIDs;
- funding statement;
- competing interests;
- author contributions.

## Remaining submission work

Completed:
- manuscript citation/reference audit: 29 main-text references, all cited; Yuan et al. 2026 is Supplementary-only with a local full citation;
- abstract/main-text/reference count synchronization;
- independent verification of complete-Shannon and temporal-routing results.

Still required:
1. final repository-wide CI for the final content head;
2. final rendered figure/PDF inspection;
3. archive the exact code/data-analysis state and insert the permanent DOI;
4. fill author-controlled title-page fields;
5. record the submitted commit/tree.

## Stop rule

No further deterministic theorem hunting or broad public-data search is needed
for the initial Ecology Letters submission.
