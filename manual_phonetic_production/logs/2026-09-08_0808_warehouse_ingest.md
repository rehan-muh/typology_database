# 2026-09-08 08:08 PT — aggressive warehouse ingest

## Backlog ingestion
- Continued accepted Coretta Italian vowel production source `coretta_italian_vowel_2018_2026` from authoritative `stefanocoretta/coretta2018itaegg/data-raw/datasets/measurements.csv`.
- Upstream immutable blob re-verified as `f3a67a6acb3aac900584698c68966177fe4f04e7`.
- Added three non-overlapping source-faithful chunks: source lines 1262–1291, 1292–1321, and 1322–1351 (90 data observations total).
- Durable Coretta measurement coverage is now data rows 1–1,350 of 3,268. Remaining: 1,918 rows. Exact continuation: source line 1352 / data row 1351.
- Preserved the original 14-column schema, original numeric precision, original Italian stimulus strings, and literal `--undefined--` missing markers. No IPA/context was inferred and no raw value was standardized in place.
- Full-table consolidation rule remains: eventual complete `measurements.csv` must supersede the partial chunk representation, not append to it, to avoid lineage-level double counting.

## Discovery screening
Fresh searches covered manually corrected phonetic boundaries, TextGrid production deposits, EMA/ultrasound production databases, and repository-backed learner/clinical speech resources.

- **Russian fricatives production database (59 speakers; 22,561 target fricatives)**: strong candidate already documented in the literature as primary read speech where automatic segmentation was followed by manual boundary correction and companion Praat TextGrids are distributed. Kept as a discovery priority for direct repository/file-manifest resolution rather than creating a paper-only core record.
- **AUSpeech**: primary Mandarin audio+ultrasound with `.lab`/`.TextGrid` material; normal-speaker MFA alignment is followed by manual labeling checks and patient pronunciation labeling is manual. Remains review-only until the exact exhaustiveness and file-level annotation provenance can be established.
- **SAIT-EMA**: public CC BY 4.0 synchronized Mandarin EMA/audio remains review-only because instrument-generated trajectories alone do not establish the required manual/human-verified phonetic layer.
- **IFCASL**: approximately 100 French/German native and non-native speakers, word/phone segmentation, and >50% manually corrected data. This is relevant but does not satisfy the database's core requirement at whole-corpus level unless the manually corrected subset can be isolated unambiguously; prioritize locating a public file-level correction flag or separable manual subset before registry admission.
- Search also surfaced singing/media-derived resources; these remain excluded by policy and were not added merely because manual annotations exist.

## Warehouse/accounting
- Parsed row counter advanced by exactly +90 to 693,851.
- Complete logical tables remain 73; variable dictionary remains 880 records because no new schema was introduced by this continuation.
- Registry counts intentionally unchanged: 39 accepted / 25 excluded / 54 review. No ambiguous discovery was promoted without file-level provenance.

## Integrity checks
- Range continuity: previous durable terminal source line 1261; new ranges start at 1262 and end at 1351.
- No chunk overlap introduced.
- Source SHA is unchanged from prior ingestion runs.
- Writes confined to `manual_phonetic_production/`.

## Next backlog priorities
1. Coretta `measurements.csv` source line 1352 onward.
2. Materialize accepted VoxAngeles trajectory TSVs without collapsing sampled timepoints.
3. Continue Tang MAT trial/object extraction and ROG 1.1 isolatable manual annotation layers.
4. Resolve repository-level files for Russian fricatives and IFCASL; only admit subsets with defensible manual-correction provenance.
