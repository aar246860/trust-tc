# Reproducibility

These commands reproduce the public TRUST-TC interval tool examples from a
local checkout.

```powershell
$env:PYTHONPATH=(Resolve-Path .\src)
python -m trust_tc --help
python -m trust_tc interval --input examples/example_fitted_results.csv --output outputs/tool_demo/intervals.csv
python -m trust_tc interval --input examples/ntu_tool_demo.csv --output outputs/tool_demo/ntu_intervals.csv
python -m trust_tc interval --input examples/fukuoka_tool_demo.csv --output outputs/tool_demo/fukuoka_intervals.csv
python -m trust_tc interval --input examples/two_site_demo.csv --output outputs/tool_demo/two_site_intervals.csv
python -m pytest tests/test_tool_interval_mode.py -q
```

The generated CSV files report corrected medians, P05--P95 intervals,
reliability classes, design reference factors, warning flags, and calibration
provenance. No output column is named `true_lambda`, `true_C`, `true_alpha`, or
`field_truth`.
