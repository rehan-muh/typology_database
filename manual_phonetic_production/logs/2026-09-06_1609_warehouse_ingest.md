# Warehouse ingestion pass — 2026-09-06 16:09 PT

## Scope

Shifted collection from an F1/F2-only/coarticulation-first workflow to an analysis-agnostic manually grounded phonetic-production warehouse. Singing/music production remains excluded. All available source variables are retained before analysis-specific harmonization.

## Backlog ingestion completed in this pass

Reused the latest public-data audit staging artifact rather than redownloading identical repository files. Parsed/inspected 49 source tables plus the PAVOQUE segment table. Aggregate staging coverage is **419,230 rows** and **659 source-variable records**.

### Parsed source coverage

- `chaturvedi_shaw_2025_vowel_errors`: 5 tables, 65,268 rows, 124 table-variable records. Measures/fields include F1-F3 trajectories, midpoints, vowel/error/production labels, coarticulation type, duration-derived quantities and model-derived ratios.
- `cohn_zellou_2023_clear_speech`: 1 table, 2,441 rows, 79 variables. Includes utterance timing, intensity, RMS, F0 summaries, pause/rate measures, demographics/conditions, vowel F1-F3 trajectories, neighboring-sound fields, A1-P0, vowel-space and normalized/derived measures.
- `cox_dideriksen_kerenportnoy_2023_danish_ids`: 15 tables, 40,502 rows, 143 table-variable records. Includes 9,267 vowel observations with F1-F3 in Hz/Mel/z, duration, stress/length/focus/content-word status and caregiver/child covariates; utterance tables additionally provide F0 distribution, pause and speaking/articulation-rate measures; VSA/model tables preserved separately.
- `mitra_dutta_2023_bengali_english`: 1 parsed table, 2,333 rows, 19 variables. Includes speaker/task/language-context fields, lexical item/vowel, F1/F2 at 5/15/25/35/45%, vowel duration and midpoint F1.
- `swehvd_2023_2024`: 26 parsed tables, 75,728 rows, 274 table-variable records. Includes talker/demographic/token/location fields, duration, speaking rate, F0, F1-F3, quantity, reliability/outlier fields and repair/final-measurement lineage. One semicolon-encoded raw-formant summary remains to be reparsed correctly.
- `pavoque`: 232,958 non-silence segment observations generated from the manually corrected YAML phone tiers. Source labels/context/style/duration retained. Because the full source-faithful batch is large, its repository-transfer status is explicitly **generated, not yet mirrored** rather than falsely marked committed.

## Warehouse infrastructure committed

- `scripts/build_phonetic_warehouse.py`: reproducible all-variable inventory/dictionary builder. It preserves unknown variables, assigns conservative domains, records source provenance/manual scope, recognizes documented within-vowel time windows, and does not assume public download implies redistribution permission.
- `data/warehouse/source_table_variable_inventory.csv`: exact table-level row/column inventory with original variable names.
- `data/warehouse/ingestion_status.csv`: source-level discovery/parsed-row/variable/status/pending-work tracker.
- `data/warehouse/README.md`: master policy separating source-faithful storage from downstream analysis views.

## Discovery decisions

### Accepted restricted subset: Russian Fricatives

Added `ulrich_russian_fricatives_2022` as `INCLUDE_RESTRICTED_TARGET_SUBSET`. The primary corpus reports 59 speakers and approximately 22,561 target-fricative tokens. MAUS provided initial phone segmentation, but every **target fricative** boundary was manually inspected/corrected. The surrounding phone tier remains automatically aligned and is therefore not promoted to the manually grounded core. SWISSUbase access is controlled/research-only; data are indexed rather than redistributed.

### Review: Dutch intonational phrase boundaries

Geutjes, Junge & Chen: 16-speaker primary Dutch production; pre-boundary syllables/words and pauses manually segmented/annotated in Praat, with pitch and temporal measures. Associated Yoda data are available on request, not anonymous public download, so source remains review rather than core ingest.

### Review: Media Lengua vowel sequences

Onosson & Stewart: 1,096 manually segmented vowel-sequence tokens across Media Lengua, Quichua and Spanish, with F1/F2/F3 sampled at 5% intervals. High-value multilingual trajectory source, but no complete public data deposit was located in this pass; retained in review queue pending a reusable deposit.

## Licensing/provenance safeguards

Public OSF/Zenodo access is not treated as permission to republish. Where source-level redistribution terms are not verified, this pass preserves authoritative repository references, schemas, counts, checksums via the reproducible builder and variable dictionaries without copying the original observations into GitHub. Explicitly licensed sources can enter `source_faithful/`; restricted sources remain metadata/reference layers.

## Next ingestion priorities

1. Reparse SwehVd's semicolon raw-formant summary and reconcile repair/final-measurement lineage.
2. Resolve Schertz manual burst/periodicity/vowel-end landmark files and ingest all VOT/vowel-duration event variables.
3. Continue Mitra-Dutta repository triage beyond the already parsed formant table.
4. Build complete table/variable inventories for newly accepted Japanese vowel data and restricted Russian target-fricative source.
5. Verify redistribution licenses source-by-source before any raw/derived table mirroring.
