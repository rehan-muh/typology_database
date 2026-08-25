# PHONOTACTICS / DISTRIBUTION shard — continuation checkpoint

## Isolation and exact totals
Work remained exclusively on `agent/phonotactics-worker-20260825-1353`, under `staging/phonotactics_distribution/` and `tools/phonotactics_distribution/`. No shared curated denominator or canonical table was edited.

Prior checkpoint: **147 atomic records across 18 JSONL batch files**.
This continuation: **40 atomic records across 6 new batch files**: **39 high-confidence, 1 medium-confidence**.
Current shard total: **187 atomic staged records across 24 JSONL batch files**.

## New batches and commits

| batch | focus | records | confidence | commit |
|---|---|---:|---|---|
| `2026-08-25_bakairi_structure_segments_batch19.jsonl` | Bakairi codas, CV gaps, positional voicing, fricative/liquid distribution, syllable templates, minimality, CGV variation | 10 | 10 high | `af81728515e5f29b3c979e7c972bfcebb808cfb4` |
| `2026-08-25_bakairi_prosody_harmony_loans_batch20.jsonl` | Bakairi stress/weight, nasal spreading, harmony, fast-speech deletion, h-deletion, loan strata/repair | 12 | 12 high | `67e4c33aa10b7df4071037cde4ac2c87aadbf5ce` |
| `2026-08-25_guugu_yimidhirr_quantity_stress_batch21.jsonl` | Guugu Yimidhirr suffix-conditioned quantity, quantity domain, main/secondary stress, clash avoidance and double-stress disagreement | 6 | 6 high | `c03bbe288769220e8ed2f07999e99353e508a5e8` |
| `2026-08-25_leti_distribution_continuation_batch22.jsonl` | Leti vowel-sequence nuclei, predictable length, labial-fricative variation, sonority-conditioned initial-cluster repair | 4 | 3 high + 1 medium | `371b882d00434f951664cc22748457c8292eea21` |
| `2026-08-25_mbabaram_stress_onsets_batch23.jsonl` | Mbabaram onset-sensitive stress, closed-σ2 frequency, long-V confound, initial rhotic ban and onsetless word edge | 5 | 5 high | `889aed87e71bcd27301d739166910d0f2b3ed841` |
| `2026-08-25_kalmyk_harmony_batch24.jsonl` | Literary Kalmyk/Oirat palatal harmony, first-vowel trigger including initial /i/, suffix harmony/no rounding harmony | 3 | 3 high | `f899509c8488c1f729b7a60f918b8f2b4a2a2e81` |

Reusable read-only summary/audit tool added:
- `tools/phonotactics_distribution/summarize_staging.py` — commit `47efdda180fec1a94db441fb3031b6c5901f7a67`.
- Reports batch/record totals, distributions by lect/source/domain/confidence, duplicate `record_id`/`dedup_key`, unresolved parent/dependency links, and parse errors; never edits staging or curated data.

## Empirical additions

### Bakairi — direct grammar pass (Faria 2022)
- Native coda inventory staged as **glides only**, with the ideophone/glottal-coda marginal class kept as an explicit exception rather than silently folded into the denominator.
- Preserved lexical CV gaps and frequency qualifications: `/de bu zɔ he hi su ʔə/` unattested in the surveyed lexicon, while `/te/` is rare but attested in three words.
- Added robust **word-initial voicing neutralization**: nonsonorants surface voiceless at the left edge, while prefixation can place the same root-initial segment word-medially and permit voiced realizations. Ideophones, the likely-loan ethnonym, and newer Portuguese loans remain explicit exception strata.
- Added the strong but non-exceptionless **one non-initial voiceless obstruent** generalization for polysyllabic words, preserving the grammar's listed lexical counterexamples and free-variation pair.
- Added /s/ distribution and palatalization before close vowels, /h/ word/vowel restrictions, and the rare-initial liquid/dialectal-/r/ frequency distinction.
- Added `(C)V` basic syllable structure plus glide-bearing `V CV GV VG CGV CVG` surface patterns, explicitly distinguishing them from ordinary CC clusters.
- Added bimoraic minimal-word structure: monosyllables require a long vowel.
- Added variable `/s,h/+G` glide deletion/fricative alternation as within-speaker variation rather than a categorical repair.
- Added penultimate-mora main stress, rising/falling glide-sequence weight asymmetry, and the fact that vowels nasalized by spreading remain light for stress.
- Nasal harmony records preserve direction, optionality, target/transparent/blocker classes, and a separate postlexical regressive external-sandhi domain.
- Added two **morpheme-specific vowel-harmony** patterns rather than overstating Bakairi as generally vowel-harmonic: the detransitivizing/reflexive-reciprocal prefix and possessum `-rɨ ~ -ru` suffix.
- Added fast-speech function-word vowel deletion and dialect-/morpheme-conditioned /h/-deletion between identical back vowels.
- Portuguese loans are explicitly stratified: older loans are usually more adapted; recent loans may retain initial voiced segments, multiple internal voiceless obstruents, and consonant codas. Integrated loans show coda deletion, stress reassignment, and native morphophonological voicing repairs.

### Guugu Yimidhirr — direct Haviland + stress triangulation
- Haviland p.44 now supplies the suffixal quantity system: ordinary, lengthening, and shortening suffix classes interact with the second vowel and stem-final segment class.
- The **domain restriction is explicit**: suffix-triggered length changes target the second syllable of disyllabic stems; monosyllabic and trisyllabic-or-longer stem quantity is unaffected.
- Elías-Ulloa's reanalysis preserves Haviland's data while adding the full stress distribution: main stress defaults to σ1, σ2 long vowels attract main stress when σ1 is short, and closed syllables do not independently attract main stress.
- Secondary stress is rhythmic but clash-sensitive; final odd syllables may bear secondary stress even when open if no clash results.
- The famous two-main-stress issue is stored as **analytical disagreement**: Haviland's two-main-stress transcription versus Elías-Ulloa's single-head reanalysis. Neither analysis is silently promoted to uncontested fact.

### Leti — continuation
- Added the source's explicit **no-diphthong analysis**: each transcribed vowel is a syllable peak; identical adjacent vowels have a long realization except word-finally.
- Added predictable long-vowel distribution tied to morphemes alternating with hiatus forms.
- Added `[β] ~ [v]` free variation without inventing a conditioning environment, plus the reported geminate-inventory gap.
- Added phrase-initial sonority-violation repair by syllabic C1, contrasted with sonority-licensed intact clusters. Confidence is **medium** because Hume explicitly says the sonority grading rests on native-speaker intuition rather than independent phonological evidence.

### Mbabaram — specialist triangulation back to Dixon 1991
- Added onset-sensitive stress with the quantitative qualification that a closed second syllable attracts stress in about **95%**, not categorically.
- Preserved the separate trisyllabic σ2 stress generalization.
- Long vowels are reported stressed but are extremely rare and positionally confounded: virtually all occur in monosyllables or σ2 of vowel-initial words, where stress is independently expected.
- Added the word-initial rhotic ban while retaining laterals and glides as explicit permitted onsets; this blocks an overbroad 'high-sonority onset ban' interpretation.
- Added the independent fact that Mbabaram is initial-dropping and licenses onsetless word-initial syllables. This is linked to, but kept distinct from, their stress avoidance.

### Literary Kalmyk / Oirat
- Added word-level palatal/front-back harmony with invariant-quality /i/.
- Added the crucial trigger asymmetry: the **first vowel determines harmony class**, and initial /i/ selects front harmony despite being neutral in its own alternation.
- Added suffixal two-way front/back alternation with **no productive rounding-harmony series** in Svantesson's literary Kalmyk system.
- Dialectal/historical qualifications are explicit; these records are not generalized to every Oirat variety or to East Mongolian harmony.

## Validation and provenance
- All 40 new records were generated as valid JSON objects before writing and contain the shard-required provenance fields: source ID, lect/time scope, domain, source forms, formal and normalized environments, restriction type, scope, exceptions/counterexamples, exact page/section/table-or-example provenance, confidence, links, and dedup key.
- All six empirical files committed independently and all six completed GitHub **round-trip reads** after writing.
- Branch head after the audit-tool commit was independently read from the Git tree as `47efdda180fec1a94db441fb3031b6c5901f7a67`; the tree shows batches 19–24 under shard staging only.
- A complete local `validate_jsonl_batch.py staging/phonotactics_distribution/*.jsonl` rerun was attempted after writing. The local execution container failed before cloning because DNS could not resolve `github.com`; this is a transport/DNS failure, not a reported schema error. GitHub connector reads/writes remained successful throughout.
- The Guugu Yimidhirr full Haviland PDF remains too large/disabled for the web PDF renderer, but exact indexed p.44 text was available from the ANU-hosted volume and the direct Haviland chapter search index. No unreadable table cell was reconstructed.
- For Elías-Ulloa, the accessible HTML full text was used for the detailed stress sections. For Mbabaram, Gordon and Smith were used only where they give explicit Dixon page references and quantitative/descriptive qualifications; no unsupported reconstruction of Dixon's unavailable pages was made.
- Kalmyk records are restricted to claims recoverable from Svantesson's article text and do not import newer phonetic controversies into the same records.

## High-yield next queue
1. **Bakairi continuation:** finish §2.5 voicing Generalization 3 and any remaining prosodic/segmental exception tables; link staged restrictions to an explicit Bakairi inventory/process index if a stable shard-local ID map is available.
2. **Wargamay Appendix-D reconciliation:** classify all 57 weighted model-only constraints against corpus support/violations as supported gradient pattern, sparse-data artifact, likely overfit, or unresolved; retain weights separately from facts.
3. **Pitta-Pitta direct source:** locate the grammar/phonology underlying Smith's positional-onset candidate and extract initial-vs-medial segment inventories, stress/quantity, clusters, and explicit exceptions.
4. **Mbabaram direct Dixon extraction:** seek a readable chapter copy for pp.351–359 and 398–401 to replace specialist triangulation with direct page records and extend into cluster/coda/allophonic distribution.
5. **Kalmyk/Oirat direct expansion:** add noninitial-vowel reduction, harmony exceptions/loan behavior, and dialect distinctions from a directly readable grammar or article; keep literary Kalmyk distinct from modern spoken varieties.
6. **Sardinian/Sestu-Iglesias:** directly verify the initial-rhotic repair candidate and capture epenthesis/domain/loan qualifications rather than relying on typological summaries.
7. **Tongan and Samoan:** finish remaining raw deletion/length tables for Tongan; retry a direct Samoan grammar or an accessible chapter mirror for suffix/domain and VVV tables.
8. **Fresh high-density grammars:** run the page-ranker over grammars with dedicated phonotactics + morphophonology chapters, prioritizing sources with explicit distribution tables, loan strata and exception lists.
