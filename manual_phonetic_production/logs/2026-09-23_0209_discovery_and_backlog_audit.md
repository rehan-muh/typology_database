# Manually Annotated Phonetic Production Database — ingestion/discovery audit

Timestamp: 2026-09-23 02:09 America/Los_Angeles
Scope: `manual_phonetic_production/` only.

## Backlog audit

Re-opened the canonical PAVOQUE source-faithful state before further promotion. `source_faithful/pavoque/ingestion_status.json` currently records 242 complete mirrored utterances, 29 promoted utterance rows, and 164 promoted segment intervals, with the durable angry-style source mirror ending inside `m0199`. This is materially different from older run summaries that described a simple `spike0001+` contiguous promotion path, so no potentially duplicative downstream promotion was written in this pass. The canonical status remains authoritative.

Verified existing source-faithful chunks around angry-style `spike0031`–`spike0035`; source labels/endpoints remain German SAMPA-like and are not to be silently converted to IPA. The next ingestion pass should promote records by checking namespaced observation IDs against canonical promoted tables first, rather than assuming the next `spike` number from an earlier run narrative.

## Fresh discovery

Repository-first/web sweep covered manual/manual-corrected speech segmentation, phonetic production, L2 production, articulatory production, and manually annotated event corpora.

### MRPL2 Non-native Speech Corpus — retain restricted/review status
Zenodo 20365865. 4,500 utterances, 23 non-native English speakers, 14 L1s. Record explicitly says each utterance is manually annotated for phonetic mispronunciations and includes annotated TextGrids plus expected/ground-truth phoneme sequences, but deposited files are restricted. Strong fit scientifically; no observation-level ingest possible without access.

### RescueSpeech — already-known accepted target; prioritize archive enumeration
Zenodo 8030657 (newer version linked by Zenodo). Primary German speech from simulated search-and-rescue exercises; record explicitly describes manually annotated recordings. Continue object-level archive enumeration rather than creating another registry-only source. Preserve clean original speech lineage separately from synthetic/noise-added enhancement derivatives.

### Spoken Wikipedia / German-English Code-Switching corpus — REVIEW, lineage concern
Zenodo 4434251 states that source Spoken Wikipedia audio is manually annotated at word and segment level in XML. However this is a resegmented subset/derivative of an existing corpus, so admission requires isolating genuinely new manual annotations contributed by the derivative study and deduplicating against underlying SWC recordings. Do not admit derivative audio merely because segmentation is manual.

### PodcastFillers — EXCLUDE from core
Zenodo 7121457 has 85,803 manually annotated audio events, but underlying podcast recordings are third-party SoundCloud media. This violates the database's third-party-media exclusion even though the annotations are human-created.

### PAVOQUE upstream re-verification
`marytts/pavoque-data` documentation/upstream YAML continues to expose optional manually corrected phonetic segments, with source-native labels and cumulative endpoints. Existing canonical source-faithful mirror/provenance should be extended, not replaced.

## QC / integrity decisions

- No unfamiliar source variables were dropped.
- No IPA values were invented.
- No automatic/forced-aligned boundaries were promoted as manual.
- No third-party-media corpus was admitted.
- No duplicate recording lineage was created.
- No files outside `manual_phonetic_production/` were modified.

## Next backlog priorities

1. Reconcile canonical PAVOQUE promoted observation IDs against the 242 mirrored complete utterances and promote unrepresented complete utterances/segments in bulk, preserving source endpoints and terminal residuals.
2. Enumerate RescueSpeech archive members and ingest accessible annotation/transcript metadata at observation level; reconcile published count discrepancies from actual members.
3. Attempt object-level access for IFCASL/CORPRES/BAS manually segmented corpora and record exact access/licensing outcomes.
4. Keep MRPL2 in restricted review until files become accessible.
5. For SWC/code-switching derivative, establish recording-level lineage and whether any new manual annotations are isolatable before admission.

## Sources checked

- https://zenodo.org/records/20365865
- https://zenodo.org/records/8030657
- https://zenodo.org/records/4434251
- https://zenodo.org/records/7121457
- https://github.com/marytts/pavoque-data
