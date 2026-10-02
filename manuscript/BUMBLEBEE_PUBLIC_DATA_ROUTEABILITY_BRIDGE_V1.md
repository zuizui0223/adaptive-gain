# Bumblebee public-data routeability bridge v2

Date: 2026-10-02

Status: canonical empirical-bridge plan for the information-accessibility
manuscript.

## Decision

The previous statement

> no public dataset can directly test routeability

was too coarse.

The defensible conclusion is now:

\[
\boxed{
\text{no single public dataset validates the full relational theorem,}
}
\]

but

\[
\boxed{
\text{public Bombus data directly validate several operational components.}
}
\]

This is strong enough for one compact empirical-convergence subsection or
panel in the theory paper. It must be labelled **componentwise public
validation / empirical bridge**, not a measurement of the exact deterministic
quantity \(C_A<C_F\).

---

## 1. Full-theorem gate

A one-dataset validation of the current deterministic theorem would ideally
contain all of the following:

1. one common physical cue environment;
2. a focal target/action map;
3. an early observation with multiple realized outcomes;
4. different later cues becoming relevant after different early outcomes;
5. measurable acquisition costs or delays;
6. a contingent-access policy and a fixed/unconditional-access comparison;
7. one common finite budget;
8. trial- or trajectory-level public raw data.

The defining positive signature is

\[
q_0=a\Longrightarrow q_i \text{ useful next},
\qquad
q_0=b\Longrightarrow q_j \text{ useful next}.
\]

No located public Bombus dataset simultaneously satisfies all eight items.

The public-data strategy is therefore to test **nonredundant components** of the
theory rather than to relabel ordinary multicue effects as the whole theorem.

---

## 2. Yuan et al. 2026 — direct costly contingent information acquisition

Preprint:
**Uncertainty-Guided Decision-Making in Bumble Bees**,
bioRxiv DOI 10.64898/2026.09.15.751944.

Species: *Bombus terrestris*.

Immutable public source used here:
- repository: \`Cuixiaojian21/bee_metacognition\`;
- source commit:
  \`7f886394b4de872ecdb19ca4ea214ec321d5dce9\`;
- raw file:
  \`data/4_active_information_seeking_trials.csv\`;
- raw blob:
  \`26259c9071c6d73141d56b9bedd396cab1a04491\`.

The file contains exactly 19,200 trials from 192 individually identified bees.

### Task

The task has two sequential zones.

In Regular trials, landing on the Zone-1 information-request platform provides
no immediate reward but triggers a brief predictive cue for the mandatory
Zone-2 discrimination.

Information is economically costly:

- correct without request: 30% sucrose;
- correct after request: 15% sucrose.

Thus platform landing is a voluntary information-acquisition action with an
explicit reward cost.

### Independent raw-data reaggregation

The full public CSV was fetched in four non-overlapping line ranges and
reaggregated independently of the paper's reported summaries and independently
of the existing repository receipt.

Regular trials:

| Difficulty | trials | requests | request rate | post-request accuracy | no-request accuracy |
|---|---:|---:|---:|---:|---:|
| Easy | 6,140 | 591 | 0.0963 | 0.9391 | 0.7502 |
| Hard | 6,108 | 2,866 | 0.4692 | 0.9288 | 0.4935 |
| Impossible | 3,112 | 2,229 | 0.7163 | 0.9300 | 0.2072 |

Relative to Easy trials, the raw request odds are approximately:

\[
OR_{\rm Hard/Easy}=8.30,
\]

\[
OR_{\rm Impossible/Easy}=23.70.
\]

The descriptive pattern is therefore unusually clean:

\[
\text{unaided accuracy}\downarrow
\quad\Longrightarrow\quad
\text{costly acquisition}\uparrow,
\]

while post-acquisition accuracy stays near \(0.93\).

### Random Free-Cue control

Twenty percent of trials provide the predictive cue automatically when the bee
enters Zone 1, independent of platform landing.

The raw data separate cue receipt from platform landing:

| Difficulty | free-cue trials | platform-landing rate | post-cue accuracy |
|---|---:|---:|---:|
| Easy | 1,540 | 0.6169 | 0.9487 |
| Hard | 1,572 | 0.5884 | 0.9434 |
| Impossible | 728 | 0.2102 | 0.9258 |

This control is important because it breaks the trained causal link

\[
\text{platform landing}\to\text{information}.
\]

The platform is therefore not merely a neutral response location. Its use
changes when information is supplied independently of the acquisition action.

### What Yuan validates

Directly supported:

- information can be actively acquired rather than passively received;
- acquisition has a real reward cost;
- acquisition probability changes strongly with the current informational
  state;
- acquisition restores high decision accuracy;
- an unconditional/free-information control changes the acquisition behaviour.

This is substantially closer to the theory's adaptive-versus-unconditional
access distinction than a simple cue-preference experiment.

### Claim ceiling

The task still offers only **one optional predictive information source**.
It does not ask the bee to choose between \(q_i\) and \(q_j\) after different
earlier outcomes.

Therefore Yuan is not a direct measurement of the deterministic
\(C_A<C_F\) theorem.

It is the strongest current public validation of the theory's
**costly contingent acquisition** component.

---

## 3. Spaethe et al. 2026 — direct secondary-cue recruitment

Paper:
**Bees flexibly adjust decision strategies to information content in a
foraging task**, *Science Advances*,
DOI 10.1126/sciadv.adw9320.

Species: *Bombus terrestris*.

Public assets:
- source-data share: Figshare \`c4c912de7dd7e24a9ec8\`;
- public analysis repository:
  \`stoeckl-lab/Spaethe_et_al_2024_beeDecisions\`;
- archived code: Zenodo DOI 10.5281/zenodo.15911965.

The public analysis code contains individual conflict-test values for colour
versus pattern/shape.

### Registered bridge statistic

Before reanalysing the embedded values, define

\[
R=1-p_{\rm colour}
\]

as the secondary-cue recruitment index.

The prospectively registered direction was

\[
\Delta_R
=
E[R\mid\text{hard primary colour}]
-
E[R\mid\text{easy primary colour}]
>0.
\]

### Reconstructed public result

From the authors' public individual values:

| Secondary cue | easy-colour \(R\) | hard-colour \(R\) |
|---|---:|---:|
| pattern | 0.0250 | 0.3800 |
| shape | 0.0267 | 0.3667 |
| pooled | 0.0257 | 0.3743 |

Thus

\[
\boxed{
\Delta_R^{\rm pooled}=0.3486
}
\]

or about **35 percentage points more secondary-cue recruitment** when the
primary colour cue is difficult.

Pattern and shape both show the same direction independently.

Executable receipt:
- \`adaptive_gain/bumblebee_public_bridge.py\`;
- \`tests/test_bumblebee_public_bridge.py\`.

The test is green in the repository CI.

### What Spaethe validates

Directly supported:

> the same nominal two-cue vocabulary does not imply the same information
> burden; bees largely ignore the secondary attribute when the primary cue is
> sufficient and recruit it when the primary cue becomes insufficient.

### Claim ceiling

The two attributes are simultaneously available, and the easy/hard treatment
changes physical colour discriminability.

This is **cue-set recruitment by information need**, not within-encounter
branch-specific next-cue acquisition.

---

## 4. MaBouDi et al. 2025 — direct selective sequential sensory sampling

Paper:
**Active vision of bees in a simple pattern discrimination task**,
*eLife* 14:e106332,
DOI 10.7554/eLife.106332.

Species: *Bombus terrestris*.

Public behavioural trajectories and analysis code:
Figshare DOI **10.15131/shef.data.14185865.v1**.

### Relevant result

High-speed trajectories show that bees do not need to process the full visual
pattern in parallel. They inspect restricted regions before accepting or
rejecting a stimulus.

The scanned region differs between the plus and multiplication patterns, and
the learned scanning strategy remains pattern-specific when reward/punishment
valence is reversed.

### What MaBouDi validates

Directly supported:

- sensory information acquisition is physically sequential;
- bees selectively sample small diagnostic portions of the available stimulus;
- sampling path is stimulus-specific;
- simply complementing reward labels does not automatically reorganize the
  sensory route.

The last point is a useful negative control for the theory: a mere renaming of
target labels is not necessarily a change in decision topology.

### Claim ceiling

This study does not positively manipulate a new action topology on one cue
matrix. It validates **selective sequential access**, not the full relational
theorem.

---

## 5. Essenberg et al. 2015 — closest branch-specific relevance example

Paper:
**The value of information in floral cues: bumblebee learning of floral size
cues**, *Behavioral Ecology* 26:1335–1344,
DOI 10.1093/beheco/arv061.

Species: *Bombus impatiens*.

Two flower types are identified by colour and scent.

Within one flower-type branch, size predicts reward; within the other branch,
size is uninformative.

The same bees learn:

\[
\text{flower type A}
\Longrightarrow
\text{size relevant},
\]

\[
\text{flower type B}
\Longrightarrow
\text{size irrelevant}.
\]

This is the closest located biological realization of **branch-specific cue
relevance**.

### Why it is not the main public reanalysis

- the uninformative branch is stochastic rather than a deterministic exact
  target-resolution task;
- a stable reusable trial-level public dataset for the 2015 experiment itself
  has not been located.

The paper should nevertheless be cited prominently because it shows that the
critical conditional architecture is biologically realizable in bumblebees.

---

## 6. Context-conditioned action is also biologically feasible

Dale et al. (2005), DOI 10.1242/jeb.01370, trained bumblebees in a sequential
priming task where the earlier priming colour changed which later target should
be approached.

With suitable supporting spatial cues, bees performed almost without error.

Lotto & Chittka (2005) likewise showed that illumination context can reverse
the correct target colour.

These studies establish that

\[
\text{earlier context}
\Longrightarrow
\text{later action rule}
\]

is within Bombus cognitive capacity.

No modern reusable public raw dataset for these historical experiments has
been located.

---

## 7. Secondary public datasets

Useful corroboration, but not needed for the main empirical bridge:

- **Smolla et al. 2016**, Dryad DOI 10.5061/dryad.3jb68:
  sequential landings and uncertainty-dependent social-information use.
- **Baracchi et al. 2017**, Dryad DOI 10.5061/dryad.743g3:
  social information is weighted more strongly in difficult foraging tasks.
- **Robert et al. 2024**, DOI 10.1007/s00265-024-03432-z:
  public visual-search data show that learned value changes inspection effort.
- **Eckel et al. 2025**, DOI 10.1242/jeb.250485;
  dataset DOI 10.4119/unibi/3004993:
  closed-loop walking trajectories make physical access/time costs observable.
- **Graver et al. 2026**, DOI 10.1242/jeb.251126:
  colour/odour weighting changes with the spatial and temporal scale of the
  decision.

Do not pool these heterogeneous studies into a meta-analysis.

---

## 8. The public Bombus evidence now forms one coherent chain

The empirical mapping to the theory is:

\[
\boxed{
\begin{array}{ll}
\text{Yuan 2026} &
\text{information is actively and costly acquired when needed}\\
\text{Spaethe 2026} &
\text{secondary cues are recruited when primary information is insufficient}\\
\text{MaBouDi 2025} &
\text{sensory access is selective and sequential}\\
\text{Essenberg 2015} &
\text{context determines whether a later cue is relevant}\\
\text{Dale 2005} &
\text{earlier context can determine the later action rule}
\end{array}
}
\]

These are not five replications of one effect. They eliminate five different
biological objections to routeability.

---

## 9. Recommended use in the theory paper

Use one compact **Bombus empirical-convergence panel** rather than claiming a
single observational validation.

### Panel A — costly acquisition

Yuan raw trials:

\[
P(\text{request})
=
0.096,\ 0.469,\ 0.716
\]

for Easy, Hard and Impossible decisions.

Pair with unaided accuracy:

\[
0.750,\ 0.494,\ 0.207.
\]

### Panel B — secondary-cue recruitment

Spaethe public conflict data:

\[
R_{\rm easy}=0.026,
\qquad
R_{\rm hard}=0.374.
\]

### Panel C — sequential sampling schematic/data citation

MaBouDi:
bees inspect only restricted diagnostic regions before commitment.

### Caption claim

> Public Bombus datasets independently support costly contingent information
> acquisition, need-dependent recruitment of secondary cues, and selective
> sequential sensory sampling. Historical experiments further demonstrate
> branch/context-dependent cue relevance. None of these datasets alone
> identifies the exact adaptive and fixed worst-case costs defined by the
> theorem.

This is strong biological grounding without overclaiming.

---

## 10. Remaining direct experiment

What is still missing is now extremely specific:

> On one unchanged physical cue matrix, change the focal action map so that one
> early outcome makes cue \(q_i\) useful next while the other outcome makes
> \(q_j\) useful next; make cue acquisition costly; impose a common finite
> budget; compare contingent and fixed access.

That is the dedicated Bombus routeability experiment.

It is no longer needed to establish that bees can:
- acquire costly information;
- allocate extra cues only when needed;
- sample sequentially;
- use contextual conditional rules.

Public data already establish those ingredients.

## Stop rule

Do not delay the theory paper for additional broad dataset searches.

Only reopen the public-data search if a candidate exposes, in one public raw
dataset:

- an early realized cue outcome;
- two or more alternative later cue acquisitions;
- acquisition order/cost;
- a matched or manipulable action map.

Anything weaker belongs in the convergence panel, not in the theorem-validation
claim.
