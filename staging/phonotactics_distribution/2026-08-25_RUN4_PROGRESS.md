# PHONOTACTICS / DISTRIBUTION shard — continuation checkpoint

## Isolation and totals
Work remained exclusively on `agent/phonotactics-worker-20260825-1353` under shard-specific staging/tool paths. No shared curated denominator or canonical table was edited.

Prior checkpoint: 100 atomic records across 9 JSONL batch files.
This continuation: **31 atomic records across 6 new batch files** (**27 high-confidence, 4 medium-confidence**).
Current shard total: **131 atomic staged records across 15 batch files**.

## New batches and commits

| batch | focus | records | commit |
|---|---|---:|---|
| `2026-08-25_wargamay_additional_batch10.jsonl` | Wargamay learned-constraint qualifications / explicit overfit | 3 | `774b6a97fd575e3c1ac56b05738c71c7ca83b534` |
| `2026-08-25_samoan_domain_continuation_batch11.jsonl` | Samoan reduplication, PWd boundaries, ViVi, VVV, affix productivity | 8 | `75fc530c2b9c0a521de76a45be4b3f16959fec73` |
| `2026-08-25_shona_direct_batch12.jsonl` | direct Shona height harmony, /a/ opacity, rounding exception | 4 | `c3531cbd1fa10a6922990cd36050646d87c4bf96` |
| `2026-08-25_guugu_yimidhirr_batch13.jsonl` | root template, codas, positional allophony, C-V frequencies, weak harmony, vowel-length domain | 8 | `1afdbba169193aff7c97dd5907640444b256c46b` |
| `2026-08-25_tongan_stress_distribution_batch14.jsonl` | moraic stress, definitive accent, VV controversy, stress-conditioned vowel realization | 4 | `6f071ccd38a06b7e772238e033fdee5ac86984bc` |
| `2026-08-25_leti_metathesis_phonotactics_batch15.jsonl` | onset/cluster restrictions, phrase-edge vowel requirement, metathesis domains, high-V cooccurrence | 4 | `2c78af72910741c1b081c817a182bd4dbde22e91` |

## Main empirical additions

### Wargamay
- Separated weak minimal-word penalties from categorical phonotactics: both learned minimal-word constraints have weight 0.94, while 15 heavy monosyllables are actually attested (<1% of the corpus).
- Preserved Hayes & Wilson's own warning that several /i, i:/ CV/VC penalties likely reflect low segment frequency.
- Staged the explicit two-root overfit example (`ngaara`, `juura` in source transcription) as an `explicit_overfit_warning`, not a language-wide restriction.

### Samoan
- CV reduplication is integrated into the root PWd, but bimoraic reduplication has evidence for a PWd boundary; the latter is medium confidence because the diagnostic set is small.
- Identical vowels remain hiatus across compound boundaries in careful speech but fuse/behave long-vowel-like with monomoraic `-a` inside the PWd.
- Productive `-ina` projects its own PWd and blocks i+i fusion; semi-/unproductive `-Ci/-ia` can remain within the stem PWd.
- Diphthongisation is blocked by productive/compound PWd boundaries; final-VVV patterns were staged separately because final /a/ broadens the stress-disrupting VV set.

### Shona
- Direct Beckman extraction now records the full privileged-position generalisation rather than only the abstract: root-initial full height contrast, noninitial height licensing, root-to-extension harmony domain, opaque/blocking /a/, and the specific rounding-conditioned `e...u` exception to the simple height rule.

### Guugu Yimidhirr
- Direct Haviland §2.2: `C1V1(C2V2)n(C3)` root template, near-obligatory root-initial consonant with exactly two named particle exceptions, and a sonorant-only root-final inventory plus the isolated `gaw` /w/-final exclamation.
- Positional stop voicing and rapid-speech `d` -> rhotic realization were linked as allophonic/speech-rate records.
- Quantitative C-V cooccurrence skews and Haviland's explicitly weak statistical vowel-matching tendency were staged as frequency-qualified effects, not categorical harmony.
- Kager triangulation adds obligatory simple onset/nonbranching coda, bimoraic minimum with rare heavy monosyllables, and the no-exception stem-domain restriction of long vowels to syllables 1-2; compounds are retained as a domain counterexample to a naive absolute-word-position statement.

### Tongan
- Primary stress = penultimate mora of PWd; secondary stress is morphology-sensitive and loan-variable.
- Definitive accent final-vowel reduplication triggers stress shift and can yield a trimoraic final sequence.
- The literature disagreement over 'syllable fusion' is encoded as `explicit_analytical_uncertainty`; no disputed VV sequence was promoted to an established fact.
- Acoustic results record stress-conditioned vowel realization with explicit preservation of the lexical-stress/postlexical-accent confound.

### Leti
- Onset licensing and avoidance of tautosyllabic complex margins are linked directly to phrase-medial metathesis.
- Phrase-final vowel requirement is represented as a prosodic-edge restriction, distinct from phrase-medial syllable repair.
- CC- and CVV-triggered metathesis environments, the high-vowel deletion qualification, surviving sonority-licensed phrase-initial clusters, and lack of general epenthesis/deletion repairs are preserved rather than collapsed into a blanket no-cluster rule.

## Validation / provenance checks
- Every new row uses the shard schema: source ID, lect/time scope, domain, claim, source forms, formal and normalized environment, restriction type, scope, explicit exceptions/counterexamples, page/section/table provenance, confidence, parent/dependency links, and dedup key.
- All six writes were accepted as separate GitHub commits on the isolated branch. Round-trip content reads were completed for batches 10, 11, 13, 14, and 15; batch 12 was committed successfully with the same schema and was sourced from the directly inspected Beckman full-text sections.
- Guugu Yimidhirr root-frequency claims were taken from Haviland's direct §2.2 text; Kager was used only for the stronger prosodic interpretation and explicit 731-root counts.
- Tongan PDF pages 14-15 were visually checked as rendered pages; disputed syllable fusion remains unresolved by design.
- Leti records are from Hume's full 35-page manuscript, including §§2-3 rather than abstract-only extraction.
- No inferred exception counts or unattested environments were inserted.

## High-yield next queue
1. Finish Haviland Guugu Yimidhirr pp.40-49: medial cluster inventory/sonority and exact stress/length alternations under suffixation.
2. Exhaust Hume Leti pp.4-25 for onsetless-VV repair, secondary-articulation/glide distributions, cluster sonority exceptions, and phrase/morphology-conditioned alternants; cross-check van Engelenhoven where available.
3. Direct Anderson & Otsuka Tongan definitive-accent paper plus Zuraw/O'Flynn/Ward loan stress to replace second-hand stress/productivity summaries with primary records.
4. Continue Wargamay Appendix B: classify remaining 57 learned constraints into supported generalisation / frequency artifact / likely lexical overfit, retaining weights and violation evidence.
5. Direct Mosel & Hovdhaugen Samoan phonology/prosody tables, especially complete consonant cooccurrence, fast-speech reductions and register stratification.
6. Beckman/Fortune Shona: exact dialect/lexical strata, extension-by-extension alternants, and any documented loan/ideophone exceptions.
7. Resume direct-source verification of Smith candidates: Sardinian, Bakairi, Mongolian/Kalmyk, Pitta-Pitta and Mbabaram.
