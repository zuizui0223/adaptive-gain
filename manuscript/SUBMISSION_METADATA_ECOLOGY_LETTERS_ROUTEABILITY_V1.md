# Ecology Letters routeability submission metadata v1

Date: 2026-10-02  
Status: text-ready; figures and final submission packaging pending.

## Target

**Journal:** Ecology Letters  
**Article type:** Letter

Verified journal limits at preparation:
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

- abstract: **142 words**
- main text: **approximately 4,915 words**
- references: **22**
- main figures: **2**
- main tables: **0**
- text boxes: **0**

Canonical manuscript:

`manuscript/MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_4_INFORMATION_ACCESS.md`

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
information-acquisition costs; public *Bombus* data independently support the
costly, need-dependent and sequential acquisition mechanisms required for this
distinction to matter biologically.

## Headline theorem

For deterministic exact resolution,

[
C_F=
min_{S:I(T;Q_S)=H(T)} c(S).
]

The 12-state matched twins have the same complete Shannon entropy vector but

[
(C_A,C_F)_A=(4,4),
qquad
(C_A,C_F)_B=(3,4).
]

Their (r)-fold products preserve complete entropic equivalence and give

[
(4r,4r)
qquad	ext{versus}qquad
(3r,4r),
]

so the adaptive-cost difference is unbounded additively.

A separate exactly-balanced family gives an unbounded multiplicative
(C_F/C_A) separation under weaker information matching.

## Public Bombus empirical convergence

Canonical receipt:

`validation/bombus_empirical_convergence_panel_v1.json`

### Yuan et al. 2026

Public source:
`Cuixiaojian21/bee_metacognition`,
commit `7f886394b4de872ecdb19ca4ea214ec321d5dce9`,
raw blob `26259c9071c6d73141d56b9bedd396cab1a04491`.

Independent reaggregation:
- 19,200 trials;
- 192 bees;
- Regular information-request/landing rates:
  0.096, 0.469, 0.716 for Easy, Hard, Impossible;
- Random Free-Cue landing rates:
  0.617, 0.588, 0.210;
- within-bee Impossible-versus-Easy difficulty × access-mode interaction:
  mean (1.018), positive for 191/192 bees,
  exact one-sided sign-test (p=3.1	imes10^{-56}).

Interpretation:
difficulty drives platform landing specifically when landing is required to
obtain information.

### Spaethe et al. 2026

Public analysis repository:
`stoeckl-lab/Spaethe_et_al_2024_beeDecisions`.

Prospectively defined secondary-cue recruitment:

[
R_{m easy}=0.026,
qquad
R_{m hard}=0.374,
]

difference (0.349), pooled Cliff's (delta=0.980).

Interpretation:
secondary cues are recruited when primary information is insufficient.

### Additional public/mechanistic support

- MaBouDi et al. 2025: selective sequential visual sampling;
- Chow et al. 2022: early context switches the later correct action;
- Essenberg et al. 2015: closest branch-specific cue-relevance precedent.

Claim ceiling:
these studies provide **componentwise public validation**, not one direct
estimate of the exact deterministic (C_A<C_F) theorem.

## Main figures

### Figure 1

**Entropic equivalence does not imply adaptive equivalence**

Panels:
- common 12-state/four-cue environment and two target maps;
- all 32 Shannon entropies exactly matched;
- (C_F=4) in both, (C_A=4) versus 3;
- direct-product amplification.

### Figure 2

**When information accessibility becomes ecological**

Panels:
- ecological budget window (C_Ale B<C_F);
- public *Bombus* convergence:
  Yuan access-mode interaction and Spaethe secondary-cue recruitment;
- prospective matched four-state causal test;
- measurement pipeline.

Canonical plan:

`manuscript/RELATIONAL_ROUTEABILITY_FIGURE_PLAN_V1.md`

## Supplement

Formal proof and finite verification material:

`manuscript/SUPPLEMENT_RELATIONAL_ROUTEABILITY_PROOFS_V1.md`

Mathematical-companion extremal material should remain supplementary or
separate; do not load the Letter with star--edge--star and (D_h(n)) tables.

## Data accessibility statement — draft content

The mathematical constructions, exact verification code and analysis tests are
maintained in the `adaptive-gain` repository. The empirical-convergence
analyses use previously public data from the cited repositories/DOIs, including
the Yuan et al. trial-level repository and the Spaethe et al. public analysis
repository. Before submission, archive the exact submitted code state in a
permanent repository and insert its DOI here.

Do not claim ownership of the external public datasets.

## Novelty firewall

Do not claim novelty for:
- all-subset entropy profiles;
- entropy-vector insufficiency as a generic information-theory phenomenon;
- adaptive feature acquisition;
- conditional mutual information;
- PID/synergy;
- sequential value of information;
- generic adaptive-versus-fixed decision trees.

The manuscript-specific contribution is:

> complete Shannon entropic equivalence can coexist with different optimal
> adaptive worst-case ecological resolution costs on one physical cue
> environment, with unbounded additive amplification and a finite-budget
> ecological consequence.

## Author-controlled title-page fields — unresolved

Verify deliberately before upload:
- author list and order;
- publication spelling of names;
- affiliations;
- corresponding author;
- correspondence address/e-mail;
- ORCIDs;
- funding statement;
- competing interests;
- author contributions.

## Remaining submission work

1. render and verify the two main figures;
2. final reference and citation audit;
3. archive the exact code/data-analysis state and insert DOI;
4. prepare cover letter and novelty statement;
5. final PDF/math-symbol inspection;
6. record submitted commit/tree.

## Stop rule

No further deterministic theorem hunting or broad public-data search is needed
for the initial Ecology Letters submission.
