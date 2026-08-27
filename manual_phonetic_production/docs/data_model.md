# Data model

The harmonized database uses a relational hierarchy:

`study -> dataset -> speaker -> recording -> utterance -> word -> syllable -> segment -> landmark -> measurement`

## Required provenance fields on every derived observation

- `source_id`
- `source_recording_id`
- `source_annotation_id`
- `annotation_provenance`
- `manual_scope`
- `measurement_origin` (`ORIGINAL` or `RECOMPUTED`)
- `source_url`
- `source_license`
- `retrieved_at`

## Segment table

Recommended fields:

`source_id, dataset_id, speaker_id, recording_id, utterance_id, language, glottocode, variety, task, style, word, syllable, segment_original, segment_ipa, start_s, end_s, duration_s, annotation_provenance, annotator, source_license`

## Landmark table

Recommended fields:

`source_id, recording_id, token_id, landmark_type, time_s, manual_scope, annotation_provenance, definition, annotator`

## Measurement table

Recommended long format:

`source_id, token_id, measure, value, unit, time_normalized, algorithm, settings_json, measurement_origin, manual_verification`
