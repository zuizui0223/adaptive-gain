# Uehara et al. 2026 individual probe-latency audit v1

Status: public-code empirical gate for the V6 fitness-frontier programme.

Source paper:

Uehara, Dong & Duvall (2026), Communications Biology,
"Behavioral heterogeneity in host seeking and post-feeding suppression among
disease vector mosquitoes", DOI 10.1038/s42003-026-09987-z.

Public code:

Duvall-Lab/UeharaDongDuvall2025

## 1. Why this dataset is useful

The Chandel Figure 3a dataset supplies a high-resolution aggregate temporal
response but not a mapped individual completion-time distribution.

The Uehara pipeline is closer to the quantity needed by the V6 theory.

The paper reports:

- 60 fps behavioral recording;
- individual wells analyzed separately;
- framewise behavioral classification;
- behavioral categories including probing;
- all code public on GitHub;
- raw data supplied with the paper and videos archived on Zenodo.

This makes an individual first-probe latency distribution feasible in
principle.

## 2. Public-code audit

The repository's acquisition README states:

- frame rate: 60 fps.

The analysis notebook shows the post-blood-feeding behavior pipeline reading
XLSX files in which:

- rows are framewise behavior observations;
- columns are individual animals;
- behavior code 0 is treated as inactive;
- behavior code 2 is treated as probing.

For the 8-minute analysis window the notebook uses:

[
	ext{start frame}=3600,
]

[
	ext{end frame}=3600+3600	imes8=32400.
]

At 60 fps this corresponds to:

- 60 s before the analyzed stimulus window;
- 28,800 analyzed frames;
- 480 s of behavior.

The notebook computes, for every individual column,

[
rac{#{	ext{frames coded probe}}}{28800},
]

confirming that the underlying files retain individual framewise behavior codes
rather than only group summaries.

## 3. Candidate completion-time variable

For one individual define

[
T_{m probe}
=
rac{
f_{m first probe}-f_{m stimulus onset}
}{60}.
]

A first analysis should use the already processed behavioral-state XLSX rather
than reclassifying video.

Trials with no probe during the declared observation window should remain
right-censored for survival-style summaries or be encoded as
(T=infty) only for a finite-window timely-success calculation.

These two treatments must not be mixed.

## 4. What this can estimate

If the frame-level XLSX files are recovered, the public data can estimate:

[
F_j(t)
=
P(T_{m probe}le t)
]

for each declared condition (j).

This is much closer to the V6 process variable than aggregate percent probing.

It can test:

- early-tail differences;
- median latency differences;
- persistence of non-probing;
- whether two conditions have crossing completion CDFs;
- whether mean latency is a misleading summary.

It still does not supply the ecological value function (U(t)) by itself.

## 5. Claim ceiling

A first-probe CDF is not automatically:

- time to successful blood feeding;
- time to a physiologically sufficient meal;
- reproductive fitness;
- an adaptive-versus-fixed architecture comparison;
- the natural opportunity distribution.

The public data can close the individual completion-time side of the V6
process, not the full selection chain.

## 6. Current data gate

The GitHub repository contains analysis code but not the local
`data_stage_4` / `data_stage_5` XLSX files referenced by the notebook.

The Communications Biology paper states that raw data are provided in the
associated data file and videos are deposited at Zenodo DOI
10.5281/zenodo.15478199.

The next empirical gate is therefore:

1. obtain the associated frame-level behavior XLSX or identify its public
   mapping;
2. verify that the columns and behavior codes match the notebook assumptions;
3. freeze a stimulus-onset and censoring contract;
4. run the latency extractor added in this branch;
5. compare individual (F_j(t)) curves before any fitness interpretation.

No latency result is claimed until that gate is crossed.
