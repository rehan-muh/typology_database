# Manually Annotated Phonetic Production Database — ingestion pass

Timestamp: 2026-09-10T01:11:18-07:00

## Backlog ingestion

- Source: `voxangeles_2024`.
- Authoritative upstream: `pacscilab/voxangeles`, commit `e30c638a8a2c22e576f871f0e2044780d56eab82`, blob `9492dd2ed35044219aed483613fd3f7a44f292d3`.
- Parsed and durably committed exact source lines 2656–2855 from `data/phonetic_measurements/voxangeles_meanf0_file.tsv`.
- New observations: 200.
- Durable VoxAngeles mean-F0 coverage: 2,854 observations, exact source lines 2–2855.
- Next deterministic continuation: source line 2856.
- Original recording IDs and original numeric strings retained verbatim.
- No unaudited forced-alignment branch material admitted.
- Read-back validation succeeded; committed tail ends `hun-001-056 = 116.37760796589541`, matching authoritative upstream line range.

## Discovery

Fresh searches covered OSF, Zenodo, GitHub, Journal of Phonetics and Laboratory Phonology oriented queries, with automatic-only annotation tools screened out under the inclusion rule.

### New HIGH-priority review source

`schertz_khan_2020_hindi_urdu` — Schertz & Khan (2020), *Acoustic cues in production and perception of the four-way stop laryngeal contrast in Hindi and Urdu*, Journal of Phonetics 81, 100979.

- Public OSF project: https://osf.io/qxpbg/
- Primary Hindi/Urdu stop-production experiment.
- Production measures include prevoicing duration, aspiration duration, voice quality/breathy-voice cues, and f0.
- Kept in REVIEW rather than core because the currently surfaced sources do not yet establish that the acoustic landmarks/measurements were manually created, manually corrected, or exhaustively human-verified.
- Before admission: enumerate OSF files, verify annotation/measurement provenance from methods/readme, and isolate production observations from perception materials.

## Accounting after pass

- Tracked sources: 130
- Accepted: 42
- Excluded: 25
- Review: 63
- Materially ingested sources: 42
- Parsed rows: 1,358,809
- Logical tables: 84
- File-manifest records: 928
- Variable-dictionary records: 1,085

## Remaining highest-priority backlog

1. Continue VoxAngeles mean-F0 from source line 2856.
2. Retrieve and mirror the complete VoxAngeles phone/word duration table and 10-point F0/F1–F3 trajectories through a byte-capable UTF-16 path; current connector does not expose usable bytes for those large files.
3. Continue durable PAVOQUE manual segment/utterance mirroring.
4. Resolve observation-level files and manual-provenance questions for Schertz–Khan Hindi/Urdu, Gorba–Cebrian VOT, Tibetan trilingual diphthongs, Plastic Mandarin tones, KEC/EMA, IFCASL and other HIGH-priority review sources.

All writes in this pass were confined to `manual_phonetic_production/`.
