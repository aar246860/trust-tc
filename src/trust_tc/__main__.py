from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .open_tool import run_interval_mode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="trust-tc")
    parser.add_argument("--version", action="version", version=f"trust-tc {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    interval = subparsers.add_parser(
        "interval",
        help="Convert existing apparent TRT estimates into uncertainty intervals.",
    )
    interval.add_argument("--input", required=True, help="Input CSV with apparent TRT estimates.")
    interval.add_argument("--output", required=True, help="Output CSV for uncertainty intervals.")
    interval.add_argument(
        "--calibration",
        default=None,
        help="Optional calibration summary CSV. Defaults to TRUST-TC outputs.",
    )
    interval.add_argument(
        "--calibration-domain",
        default="full_3d_production",
        help="Calibration domain label for traceability. The bundled default is full_3d_production.",
    )

    args = parser.parse_args(argv)
    if args.command == "interval":
        result = run_interval_mode(
            Path(args.input),
            Path(args.output),
            root=Path.cwd(),
            calibration_csv=Path(args.calibration) if args.calibration else None,
            calibration_domain=args.calibration_domain,
        )
        print(f"Wrote {len(result)} interval estimates to {args.output}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
