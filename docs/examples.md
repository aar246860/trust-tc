# TRUST-TC Examples

The repository contains small CSV examples for reviewer and user testing.

## Generic fitted-result example

Input:

```text
examples/example_fitted_results.csv
```

Command:

```powershell
python -m trust_tc interval --input examples/example_fitted_results.csv --output outputs/tool_demo/intervals.csv
```

## NTU field demonstration

Input:

```text
examples/ntu_tool_demo.csv
```

Command:

```powershell
python -m trust_tc interval --input examples/ntu_tool_demo.csv --output outputs/tool_demo/ntu_intervals.csv
```

## Fukuoka field demonstration

Input:

```text
examples/fukuoka_tool_demo.csv
```

Command:

```powershell
python -m trust_tc interval --input examples/fukuoka_tool_demo.csv --output outputs/tool_demo/fukuoka_intervals.csv
```

## Combined two-site demonstration

Input:

```text
examples/two_site_demo.csv
```

Command:

```powershell
python -m trust_tc interval --input examples/two_site_demo.csv --output outputs/tool_demo/two_site_intervals.csv
```

All example outputs include corrected medians, P05--P95 intervals, reliability
classes, design reference factors, warning flags, and calibration provenance.
