# Manually Annotated Phonetic Production Database — ingestion pass 2026-09-09 00:07 PDT

## Backlog ingestion

Continued `coretta_italian_vowel_2018_2026` from the deterministic prior continuation point in the public CC-BY-4.0 upstream repository `stefanocoretta/coretta2018itaegg`, path `data-raw/datasets/measurements.csv`.

- Upstream Git blob SHA remained `f3a67a6acb3aac900584698c68966177fe4f04e7` on all retrievals.
- Added exact source-faithful slices `measurements_lines_2702_2731.csv`, `measurements_lines_2732_2761.csv`, and `measurements_lines_2762_2791.csv`.
- 30 observations per slice; 90 newly materialized observations total.
- Preserved source strings, numeric precision, column order, and literal `--undefined--` values. No IPA, labels, contexts, or normalized values were inferred.
- Durable `measurements.csv` coverage is now 2,790 / 3,268 observations (85.4%); 478 remain.
- Exact next continuation: upstream source line 2792 / data row 2791.
- Chunk files remain provisional exact slices: any future consolidated exact copy must atomically supersede them in counting/derived views so chunk and consolidated representations are never double-counted.

A range-level provenance audit was added at `data/warehouse/coretta_italian_vowel_2018_2026_range_audit_2026-09-09_0007.csv`.

## Status reconciliation and validation

`data/warehouse/ingestion_status.csv` had lagged the already committed Coretta chunk state. Reconciled its Coretta row to 2,790 / 3,268 measurements and the same continuation point. Global parsed-row accounting advances from 695,201 to 695,291; logical-table count and variable-dictionary count are unchanged because these rows extend an existing source table/schema.

Validation performed in this pass:

- upstream SHA consistency across all three source ranges;
- exact 30-row range boundaries;
- contiguous progression from prior source line 2701 through source line 2791 with no intentional overlap;
- source missing markers preserved rather than filtered;
- registry counts left unchanged because no discovery candidate crossed the qualifying threshold;
- all repository writes confined to `manual_phonetic_production/`.

## Discovery screening

Discovery was run in parallel with backlog ingestion.

- **PAVOQUE** resurfaced with manually corrected phonetic segments in its public YAML annotations. It is already represented in the database, so no duplicate source was created.
- **PxCorpus / PxSLU** (Zenodo 6524162) contains 1,981 primary French drug-prescription recordings from 55 participants and human-verified/manual transcripts plus semantic annotations. The surfaced deposit does not establish a manually created/corrected phonetic timing, landmark, segment-boundary, articulatory, or acoustic-measurement layer. It was therefore not promoted to core on transcript verification alone.
- **French OSCE Dialogue Dataset** contains primary clinical-training recordings and some manually corrected transcriptions, but files are restricted and the surfaced annotation layer is transcript-level rather than a demonstrated phonetic interval/landmark/measurement layer. No core promotion.
- **TunSwitch** contains primary prompted Tunisian Arabic production and meticulous manual code-switch tagging, but the demonstrated manual annotations identify French/English words rather than phonetic production intervals, landmarks, or measurements. No core promotion.

These conservative decisions avoid inflating the database with orthographic/semantic annotation resources that do not meet the manual-phonetic criterion.

## Next backlog priorities

1. Continue Coretta exactly at source line 2792; 478 observations remain.
2. Resolve and parse Jordanian Arabic acoustic-dataset TextGrid and metadata file objects.
3. Expand CCOST file-level TextGrid ingestion.
4. Continue VoxAngeles manual-layer durations and decile trajectories while preserving recording lineage.
5. Run/ingest participant-level Tang MAT field extraction rather than treating summary tables as trials.
6. Parse ROG 1.1 manually corrected prosodic-unit layer with strict GOS lineage isolation.
7. Continue file-level review resolution for KEC and the Plastic Mandarin tone-trajectory deposit.
