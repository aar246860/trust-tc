# TRUST-TC Existing-Result Input Schema

Required columns:

- `site`: site name.
- `depth_interval`: interpreted depth interval or `whole`.
- `interpretation_model`: `LT-ILS`, `ILS`, `ICS`, or `FLS`.
- `parameter`: `lambda`, `C`, or `alpha`.
- `apparent_estimate`: fitted apparent estimate from a TRT interpretation.

Optional columns:

- `support_id`: calibration depth category such as `shallow`, `middle`, `deep`,
  or `whole`.
- `reliability_class`: user supplied class if the field-data completeness has
  already been assessed.

The input table must not include prescribed field-property columns. TRUST-TC
calibrates uncertainty intervals from numerical benchmarks with prescribed
properties.

## Accepted interpretation aliases

- `LT-ILS`, `late-time ILS`, `late time ILS`
- `ILS`, `exact ILS`
- `ICS`, `cylindrical source`, `cylindrical`
- `FLS`, `finite line source`

Unsupported interpretation names raise `unsupported_model`.

## Accepted parameter aliases

- `lambda`, `conductivity`, `thermal_conductivity`
- `C`, `heat_capacity`, `volumetric_heat_capacity`
- `alpha`, `diffusivity`, `thermal_diffusivity`

Unsupported parameter names raise `unsupported_parameter`.

## Missing values

Rows with missing `apparent_estimate` are retained, but interval values are
reported as missing and `warning_flag` contains `missing_apparent_estimate`.
