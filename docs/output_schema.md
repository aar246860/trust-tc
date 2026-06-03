# TRUST-TC Interval Output Schema

Output columns:

- `site`
- `depth_interval`
- `interpretation_model`
- `parameter`
- `apparent_estimate`
- `corrected_median`
- `interval_p05`
- `interval_p95`
- `correction_factor_p50`
- `correction_factor_p05`
- `correction_factor_p95`
- `reliability_class`
- `design_reference_factor`
- `warning_flag`
- `calibration_source`
- `calibration_domain`
- `calibration_version`

For thermal conductivity, the design reference factor is based on the lower
conductivity interval endpoint because required borehole length scales
approximately with \(1/\lambda\). For heat capacity and diffusivity, the factor
summarizes interval spread and should be treated as a reporting aid rather than
a direct borehole-length factor.

## Warning flags

- `outside_calibration_domain`: no calibrated factors are available for the
  requested model.
- `parameter_not_identifiable`: the calibrated table does not support an
  interval for the requested parameter.
- `missing_apparent_estimate`: the input row lacks a numeric apparent estimate.
- `unsupported_model`: raised as an error for unsupported interpretation names.
- `unsupported_parameter`: raised as an error for unsupported parameter names.

## Provenance columns

`calibration_source`, `calibration_domain`, and `calibration_version` record
which transformation uncertainty table generated the interval. These fields
allow the same input table to be rerun against future calibration releases.
