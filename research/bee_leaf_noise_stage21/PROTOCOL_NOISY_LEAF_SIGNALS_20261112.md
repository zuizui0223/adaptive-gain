# Stage21 — Information gained from a paid U/V cue may itself be misrecognized

**2026-11-12. Exact source-free Bayesian mathematics and 40 MOCK blinded U/V recognition rows. No real animals, cue recordings, original genetic/environmental datasets, colony-level empirical evidence, or experimental ethics approval.** Draft Stage21 is stacked on Stage20 PR #98; earlier frozen empirical outcomes and theory, V5/V6, and main are unchanged.

## New biological obstacle and restricted mathematical task
Stage20 correctly distinguished class-specific root confusion \(s_0=P(Z=0\mid R=0)\) and \(s_1=P(Z=1\mid R=1)\), but assumed *perfect* paid follow-up U/V recognition. That is exactly the quantity a real source-triggered information-acquisition experiment needs to calibrate, not assume.

Keep original hidden world iid-with-replacement per trial: \(R\sim Bern(1/2)\), \(U\sim Bern(q)\), \(V\sim Bern(1/2)\), correct target \(T=U\) when R0 else V, and noisy root observation Z with class-specific \(s_0,s_1\). After each genuine paid original leaf request, the subject receives one binary readout \(\widehat U\) or \(\widehat V\). For Stage21's *restricted symmetric-channel* model, these have reliabilities \(a_U=P(\widehat U=U)\) and \(a_V=P(\widehat V=V)\) in [1/2,1] with independent conditional bit errors. Both treatment arms receive Z. Contingent chooses initial SKIP/U/V after Z; precommit binds first SKIP/U/V before Z; an optional paid request of the other unvisited source is permitted after the first observation. The same source cannot be requested twice.

Correct binary target pays normalized utility 1, wrong 0, each leaf costs \(c\). These do **not** represent calibrated sucrose mass, seconds of delay, bumblebee sensory biology or evolutionary fitness. No original animal has learned or performed this task here.

## Exact nontrivial theorem at q=1/5 and c=1/4
For **all** \(s_0,s_1,a_U,a_V\in[1/2,1]\), exhaustive exact Bayes optimization gives:

\[
\boxed{\Delta(s_0,s_1,a_V)=
\max\big(0,\,[s_1(a_V-3/4)-(11/20)(1-s_0)]/2\big).}
\]

The optimal PRECOMMITTED first action is SKIP, with value 13/20. The contingent action after observed Z0 is SKIP. After observed Z1, V is worth requesting if and only if

\[
\boxed{a_V>\frac34+\frac{11}{20}\frac{1-s_0}{s_1}.}
\]

Equality chooses SKIP under the fixed no-unnecessary-query tie rule. If the right-hand side is ≥1, **no** paid V channel with admissible accuracy can generate a strict contingent access advantage. At \(s_0=.8,s_1=.6\), the sharp V threshold is **14/15 = 93.333...%**, even though the original Stage20 perfect-V gain was .020 normalized reward.

Within this **specific** q/c task, the accuracy of U does NOT affect the optimum. Why? U is informative only in the R0 branch, and even a perfect U display can improve the best guess by at most q=.2 times the posterior probability of R0. Since the paid cost is c=.25, requesting U cannot be worthwhile. This is a mathematical restriction, NOT a claim that real U clues have no value in ecology; it changes at other priors, costs, signal channels, or tasks.

Reducing to \(a_V=1\) yields exactly Stage20's sharp \(11s_0+5s_1>11\) boundary; reducing to \(s_0=s_1=1\) gives the Stage18 perfect-root conditional V decision, now sensitive to V recognition.

## Two independent nonidentification counterexamples
1. With \(s_0=.8,s_1=.6\), \((a_U,a_V)=(.8,1)\) produces \(\Delta=.020\), while \((1,.8)\) produces **0**. Both have *the same 90% mean paid-cue recognition*. Average U/V accuracy is not a sufficient statistic for the value of buying the relevant cue.
2. Two purely fabricated, equally weighted colony/bee confusion profiles A=(.8,1) and B=(1,.8) have individual theoretical gains .020 and 0, giving equal-colony mean **.010**, while evaluating the optimum at the pooled accuracies (.9,.9) gives **0**. This is nonlinear aggregation of a positive-part function, not a discovery of a colony effect.

## Source-only pilot measurement gate, NOT a completed live pilot
The 40 artificial original-trial rows consist of two invented colony IDs, one invented bee each, 10 U and 10 V detection trials per imaginary animal, balanced over source TRUE bit=0/1 to prevent biased U~Bern(.2) base rate from manufacturing high classification accuracy. A root cue, target reward position and any alternate source are NOT accessible. Each trial records native leaf type, hidden true bit, original reported bit, temporal order of cue→response→feedback, video verification markers and source original IDs. Real animal records are **rejected** by this public QA module.

The QA emits **per-original-bee and per-true-bit** values:
- \(P(\widehat U=0\mid U=0)\) and \(P(\widehat U=1\mid U=1)\);
- \(P(\widehat V=0\mid V=0)\) and \(P(\widehat V=1\mid V=1)\).

The theorem assumes symmetrical bit flips for each paid channel, but **real finite-pilot empirical class sensitivities will rarely be numerically identical**. Exact equality is used here only to validate the deliberately symmetric mock fixture. An actual animal pilot must retain all four confusion entries, their sampling uncertainty, separately qualified independent-colony clusters, and if asymmetric effects matter, use a NEW four-error-channel decision model—not silently average them or delete discrepant bees. Neither the invented 40 samples nor their math gains estimate any true animal recognition or generalization.

Real-pilot prerequisites: learn and test R and conditional U/V task priors independently, source-verify true **animal-selected** SKIP/U/V actions with optional second request, ensure no cue identity/reward leaks before acquisition, calibrate device delay and consumed sucrose separately, retain true sensor failures as missing rather than confirmed no-drink zero, require original bee/colony lineage IDs and prospective ethical review/registration. A merely positive fitted threshold based on guessed parameters is not proof of a natural information-routing advantage.

## Verification
[Stage21 exact/noisy-leaf and mock pilot Actions #43216365839](https://github.com/zuizui0223/adaptive-gain/actions/runs/43216365839): **SUCCESS, 17 focused tests**: independently written normalized-posterior Bayesian eight-world optimizer vs separate Fraction-valued joint-mass source; 480 exact sensitivity grid cells, a \(14/15\) sharp threshold and tests of Stage20 when \(a_U=a_V=1\). The 40 mock leaf recordings validate source cell grain only. No original biological observation is incorporated.

**Scientific stopping rule:** No result is promoted as a positive empirical claim. Report zero current bee observations; do not adjust the .25 normalized query cost, q=.2 or information channels after future outcomes to rescue an effect. A real physical cost can be determined only by a blinded, preregistered pilot; Stage21 uses hypothetical cost units.
