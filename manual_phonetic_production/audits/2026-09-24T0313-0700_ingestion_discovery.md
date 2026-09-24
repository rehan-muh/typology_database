# Ingestion/discovery pass — 2026-09-24 03:13 PDT

## Discovery

### Spontal-N — REVIEW
Source: Sikveland, Aksnes, Eklund, Enflo & Hansen (LREC 2010), *Spontal-N: A Corpus of Interactional Spoken Norwegian*.

Verified from the public corpus description:
- primary studio-quality audio/video;
- four approximately 30-minute free conversations between acquaintances;
- complete material manually orthographically transcribed;
- approximately 50% automatically phone-aligned from the manual transcription;
- approximately 7% of the automatic phone transcription manually corrected and used as a gold standard.

Decision: **review**, not accepted wholesale. The automatic phone layer fails the database inclusion rule unless the manually corrected subset can be isolated. The full manual orthographic layer is human-created but does not by itself establish manual phonetic boundaries. Next action is to locate the authoritative distribution and enumerate annotation objects/tiers, correction markers, license, and recording lineage.

Created `data/registry/review_increment_2026-09-24_0313.csv` and a six-row seed variable dictionary. No IPA was inferred and no automatic phone intervals were promoted to the manual core.

## Backlog ingestion / audit

Rechecked the current L2-ARCTIC documentation against the existing accepted manual-layer entry. Public documentation now gives corpus-wide counts of 26,867 utterances / 27.1 h / 24 speakers, but the manual subset is specifically 3,599 human-examined utterances with 14,098 substitutions, 3,420 deletions, and 1,092 additions. The manual annotations include corrected word and phone boundaries. This confirms the existing tier-level eligibility decision: `/annotation` manual objects are eligible; ordinary forced-aligned word/phone boundaries must remain excluded.

No new L2-ARCTIC observation rows were claimed because the authoritative downloadable manual TextGrid objects were not materialized in this pass. Existing source/dictionary records were left untouched rather than duplicating them.

## Exclusion / review checks

- RescueSpeech: already represented; no duplicate source created.
- MRPL2: remains high-value but restricted-file access prevents object-level ingestion.
- ROG: remains lineage-sensitive because it builds on SST/GOS2; new manual prosodic/interactional layers need isolating from inherited recordings before core admission.
- Nonspeech7k: not eligible (third-party nonspeech media).
- Jingju a Cappella: not eligible because singing/music production is explicitly excluded.

## QC

- Only `manual_phonetic_production/` was modified.
- No unrelated repository files touched.
- No unverified automatic alignment admitted as manual data.
- No duplicate recording lineage intentionally created.
- Unknown source-internal names remain marked pending rather than invented.
- This pass prioritizes conservative provenance over inflated row counts.

## Next backlog priorities

1. Find and enumerate the Spontal-N authoritative annotation distribution; isolate the manually corrected phone subset.
2. Materialize L2-ARCTIC manual `/annotation` TextGrids if public access permits, then parse every tier and preserve corrected boundaries/errors source-faithfully.
3. Continue MRPL2 access monitoring and object enumeration if files become available.
4. Resolve CORPRES public-distribution status and whether its manually segmented 40% can be isolated.
5. Continue BAS manual-layer corpus sweep (VM2/PD1/SC10) without admitting automatic MAUS layers.
