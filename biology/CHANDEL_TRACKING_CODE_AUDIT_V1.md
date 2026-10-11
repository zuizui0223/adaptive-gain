# Chandel et al. public tracking-code audit for Phase A

Status: external-code audit for the proposed Aedes public-data latency reanalysis. This note does not challenge the published biological conclusion. It identifies code-level issues that matter specifically if the public pipeline is reused to estimate time-to-event distributions.

## Source frozen for this audit

Repository:

- \`Craig-Montell-Lab/Chandel_DeBeaubien_2023\`
- latest repository commit inspected: \`f027ebc229bee60d952240ccdc0887cf213b169d\`
- focal files:
  - \`Aedes_track/MosquitoTrackerExpressv1.m\`
  - \`Aedes_track/TrackFinderv2.m\`
  - \`Aedes_track/stat_remover.m\`

The Nature paper and Dryad record state that Aedes videos were recorded at 10 FPS for 300 s and that the custom tracking code was used to quantify actively host-seeking mosquitoes.

## 1. Useful properties for the proposed latency analysis

\`MosquitoTrackerExpressv1.m\` explicitly sets

\`\`\`matlab
FR = 10;
start_time = 0;
end_time = 300;
\`\`\`

and retains framewise detections in \`cords\`.

It also calls \`TrackFinderv2\` and saves the entire MATLAB workspace to the output MAT file with

\`\`\`matlab
save(outpath);
\`\`\`

rather than saving only the final PI/HSI summaries.

This means the public workflow contains enough intermediate structure to support a time-resolved reanalysis in principle.

## 2. Code-level anomaly A — stationary filtering uses Y displacement twice

In \`stat_remover.m\`, the active-motion filter currently contains

\`\`\`matlab
d1 = (diff(points(:,2))).^2;
d2 = (diff(points(:,2))).^2;
fin_dis = (d1 + d2).^0.5;
\`\`\`

Both components use column 2.

If the intended quantity was Euclidean XY displacement, the first component would normally use column 1.

As written,

\[
d_{\rm code}
=
\sqrt{2}\,|\Delta y|,
\]

rather than

\[
d_{\rm euclid}
=
\sqrt{(\Delta x)^2+(\Delta y)^2}.
\]

Consequences for a latency reanalysis:

- horizontal movement with little Y displacement can fall below the movement threshold;
- movement classification can depend on track orientation relative to the camera;
- first-active-host-seeking time inferred from the already-filtered \`final_pts\` may therefore differ from a true 2D movement criterion.

This is a code-level observation only. Its material effect on the published PI/HSI values has not been quantified here.

## 3. Code-level anomaly B — final surviving-track loop uses length(wind)

In \`TrackFinderv2.m\`, \`wind\` is constructed as a scalar:

\`\`\`matlab
wind = round(max(big)*1.02);
\`\`\`

but the final append loop is

\`\`\`matlab
for ii = 1:length(wind)
    track_set{tick} = [[trax_X{:,ii}]',[trax_Y{:,ii}]'];
    tick = tick+1;
end
\`\`\`

For an ordinary scalar MATLAB value,

\[
\operatorname{length}(wind)=1.
\]

Thus this loop appends only the first still-active trajectory at the end of the recording, rather than iterating through the allocated/current trajectory columns.

Tracks that terminated earlier are appended elsewhere when their continuation fails, so the potential omission concerns trajectories still alive at the final frame.

Again, this is a code-level observation. The number of affected tracks and effect on published summaries require empirical reproduction.

## 4. Why these issues matter more for latency than for the original aggregate analysis

The original paper used aggregate PI/HSI summaries over a five-minute assay.

The proposed adaptive-gain Phase A asks a different question:

\[
F_j(t)=P(T_j\le t).
\]

Time-to-first-event and early-tail estimates are more sensitive to:

- exactly when a track begins and ends;
- whether movement is classified active at each frame;
- whether final surviving tracks are retained;
- whether time indices are preserved through filtering.

Therefore the public code should not simply be rerun unchanged and treated as an independent latency extractor.

## 5. Phase A reanalysis rule

Use one of two defensible routes.

### Route A — raw-video reprocessing

Reprocess a frozen subset of raw videos with a corrected and independently validated tracker that:

- retains original frame indices;
- uses 2D displacement;
- retains all trajectories alive at the final frame;
- uses one-to-one assignment or explicitly audits duplicate nearest-neighbour assignments;
- freezes segmentation and motion thresholds before comparing cue conditions.

This is the strongest route.

### Route B — source-data time-course analysis

If the Nature Source Data provide per-timepoint IHSI or comparable time-resolved summaries for the focal experiment, estimate a population-level response curve directly from those source values.

This route does not recover individual completion-time distributions and must not be labelled as such.

## 6. Do not use final_pts as a latency dataset without reconstruction

\`final_pts\` concatenates filtered coordinates across trajectories and does not retain an explicit frame-time index.

It is suitable for spatial aggregate calculations such as zone counts, but not by itself for reconstructing

\[
T=\text{first qualifying active event time}.
\]

A latency analysis therefore needs frame-indexed detections or trajectories.

## 7. Additional tracking issue to audit before full reanalysis

\`TrackFinderv2.m\` assigns each previous point to its nearest point in the next frame using \`knnsearch\`.

The shown code does not visibly enforce a one-to-one assignment constraint before writing the next positions. Two previous tracks can therefore in principle select the same next detection.

Before using this logic for individual survival/latency distributions, quantify how often such collisions occur in representative videos.

## 8. Claim boundary

The audit licenses the following statement:

> The public archive is rich enough for a prospective time-resolved reanalysis, but the published MATLAB pipeline should not be treated as a ready-made individual latency extractor without correction and validation.

It does not license:

- a claim that the published PI/HSI results are wrong;
- a quantified bias estimate;
- an individual-level latency result before raw data are reprocessed;
- a fitness claim from the public host-seeking assay alone.
