# Chandel Figure 3a raw-video mapping blocker v1

Status: empirical gate receipt. This records why the public archive does not
currently license assignment of individual raw videos to Figure 3a.

## 1. What is available

The public Nature Source Data Figure 3 workbook contains the complete aggregate
Figure 3a time series:

- sheet: Figure 3a;
- 3,000 frames;
- 10 FPS;
- 300 s;
- aggregate mean IHSI across 18 trials.

The Dryad dataset also exposes a large archive:

- IR_vids.zip;
- approximately 31.64 GB;
- public legacy stream ID 3370964.

The aggregate Phase A analysis is therefore reproducible.

## 2. The missing mapping

The Dryad README states that exact video IDs used for figures are recorded in
the Source Data.

A workbook-level audit found IR_#### identifiers for other Figure 3 panels, but
the Figure 3a sheet itself contains no video IDs.

The Source Data workbook therefore does not provide a direct mapping from the
18 Figure 3a trials to individual members of IR_vids.zip.

Do not infer those 18 videos from neighboring numeric IDs, file order, or
unreferenced-ID complements without an independent mapping receipt.

## 3. Why the ZIP member list cannot currently be inspected cheaply

Two public download routes were probed from a GitHub runner.

### Dryad REST API download

The documented endpoint

https://datadryad.org/api/v2/files/3370964/download

returned HTTP 401 to the anonymous runner.

### Legacy public file stream

The endpoint

https://datadryad.org/downloads/file_stream/3370964

returned HTTP 200 but did not honor byte Range requests.

That matters because ZIP member names are stored in the central directory near
the end of the archive. Without Range access, reading that directory requires
streaming the approximately 31.64 GB archive rather than fetching only a small
tail segment.

The programme deliberately does not download the full archive merely to guess
the Figure 3a mapping.

## 4. Empirical claim ceiling

Current public evidence licenses:

- aggregate Figure 3a temporal-response analysis;
- value-of-time sensitivity of that aggregate response;
- code audit of the published tracking workflow;
- construction and testing of a corrected frame-preserving reanalysis pipeline.

It does not yet license:

- individual Figure 3a event-time distributions;
- individual first-entry or probing latencies;
- trial-level completion CDFs for Figure 3a;
- any adaptive-versus-fixed fitness estimate based on the raw videos.

## 5. What would unblock raw-video Gate 2

Any one of the following would be sufficient:

1. an author-provided list mapping the 18 Figure 3a trials to video IDs;
2. a public metadata/manifest endpoint exposing the member names of IR_vids.zip;
3. authenticated Dryad access that exposes a range-readable object or archive
   manifest;
4. a justified full-archive acquisition followed by checksum-pinned member
   enumeration.

Until one of these is available, raw-video Gate 2 is classified:

RAW_VIDEO_CONTENT_PUBLIC
FIG3A_VIDEO_MAPPING_UNRESOLVED
INDIVIDUAL_LATENCY_CLAIM_BLOCKED

## 6. Scientific consequence

This blocker does not weaken the aggregate Phase A result.

It instead marks the exact boundary between two empirical objects:

aggregate temporal performance profile
    versus
individual completion-time distribution.

The fitness-process theory requires the latter for a direct P(T<=B) estimate.
The former remains useful as a process-shape anchor but cannot be promoted by
interpretation alone.
