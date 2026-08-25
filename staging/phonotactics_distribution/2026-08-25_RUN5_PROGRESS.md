# PHONOTACTICS / DISTRIBUTION shard — continuation checkpoint

## Isolation and totals
Work remained exclusively on `agent/phonotactics-worker-20260825-1353`, under shard-specific staging/tool paths. No shared curated denominator or canonical table was edited.

Prior checkpoint: **131 atomic records across 15 JSONL batch files**.
This continuation: **16 atomic records across 3 new batch files**, all **high confidence**.
Current shard total: **147 atomic staged records across 18 batch files**.

## New batches and commits

| batch | focus | records | commit |
|---|---|---:|---|
| `2026-08-25_leti_distribution_continuation_batch16.jsonl` | Leti stress/weight, resyllabification, high-V secondary articulation, repair ranking, CVV conditioning, compensatory lengthening, phrase-initial cluster licensing | 8 | `1ce730eaf4d73970aff3ae1a8407b64699e6284d` |
| `2026-08-25_tongan_loans_batch17.jsonl` | direct Tongan loan secondary stress, deletion, final-V length, native/loan stratum distinctions | 5 | `14a229ff6d2b13f7fac726a0e7b28c202874e77b` |
| `2026-08-25_wargamay_model_evidence_batch18.jsonl` | training-set exceptions + Appendix-D/model-only constraint status | 3 | `769e2785269c8e31e690847025a36585409f220d` |

Reusable validator added:
- `tools/phonotactics_distribution/validate_jsonl_batch.py` — commit `4e6d247ab6ca645d18aeae1787d867bbc540a499`.

## Empirical additions

### Leti
- Added prosodic-weight and morphology interaction: long vowels are obligatorily stressed in the analysis, secondary stress alternates leftward, and suffixes are described as typically extraprosodic; consonantal codas are non-moraic.
- Distinguished V-final phrase-medial behavior from C-final metathesis: before simple onsets, V-final forms do not undergo the same VC metathesis; final high vowels may surface as secondary articulation and deletion is context-conditioned.
- Added boundary resyllabification: a first-morpheme final consonant supplies the onset before a following vowel-initial morpheme.
- Added unstressed prevocalic high-V glide/secondary-articulation distribution across both internal and morpheme-boundary contexts, with source examples retained.
- Encoded the source's repair preference: vowel deletion is a last-resort strategy where metathesis or secondary articulation can preserve vocalic material.
- Added the V-final + CVV environment in which metathesis would itself create an onsetless syllable and glide/secondary-articulation repair surfaces instead.
- Added environment-specific compensatory lengthening for VVC-final morphemes whose final vowel is transposed/deleted; this is explicitly not generalized into a universal consonant/vowel-loss rule.
- Reconciled initial-cluster evidence: sonority-licensed phrase-initial CC sequences can surface, so `*COMPLEX` is not a categorical ban on every surface cluster.

### Tongan loans
- Direct Zuraw, O'Flynn & Ward (2019) records replace generic loan qualifications with measured distributions from three speakers.
- Secondary stress is probabilistically repelled by vowels with no English correspondent. The paper reports 26% V1 stress when V1 is epenthetic versus 66% when V1 corresponds to an unstressed English vowel in the relevant comparison; V1 stress reaches about 84% overall in the compared cells when V2 is epenthetic.
- Vowel deletion is significantly more likely for epenthetic vowels (reported model coefficient 1.492, p=.005), while remaining variable and speaker-sensitive.
- Final vowel length has a three-way source-conditioned distribution over 114 relevant tokens: it is most favored after an epenthetic penult, intermediate after a penult corresponding to English unstressed material, and disfavored after a penult corresponding to English stressed material.
- Native-versus-loan stratum linkage is explicit: marginal distinctions in loans are manifested through stress, deletion probability, and final length, not naively as free permission for native-illegal CC forms.

### Wargamay model evidence
- Staged the 43-versus-57 distinction explicitly: 43 discussed learned constraints correspond to the phonotactics Hayes & Wilson identify from Dixon, while 57 additional learned constraints have no direct Dixon analogue and require evidential reconciliation.
- Preserved training-data construction counterevidence. Reduplicated forms and a handful of blatant violations were removed before training; loans and exceptional cluster/final-obstruent forms therefore cannot be used as if the learned grammar had been fit to an exception-inclusive denominator.
- Appendix D is represented as a weighted model-output inventory (57 constraints, weights 3.91 down to 0.40), not as 57 independently established categorical restrictions.

## Validation and provenance
- The three new JSONL batches retain the shard schema: source ID, lect/time scope, domain, claim, source forms, formal and normalized environments, restriction type, scope, explicit exceptions/counterexamples, page/section/table provenance, confidence, parent/dependency links, and dedup key.
- All three writes committed independently to the isolated branch and all three completed GitHub round-trip reads after writing.
- Tongan records use the directly accessible 2019 author manuscript and preserve sample sizes, raw percentages, model coefficient, and probabilistic language. No probabilistic effect was converted into a categorical constraint.
- Leti records use Hume's full manuscript; the web PDF renderer's screenshot cache failed during this run, but the source's indexed full text remained directly readable with page-localized sections/examples. No claim requiring unreadable figures was staged.
- Hayes & Wilson Appendix D and Wargamay training-data footnote were read directly from the full article. PDF screenshot calls also cache-missed, so feature strings that were not safely recoverable from text extraction were deliberately not normalized as IPA facts.
- New validator checks JSON syntax, required provenance fields, confidence vocabulary, duplicate `record_id`/`dedup_key`, and unresolved parent/dependency references among supplied files/optional known-ID index. It is read-only and cannot alter curated data.

## Blocked / deferred sources
- Mosel & Hovdhaugen's Samoan grammar remains access-restricted in the surfaced full-text host; no mirror-derived categorical facts were added.
- Haviland's Guugu Yimidhirr PDF is accessible as a very large source but was not reliably renderable through the current PDF path; rather than infer pp.40–49 cluster details from incomplete snippets, that continuation was deferred.
- PDF image screenshots for the accessible Hume, Zuraw et al., and Hayes & Wilson texts returned cache-miss errors. Text extraction remained available, and only claims with direct text/page provenance were staged.

## High-yield next queue
1. **Leti direct continuation:** exhaust the remainder of Hume's phrase-final section and secondary-articulation/OCP discussion, then triangulate with van Engelenhoven for lexical class and dialect/phrase-domain qualifications.
2. **Tongan direct continuation:** vowel-deletion tables and complete final-length raw distributions in Zuraw et al.; Anderson & Otsuka definitive-accent direct paper when the full article body is accessible.
3. **Wargamay Appendix D reconciliation:** map each of the 57 weighted constraints against corpus support/violations and classify as supported gradient generalization, frequency artifact, likely lexical overfit, or unresolved model-only pattern. Keep weights and support counts separate from language facts.
4. **Guugu Yimidhirr:** seek a smaller/text-readable Haviland copy or chapter extraction for pp.40–49 before adding exact medial-cluster and suffixal length/stress records.
5. **Direct Smith-candidate verification:** Sardinian/Sestu-Iglesias, Bakairi, Kalmyk/Mongolian, Pitta-Pitta and Mbabaram, prioritizing directly readable grammars or specialist full text.
6. **Fresh grammar mining with the candidate-page ranker:** prioritize sources where syllable/cluster tables intersect with allophony, prosodic conditioning, and morphology/exception sections, to maximize independent restrictions per source.
