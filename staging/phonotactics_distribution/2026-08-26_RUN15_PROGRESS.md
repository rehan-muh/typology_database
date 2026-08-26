# PHONOTACTICS / DISTRIBUTION shard — Run 15 checkpoint

## Isolation and baseline

- Repository: `rehan-muh/typology_database`
- Branch: `agent/phonotactics-worker-20260825-1353`
- Baseline checkpoint/head: `2645d4273ae70c6207d275df59ad2119540667bb`
- Baseline staged empirical total: **397 atomic records across 49 JSONL batches**.
- This run wrote only under `staging/phonotactics_distribution/`. No shared curated denominator/canonical table was modified.

## New empirical batches and commits

| Batch | Records | Main coverage | Commit |
|---|---:|---|---|
| `2026-08-26_hewrami_direct_phonotactics_batch50.jsonl` | 29 | Tekht Hewramî syllable templates/frequencies; onset/coda and rhotic/lateral restrictions; heterosyllabic clusters; careful-speech epenthesis; stop positional allophony; intervocalic /d/ neutralization/deletion and counterexample; dialectal /b/ lenition; /w/ distribution; lexical-category and morpheme-indexed stress | `ddde2da47eec0306141c6b5054ef27a5141dd597` |
| `2026-08-26_tuatschin_direct_distribution_batch51.jsonl` | 26 | Stress-conditioned vowel quantity/reduction; German-loan marginal segments; diphthong inventory/gaps; hiatus vs gliding; cross-word elision and rare /n/ epenthesis; syllabic liquids; cluster reduction; rapid-speech affricate weakening; final devoicing with lexical counterexamples; complex-onset/coda structure; lexical stress | `acb25b2429571ece5c658b2bf6742fd0a0efd333` |
| `2026-08-26_sherbro_direct_phonology_batch52.jsonl` | 25 | CV(C); positional vowel length; closed-syllable centralization; loan vowel mapping; front/back free variation; exact coda classes; prenasalized-stop positional split; nasal assimilation/nasalization; palatalization; /w/ allophony; dialectal /h~w/; tone; onset strengthening; suffix vowel harmony | `d6cd839665f9c6cfeca5e4c8e3d236edaa4bf957` |
| `2026-08-26_paunaka_direct_phonotactics_batch53.jsonl` | 18 | Native (C)V(V) vs loan/derived codas and complex onsets; bimoraic minimality; iambic/trochaic stress and opaque pre-elision stress; reduplicative and /hV/ stress exceptions; person-marker and irrealis vowel elision; /j+i/ co-occurrence restriction; loan strata; rhinoglottophilia; speaker/style final prominence | `4ae694855f18075afe28d26c1aef154b95c885ba` |

**New empirical records this run: 98 across 4 batches.**

**Cumulative staged empirical total: 495 atomic records across 53 JSONL batches.**

New-record confidence: **96 high, 2 medium**. The medium-confidence records are explicitly noncategorical: Tuatschin's listed unattested diphthong cells are inventory gaps rather than demonstrated productive bans, and Paunaka's elder-/speaker-associated final prominence has an unresolved discourse function.

## High-value extraction and reconciliation decisions

### Tekht Hewramî

The new direct grammar layer distinguishes frequency from categorical licensing. CV, CVC and CVCC are the most frequent syllable patterns, while V, VC, CCV, CCVC and CCVCC are also attested. CCV may alternate with CVCV by /ɨ/ epenthesis, especially in careful speech and when the word is stressed; the unrepaired CCV form is therefore not coded as illicit. Complex-onset and coda statements preserve the grammar's gradient wording (`generally`, `often`, `usually`).

The rhotic/lateral system now exposes genuine positional structure: /ɾ/ and /ɫ/ can head internal syllables but not words, /r/–/ɾ/ is neutralized initially, /ɫ/ is coda-favored but can become an internal onset after suffixal resyllabification, and pharyngealized /rˤ/ is a low-functional-load internal-onset segment with speaker variation. Intervocalic /d/ has [ɹˠ] ~ [j] ~ zero realizations; [j] therefore creates positional phonetic neutralization with phonemic /j/. Post-rhotic /d/ deletion is explicitly nonexceptionless because `merđ` retains it.

Stress is represented by morphological domain rather than a single default rule: masculine/feminine noun tendencies, vocative penultimate stress, stress-bearing versus non-stress-bearing suffixes/clitics, adjective gender/degree patterns, present imperfective suffix stress versus subjunctive initial stress, and past-stem final-stem stress are separate records.

### Tuatschin

Reduced [ə, ɐ] are restricted to unstressed syllables, but their mutual distribution is left unresolved by the grammar. Vowel length is similarly stress-conditioned. The diphthong layer distinguishes the productive inventory from an explicit list of unattested sequences; the latter is medium-confidence because a lexical gap is not automatically a phonological ban. Several /iu, iɐ/ sequences vary between hiatus and gliding, while other forms are explicit hiatus counterexamples.

Across word boundaries, ordinary hiatus repair is weak-final-vowel deletion; /n/ epenthesis is rarer and associated more strongly with Standard Sursilvan usage. Final devoicing is encoded from the underlying-voicing evidence rather than as a mechanically reversible alternation: lexically voiceless /k/ in forms such as `briak`, `ljuk` and `fjuk` stays voiceless before vowels/voiced material, directly blocking the false rule that every final voiceless consonant voices before a voiced following segment.

The syllable layer records CC onsets as stop+liquid, CCC as /ʃ/+stop+liquid, lexical codas up to CC, and morphology-created CCC codas with plural `-s`. Stress is lexically fixed (ultimate, penultimate, rare antepenultimate); secondary stress remains explicitly unanalyzed.

### Sherbro

The direct grammar provides a useful positional inventory profile. CV(C) is the general pattern. Vowel length is contrastive only in monosyllables or the first syllable of disyllables and can shorten in compounds. /i/ and /e/ centralize in closed syllables, but the source includes an open-syllable [ə] counterexample for /e/, retained as such.

The coda inventory is kept segment-class specific, including the grammar's unitary treatment of prenasalized stops. Voiceless prenasalized stops are coda/medial biased, while voiced prenasalized sequences are onset/derived and usually arise after a nasal prefix loses syllabicity. Nasal place assimilation is obligatory before an obstruent within words and across morpheme boundaries. Vowel nasalization is noncontrastive and especially strong after /h/; loss of coda /ŋ/ can leave nasalization and compensatory lengthening.

Sherbro's boundary processes are separated into two linked onset-strengthening patterns: after a nasal, weak /l,w,j,Ø/ onsets may become [d]; after /l/, /w,j,Ø/ may become [l], yielding gemination. The suffix `-il/-ul` is separately coded as a morpheme-specific [back] harmony system rather than evidence for general lexical vowel harmony. Tone is retained as H/L contrast with lexical instability across speakers but active grammatical use.

### Paunaka

The native syllable canon is (C)V(V) with CV most frequent. Closed syllables are concentrated in loans; two native CVC cases are independently stored as probable vowel-deletion outputs. Spanish stop+/ɾ/ complex onsets can survive or be variably repaired by vowel insertion. All content words are minimally bimoraic; monomoraic verb roots require obligatory morphology before surfacing.

Stress is explicitly moraic. Most stems with three or more morae are parsed left-to-right as iambs with final-syllable extrametricality; bimoraic words are trochaic. Person-marker vowel deletion applies after stress assignment, producing opaque surface stress. Repeated material is not consistently extrametrical, and [hĩ]/[hɨ̃] only sometimes attracts stress; explicit normal-stress counterexamples prevent either tendency from becoming a categorical rule.

Person-marker elision has a strong lexical-class interaction: /u/-initial verbs trigger deletion, while the corpus's /u/-initial bound nouns preserve the person-marker vowel; the two apparent noun counterexamples are structurally verbal/nominalized. Initial /i/ of irrealis `-ina` deletes after diphthong/VV-final stems. The native segmental layer includes a direct /j+i/ co-occurrence restriction, while Bésiro-derived [ʃ,ʂ] belongs to the loan stratum. Rhinoglottophilia affects all vowels/diphthongs after /h/; other nasalization is optional and noncontrastive.

## Validation / repository integrity

- Before remote writes, the first three batches were machine-parsed locally: **80 records, 80 unique record IDs, 80 unique dedup keys, 0 schema errors**.
- GitHub round-trip reads succeeded for all four new batch files, preserving UTF-8/IPA and the expected record ordering.
- GitHub comparison from baseline `2645d4273ae70c6207d275df59ad2119540667bb` to empirical head after batch53 reports **4 commits ahead, 0 behind**.
- The compare reports exactly four added staging files with **29 + 26 + 25 + 18 = 98 additions/atomic records**, and no modified or deleted pre-existing/shared file.
- The Paunaka batch was also round-trip read from the branch after creation. Its 18 JSONL objects use the same required staging fields as batches50–52.
- Existing read-only validators/auditors were left unchanged; there was no need to create tool churn this run.

## Source-access notes

- Hewramî: direct Language Science Press GitHub LaTeX source (`langsci/517`, chapter 3). Section/table provenance is exact; printed PDF page numbers were not guessed.
- Tuatschin: direct Language Science Press GitHub LaTeX source (`langsci/308`, chapter 2). Section/table provenance is exact; printed page numbers were not guessed.
- Sherbro: direct Language Science Press GitHub LaTeX source (`langsci/403`, `chapters/phonology.tex`). Section/table/example provenance is exact; no page-image verification is claimed.
- Paunaka: direct Language Science Press GitHub LaTeX source (`langsci/400`, `chapters/3-03_Phonology.tex`). Section/table/example provenance is exact; printed page numbers were not guessed.
- Direct Crowley Yaygir and Eades Gumbaynggir access was retried through publisher/handbook endpoints. Chapter HTML/PDF access remained blocked/cache-missed, so no pseudo-primary records were generated from inaccessible text.

## High-yield next queue

1. **Hewramî:** exhaust remaining verb/adposition stress subsections; turn the heterosyllabic C×C frequency table into row/cell records; finish vowel positional/allophonic distributions and source-qualified cluster gaps.
2. **Paunaka:** row-level diphthong/vowel-sequence inventory; exact /β/ following-vowel allophones; the remainder of person-marker nonelision table; /a+ina/ fusion; complete word-initial /a,u/ deletion table with speaker counts; marker-conditioned stress table.
3. **Sherbro:** row-level prenasalized-stop distributions; full nasalization and tone paradigms; derivational vs past-suffix harmony tables including explicit exceptions; onset-strengthening contexts at individual boundary types.
4. **Tuatschin:** full diphthong table row-by-row; distinguish lexical gaps from phonotactic statements; final-obstruent sandhi by segment; full syllable-type table and morphologically created coda cells.
5. **Gumbaynggir/Yaygir:** retry direct primary access; if still blocked, immediately fall through to another directly accessible grammar rather than mining secondary summaries.
6. **Cross-source reconciliation:** compare newly staged Paunaka records against earlier isolated-run Paunaka material before any future merge, especially stress exceptions, native CVC status and loan-stratum restrictions.
7. **Whole-shard validation:** when an executable mounted clone is available, run JSON parse, unique IDs/dedup keys, parent/dependency resolution, environment normalization and conflict audit over all **495** staged records.
