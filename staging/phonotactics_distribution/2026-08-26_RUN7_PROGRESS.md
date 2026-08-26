# PHONOTACTICS/DISTRIBUTION shard — Run 7 checkpoint

## Isolation
- Repository: `rehan-muh/typology_database`
- Branch: `agent/phonotactics-worker-20260825-1353`
- Baseline checkpoint: `1d807e9f19ca1eb840c886c1076cc2c2e8ab0080`
- Shared curated denominators/canonical tables: **not modified**.

## Exact counts
- Baseline: **187 atomic records / 24 JSONL empirical batches**.
- Added this run: **55 atomic records / 8 JSONL empirical batches**.
- End state: **242 atomic records / 32 JSONL empirical batches**.
- New-record confidence: **54 high, 1 medium**.

## Empirical commits
1. `246fe9b04971bfdb5bdf4ffb02a67cdc0ced1e5d` — `2026-08-26_sardinian_smith_direct_batch25.jsonl` — 7 records.
   - Sestu vs Iglesias initial-onset microvariation; prothesis; CGV/rising-diphthong contrast; connected-speech qualification; observed facts kept separate from Smith's nuclear-on-glide analysis.
2. `1e4d3a34825d75066e2b0723461f309c16fd2c40` — `2026-08-26_pitta_pitta_reconciliation_batch26.jsonl` — 8 records.
   - Initial-liquid restriction, explicit proper-name/language-name exceptions, initial high-vowel/glide source disagreement, fixed initial stress, minimality, gradient laminal-before-/u/ frequencies.
3. `06127e65435bc5956935d071ab2649f469651555` — `2026-08-26_yaygir_edges_neutralization_batch27.jsonl` — 5 records.
   - Underlying initial-liquid restriction, initial /d/∼[l] neutralization, final-segment inventory, historical onset loss, direct-primary-source section map.
4. `0e177e17fa13ed81e2b26dbabb64bbdb374caa74` — `2026-08-26_campidanese_distribution_metathesis_batch28.jsonl` — 8 records.
   - Stop spirantization distribution, [z] complementarity, suffix/copy-vowel allophony, lenition non-targets and lexical variability, stress-conditioned /n/ deletion, synchronic rhotic metathesis, metathesis-conditioned stop effects, lexical raddoppiamento trigger set.
5. `0f207439eae86afea62e9444cdda8ad52f113fde` — `2026-08-26_jewish_gabes_phonotactics_batch29.jsonl` — 10 records.
   - Syllable-template inventory, open-syllable quantity restriction and imperative exceptions, initial CC/rare CCC, morphology- and guttural-conditioned epenthesis, final-CCC repair, final-cluster cooccurrence, edge asymmetry, morphological overrides, mobile weight-sensitive stress.
6. `b6320b01f8f387f6241ad815af0dcb6f3cc1d4b8` — `2026-08-26_jewish_gabes_emphasis_batch30.jsonl` — 5 records.
   - Trigger-specific /y/ opacity/transparency, phonological-word rightward spread, inflectional-prefix exclusion, cross-word source disagreement, negative-suffix emphatic allophony and /x/ triggering.
7. `54137039c2990cbf976b73340eb0ef9d7c6c5c12` — `2026-08-26_gumbaynggir_clusters_stress_batch31.jsonl` — 6 records.
   - Root-medial cluster grammar, rare cluster exceptions, morpheme-boundary generalization, long-vowel/glide-coda stress attraction, monosyllabic-root qualification, long-vowel-plus-cluster permission.
8. `5fbebf80d5181247502c3ac6ef820a6eb783ef1e` — `2026-08-26_korean_liquid_strata_batch32.jsonl` — 6 records.
   - Native/Sino initial-liquid restriction, Sino positional repair, English-loan relaxation, position-specific liquid adaptation, diachronic retention rates, residual gradient [n] repair in present-day speech.

## Tooling checkpoint
- `d63f91e655eed85770d0d508018763e374759ff9` — `tools/phonotactics_distribution/audit_source_conflicts.py`.
- Read-only review utility grouping records by lect + normalized environment and surfacing multi-source heterogeneous claims plus explicit `source_disagreement`/`analysis_uncertainty` records.
- Intentionally over-flags for human reconciliation; never edits staging or curated data.

## Validation / provenance status
- All eight empirical files were accepted as independent commits on the isolated shard branch.
- GitHub round-trip reads succeeded for batches 25–32 after writing. This verifies the files are present on the intended branch and the stored UTF-8 JSONL content can be retrieved.
- Parent/dependency relations were used to connect triangulations, exceptions, repairs, and analysis-qualification records to the facts they qualify.
- No direct-source fact was fabricated when a primary PDF was inaccessible.
- Direct Crowley 1979 PDF access was blocked; Yaygir's detailed records therefore use Proctor/Evans secondary extraction while a separate provenance-only record identifies Crowley's primary §§2.2/2.3.1 targets.
- The Jewish Gabes OpenBook PDF endpoint was bot/JS blocked; indexed full-text sections and other accessible copies/search results were exhausted instead.
- Direct Pitta-Pitta grammar retrieval was blocked in this pass; disagreements among Blake & Breen/Blake descriptions are represented explicitly rather than silently reconciled.
- A local whole-shard validator/summarizer clone attempt could not resolve `github.com`; connector-side GitHub reads/writes remained healthy. Treat this as a transient local DNS/transport limitation, not as a detected schema/data error.

## Important reconciliation decisions
- **Sestu/Iglesias:** observed onset/CGV distributions are separate from the proposed subsyllabic representation of glides.
- **Pitta-Pitta:** rare language-name/clan-name liquid-initial forms remain explicit exceptions; initial /i,u/ + homorganic-glide descriptions remain a source conflict.
- **Yaygir:** surface initial [l] from /d/∼[l] neutralization does not recode the language as having a free underlying initial-/l/ contrast.
- **Jewish Gabes:** emphasis domains are trigger-, direction-, and morphology-sensitive; a one-domain harmony record would erase documented opacity and cross-word disagreement.
- **Korean:** native/Sino restrictions, recent loan phonotactics, orthographic diachrony, and spoken residual repair are kept in distinct strata.
- **Gumbaynggir:** dominant cluster patterns, one-root rare types, and cross-morpheme behavior are represented separately; frequency exceptions are not converted into categorical permissions.

## High-yield next queue
1. **Wargamay:** complete constraint-by-constraint reconciliation of all 57 Hayes–Wilson learned penalties against observed forms, violations, accidental gaps, and explicitly identified overfit; preserve model weight as model evidence rather than categorical grammar.
2. **Yaygir:** direct Crowley 1979 §§2.2 and 2.3.1 from an accessible mirror; extract the full permissible sequence tables and any morphological/phonetic qualifications.
3. **Gumbaynggir:** direct Eades 1979 pp. 264–269 and lexical tables; verify Sherer's sequence inventory and retrieve any word-edge/onset/coda distributions omitted by the reanalysis.
4. **Jewish Gabes:** exhaust remaining §5 material (word-initial prothesis, epenthetic-vowel quality, final patterns), diphthong distributions, and full emphasis Table 5/6 contrasts.
5. **Korean:** quantify age/lexical effects on initial-liquid repair and medial /l/ singleton/geminate adaptation; mine cluster restrictions involving sonorants/liquids.
6. **Campidanese/Sestu:** full fortition/lenition table reconciliation and primary Bolognesi metathesis/prothesis distributions if direct text becomes accessible.
7. **Guugu Yimidhirr:** finish direct medial-cluster inventory plus suffix-conditioned length/stress evidence.
8. **Tongan/Samoan and Kalmyk/Oirat:** remaining direct tables, loan/native strata, harmony exceptions, and productivity/frequency qualifications.
