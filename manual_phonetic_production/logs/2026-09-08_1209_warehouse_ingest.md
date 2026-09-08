# Ingestion pass — 2026-09-08 12:09 -07:00

## Backlog ingestion

Advanced `coretta_italian_vowel_2018_2026` source-faithful materialization for upstream `stefanocoretta/coretta2018itaegg:data-raw/datasets/measurements.csv`.

- Immutable upstream blob re-verified as `f3a67a6acb3aac900584698c68966177fe4f04e7`.
- Added source lines 1622–1651 (data rows 1621–1650): 30 rows.
- Added source lines 1652–1681 (data rows 1651–1680): 30 rows.
- Added source lines 1682–1711 (data rows 1681–1710): 30 rows.
- Net new durable observations: 90.
- Durable Coretta `measurements.csv` coverage: 1,710 / 3,268 rows.
- Remaining Coretta observations: 1,558.
- Exact continuation: source line 1712 / data row 1711.
- Original 14-column source schema retained; numeric values and literal `--undefined--` missing markers preserved verbatim.
- Chunk ranges are contiguous with the prior durable endpoint and non-overlapping. Eventual full-table consolidation must replace/supersede chunk accounting rather than append duplicate observations.
- Post-write re-read of the final chunk confirmed the committed source-faithful material.

Warehouse counter after this increment: 694,211 parsed rows; 73 complete logical tables; 880 variable records.

## Discovery

Added `corpres_russian_2010` to review, not core. Skrelin et al. (2010) describe a primary Russian production corpus with 8 speakers, 60 hours / 528,458 running words, and six annotation layers (pitch marks, phonetic events, narrow/wide phonetic transcription, orthographic and prosodic transcription). The paper states that 40% was manually segmented and fully annotated across all speakers/styles. This is highly promising but the public/authorized data deposit and an isolatable file-level manual subset were not resolved in this pass. Core admission is therefore prohibited until file access, license, formats, and manual-vs-generated provenance are verified.

Existing candidates encountered during broad screening were not duplicated when already represented in the registry/review backlog.

## Integrity / scope

- Accepted: 39.
- Excluded: 25.
- Review: 56.
- No ambiguous automatically aligned material was promoted to core.
- No raw audio was added.
- All writes in this pass were confined to `manual_phonetic_production/`.

## Next backlog priorities

1. Continue Coretta `measurements.csv` from source line 1712 / data row 1711.
2. Continue accepted large observation-level backlogs, especially VoxAngeles trajectory materialization, Tang MAT trial extraction, and ROG 1.1 isolatable new annotation layers.
3. Resolve CORPRES authoritative distribution/access and isolate the manually segmented 40% before any core admission.
4. Continue file-level review of high-value articulatory/clinical resources only where human verification can be proven and isolated.
