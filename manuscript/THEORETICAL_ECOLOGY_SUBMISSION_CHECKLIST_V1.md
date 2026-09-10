# Theoretical Ecology submission checklist v1

## Checked target fit

Target journal: *Theoretical Ecology* (Springer Nature).

Checked 2026-09-10 and carried into finalization on 2026-09-11. The journal's editorial direction emphasizes theoretical approaches that answer questions of ecological interest and remain readable by a broad audience of ecologists. The manuscript therefore leads with the ecological reachability question and natural-history meaning of finite sensing structure rather than with combinatorial terminology.

Relevant public journal page used for fit check:

- https://link.springer.com/article/10.1007/s12080-010-0070-4

Recent published articles were also inspected for the current submission-facing pattern of abstract, keywords, figures, data/code availability, author contributions/correspondence, funding, and competing-interest declarations. Exact portal labels can change and must be rechecked at upload; they do not alter theorem content.

## Current manuscript-facing status

Finalization branch:

`manuscript/theoretical-ecology-finalization-20260911`

Frozen line-edited text:

`release/theoretical-ecology-submission-text-v1` at `e1735f60a11508c7c18ed59cca1cf4848b5296eb`.

Frozen text + four reproducible main figures:

`release/theoretical-ecology-submission-with-figures-v1` at `789d9ef993148258d22222b2c83e45164fbc09d3`, tree `f565d90b6b3c4d7095af84b69b3ece322a61164c`.

Post-merge workflow `34500493463` passed Python 3.10, 3.11, and 3.12 with full `pytest`, `examples/audit_witnesses.py`, and `examples/audit_certificate_ladder.py`.

### Title — READY

> Finite sensing structure constrains eco-evolutionary feedback regimes

The title is short, biologically legible, avoids overly broad `information structure` branding after the Moffett-Eckford prior-art audit, and foregrounds the principal feedback-reachability theorem.

### Abstract — READY

Current abstract length: approximately 190 words by internal whitespace/token count.

It contains no citations or undefined theorem notation, introduces biological intuition before combinatorial terminology, states the principal reverse reachability result first, labels the structural-temporal result as an extremal ceiling, keeps oscillation model-conditional and diagnostic, treats stasis as a mechanistic distinction, and explicitly distinguishes finite structural counts from Shannon-information/rate-distortion bounds.

### Keywords — READY

- Adaptive information use
- Decision trees
- Evolutionary stasis
- Fluctuating selection
- Temporal autocorrelation

### Main figures — READY AND REPRODUCIBLE

Four main figures are complete in `manuscript/figures/`:

1. `figure1_state_space.svg`
2. `figure2_reachability.svg`
3. `figure3_extremal_envelope.svg`
4. `figure4_long_time_outcomes.svg`

They are deterministic 1600x900 vector SVGs generated with the Python standard library. `tests/test_theoretical_ecology_main_figures.py` verifies committed checksums, XML validity, absence of raster image elements, exact regeneration, and numerical fixtures. The figure branch, PR #10, and post-merge main all passed the three-version CI matrix.

Controlled legends and preferred callout positions are in `manuscript/FIGURE_LEGENDS_V1.md`.

## Ecological readability gate — PASS

Before encountering the principal theorem, a reader can identify:

1. the organismal task: sampling cues to distinguish ecologically relevant alternatives;
2. contingent sensing: later cues can depend on earlier outcomes;
3. the fixed comparison: one cue set must guarantee the same distinctions without contingent routing;
4. the structural gap: extra worst-case burden of the fixed strategy;
5. the ecological role: natural history declares alternatives/cues/distinctions and recurrent ecological states determine how rewards recur;
6. the reverse theorem: a required local feedback regime maps back to a minimum or Pareto-minimal finite sensing architecture.

The one-paragraph generic example `coarse cue -> branch choice -> fine-scale cue -> action` remains illustrative and is not an observation-design protocol.

## Claim boundary gate — PASS

Do not use the following as novelty phrases:

- `minimum information` without qualification;
- `fitness value of information`;
- `information threshold`;
- generic eco-evolutionary feedback;
- generic oscillation or critical slowing;
- generic adaptive decision trees or adaptivity gaps.

Preferred principal claim:

`required local feedback regime -> required adaptive/fixed structural gap -> minimum/Pareto-minimal finite deterministic sensing architecture over (n,m,E)`.

The structural quantities are worst-case and distribution-free once the task is declared. They are not Shannon bits and do not generally determine, or follow from, mutual information without additional probabilistic assumptions.

## Main-text hierarchy gate — PASS

Keep the order:

1. principal reachability theorem;
2. supporting structural-temporal extremal envelope;
3. diagnostic model-compatible oscillation result;
4. mechanistic cancellation-versus-restoration proposition.

Figure 2 carries the principal visual claim; Figures 3 and 4 must not be promoted into coequal novelty headlines.

## Submission declarations

Controlled declarations are in `manuscript/SUBMISSION_DECLARATIONS_V1.md`.

### Data and code availability — READY

The study is theoretical and generates/analyses no empirical dataset. Public source code, executable audits, and the deterministic figure generator are available in `zuizui0223/adaptive-gain`. A permanent archive DOI may replace or supplement the repository reference only after one is actually minted.

### Funding — AUTHOR INPUT REQUIRED

No statement is inferred.

### Competing interests — AUTHOR INPUT REQUIRED

No statement is inferred.

### Author contributions — AUTHOR INPUT REQUIRED

Complete after final author list/order is deliberately set.

### Corresponding author / affiliation / ORCID — AUTHOR INPUT REQUIRED

Do not infer from Git metadata, account information, or unrelated projects.

### Ethics / consent — PORTAL CHECK

Expected to be not applicable for this theoretical study, but use the portal wording in force at submission.

## Submission metadata control

`manuscript/SUBMISSION_METADATA_V1.md` contains the frozen title, abstract source, keywords, figure paths, release refs, claim hierarchy, and unresolved author-controlled fields.

## Remaining submission work

No new theorem or figure is required. Remaining work is narrow:

1. integrate the controlled Fig. 1-4 callouts and legends into the exact upload manuscript or deterministic export;
2. supply and verify final author list/order, affiliations, correspondence metadata, and ORCID(s) if used;
3. author-approve funding, competing-interests, and contribution declarations;
4. render/check references in the exact current submission format and inspect the portal-generated PDF for mathematical-symbol corruption;
5. if desired, mint a permanent code archive DOI and replace/supplement the GitHub-only availability reference;
6. record the exact commit/tree and files actually uploaded.

These are submission-control tasks. None justifies reopening the mathematical theory.

## Stop rule

Do not reopen theory development merely to make the manuscript look more substantial. A new theorem belongs on a separate theory branch and requires a fresh claim audit before it can enter the submission surface.
