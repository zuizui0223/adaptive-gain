"""Extract individual first-probe latencies from Uehara-style frame XLSX.

The public analysis notebook for Uehara et al. 2026 treats each XLSX column as
one individual framewise behavior sequence, uses 60 fps, and counts behavior
code 2 as probing. The canonical post-BF window starts at frame 3600 and spans
28800 frames.

This helper does not infer experimental condition labels. It simply converts
one or more compatible XLSX files into individual latency rows.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def first_code_frame(
    values: list[object],
    *,
    code: int,
    start_frame: int,
    end_frame: int,
) -> int | None:
    if start_frame < 0 or end_frame <= start_frame:
        raise ValueError("invalid frame window")
    stop = min(end_frame, len(values))
    for frame in range(start_frame, stop):
        value = values[frame]
        try:
            numeric = int(value)
        except (TypeError, ValueError):
            continue
        if numeric == code:
            return frame
    return None


def extract_workbook(
    path: Path,
    *,
    fps: float = 60.0,
    start_frame: int = 3600,
    end_frame: int = 32400,
    probe_code: int = 2,
) -> list[dict[str, object]]:
    if not math.isfinite(fps) or fps <= 0:
        raise ValueError("fps must be finite and positive")

    try:
        from openpyxl import load_workbook
    except ImportError as exc:
        raise RuntimeError(
            "openpyxl is required for XLSX latency extraction"
        ) from exc

    workbook = load_workbook(path, data_only=True, read_only=True)
    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        return []

    # The notebook reads the files with pandas and iterates over columns. Use
    # the first row as headers when it contains labels; otherwise synthesize
    # stable column names.
    header = list(rows[0])
    data_rows = rows[1:]

    width = max((len(row) for row in rows), default=0)
    results: list[dict[str, object]] = []
    for column in range(width):
        label = (
            str(header[column])
            if column < len(header) and header[column] not in (None, "")
            else f"animal_{column}"
        )
        values = [
            row[column] if column < len(row) else None
            for row in data_rows
        ]
        frame = first_code_frame(
            values,
            code=probe_code,
            start_frame=start_frame,
            end_frame=end_frame,
        )
        if frame is None:
            latency = math.inf
            status = "no_probe_in_window"
        else:
            latency = (frame - start_frame) / fps
            status = "observed_probe"
        results.append(
            {
                "source_file": path.name,
                "animal": label,
                "first_probe_frame": "" if frame is None else frame,
                "latency_s": "inf" if math.isinf(latency) else latency,
                "status": status,
                "fps": fps,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "probe_code": probe_code,
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--fps", type=float, default=60.0)
    parser.add_argument("--start-frame", type=int, default=3600)
    parser.add_argument("--end-frame", type=int, default=32400)
    parser.add_argument("--probe-code", type=int, default=2)
    args = parser.parse_args()

    all_rows = []
    for path in args.inputs:
        all_rows.extend(
            extract_workbook(
                path,
                fps=args.fps,
                start_frame=args.start_frame,
                end_frame=args.end_frame,
                probe_code=args.probe_code,
            )
        )

    fieldnames = [
        "source_file",
        "animal",
        "first_probe_frame",
        "latency_s",
        "status",
        "fps",
        "start_frame",
        "end_frame",
        "probe_code",
    ]
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)


if __name__ == "__main__":
    main()
