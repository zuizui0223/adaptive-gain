import math

import pytest

from adaptive_gain.frame_preserving_tracking import (
    FrameTrack,
    TrackPoint,
    euclidean_distance,
    event_time_seconds,
    first_active_zone_entry_frame,
    link_frame_detections,
)


def test_horizontal_motion_is_real_euclidean_motion():
    a = TrackPoint(0, 0.0, 5.0)
    b = TrackPoint(1, 3.0, 5.0)
    assert euclidean_distance(a, b) == pytest.approx(3.0)


def test_empty_frame_does_not_compress_absolute_time():
    frames = [
        [(0.0, 0.0)],
        [],
        [(1.0, 0.0)],
    ]
    tracks = link_frame_detections(
        frames,
        max_speed_px_per_frame=1.0,
        max_frame_gap=2,
    )

    assert len(tracks) == 1
    assert [p.frame for p in tracks[0].points] == [0, 2]
    assert event_time_seconds(2, frame_rate_hz=10.0) == pytest.approx(0.2)


def test_detection_is_assigned_to_at_most_one_track():
    frames = [
        [(0.0, 0.0), (2.0, 0.0)],
        [(1.0, 0.0)],
    ]
    tracks = link_frame_detections(
        frames,
        max_speed_px_per_frame=2.0,
        max_frame_gap=1,
    )

    points_at_frame_one = [
        p
        for track in tracks
        for p in track.points
        if p.frame == 1
    ]
    assert len(points_at_frame_one) == 1


def test_tracks_surviving_final_frame_are_retained():
    frames = [
        [(0.0, 0.0), (10.0, 0.0)],
        [(0.5, 0.0), (10.5, 0.0)],
        [(1.0, 0.0), (11.0, 0.0)],
    ]
    tracks = link_frame_detections(
        frames,
        max_speed_px_per_frame=2.0,
    )

    assert len(tracks) == 2
    assert sorted(track.last_frame for track in tracks) == [2, 2]
    assert sorted(len(track.points) for track in tracks) == [3, 3]


def test_first_active_zone_entry_uses_true_frame_gap_and_2d_speed():
    track = FrameTrack(
        0,
        [
            TrackPoint(0, 0.0, 0.0),
            TrackPoint(2, 4.0, 0.0),
            TrackPoint(3, 5.0, 0.0),
        ],
    )
    polygon = (
        (3.0, -1.0),
        (6.0, -1.0),
        (6.0, 1.0),
        (3.0, 1.0),
    )

    event = first_active_zone_entry_frame(
        track,
        polygon,
        min_speed_px_per_frame=1.5,
    )

    # Frame 2 is inside the zone and moved 4 px over two real frames = 2 px/frame.
    assert event == 2


def test_no_event_returns_infinite_time():
    assert math.isinf(event_time_seconds(None, frame_rate_hz=10.0))
