# Ingestion/discovery audit — 2026-09-20 02:11 -0700

## Discovery

### ACCEPTED: `aphasiabd_zenodo_21863777`
- **Title:** AphasiaBD: A Bengali Speech Dataset for Broca's and Global Aphasia.
- **Authoritative deposit:** Zenodo record 21863777.
- **Primary production:** yes. Speech was collected directly from 38 post-stroke aphasia patients in Bangladesh.
- **Tasks:** conversation, repetition, question answering, reading.
- **Public scale:** 335 segmented audio clips.
- **Manual provenance:** Zenodo metadata explicitly says recordings were manually segmented at sentence level and identifies annotators.
- **Admission boundary:** only the manually segmented clip/sentence layer is presently established. Descriptions of phonemic distortions, substitutions, pauses, and incomplete utterances are NOT treated as observation-level manual labels unless archive sidecars establish them.
- **Pending:** enumerate archive members; capture license and per-file checksums; inspect annotation/metadata sidecars; create source-faithful participant/task/recording tables; harmonize only fields actually supplied.

## Backlog/integrity pass
- Re-opened live repository tree before writing. Existing warehouse contains distinct `harmonized`, `registry`, `coarticulation`, source/provenance structures and extensive JSUT chunks; no attempt was made to recreate existing chunks.
- PAVOQUE remains a high-priority observation backlog from the preceding pass; continuation should resume from the already recorded immutable upstream blob/cursor rather than restart the YAML.
- Marathi VOT remains pending for the unparsed TextGrids/workbook; workbook units must not be guessed.
- AKiD remains review-only until manual/human-verified provenance for vowel landmarks/measurement selection is established.

## Exclusions screened in discovery
- GTSinger / Jingju a Cappella: singing; excluded under non-singing criterion.
- MaMa Sounds: third-party/natural sound collection and perception-oriented; excluded.
- DPI-Watch: inhaler respiratory events rather than phonetic speech production; excluded.
- Generic Praat vowel-analysis scripts: software/methods, not primary datasets; not registry sources.

## Validation
- New source ID is namespaced and not known to collide with prior source IDs.
- No automatic boundaries, inferred IPA, inferred segment context, or fabricated acoustic rows were admitted.
- No raw audio was committed.
- Writes in this pass are confined to `manual_phonetic_production/`.

## Next priorities
1. Open/download AphasiaBD archive manifest and ingest every metadata/annotation table and file checksum permitted by license.
2. Continue PAVOQUE from the saved cursor and promote complete manual segment records.
3. Finish Marathi TextGrid parsing and verify the VOT workbook schema/units before measurement ingestion.
4. Resolve AKiD annotation provenance; admit only if manual/exhaustive human verification is documented.
5. Continue repository/journal discovery for public TextGrid/EAF/EMA/ultrasound/EPG/aerodynamic and token-level acoustic deposits.
