# Ingestion + discovery audit — 2026-09-18 21:12 -0700

## Backlog ingestion: PAVOQUE
Continued accepted PAVOQUE angry annotations from cursor `spike0017`. Ingested 35 source-faithful manually corrected segment observations for `spike0017` (*Ich glaube du hast mir eine Frage gestellt.*), utterance 56.28–60.36 s. Original labels and cumulative endpoints are retained unchanged from `pavoque-angry.yaml`, blob SHA `bff79d978f740f6c2b09bc595ade03b6bdf33423`. Final endpoint 4.075 s vs utterance span 4.080 s; the 5-ms source residual is preserved. Endpoints are monotonic and imply no negative durations. No IPA was inferred. Next cursor: `spike0018` (74 source intervals; verified upstream in this pass).

Source-faithful shard: `data/source_faithful/pavoque_angry_spike0017_2026-09-18_2112.csv`.

## Discovery / qualification
- L2-ARCTIC reverified as an unusually strong accepted/manual-subset target: 24 speakers, 26,867 total utterances, with 3,599 human-examined utterances. Documentation states the manual annotation subset contains corrected word and phone boundaries plus substitution/deletion/addition labels; corpus-wide forced-aligned tiers remain ineligible unless part of a human-corrected annotation file. Public documentation also exposes per-speaker annotation counts (~150 each), allowing deterministic isolation of `/annotation` from `/textgrid`.
- ROG (LREC 2026) discovered/rechecked: ~10 h / >75k words of Slovenian speech with manual prosodic/interactional layers, but it builds on pre-existing SST/GOS 2 recordings. Keep in REVIEW until the newly contributed manual production/prosodic layers can be isolated from secondary recording lineage and repository files enumerated.
- Golos discovered/rechecked: ~1240 h Russian audio described as crowd-manually annotated. Keep in REVIEW because the relevant annotation appears primarily orthographic/ASR labeling; do not admit without evidence of qualifying phonetic/prosodic manual annotation.
- IMS GECO revalidated EXCLUDE for phonetic timing core: segment/syllable/word timing is forced aligned; manual orthographic transcription alone does not satisfy the phonetic-production annotation criterion.
- Nonspeech7k remains EXCLUDE: third-party source lineage and non-speech production.

## Integrity / provenance
- New IDs are source/prompt/segment-index addressable and do not overlap prior PAVOQUE shards.
- No raw audio committed.
- Source SHA retained on every new observation.
- No normalization overwrote original labels or timing.
- No files outside `manual_phonetic_production/` modified.

## Next priorities
1. PAVOQUE `spike0018+` (74 verified intervals in next item), then remaining styles.
2. L2-ARCTIC: enumerate publicly accessible `/annotation` TextGrids and ingest only the human-corrected subset, preserving error tags/comments and speaker/L1 metadata.
3. RescueSpeech: enumerate ASR archive and isolate exact manual layer.
4. Continue JSUT from actual latest repository cursor.
5. CORPRES manually segmented 40%: locate isolatable file partition.
6. Continue repository-first discovery across OSF/Zenodo/GitHub/DataCite and priority phonetics journals.
