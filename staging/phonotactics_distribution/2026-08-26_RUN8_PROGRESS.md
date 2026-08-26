# PHONOTACTICS / DISTRIBUTION shard — Run 8 checkpoint

## Isolation and baseline

- Branch: `agent/phonotactics-worker-20260825-1353`
- Baseline checkpoint/head: `683d994984c4745fcae5d8eb2c2f20cac8aa7e3d`
- Baseline staged empirical total: **242 atomic records across 32 JSONL batches**.
- This run wrote only under `staging/phonotactics_distribution/` and `tools/phonotactics_distribution/`. No shared curated denominator/canonical table was modified.

## New empirical batches and commits

| Batch | Records | Main coverage | Commit |
|---|---:|---|---|
| `2026-08-26_wargamay_appendixD_model_constraints_batch33.jsonl` | 27 | Hayes & Wilson Appendix D constraints 1–27, exact feature strings/weights, explicitly model-output-only | `518bcec0a81a83b35414d0bac736093281889d1f` |
| `2026-08-26_wargamay_appendixD_model_constraints_batch34.jsonl` | 16 | Appendix D constraints 28–43 | `95fc471440cd7831f5b766adeda4aeb6a990cdf5` |
| `2026-08-26_wargamay_appendixD_model_constraints_batch35.jsonl` | 14 | Appendix D constraints 44–57 | `f101182d20d58356c1be89f648de0e201c06d21b` |
| `2026-08-26_korean_medial_liquid_quantitative_batch36.jsonl` | 5 | Korean medial English-/l/ variation: normative vs spoken rates, cluster/prosodic effects, Japanese mediation | `555cf971cbbfea634672467c2d5a337a6b79c5a8` |
| `2026-08-26_korean_initial_liquid_contact_batch37.jsonl` | 4 | Seoul vs Northern Hamkyeong initial-liquid allophony, age/contact effects, lexical-stratum productivity probe | `bdc58627c712350ba67cd2052231dd3bfc9135a0` |
| `2026-08-26_tongan_definitive_accent_direct_batch38.jsonl` | 4 | Direct definitive-accent NP domain, duration, phonemic length × DA, penultimate-mora stress | `6b1295ea7b4506021ca7d7a58c8702f000a90996` |
| `2026-08-26_kalmyk_positional_harmony_batch39.jsonl` | 5 | Kalmyk postinitial rounding neutralization, suffix-vowel inventory/harmony, /i/ evidential caveat, historical quantity | `08bdca5564a7dd4c558a582eb9b0404bba3236b1` |
| `2026-08-26_jewish_gabes_vowel_distribution_batch40.jsonl` | 6 | Jewish Gabes schwa allophony, marginal /u,o/, diphthong contraction and secondary diphthongization | `9642e74f095c4c664f973788b632116b574de2bd` |
| `2026-08-26_wargamay_constraint_reconciliation_batch41.jsonl` | 3 | Aggregate 28/29 Appendix-D evidence split, early-stopping/MDL qualification, secondary-stress naturalness warning | `68a181d1d0dfcc5c2c9e572409092b85767ed0c6` |
| `2026-08-26_modern_kalmyk_stress_vowel_distribution_batch42.jsonl` | 4 | Modern positional vowel restrictions, noninitial -go exception, source-specific quantity reanalysis, first-syllable harmony control | `5e54fc708403a9abaa94625fe5dfa55258932cbc` |
| `2026-08-26_samoan_root_quantitative_batch43.jsonl` | 5 | Direct root phonotactics: diphthong inventory, /v/+back near-gap, VV co-occurrence, order-sensitive CC OCP, nasal/historical-place qualification | `c233865e05cd1576dd7b820ea1e398e54f96e10c` |

**New empirical records this run: 93 across 11 batches.**

**Cumulative staged empirical total: 335 atomic records across 43 JSONL batches.**

## Reusable validation tooling

Added `tools/phonotactics_distribution/audit_weighted_constraints.py` in commit `e8eaa481e6982a0b87108d34c0a23e3be3a6d59a`.

This read-only auditor checks weighted model-constraint batches for JSON validity, unique record/dedup IDs, integer constraint numbers, numeric weights, missing/duplicate constraint numbers, weight-order monotonicity, and agreement between the source constraint string and `formal_environment`. It never edits source/staging data or promotes learned-model output to empirical grammar.

## High-value source reconciliation / qualifications

### Wargamay

The entire 57-item Hayes & Wilson Appendix-D learned constraint table is now individually staged with exact weights and source feature strings. These are **high-confidence transcriptions of learned model output**, not high-confidence categorical Wargamay grammatical facts. Hayes & Wilson state that the 57 additional constraints have no direct analogue in Dixon: 28 are unviolated in the training data and 29 are violated only a few times / reflect underrepresentation, but the published Appendix-D list does **not** map the two statuses item-by-item. No per-item zero-violation/sparse-violation label was invented.

The source also says the last nonredundant Dixonian constraint was learned 56th, so naive early stopping would throw away a known generalization. Twelve puzzling learned constraints refer specifically to `[+stress,-main]`; Hayes & Wilson themselves question the phonological naturalness of such nonhierarchical secondary-stress-conditioned sequencing constraints. Those qualifications are stored separately from the 57 table rows.

### Korean liquids

Kang's diachronic/modern loan data are now represented quantitatively rather than as a binary loan phonotactic. Word-medial English /l/ singleton realization is 2.3% (7/308) in the NIKL normative list but 9.1% (335/3670) in Choi's 367-speaker survey. Historical datasets show lower singleton rates in obstruent+/l/ clusters than intervocalically, and the 1930s regression retains cluster, post-tonic, English-initial-syllable, and especially Japanese-mediation effects. Separate Yun & Kang records capture dialect-, age-, and contact-conditioned initial-liquid allophony without turning proportional differences into categorical dialect rules.

### Tongan

Anderson & Otsuka directly support a phrase/domain analysis of definitive accent: it falls on the final word of the relevant NP, not necessarily the noun. DA strongly lengthens the final vowel and interacts with phonemic length, while F0 alignment supports penultimate-mora stress. This provides direct triangulation for earlier secondary-source Tongan stress records.

### Kalmyk / Oirat

Kaun's treatment separates postinitial **rounding neutralization** from productive rounding harmony: non-high rounded vowels are initial-syllable-only and absent from suffixes, while suffix alternations are front/back. Critically, Kaun notes that the cited Svantesson corpus has no /i/ flanked by back vowels; suffixal /i/ is the directly demonstrated neutral context. Therefore a blanket root-internal `/i/ = transparent` coding would overstate the evidence.

Suseeva (2025) adds modern positional and morphological detail, including a noninitial [o] exception in derivational `-go`. Her claim that Kalmyk vowel length is stress-conditioned rather than phonemic is preserved explicitly as a **source-specific competing analysis** and does not replace any shared inventory denominator.

### Jewish Arabic of Gabes

New records distinguish environmentally conditioned schwa qualities from lexically retained/loan short [u], preserve the rarity and uncertain status of short /o/, and separate historical /ay,aw/ contraction from a secondary, guttural/emphatic-conditioned tendency to re-diphthongize long /ī/. Frequency/tendency wording and variation are retained rather than made categorical.

### Samoan

Alderete & Bradshaw adds direct quantitative root evidence beyond the existing Kuo/Zuraw records. The new batch preserves the seven diphthongs in their syllabification plus the special initial-/ui/ glide qualification; the nearly categorical but nonabsolute /v/+back-vowel restriction (`vo` = 2 tokens, `vu` = 0); gradient V–V similarity effects; order-sensitive same-place C–C underrepresentation; and the fact that `ŋ...n` changes sharply depending on the corpus slice while identical `ŋ...ŋ` is overrepresented. This prevents accidental recoding of sparse gaps as categorical OCP constraints. The accessible HTML exposes exact sections/tables but not reliable PDF page numbers, so records state that pagination limitation rather than fabricate pages.

## Validation and repository integrity

A GitHub compare from baseline `683d994984c4745fcae5d8eb2c2f20cac8aa7e3d` to pre-checkpoint head `c233865e05cd1576dd7b820ea1e398e54f96e10c` reports **12 commits ahead, 0 behind**. The only changed paths are the 11 new shard JSONL batches and the one new read-only shard tool. There are no modified/deleted shared-curated files. The compare's per-file additions sum to exactly **93 empirical JSONL records** plus the tool.

Round-trip GitHub reads were performed on the new Wargamay and Samoan batches (including the final batch43) after their writes. New records were constructed with the shard validator's required provenance/link/confidence fields. The connector runtime does not execute repository Python, so the whole-shard `validate_jsonl_batch.py` and new weighted-constraint auditor were **not executed locally in this run**; this is a runtime limitation, not evidence of a validation failure. A local executable whole-shard pass remains worthwhile when the branch can be cloned/mounted.

## Source-access limitations handled conservatively

- Full Mosel & Hovdhaugen Samoan grammar access remained restricted; direct specialist sources and accessible quoted/descriptive material were used instead.
- The Jewish Gabes chapter endpoint was intermittently bot/JS-blocked; accessible book/search text was used, and no unreadable table was reconstructed.
- Some PDF screenshot requests cache-missed even where machine-readable text was available. Unreadable IPA/table content was never guessed.
- Where exact PDF pagination was unavailable (notably Alderete & Bradshaw's accessible HTML), section/table provenance is exact and pagination is explicitly marked unavailable.

## High-yield next queue

1. **Guugu Yimidhirr:** recover a reliably readable Haviland pp. 40–49 extraction and exhaust the medial-cluster inventory/restrictions, plus suffix-conditioned stress/quantity links.
2. **Samoan:** direct Mosel & Hovdhaugen if accessible; otherwise exhaust Alderete & Bradshaw's remaining CV/OE/root-frequency tables and reconcile all quantitative patterns with Kuo 2024 and Zuraw–Yu–Orfitelli domains.
3. **Yaygir:** direct Crowley §§2.2/2.3.1 for edge restrictions, clusters, and the /d/–[l] positional-neutralization analysis.
4. **Gumbaynggir:** direct Eades pp. 264–269 cluster tables and rare-root counterexamples.
5. **Jewish Gabes:** remaining assimilation and emphasis quantitative tables, including cross-word/domain variability where directly supported.
6. **Campidanese Sardinian:** reconcile stop fortition/lenition, stress-conditioned deletion, rhotic metathesis, and lexical/morphological exceptions across direct sources.
7. **Kalmyk/Oirat:** traditional phonemic-length analyses versus Suseeva's stress-based reanalysis; spoken distribution and harmony exceptions.
8. **Tongan:** remaining loan deletion/length tables, loan stress, and definitive-accent domain interactions.
9. **Wargamay:** now that the full 57-row model table is staged, reconstruct empirical support/violations from the training lexicon if a usable Dixon-derived dataset becomes available; keep this as reconciliation metadata rather than silently changing learned-model rows.
10. Run whole-shard JSONL/link/dedup validation plus the weighted-constraint auditor in an executable clone/mount when runtime access permits.
