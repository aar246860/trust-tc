# TRUST-TC Software Architecture

TRUST-TC separates calibration data from the software interface. The package
loads calibrated transformation uncertainty factors and applies them to
user-supplied TRT estimates.

## Package layers

1. Input reader: reads existing apparent TRT estimates from CSV.
2. Name normalizer: maps model and parameter aliases to stable public names.
3. Calibration loader: loads the bundled or user-supplied transformation
   uncertainty table and records its provenance.
4. Interval engine: multiplies apparent estimates by calibrated correction
   factors to obtain corrected medians and P05--P95 intervals.
5. Design-factor reporter: computes a design reference factor for geothermal
   interpretation.
6. CSV writer: writes intervals, reliability classes, warning flags, and
   calibration provenance.

## Public interface

Distribution name: `trust-tc`

Python import name: `trust_tc`

Stable CLI:

```powershell
trust-tc interval --input INPUT.csv --output OUTPUT.csv
```

Stable Python API:

```python
trust_tc.run_interval_mode(input_csv, output_csv, root=None, calibration_csv=None)
```

## Calibration interface

The default calibration table is packaged with the library:

```text
src/trust_tc/calibration/full3d_production_correction_factor_distribution.csv
```

Users can supply a custom calibration file with `--calibration`. The output
always records the calibration source, domain, and version.

## Scope

Existing-result mode is stable for version `0.1.1`. Direct fitting from raw
temperature time series is not part of this public release.
