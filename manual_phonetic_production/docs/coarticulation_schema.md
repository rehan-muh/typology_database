# Canonical coarticulation analysis schema

This project now treats the following ten phenomena as the only primary coarticulation targets:

1. `VV_CARRYOVER` — V→V carryover
2. `VV_ANTICIPATORY` — V→V anticipatory
3. `CV_PLACE` — consonant-to-vowel place effects
4. `VC_EFFECT` — vowel-to-consonant acoustic effects
5. `NASAL` — nasal coarticulation
6. `LARYNGEAL` — laryngeal coarticulation
7. `VOT_VOWEL` — VOT/following-vowel interaction
8. `LABIALIZATION` — rounding/labialization coarticulation
9. `RHOTIC_LATERAL` — rhotic/lateral effects on adjacent vowels
10. `TEMPORAL` — temporal coarticulation from segment durations and boundary timing

Speech rate, speaking style, task, age, sex/gender when supplied, bilingual status, clinical status, and similar variables are covariates/moderators, not separate coarticulation outcomes.

## Analysis hierarchy

Every analysis-ready observation must preserve:

`study/source -> dataset -> language -> speaker -> recording -> utterance -> target token -> time point/event`

Speaker IDs are globally namespaced as `source_id::source_speaker_id`. Bilingual speakers retain one speaker UID while each token receives its actual production language and Glottocode. Study/source is always modeled separately from language because protocol and language are often partially confounded.

## Canonical tables

### 1. `coarticulation_tokens.csv`

One row per target segment token. It stores the target plus immediately adjacent phonetic context, segment timing, speaker/language/study identifiers, and experimental covariates.

Required identifiers:

- `source_id`
- `dataset_id`
- `speaker_uid`
- `speaker_source_id`
- `language`
- `glottocode`
- `recording_id`
- `utterance_id`
- `token_id`

Required phonetic context:

- `prev_segment_ipa`, `target_segment_ipa`, `next_segment_ipa`
- `prev_start_s`, `prev_end_s`
- `target_start_s`, `target_end_s`
- `next_start_s`, `next_end_s`
- `target_duration_ms`

Recommended derived context features:

- vowel/consonant class
- place and manner
- laryngeal class
- nasal status
- labial/rounded status
- rhotic/lateral status
- vowel height/backness/rounding
- stress, syllable position, word position

Missing context is represented as empty/NA, never inferred from orthography unless a documented source-to-IPA mapping exists.

### 2. `coarticulation_trajectories.csv`

One row per token × acoustic measure × time point. This is the primary input for trajectory GAMMs/hierarchical models.

Required fields:

- `source_id`, `dataset_id`, `speaker_uid`, `token_id`
- `measure`
- `time_norm` on [0,1] relative to the target interval
- `time_s` where recoverable
- `value`, `unit`
- `measurement_origin` = `ORIGINAL` or `RECOMPUTED`
- `algorithm`, `settings_json`
- `manual_verification`
- `quality_flag`

Canonical measure vocabulary includes:

`F0_HZ`, `F0_ST`, `F1_HZ`, `F2_HZ`, `F3_HZ`, `H1H2_DB`, `H2H4_DB`, `CPP_DB`, `A1P0_DB`, `A1P1_DB`, `NASALANCE`, `RMS_DB`, `COG_HZ`, `SPECTRAL_SLOPE_DB_OCT`, `SPECTRAL_SKEWNESS`, `SPECTRAL_KURTOSIS`, `BURST_PEAK_HZ`.

Original source variable names are retained in `source_measure_name`.

For newly extracted trajectories, default normalized sampling points are 0.05, 0.10, ..., 0.95 of the target interval. Existing source trajectories are retained at their native sample points and may later be interpolated only in analysis code.

### 3. `coarticulation_events.csv`

One row per temporal landmark or interval event. This supports VOT and temporal analyses and anchors acoustic measurements to manually verified segmentation.

Canonical event vocabulary:

`SEGMENT_ONSET`, `SEGMENT_OFFSET`, `CLOSURE_ONSET`, `CLOSURE_OFFSET`, `BURST`, `VOICING_ONSET`, `FRICATION_ONSET`, `FRICATION_OFFSET`, `ASPIRATION_ONSET`, `ASPIRATION_OFFSET`, `NASAL_ONSET`, `NASAL_OFFSET`.

Events may be point landmarks (`event_time_s`) or intervals (`event_start_s`, `event_end_s`). Each event retains annotation provenance, manual scope, and whether it was original or recomputed.

## Eligibility rules by phenomenon

### `VV_CARRYOVER`
Target must be a vowel and preceding segment/context must contain a vowel. Preferred evidence is target F1/F2 trajectory with >=3 time points; analysis emphasizes early target time.

### `VV_ANTICIPATORY`
Target must be a vowel and following segment/context must contain a vowel. Preferred evidence is target F1/F2 trajectory with >=3 time points; analysis emphasizes late target time.

### `CV_PLACE`
Target vowel must have a preceding consonant whose place is recoverable. Preferred measures are early-vowel F2/F3 trajectories, approximately the first 30% of the vowel.

### `VC_EFFECT`
Target consonant must have a preceding vowel whose identity/features are recoverable. Preferred consonant measures are burst peak/spectrum for stops and COG/slope/skewness/kurtosis for fricatives.

### `NASAL`
Target is normally a vowel adjacent to a nasal/oral contrast. Preferred measures are A1-P0, A1-P1, nasalance, and/or a validated nasalization measure across normalized vowel time.

### `LARYNGEAL`
Target vowel follows a consonant with recoverable laryngeal category. Preferred early-vowel measures are F0, H1-H2, CPP, and related voice-quality trajectories.

### `VOT_VOWEL`
Requires stop release/burst and voicing-onset landmarks or an original manually verified VOT value, plus following-vowel acoustics and/or duration. VOT is derived from event timing when both landmarks are present.

### `LABIALIZATION`
Requires an adjacent segment with recoverable labial/rounded/labialized status. Preferred target-vowel evidence is F2/F3 trajectory.

### `RHOTIC_LATERAL`
Requires adjacent rhotic/lateral identity. Preferred target-vowel evidence is F2/F3 trajectory, with F3 particularly important for rhotic effects.

### `TEMPORAL`
Requires manually produced or exhaustively human-corrected segment boundaries. Outcomes include target duration, adjacent-segment duration, inter-landmark intervals, normalized timing, and overlap/proximity measures that can be justified from the annotation scheme.

## Pooling rules

A source may be accepted into MPPD but excluded from a particular coarticulation analysis. Eligibility is determined per phenomenon and per annotation/measurement tier.

Default pooled speech analyses exclude specialized singing data and retain clinical or L2 sources with explicit domain indicators so sensitivity analyses can include/exclude them. Single-speaker datasets may contribute token-level evidence but cannot independently identify speaker-level variance.

## Future ingestion contract

Every newly accepted source must receive:

1. a registry entry with provenance;
2. a source-capability assessment for all ten phenomena;
3. a mapping from source variable names/labels to canonical fields;
4. analysis-ready token/context rows when enough metadata exist;
5. trajectory rows for any usable acoustic measure;
6. event rows for any usable landmarks/intervals;
7. explicit `NOT_SUPPORTED` rather than silently missing data for unsupported phenomena.

Do not force a source into the schema by inventing phones, contexts, speaker IDs, or acoustic measures. If raw audio plus valid manual boundaries allow a missing measure to be recomputed, mark the capability `REEXTRACT`; if the needed context/boundary is absent, mark it `NOT_SUPPORTED`.