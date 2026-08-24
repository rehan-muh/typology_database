# PHONOTACTICS/DISTRIBUTION shard — 2026-08-23 run 1

Branch: `agent/phonotactics-worker-20260823-1754`

## Staged records

- Batch 01 — Kuo Māori + Malagasy: 14 records
- Batch 02 — Dai English + Polish + Turkish: 16 records
- Batch 03 — Smith positional initial-onset cases: 8 records
- Total new atomic records: **38**
- Source works represented: **4** (`kuo2023_dissertation`, `kuo2024_malagasy_phonology`, `dai2025_exception_filtering`, `smith2002_dissertation`)
- Lect/scope labels represented: **7** (Māori, Official Malagasy, English, Polish, Turkish, Northern Arapaho, Guhang Ifugao), plus 1 explicitly secondary cross-linguistic candidate record.

All records carry page/section provenance, source ID, lect/time scope, confidence, formal and normalized environments, source forms where present, exception/counterexample fields, parent/dependency fields, and a dedup key. No shared curated denominator was edited.

## Validation

Added `tools/phonotactics_distribution/validate_staging.py`. It is fail-closed on malformed JSON, missing required fields, empty provenance identifiers, invalid confidence values, wrong source/link types, duplicate record IDs, duplicate dedup keys, and unresolved parent/dependency links across supplied batches. The three batch files were authored against this schema; connector-side writes succeeded. A local execution of the validator was not available in this connector-only run, so runtime validation remains the first next action before promotion.

## High-yield next queue

1. Kuo 2023, Samoan §§4.1–4.2 (pp. 97–112): inventory/phonotactics, OCP-place stem restrictions, gradient place and sonorancy effects, historical Proto-Oceanic/Proto-Polynesian comparison.
2. Kuo 2024 Journal of Phonetics Samoan study: OCP-LAB, OCP-COR-SON, OCP-BACK, distance-sensitive similarity avoidance, explicit corpus/model qualifications.
3. Hayes & Wilson 2008: exhaust Shona vowel harmony and Wargamay whole-language phonotactics, including representation/domain assumptions and gradient restrictions.
4. Smith 2002 §§4.2.1.2–4.4: Sestu Campidanian, Mongolian, Kuman, Guugu Yimidhirr, Pitta-Pitta, Mbabaram initial high-sonority restrictions; direct-source verification queue for Salzmann/Newell/Landman and the secondary Hausa/Guaraní/Tabukang Sangir candidates.
5. Dai 2025: exhaust Polish learned constraint table and Turkish Table 16/O-E exception distribution rather than only prose-level generalizations.
6. Existing taxonomy export: return to Kalamang, Komnzo, Gyeli and other grammar records whose report marks dedicated phonotactic sections requiring further atomic extraction.

## Checkpoints

- `e79a6e550ac0859e1f9f91d3f1da05bb07530e33` — Kuo Māori/Malagasy batch
- `3a45e5fc856025d974825315e48a9f89452e7236` — Dai English/Polish/Turkish batch
- `2668dc14ab85054fa72e3abe38caba547386a78c` — Smith initial-onset batch
- `6c8d5903788c39f9475dc9f623a6474896864c01` — staging validator
