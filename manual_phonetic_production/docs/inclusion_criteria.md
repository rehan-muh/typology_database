# Inclusion and exclusion criteria

## Required for core inclusion

1. **Primary collection**: recordings were collected by the depositing study/corpus team for that project, rather than drawn from a pre-existing speech database or third-party media archive.
2. **Production data**: natural or elicited human vocal production with acoustic and/or articulatory observations.
3. **Human grounding**: every relevant included token has boundaries, landmarks, labels, or measurements that were manually created, manually corrected, or explicitly verified by a human.
4. **Traceable provenance**: a paper, README, annotation manual, repository record, or author statement documents the annotation process.
5. **Stable source**: repository URL/DOI or other persistent identifier is recorded.

## Accepted provenance states

- `MANUAL_FROM_SCRATCH`
- `AUTO_THEN_ALL_CORRECTED`
- `AUTO_THEN_ALL_VERIFIED`
- `MANUAL_MEASUREMENT_ONLY`

## Rejected provenance states

- `AUTO_UNVERIFIED`
- `AUTO_SPOT_CHECKED`
- `AUTO_LOW_CONFIDENCE_ONLY_CORRECTED`
- `PROVENANCE_UNCLEAR`

## Primary-data exclusions

- Pre-existing speech/phonetic database reused by a later study.
- Broadcast, YouTube, podcast, or SoundCloud material not collected by the research team (tracked as secondary-media sources, not core).
- Synthetic/TTS speech.
- Perception-only data.
- Pure forced alignment or ASR-derived boundaries without exhaustive correction/verification.

## Mixed pipelines

Eligibility is assessed at the tier/measurement level. Example: forced-aligned word boundaries plus manually placed VOT burst/voicing landmarks means the VOT landmarks may qualify while uncorrected phone durations do not.
