# Ingestion + discovery audit — 2026-09-18 20:07 -0700

## Backlog ingestion: PAVOQUE

Continued the accepted PAVOQUE angry-style annotation stream from the established cursor `spike0015` through `spike0016` using upstream `pavoque-angry.yaml`, immutable blob SHA `bff79d978f740f6c2b09bc595ade03b6bdf33423`.

- `spike0015` — *Bist du noch da?* — 13 source segments; utterance 49.92–52.38 s; final source-relative endpoint 2.455 s vs utterance span 2.460 s.
- `spike0016` — *Gibt es noch etwas, das du sagen willst?* — 33 source segments; utterance 52.38–56.28 s; final source-relative endpoint 3.895 s vs utterance span 3.900 s.
- Total newly ingested source-faithful observations: **46**.
- Source labels and cumulative endpoints were copied without normalization. No IPA was inferred. Source-level timing residuals (5 ms) are preserved, not silently repaired.
- Next PAVOQUE angry cursor: **spike0017**.

Source-faithful file: `data/source_faithful/pavoque_angry_spike0015_0016_2026-09-18_2007.csv`.

## Discovery / qualification audit

### RescueSpeech — retain in REVIEW, now with stronger file-level metadata
Zenodo record `10.5281/zenodo.8030657` describes authentic German speech from simulated search-and-rescue exercises and explicitly calls the recordings manually annotated. The ASR portion reports 2,412 clean utterances, 1:36:10 total duration, 26 speakers, 44.1-kHz original capture downsampled to 16 kHz. Public archive `Task_ASR.tar.gz` is 628.8 MB with MD5 `fd4fa71002f669964f616af83865ba51`; `Readme.md` MD5 is `c10f41429261b89c9eea7b6f8bbc4a33`. The enhancement archive contains synthetic/noise-augmented derivatives and is not eligible as primary production observations. Keep RescueSpeech in review until the ASR archive's annotation/transcript files are enumerated and the exact manually created/corrected layer can be isolated. Do not admit synthetic noisy copies.

### MRPL2 — qualifying study, observation ingest blocked by access
Zenodo `10.5281/zenodo.20365865` reports 4,500 utterances from 23 non-native speakers / 14 L1s, each manually annotated for phonetic mispronunciations, with TextGrids and expected/ground-truth phoneme sequences. Files are restricted. Preserve as access-blocked; do not fabricate observation rows.

### German-English Code-Switching Speech Corpus — excluded from primary core
Zenodo `10.34777/bkr1-ay03` resegments a subset of the pre-existing Spoken Wikipedia Corpus. Although underlying audio is manually annotated at word and segment level, the recording lineage is secondary and the new code-switching extraction is not a new isolatable manual phonetic annotation layer. Retain exclusion at recording-lineage level.

## Integrity checks

- PAVOQUE IDs are namespaced by source/prompt/segment index in downstream harmonization; this source-faithful shard retains the original prompt and segment index.
- Endpoints are monotonic within both newly ingested utterances.
- No negative durations implied by the endpoint sequences.
- Upstream blob SHA stored on every source-faithful row.
- No raw audio added.
- No files outside `manual_phonetic_production/` modified.

## Next backlog priorities

1. PAVOQUE angry `spike0017+` and then continue across remaining styles while preserving source style and immutable blob SHA.
2. RescueSpeech: enumerate `Task_ASR.tar.gz` contents if repository tooling permits; isolate transcripts/annotation files from audio and synthetic derivatives.
3. Continue JSUT from the repository's actual latest ingested cursor, not historical cursors.
4. L2-ARCTIC human-examined subset: ingest only human-corrected word/phone boundaries and error labels where publicly/legally retrievable.
5. CORPRES: locate a file-level partition for the reported manually segmented 40% before admission.
6. Continue discovery in Journal of Phonetics, Laboratory Phonology, Phonetica, JIPA, JASA, Language and Speech, Speech Communication, Language Variation and Change, JSLHR, OSF, Zenodo, GitHub, and DataCite-linked deposits.
