# TRUST-TC

TRUST-TC is an MIT-licensed research tool for transformation uncertainty
analysis in thermal response test (TRT) interpretation. It converts apparent
TRT estimates of thermal conductivity, volumetric heat capacity, and thermal
diffusivity into uncertainty intervals, reliability classes, and geothermal
design reference factors.

This public repository contains only the software, calibration table,
documentation, tests, and small CSV examples needed to run the interval
analysis tool. It does not include raw field data.

## Install

Editable install:

```powershell
python -m pip install -e .
trust-tc --help
```

Repository-local execution without installing:

```powershell
$env:PYTHONPATH=(Resolve-Path .\src)
python -m trust_tc --help
```

## Quick Start

Run the stable mode for existing TRT results:

```powershell
python -m trust_tc interval --input examples/example_fitted_results.csv --output outputs/tool_demo/intervals.csv --calibration-domain full_3d_production
```

The command reads apparent TRT estimates and writes corrected medians,
P05--P95 uncertainty intervals, reliability classes, design reference factors,
warning flags, and calibration provenance.

Use a custom calibration table when needed:

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

## Input Models

The public model names are:

- `LT-ILS`: late time infinite line source approximation.
- `ILS`: exact infinite line source solution.
- `ICS`: infinite cylindrical source or finite radius solution.
- `FLS`: finite line source solution.

Common aliases such as `late time ILS`, `exact ILS`, `cylindrical source`, and
`finite line source` are accepted.

## Scope

The stable release is version `0.1.0`. The existing-result mode is stable and
is designed for users who already have apparent TRT estimates from common
interpretation models. Direct fitting from raw temperature time series is not
part of this public release.

TRUST-TC reports design estimates with uncertainty intervals. It does not
estimate true field thermal properties from field data. The bundled calibration
table comes from prescribed-property full 3D numerical benchmark cases.

## Documentation

- `docs/tool_usage.md`: commands and example runs.
- `docs/input_schema.md`: required and optional input columns.
- `docs/output_schema.md`: output columns and warning flags.
- `docs/software_architecture.md`: package layers and calibration interface.
- `docs/examples.md`: example files and expected outputs.
- `docs/reproducibility.md`: commands used to reproduce the software examples.

## Citation

Please cite the software record in `CITATION.cff`. A Zenodo DOI can be minted
from the GitHub `v0.1.0` release. The package is released under the MIT license.

## Public Data Boundary

The public software release includes processed CSV examples and the calibrated
full 3D correction factor table required by interval mode. It does not include
restricted raw field files under `data/raw/`. Example field-like rows are
provided only as interval analysis demonstrations.
