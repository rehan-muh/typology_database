# Manual phonetic production ingestion/discovery audit — 2026-09-19 00:10 PDT

## Backlog / lineage integrity

Re-audited PAVOQUE against the authoritative upstream `marytts/pavoque-data/pavoque-angry.yaml` (blob `bff79d978f740f6c2b09bc595ade03b6bdf33423`). Upstream documentation states that segment labels/endpoints are manually corrected. The durable source-faithful mirror already contains 50 chunks, 182 utterances, and 5,729 intervals through literal upstream record `m0136`; its correct next cursor is `m0137`.

A critical deduplication issue was identified: later spike-specific files (`spike0001` through `spike0019`) are re-materializations/reverification of observations from the same PAVOQUE recording lineage and therefore must not be added to scientific observation totals. The ingestion-status file was updated with an explicit duplicate-lineage guard. The apparent prompt-number gap between `spike0019` and `spike0021` remains a source-native gap and is not evidence of missing data. Future durable ingestion must resume from literal upstream record `m0137`, not from `spike0021`.

No source observations were deleted: source-faithful historical artifacts remain immutable evidence, but downstream counts/views must deduplicate them by PAVOQUE source lineage + utterance/prompt + segment order/timing.

## Discovery

Added `ifcasl_2016` to review. Trouvain et al. (LREC 2016) describe a primary French–German bilingual learner corpus with roughly 100 speakers, word- and phone-level segmentation, and more than 50% manually corrected data. Project documentation independently states that automatic speech-text alignment was followed by manual checking/annotation for French and German, native and non-native speech. This satisfies study-level inclusion logic, but this pass did not locate a public observation-level deposit that cleanly identifies the manually corrected subset, so IFCASL is not admitted to core yet.

Also rechecked CORPRES: 60 hours, 8 speakers, six annotation levels, with 40% manually segmented and fully annotated. It remains review until the manually segmented 40% can be isolated in accessible files.

## Validation / next priorities

1. PAVOQUE: continue durable source-faithful parse at `m0137`; do not count spike-specific reverification files as new observations.
2. IFCASL: locate institutional/ELRA/CLARIN data deposit and a file/subset-level manual-correction indicator; ingest all public corrected phone/word tiers if found.
3. CORPRES: locate distributable annotation files and isolate the manually segmented 40%.
4. Continue L2-ARCTIC human-examined `/annotation` subset and JSUT from their true durable cursors rather than old convenience cursors.

All changes in this pass are confined to `manual_phonetic_production/`.
