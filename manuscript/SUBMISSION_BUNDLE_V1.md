# Deterministic scientific submission bundle v1

This bundle freezes the scientific upload material for the *Theoretical Ecology* submission without inventing author-controlled metadata.

## Build

From the repository root:

```bash
python manuscript/build_submission_bundle.py
```

Default output:

`dist/theoretical-ecology-scientific-bundle-v1.zip`

The ZIP uses stable file ordering, fixed timestamps, stored entries, and fixed POSIX file metadata. CI verifies deterministic repeated builds independently under Python 3.10, 3.11, and 3.12. Cross-version byte identity is not claimed unless separately compared.

## Contents

The archive contains exactly seven files:

1. `MANUSCRIPT_SUBMISSION.md` — generated from `MANUSCRIPT_V1.md` by inserting only the four controlled figure callouts and four controlled legends;
2. `SUPPLEMENT_V1.md`;
3. `figure1_state_space.svg`;
4. `figure2_reachability.svg`;
5. `figure3_extremal_envelope.svg`;
6. `figure4_long_time_outcomes.svg`;
7. `BUNDLE_MANIFEST.json` — byte counts and SHA-256 hashes for the six scientific payload files.

The ZIP is a staging package, not necessarily the single file uploaded to the journal portal. At submission, extract the files and upload them in the portal's requested slots or convert the manuscript body to the portal's accepted editable format after author metadata has been supplied.

## Deliberate exclusions

The archive does not contain inferred or placeholder values for:

- final author list/order;
- affiliations;
- corresponding author/contact details;
- ORCIDs;
- funding;
- competing interests;
- author contributions.

Those are controlled in `SUBMISSION_DECLARATIONS_V1.md` and `SUBMISSION_METADATA_V1.md` and remain a human-author hard stop.

## Safety properties

- scientific source text is never rewritten by the bundle builder;
- the manuscript assembly step is already tested as pure insertion;
- all four figures remain the checksum-frozen deterministic SVGs;
- the bundle manifest hashes the scientific payloads actually placed into the archive;
- two independent bundle builds must be byte-identical in each supported CI runtime;
- archive entries must use the fixed timestamp `1980-01-01 00:00:00` and contain no extra files.

The scientific source baseline is `release/theoretical-ecology-submission-finalization-v1`.
