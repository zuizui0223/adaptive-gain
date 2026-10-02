from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/MANUSCRIPT_RELATIONAL_ROUTEABILITY_V0_4_INFORMATION_ACCESS.md"
RECEIPT = ROOT / "validation/ecology_letters_routeability_submission_readiness_v1.json"


def _words(text):
    return re.findall(r"\b[\wÀ-ÿ'-]+\b", text)


def _sections():
    text = MANUSCRIPT.read_text()
    abstract = text[text.index("## Abstract"):text.index("## Keywords")]
    main = text[text.index("## 1. Introduction"):text.index("## References")]
    references = text[text.index("## References"):]
    return text, abstract, main, references


def test_ecology_letters_letter_limits():
    receipt = json.loads(RECEIPT.read_text())
    _, abstract, main, references = _sections()
    assert len(_words(abstract)) <= receipt["limits"]["abstract_words_max"]
    assert len(_words(main)) <= receipt["limits"]["main_text_words_max"]
    assert len(re.findall(r"(?m)^- ", references)) == receipt["current_counts"]["references"]
    assert len(receipt["figures"]) <= receipt["limits"]["combined_figures_tables_boxes_max"]


def test_ecology_letters_submission_files_exist():
    receipt = json.loads(RECEIPT.read_text())
    for rel in receipt["required_submission_files"]:
        assert (ROOT / rel).exists()


def test_ecology_letters_main_figures_exist_and_parse():
    receipt = json.loads(RECEIPT.read_text())
    for rel in receipt["figures"]:
        path = ROOT / rel
        assert path.exists()
        assert ET.parse(path).getroot().tag.endswith("svg")


def test_data_accessibility_still_flags_permanent_archive_requirement():
    text = (ROOT / "manuscript/DATA_ACCESSIBILITY_ECOLOGY_LETTERS_ROUTEABILITY_V1.md").read_text()
    assert "[PERMANENT DOI]" in text
    assert "Do not submit with the placeholder unresolved." in text
