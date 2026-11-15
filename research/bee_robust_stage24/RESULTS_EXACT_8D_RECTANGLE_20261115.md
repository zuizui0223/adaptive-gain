# Stage24 — exact uniform information-access benefit across an eight-dimensional uncertainty rectangle

**15 November 2026. Finite-model mathematics only. No new animal observations or biological inference.** Draft extension of Stage23 PR #101, which itself extends Stage22 PR #100. Existing sources, all prior results, V5/V6 and main remain unchanged.

## Scientific question

Stage23 proves a nonmonotonic optimum as the common paid-query cost c varies at one fixed parameter set. Does *any* advantage from conditioning first-information purchases on the noisy root cue remain after jointly varying the learned branch prior, the recognition asymmetries of all three sources, and the query cost?

We distinguish a deterministic **fixed contingent policy** from the **optimal contingent value**. The former supplies a lower bound on the latter. We make no assumption that the globally optimal action sequence stays unchanged throughout the parameter region.

## Uncertainty region (illustrative theoretical assumptions, not statistical intervals)

The frozen hidden state is R~Bern(.5), U~Bern(q), V~Bern(.5), mutually independent and redrawn with replacement per trial. The correct target is U when R0 else V. Both arms observe noisy root report Z. The fixed contingent policy is: on observed Z0, purchase nothing and answer 0; on observed Z1, purchase V and answer its reported bit; never purchase U.

| Independent parameter | Inclusive range |
|---|---|
| q=P(Utrue1) | [.16,.24] |
| s0=P(Z0 given R0) | [.76,.84] |
| s1=P(Z1 given R1) | [.56,.64] |
| u0=P(Ureport0 given Utrue0) | [.85,1] |
| u1=P(Ureport1 given Utrue1) | [.85,1] |
| v0=P(Vreport0 given Vtrue0) | [.96,1] |
| v1=P(Vreport1 given Vtrue1) | [.86,.94] |
| c=cost per actual paid source, normalized unit-correct reward | [.13,.17] |

The precommitted comparator chooses its first action SKIP/U/V before seeing Z, but can then make an optional second distinct request based on Z and the first purchased source. No information source may be purchased more than once. Both arms may make their final binary guess using all information available. Correct answer pays 1, wrong 0, each purchase costs c. No real time, sucrose, or metabolic expenditure has been calibrated.

## Main result — rigorous worst-case guarantee for ALL continuum points, not just 256 examples

Let V_fix(theta) be the expected utility of the single Z0->SKIP/0, Z1->V/report-V contingent strategy; let V_pre*(theta) be the Bayesian-optimal precommit strategy including every allowed optional second query. Exact rational optimization across all 2^8=256 vertices of the independent rectangular parameter box gives:

\[
\min_{\theta\in B}\big(V_{\rm fix}(\theta)-V^*_{\rm pre}(\theta)\big)=63/6250=+0.01008.
\]

Therefore, throughout the ENTIRE 8D continuous box:

\[
\boxed{V^*_{\rm contingent}(\theta)-V^*_{\rm pre}(\theta)\ \ge\ 63/6250\ >0.}
\]

The sharp worst vertex for the fixed strategy is q=.16, s0=.76, s1=.56, u0=u1=.85, v0=.96, v1=.86, c=.17. There V_fix=8501/12500=.68008 and V_pre*=67/100=.67. At the central Stage23 parameter values and c=.15, V_fix−V_pre*=6/125=.048.

### Why the vertex test is a proof

For any one specified deterministic policy (contingent or precommitted), its probability of each finite observation history is a product of terms linear in each of q,s0,s1,u0,u1,v0,v1. Every source is purchased at most once, and its net reward is an affine expression in c. Therefore each fixed-policy expected utility is a **multiaffine** function of the eight coordinates.

Fix the above contingent strategy pi. For EACH permitted precommitted strategy rho, the difference V_pi(theta)−V_rho(theta) is also multiaffine and reaches its minimum somewhere among the rectangle's 256 vertices. Because there are only finitely many deterministic rho, the minima commute:

\[
\min_{\theta\in B}\min_\rho[V_{\pi}(\theta)-V_\rho(\theta)]
=\min_{\rho}\min_{\theta\in B}[V_{\pi}(\theta)-V_\rho(\theta)]
=\min_{v\in{\rm corners}(B)}[V_\pi(v)-\max_{\rho}V_\rho(v)].
\]

The rightmost expression is calculated exactly by Fraction-valued eight-world dynamic programming. A randomized precommit strategy cannot improve beyond the deterministic optimal value, because expected utility is linear in strategy mixtures. The result is thus global for the entire parameter rectangle. Importantly, the exact +.01008 is the sharp worst-case of THIS fixed contingent strategy against optimal precommit, and a guaranteed lower bound for the optimally adaptive contingent strategy; it is not claimed as the sharp global worst-case optimal-to-optimal gap.

The fixed contingent strategy's closed-form expected payoff is

\[
s_0(1-q)/2 +(1-s_1)/4+s_1(v_0+v_1)/4
+(1-s_0)[1+(1-2q)(v_0-v_1)]/4
-c(1-s_0+s_1)/2.
\]

The source code verifies this independent closed form against explicit joint probability summation. The precommit DP is independently checked against a separately written *normalized posterior* Bayes optimizer at every one of the 256 vertices.

## Negative robustness control and correct limitation

For a deliberately broader theoretical box q=[.15,.25], s0=[.75,.85], s1=[.55,.65], u0=u1=[.8,1], v0=[.95,1], v1=[.85,.95], c=[.12,.18], the worst **fixed-policy** advantage is −11/8000. The certificate correctly refuses to conclude uniform positivity there. This negative value does **NOT** imply that the optimal contingent-vs-precommit gap is negative, or even zero: the fully optimal contingent agent can choose a different policy. Neither box represents empirical 95% confidence bounds or data from bees.

## Verification and inference ceiling

The 7 new isolated tests verify: the exact rectangular uniform lower bound and witness; fixed-policy closed form vs direct 8-world sum at all 256 vertices; precommitted joint-mass DP vs independently normalized Bayes posterior oracle at all 256; 66 interior rational points; fail-closed invalid parameter rectangles; a negative wider-box fixed-policy control; and no-biological-observation flags. All arithmetic is Fraction-exact. A dedicated GitHub Actions job writes a JSON machine-readable certificate for this source-free result. Full Python 3.10–3.12 repository CI remains a separate gate.

**STOP:** This Stage24 does not document actual bee perception, animal-chosen queries, colony replication, field behavior, normalized cost calibration, evolutionary fitness, or ethical permission. The bounds are constructed assumptions. Do not call them empirical uncertainty intervals or convert +.01008 into expected seed set/bee fitness. Such attribution needs original source trials and independent sampling before any biological claim.
