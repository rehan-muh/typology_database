# Ingestion pass — 2026-09-22 16:07 PT

## Backlog ingestion: PAVOQUE

Advanced the accepted PAVOQUE backlog from the authoritative upstream `marytts/pavoque-data` repository. Inspected `pavoque-angry.yaml` at upstream commit `66c0f3a7d67bd185079744e1acbedbe69a7b6ad5` and source blob `bff79d978f740f6c2b09bc595ade03b6bdf33423`.

Committed a source-faithful utterance table for `spike0015`–`spike0017` (3 primary angry-speech utterances). Preserved original text, original utterance start/end timestamps, source audio filename, emotion label, annotation provenance, upstream filename, and immutable upstream commit. Namespaced IDs use `pavoque::spikeNNNN`.

The corresponding source contains 83 deposited segment labels/cumulative endpoints across these three utterances (14 + 34 + 35). They were enumerated and QC-checked during this pass but are NOT counted as ingested observations until committed to a structured segment table in a later pass. No normalized IPA was inferred from MaryTTS labels.

QC: source segment endpoints are monotonic within each utterance. The last segment endpoint does not equal the enclosing utterance duration for these records; this discrepancy is preserved as source behavior and must not be silently stretched to the utterance boundary.

## Discovery

Ran fresh repository/web discovery for manually annotated/corrected phonetic production deposits, including TextGrid, manual segmentation, L2 production, EMA/articulatory, and corpus queries. Search results were dominated by already-known corpora, automatic/forced-aligned resources without adequate human verification, or resources requiring lineage review. No new source was admitted on weak evidence.

## Counts for this pass

- New source-faithful observations committed: 3 utterance rows.
- Segment observations enumerated but pending commit: 83.
- New accepted/review/excluded sources: 0/0/0.
- New source-faithful table: 1.

## Next backlog priorities

1. Commit the 83 `spike0015`–`spike0017` segment rows with original labels/endpoints plus separate deterministic start/duration/absolute-time fields.
2. Continue contiguous PAVOQUE angry YAML ingestion beyond `spike0017` rather than rediscovering the source.
3. Continue CCOST archive/metadata ingestion and restricted-source access checks already present in backlog.
4. Keep normalized IPA blank unless an explicit defensible mapping for the MaryTTS label inventory is documented.
