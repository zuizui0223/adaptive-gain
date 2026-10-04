# Relational routeability figure plan v2 — information accessibility

Status: canonical two-figure architecture for
\`MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_4_INFORMATION_ACCESS.md\`.

Design rule: the main paper is not a catalogue of balanced-query extremal
results. It is one ecological information claim:

> **the information present in an environment does not determine how cheaply
> that information can be accessed after realized observations.**

Keep the main paper to two figures.

---

## Figure 1 — Entropic equivalence does not imply adaptive equivalence

### Purpose

Make the strongest theorem visible before any asymptotic construction.

A reader should be able to see in one page that:

\[
\text{same physical cues}
+
\text{same complete Shannon entropy vector}
\not\Rightarrow
\text{same adaptive accessibility}.
\]

### Panel A — one physical cue environment

Show the 12 represented states as rows and the four binary cues as columns.

Use the **same cue matrix only once**, not duplicated artwork.

Annotate:

- 12 states;
- 4 binary unit-cost cues;
- every cue exactly 6:6 balanced;
- physical cue matrix held fixed.

Then place two target/action columns beside the matrix:

- Twin A target map;
- Twin B target map.

Target prevalence is 8:4 in both.

The visual point is that only the action map changes.

### Panel B — temporal routing plus cross-system scope

Use the upper-right half to connect the static theorem to a dynamic decision
prediction without making any taxon the subject of the paper.

#### B1 — temporal predictive routing

Plot

[
G_{m time}=rac{|2ho-1|}{4}
]

against (hoin[0,1]). Show the V-shaped values:

- (ho=0): gain (=0.25), predictable alternation;
- (ho=0.5): gain (=0), temporal independence;
- (ho=1): gain (=0.25), predictable persistence.

Main annotation:

**present context matters when it predicts which later cue will be useful**

Do not describe positive persistence as uniquely favorable; predictable
alternation has the same gain with the opposite continuation rule.

#### B2 — one quantified biological example: Spaethe et al. 2026

Plot the peer-reviewed secondary-cue recruitment index

[
R=1-p_{m colour}.
]

Show

[
R_{m easy}=0.026,
qquad
R_{m hard}=0.374,
]

with pooled Cliff's (delta=0.980).

Main annotation:

**primary cue sufficient -> secondary cue mostly ignored**

**primary cue difficult -> secondary cue recruited**

This is one flexible-generalist example, not a direct routeability estimate.

#### B3 — parallel staged ecological decisions

Use three small schematic boxes:

- parasitoid host finding: host habitat -> host assessment;
- fiddler-crab predator assessment: information changes across escape stages;
- patch foraging: repeated stay/leave decisions.

These establish scope across ecological interactions and taxa. They do not
estimate (C_A) or (C_F).

Yuan et al. (2026) is **not** part of the main figure. Its public reaggregation
is retained only as a Supplementary provisional costly-information component
because the study is a preprint and one raw accuracy field remains unresolved.

### Panel C — realized outcomes create different continuation problems

Draw only the first informative split needed to expose the difference.

Twin A:
- every branch retains enough unresolved obligations that worst-case adaptive
  depth remains 4.

Twin B:
- after one realized outcome, different later cues become relevant on
  different branches;
- an optimal tree has depth 3.

Display:

\[
(C_A,C_F)_A=(4,4),
\qquad
(C_A,C_F)_B=(3,4).
\]

Main annotation:

**same static information; different conditional accessibility**

This is the conceptual center of the paper.

### Panel D — the difference is not a finite curiosity

Use the \(r\)-fold direct-product theorem as a one-line scaling panel:

\[
A^{\otimes r}:(C_A,C_F)=(4r,4r),
\]

\[
B^{\otimes r}:(C_A,C_F)=(3r,4r).
\]

Plot only the two adaptive costs against \(r\); the fixed costs coincide.

Label:

\[
\Delta C_A=r\to\infty.
\]

Subtitle:

**complete Shannon entropic equivalence is preserved**

Do not imply an unbounded multiplicative ratio here.

### Figure 1 message

\[
\boxed{
\text{static Shannon information}
\neq
\text{sequential information accessibility}.
}
\]

---

## Figure 2 — When information accessibility becomes ecological

### Purpose

Translate the theorem into an ecological measurement and causal prediction
without pretending that current public data directly validate routeability.

### Panel A — finite ecological budget

Horizontal axis: observation/acquisition budget \(B\).

For a routeable task mark:

1. \(B<C_A\): neither access mode guarantees resolution;
2. \(C_A\le B<C_F\): contingent access changes feasibility;
3. \(B\ge C_F\): fixed and contingent access are both sufficient.

Headline:

\[
\boxed{C_A\le B<C_F}
\]

is the topology-sensitive ecological window.

Examples beneath the axis:
- host departure time;
- floral handling opportunity;
- predator exposure;
- energetic or reward cost of additional sampling.

Yuan et al. (2026) can be cited in the legend as empirical precedent that
bumble bees can voluntarily pay a reward cost to obtain information. It is
**not** plotted as routeability validation.

### Panel B — one quantified biological example: *Bombus*

Use two quantitative mini-panels and one qualitative icon row.

#### B1 — costly information acquisition depends on access mode (Yuan et al. 2026)

Plot **platform-landing probability** against difficulty as two connected
series from the independently reaggregated 19,200 public trials:

| Difficulty | Regular: landing obtains cue | Random Free-Cue: cue supplied independently |
|---|---:|---:|
| Easy | 0.096 | 0.617 |
| Hard | 0.469 | 0.588 |
| Impossible | 0.716 | 0.210 |

The two gradients cross.

Add the individual-level interaction certificate:

\[
\Delta\Delta_{\rm Impossible-Easy}=1.018,
\]

positive in **191/192 bees**,
exact one-sided sign-test \(p=3.1\times10^{-56}\).

Main annotation:

**difficulty increases landing only when landing is needed to obtain information**

A small inset may show that unaided accuracy falls
\(0.750\to0.494\to0.207\), whereas post-acquisition accuracy remains near
\(0.93\).

Do not label Free-Cue platform landing as an information request: the cue is
already delivered independently in that condition.

#### B2 — recruitment of a second cue (Spaethe et al. 2026)

Plot the prospectively defined secondary-cue recruitment index

\[
R=1-p_{\rm colour}.
\]

Show only the pooled public result:

\[
R_{\rm easy}=0.026,
\qquad
R_{\rm hard}=0.374.
\]

Add a thin indication that pattern and shape experiments independently share
the same direction.

Main annotation:

**primary cue sufficient → secondary cue mostly ignored**

**primary cue difficult → secondary cue recruited**

#### B3 — sequential access exists

Use a small schematic/citation rather than another numerical axis:

- MaBouDi et al. 2025: selective high-speed visual scanning of restricted
  pattern regions;
- Essenberg et al. 2015: flower type determines whether size is a useful reward
  cue.

Caption firewall:

> These data illustrate operational ingredients relevant to conditional cue routing; they do not validate or estimate the exact matched \(C_A<C_F\) theorem.

Do not combine effect sizes across studies.

### Panel C — prospective causal test

Show the registered minimal experiment:

- four states;
- three cues;
- matched physical cue environment;
- routeable versus matched-control action map;
- budget ladder \(B=1,2,3\).

Primary qualitative interaction:

\[
\Delta_{B=1}=0,
\qquad
\Delta_{B=2}>0,
\qquad
\Delta_{B=3}=0.
\]

The middle-budget effect is the discriminating prediction.

Beside it, optionally show the ten-state exact-balanced stress test:

\[
(C_A,C_F)_R=(3,4),
\qquad
(C_A,C_F)_K=(2,2),
\]

with every cue exactly 5:5 balanced.

At \(B=3\), the deterministic ceiling interaction is \(1/5\).

Label clearly:

**task ceiling, not assumed behavioral effect size**

### Panel D — measurement rule

Use a small pipeline:

\[
\text{focal action}
\to
\text{represented alternatives}
\to
\text{cue outcomes}
\to
\text{cue costs}
\to
(C_A,C_F)
\to
B.
\]

Add the rule:

> **measure the action-conditioned cue table first; summarize it second.**

This panel turns the theory into an empirical protocol.

### Figure 2 message

The theory predicts an ecological effect only when organisms face finite
information-acquisition constraints and can condition later acquisition on
earlier outcomes.

---

## Supplementary Figure S1 — Strong matching ladder

Display the successive matching levels:

\[
\text{state/cue counts}
\to
\text{cue marginals}
\to
\text{cue-only joint distribution}
\to
H(T)
\to
I(T;Q_{\rm all})
\to
\text{pairwise target-cue profiles}
\to
\{I(T;Q_S)\}_{S\subseteq Q}
\to
\text{complete Shannon entropy vector}
\to
\text{complete action-conditioned table}.
\]

Mark explicit counterexamples through the complete Shannon entropy-vector
level.

Only the complete action-conditioned table with cue costs specifies the
deterministic adaptive problem.

Important caption boundary:

- an all-subset entropy profile is not a novel object;
- PID can retain distributional structure not captured by an entropy vector;
- the theorem concerns insufficiency of the complete Shannon entropy vector for
  exact adaptive accessibility.

---

## Supplementary Figure S2 — Exact-balanced asymptotic counterpoint

Keep the older routing family out of Figure 1 so the two theorem strengths are
not confused.

Show:

\[
C_F\ge2^d,
\qquad
C_A\le d+1,
\]

with every query exactly 50/50 balanced.

Matched control:

\[
C_A=C_F=2.
\]

Caption boundary:

- this gives an unbounded **multiplicative** adaptive/fixed ratio;
- it matches weaker information summaries than the entropic-twin theorem;
- the entropic-twin direct product gives the stronger information matching but
  only an unbounded **additive** separation currently.

---

## Omit from main figures

Do not include:

- star--edge--star extremal geometry;
- \(D_3,D_4,D_5\) finite envelope tables;
- diversity--stability speculation;
- community-resilience claims;
- stochastic expected-loss extensions;
- additional quantitative taxon panels added only to make the theory look general.

Those belong in the mathematical supplement, future work or a separate
empirical paper.

## Stop rule

No third main figure before submission.

A third figure is justified only by a concrete editorial/reviewer need or by a
new direct biological routeability dataset that passes the preregistered
eligibility gate.
