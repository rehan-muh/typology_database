# Manual Phonetic Production Database (MPPD)

A provenance-first database of **primary phonetic production data with manual or exhaustively human-corrected annotations**.

## Core rule

A dataset enters the core only when the relevant token boundaries, landmarks, labels, or measurements are human-produced or exhaustively human-verified/corrected. Pure forced alignment and secondary reuse of pre-existing speech databases are excluded.

The decision is made at the annotation/measurement level, not only at the paper level. A study may therefore contribute one eligible tier while another tier is rejected.

## Repository layout

- `data/registry/sources.csv` — accepted/conditionally accepted primary sources.
- `data/registry/exclusions.csv` — rejected sources with explicit reasons.
- `data/registry/review_queue.csv` — promising sources needing provenance/access adjudication.
- `data/examples/` — small normalized examples used to test parsers.
- `data/derived/` — harmonized token/segment/landmark tables generated from source data.
- `data/raw/` — local source downloads; intentionally gitignored.
- `docs/` — inclusion criteria, schema, provenance policy, and licensing policy.
- `scripts/` — harvesters, parsers, normalizers, validators, and daily discovery runner.
- `logs/` — dated discovery/adjudication logs.

## Inclusion classes

- `MANUAL_FROM_SCRATCH`: human segmentation/landmarking/labelling from raw signal.
- `AUTO_THEN_ALL_CORRECTED`: automatic proposal, then every relevant boundary/label manually corrected.
- `AUTO_THEN_ALL_VERIFIED`: automatic proposal, then every relevant item explicitly human-verified.
- `MANUAL_MEASUREMENT_ONLY`: manually measured values are available but reusable boundaries/audio may not be.

Partial spot-checking does **not** qualify the unreviewed tokens.

## Primary-data rule

The core excludes analyses whose underlying recordings come from a previously established speech/phonetic database (e.g. Buckeye, Speech Accent Archive, UCLA Phonetics Lab Archive), even when a later paper creates new automatic measurements. New manual annotations layered onto an existing database are tracked separately but are not part of the primary-data core under the current project definition.

## Raw media and licensing

This repository does not republish source audio by default. `scripts/` records source URLs, repository identifiers, file checksums, licenses, and retrieval dates. Raw material is downloaded locally into `data/raw/` only when licensing/access permits. Derived data retain source-specific licensing metadata and attribution.

## First-pass status (2026-08-27)

The initial crawl has validated primary human-grounded sources for Swedish, Standard Thai, Twi, German expressive speech, American English read speech, and several experimental production datasets. It also records hard exclusions for secondary-database reuse and unverified forced alignment.

This is a living registry. All inclusion decisions are auditable in the CSVs and daily logs.
