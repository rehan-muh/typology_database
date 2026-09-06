# Canonical vowel-coarticulation analysis schema

The scientific target of this subtree is now **coarticulatory displacement of vowel F1 and F2 only**. Other acoustic measures (F0, A1-P0, CPP, spectral tilt, VOT, duration, etc.) may be retained as source metadata/covariates but are not target outcomes.

## Core estimands

Every analysis should target one or more of:

1. **MAGNITUDE** — contextual displacement of vowel F1/F2 relative to a context-neutral or internally matched reference.
2. **TEMPORAL EXTENT** — the trajectory of that displacement over normalized vowel time, including onset/offset, peak location, decay/growth, and optionally area under the absolute contextual-effect curve.
3. **FLEXIBILITY** — within-speaker changes in magnitude or temporal extent across speaking style, rate, task, language mode, or other moderators.

For C→V effects, prioritize early-vowel F1/F2 and contrasts in preceding consonant place/manner. For anticipatory effects of following consonants, prioritize late-vowel F1/F2. For V→V carryover and anticipatory effects, retain adjacent/following vowel identity and use early/late trajectory regions as appropriate.

Midpoint-only F1/F2 data can support **MAGNITUDE** when contextual predictors are recoverable, but cannot identify **TEMPORAL EXTENT**.

## Analysis hierarchy

Every observation preserves:

`study/source -> dataset -> language -> speaker -> recording -> utterance -> target vowel token -> time point`

Speaker IDs are globally namespaced as `source_id::source_speaker_id`. Bilingual speakers retain one speaker UID; each token retains its actual production language when supplied. Study/source is modeled separately from language because protocol and language are often partially confounded.

## Canonical tables

### 1. `coarticulation_tokens.csv`

One row per target vowel token. Required identifiers are:

- `source_id`
- `dataset_id`
- `speaker_uid`
- `speaker_source_id`
- `language`
- `glottocode`
- `recording_id`
- `utterance_id`
- `token_id`

Core phonetic/context fields are:

- `prev_segment_ipa`, `target_segment_ipa`, `next_segment_ipa`
- `prev_start_s`, `prev_end_s`
- `target_start_s`, `target_end_s`
- `next_start_s`, `next_end_s`
- `target_duration_ms`
- stress, syllable/word position, preceding/following vowel identity where available
- source-native context labels when canonical IPA cannot be established without inference

Missing IPA/context remains empty/NA. Never reconstruct IPA from orthography unless the source provides a documented mapping.

Recommended moderators include speaking rate, style, task, bilingual/language mode, clinical status, age, sex/gender, and other demographics supplied by the source.

### 2. `coarticulation_trajectories.csv`

One row per target vowel token × F1/F2 × normalized time point.

Required fields:

- `source_id`, `dataset_id`, `speaker_uid`, `token_id`
- `measure` (`F1_HZ` or `F2_HZ` for target analyses)
- `time_norm` in [0,1]
- `time_s` where recoverable
- `value`, `unit`
- `measurement_origin` = `ORIGINAL` or `RECOMPUTED`
- `algorithm`, `settings_json`
- `manual_verification`
- `quality_flag`
- `source_measure_name`

For newly re-extracted trajectories, use standardized samples at 0.05, 0.10, ..., 0.95 of the manually verified vowel interval unless source-specific constraints require otherwise. Existing source trajectories remain at their native measurement points/windows. If a source reports windows rather than points, retain the native window bounds and use the window midpoint as `time_norm`.

### 3. `coarticulation_events.csv`

This table is retained only to preserve manual/human-corrected segmentation landmarks needed to anchor vowel acoustics. Relevant canonical events include `SEGMENT_ONSET` and `SEGMENT_OFFSET`; other source landmarks may remain as provenance/covariates but are not target outcomes.

## Eligibility tiers

A source is eligible only when the relevant target-vowel boundaries, adjacent segment labels/context, or original acoustic measurements were manually created or exhaustively human-verified/corrected.

- **READY** — released F1/F2 plus sufficient source context for at least one contextual analysis.
- **REEXTRACT** — audio plus valid manual/human-corrected vowel/phone boundaries permit standardized F1/F2 extraction.
- **POSSIBLE** — F1/F2 exist but contextual mapping requires further verified source documentation.
- **NOT_SUPPORTED** — no defensible F1/F2 vowel-coarticulation analysis can be constructed.
- **RESTRICTED** — potentially eligible but files are not currently accessible.
- **SPECIALIZED** — retained only for a non-default domain sensitivity analysis (e.g. singing).

## Source prioritization

Highest priority goes to sources with:

1. speaker ID and language;
2. manually verified vowel or phone boundaries;
3. explicit preceding/following segment or vowel context;
4. F1 and F2 at three or more within-vowel time points, or audio permitting re-extraction;
5. repeated contexts or moderator conditions within speakers.

Midpoint-only datasets are secondary because they estimate magnitude but not temporal extent.

## Pooling rules

Default pooled analyses include ordinary speech and retain explicit domain indicators for L2, bilingual, and clinical data so sensitivity analyses can exclude them. Singing sources are not mixed into default speech analyses. Single-speaker sources can contribute token-level evidence but cannot identify population speaker variance independently.

## Future ingestion contract

Every accepted source should receive:

1. a provenance registry entry;
2. a source-capability assessment;
3. a mapping from source variable names to canonical fields;
4. canonical token rows when enough metadata exist;
5. canonical `F1_HZ`/`F2_HZ` trajectory rows for usable measurements;
6. event rows only where manual landmarks help anchor vowel acoustics;
7. validation with `scripts/validate_coarticulation.py`.

Do not force a source into the schema by inventing phones, IPA, contexts, speakers, or acoustic measurements. Preserve source-native labels whenever canonicalization would otherwise require inference.
