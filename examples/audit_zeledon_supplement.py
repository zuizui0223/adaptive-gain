#!/usr/bin/env python3
"""Fetch and audit the Zeledon 2024 chemistry supplement through NCBI PMC-SM-BioC."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from adaptive_gain.zeledon_supplement import (
    audit_bioc_xml,
    live_audit,
    receipt_json,
    supplement_url,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--xml",
        type=Path,
        help="Audit a previously downloaded BioC XML file instead of making a live request.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Timeout in seconds for the live NCBI request.",
    )
    args = parser.parse_args()

    if args.xml:
        xml_text = args.xml.read_text(encoding="utf-8")
        receipt = audit_bioc_xml(xml_text, source_url=str(args.xml))
    else:
        try:
            receipt = live_audit(timeout=args.timeout)
        except Exception as exc:  # operational CLI should surface retrieval failure cleanly
            print(f"RETRIEVAL_FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
            print(f"Canonical URL: {supplement_url()}", file=sys.stderr)
            return 2

    print(receipt_json(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
