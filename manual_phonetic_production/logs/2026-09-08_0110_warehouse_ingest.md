# Ingestion pass — 2026-09-08 01:10 PDT

## Backlog ingestion

- Continued `coretta_italian_vowel_2018_2026` from the exact prior continuation point in upstream `data-raw/datasets/measurements.csv`.
- Immutable upstream blob: `f3a67a6acb3aac900584698c68966177fe4f04e7`.
- Added source lines 632–661, 662–691, and 692–721 as three source-faithful chunks (90 observation rows total).
- Durable Coretta measurement coverage is now data rows 1–720 of 3,268; 2,548 rows remain pending. Next continuation point: upstream source line 722 / data row 721.
- Preserved all 14 original fields and literal `--undefined--` missing markers exactly. No IPA, segment context, timing values, or normalized values were inferred or overwritten.
- The newly materialized range crosses from speaker `it04` to `it05`; the source itself begins supplying `voice_ons` and `voice_off` values in the `it05` rows, and these were retained verbatim.
- Lineage rule remains unchanged: these chunks are portions of one logical 3,268-row timing/landmark table and must be superseded, not duplicated, when a consolidated full table is materialized.

## Validation / provenance

- Re-read the final new durable chunk after commit and verified its content and 30-row extent.
- Recorded the three ranges and cumulative logical-table state in `data/warehouse/coretta_italian_vowel_2018_2026_chunk_ingestion_2026-09-08_0110.csv`.
- Warehouse counters updated from 693,131 to 693,221 parsed rows; complete logical-table count remains 73; variable dictionary count remains 880.
- Registry counts after discovery: 39 accepted / 24 excluded / 52 review.

## Discovery

### L2-ARCTIC manual subset — REVIEW / HIGH

- Added `l2_arctic_2018_2020_manual_subset` to the review queue.
- Primary non-native English production from 24 speakers across Arabic, Hindi, Korean, Mandarin, Spanish, and Vietnamese L1 groups.
- Current corpus documentation reports 26,867 utterances and 3,599 manually examined/annotated utterances. The manual subset has corrected word/phone boundaries and production-error labels for substitutions, deletions, and additions.
- Repository structure explicitly separates forced-aligned `/textgrid` files from manually annotated `/annotation` TextGrids, so the qualifying human-grounded layer is isolatable rather than requiring admission of the automated corpus.
- The spontaneous suitcase subset has a particularly strong manual-provenance statement: two trained research assistants split transcription, cross-checked one another, and the full set was then checked by project co-PI John Levis.
- Core admission deferred because authoritative download requires agreeing to CC BY-NC 4.0 terms and submitting name/email/affiliation to receive a direct link. A later pass should inspect the authoritative archive rather than treating mirrors as provenance-equivalent, enumerate all `/annotation` and suitcase files, and deduplicate recordings used by derivative mispronunciation-detection studies.

## Next priorities

1. Continue Coretta `measurements.csv` at source line 722 / data row 721 and keep contiguous non-overlapping chunks.
2. Once Coretta timing/landmark table is complete, consolidate it once, validate joins against `stimuli.csv`, `formants-ids.csv`, and lexical metadata, and retire chunk counting without row duplication.
3. Continue large accepted-source backlog: VoxAngeles trajectory materialization, Tang MAT trial extraction, and ROG 1.1.
4. Revisit HIGH review deposits with isolatable manual layers, especially L2-ARCTIC and MRPL2, when authoritative files are directly accessible.
