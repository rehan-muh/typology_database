# Manual phonetic production ingestion — 2026-09-09 20:07 PDT

## Backlog ingestion
- Source: `voxangeles_2024`
- Authoritative upstream: `pacscilab/voxangeles:data/phonetic_measurements/voxangeles_meanf0_file.tsv`
- Immutable upstream blob: `9492dd2ed35044219aed483613fd3f7a44f292d3`
- Added source-faithful rows 1656–1755: 100 observations.
- Added source-faithful rows 1756–1855: 100 observations.
- New durable cumulative coverage: source lines 2–1855 = 1,854 observations.
- Next exact continuation: source line 1856.
- Original recording IDs and numeric strings preserved verbatim.
- No unaudited forced-alignment material admitted.

## Discovery
Fresh screening targeted public manually annotated/corrected phonetic-production resources across repository and web search. PAVOQUE reappeared and is already tracked/ingested. L2-ARCTIC was re-screened: its manual subset includes corrected word/phone boundaries plus substitution/deletion/addition labels, but its broader corpus remains forced aligned; no duplicate registry entry was added. Recent manually corrected speech corpora surfaced in search, but none provided sufficient evidence in this pass for a new, isolatable phonetic measurement/interval layer meeting the core rule, so no weak registry-only record was added.

## Validation and provenance
- Both newly materialized chunks were fetched from the same immutable upstream blob as the prior mirror.
- Previous durable endpoint was line 1655; new chunks begin at 1656 and are contiguous/non-overlapping.
- Source manifest updated to `partial_ingested_lines_2_1855_1854_rows`.
- Source ingestion status updated to 1,854 rows and next line 1856.
- Global warehouse status advanced by exactly 200 rows.
- Known blocker remains unchanged for the large UTF-16 VoxAngeles duration and full decile trajectory TSVs; those rows remain uncounted until byte-capable retrieval succeeds.

## Warehouse state after this pass
- Sources tracked: 128
- Accepted: 42
- Excluded: 25
- Review: 61
- Materially ingested sources: 42
- Parsed rows: 1,357,809
- Logical tables: 84
- File-manifest records: 922
- Variable-dictionary records: 1,074

## Next priorities
1. Continue exact VoxAngeles mean-F0 mirroring from source line 1856 while the large-file blocker persists.
2. Prioritize a byte-capable path for complete phone/word durations and all 10-point F0/F1–F3 trajectories.
3. Continue PAVOQUE durable mirroring from its recorded continuation point and exhaust all styles.
4. Continue repository-first discovery for manually verified VOT, vowel/formant, voice-quality, prosodic, articulatory, aerodynamic, EGG, ultrasound, and clinical-production deposits.
