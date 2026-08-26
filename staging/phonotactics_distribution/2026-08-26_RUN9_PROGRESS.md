# PHONOTACTICS / DISTRIBUTION shard — Run 9 checkpoint

## Isolation and baseline

- Repository: `rehan-muh/typology_database`
- Branch: `agent/phonotactics-worker-20260825-1353`
- Baseline checkpoint/head: `eff76631cc1d2030678decbb7751c517ba5fde24`
- Baseline staged empirical total: **335 atomic records across 43 JSONL batches**.
- This run wrote only under `staging/phonotactics_distribution/`. No shared curated denominator/canonical table was modified.

## New empirical batches and commits

| Batch | Records | Main coverage | Commit |
|---|---:|---|---|
| `2026-08-26_guugu_yimidhirr_clusters_batch44.jsonl` | 8 | Haviland medial C2 size/classes; homorganic NC; sonorant+peripheral and sparse laminal clusters; /yng/ accidental gap; sonorant+apical ban with retroflex-analysis qualification; morpheme-boundary repair; age/speaker variation; rare reduplicative violations | `ccd67ee1f01272c0d7aa67c242ecc139b4b8a915` |
| `2026-08-26_kuku_yalanji_phonotactics_loans_batch45.jsonl` | 12 | Root template/minimality; root-edge inventories; medial cluster inventory; systematic vs accidental gaps; boundary-domain relaxation and repair; cluster frequencies; CV co-occurrence; older vs younger loan strata; loan edge/cluster repairs | `41082b5ccff56d7b2700f3c6795b7e86f1bd5556` |
| `2026-08-26_kuku_yalanji_processes_prosody_batch46.jsonl` | 12 | Stop voicing; vowel/nasal/velar assimilation; morphologically indexed suffix harmony and neutral allomorphs; /y/ deletion; rare/frequent reduction processes; lexicalized partial reduplication; initial primary and optional style-sensitive secondary stress | `b2b501f63c8e56f08375f5f976ea3d669e81202c` |

**New empirical records this run: 32 across 3 batches.**

**Cumulative staged empirical total: 367 atomic records across 46 JSONL batches.**

**New-record confidence: 32 high.** Confidence refers to fidelity to the cited source statements, not to theoretical certainty; analytical qualifications, tendencies, and source-described accidental gaps remain explicitly coded as such.

## High-value extraction / reconciliation decisions

### Guugu Yimidhirr

The previously outstanding Haviland medial-cluster block is now represented at atomic resolution. C2 permits up to three consonants but is highly structured. Homorganic nasal-stop sequences are separated from the larger sonorant+peripheral class, and the much sparser sonorant+laminal attested set is not promoted to an exhaustive inventory where Haviland himself treats further combinations as possible. The unattested `/yng/` cell is explicitly stored as a **presumed accidental gap**, not a categorical ban.

The apparent `rd/rn/rnd` counterexamples to the sonorant+apical restriction retain Haviland's representational caveat that these can be analyzed as retroflex units. Morphology provides an important productivity test: reduplication/suffixation can create illicit liquid+apical sequences, with older-speaker `/rr/` deletion or `/l/`-conditioned retroflexization. Younger-speaker and Hopevale variation is preserved, rather than representing the repair as community-wide categorical grammar. Rare reduplicated medial `/w/` violations are also retained together with speakers' more usual self-corrected cluster-avoiding forms.

### Kuku Yalanji

A new 24-record grammar block adds a dense, internally linked phonotactic profile. Native roots are overwhelmingly disyllabic and consonant-initial, with three monosyllabic interjections and one specially qualified rhotic-initial lexical item. Root-final consonants are sharply restricted, while medial C2 permits structured two- and three-consonant clusters. Patz's key evidential distinction is preserved: symmetrical rhotic+palatal gaps motivate a proposed systematic restriction, whereas `/yng/` and `/ynyj/` are explicitly treated as possible accidental gaps; very low-frequency `/rn/` and `/rnd/` are stored as attested rare types.

Morpheme boundaries are coded as a separate domain. Reduplication, compounding and inflection may create clusters impossible inside roots, but most inflectional C+C contacts are repaired by vowel insertion and identical cross-boundary consonants are reduced because geminates are not licensed. Quantitative qualifications are retained: among 574 medial-cluster tokens, homorganic nasal-stop clusters account for 34%, `/l,rr/` plus a peripheral stop for 26%, and every other type for under 5%.

The English-loan material is explicitly stratified by contact period/speaker generation. About a score of older integrated loans display native-style phonological adaptation; Patz reports that this productive adaptation had largely ceased among younger bilinguals, who can combine English lexical forms with Kuku Yalanji morphology. Older-stratum repairs include cluster-breaking vowel insertion, one documented initial-cluster deletion case, glide prothesis before vowel-initial loans, and several final-consonant repair strategies. Sparse subpatterns are not generalized beyond the source evidence.

The process/prosody batch separates phonetic allophony from phonological/morphological restrictions. Stop voicing is a positional tendency, not a phonemic contrast. Regressive vowel palatalization, /n/ palatalization and /k/ labialization retain speaker-variable wording and the documented rule-ordering evidence. Suffix vowel harmony is coded as **morphologically indexed** (`u` after stem-final `u`, `a` after `a/i`) with neutral ergative/perlative allomorphs stored as explicit exceptions rather than forcing a word-wide harmony analysis.

The `/y/` deletion record preserves complementary-distribution evidence from inflection: post-/i/ `/y/` deletes word-finally or before another consonant, so citation forms can hide an underlying `-iy` recovered in morphology. Reduction processes are frequency-qualified: locative `-anga -> -a:` is very rare and rejected on playback, while causative `-bungal -> -bal` is frequent and potentially advancing. Six common verbs have lexicalized partial reduplication and are separated from productive full-root reduplication. Primary stress is initial; secondary stress is optional, morphology/length conditioned, and strongly speech-style sensitive.

## Validation / repository integrity

- GitHub round-trip reads succeeded for all three new JSONL batches after writing; UTF-8/IPA content and the intended branch paths are retrievable.
- A GitHub compare from baseline `eff76631cc1d2030678decbb7751c517ba5fde24` to empirical head `b2b501f63c8e56f08375f5f976ea3d669e81202c` reports **3 commits ahead, 0 behind**.
- The compare reports exactly three added files and per-file additions of **8 + 12 + 12 = 32 lines/atomic records**, matching the stated increment. No existing/shared file is modified or deleted.
- Parent/dependency links connect cluster generalizations to accidental gaps, repairs to the restrictions they diagnose, harmony to neutral allomorphs, and primary to secondary stress. Forward links within a batch or across already staged batches were deliberately retained where they resolve to named records.
- Existing shard-side read-only validators (`validate_jsonl_batch.py`, `summarize_staging.py`, `audit_source_conflicts.py`, `audit_weighted_constraints.py`) were not rewritten merely to duplicate their functionality.
- The connector runtime did not provide an executable mounted clone in this pass, so those Python validators were not falsely reported as executed. The GitHub round-trip and compare checks are the validation actually performed here.

## Source-access limitations handled conservatively

- Haviland's Guugu Yimidhirr grammar was machine-indexed sufficiently to recover the pp. 40–41 phonotactic discussion, but the large PDF endpoint would not render through the available PDF screenshot path. Exact page/section attribution therefore comes from the indexed grammar text; no visually unreadable table cell was reconstructed by guesswork.
- The official ANU Kuku Yalanji PDF endpoint was not reliably renderable in this run. Extraction used a complete accessible text transcription preserving the grammar's internal page, section and table numbering, cross-checked against bibliographic metadata for Patz's grammar. Claims requiring an unreadable image/table were not invented.
- Direct Eades Gumbaynggir full text remained inaccessible in the available web path. Sherer's accessible specialist treatment reproduces the cluster inventory, but because the shard already contains the corresponding secondary-source Gumbaynggir block, no duplicate pseudo-direct records were added simply to inflate throughput.

## High-yield next queue

1. **Kuku Yalanji:** exhaust any remaining quantitative Tables 2.3–2.6 and phrase/utterance prosody only where directly distributional; triangulate with comparative Guugu Yimidhirr/Wargamay patterns without collapsing lect-specific evidence.
2. **Gumbaynggir:** obtain direct Eades 1979 pp. 264–269; reconcile each cluster in the Sherer-derived batch against the primary inventory, including the three one-root laminal-nasal sequences and the exceptional `wg`/labial-velar patterns.
3. **Samoan:** finish remaining Alderete & Bradshaw root-frequency/CV/OE tables and reconcile quantitative cells against Kuo and Zuraw–Yu–Orfitelli; prioritize exact noncategorical gaps and domain effects.
4. **Yaygir:** obtain direct Crowley §§2.2/2.3.1 and replace provenance-only targets with primary edge/sequence records, retaining the underlying `/d/`–surface `[l]` neutralization distinction.
5. **Jewish Arabic of Gabes:** remaining assimilation/emphasis tables, cross-word variability, guttural/emphatic conditioning, and explicit marginal-vowel strata.
6. **Campidanese/Sestu Sardinian:** reconcile full stop fortition/lenition tables with stress-conditioned deletion, rhotic metathesis, lexical triggers and connected-speech qualifications.
7. **Kalmyk/Oirat:** direct spoken positional distributions and exceptions; keep traditional phonemic-length analyses separate from Suseeva's competing stress-based analysis.
8. **Tongan:** remaining loan deletion/length tables, loan-stress distributions, and definitive-accent domain interactions.
9. **Wargamay:** use a usable Dixon-derived lexicon, if obtained, to map empirical support/violations onto the already staged 57 learned Hayes-Wilson constraints without converting model penalties into grammatical facts.
10. **Validation:** when an executable clone/mount is available, run whole-shard JSON parsing, record/dedup uniqueness, parent/dependency resolution, staging summary, conflict audit and weighted-constraint audit in one pass.
