# PHONOTACTICS / DISTRIBUTION shard — 2026-08-25 checkpoint

## Scope
Continuation of the private phonological-taxonomy PHONOTACTICS/DISTRIBUTION shard only. Work is isolated on `agent/phonotactics-worker-20260825-1353`, based on the previous shard branch. No shared curated denominator or canonical table was edited.

## New staged batches

| batch | source focus | atomic records | confidence |
|---|---|---:|---|
| `2026-08-25_wargamay_continuation_batch07.jsonl` | Hayes & Wilson 2008, Wargamay §§8.3.3–8.4 | 10 | 10 high |
| `2026-08-25_samoan_synopsis_batch08.jsonl` | Alderete & Bradshaw 2012 Samoan grammar synopsis, principally Mosel & Hovdhaugen 1992 | 14 | 9 high, 5 medium |
| `2026-08-25_samoan_shona_triangulation_batch09.jsonl` | Zuraw, Yu & Orfitelli 2014 Samoan prosody + Beckman 1997 Shona | 6 | 5 high, 1 medium |
| **new this run** |  | **30** | **24 high, 6 medium** |

The prior checkpoint contained 70 atomic staged records across six batch files. The shard now contains **100 atomic staged records across nine batch files**.

## Empirical coverage added

### Wargamay
- Root-internal medial bi-/triconsonantal cluster structural types and cluster-slot restrictions.
- Place co-occurrence restrictions and homorganic nasal-stop preference.
- Explicit productivity qualification: about 2,400 logically possible clusters versus 46 perfect-scoring clusters in the learned grammar.
- Accidental gaps separated from rare-but-attested clusters.
- Inflection-only clusters and morphophonological repair/assimilation under the ergative/instrumental suffix.
- Yotic Deletion: /i/ survives prevocalically but is absent before consonants and word-finally.
- Right-to-left trochaic stress for all-light words; long-vowel-only heaviness; heavy syllables initial and primary-stressed.
- Polysyllabic final-stress ban and the resulting heavy-initial trisyllabic lapse pattern.

### Samoan: segmental distribution and speech/register conditioning
- Loan/formal-register restriction of /k h r/, with explicitly retained interjection/register qualifications.
- Fast-speech intervocalic stop voicing; weak aspiration; socially patterned /t/ affrication before /i/.
- Intervocalic and initial glottal-stop instability, including prothetic initial [ʔ] in strong prosodic contexts.
- Native-stratum /v/ co-occurrence restriction before back vowels.
- Morpheme-internal labial OCP/co-occurrence restrictions, identity exemption, direct counterexamples, and boundary/loan exceptions.
- Frequency/register warnings for apparent /n, ŋ, v/ co-occurrence gaps.
- Unstressed vowel reduction/gliding, final-vowel elision creating derived surface codas, and identical-vowel contraction at boundaries.
- `(C)V(V)` canonical syllable structure with derived fast-speech coda exceptions.
- Diphthong/hiatus inventory qualification, word stress, and phrasal accent restrictions.

### Samoan: direct specialist-prosody triangulation
- Root + close/monosyllabic suffix as one prosodic word versus prefixes and most disyllabic suffixes forming separate domains.
- Trochaic shortening as domain-sensitive long-vowel repair.
- Empirically delimited monomorphemic stress-disrupting VV inventory: /ai au ei ou/ versus ten explicitly non-diphthongising sequences; six sequences left unresolved for lack of suitable items.
- Morpheme-specific prosodic exceptions: ergative `-ina` as separate p-word, ergative/denominal `-a` idiosyncratic pre-stressing/foot-final behavior.
- Tentative high-vowel glide allophony, explicitly marked medium confidence because the source itself labels the section speculative.

### Shona direct triangulation
- Beckman 1997 directly confirms root-initial positional privilege: /e, o/ are contrastive root-initially and noninitial mid vowels require a root-initial mid-vowel harmony licensor. Corpus-level exceptions remain attached to the Hayes & Wilson records rather than inferred into the direct-source record.

## Provenance and reconciliation safeguards
- All 30 new records retain `source_id`, lect, time scope, domain, claim, source forms, formal environment, normalized environment, restriction type, source scope, exceptions/counterexamples, exact page/section/table provenance, confidence, parent/dependency links, and dedup key.
- Hayes & Wilson PDF pages covering Wargamay §§8.3.3–8.4 were visually checked as page images as well as text-extracted before staging.
- Zuraw, Yu & Orfitelli manuscript pp.1, 20, 30 and 41 were visually checked as page images; the records distinguish direct empirical generalizations from speculative glide analysis.
- Beckman record is limited to the article abstract because full-text access was not available; no unattested exception details were inferred from it.
- Samoan synopsis records explicitly identify that source as a synopsis and preserve lexical-stratum/register/speech-rate qualifications rather than collapsing them into categorical language-wide rules.
- Batch07 and batch09 completed GitHub contents round-trip reads after commit. Batch08 also round-tripped successfully; the connector truncated the display because of size, not because the file was incomplete.
- A full local validator/reconciler run was attempted by cloning the branch into the execution container. The container could not resolve `github.com`, so no network clone was possible. This is a transport/DNS limitation; no validation error was observed. Existing shard schema and unique dedup conventions were retained.

## Reusable tooling added
`tools/phonotactics_distribution/rank_candidate_pages.py`
- accepts form-feed-separated grammar/article text (e.g. `pdftotext -layout` output);
- ranks candidate pages using weighted cues for syllable structure, clusters, word-edge/positional restrictions, harmony, prosody, distribution/allophony, morphological domains, exceptions/loans/frequency qualifications, and formal tables/rules;
- rewards cue diversity to suppress isolated bibliography mentions;
- outputs TSV or JSONL with matched cue classes and previews;
- prioritizes only and never auto-creates linguistic facts.

## Checkpoints created this run
- `9e2eb904432f64365fee2330331a923819a2dfc9` — Wargamay continuation batch 07
- `203e7bd15060be9d035aba2349ee9b8b126a199f` — Samoan synopsis batch 08
- `f88c878bd3aaf34dd345d384f23fb21611dba4eb` — Samoan/Shona direct-source triangulation batch 09
- `a5581a7d37a5b07132648bea38afc2aa8d52f008` — reusable candidate-page ranker

## High-yield next queue
1. **Wargamay §8.5 continuation:** extract the 57 learned constraints without direct Dixon analogues, separating likely overfit/underrepresentation constraints from general restrictions; retain their violation counts/weights rather than promoting them categorically.
2. **Samoan Zuraw et al. §§4–7:** exhaust tables for individual mono-/bimoraic suffix classes, trochaic shortening productivity/asymmetry, coalescence, compound/reduplicant p-word boundaries, and VVV stress exceptions.
3. **Direct Samoan grammar triangulation:** Mosel & Hovdhaugen 1992 §§phonology/prosody, especially exact consonant co-occurrence tables, vowel sequences, glottal behavior, registers, and fast-speech reductions.
4. **Shona specialist continuation:** Beckman 1997 full article if accessible plus Fortune 1955, extracting exact suffix alternants, /a/ transparency/blocking behavior, root-initial privilege, morphological harmony domain, and lexical/idiophone/loan exception strata.
5. **Direct-source verification of Smith candidates:** Bolognesi 1998 (Sestu/Iglesias), Wetzels & Mascaró 2001 (Bakairi), then Mongolian/Kuman/Guugu Yimidhirr/Pitta-Pitta/Mbabaram original descriptions.
6. **Apply the new page ranker to the taxonomy grammar catalog** and prioritize grammars with dense intersection of cluster tables + allophony/distribution + prosodic/morphological-domain sections.
