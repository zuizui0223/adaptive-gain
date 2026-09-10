# Theoretical Ecology submission checklist v1

## Checked target fit

Target journal: *Theoretical Ecology* (Springer Nature).

Checked 2026-09-10. The journal's stated editorial direction emphasizes theoretical approaches that answer questions of ecological interest and remain readable by a broad audience of ecologists. The current manuscript should therefore lead with the ecological reachability question and natural-history meaning of the finite sensing structure, not with combinatorial terminology.

Relevant public journal page used for fit check:

- https://link.springer.com/article/10.1007/s12080-010-0070-4

The current published journal surface uses standard research-article organization with an abstract, keywords, main text, references, figures and declarations. Exact submission-portal formatting can change, so portal-specific metadata should be checked again at upload; it is not used to alter theorem content.

## Current manuscript-facing status

Branch: `manuscript/theoretical-ecology-line-edit-20260910`

Frozen prior submission candidate: `release/theoretical-ecology-submission-candidate-v1` at `fa87a79d6f3d99048f357ad9253d53706cf227ff`.

### Title

Current proposed title:

> Finite sensing structure constrains eco-evolutionary feedback regimes

Rationale:

- short and biologically legible;
- avoids the overly broad phrase `information structure` after the Moffett-Eckford prior-art audit;
- foregrounds sensing rather than Shannon information;
- emphasizes the principal feedback-reachability theorem rather than treating all supporting results equally.

### Abstract

Current abstract length: approximately 190 words by whitespace/token word count.

Abstract requirements imposed internally:

- no citations;
- no undefined theorem notation;
- biological intuition before combinatorial terminology;
- principal reverse reachability result first;
- structural-temporal bound explicitly described as an extremal ceiling;
- oscillation result explicitly model-conditional and diagnostic;
- stasis result explicitly a mechanistic distinction;
- finite structural result explicitly distinguished from Shannon-information/rate-distortion bounds.

### Keywords

Five current keywords:

- Adaptive information use
- Decision trees
- Evolutionary stasis
- Fluctuating selection
- Temporal autocorrelation

These support discoverability without turning `minimum information` or `information threshold` into manuscript branding.

## Ecological readability gate

The first page should allow an ecologist to answer the following before encountering the main theorem:

1. What is the organism doing? It samples cues to distinguish ecologically relevant alternatives.
2. What is adaptive about the sensing architecture? Later cues may depend on earlier outcomes.
3. What is the fixed comparison? One cue set must guarantee the same distinctions without contingent routing.
4. What is the structural gap? The extra worst-case burden of the fixed strategy relative to contingent sensing.
5. Why does ecology matter? Natural history declares the alternatives, cues and required distinctions; recurrent ecological states determine how structural rewards recur through time.
6. What does the theorem reverse? A required local feedback regime is mapped back to the minimum or Pareto-minimal finite sensing architecture capable of supporting it.

If any of these answers disappears during later shortening, restore the ecological explanation rather than adding more formal notation.

## Claim boundary gate

Do not use the following as novelty phrases:

- `minimum information` without qualification;
- `fitness value of information`;
- `information threshold`;
- generic eco-evolutionary feedback;
- generic oscillation or critical slowing;
- generic adaptive decision trees or adaptivity gaps.

Preferred principal claim:

`required local feedback regime -> required adaptive/fixed structural gap -> minimum/Pareto-minimal finite deterministic sensing architecture over (n,m,E)`.

The finite structural quantities are worst-case and distribution-free once the task is declared. They are not Shannon bits and do not generally determine, or follow from, mutual information without additional probabilistic assumptions.

## Main-text hierarchy gate

Keep the following order:

1. principal reachability theorem;
2. supporting structural-temporal extremal envelope;
3. diagnostic model-compatible oscillation result;
4. mechanistic cancellation-versus-restoration proposition.

Do not restore a four-coequal-theorem presentation.

## Natural-history gate

The main Model may contain one short generic example of sequential habitat/resource assessment:

`coarse cue -> branch choice -> fine-scale cue -> action`

Its purpose is only to explain adaptive routing. It must not become an observation-design protocol or imply that all ecological applications share the same sensory sequence.

## Remaining submission work

No new theorem is required. Remaining tasks are:

1. audit the line-edited manuscript against the frozen theorem spine so no formula or domain condition changed;
2. complete Figure 1-4 as publication-ready conceptual/theoretical figures;
3. add title-page author/affiliation/correspondence metadata only when final author information is deliberately set;
4. add standard declarations required by the submission portal (funding, competing interests, data/code availability as applicable);
5. render the bibliography to the journal's exact current style at upload;
6. record the exact manuscript commit/tree used for submission.

## Stop rule

Do not reopen theory development merely to make the manuscript look more substantial. A new theorem belongs on a separate theory branch and requires a fresh claim audit before it can enter the submission surface.
