# Ingestion pass — 2026-09-10 23:11 PDT

## Backlog ingestion

- Source: `pavoque` / `marytts/pavoque-data`.
- Advanced exact source-faithful mirror of `pavoque-angry.yaml` from source lines 4921 through 5320.
- Added four immutable 100-line chunks:
  - `pavoque_angry_lines_4921_5020_source_faithful.yaml`
  - `pavoque_angry_lines_5021_5120_source_faithful.yaml`
  - `pavoque_angry_lines_5121_5220_source_faithful.yaml`
  - `pavoque_angry_lines_5221_5320_source_faithful.yaml`
- Upstream blob SHA verified unchanged: `bff79d978f740f6c2b09bc595ade03b6bdf33423`.
- Durable angry-style coverage: lines 1-5320.
- Complete utterances represented: 143.
- Partial utterances represented at endpoint: 1 (`m0098`).
- Newly completed utterances in this increment: `m0087`, `m0088`, `m0089`, `m0090`, `m0091`, `m0092`, `m0093`, `m0094`, `m0095`, `m0097`. No `m0096` record occurs in this source range.
- Next exact continuation: source line 5321.
- No PAVOQUE rows promoted to harmonized warehouse tables yet; staging remains source-faithful pending complete relational reconstruction.

## Discovery / screening

Fresh repository/web screening included manually annotated/corrected speech, TextGrid, VOT, vowel, and segmentation candidates.

- Jingju manually segmented resources: excluded from this database scope because they are singing/music production.
- Russian Fricatives (LaRS/SwissUbase): not admitted. Public documentation states that TextGrid segmentation was generated automatically with MAUS; only limited vowel transcription corrections are documented, while the target fricative segmentation does not establish qualifying human verification.
- RescueSpeech: not promoted. The record describes manually annotated authentic German speech recordings but the surfaced documentation does not establish an isolable manually created/corrected phonetic interval or measurement layer suitable for the core database.
- MRPL2 remains REVIEW: strong manual mispronunciation annotation provenance, but files are restricted and interval-level provenance cannot yet be audited.
- IFCASL remains a high-priority review/access target because its published description states >50% manual correction at phone/word segmentation level.

## Validation

- PAVOQUE source ledger and file manifest reconciled to line 5320.
- Namespaced-ID and no-invented-IPA policy unchanged.
- Global promoted warehouse totals intentionally unchanged: 1,361,409 rows / 84 logical tables.
- Registry totals unchanged: 137 tracked / 44 accepted / 25 excluded / 68 review / 43 materially ingested.
- File-manifest and variable-dictionary global counts unchanged: 946 / 1,138.
- Writes confined to `manual_phonetic_production/`.

## Next backlog priorities

1. Continue PAVOQUE angry from line 5321 and close partial `m0098`.
2. Begin relational promotion of complete PAVOQUE utterances/segment intervals while retaining raw SAMPA and source-relative endpoints.
3. Parse accepted Chenghai Southern Min TextGrid/XLSX material into observation-level VOT/closure tables as soon as accessible bytes can be retrieved.
4. Continue review/access resolution for IFCASL and MRPL2.
