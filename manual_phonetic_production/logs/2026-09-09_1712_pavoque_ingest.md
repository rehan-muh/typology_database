# 2026-09-09 17:12 PDT — discovery + backlog ingestion

## Backlog ingestion: PAVOQUE manually corrected segment layer

- Continued the accepted PAVOQUE spoken-German corpus from the prior durable endpoint `spike0003`.
- Authoritative upstream annotation file: `marytts/pavoque-data/pavoque-angry.yaml`, immutable Git blob `bff79d978f740f6c2b09bc595ade03b6bdf33423`.
- Parsed five complete utterances: `spike0004` through `spike0008`.
- Added 5 source-faithful utterance rows preserving original prompt ID, German orthography, style, utterance start/end, and source blob provenance.
- Added 130 manually corrected segment/silence rows preserving original SAMPA/source labels and original segment endpoints. Segment starts and durations are derived separately from successive endpoints; no IPA was invented.
- New durable files:
  - `data/source_faithful/pavoque_angry_utterances_chunk002.csv`
  - `data/source_faithful/pavoque_angry_segments_chunk002.csv`
- Cumulative durable PAVOQUE mirror: 8 utterances (`spike0001`–`spike0008`) and 227 segment/silence rows across chunks 001–002.
- Exact continuation point: `spike0009`.
- The pre-existing status record notes a 232,958-row locally generated full segment batch; this is kept distinct from the durable committed mirror and must never be double-counted.

## Validation

- Composite segment keys `(utterance_id, segment_index)` are unique within the new chunk.
- Segment endpoints are monotonically increasing within every utterance.
- Final segment endpoints remain within the parent utterance duration: spike0004 3.775 <= 3.780; spike0005 4.435 <= 4.440; spike0006 3.835 <= 3.840; spike0007 2.995 <= 3.000; spike0008 1.915 <= 1.920 seconds.
- New observation rows this pass: 135 (5 utterances + 130 segments).
- No raw audio was committed.

## Discovery

- Screened fresh production-literature/repository leads while ingesting backlog.
- A 2026 conversational-Spanish vowel-production study reports an isolatable manually bounded subset of 1,043 vowels, with duration and F1/F2/F3 derived from those human boundaries. No public observation-level repository was resolved in this pass, so it was not admitted to core or counted as a new source. It remains a discovery lead pending a public deposit that allows the manual subset to be isolated.
- Other surfaced multimodal/automatic resources were not promoted without explicit evidence of a qualifying human-created/corrected annotation layer.

## Accounting after pass

- tracked sources: 127
- accepted: 42
- excluded: 25
- review: 60
- materially ingested sources: 42
- parsed rows: 1,357,295
- logical tables: 84
- file-manifest records: 922
- variable-dictionary records: 1,074

## Next backlog priorities

1. Continue PAVOQUE angry annotations from `spike0009`, then exhaust angry and proceed through happy, neutral, poker, sad, and outtakes.
2. Preserve original utterance/style/text and all manually corrected segment timing; do not infer IPA where source mapping is not explicit.
3. Continue broader accepted-source backlog, especially observation-level files already inventoried but not yet mirrored.
4. Keep screening new public production deposits in parallel; ambiguous automatic/manual mixtures stay in review until the manual contribution is isolatable.
