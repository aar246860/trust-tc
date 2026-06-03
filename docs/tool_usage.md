# TRUST-TC Tool Usage

TRUST-TC converts apparent thermal response test (TRT) estimates into
interpretation conditioned uncertainty intervals using the bundled full 3D
calibration table.

## Install or run locally

Editable install:

```powershell
python -m pip install -e .
trust-tc --help
```

Repository-local execution:

```powershell
$env:PYTHONPATH=(Resolve-Path .\src)
python -m trust_tc --help
```

## Existing-result mode

Use this mode when a TRT has already been interpreted by a conventional model.

```powershell
$env:PYTHONPATH=(Resolve-Path .\src)
python -m trust_tc interval --input examples/example_fitted_results.csv --output outputs/tool_demo/intervals.csv --calibration-domain full_3d_production
```

The command writes apparent estimates, corrected medians, P05--P95 intervals,
reliability class, design reference factor, warning flag, and calibration
provenance.

The equivalent installed command is:

```powershell
trust-tc interval --input examples/example_fitted_results.csv --output outputs/tool_demo/intervals.csv --calibration-domain full_3d_production
```

Use a custom calibration table:

```powershell
python -m trust_tc interval `
  --input examples/example_fitted_results.csv `
  --output outputs/tool_demo/custom_intervals.csv `
  --calibration src/trust_tc/calibration/full3d_production_correction_factor_distribution.csv `
  --calibration-domain full_3d_production
```

## Python API

```python
from trust_tc import run_interval_mode

run_interval_mode(
    "examples/example_fitted_results.csv",
    "outputs/tool_demo/intervals.csv",
    calibration_domain="full_3d_production",
)
```

The stable public API is:

```python
trust_tc.run_interval_mode(input_csv, output_csv, root=None, calibration_csv=None, calibration_domain="full_3d_production")
```

## Time-series fitting

Direct fitting from raw temperature time series is not part of this public
release. The stable release accepts existing fitted TRT estimates and converts
them into interval estimates.
