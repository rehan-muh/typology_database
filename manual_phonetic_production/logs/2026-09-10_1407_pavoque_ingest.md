# 2026-09-10 14:07 PDT ingestion pass

## Backlog ingestion
- PAVOQUE (`pavoque`): fetched and durably committed exact authoritative source lines 1321-1720 of `pavoque-angry.yaml` from public upstream `marytts/pavoque-data`, immutable blob `bff79d978f740f6c2b09bc595ade03b6bdf33423`.
- Four new source-faithful chunks: 1321-1420, 1421-1520, 1521-1620, and 1621-1720.
- Durable PAVOQUE angry-style coverage is now lines 1-1720.
- The new range closes the previously partial `spike0038` and continues through complete `spike0050`. Total durable complete annotated utterances recorded in source status: 48; current partial utterances: 0.
- Original German-SAMPA labels, source text/style fields, utterance start/end times, and manually corrected segment endpoints were preserved exactly. No IPA labels or missing context were invented.
- PAVOQUE remains source-faithful staging pending relational conversion; no staged lines were counted as promoted warehouse rows.

## Discovery
- Ran fresh searches across Zenodo, OSF-indexed material, public GitHub resources, manual segmentation/correction terminology, clinical production, learner speech, and phonetic trajectory resources.
- Re-screened AphasiaBD (38 Bengali post-stroke speakers; 335 manually sentence-segmented clips) and confirmed it is already present in the review queue, avoiding duplicate registration.
- Re-screened IFCASL (about 100 French/German native and non-native speakers; >50% of word/phone segmentation manually corrected) and confirmed it is already present in the review queue; clean identification of the manually corrected subset remains the gating issue.
- Singing datasets surfaced by broad searches were rejected under the explicit non-singing criterion.
- No candidate was promoted solely because a transcript was manually corrected; manual provenance must attach to the relevant production annotation/measurement layer.

## Validation and accounting
- New PAVOQUE chunks are contiguous, non-overlapping, and pinned to the same upstream blob as prior coverage.
- Current endpoint is exactly the final segment line of `spike0050`; deterministic continuation is source line 1721.
- Manifest and source-specific ingestion status were reconciled to the same endpoint and complete-utterance count.
- Global warehouse accounting remains 1,361,409 promoted rows across 84 logical tables, with 133 tracked sources (43 accepted, 25 excluded, 65 review) and 43 materially ingested sources.
- File-manifest and variable-dictionary global record counts remain 943 and 1,134 respectively because this pass extended an already inventoried upstream file and introduced no new source variables.
- No raw audio was committed. No unrelated repository paths were modified.

## Next backlog priorities
1. Continue `pavoque-angry.yaml` from source line 1721, then mirror happy/neutral/poker/sad/outtakes YAML annotations.
2. Convert completed PAVOQUE utterances into namespaced utterance and segment/interval tables, deriving interval starts only from the immediately preceding source endpoint while retaining the original endpoint values.
3. Continue lineage-safe Puggaard-Rode Jutland `/t/` promotion and ingest the full release-spectrum trajectory table without reducing it to COG.
4. Resume high-priority public manual VOT/formant/voice-quality/EMA/ultrasound/clinical-production file harvesting.
