# C. elegans context routing zero-gap control v1

## Purpose

A 2026 C. elegans result provides an unusually strong causal example of state-dependent receptor routing: hunger and intestinal infection induce `sri-36` in ADF serotonergic neurons, and SRI-36 is required and sufficient for ADF diacetyl sensitivity under the tested conditions.

This looks superficially like exactly the kind of context-dependent sensing architecture sought by adaptive-gain. It is therefore a useful stress test.

The result of that stress test is important:

> **Context-dependent receptor routing does not by itself imply a positive adaptive/fixed sensing gap.**

## Biological facts used for the control

The 2026 study reports that:

- fasting induces `SRI-36` in ADF and Pseudomonas infection further increases its expression;
- ADF-specific `sri-36` RNAi abolishes the relevant ADF diacetyl response;
- a CRISPR deletion of `sri-36` eliminates ADF responses to diacetyl in fasted/infected backgrounds;
- ADF-specific rescue restores the response;
- ectopic expression of `sri-36` in ASH confers diacetyl sensitivity;
- an endogenous SRI-36::mNeonGreen knock-in confirms state-dependent ADF expression;
- receptor abundance changes both sensory response strength and behavior.

This is strong evidence for

`internal/pathogen state -> receptor expression -> odor sensitivity -> behavior`.

It strengthens G1, G2, G3 and G7 of the genotype-policy qualification ledger.

## Why the obvious finite task has g=0

Consider the natural four-world construction formed from two physiological contexts and absence/presence of diacetyl:

| World | physiological context R | diacetyl cue D | target response |
|---|---:|---:|---|
| w1 | 0 | 0 | y00 |
| w2 | 0 | 1 | y01 |
| w3 | 1 | 0 | y10 |
| w4 | 1 | 1 | y11 |

Even if different receptor/neuron implementations are used in the two contexts, the organism-level information sources required to distinguish the four worlds are still just `R` and `D` under this declaration.

A fixed strategy can acquire both cues:

`C_F <= 2`.

An adaptive strategy cannot in general guarantee four distinct context-by-odor targets with only one binary cue, so under the ordinary fully distinct target assignment:

`C_A = 2`.

Hence

`g = C_F - C_A = 0`.

Changing which receptor implements `D` in each context changes the biological implementation, not automatically the finite decision/separation structure.

## Why receptor identity must not be counted as two cues post hoc

It would be tempting to write

- `D_AWA = ODR-10-mediated diacetyl sensing`;
- `D_ADF = SRI-36-mediated diacetyl sensing`;

and then count them as two terminal queries.

That move is not licensed merely because two receptor systems exist. If both report the same environmental variable and there is no prospectively demonstrated state in which their distinct acquisition creates different required distinctions, splitting them into separate queries would manufacture an adaptive gap by changing the representation.

The finite-task admission protocol therefore treats receptor implementation and organism-level information source as separate concepts.

## What would convert this into a positive-gap candidate

A positive q=1 witness needs a second branch-specific environmental distinction, not merely a second receptor implementation of the same distinction.

For example, one would need prospectively verified biology of the form:

1. a coarse context `R`;
2. environmental cue `A` that is required to distinguish two targets only when `R=0`;
3. a different environmental cue `B` required only when `R=1`;
4. `A` is genuinely non-informative for the branch-B target distinction and `B` is genuinely non-informative for the branch-A distinction;
5. all of the above are fixed before computing the gap.

Then the four-world star can give `C_A=2`, `C_F=3`.

The SRI-36 result currently supplies a strong candidate context-regulated sensory module, but not that second branch-specific environmental distinction.

## Scientific role of this negative control

This control prevents a serious category error:

`context-dependent molecular implementation`

is not the same as

`positive finite adaptive-gain structure`.

That distinction makes the biological program more falsifiable. A highly convincing receptor-routing system is allowed to return `g=0`; positive gap is not inferred from mechanistic sophistication.

## Reference anchor

Lei Y., Chen C., Zhan X. et al. 2026. *Intestinal pathogens override hunger-driven decision-making via immune regulation of central serotonin signaling in C. elegans*. Nature Communications. Published 25 February 2026. PubMed PMID 41735301.

## Verdict

`SRI-36` is promoted as a **causal context-routing positive control** for G1/G2/G3/G7, but simultaneously a **finite adaptive-gain zero-gap control** under the natural context × diacetyl task.

Do not use receptor switching itself as evidence for `g>0`.