from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

from trust_tc.open_tool import run_interval_mode


def test_interval_mode_converts_existing_results_without_field_truth_columns(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    input_csv = tmp_path / "fitted_results.csv"
    output_csv = tmp_path / "intervals.csv"

    pd.DataFrame(
        [
            {
                "site": "Demo",
                "depth_interval": "whole",
                "interpretation_model": "ICS",
                "parameter": "lambda",
                "apparent_estimate": 2.5,
                "support_id": "whole",
            },
            {
                "site": "Demo",
                "depth_interval": "whole",
                "interpretation_model": "ICS",
                "parameter": "C",
                "apparent_estimate": 2.4e6,
                "support_id": "whole",
            },
            {
                "site": "Demo",
                "depth_interval": "whole",
                "interpretation_model": "ICS",
                "parameter": "alpha",
                "apparent_estimate": 1.04e-6,
                "support_id": "whole",
            },
        ]
    ).to_csv(input_csv, index=False)

    result = run_interval_mode(input_csv, output_csv, root=root)

    expected_columns = {
        "site",
        "depth_interval",
        "interpretation_model",
        "parameter",
        "apparent_estimate",
        "corrected_median",
        "interval_p05",
        "interval_p95",
        "correction_factor_p50",
        "correction_factor_p05",
        "correction_factor_p95",
        "reliability_class",
        "design_reference_factor",
        "warning_flag",
        "calibration_source",
        "calibration_domain",
        "calibration_version",
        "mesh_gate_status",
        "numerical_stability_status",
    }
    assert expected_columns.issubset(result.columns)
    assert output_csv.exists()
    assert not any(column.startswith("true_") for column in result.columns)
    assert result["interval_p05"].notna().all()
    assert result["interval_p95"].notna().all()
    assert (result["interval_p95"] >= result["interval_p05"]).all()
    assert (result["design_reference_factor"] >= 1.0).all()
    assert set(result["interpretation_model"]) == {"ICS"}
    assert result["calibration_source"].str.len().gt(0).all()
    assert result["calibration_domain"].isin(["full_3d", "full_3d_production"]).all()
    assert result["calibration_version"].str.len().gt(0).all()


def test_interval_mode_cli_runs_on_example_file(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    example = root / "examples" / "example_fitted_results.csv"
    output_csv = tmp_path / "cli_intervals.csv"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "trust_tc",
            "interval",
            "--input",
            str(example),
            "--output",
            str(output_csv),
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    out = pd.read_csv(output_csv)
    assert len(out) >= 3
    assert "true_lambda" not in out.columns
    assert "design_reference_factor" in out.columns
    assert "calibration_source" in out.columns


def test_interval_mode_uses_packaged_calibration_without_project_outputs(tmp_path: Path) -> None:
    input_csv = tmp_path / "external_results.csv"
    output_csv = tmp_path / "external_intervals.csv"

    pd.DataFrame(
        [
            {
                "site": "External",
                "depth_interval": "whole",
                "interpretation_model": "ICS",
                "parameter": "lambda",
                "apparent_estimate": 2.5,
            }
        ]
    ).to_csv(input_csv, index=False)

    result = run_interval_mode(input_csv, output_csv, root=tmp_path)

    assert output_csv.exists()
    assert result.loc[0, "interval_p05"] > 0
    assert result.loc[0, "calibration_source"].endswith("full3d_production_correction_factor_distribution.csv")
    assert result.loc[0, "calibration_domain"] == "full_3d_production"


def test_interval_mode_accepts_aliases_and_custom_calibration(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    input_csv = tmp_path / "alias_results.csv"
    output_csv = tmp_path / "alias_intervals.csv"
    custom_calibration = tmp_path / "custom_calibration.csv"
    pd.DataFrame(
        [
            {
                "pathway_id": "A2",
                "calibration_domain": "full_3d_production",
                "p05_factor_lambda": 0.8,
                "p50_factor_lambda": 0.9,
                "p95_factor_lambda": 1.1,
                "p05_factor_C": 0.85,
                "p50_factor_C": 1.0,
                "p95_factor_C": 1.15,
                "recommended_reliability_class_candidate": "B",
            },
            {
                "pathway_id": "A3",
                "calibration_domain": "full_3d_production",
                "p05_factor_lambda": 0.75,
                "p50_factor_lambda": 0.95,
                "p95_factor_lambda": 1.2,
                "p05_factor_C": 0.8,
                "p50_factor_C": 1.0,
                "p95_factor_C": 1.25,
                "recommended_reliability_class_candidate": "C",
            },
        ]
    ).to_csv(custom_calibration, index=False)

    pd.DataFrame(
        [
            {
                "site": "Alias",
                "depth_interval": "whole",
                "interpretation_model": "cylindrical source",
                "parameter": "thermal_conductivity",
                "apparent_estimate": 2.5,
                "support_id": "whole",
            },
            {
                "site": "Alias",
                "depth_interval": "whole",
                "interpretation_model": "finite line source",
                "parameter": "thermal_diffusivity",
                "apparent_estimate": 1.1e-6,
                "support_id": "whole",
            },
        ]
    ).to_csv(input_csv, index=False)

    result = run_interval_mode(input_csv, output_csv, root=root, calibration_csv=custom_calibration)

    assert result["interpretation_model"].tolist() == ["ICS", "FLS"]
    assert result["parameter"].tolist() == ["lambda", "alpha"]
    assert result["calibration_source"].str.endswith("custom_calibration.csv").all()
    assert result["interval_p05"].notna().all()


def test_interval_mode_flags_missing_apparent_estimate(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    input_csv = tmp_path / "missing_value.csv"
    output_csv = tmp_path / "missing_value_intervals.csv"

    pd.DataFrame(
        [
            {
                "site": "Demo",
                "depth_interval": "whole",
                "interpretation_model": "LT-ILS",
                "parameter": "lambda",
                "apparent_estimate": "",
                "support_id": "whole",
            }
        ]
    ).to_csv(input_csv, index=False)

    result = run_interval_mode(input_csv, output_csv, root=root)

    assert result.loc[0, "warning_flag"] == "missing_apparent_estimate"
    assert pd.isna(result.loc[0, "corrected_median"])


def test_interval_mode_rejects_unknown_model_and_missing_calibration(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    input_csv = tmp_path / "bad_model.csv"
    output_csv = tmp_path / "bad_model_intervals.csv"

    pd.DataFrame(
        [
            {
                "site": "Demo",
                "depth_interval": "whole",
                "interpretation_model": "unsupported model",
                "parameter": "lambda",
                "apparent_estimate": 2.5,
            }
        ]
    ).to_csv(input_csv, index=False)

    with pytest.raises(ValueError, match="unsupported_model"):
        run_interval_mode(input_csv, output_csv, root=root)

    good_input = tmp_path / "good.csv"
    pd.DataFrame(
        [
            {
                "site": "Demo",
                "depth_interval": "whole",
                "interpretation_model": "ILS",
                "parameter": "lambda",
                "apparent_estimate": 2.5,
            }
        ]
    ).to_csv(good_input, index=False)

    with pytest.raises(FileNotFoundError, match="Calibration table not found"):
        run_interval_mode(good_input, output_csv, root=root, calibration_csv=tmp_path / "missing.csv")
