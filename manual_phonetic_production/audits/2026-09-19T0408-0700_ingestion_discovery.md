# Ingestion/discovery audit — 2026-09-19 04:08 -0700

## Backlog ingestion

Advanced the missing JSUT source-faithful block `BASIC5000_1391`–`BASIC5000_1430` from the authoritative `sarulab-speech/jsut-label` `e2e_symbol/phoneme.yaml`. Added 40 complete rows to `data/source_faithful/jsut_basic5000_1391_1430_20260919_0408.csv`. Preserved exact upstream symbolic strings and blob SHA `ae8933677c082c22238a895012b6b6dcba1f6625`. No IPA, timing, lexical context, or automatic Julius alignment was inferred. This repairs a durable coverage gap between the existing 1351–1390 block and later 1431+ material.

Validation: 40 unique utterance IDs; contiguous numeric range 1391–1430; no duplicate IDs within the new file; every row has source ID, upstream file, annotation method, and immutable blob SHA.

## Discovery / qualification

Re-audited **Russian Fricatives** (Ulrich 2022; DOI 10.48656/4q9c-gz16). Repository/article evidence establishes primary read-speech production and a manually verified target layer: initial preprocessing used MAUS, but target-fricative boundaries were manually inspected and corrected in Praat. The dataset description reports 198 sentence types/files, 77 recording sessions, and 22,561 target-fricative tokens; the associated database article reports 59 speakers. SWISSUbase exposes six payload groups (`1_filter_the_noise.zip`, `2_fricative_extraction.zip`, `Recording_1.zip`, `Recording_2.zip`, `metadata.zip`, `sentence_list.zip`) but download is governed by a closed research/teaching usage agreement and authenticated access. Therefore no restricted bytes or observation rows were copied into GitHub. Added an explicit ingestion-status record separating the qualifying manual target layer from nonqualifying automatic boundaries.

Fresh discovery also surfaced 2026 multimodal EMA/EEG/audio production resources and SAIT-EMA; these remain review candidates until manual annotation/correction provenance is demonstrated at the relevant observation layer. Search hits involving medical ultrasound, semantic treebanks, perception/neural-only stimuli, synthetic speech, and music were excluded from admission.

## Next priorities

1. Continue JSUT only from the first genuinely uncovered durable range after reconciling all existing 1431+ and 1481+ blocks; do not re-ingest already present rows.
2. Russian Fricatives: if authorized payload access becomes available, ingest metadata and manually corrected target intervals only, with `SentenceNo`/`IntervalNo` lineage; never commit restricted raw audio.
3. TaL manual short-segment boundaries and L2-ARCTIC's 3,599 human-reviewed utterances: isolate public manual tiers and ingest actual interval/token observations.
4. Audit SAIT-EMA and the 2026 German EMA+EEG dataset specifically for human annotation provenance before core admission.
5. Continue RescueSpeech/IFCASL/CORPRES file-level isolation and preserve ambiguous mixed automatic/manual corpora in review.

All writes in this pass are confined to `manual_phonetic_production/`.
