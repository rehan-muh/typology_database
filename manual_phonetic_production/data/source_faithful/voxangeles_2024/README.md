# VoxAngeles — audited manual layer

This subtree ingests only the **human-audited** VoxAngeles annotation/measurement lineage. The underlying recordings are pre-existing archival/field recordings; they are not treated as a new primary recording collection here. VoxAngeles qualifies because it contributes a separately isolatable manual correction/audit layer (`data/audited_aligned`) and production measurements derived from those audited TextGrids. The repository's `data/unaudited` forced-alignment branch is explicitly excluded from core.

## Current durable ingest

- `meanf0_abk_source_faithful.tsv`: 54 Abkhaz recording-level mean-F0 observations copied exactly from upstream `voxangeles_meanf0_file.tsv` (blob `9492dd2ed35044219aed483613fd3f7a44f292d3`).
- `file_manifest.csv`: exact GitHub blob SHA/size records for all six public phonetic-measurement tables and four extraction scripts.
- `variable_dictionary.csv`: 75 table-specific records documenting every verified original variable in the duration, F0-decile, formant-decile, and recording-mean-F0 schemas. Quartile schemas remain pending rather than being inferred.
- `ingestion_status.json`: continuation state and lineage restrictions.

## Verified trajectory semantics

The upstream Praat scripts sample vowel F0 and F1/F2/F3 at ten positions `start + i*(duration/10)`, i=1..10. The source-faithful tables must retain all ten original samples. A harmonized long view may additionally expose normalized time 0.1..1.0, but must not overwrite or collapse the raw columns.

## Pending

Mirror the remainder of mean F0, complete duration/F0/formant tables, verify and ingest quartile schemas, enumerate all audited language ZIP contents/TextGrids, and build namespaced recording/token/context views. Do not ingest unaudited alignments.
