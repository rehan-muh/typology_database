# Ingestion/discovery audit — 2026-09-17 23:07 -0700

## Backlog ingestion completed

### PAVOQUE angry: recovery of spike0009–spike0011

Directly re-read `marytts/pavoque-data/pavoque-angry.yaml` at blob `bff79d978f740f6c2b09bc595ade03b6bdf33423` and source-faithfully ingested the three utterances that had previously been quarantined after the source-fidelity failure.

- utterances added: 3 (`spike0009`, `spike0010`, `spike0011`)
- manually corrected segment endpoints added: 83
- original labels retained verbatim
- original utterance text/style/start/end retained
- no IPA mapping attempted
- no normalized or inferred timing overwrote source values
- all endpoint sequences checked monotonic
- all final endpoints fall within corresponding utterance duration

This closes the explicit `spike0009`–`spike0011` recovery gap. Existing verified `spike0012`–`spike0017` remain untouched. Durable next angry-style continuation point: `spike0018`.

## Discovery

### English and Spanish Vowel Formants from DIAPIX-FL — Zenodo 14411925

Repository record inspected directly. Public file: `vowels.txt`, 2.6 MB, MD5 `7dfb94e5fb0c7845db1ec33fd1350289`, CC BY 4.0. The deposit describes one row per vowel and explicitly documents variables `l1`, `speaking`, `speaker`, `frag`, `nwords`, `vowel`, `word`, `length`, `en`, `f0`, `f1`, `f2`, `f3`; `length` is in 10-ms frames. This is broad, potentially useful L1/L2 conversational production material.

**Admission decision: EXCLUDE the full 2024 vowel-measurement table from the manual core.** A 2026 methods description of the same derived dataset states that vowel segments were extracted after automatic Montreal Forced Aligner alignment. It separately reports a manually boundary-annotated validation subset of 1,043 Spanish vowels, but the Zenodo table does not identify those rows as a separable manual layer. Therefore admitting the 53k+ derived vowel table would violate the manual/manual-corrected/human-verified boundary criterion. Do not infer that validation of a subset human-verifies the entire automatic table.

Potential salvage path: locate a public object containing the 1,043 manually bounded Spanish validation vowels or row identifiers linking them unambiguously into `vowels.txt`. If found, ingest only that isolatable manual subset, preserving duration/F1/F2/F3 and all contextual columns.

## Integrity / lineage safeguards

- No unrelated repository paths modified.
- No automatic DIAPIX-FL vowel rows admitted.
- PAVOQUE source SHA pinned and actual upstream values re-read before writing.
- Namespaced source identity retained (`pavoque` + source prompt).
- Existing PAVOQUE records were not overwritten.

## Next backlog priorities

1. Continue PAVOQUE angry from `spike0018` using direct source verification.
2. L2-ARCTIC `/annotation` manual layer: obtain/parse package if publicly reachable; never substitute `/textgrid` forced alignments.
3. Tang–Parrell–Niziolek OSF tables: enumerate every object and ingest trial/formant/timing variables.
4. Russian Fricatives: parse manually corrected session TextGrids and measurement tables.
5. Estonian spontaneous-speech corpus: resolve current Dataverse package and ingest manual word/phone/syllable/prosody/voice-quality tiers.
6. Search specifically for the DIAPIX-FL 1,043-vowel manual validation subset; admit only if isolatable.
