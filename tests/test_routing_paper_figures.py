from pathlib import Path

from routing_paper.figures.generate_figures import generate_all


def test_routing_paper_figures_are_reproducible_and_semantically_pinned(tmp_path: Path):
    outputs = generate_all(tmp_path)
    names = {p.name for p in outputs}
    assert names == {
        "figure1_routing_layers.svg",
        "figure2_occupancy_thresholds.svg",
        "figure3_scope_controls.svg",
    }

    texts = {p.name: p.read_text(encoding="utf-8") for p in outputs}
    for text in texts.values():
        assert "<svg" in text[:500]
        assert text.rstrip().endswith("</svg>")
        assert len(text) > 1000

    f1 = texts["figure1_routing_layers.svg"]
    for token in ("19", "7", "1", "2^k - 1"):
        assert token in f1

    f2 = texts["figure2_occupancy_thresholds.svg"]
    for token in ("mode", "majority", "49/117", "9.09", "q+2", "q+3"):
        assert token.lower() in f2.lower()

    f3 = texts["figure3_scope_controls.svg"]
    for token in ("4/7", "4/37", "representation", "neutral mutation"):
        assert token.lower() in f3.lower()
