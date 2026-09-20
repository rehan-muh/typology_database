# Ingestion/discovery audit — 2026-09-19 17:07 -0700

## Discovery

### SAIT-EMA (Jia et al. 2026) — REVIEW
- Primary production: yes. 18 healthy adults; 12 native Mandarin and 6 L2 Mandarin speakers; synchronized Carstens AG501 3-D EMA and 48 kHz/16-bit mono audio.
- Public data: Zenodo DOI 10.5281/zenodo.17506802, CC BY 4.0 according to the Scientific Data data-record statement.
- Manual/human verification evidence: experimenters documented misreadings and re-recorded erroneous tokens; head displacement and sensor detachment triggered re-recording; post-recording, session logs were used to manually screen and remove misaligned tokens/unintentional repetitions, leaving one verified token per target stimulus.
- Critical exclusion boundary: supplied phonetic TextGrids are explicitly generated automatically with Montreal Forced Aligner. The paper warns of systematic temporal offsets and recommends manual verification/refinement for precise landmarks. These TextGrids therefore MUST NOT enter the manual core unless an independently human-corrected layer is found.
- Measurement scope worth preserving if admitted at verified-measurement level: complete 3-D EMA trajectories for tongue tip, tongue blade, tongue dorsum, upper lip, lower lip, lower incisor/jaw reference and three head-reference sensors; synchronized audio; raw POS; session/stimulus metadata. Do not collapse trajectories to summary values.
- Decision: review, not accepted. The raw measurement stream is primary and the final token inventory was manually screened, but this pass does not equate that QC with manual phonetic landmark annotation. Resolve against database inclusion policy before observation-level core ingest.

## Backlog ingestion / integrity audit
- Re-read current repository tree and confirmed the database continues to maintain separate `data/harmonized`, `data/registry`, coarticulation templates/views, audits, and other source/provenance structures.
- JSUT backlog remains present in many chunked harmonized files. GitHub code search is not indexed for this repository, so this pass did not create another JSUT chunk without a collision-safe boundary check.
- IFCASL remains review-only: ~100 French/German native/L2 speakers; word/phone segmentation with >50% manually corrected, but no public observation payload with an isolatable correction flag/subset was located in this pass.
- L2-ARCTIC remains a strong accepted/manual-layer target: 3,599 manually examined utterances; corrected boundaries and substitution/deletion/addition tags. Corpus-wide forced alignment remains excluded.

## Fresh exclusions / non-promotions
- SAIT-EMA automatic MFA TextGrids: excluded from manual core.
- AdoVoc Pro: singing; excluded by scope.
- HAMATAC: manual disfluency annotation and manually corrected POS/lemmas are not sufficient evidence of manual phonetic intervals/measurements; not promoted.
- UrduSpeech: search evidence includes third-party/news/drama-style curation and a manually corrected benchmark, but does not establish primary laboratory/field production with qualifying manual phonetic annotation; not promoted.

## Counts this pass
- New accepted sources: 0
- New review sources: 1 (SAIT-EMA)
- New registry rows: 1
- New observation rows: 0
- Automatic annotation layers explicitly quarantined: 1 (SAIT-EMA MFA TextGrids)
- New audit files: 1

## Next priorities
1. Enumerate the Zenodo SAIT-EMA payload/file manifests and determine whether session logs expose token-level human-QC decisions; if so, preserve those decisions and raw trajectories separately from automatic TextGrids.
2. Continue collision-safe JSUT ingestion only after determining the highest existing BASIC5000 chunk from repository contents rather than guessing from search.
3. Obtain/enumerate UltraSuite manual `slt_labels` and manually revised `reference_labels` archives and ingest interval observations.
4. Isolate the L2-ARCTIC 3,599 manually examined TextGrids and parse human-corrected phone boundaries/error tags if access terms permit.
5. Locate IFCASL distribution and isolate the manually corrected portion before core admission.

## Validation
No unrelated repository path was modified. No automatic-only phonetic boundary was admitted as manual. No IPA, context, timing, units, or annotation status was inferred where the source did not establish it.
