# EURASIA shard checkpoint

## Batch totals

- Structured source files: **7**
- Structured rows: **98**
- Core language/lect complexes: **6**
- Families represented: **6**
- Source works: **7**
- Shared curated denominators edited: **0**
- All writes remain under `staging/eurasia/automation01_20260824_0005/` on the shard-specific branch.

## Coverage added

1. **Hewramî (Tekht; West Iranian)** — synchronically scoped consonant/vowel inventory, quantity, syllable template, epenthetic cluster repair, onset/coda restrictions, /w/ allophony, lexical/grammatical stress, plus separate 2025 diachronic reconstruction of pretonic reduction, vowel loss, cluster reduction, morphologized stress, relative chronology and ongoing apparent-time prefix loss.
2. **Hinuq (Tsezic)** — vowel inventory and tense/lax realization, syllable/root restrictions, superheavy loan vs native inflection distinction, cluster repair, minimal word, geminates, glottal/labialized distribution, and explicit candidate queues for atomizing the remaining morphophonology/stress subsections.
3. **Udihe (Tungusic)** — segment inventories, Bikin-specific allophony, /g/ and /c/ lenition, /ŋ/ deletion, /s/ palatalization, /r/-less loan adaptation, declining vowel harmony, suffix harmony, assimilation, historical *r/*k/*s loss, creaky/breathy-vowel decline, Chinese-contact hypotheses, syllable structure, phonemic quantity and stress.
4. **Basque (isolate)** — native and borrowed onset/coda phonotactics, historical emergence of stop+liquid clusters, initial rhotic prothesis, affricate restrictions, stop allophony and final neutralization, /f/ loan adaptation, old intervocalic-n loss, Standard Basque stress and dialect prosodic nonuniformity.
5. **Ket (Yeniseian)** — four contrastive monosyllabic tonemes, disyllabic and polysyllabic prosody, tone-conditioned vowel allophony, compact segment inventories, competing /p/ and palatalization analyses, intervocalic velar/uvular frication, initial/final cluster restrictions, grammatical-morpheme distribution, tone-only plural marking and contractive plural morphophonology.
6. **Eastern Khanty (Vasyugan/Alexandrovo; Uralic)** — full/reduced vowel contrast, epenthetic schwa, directional backness harmony and its word domain, areal comparison, syllable templates, extrametrical CCC observations, dynamic stress conditioning and explicit stress noncontrastivity.

## Provenance and confidence policy

Every row has an `id`, `language`, `family`, `source_id`, `domain`, `claim`, `confidence`, `dedup_key`, and at least one source-location field (`page`, `pages`, `section`, or `table`). Lect/time scope is explicit where the source distinguishes dialects, generations or historical stages. Dependencies are used where an extracted generalization presupposes another row (e.g. Ket tone-conditioned allophony and Hewramî chronology). Rows derived only from a table of contents or section-level candidate scope are marked accordingly rather than promoted to atomized facts.

The repository tree was re-read after staging and confirms all seven JSONL source files are present. A shard-local validator, `tools/validate_jsonl.py`, now checks JSON parsing, required fields, source-location provenance, confidence vocabulary, duplicate IDs, duplicate dedup keys, exact repeated claims and dangling dependency IDs. The GitHub connector available in this run can write/read repository files but cannot execute repository code, so I do **not** claim that this script itself was executed remotely. Static batch construction used unique IDs/dedup keys, and the manifest records the exact expected 98-row count for execution in a normal checkout.

## Source-access decisions

- When the Hewramî Zenodo endpoint was rate-limited, extraction moved to accessible publisher/repository mirrors instead of stalling.
- Ket was extracted from a page-addressable copy of Georg (2007); page/section provenance follows the printed pagination.
- Eastern Khanty used the author/institutional repository copy and web-rendered chapter text; the vowel-inventory row is explicitly marked `table_verified_web_rendering_partial_unicode` because some reduced-vowel glyphs are poorly preserved in the HTML rendering rather than silently normalized.
- Blocked/paywalled results were skipped when they did not expose enough verifiable text.

## Checkpoints

- `9db99a2ae018d8bb2a50d42a40b71551d7d5f9ca` Hewramî grammar batch
- `82e61c13eccc8183497f628d3a10bcb0002ce413` Hinuq batch
- `e8df3fe2e6dedc3cdb83b5e5df88e77020f9fd4b` Udihe batch
- `012bdb8f9b9b9867d5bf2623569f171f831a4d65` Basque batch
- `7c07f4cbcd8018149d5662c1391dde79f39de259` Ket batch
- `ca4d612bf212c16c6e32028bd3b3dd1f9d2c152e` Eastern Khanty batch
- `fe9881a9ef96e903502ee344ad4303e50fcbf229` Hewramî specialist diachrony batch
- `d2f9983ec453ea5a4ca892543e192aa5c082add4` validator tooling
- `f2388896f7a2282e65db8eeae831ced95ea1c15b` exact source manifest

## High-yield next queue

1. **Eastern Khanty:** atomize consonant inventory/allophony and the dedicated consonant–vowel-harmony section from Filchenko; reconcile dissertation vs 2010 book pagination.
2. **Hinuq:** exhaust §§2.4–2.5 into process-level rows (epenthetic vowels, o~zero, vowel deletion, glide insertion, identical-vowel resolution, sonorant deletion, palatalization, ablaut, loan integration, reduplication; then stress by lexical category).
3. **Ket:** exhaust §3.3.2 allophony and §4.4.4 morphotactic truncation/anaptyxis rules; link rule dependencies to prosodic-word boundaries.
4. **Udihe:** reconcile Kazama (2022) against Nikolaeva & Tolskaya (2001), especially vowel-harmony analysis, tone claims and dialect differences; keep competing analyses as separate rows rather than overwriting.
5. **Caucasus:** add an underrepresented Kartvelian lect (e.g. Svan or Laz) and another Northeast Caucasian lect not already in the old Eurasia manifest, with loan/contact chronology where source-supported.
6. **Central/South Asia:** add Wakhi/Shughni or another Pamir language plus a Nuristani/Dardic grammar not already represented, prioritizing stress, vowel harmony/umlaut, cluster phonotactics and historical/contact sections.
7. **Siberia/Far East:** add Chulym/Selkup or another underrepresented Uralic/Turkic lect, followed by an independent Yukaghir specialist source for reconciliation rather than duplicating the existing Kolyma Yukaghir grammar extraction.

Do not merge or canonicalize these rows automatically. Reconciliation should happen in a later curated pass that can compare source scopes, dialects and competing analyses.
