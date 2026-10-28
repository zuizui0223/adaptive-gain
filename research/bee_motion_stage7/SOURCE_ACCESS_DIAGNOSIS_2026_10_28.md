# Stage 7 (two-hive moving-flower trajectories) — original-source access diagnosis, 2026-10-28

**Status: SOURCE METADATA VERIFIED; ORIGINAL TRAJECTORY ARCHIVE UNAVAILABLE FROM THE GITHUB ACTIONS RUNNER; NO ORIGINAL MEASURED FLIGHT-HEADING OR FLOWER-TRACKING RESULT HAS BEEN COMPUTED.**

Independent original source: de Vries et al. (2025), *Journal of Experimental Biology*, DOI https://doi.org/10.1242/jeb.249380, Dryad dataset DOI https://doi.org/10.5061/dryad.qbzkh18tj. The publisher describes 728 successful landing trajectories from two hives, five robot flower-motion frequencies (0, 0.03, 0.24, 0.53, 0.65 Hz). This dataset is only successful landings; it cannot estimate all attempted landing success or individual cue-query cost without failures.

### Official DataCite/Dryad original metadata independently fetched
- Native Dryad API v2 dataset, version **353039**.
- Official original file `data_bumblebee_landing_moving_flower.7z`, native file id **3963254**, provider size **17,312,155 bytes**, provider **SHA-256** `84abb80d0b69d8c8be5dc391a85d405d58a22cba6bbcc3e47d00124f5a1641bf`.
- Official original `README.md`, native file id **3963273**, provider size **1,845 bytes**, provider **SHA-256** `0ba6034f9131d803bf79e5ca06aa9652f94a5bfba6a383da46eb970d633b082e`.
- These are provider **metadata digests only**. Because source bytes could not be retrieved, independent local byte-level SHA-256 verification and actual file content audit are **NOT** complete. Original arrays/measurements and the 728-event claim have not been empirically rechecked.

### Three provider-owned unauthenticated attempts and independent CI results

1. Original native file download `https://datadryad.org/api/v2/files/3963254/download`: **HTTP 401 Unauthorized**.
2. Native provider public-file-stream route using the *same provider file id* `https://datadryad.org/stash/downloads/file_stream/3963254`: **HTTP 403 Forbidden**.
3. Original dataset-wide native bundle route `https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.qbzkh18tj/download`: **HTTP 401 Unauthorized**.

All requests performed on the GitHub Actions runner; source JSON metadata was available without authentication. The [diagnostic run 40611388945](https://github.com/zuizui0223/adaptive-gain/actions/runs/40611388945) records all three download blockers and an original-source manifest artifact. The failure is **external read access for original bytes**, not a numerical result and not a justified reason to fake or mirror synthetic flight data.

### Resolution boundary
Do not run the kinematic model on fabricated or paper-digitized trajectory values. The original public service would need to provide actual source bytes (e.g., accessible authorized download or a provider-published mirror with **exact matching SHA-256**) before measured flight heading, bee–flower lag and two-hive cross-validation can be attempted.

A separate accessible original experiment, **18-colony robotic-flower reward sensing** (KU Leuven RDR DOI 10.48804/UIIVLP), has been independently audited in a separate PR #81. That original dataset has *colony and flower-device IDs but no worker/individual ID and no continuous flight trajectory*. Its colony-level temporal-use analysis is **not** a replacement for the 728 landing trajectories, and cannot be represented as replication of individual flight mechanics.

Frozen V5/V6 manuscripts and earlier Stage 4–6 source results remain unchanged.
