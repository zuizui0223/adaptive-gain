# Uehara et al. 2026 individual probe-latency audit v1

Status: public-data empirical gate for the V6 fitness-frontier programme.

Source paper:

Uehara, Dong & Duvall (2026), *Communications Biology* 9:757,
"Behavioral heterogeneity in host seeking and post-feeding suppression among
disease vector mosquitoes", DOI 10.1038/s42003-026-09987-z.

Public code:

- \`Duvall-Lab/UeharaDongDuvall2025\`

Public Supplementary Data 1:

- \`42003_2026_9987_MOESM3_ESM.xlsx\`

## 1. Why this dataset is useful

The Chandel Figure 3a dataset supplies a high-resolution aggregate temporal
response but not a mapped individual completion-time distribution.

The Uehara programme retains individual behavioral trajectories and therefore
offers a route to the V6 completion-profile object

\[
F_j(t)=P(T_j\le t).
\]

The paper reports:

- 60 fps behavioral recording;
- individual wells analyzed separately;
- framewise behavioral classification;
- behavioral categories including probing;
- public analysis code;
- public Supplementary Data;
- videos archived at Zenodo DOI 10.5281/zenodo.15478199.

## 2. Public-code audit

The acquisition README states a frame rate of 60 fps.

The analysis notebook reads XLSX files in which:

- rows are framewise behavioral observations;
- columns are individual animals;
- behavior code 0 is treated as inactive;
- behavior code 2 is treated as probing.

For the focal 8-minute analysis window the notebook uses

\[
\text{start frame}=3600,
\]

and

\[
\text{end frame}=32400.
\]

At 60 fps this corresponds to:

- a 60 s pre-window;
- 28,800 analyzed post-onset frames;
- 480 s of behavior.

The private/local stage-4 and stage-5 XLSX files referenced by the notebook are
not present in the public GitHub repository.

## 3. Frame-resolved candidate endpoint

If the processed framewise behavior XLSX is recovered, define for one individual

\[
T_{\rm probe}
=
\frac{
f_{\rm first\ probe}-f_{\rm stimulus\ onset}
}{60}.
\]

Trials with no probe in the declared window should remain right-censored for
survival-style summaries, or be represented as \(T=\infty\) only for a
finite-window timely-success calculation.

Those two treatments must not be mixed.

## 4. Supplementary Data closes a coarser individual gate

The published Supplementary Data do **not** contain 28,800 frame rows.

However, sheet \`Fig2D and S2\` retains one row per included individual and
separate one-minute Probe percentages for:

\[
-1\text{ to }0\ {\rm min}
\]

and

\[
0\text{ to }1,\ 1\text{ to }2,\ldots,7\text{ to }8\ {\rm min}.
\]

The number of individual rows in each species block exactly matches the
timepoint-0 inactive-before-cue count in sheet \`Excl_Spp_Cond\`.

Therefore a defensible coarse endpoint is already recoverable:

> among individuals with zero probing in the -1 to 0 min bin, record the first
> post-stimulus one-minute bin with Probe% > 0.

This is a one-minute **interval-censored** first-probe onset, not a frame-resolved
latency.

The resulting public-data analysis is recorded in:

- \`biology/UEHARA_2026_BINNED_FIRST_PROBE_RESULTS_V1.md\`;
- \`validation/uehara_binned_first_probe_v1.json\`;
- \`scripts/analyze_uehara_binned_first_probe.py\`.

## 5. What the coarse data can estimate

The Supplementary Data now provide individual discrete completion profiles:

\[
F_j(k)
=
P(T_{\rm probe}\le k\ {\rm min}),
\qquad
k=1,\ldots,8,
\]

conditional on no observed probing in the preceding one-minute bin.

This permits direct description of:

- early-tail mass;
- delayed onset;
- right-censoring through 8 min;
- cross-species differences in discrete completion-profile shape.

It is already substantially closer to the V6 expected-value layer than an
aggregate percent-probing trajectory.

## 6. What still requires frame-level data

The coarse Source Data cannot identify:

- sub-minute first-probe latency;
- exact within-bin event order;
- whether probing began at 2 s versus 58 s inside one minute;
- short-timescale completion-CDF crossings;
- frame-resolved response to cue onset.

Those remain a refinement gate, not a prerequisite for demonstrating
individual temporal heterogeneity.

## 7. Claim ceiling

Neither the coarse nor future frame-level first-probe endpoint is automatically:

- time to successful blood feeding;
- time to a physiologically sufficient meal;
- reproductive fitness;
- the natural opportunity distribution;
- an adaptive-versus-fixed architecture comparison.

The public data close an **individual temporal-process** layer, not the full
selection chain.

## 8. Current empirical gate

Status:

\[
\boxed{
\text{individual coarse completion profile: OPEN}
}
\]

because the public Supplementary Data are sufficient.

Status:

\[
\boxed{
\text{frame-resolved first-probe latency: PENDING}
}
\]

because the processed framewise XLSX mapping is still absent from the public
GitHub repository.

The frame-level refinement should be pursued only if it changes a V6 inference;
the one-minute Source Data result is already a valid empirical anchor at its
declared resolution.
