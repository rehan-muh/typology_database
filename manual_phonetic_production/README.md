# Manual Phonetic Production Database (MPPD)

A provenance-first database of **primary phonetic production data with manual or exhaustively human-corrected annotations**.

## Core rule

A dataset enters the core only when the relevant token boundaries, landmarks, labels, or measurements are human-produced or exhaustively human-verified/corrected. Pure forced alignment and secondary reuse of pre-existing speech databases are excluded.

The decision is made at the annotation/measurement level, not only at the paper level. A study may therefore contribute one eligible tier while another tier is rejected.

## Primary analysis target: coarticulation

The harmonized analysis layer is now designed specifically for ten phenomena:

- V→V carryover
- V→V anticipatory
- C→V place effects
- V→C acoustic effects
- nasal coarticulation
- laryngeal coarticulation
- VOT/following-vowel interaction
- labialization/rounding coarticulation
- rhotic/lateral effects
- temporal coarticulation

Rate, style, task and speaker metadata are retained as moderators/covariates rather than treated as separate coarticulation outcomes.

See `docs/coarticulation_schema.md` for the canonical analysis contract. Every usable source is mapped into three linked long-format tables under `data/coarticulation/`: target/context tokens, acoustic trajectories, and temporal landmarks/events. `data/coarticulation/source_capabilities.csv` records whether each accepted source is `READY`, `REEXTRACT`, `POSSIBLE`, `NOT_SUPPORTED`, `RESTRICTED`, or `SPECIALIZED` for each of the ten analyses. `data/coarticulation/ingestion_queue.csv` is the prioritized conversion backlog.

Future derived batches must pass `scripts/validate_coarticulation.py` before they are treated as analysis-ready.

## Repository layout

- `data/registry/sources.csv` — accepted/conditionally accepted primary sources.
- `data/registry/exclusions.csv` — rejected sources with explicit reasons.
- `data/registry/review_queue.csv` — promising sources needing provenance/access adjudication.
- `data/coarticulation/` — canonical analysis schema, source capabilities, ingestion queue, templates and derived batches.
- `data/raw/` — local source downloads; intentionally gitignored.
- `docs/` — inclusion criteria, schema, provenance policy, licensing policy, and coarticulation specification.
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

## Analysis safeguards

Study/source, language and speaker are always kept as separate identifiers. Speaker IDs are globally namespaced as `source_id::source_speaker_id`; bilingual speakers retain one speaker UID with token-level production language. Specialized singing sources are not pooled with ordinary speech by default, and clinical/L2 domains remain explicit for sensitivity analyses. A source may be accepted into MPPD but contribute to none of the ten coarticulation analyses if its validated annotation tier lacks the required context or measurement.

This is a living registry and harmonized analysis database. All inclusion and analysis-eligibility decisions are auditable in the CSVs and daily logs.
