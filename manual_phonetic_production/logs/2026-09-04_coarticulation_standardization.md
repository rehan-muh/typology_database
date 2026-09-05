# 2026-09-04 — Coarticulation standardization

The analysis layer was narrowed to ten phenomena only: VV_CARRYOVER, VV_ANTICIPATORY, CV_PLACE, VC_EFFECT, NASAL, LARYNGEAL, VOT_VOWEL, LABIALIZATION, RHOTIC_LATERAL, and TEMPORAL.

Implemented:

- canonical long-format schema in `docs/coarticulation_schema.md`;
- machine-readable phenomenon definitions in `config/coarticulation_phenomena.csv`;
- token/context, trajectory, event, and source-mapping templates under `data/coarticulation/templates/`;
- capability matrix for all 23 currently accepted source records in `data/coarticulation/source_capabilities.csv`;
- prioritized existing-data migration queue in `data/coarticulation/ingestion_queue.csv`;
- strict table validator in `scripts/validate_coarticulation.py`;
- generic manual-segment-table to target/context converter in `scripts/segments_to_coarticulation_tokens.py`;
- README and STATUS updates describing `coarticulation-v1`.

Key design decisions:

- study/source, language, and speaker remain separate model levels;
- speaker IDs are globally namespaced as `source_id::source_speaker_id`;
- bilingual speakers retain one speaker UID with token-level production language;
- all acoustic trajectories use long format and normalized target time;
- original measure/label names are preserved alongside canonical names;
- unsupported phenomena are explicitly marked rather than inferred;
- singing data are retained in MPPD but excluded from default speech pooling;
- clinical and L2 domains remain explicit for sensitivity analyses;
- the earlier `jingju_acappella_primary_subset` entry is flagged as the same JaCRC resource represented more precisely by `jingju_jacrc_primary_manual_2022`, so it must never be double counted.

The scheduled daily crawl was updated so that discovery is no longer sufficient: future runs must also assess the ten target capabilities, convert accessible accepted datasets into the canonical tables, validate each derived batch, and continue the prioritized backlog.
