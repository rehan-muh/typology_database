# Warehouse ingestion log — 2026-09-06 20:10 PT / 2026-09-07 UTC

## Scope
Aggressive discovery + backlog pass for primary non-singing phonetic production with manual, manually corrected, or exhaustively human-verified relevant annotations/measurements. Source-faithful provenance and recording-level deduplication were enforced before admission.

## Newly accepted / linked sources

### jaeger_daeglau_2026_unscripted_monologues
- 2026 Data in Brief annotation release linked to the same project's primary German audiovisual recordings (Zenodo 8082844).
- Six speakers, 60 takes, >300 min.
- New separable layer: manually corrected word/phoneme/pause event timing, orthography, X-SAMPA phonetic/canonical forms, syllabification, POS and lemma.
- Added registry row, two-layer file manifest, 14-field documented variable dictionary and ingestion-status record.
- Deduplication rule: do not count the underlying audiovisual recordings a second time; this source contributes the corrected annotation layer.

### erattakulangara_2025_vocal_tract_mri
- 53 3D vocal-tract volumes from 10 French speakers; 21 phonemes + 3 voiceless tasks.
- New isolatable manual annotation layer on an earlier primary MRI corpus: expert-vocologist / graduate-student masks plus STAPLE consensus labels.
- Figshare annotation dataset is MIT licensed.
- Added registry, lineage-aware manifest, documented variable dictionary and ingestion-status record. Individual manual masks and consensus masks remain distinct.

### girafe_2024_2025_glottal_imaging
- 65 high-speed laryngeal videoendoscopic recordings from 50 native Spanish-speaking participants; 502 frames per sequence / 32,630 images, 4000 fps.
- Sustained vowel phonation, sometimes including vocal onset; expert manual glottal-gap segmentation for every recording.
- Important access correction during this pass: companion GitHub code is MIT, but current Zenodo imaging/mask files are restricted/request-access and the Data in Brief dataset license is CC BY-NC 4.0. Registry, manifest and ingestion status were corrected accordingly; no imaging files were mirrored.
- Clinical/health status remains a covariate: healthy, diagnosed voice disorder, and unknown-health records are kept distinct without inference.

## High-priority review

### nieber_kachel_scharinger_2026_gendered_self
- Journal of Phonetics 2026, German semi-spontaneous production, 52 analyzed speakers.
- Manual Praat segmentation at picture/carrier-word/target-sound levels and broad acoustic coverage (F0, vowel formants/space, sibilant spectra, voice quality) with rich demographic/gender metadata.
- Paper states data/Praat/R code are on OSF, but the exact public OSF project/file-level access/license was not recovered in this pass. Added to HIGH review rather than admitted without direct deposit verification.

## Explicit exclusions / lineage controls

### hantzsch_2022_one_shot_adaptation
- Excluded as a secondary reanalysis of six previous studies (131 participant records, with overlapping participants). Retain only as lineage/methodological reference and ingest eligible component studies individually.

### hiemstra_sadakata_2024_speech_to_song
- Excluded despite manual Praat word/phoneme/vowel segmentation because the speech stimuli are selected from audiobook / pre-existing stimulus collections rather than a new primary production corpus. This enforces the third-party-media exclusion.

## Backlog work

### Tang et al. 2022 perturbation data
- Added OSF STJC9 to the recursive open-data auditor; audit completed successfully.
- Discovered 83 files. Ten directly readable CSV tables were parsed, totaling 1,344 rows and 116 table-variable records (27 unique source variable names).
- Five acoustic summary tables contain `dura`, `stddura`, `RT`, `stdRT`, `stdf1_mid`, `stdf2_mid`, `stdf1_init`, `stdf2_init`, `medf1`, `medf2`, `initdists`, `middists`, `area`, `centering`, `centperc`, `cond`, `vowel`, `subj`, `stdmajor`, and `stdminor`. Conditions observed include baseline, hold2, washout, holdIn and holdOut.
- Five regression/normalization tables contain baseline and normalized distance measures by vowel.
- Participant-level `dataVals.mat` files (many ~34–69 MB) and `expt.mat` files remain the highest-value next layer. Released `free-speech` code shows that `dataVals` stores within-vowel F1/F2 tracks and intensity bounded by onset/offset indices, so those MAT files should be parsed rather than reducing the source to the 1,344 summary rows.
- Added `tang_2022_table_inventory.csv` and a semantic `tang_2022_variable_dictionary.csv`; source CSV contents remain reference-layer data until redistribution terms are confirmed.

### Mitra-Dutta audit resilience
- Prior deep crawl failure was traced to a transient OSF GitHub-provider 502 at `nodes/dsb2x/files/github/draft_BLC/`. Existing 340-file manifest/parsed reference layer remains valid; future deep traversal should add retry/continue behavior rather than discarding partial progress.

## Warehouse state after committed decisions
- Accepted records: 31.
- Excluded records: 17.
- Review queue: 31.
- Confirmed parsed warehouse totals: 431,751 observations / 64 source tables / 846 parsed table-variable records.
- New documented dictionaries/manifests are not counted as parsed observations unless source tables were actually opened and profiled.

## Next highest-yield actions
1. Parse Tang participant-level `dataVals.mat` / `expt.mat` files into source-faithful trial/trajectory structures; preserve F1/F2/intensity tracks and corrected landmark lineage.
2. Parse the 6.2 MB Jaeger-Daeglau annotation ZIP into recording/event/lexical tables and preserve source X-SAMPA alongside any defensible future IPA mapping.
3. Inventory the MIT-licensed 3D MRI Figshare hierarchy and capture speaker/phoneme/task/volume/mask linkage without double-counting the earlier MRI corpus.
4. Continue Schertz 5,801 production-row harmonization, preserving unresolved macro/micro VOT scales separately.
5. Make the Mitra-Dutta recursive auditor tolerant of transient OSF/GitHub-provider 5xx failures and continue the 340-file backlog.
