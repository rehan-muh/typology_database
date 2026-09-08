# Ingestion pass — 2026-09-08 10:09 PDT

## Backlog ingestion

Source: `coretta_italian_vowel_2018_2026` / upstream `stefanocoretta/coretta2018itaegg`, `data-raw/datasets/measurements.csv` at commit `ec1b00809244eb873f12011c0c06e7460f889947`.

Immutable upstream blob SHA: `f3a67a6acb3aac900584698c68966177fe4f04e7` (unchanged from prior passes).

Added 90 source-faithful observations in three non-overlapping chunks:

- `measurements_lines_1442_1471.csv` — 30 rows
- `measurements_lines_1472_1501.csv` — 30 rows
- `measurements_lines_1502_1531.csv` — 30 rows

These correspond to Coretta data rows 1,441–1,530 because source line 1 is the CSV header. Cumulative durable coverage is therefore 1,530 / 3,268 measurement observations. Next continuation: upstream source line 1532 / data row 1,531. Pending: 1,738 observations.

All 14 source variables were retained exactly: `speaker`, `ipu`, `stimulus`, `sentence_ons`, `sentence_off`, `word_ons`, `word_off`, `v1_ons`, `c2_ons`, `v2_ons`, `voice_ons`, `voice_off`, `c1_rel`, `c2_rel`. Numeric precision was not rounded. Literal `--undefined--` values were retained and not recoded. No IPA, segment context, or missing landmarks were inferred.

Observed missingness in this increment includes literal `--undefined--` in `c2_rel` for multiple tokens; these are source values, not parser errors.

The final chunk was re-read after commit to confirm durable GitHub content. Full-table consolidation must supersede these range chunks rather than append them again.

## Warehouse accounting

- Parsed rows before pass: 693,941
- New durable source-faithful rows: +90
- Parsed rows after pass: 694,031
- Parsed logical tables: 73 (unchanged; Coretta `measurements.csv` is still one partial logical table)
- Variable records: 880 (unchanged; no new source columns introduced)
- Registry: 39 accepted / 25 excluded / 54 review (unchanged)

## Discovery pass

Repository/journal discovery was run in parallel with backlog ingestion.

### UrduSpeech (2026) — not promoted

A newly surfaced Urdu speech corpus reports 156 hours / 71,792 utterances and a 9-hour benchmark manually corrected by native annotators. However, the surfaced description also indicates that the broader corpus is assembled through a curation pipeline and includes categories such as news and drama. This creates unresolved primary-recording / third-party-media lineage risk under the database policy. No registry promotion was made without file-level proof that a separable subset consists of primary elicited/recorded production with qualifying manual phonetic annotation.

### DEBATE — not promoted

A Zenodo-linked Chinese ambiguity corpus surfaced with public audio/annotation files and systematic manual annotation of linguistic ambiguity/focus categories. The surfaced evidence does not establish that the relevant phonetic intervals, segment boundaries, landmarks, or acoustic/articulatory measurements were manually created/corrected. It therefore remains a discovery lead only rather than a core/review admission based on semantic labels alone.

### SAIT-EMA — remains review-only

The 2026 Mandarin/L2 Mandarin EMA database remains valuable for synchronized 250 Hz articulography and 48 kHz audio, but instrument-generated coordinates alone do not satisfy the manual-annotation inclusion rule. No status change was made without evidence for a qualifying human-verified segmentation/landmark layer.

## Integrity / scope validation

- Writes confined to `manual_phonetic_production/`.
- No unrelated repository paths modified.
- No raw audio committed.
- No duplicate recording lineage added.
- Existing accepted/excluded/review decisions were not changed without stronger file-level evidence.
- Source-faithful values remain separate from any future harmonized or normalized fields.

## Next backlog priorities

1. Continue Coretta from source line 1532 / data row 1,531.
2. Materialize pending accepted VoxAngeles measurement/trajectory TSVs while retaining audited-vs-unaudited lineage separation.
3. Continue Tang MAT and ROG 1.1 file-level parsing where qualifying manual layers are already established.
4. Resolve file-level manual-annotation provenance for high-value articulatory and L2 review candidates before admission.
