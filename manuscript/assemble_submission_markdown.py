"""Assemble the submission-facing manuscript without rewriting scientific source text.

The canonical scientific prose remains manuscript/MANUSCRIPT_V1.md.  This script
performs only two deterministic submission-surface operations:

1. insert one controlled Fig. 1--4 callout at four exact prose anchors;
2. extract the four controlled legend paragraphs from FIGURE_LEGENDS_V1.md and
   place them before the reference list.

It intentionally does not inject author names, affiliations, funding, competing
interests, or contribution statements. Those are author-controlled metadata.
"""
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "MANUSCRIPT_V1.md"
LEGENDS = HERE / "FIGURE_LEGENDS_V1.md"
DEFAULT_OUTPUT = HERE / "MANUSCRIPT_SUBMISSION.md"

CALLOUTS = (
    (
        "We call this obligation family the `productive frontier`; only its size `E_i` enters the main ecological argument.",
        "The distinction between contingent and fixed cue use, and its connection to recurrence of the same ecological states, is summarized in Fig. 1.",
    ),
    (
        "This reverse map is the principal result: a requested local dynamical phase imposes a lower bound on the finite deterministic sensing architecture capable of supporting it. It is not a lower bound on Shannon mutual information.",
        "The reverse map, its binary exact corner, and the bounded-arity Pareto trade-off are summarized in Fig. 2.",
    ),
    (
        "an asymptotic crossover proxy rather than a finite-time hitting-time bound.",
        "Figure 3 separates extremal sharpness from realized tightness by displaying the two exact multiplicative sources of slack.",
    ),
    (
        "The distinction matters because the two mechanisms respond differently to perturbation; the underlying identity-map versus contraction algebra is standard.",
        "The four long-time outcomes and the stronger feedback implication of model-compatible oscillatory restoration are contrasted in Fig. 4.",
    ),
)

REFERENCE_HEADING = "## References cited in the current draft"


def _extract_legends(text: str) -> list[str]:
    legends: list[str] = []
    for number in range(1, 5):
        pattern = re.compile(
            rf"^\*\*Figure {number} \|.*?\*\*.*?(?=\n\n\*\*Preferred first callout:)",
            flags=re.MULTILINE | re.DOTALL,
        )
        match = pattern.search(text)
        if match is None:
            raise ValueError(f"controlled Figure {number} legend not found")
        legend = match.group(0).strip()
        if f"Figure {number} |" not in legend:
            raise AssertionError("legend extraction lost figure identifier")
        legends.append(legend)
    return legends


def assemble(source_text: str, legend_text: str) -> str:
    out = source_text

    for anchor, callout in CALLOUTS:
        if out.count(anchor) != 1:
            raise ValueError(f"callout anchor must occur exactly once: {anchor[:70]!r}")
        if callout in out:
            raise ValueError("source manuscript already contains a controlled figure callout")
        out = out.replace(anchor, anchor + "\n\n" + callout, 1)

    if out.count(REFERENCE_HEADING) != 1:
        raise ValueError("reference heading must occur exactly once")

    legends = _extract_legends(legend_text)
    legend_block = "## Figure legends\n\n" + "\n\n".join(legends) + "\n\n"
    out = out.replace(REFERENCE_HEADING, legend_block + REFERENCE_HEADING, 1)

    # Submission-surface invariants.
    for number in range(1, 5):
        assert out.count(f"Fig. {number}.") == 1
        assert out.count(f"Figure {number} |") == 1
    assert out.count("## Figure legends") == 1
    assert out.count(REFERENCE_HEADING) == 1
    assert out.index("## Figure legends") < out.index(REFERENCE_HEADING)
    return out


def main(output: Path = DEFAULT_OUTPUT) -> Path:
    source_text = SOURCE.read_text(encoding="utf-8")
    legend_text = LEGENDS.read_text(encoding="utf-8")
    assembled = assemble(source_text, legend_text)
    output.write_text(assembled, encoding="utf-8")
    return output


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    main(args.output)
