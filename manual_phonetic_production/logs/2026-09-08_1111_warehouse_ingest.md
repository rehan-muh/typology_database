# Manually Annotated Phonetic Production ingestion pass — 2026-09-08 11:11 PT

## Backlog ingestion

- Continued accepted source `coretta_italian_vowel_2018_2026` from the exact previous checkpoint.
- Authoritative upstream: `stefanocoretta/coretta2018itaegg`, `data-raw/datasets/measurements.csv`, immutable blob `f3a67a6acb3aac900584698c68966177fe4f04e7`.
- Added source lines 1532–1621 = data rows 1531–1620, in three non-overlapping 30-row chunks.
- New rows this run: **90**.
- Durable Coretta `measurements.csv` coverage: **1,620 / 3,268** rows.
- Remaining Coretta measurement rows: **1,648**.
- Next exact continuation: **source line 1622 / data row 1621**.
- Preserved all 14 source variables and original values. Literal `--undefined--` markers remain literal and were not coerced to NA or imputed.
- No IPA, context, or measurements were inferred beyond source-supplied fields.
- Full-table consolidation must supersede the chunk files rather than append them again.

## Integrity / provenance

- Upstream blob SHA remained unchanged during the pass.
- Re-read the beginning of `measurements_lines_1532_1561.csv` and the end of `measurements_lines_1592_1621.csv` after commit; observed values match the upstream ranges.
- Range-level audit written to `data/warehouse/coretta_italian_vowel_2018_2026_chunk_ingestion_2026-09-08_1111.csv`.
- Warehouse row counter advanced from 694,031 to **694,121**. Logical-table and variable-dictionary counts remain **73** and **880**, because these rows extend an already registered logical table/schema.

## Discovery

### `parker_2008_sonority_mendeley` — HIGH review

- Mendeley Data DOI: `10.17632/5jcwt7rffw.6`; related Journal of Phonetics article DOI: `10.1016/j.wocn.2007.09.003`.
- Deposit states that the files are primary English and Spanish recordings collected in 2005, digitized at 44.1 kHz, and that WAV files were manually segmented and analyzed in Praat 4.3.17.
- Deposit is CC BY 4.0.
- Not admitted to core in this run because the surfaced repository record exposes raw WAV provenance but did not expose a machine-readable file inventory or clearly downloadable manual segmentation / derived-measurement layer. The next pass should resolve Mendeley file objects/API or another authoritative supplement and ingest only the genuinely manual products plus source references/checksums for audio.

## Registry/status

- Accepted: **39**.
- Excluded: **25**.
- Review: **55**.

## Next backlog priorities

1. Continue Coretta at source line 1622 / data row 1621 without overlap.
2. Resolve and materialize pending VoxAngeles large TSV trajectory tables while preserving every timepoint.
3. Continue Tang MAT trial parsing and ROG 1.1 manual prosodic annotation isolation.
4. Resolve Parker Mendeley file inventory and determine whether manual segmentation/measurement products are publicly obtainable.
5. Continue repository-level discovery across Journal of Phonetics, Laboratory Phonology, JIPA, JASA, Phonetica, Language and Speech, Speech Communication, LVC and JSLHR deposits.

All repository writes in this pass were confined to `manual_phonetic_production/`.
