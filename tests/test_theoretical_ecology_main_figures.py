from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "manuscript" / "figures"
RECEIPT = ROOT / "validation" / "theoretical_ecology_main_figures_v1.json"
GENERATOR = FIGURE_DIR / "generate_main_figures.py"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _audit_committed_figures(receipt: dict) -> dict[str, str]:
    observed: dict[str, str] = {}
    for name, expected in receipt["figure_files"].items():
        path = FIGURE_DIR / name
        assert path.exists()
        assert path.stat().st_size == expected["bytes"]
        observed[name] = _sha256(path)
        assert observed[name] == expected["sha256"]
        root = ET.parse(path).getroot()
        assert root.tag.endswith("svg")
        assert root.attrib.get("viewBox") == expected["viewbox"]
        assert not any(node.tag.endswith("image") for node in root.iter())
    return observed


def test_main_figures_are_exactly_reproducible() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    before = _audit_committed_figures(receipt)

    subprocess.run([sys.executable, str(GENERATOR)], cwd=ROOT, check=True)

    after = _audit_committed_figures(receipt)
    assert after == before


def test_generator_declares_and_passes_numerical_audit() -> None:
    namespace: dict[str, object] = {"__name__": "figure_audit_import"}
    exec(GENERATOR.read_text(encoding="utf-8"), namespace)
    namespace["audit"]()
    assert namespace["pareto_fixture"](3, 4) == [(8, 5, 5, 2), (7, 6, 6, 3)]
