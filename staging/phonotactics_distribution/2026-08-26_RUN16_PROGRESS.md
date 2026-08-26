# PHONOTACTICS/DISTRIBUTION Run 16 progress

## Exact counts

- Baseline from Run 15 checkpoint: **495 atomic records / 53 JSONL batches**.
- Added this run: **133 atomic records / 6 JSONL batches**.
- New-batch split: Komnzo **22**, Moloko **20**, Ik **20**, Japhug **16**, Yakkha **31**, Rapa Nui **24**.
- Confidence in new records: **130 high / 3 medium**.
- Canonical shard staging after this run: **628 atomic records / 59 JSONL batches**.
- Shared curated denominators/canonical tables modified: **0**.

## Empirical commits

1. `49f09612e6447c574b7995721791c158f958291e` — Komnzo batch54 (22 records)
2. `3698875492f1c61c888443531e057c4f6b431ea5` — Moloko batch55 (20)
3. `d4beea257d8e8ef88a67b3381d5bc5540bee3394` — Ik batch56 (20)
4. `6a307d49ebd41e3ab7d423df09787f54a2c6f188` — Japhug batch57 (16)
5. `dd4dab2203003f700f2872473386227bf46156b6` — Yakkha batch58 (31)
6. `556127dffab708c2767a83bb3d0929d40ed4a97c` — Rapa Nui batch59 (24)

GitHub comparison from prior checkpoint `2c1021c6e1ecbf229339d9c7c2463d0605280b44` to the final empirical commit reports **6 commits ahead, 0 behind** and exactly six newly added files with **22 + 20 + 20 + 16 + 31 + 24 = 133 additions**, no deletions and no changes to pre-existing files.

## Validation

- The locally constructed Komnzo, Moloko, Ik, Japhug and Yakkha batches (109 records) passed schema/field validation: **109/109 unique record IDs, 109/109 unique dedup keys, zero unresolved local parent/dependency links, zero confidence-vocabulary errors, zero required-field errors**.
- Rapa Nui batch59 was separately remote-round-trip checked after creation; GitHub reports exactly **24 added JSONL lines** and the returned file parses at the record-line boundary inspected. It follows the same shard schema and identifier/dedup convention.
- Remote round-trip checks were performed on newly written staging files; the live compare confirms only shard-specific additions.
- Existing reusable tools under `tools/phonotactics_distribution/` were inspected and already cover batch validation, staging validation, candidate-page ranking, normalized constraint reconciliation, weighted-constraint auditing, source-conflict auditing and staging summaries. No redundant validator was added.

## Main additions

### Komnzo

Direct extraction from Döhler's Language Science Press source substantially deepens the previously shallow Komnzo profile. New records cover onset-only /kʷ, ᵑgʷ/; the geminate inventory and exclusions; syllable-coda devoicing versus exceptional word-final-only /r/ devoicing; resyllabification-induced restoration of voicing; a broad heterosyllabic C×C system; restrictions on prenasalized Cb; a corpus-only homorganic nasal+prenasalized gap retained as medium-confidence non-categorical evidence; onset maximization; k.w/ᵑg.w versus complex-segment diagnostics; the ordered right-to-left epenthesis algorithm; morpheme-specific epenthesis placement; glide-conditioned epenthetic vowel quality; onset requirements; and specified-vowel bimoraic minimality.

### Moloko

Direct Friesen extraction links consonantal-root structure, epenthesis, stress, and the language's word-level palatalization/labialization system. The staging separates the single underlying vowel /a/ from prosodically conditioned full vowels and epenthetic-vowel allophones; suffix/root prosody from its leftward word-level domain; cross-word non-spreading; phrase-final stress from its obligatory full-vowel realization; consonant targets such as /nz/→[nʒ]; neutral-suffix prosodic neutralization; and citation-form effects. Source sample size (~1,500 lexical items) is retained as a provenance/frequency qualification.

### Ik

The new direct Ik block adds final vowel requirements and pause-conditioned devoicing, final consonant devoicing, initial-only [ɦʲ], lexically indexed deaffrication, place-based haplology with explicit 3pl exception, velar deletion before -uƙot-, final/non-final morpheme alternations, progressive and regressive vowel assimilation, back-vowel desyllabification plus compensatory lengthening and the nominative exception, word-level ATR harmony, /a/ blocking, dominant [+ATR] suffixes, compound blocking and second-member-/i/ exception, host-copying versus dominant clitics, and tone-domain records.

### Japhug

The grammar's updated onset inventory is staged as at least **424 clusters (320 CC + 104 CCC)** with inherited/ideophone/Tibetan-loan stratification. Productive partial reduplication supplies a live diagnostic of cluster constituency: /ɯ/ reduplicant nuclei round after /u,o/; specified final sonorants delete under well-defined preceding-consonant classes; other clusters retain them; /rj-/ gives an explicit exception. The source's restricted preinitial inventory, near-absence of stop preinitials, and the fact that heterosyllabic/secondary clusters are outside the 424 count are all separated into distinct records.

### Yakkha

Direct Schackow extraction adds the five-vowel system, marginal diphthongs and their lexical strata, initial-r restriction, loan retroflexes, complex onset inventories, prefix-derived NC onsets, nasal place assimilation, restricted coda inventory, coda-stop neutralization, prosodic-word-final glottal exclusion, morphology-conditioned CC repair, highly restricted fast-speech NCL clusters, multiple Nepali/English loan repairs, initial/closed-syllable-sensitive stress, construction-specific stress domains, and a detailed contextual voicing system. Voicing is decomposed into its general environments, speech-rate effects, nasal-versus-vocalic prefix asymmetry, aspirated-stop non-targets/function-verb exceptions, intervocalic continuant lenition, suffix/clitic exceptions, and the stem-final /t/ exception.

### Rapa Nui

The direct Kieviet source adds strict native `(C)V(ː)` syllables and the analysis of all non-identical VV as disyllabic, supported separately by reduplication, stress and metrical evidence. The word-level layer preserves moraic weights, trochaic parsing, noninitial-foot minimality, the grammar's strong heavy+odd-following-mora restriction, Tahitian-loan shortening, exact metrical-pattern frequencies, and the fact that 7–8 mora lexical entries are restricted to reduplications/compounds. Loan codas are retained as a separate non-moraic stratum. The particle-glottal analysis is quantitative: phrase-initial particles have [ʔ] in **755/792 = 95.3%** of tokens, while non-phrase-initial particles lack [ʔ] in **1020/1088 = 93.8%**; this is stored separately from genuine lexical/content-word /ʔ/ contrast. Initial /ŋ/ is recorded as a strong frequency bias rather than a ban, and the >1.6M-segment corpus frequency qualification is preserved.

## Source/access notes

- Komnzo, Moloko, Ik, Japhug, Yakkha and Rapa Nui were mined from directly accessible Language Science Press LaTeX source repositories, so section/table provenance is preserved without inventing printed page numbers.
- Direct Gumbaynggir (Eades) and Yaygir (Crowley) primary-source access was retried in the surrounding shard work and remained blocked/cache-missed; no pseudo-primary records were generated.
- No source absence, corpus zero, analytical proposal, or historical explanation was promoted to a categorical synchronic restriction without explicit qualification.

## High-yield next queue

1. **Komnzo**: finish the row-level heterosyllabic C×C matrix, onset tables, stem/affix-specific epenthesis exceptions, and full stress/quantity interactions.
2. **Yakkha**: complete the stress tables, nasal-to-vowel nasalization before glides/liquids, deletion/gliding processes, loan tables at row level, and dialectal Tumok/non-Tumok voicing splits.
3. **Rapa Nui**: extract the full §2.3.3 consonant/vowel co-occurrence tables, §2.4 stress/phrase-stress rules, §2.5 regular/lexicalized processes, and loan cluster inventories; distinguish Tahitian from Spanish strata.
4. **Moloko**: exhaust the remainder of Ch.2 for segmental target/non-target tables, syllable/word-break restrictions, tone interactions, fast-speech restructuring, and morpheme-specific prosody neutralization.
5. **Japhug**: row-level two-/three-consonant onset inventories by preinitial/medial class, heterosyllabic clusters, synizesis-derived secondary clusters, and reduplication exceptions.
6. Retry direct **Gumbaynggir/Yaygir** primary access; if blocked, immediately move to the next open direct grammar rather than stall.

## Isolation

All writes in this run are confined to `staging/phonotactics_distribution/` on branch `agent/phonotactics-worker-20260825-1353`. Existing curated denominators and canonical data files were not altered.
