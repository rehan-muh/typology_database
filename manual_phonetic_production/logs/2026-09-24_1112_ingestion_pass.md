# MPPD ingestion pass — 2026-09-24 11:12 PT

## Discovery: TaL Corpus
Decision proposed: INCLUDE_MANUAL_SUBSET.

Authoritative UltraSuite documentation identifies the Tongue and Lips (TaL) corpus as primary synchronized articulatory/acoustic production from 82 native English speakers: TaL1 (1 professional voice talent, six sessions) and TaL80 (81 speakers). Core objects include prompt .txt, waveform .wav, hardware synchronization .sync, raw ultrasound .ult + .param, and synchronized lip video .mp4. TaL1/core is 49 GB and TaL80/core is 498 GB.

Crucially, spontaneous utterances (tag spo) can be up to 60 s and were manually annotated into shorter, typically 5–10 s segments. The manual annotation is distributed as .lab CSV with start time, end time, and transcription. This is an isolatable manually annotated layer over primary recordings and satisfies MPPD inclusion for that layer. Do not infer manual phone boundaries for other prompt types.

Proposed source_id: tal_corpus_2021.
Source: https://ultrasuite.github.io/data/tal_corpus/
Paper: Ribeiro et al. 2021, SLT, DOI 10.1109/SLT48900.2021.9383532.
Lineage: TaL1 and TaL80 are independent datasets but share some prompts; this is stimulus overlap, not duplicate recordings.
Backlog: enumerate all .lab files first via rsync; ingest segment rows with source_id::speaker/session::utterance::segment IDs; preserve raw start/end/transcription; link to corresponding .wav/.ult/.param/.sync/.mp4 manifests without committing bulk media.

## Discovery: AusKidTalk
Keep in REVIEW / access-restricted backlog, not public core ingest. 620 Australian-English-speaking children completed five production tasks. Task 1 has 139 elicited targets. 461 files were manually transcribed/corrected (403 ASR-assisted + 58 from scratch); a 380-child sample yielded 61,371 target words from 85,436 reviewed intervals. The correction workflow outputs clean corrected TextGrids and CSV rows with label/start/end and blocks inconsistent edits. Data are available only under a custodian/request model, not as a public deposit. Do not ingest unavailable observations or fabricate filenames.

Source: https://doi.org/10.1007/s10579-026-09929-5

## Exclusion/review notes
UrduSpeech remains unsuitable for automatic admission from the surfaced evidence: the 156 h corpus is LLM-curated from heterogeneous categories and primary-recording lineage is unresolved; only a 9 h benchmark is described as manually corrected.
PINC is third-party European Parliament media and therefore fails the primary-recording rule.
Brain Treebank is perception/neural data over Hollywood movie audio, not primary speech production.

## Next backlog priorities
1. TaL: enumerate and parse .lab manual segment files; create manifests for linked multimodal objects without mirroring 547 GB media.
2. PAVOQUE: exhaustively parse all five eligible style YAMLs.
3. L2-ARCTIC: isolate and parse human-reviewed TextGrids only.
4. CORPRES: locate downloadable manually segmented 40% and six annotation tiers.
5. AusKidTalk: retain metadata/review record unless public research-access files become directly obtainable.
