# Ingestion + discovery audit — 2026-09-22 23:12 PT

## Backlog ingestion

Canonical `main` was checked before writing. `data/source_faithful/pavoque/` contained only the contiguous angry blocks `spike0001_0002` and `spike0003_0004`, so this run resumed from `spike0005` rather than trusting later-run summaries that were not present in the canonical tree.

Upstream authority: `marytts/pavoque-data`, `pavoque-angry.yaml`, blob SHA `bff79d978f740f6c2b09bc595ade03b6bdf33423`.

Ingested `spike0005` and `spike0006` into `data/source_faithful/pavoque/pavoque_angry_spike0005_0006_segments.csv`.

- spike0005: 42 segment rows; utterance [15.72, 20.16], duration 4.440 s; final deposited segment endpoint 4.435 s; residual 0.005 s.
- spike0006: 33 segment rows; utterance [20.16, 24.00], duration 3.840 s; final deposited segment endpoint 3.835 s; residual 0.005 s.
- total new observation rows: 75.
- original MaryTTS labels preserved exactly.
- segment starts are deterministic previous-end derivations and do not overwrite source endpoints.
- no IPA conversion was invented.
- endpoint sequences are monotonic and all derived durations are positive.
- terminal residuals are preserved rather than stretching final `_` intervals.

## Discovery pass

Repository-first/web screening covered manual segmentation/phonetic annotation, L2 production, articulatory/EMA, prosody and broad speech corpora.

### High-value unresolved candidate: CORPRES

`A Fully Annotated Corpus of Russian Speech` reports 60 h from 8 speakers, with six phonetic/prosodic annotation levels; 40% is manually segmented and fully annotated, including pitch marks, phonetic events, narrow/wide phonetic transcription, orthographic transcription and prosodic transcription. This is an excellent conceptual fit. It was **not admitted** in this run because current discovery did not establish a public observation-level deposit with sufficiently clear access/redistribution terms. Next action: locate authoritative corpus host/deposit and enumerate downloadable annotation/audio objects before registry promotion.

### Re-screened

- BAS manual-segmentation corpora: BAS explicitly lists PD1/PD2/VM2/SC10/CLIPS_MT_MANUAL as manually segmented resources. Need corpus-by-corpus public-access and primary-recording lineage checks before admission.
- HAMATAC: strong manual transcription/disfluency/phonetic-phenomena provenance but repository remains restricted.
- IFCASL: >50% manually corrected word/phone segmentation; observation-level public access still unresolved.
- MRPL2: 4,500 L2 English utterances with manual mispronunciation annotation, but files restricted.
- SAIT-EMA: primary synchronized EMA/audio is public, but phonetic boundaries are MFA-generated and not exhaustively human-verified; keep review-only unless isolatable manual QC labels are found.
- L2-ARCTIC: manual subset is clearly eligible in principle (3,599 utterances manually examined; corrected boundaries plus substitution/deletion/addition labels), but this source is already known to the project and was not duplicated.

## Integrity / continuation

No unrelated repository paths were modified. Source counts were not changed because no discovery candidate cleared both inclusion and access checks. STATUS row count increased by exactly 75 and logical-table count by one. Next canonical PAVOQUE target is `spike0007` onward, continuing contiguously from what is actually present on `main`; in parallel, prioritize object-level access resolution for CORPRES/BAS/IFCASL and archive-level RescueSpeech parsing.
