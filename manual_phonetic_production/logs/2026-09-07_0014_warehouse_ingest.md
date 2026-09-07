# 2026-09-07 00:14 warehouse ingestion pass

## Discovery
- Searched current OSF/Zenodo/GitHub/journal-facing web results for manual/manual-corrected primary production resources.
- Newly accepted: `rog_slovenian_1_0_1_1_manual_prosody` (ROG 1.0/1.1 / LREC 2026). This is **not** counted as a new underlying recording corpus: ROG builds on GOS 2. Only the isolatable new manual ROG annotation layer (prosodic units, disfluencies, dialogue acts, plus linked manually assigned linguistic annotations) is admitted.
- Rechecked RescueSpeech, MRPL2, ManDi, IFCASL and other surfaced candidates. RescueSpeech remains review because its public wording `manually annotated` does not establish the temporal/phonetic level. MRPL2 remains restricted; ManDi remains restricted to its verified human-checked subset. IFCASL remains promising but current public downloadable corpus/access lineage was not established in this pass.

## ROG repository audit / ingestion work
Authoritative CLARIN.SI record: https://www.clarin.si/repository/xmlui/handle/11356/1992
Publication: https://aclanthology.org/2026.lrec-1.449/

Verified public release facts:
- `ROG.zip`: 22.24 MB, MD5 `99cca109eb226d573291fbce1886cfb7`, CC-BY-SA-4.0.
- `ROG-Art.wav.zip`: 1.31 GB, MD5 `c2875b61b30e633f2358f2975f99ed97`.
- ROG-SST: 76,341 words / 6,108 sentences.
- ROG-Art: 39,001 words / 1,969 sentences.
- Corpus-level size: 98,393 tokens, 76,341 words, 6,108 sentences; approximately 10 h is reported by the 2026 paper.
- Public archive preview exposes `ROG-speeches.tsv`, `ROG-speakers.tsv`, train/dev/test split files, CONLL-U, EXMARaLDA EXB/XML, TRS, TXT, TextGrid files with additional prosodic annotations, and linked WAV files.

Permanent warehouse additions:
- `data/warehouse/rog_slovenian_file_manifest.csv`
- `data/warehouse/rog_slovenian_documented_variable_dictionary.csv`
- row in `data/warehouse/ingestion_status.csv`
- row in `data/registry/increments/2026-09-07_accepted.csv`
- `STATUS.json` accepted count updated 35 -> 36.

## Provenance / deduplication decision
ROG uses pre-existing GOS 2 recordings, so underlying audio/speaker observations must retain GOS lineage and must not be double-counted as a fresh primary recording collection. The accepted contribution is the new manually produced ROG layer. ROG-Art's prosodic-unit, disfluency and dialogue-act annotations are treated as manual source annotations. No IPA or segmental context is inferred from orthography or non-phonetic tiers.

## Backlog ingestion status
- Existing parsed warehouse totals remain 431,751 observations / 64 parsed tables / 846 parsed variable records. These counts were deliberately **not** incremented from repository metadata or file manifests.
- Tang remains the highest-value deep structured backlog: 1,344 public CSV summary rows are already parsed, with the participant MAT audit documenting 13,000 trial structures and within-token F1/F2 arrays. No unmaterialized MAT observations were falsely added to warehouse row totals in this pass.
- ROG is now ready for source-faithful archive parsing. Next concrete ingest is the small 22.24 MB annotation ZIP: parse speaker/recording TSVs first, then EXB/TextGrid temporal tiers, retain every original tier/label/value, namespace IDs, and map manual prosody/disfluency/dialogue annotations into linked interval/prosody tables. Raw 1.31 GB audio should remain URL/checksum referenced rather than committed.

## Validation
- Registry/status counts are internally consistent after the single new acceptance (36 accepted, 19 excluded, 34 review).
- No warehouse observation count was increased without actual parsed rows.
- All permanent modifications are confined to `manual_phonetic_production/`.
