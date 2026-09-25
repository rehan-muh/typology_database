# Ingestion audit — Phonetic Corpus of Estonian Spontaneous Speech (EKSKFK)

source_id: EKSKFK_V1_2
status: ACCEPTED_METADATA_FILE_MANIFEST_PENDING_OBJECT_FETCH
source_title: Phonetic Corpus of Estonian Spontaneous Speech v1.2
doi: 10.23673/RE-293
repository: DataDOI / University of Tartu
language: Estonian
primary_recordings: yes
singing: no
manual_annotation_basis: repository metadata explicitly states manual transcription of words and phonemes and detailed segment boundaries
speakers_reported: 205
audio_hours_reported: 134
annotated_hours_reported: 106
word_intervals_reported: 914000
recording_style: spontaneous dialogues; studio/field recordings; separate channels per speaker
lineage_note: primary corpus recordings; do not merge later derived studies as independent recording lineages
repository_migration: legacy DataDOI handle now redirects to Dataverse; DOI remains authoritative

## Indexed public objects observed
- EKSKFK_words_by_IPU_full_corpus.txt — 12.37 MB — text representation of corpus
- EKSKFK_doc.zip — 21.64 KB — metadata/documentation
- SKK0_keypoints.zip — 12.00 GB — OpenPose JSON; automatic computer-vision derivative, EXCLUDE from manual core
- SKK3_keypoints.zip — 1.841 GB — OpenPose JSON; automatic computer-vision derivative, EXCLUDE from manual core
- audio and phonetic annotation archives are described by the deposit but require re-enumeration at the migrated Dataverse endpoint before checksums/object counts are asserted

## Source-faithful variable dictionary seed
source_id,file/table,original_variable,standardized_variable,variable_domain,description/meaning,units,datatype,coding/levels,missing_value_conventions,measurement_annotation_method,time_reference_window,anatomical_acoustic_target,provenance,notes
EKSKFK_V1_2,TextGrid/tier,word,word_label,lexical_annotation,orthographic word interval,,string,source orthography,source-specific,manual transcription,interval,spoken word,DataDOI v1.2,retain original label exactly
EKSKFK_V1_2,TextGrid/tier,phoneme,segment_label,segment_annotation,phoneme interval,,string,source phonetic transcription,source-specific,manual phoneme transcription/segmentation,interval,speech segment,DataDOI v1.2,do not invent IPA mapping
EKSKFK_V1_2,TextGrid/tier,xmin,start_time_s,temporal,interval start,seconds,float,,,manual boundary placement,recording time,speech boundary,DataDOI v1.2,retain raw value
EKSKFK_V1_2,TextGrid/tier,xmax,end_time_s,temporal,interval end,seconds,float,,,manual boundary placement,recording time,speech boundary,DataDOI v1.2,retain raw value
EKSKFK_V1_2,metadata,speaker,speaker_id,participant,speaker identifier,,string,,,source metadata,,,participant,DataDOI v1.2,namespace as EKSKFK_V1_2::speaker
EKSKFK_V1_2,metadata,age,age,demographic,speaker age,years,numeric,,,source metadata,,,participant,DataDOI v1.2,preserve source granularity
EKSKFK_V1_2,metadata,recording,recording_id,recording,recording/session identifier,,string,,,source metadata,,,recording,DataDOI v1.2,namespace as EKSKFK_V1_2::recording

## Ingestion state
Discovery completed against authoritative/indexed repository metadata. Object-level backlog ingestion was attempted, but the legacy handle currently redirects to the new Dataverse landing page and the current web surface did not expose stable object download URLs. No annotation rows are fabricated. Next pass should resolve DOI 10.23673/RE-438 (v1.3) first, enumerate its Dataverse files/checksums, then prefer v1.3 while retaining v1.2 lineage/version provenance. Parse every accessible TextGrid tier and every source metadata field; exclude OpenPose keypoints from manual core unless used only as explicitly automatic derivatives.

## Deduplication / QC
v1.2 and v1.3 are versions of the same corpus lineage, not independent datasets. Derived publications using EKSKFK must point to this lineage. Automatic OpenPose keypoints are not manual phonetic annotations.
