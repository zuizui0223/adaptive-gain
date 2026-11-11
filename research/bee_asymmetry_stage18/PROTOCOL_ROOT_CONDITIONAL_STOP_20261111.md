# Stage18: Root-dependent voluntary information stopping and cue-source choice

**2026-11-11 — EXACT THEOREM + ORIGINAL PRIOR-ART DATA AUDIT, ZERO new animal experiments.** Standalone theoretical extension stacked on Stage17 PR95. Neither Stage17's six-arm protocol nor Stage9b–16 results, main or V5/V6 were altered.

## Why Stage17 does not demonstrate stopping conditional on first-cue CONTENT
The original Stage17 hidden bits R/U/V are IID fair and T=U when R=0, T=V when R=1. A known root R changes WHICH leaf is relevant, but the unqueried target stays 50:50 in BOTH branches. A rational free-to-stop decision is therefore query for both branches when c<.5 and SKIP for both when c>=.5 (perfect root and leaf observation, correct payoff1/wrong0, normalized cost c). There is no *R-content-specific SKIP* prediction.

## Distinct source model with branch-dependent target uncertainty
Set R~Bern(.5), U~Bern(q) with 0<=q<=.5, and V~Bern(.5), all mutually independent and redrawn IID **with replacement** on every trial. Keep T=U if R=0, V if R=1. This makes the prior root-0 prediction of target0 have accuracy 1-q, while root-1 retains .5. Under perfect cue recognition:
- R0: SKIP if c>=q; request U if c<q.
- R1: SKIP if c>=.5; request V if c<.5.
At **q=.2,c=.25**, the rational contingent first action is **SKIP on R0** (guess target0 with .8 accuracy), and **request V on R1** (guaranteed perfect leaf). Thus the initial observation changes not only WHICH source, but WHETHER to buy any source. This is a completely constructed 8-state behavioral decision game; it has not occurred in bees.

## Explicit optional versus mandatory policy values
An optional FIRST leaf request may be SKIP/U/V. Precommitted first SKIP/U/V must be locked BEFORE R, with the ability to request a second distinct leaf after R if the first proves irrelevant; contingent chooses SKIP/U/V AFTER R.

\[
V_A^{opt}(q,c)=\tfrac12[\max(1-q,1-c)+\max(.5,1-c)].
\]

\[
V_F^{opt}(q,c)=\max\{.75-.5q,\;\tfrac12[1+\max(.5,1-c)]-c,\;\tfrac12[1+\max(1-q,1-c)]-c\}.
\]

**Optional-access advantage** \(\Delta^{opt}=V_A^{opt}-V_F^{opt}\). With first request mandated in both arms:
\[
V_A^{mand}=1-c,\quad
V_F^{mand}=\max\{\tfrac12[1+\max(.5,1-c)]-c,\;\tfrac12[1+\max(1-q,1-c)]-c\}.
\]

At q=.2,c=.25: \(V_A^{opt}=.775\), \(V_F^{opt}=.650\), advantage **.125**. Mandated-first \(V_A=.750\), \(V_F=.650\), advantage **.100**; the additional opportunity to SKIP adds **.025** to the mode advantage IN THIS CASE only. At higher cost the optional first-request contrast can vanish whereas mandatory querying still forces needless expenditure. Do NOT label all .125 “value of stopping.”

**Exact sharp maximum over c>=0**:
\[
\max_c\Delta^{opt}(q,c)=\begin{cases}
1/8\text{ at }c=1/4,&0\le q\le1/4,\\
(q+1/2)/6\text{ at }c=(q+1/2)/3,&1/4\le q\le1/2.
\end{cases}
\]
In particular q=.2 gives maximum **.125**, whereas q=.5 (symmetric) gives **1/6**. Enabling root-dependent stopping does NOT monotonically increase the maximum adaptive value.

The result follows by partitioning 0<=c<=q, q<=c<=.5 and c>=.5, and comparing the three precommitted first actions; independently verify with fully explicit posterior enumeration over the 8 states and optional second queries.

## Empirical feasibility is UNTESTED for this proposed q-asymmetric task
Real animal training would need to establish each subject learned the asymmetric branch priors (e.g., R0 correct target0 ~80%; R1 targets 50:50), that true root/leaf cues remain discriminable and masked, and that animals can voluntarily select **SKIP/U/V** with physical source-request timestamps, identical two-option feeders and calibrated delivered/consumed rewards. These are real feasibility gates; the toy q=.2 and utility c=.25 do NOT correspond to any measured sucrose dose or seconds. Root reliability is assumed 100% in the theorem. A symmetric q=.5 pilot control would help identify root-content-specific stopping, but must be independently registered and powered instead of silently appended to Stage17 after viewing animal data.

## Prior art read-only source, not a new experiment
He et al. 2026 bioRxiv PREPRINT DOI 10.64898/2026.09.15.751944 reports paid, uncertainty-guided information seeking in bumblebees. The authors' source at \`Cuixiaojian21/bee_metacognition\`, commit \`7f886394b4de872ecdb19ca4ea214ec321d5dce9\`, was re-downloaded from the exact public original commit and its Git blob SHA1 checked against \`26259c9071c6d73141d56b9bedd396cab1a04491\`. Source 192 bees and 19,200 trial rows. In REGULAR voluntary-request trials, 192/192 original bee IDs have a higher actual platform-landing fraction Hard than Easy, and 181/192 increase strictly Easy<Hard<Impossible. This is a **descriptive reconstruction of the authors' previously published phenomenon**; not new randomized evidence from adaptive-gain, nor 192 independent colonies. In 3,840 automatic Free Cue trials the flag \`Info_Requested\` equals 1 always, but actual landing only in 2,028; 1,812 rows would be misclassified as voluntary requests if the two original columns were conflated. Original data have NO actual U/V channel request or initial R-contingent SKIP experiment.

## Verification and stop
- [Stage18 exact 8-world Bayesian oracle and source audit GitHub Actions run #42967801326](https://github.com/zuizui0223/adaptive-gain/actions/runs/42967801326): **SUCCESS, 13 tests** (9 math + 4 source-integrity tests). TDD RED runs failed for missing modules and a missing mandatory decomposition; GREEN run passed. 112 pure theoretical q×cost combinations in artifact.
- Code and result receipt are not real observations. No ethics application, actual pilot, animal recruitment, reward calibration, actual colonies, or empirical p-values were performed. Do not treat mathematical 0.125 or source-author 192/192 as a confirmed causal payoff in the proposed task.
