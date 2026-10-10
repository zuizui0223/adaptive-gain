# V-HOST 2026 tracking-code audit for latency reuse

Status: external-code audit for potential raw-video reprocessing of the Chandel et al. host-seeking archive.

Repository:

- `Craig-Montell-Lab/V-HOST_DeBeaubien_etal_2025`
- associated 2026 Nature Protocols V-HOST workflow;
- focal files: `mosquitoTracker.m`, `trackFinder.m`, `statRemover.m`.

This audit asks a narrow question: can the newer V-HOST code be used unchanged to reconstruct individual time-to-event distributions for the opportunity-fitness analysis?

Answer: **not unchanged**.

## 1. One 2024 tracking defect is repaired

The older `TrackFinderv2.m` ended with

```matlab
for ii = 1:length(wind)
```

even though `wind` is scalar, so only one surviving end-of-recording track could be appended.

The V-HOST `trackFinder.m` now uses

```matlab
for ii = 1:wind
```

and therefore iterates across the allocated surviving-track columns.

For the specific end-of-recording survivor issue, the newer code is an improvement.

## 2. The stationary-motion coordinate bug persists

The newer `statRemover.m` still contains

```matlab
d1 = (diff(points(:,2))).^2;
d2 = (diff(points(:,2))).^2;
fin_dis = (d1 + d2).^0.5;
```

Both displacement components use the second coordinate.

Thus the movement score remains

[
sqrt{2}|Delta y|
]

rather than the usual two-dimensional Euclidean displacement

[
sqrt{(Delta x)^2+(Delta y)^2}.
]

A horizontal movement can therefore contribute no movement under this filter.

The issue is present in both the inspected 2024 and 2026 code bases.

This is a code-level observation; its quantitative effect on published aggregate indices is not established here.

## 3. Absolute frame time is lost inside trackFinder after any empty frame

At the start of `trackFinder.m`:

```matlab
remove_blanks = ~cellfun('isempty', cords(:,:));
cords = cords(remove_blanks);
```

`cords` originates in `mosquitoTracker.m` as one cell per original video frame.

Removing empty cells before trajectory reconstruction compresses the frame axis.

If every original frame contains at least one accepted detection, this does not matter.

But if any frame is empty, then after compression:

[
	ext{trajectory row index}

eq
	ext{original video frame index}.
]

Consequently a trajectory reconstructed from `track_set` does not, by itself, preserve exact absolute event time after an empty frame.

This is especially important for the present analysis because the target quantity is a completion/event-time distribution, not only aggregate spatial occupancy.

## 4. Track_set still stores coordinates without explicit frame identifiers

The newer code stores each completed track as

```matlab
[[trax_X{:, index}]', [trax_Y{:, index}]']
```

so each row contains only X and Y.

There is no explicit original frame number or timestamp attached to each coordinate.

Therefore even where a track is internally ordered, missing frames and later compression cannot be reconstructed from `track_set` alone.

The full saved MAT workspace retains the original `cords`, which is better for a latency reanalysis.

## 5. Nearest-neighbour matching is still not visibly one-to-one

The newer `trackFinder.m` continues to use

```matlab
[findspot, distance] = knnsearch(query, previous_positions);
```

for each prior track.

The shown code does not enforce a global one-to-one assignment between previous tracks and next-frame detections before writing matched positions.

Two previous tracks can in principle select the same next detection.

For aggregate occupancy this may have limited practical effect depending on track density and the speed threshold. For individual time-to-event distributions it must be audited.

## 6. Distance summary is also not standard Euclidean path length

The newer `trackFinder.m` calculates

```matlab
Dif_dat(2:length(XY), i) = sqrt(sum(abs(diff(XY)), 2));
```

For a displacement ((Delta x,Delta y)), this is

[
sqrt{|Delta x|+|Delta y|},
]

not

[
sqrt{(Delta x)^2+(Delta y)^2}.
]

This does not directly affect the proposed first-event time if distance is not used in its definition, but it reinforces the need not to treat all saved movement summaries as standard physical distances.

## 7. Recommended corrected latency pipeline

For the opportunity-fitness reanalysis, use the raw frame-indexed detections rather than `final_pts` or unmodified `track_set`.

Minimum requirements:

1. preserve one record for every original video frame;
2. retain the original frame index on every detection and trajectory point;
3. use true two-dimensional displacement for movement filtering;
4. use a one-to-one assignment rule between consecutive frames, or explicitly quantify assignment collisions;
5. retain all tracks present at the final frame;
6. define the focal event prospectively from zone entry / sustained active movement;
7. encode no qualifying event by the end of 300 s as right censoring for survival analysis, or as (T=infty) for finite-window timely-success calculations;
8. validate the rewritten tracker against hand-annotated frames before treatment comparisons.

## 8. What can be reused safely from V-HOST

The newer repository remains useful as a reference implementation for:

- video loading;
- image segmentation;
- zone definition;
- experiment logging;
- representative images/videos;
- the corrected end-of-recording survivor loop.

But the timing analysis should use a dedicated corrected trajectory layer.

## 9. Claim boundary

The 2026 V-HOST release does not remove all code-level obstacles to individual-latency reconstruction.

The appropriate statement is:

> V-HOST improves the original tracking workflow and repairs the final surviving-track loop, but its stationary-motion calculation still uses the Y coordinate twice and its trajectory representation can lose absolute frame timing after empty detection frames. Individual time-to-event analysis therefore requires a corrected frame-preserving tracker.

This audit does not claim that the published V-HOST aggregate activity/preference results are invalid.
