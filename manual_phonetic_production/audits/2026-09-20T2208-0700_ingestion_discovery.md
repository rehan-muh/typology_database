# Ingestion/discovery audit — 2026-09-20 22:08 -0700

## Backlog ingestion

- Source: `jsut_label` (`sarulab-speech/jsut-label`, `e2e_symbol/phoneme.yaml`).
- Immutable upstream blob SHA: `ae8933677c082c22238a895012b6b6dcba1f6625`.
- Parsed and preserved `BASIC5000_1431`–`BASIC5000_1470`: 40 source-faithful manual phonetic/prosodic annotation sequences.
- Output: `data/harmonized/jsut_label_basic5000_manual_annotation_index_1431_1470.csv`.
- Namespaced IDs: `jsut_label::BASIC5000_NNNN`.
- Preserved annotation strings verbatim. No IPA normalization, segment timing, lexical context, or other missing information was inferred.
- Automatic timing is explicitly marked `automatic_not_ingested`.
- Deduplication audit found an existing 1391–1430 extract and an existing 1471–1480 extract; neither was duplicated. Next contiguous cursor is `BASIC5000_1481`.

## Discovery

Fresh searches covered Zenodo, OSF and GitHub for manually segmented/corrected production data, including phonetic TextGrids, VOT/formant production measurements, ultrasound/articulatory annotation, and manually verified speech corpora.

### Screened, not promoted

- **PxCorpus (Zenodo 10080490)** — primary French spoken drug-prescription recordings; 55 participants and roughly 2k recordings; transcripts are manually produced/human-verified and semantic labels are available. Current evidence does not establish a manual phonetic interval, landmark, or acoustic/articulatory measurement layer, so this is not admitted to the phonetic core on transcript/semantic annotation alone.
- **TunSwitch (Zenodo 8342762)** — primary Tunisian Arabic/code-switch speech with meticulous manual annotation of language switching. Current evidence supports transcript/code-switch labels but not a manual phonetic segmentation/measurement layer; not promoted to core.
- Singing/music manual-annotation hits were rejected under the explicit non-singing criterion.
- Non-speech manual-annotation hits were rejected.

## Integrity/provenance checks

- 40 new unique source utterance IDs.
- Every row has a namespaced ID and upstream blob SHA.
- No overlap with the already stored 1391–1430 or 1471–1480 ranges.
- No automatic/forced-aligned timing admitted.
- No raw audio committed.
- Writes restricted to `manual_phonetic_production/`.

## Status delta

- Parsed rows: 1,364,067 → 1,364,107.
- Logical parsed tables: 200 → 201.
- Source adjudication totals unchanged because no discovery candidate met the threshold for a new accepted/review registry promotion in this pass.

## Next priorities

1. Continue JSUT at `BASIC5000_1481`, checking for overlapping extracts before writing.
2. Prioritize observation-level access tracing for IFCASL and the manually examined L2-ARCTIC subset.
3. Continue attempts to obtain/parse Tibetan English diphthong full F1/F2 trajectories.
4. Inspect TaL/UltraSuite manual reference, SLT, segmentation, ultrasound/EMA layers at file level.
5. Search journal supplements and DataCite-linked deposits specifically for manual VOT, formant trajectories, voice-quality and articulatory measurements rather than paper-level metadata only.
