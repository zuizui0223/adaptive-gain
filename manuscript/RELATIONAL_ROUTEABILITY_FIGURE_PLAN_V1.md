# Relational routeability figure plan v1

Status: figure architecture for the American Naturalist-oriented v0.3 draft.

## Figure 1 — Same cue environment, different action-conditioned topology

### Purpose

Show the relational theorem visually without beginning from equations.

### Panel A — one physical cue environment

Display the same set of ecological states with the same cue matrix in both tasks.

Use a compact schematic:
- rows = ecological alternatives;
- columns = cue channels;
- identical cue symbols on both sides.

Label:

**Physical cue environment held fixed**

### Panel B — two target/action maps

Place two target colorings or accept/reject labels over the same rows.

Left:
**Routeable action map**

Right:
**Matched control action map**

Emphasize:
- same states;
- same cues;
- same cue distributions;
- same target prevalence;
- different mapping from cue state to action.

### Panel C — decision trees

Routeable:
- early routing cues;
- branch-specific terminal cue;
- path cost \(\le d+1\);
- fixed burden \(\ge2^d\).

Control:
- first two routing bits already resolve target;
- \(C_A=C_F=2\).

Headline annotation:

\[
\text{same cue environment}\not\Rightarrow\text{same acquisition geometry}.
\]

### Main message

Routeability is relational, not an intrinsic scalar property of the physical environment.

---

## Figure 2 — Ecological budget exposes the topology

### Purpose

Show exactly where the mathematical distinction becomes ecological.

### Panel A — cost axis

Horizontal axis: acquisition budget \(B\).

Mark:
- \(C_A\);
- \(C_F\).

Shade three regions:

1. \(B<C_A\): neither access mode guarantees success;
2. \(C_A\le B<C_F\): contingent-only window;
3. \(B\ge C_F\): both access modes can succeed.

Use routeable architecture.

### Panel B — matched common-budget contrast

Set:

\[
B=d+1.
\]

Show four cells:

| architecture | contingent | fixed |
| --- | --- | --- |
| routeable | success | fail |
| control | success | success |

Display exact interaction:

\[
(1-0)-(1-1)=1.
\]

Add note:

**guaranteed-resolution contrast, not behavioral effect size**

### Panel C — experimental realizations

Minimal experiment:
- four states;
- three cues;
- budget ladder \(B=1,2,3\).

Stress test:
- ten states;
- six cues;
- every cue 5:5 balanced;
- \(B=3\);
- exact deterministic ceiling interaction \(=1/5\).

### Main message

Natural history enters through the observation budget, not by changing the combinatorics.

---

## Supplementary Figure S1 — Summary sufficiency ladder

Optional.

Display:

\[
\text{counts}
\to
\text{marginals}
\to
\text{cue-only joint distribution}
\to
H(T)
\to
I(T;Q_{\rm all})
\to
\text{pairwise target-cue profiles}
\to
\text{complete action-conditioned table}.
\]

Use crosses through the first levels to indicate explicit counterexamples.

Only the final complete structural table specifies the deterministic routeability problem.

---

## Figure discipline

Keep the main paper to two figures.

Do not include:
- mathematical companion star--edge--star extremal geometry;
- diversity-stability speculation;
- Villavicencio observation-model results;
- stochastic expected-loss extensions.

Those would dilute the relational theorem headline.

## Stop rule

No third main figure unless a demonstrated editorial problem requires it.
