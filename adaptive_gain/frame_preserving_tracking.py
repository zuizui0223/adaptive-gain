"""Frame-preserving trajectory utilities for public Aedes video reanalysis.

This module is deliberately small and dependency-free. It is not presented as a
general state-of-the-art multi-object tracker. Its purpose is to make the
latency-specific invariants explicit:

- original frame indices are never compressed;
- motion uses Euclidean XY displacement;
- a detection is assigned to at most one track per frame;
- tracks surviving to the final frame are retained.

Matching uses deterministic greedy one-to-one assignment over all eligible
track/detection pairs. For publication-grade raw-video analysis, assignment
sensitivity should be checked against hand annotations and, where useful, a
global assignment implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Sequence


@dataclass(frozen=True)
class TrackPoint:
    frame: int
    x: float
    y: float


@dataclass
class FrameTrack:
    track_id: int
    points: list[TrackPoint]

    @property
    def first_frame(self) -> int:
        return self.points[0].frame

    @property
    def last_frame(self) -> int:
        return self.points[-1].frame


def euclidean_distance(a: TrackPoint, b: TrackPoint) -> float:
    return math.hypot(b.x - a.x, b.y - a.y)


def _validate_detection(x: float, y: float) -> tuple[float, float]:
    x = float(x)
    y = float(y)
    if not math.isfinite(x) or not math.isfinite(y):
        raise ValueError("detection coordinates must be finite")
    return x, y


def link_frame_detections(
    detections_by_frame: Sequence[Sequence[tuple[float, float]]],
    *,
    max_speed_px_per_frame: float,
    max_frame_gap: int = 1,
) -> tuple[FrameTrack, ...]:
    """Link detections while preserving original frame numbers.

    Eligible track/detection pairs are sorted by Euclidean distance and assigned
    greedily with one-to-one constraints. A gap of g frames permits a
    Euclidean displacement up to max_speed_px_per_frame * g.
    """
    if not math.isfinite(max_speed_px_per_frame) or max_speed_px_per_frame <= 0:
        raise ValueError("max_speed_px_per_frame must be finite and positive")
    if type(max_frame_gap) is not int or max_frame_gap < 1:
        raise ValueError("max_frame_gap must be a positive integer")

    tracks: list[FrameTrack] = []
    active_ids: set[int] = set()
    next_id = 0

    for frame, raw_detections in enumerate(detections_by_frame):
        detections = [_validate_detection(x, y) for x, y in raw_detections]

        active_ids = {
            tid
            for tid in active_ids
            if frame - tracks[tid].last_frame <= max_frame_gap
        }

        candidates: list[tuple[float, int, int]] = []
        for tid in sorted(active_ids):
            last = tracks[tid].points[-1]
            gap = frame - last.frame
            if gap <= 0:
                continue
            limit = max_speed_px_per_frame * gap
            for det_index, (x, y) in enumerate(detections):
                point = TrackPoint(frame, x, y)
                distance = euclidean_distance(last, point)
                if distance <= limit:
                    candidates.append((distance, tid, det_index))

        candidates.sort(key=lambda row: (row[0], row[1], row[2]))
        assigned_tracks: set[int] = set()
        assigned_detections: set[int] = set()

        for _, tid, det_index in candidates:
            if tid in assigned_tracks or det_index in assigned_detections:
                continue
            x, y = detections[det_index]
            tracks[tid].points.append(TrackPoint(frame, x, y))
            assigned_tracks.add(tid)
            assigned_detections.add(det_index)

        for det_index, (x, y) in enumerate(detections):
            if det_index in assigned_detections:
                continue
            tracks.append(
                FrameTrack(
                    track_id=next_id,
                    points=[TrackPoint(frame, x, y)],
                )
            )
            active_ids.add(next_id)
            next_id += 1

        active_ids.update(assigned_tracks)

    return tuple(tracks)


def point_in_polygon(
    x: float,
    y: float,
    polygon: Sequence[tuple[float, float]],
) -> bool:
    """Ray-casting point-in-polygon test."""
    if len(polygon) < 3:
        raise ValueError("polygon requires at least three vertices")

    inside = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        intersects = (
            (yi > y) != (yj > y)
            and x
            < (xj - xi) * (y - yi) / ((yj - yi) or 1e-300) + xi
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def first_active_zone_entry_frame(
    track: FrameTrack,
    polygon: Sequence[tuple[float, float]],
    *,
    min_speed_px_per_frame: float = 0.0,
) -> int | None:
    """Return first zone-entry frame with sufficient Euclidean movement."""
    if not math.isfinite(min_speed_px_per_frame) or min_speed_px_per_frame < 0:
        raise ValueError("min_speed_px_per_frame must be finite and nonnegative")

    for prev, current in zip(track.points, track.points[1:]):
        frame_gap = current.frame - prev.frame
        if frame_gap <= 0:
            raise ValueError("track frames must be strictly increasing")
        speed = euclidean_distance(prev, current) / frame_gap
        if (
            speed >= min_speed_px_per_frame
            and point_in_polygon(current.x, current.y, polygon)
        ):
            return current.frame
    return None


def event_time_seconds(frame: int | None, *, frame_rate_hz: float) -> float:
    """Convert a frame index to seconds, using infinity for no observed event."""
    if not math.isfinite(frame_rate_hz) or frame_rate_hz <= 0:
        raise ValueError("frame_rate_hz must be finite and positive")
    if frame is None:
        return math.inf
    if type(frame) is not int or frame < 0:
        raise ValueError("frame must be a nonnegative integer or None")
    return frame / frame_rate_hz


def track_event_times_seconds(
    tracks: Iterable[FrameTrack],
    polygon: Sequence[tuple[float, float]],
    *,
    frame_rate_hz: float,
    min_speed_px_per_frame: float = 0.0,
) -> tuple[float, ...]:
    return tuple(
        event_time_seconds(
            first_active_zone_entry_frame(
                track,
                polygon,
                min_speed_px_per_frame=min_speed_px_per_frame,
            ),
            frame_rate_hz=frame_rate_hz,
        )
        for track in tracks
    )
