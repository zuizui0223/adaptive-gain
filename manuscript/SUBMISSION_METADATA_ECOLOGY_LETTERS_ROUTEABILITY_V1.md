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

**Conditional decision topology separates information content from ecological accessibility**

## Running title

**Conditional decision topology**

(<45 characters including spaces.)

## Counts

Using the same repository counter as the submission-surface test:

- abstract: **146 words**
- main text: **4,630 words**
- references: **26**
- main figures: **2**
- main tables: **0**
- text boxes: **0**

Canonical manuscript:

\`manuscript/MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_4_INFORMATION_ACCESS.md\`

## Keywords

1. environmental heterogeneity
2. ecological information
3. sequential decision making
4. adaptive feature acquisition
5. niche breadth
6. routeability
7. information processing
8. cue acquisition

## One-sentence contribution

Two ecological decision tasks can share one physical cue environment and the
same complete Shannon entropy vector yet have different optimal adaptive
information-acquisition costs; a finite ecological budget exposes that
difference, a nonlinear no-go links insufficient routeability contrast to
unreachable local eco-evolutionary regimes, and public *Bombus* data support
the required biological operations.

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

### Nonlinear evolutionary no-go

Let

\[
g_i=C_F(i)-C_A(i),
\qquad
\Delta g=g_2-g_1\ge0.
\]

For a nondecreasing \(L\)-Lipschitz sensing-to-selection lift, define the
selection-to-feedback scale

\[
B_f=-\beta e>0.
\]

Then

\[
G\le B_fL\Delta g.
\]

The local complex-eigenpair threshold is

\[
G_{\rm osc}
=
\frac{(\alpha-\phi)^2}{4(1-\phi)}.
\]

Therefore a stable oscillatory response is possible only if

\[
\Delta g>
\frac{G_{\rm osc}}{B_fL}.
\]

This is a necessary-condition/no-go result, not a sufficiency theorem.

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

## Public *Bombus* empirical convergence

Canonical receipts:

- \`validation/bombus_public_data_component_receipt_v1.json\`
- \`validation/bombus_empirical_convergence_panel_v1.json\`

### Yuan et al. 2026 — provisional preprint component

Public source:
\`Cuixiaojian21/bee_metacognition\`,
commit \`7f886394b4de872ecdb19ca4ea214ec321d5dce9\`,
raw blob \`26259c9071c6d73141d56b9bedd396cab1a04491\`.

Independent reaggregation:
- 19,200 trials;
- 192 bees;
- Regular information-request rates:
  0.096, 0.469, 0.716 for Easy, Hard and Impossible;
- all 192 bees show Hard > Easy request rates;
- 181/192 show Impossible > Hard;
- post-request accuracy remains approximately 0.93.

Random Free-Cue trials separate information receipt from the acquisition action.
The raw non-request accuracy coded for the Impossible subset is not used as
biological evidence because its below-chance value is not reconciled with the
identical-stimulus task description.

### Spaethe et al. 2026

Public analysis repository:
\`stoeckl-lab/Spaethe_et_al_2024_beeDecisions\`.

Prospectively defined secondary-cue recruitment:

\[
R_{\rm easy}=0.026,
\qquad
R_{\rm hard}=0.374,
\]

difference 0.349; pooled Cliff's \(\delta=0.980\).

### Additional public/mechanistic support

- MaBouDi et al. 2025: selective sequential visual sampling;
- Chow et al. 2022: early context switches the later correct action;
- Essenberg et al. 2015: closest branch-specific cue-relevance precedent.

Claim ceiling:
these studies provide **componentwise public validation**, not one direct
estimate of the exact deterministic \(C_A<C_F\) theorem.

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
- public *Bombus* convergence;
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
- nonlinear no-go proof;
- exact-balanced stress tests;
- prospective direct experiment designs;
- temporal recurrence/spectral filtering as supporting theory;
- identifiability limits;
- exact-balanced extremal geometry from the mathematical companion.

The mathematical companion is therefore a supplementary proof reservoir for
the initial submission, not a separate simultaneous manuscript.

## Portfolio rule

**Do not submit frozen V5 separately.**

V5 is retained only as provenance/revision reserve because its routeability,
budget-window and nonlinear no-go content is now incorporated into the
integrated manuscript. A separate V5 submission would create substantial
theorem/claim overlap.

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
> environment; this difference can be amplified additively, becomes
> ecologically consequential under finite acquisition budgets, and can bound
> evolutionary reachability under a specified nonlinear lift.

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

1. final repository-wide CI;
2. final rendered figure/PDF inspection;
3. final citation/reference audit;
4. archive exact code/data-analysis state and insert DOI;
5. fill author-controlled title-page fields;
6. record submitted commit/tree.

## Stop rule

No further deterministic theorem hunting or broad public-data search is needed
for the initial Ecology Letters submission.
