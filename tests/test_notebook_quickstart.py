from __future__ import annotations

import json
from pathlib import Path


NOTEBOOK = Path(__file__).resolve().parents[1] / "notebooks" / "trust_tc_interval_quickstart.ipynb"


def _notebook_text() -> tuple[dict, str]:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    text = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
    )
    return notebook, text


def test_quickstart_notebook_exists_and_has_expected_sections() -> None:
    assert NOTEBOOK.exists()
    notebook, text = _notebook_text()
    cells = notebook.get("cells", [])
    assert len(cells) >= 12
    headings = [
        "TRUST-TC interval analysis quickstart",
        "What TRUST-TC does",
        "Load an example input table",
        "Run TRUST-TC interval mode",
        "Read the interval output",
        "Plot interval estimates",
        "Run field-style examples",
        "Use a custom calibration table",
        "Command-line equivalent",
    ]
    for heading in headings:
        assert heading in text


def test_quickstart_notebook_uses_only_public_paths_and_defines_models() -> None:
    _, text = _notebook_text()
    required_paths = [
        "examples/example_fitted_results.csv",
        "examples/ntu_tool_demo.csv",
        "examples/fukuoka_tool_demo.csv",
        "src/trust_tc/calibration/full3d_production_correction_factor_distribution.csv",
    ]
    for path in required_paths:
        assert path in text
    assert "LT-ILS" in text
    assert "late time infinite line source" in text.lower()
    assert "exact infinite line source" in text.lower()
    assert "infinite cylindrical source" in text.lower()
    assert "finite line source" in text.lower()


def test_quickstart_notebook_has_no_banned_terms() -> None:
    _, text = _notebook_text()
    banned_terms = [
        "field truth",
        "known-answer",
        "known answer",
        "A0",
        "A1",
        "A2",
        "A3",
        "A4",
        "DPL",
        "tau_q",
        "tau_T",
        "MLS",
        "moving-line-source",
        "manuscript",
        "Geothermics",
        "journal submission",
    ]
    lowered = text.lower()
    for term in banned_terms:
        assert term.lower() not in lowered


def test_quickstart_notebook_writes_interval_outputs_without_truth_columns() -> None:
    _, text = _notebook_text()
    assert "run_interval_mode(" in text
    assert "outputs/tool_demo/notebook_intervals.csv" in text
    for forbidden_column in ["true_lambda", "true_C", "true_alpha", "field_truth"]:
        assert forbidden_column not in text
