# EURASIA shard checkpoint

## Exact branch state

- Structured JSONL source files: **12**
- Structured rows: **197**
- Core language/lect complexes: **10**
- Source works: **11**
- Major genealogical lineages represented: **7**
- Shared curated denominators edited: **0**
- All writes remain under `staging/eurasia/automation01_20260824_0005/` on `agent/phonology-eurasia-worker-20260824-0005`.

A count reconciliation caught an earlier bookkeeping error: the old report said 98 rows, but GitHub's per-file diff shows the seven pre-expansion files actually contained **100** rows (Udihe 22, not 21; Basque 14, not 13). This run added **97** new rows, yielding the exact current total **197**.

## Expansion completed in this session

### Eastern Khanty — Filchenko 2007, run 2: 18 rows
Exhausted the consonant/process portion that had been left in the queue: consonant-table structure, /p/ distribution, /m/ palatalization, vowel-conditioned /t s/ place realization, uncertain evidence for the /n/ ~ palatalized-n contrast, source-encoded /ƒ/ and /N/ distribution/allophony, apical–dorsal–cacuminal contrasts, nonphonemic contextual voicing, palatalization, reductive /w/ and /ƒ/ assimilation, consonant epenthesis, preconsonantal stop deletion, loan-cluster repair, derivational/inflectional gemination, multiple stress, and an **internal source inconsistency** in the prose vs formal syllable templates. The inconsistency is preserved as an analyst/source-disagreement row instead of silently normalized.

### Svan — Tuite 2004: 31 rows
Added an underrepresented Kartvelian language and pushed through the phonology/morphophonemics section rather than stopping at inventories: consonant inventory and disputed voiced uvular /G/; dialect-specific vowel inventories and length; analysis of /œ y/; initial vs final cluster asymmetry; loan-cluster epenthesis/prothesis; person-prefix cluster repair; historical final-vowel loss hypothesis; mobile-accent reconstruction; origins of long vowels; aorist accent-shift effects; poetic-register phonology; every-second-vowel reduction and its Lent’ex exception; schwa repair; reduction immunity as evidence for lost length; cross-word deletion + compensatory lengthening; palatal and lowering umlaut; target/trigger hierarchies; a three-stage umlaut chronology; labial metathesis; /r/ dissimilation; attributed voicing dissimilation; restricted ablaut; and two competing analyses of underlying ablaut vocalism.

### Shughni — Arno 2007: 10 rows
Added a Pamir/Eastern Iranian lect from a page-addressable phonology handout: consonant/vowel inventories, uvular /q/, nasal positional attestation with an explicit warning not to turn missing examples into categorical bans, long-vs-short vowel stability/allophony (attributed to Payne), positional consonant evidence, and all source-listed syllable shapes including CC onsets and up to CCC codas.

### Kâmviri / Kâmkata-vari — Strand specialist source: 26 rows
Added a Nuristani batch from Strand's field-based phonological description. Coverage includes explicit data/reliability scope, phonemic-vs-phonetic transcription policy, anticipatory cluster voicing, central-vowel fronting, historical /u/, dialectal front-rounded-vowel developments, marginal Dari/Farsi loan vowel, nasal-vowel history from *n, distinctive vowel length and accent, accent phonetics, nonphonemic vocalic on-glides, intervocalic voicing, utterance-final devoicing, /f/ loan adaptation, [ž] as /š/ allophony, doubtful y~i phonemic status, rhotic/retroflex analysis, ň~ṇ contrast, [λ̣] as /ṭl/, dental-to-retroflex place assimilation, intervocalic /k/ lenition, conservative treatment of dorsal/pharyngeal/laryngeal loan segments, terminal intonation, phonemic juncture, and expressive lengthening.

### Selkup — RAS Endangered Languages of Siberia: 12 rows
Added a Siberian Samoyedic profile with strong lect-scope safeguards: 25-vowel multidimensional inventory, 16-consonant inventory, intervocalic/post-sonorant semi-voicing, edge cluster/diphthong avoidance, /ŋ w č/ distribution, final nasal ~ homorganic stop ~ zero alternation, free dynamic/tonal stress, explicit absence of general vowel harmony, subdialectal reduced-suffix assimilation, common CV/CVC syllables, and a warning against projecting cross-dialect generalizations onto every Selkup lect.

## Provenance / integrity policy

Every newly staged record carries a stable `id`, `language`, `family`, `source_id`, `domain`, atomic `claim`, `confidence`, `verification_status`, and `dedup_key`, plus at least one exact provenance locator: page/pages, printed/PDF page, section, or table. Dialect/time/geographic scope, source orthography, dependencies, analyst attribution and uncertainty are retained whenever the source requires them. Missing examples are not converted into unattested-position claims; disputed analyses remain separate facts.

The shard-local validator remains at `tools/validate_jsonl.py`. It checks JSON parsing, required fields, source-location provenance, confidence vocabulary, duplicate IDs, duplicate dedup keys, exact repeated claims and dangling dependency IDs. The available GitHub connector cannot execute repository code, so I do not claim a remote validator run. I did reconcile **every file's row count against GitHub compare output**, which is how the earlier 98→100 baseline bookkeeping error was caught. New Eastern-Khanty and Svan batches were also constructed through JSON serialization with unique ID/dedup sets before staging.

## New checkpoints

- `9cc27584a725d9a2e6696bf2f5eeaa7963d10968` — Eastern Khanty consonants/processes run 2
- `0d6279e3a6ab0d54df36b7621a6a5a186dacfa88` — Svan phonology/morphophonology
- `aba264605c1d732deb18603038ee6c75a41664ca` — Shughni phonology
- `4a5a6248b41caa84f59a4d1507efb81f4ea76abd` — Kâmviri/Kâmkata-vari specialist batch
- `669db66ef7305021db49f42147e8ccead00645d7` — Selkup batch
- `ef77b83b4fcd243b2f3fa5ea2d61c15c28f6ebb1` — exact 197-row manifest reconciliation

Earlier checkpoints in this staging root remain intact and no canonical/shared file was touched.

## High-yield next queue

1. **Hinuq, Forker 2013 §§2.4–2.5** — obtain page text beyond the table of contents and atomize epenthetic vowels, o~zero, deletion, glide insertion, identical-vowel resolution, sonorant deletion, palatalization, ablaut, loan integration, reduplication and lexical-category stress.
2. **Ket, Georg 2007 §§3.3.2 and 4.4.4** — exhaust segmental allophony plus truncation/anaptyxis and tie rules to prosodic/morphotactic boundaries.
3. **Udihe reconciliation** — Kazama 2022 vs Nikolaeva & Tolskaya 2001 on vowel harmony, tone/prosody, dialect differences and historical loss; preserve disagreements rather than merging analyses.
4. **Oroqen** — Dresher & Nevins plus Zhang/Li source chain: RTR harmony, iterative low-vowel rounding, Xunke vs Baiyinna differences, high-vowel transparency/blocking, long-vowel trigger/target asymmetries, and explicit disagreement with Walker's analysis.
5. **Tofa / Altai-Sayan Turkic** — source-addressable Anderson/Harrison material on variable rounding/backness harmony and speaker-level optionality; prioritize derivational-vs-inflectional domain effects and language-shift conditioning.
6. **Nuristani expansion** — add Vâsi-vari or Ashkun from a grammar/specialist source and reconcile Strand's transcription/phoneme analyses against newer Halfmann/Degener work.
7. **Caucasus** — add another Northeast Caucasian lect not present in the historical Eurasia manifest, then a Laz/Mingrelian source to balance the new Svan coverage.
8. **East/Siberia** — add Oroqen plus a Chulym/Tofa lect before returning to already represented Udihe/Yukaghir.

Do not merge or canonicalize these staging records automatically. The next curated pass must compare dialect/time/source scopes and analyst disagreement explicitly.
