# Ingestion pass — 2026-09-08 00:09 PDT

## Backlog ingestion

- Continued `coretta_italian_vowel_2018_2026` from the exact prior cutoff.
- Upstream source: `stefanocoretta/coretta2018itaegg/data-raw/datasets/measurements.csv`.
- Immutable upstream blob SHA re-verified as `f3a67a6acb3aac900584698c68966177fe4f04e7`.
- Added three source-faithful chunks:
  - `measurements_lines_0542_0571.csv` — 30 rows
  - `measurements_lines_0572_0601.csv` — 30 rows
  - `measurements_lines_0602_0631.csv` — 30 rows
- These correspond to Coretta measurement data rows 541–630 (CSV source lines 542–631; line 1 is the header).
- Cumulative durable Coretta `measurements.csv` coverage is now data rows 1–630 of 3,268.
- Remaining backlog: 2,638 rows; exact next source line is 632 / data row 631.
- Original values were retained verbatim, including literal `--undefined--` missing-value markers. No IPA, context, timing normalization, rounding, or imputation was introduced.
- The table remains one incomplete logical source table and therefore does not increment the complete logical-table counter. Full consolidation must supersede partial chunks rather than append duplicate rows.

## Discovery sweep

Fresh repository/journal discovery was run in parallel across manually annotated speech-production deposits.

### Screened: AphasiaBD

- Zenodo record: `AphasiaBD: A Bengali Speech Dataset for Broca's and Global Aphasia`.
- Surfaced metadata reports 38 post-stroke aphasia participants, 335 segmented audio clips, multiple production tasks (conversation, repetition, question answering, reading), and manual sentence-level segmentation.
- This is primary non-singing production and is potentially in scope, especially for clinical/group, task, demographic, temporal, and phonetic-error domains.
- Not admitted in this pass because row-level annotation/measurement files and redistribution/license details were not successfully inspected; preserve as a discovery lead for a later direct file-manifest pass rather than creating a paper-only core entry.

### Re-screened / held out

- MRPL2 remains review-only because the record is public but files are restricted; manual mispronunciation annotations are documented, but boundary-generation provenance cannot yet be inspected directly.
- RescueSpeech surfaced as manually annotated primary German speech, but the surfaced description does not by itself establish a reusable phonetic interval/landmark/measurement layer distinct from ASR transcription; no admission without file-level inspection.
- Code-Switching Speech Corpus remains excluded because it resegments/reuses the pre-existing German Spoken Wikipedia Corpus rather than providing a new primary recording collection with isolatable new qualifying phonetic annotations.
- Singing corpora surfaced in repository search were ignored by scope.

## Counts after this pass

- Accepted sources: 39
- Excluded sources: 24
- Review queue: 51
- Warehouse parsed rows: 693,131
- Complete logical tables: 73
- Variable dictionary records: 880

## Validation and lineage

- New Coretta ranges are contiguous with the prior endpoint (source line 541) and do not overlap prior chunks.
- All three new slices were fetched from the same immutable upstream blob SHA.
- No unrelated repository paths were touched.
- No raw audio was committed.

## Next backlog priorities

1. Continue Coretta `measurements.csv` at source line 632 / data row 631 and close the remaining 2,638 rows.
2. Consolidate Coretta partial chunks into a single source-faithful table only with explicit supersession rules preventing double counts.
3. Validate Coretta joins across `measurements.csv`, `stimuli.csv`, `formants-ids.csv`, and lexical lookup data.
4. Resume large accepted-source backlogs: VoxAngeles trajectory materialization, Tang MAT trials, and ROG 1.1.
5. Revisit AphasiaBD at file-manifest level and ingest metadata/annotation tables if public redistribution and manual-boundary provenance are confirmed.
