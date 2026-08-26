# PHONOTACTICS / DISTRIBUTION shard — Run 10 checkpoint

## Isolation and baseline

- Repository: `rehan-muh/typology_database`
- Branch: `agent/phonotactics-worker-20260825-1353`
- Baseline checkpoint/head: `cf3a57be804e5b01c649ad35c0c6ae4b71585dac`
- Baseline staged empirical total: **367 atomic records across 46 JSONL batches**.
- This run wrote only under `staging/phonotactics_distribution/`. No shared curated denominator/canonical table was modified.

## New empirical batches and commits

| Batch | Records | Main coverage | Commit |
|---|---:|---|---|
| `2026-08-26_samoan_direct_structure_batch47.jsonl` | 11 | Direct Alderete & Bradshaw: syllable template; diphthong working analysis and qualifications; weight-sensitive stress and boundary-domain exception; loan consonants/register mergers; canonical root-size criterion; medial syllable distribution; positional consonant frequencies; `/v/`+back-vowel near-gap; diphthong counts | `87f9479df327defdb075721ed785217c8eab7537` |
| `2026-08-26_samoan_direct_vv_batch48.jsonl` | 8 | Cross-syllabic vowel O/E matrices; `/a/` neutrality; order effects; disyllabic χ²; significant association/dissociation cells; gradient similarity interpretation; front-back extension; robustness across root-length samples | `270c3ef3963c0af831713c917037b3f361ffc84d` |
| `2026-08-26_samoan_direct_cc_batch49.jsonl` | 11 | Homorganic consonant underrepresentation; labial order effects; positional-bias reconciliation; accidental-gap qualification; coronal sonorancy interaction; nasal and historical dorsal/glottal patterns; Table 17 aggregate counts; place-specific OCP strength | `1e30f4e346e03eb88456eadddf10f2982596cfaa` |

A targeted table-reconciliation correction to batch49 was committed as `de06b76c9b308826e5e8bcfaa486adc4bebea724`: `/m...v/` is zero in the **disyllabic** sample, but is attested in the all-root sample with O/E `.27`. The record now preserves both cells and explicitly prevents the disyllabic zero from being promoted to an exceptionless lexical ban.

**New empirical records this run: 30 across 3 batches.**

**Cumulative staged empirical total: 397 atomic records across 49 JSONL batches.**

**New-record confidence: 30 high.** Confidence indicates fidelity to the source statement/table rather than theoretical certainty. Sampling criteria, analytical choices, gradient tendencies, unresolved cases and accidental-gap interpretations are separately qualified in the records.

## High-value extraction / reconciliation decisions

### Direct Samoan structure and prosody

Alderete & Bradshaw's direct root-phonotactics study now provides a source-specific structural layer rather than relying only on earlier synopsis/secondary records. The ordinary template is `(C)V1(V2)`, with no codas and no complex onsets. Their adopted diphthong set `/ei eu ai au ou oi ui/` is not encoded as theory-neutral fact: the records preserve their warning that identical vowels and some special environments complicate the tautosyllabic/heterosyllabic division. Primary stress is final with a bimoraic final nucleus and otherwise penultimate, while special morpheme-boundary patterns such as `/fe+ita/ -> feíta` are stored as a separate prosodic-domain fact.

The same batch preserves register and lexical-stratum effects. `/k r h/` are loan/marginal in `tautala lelei`; colloquial `tautala leaga` neutralizes literary contrasts through `t~k -> k`, `n~ŋ -> ŋ`, and loan `r~l -> l`. The paper's four-mora maximum is explicitly tagged as a canonical-root/corpus-screening criterion, not an established categorical grammatical maximum.

Quantitative syllable/segment evidence is retained rather than reduced to binary restrictions. Medial syllables in tri- and quadrisyllabic roots are overwhelmingly short (`CV=295`, `CVV=3`, `V=69`, `VV=0`). Bilabial `/p,m/` strongly prefer root-initial position, whereas `/n,l,ŋ/` prefer non-initial position. The clearest CV near-gap is `/v/` before back vowels (`vo=2`, `vu=0`), explicitly represented as nearly categorical rather than absolute.

### Vowel co-occurrence

The full V-V layer records the O/E structure that is lost in a simple harmony label. Identical non-low vowels are strongly overrepresented (`ii=1.97`, `ee=2.26`, `oo=1.87`, `uu=1.82`), while several similar but non-identical pairs are underrepresented (`ie=.49`, `ei=.62`, `ou=.48`, `uo=.25`). `/a/` is comparatively neutral. Order effects are retained, including the asymmetry between `/u-o/=.25` and `/o-u/=.48` and between `/i-e/=.49` and `/e-i/=.62` in the all-root matrix.

For disyllabic roots the global independence test is stored exactly (`χ²=179.84`, `df=16`, `p<.001`) but is not misread as evidence that every matrix cell is individually significant. The source's significant associations (`e-e`, `i-i`, `o-o`, `u-u`) and dissociations (`e-o`, `i-e`, `i-u`, `u-o`) are separate from its broader gradient-similarity proposal. The close match between disyllabic and all-root matrices is stored as a robustness qualification.

### Consonant co-occurrence and counterexamples

Homorganic non-identical consonants are generally underrepresented, but the run preserves why a simple categorical OCP-PLACE statement is inadequate. Labials are strongly order-sensitive: in all roots `/m-p/=.52` and `/m-f/=.77`, while reverse `/p-m/` and `/f-m/` have O/E `0`. Much of this asymmetry is explicitly reconciled with independent positional preferences, rather than counted twice as unrelated restrictions.

Coronal co-occurrence is strongly manner-sensitive: same-sonorancy coronal pairs are more restricted than mixed-sonorancy pairs. Table 17 aggregate counts are retained (`27` non-identical labial homorganic tokens but only `6` same-sonorancy; `159` coronal homorganic tokens but only `10` same-sonorancy). The overall labial restriction is stronger than the coronal restriction.

Sample-sensitive and unexplained cells remain first-class records. `/n...v/` has O/E `0` in disyllables but `1.73` in all roots and is explicitly left unexplained by the authors. `/m...v/` was checked against both tables during this run: the disyllabic zero is potentially accidental, and the all-root sample has O/E `.27`. `/ŋ...m/` remains unattested in the all-root data while `/ŋ...n/` changes from `.33` in disyllables to `1.02` in all roots. `/ŋ...ʔ/` and `/ʔ...ŋ/` are underrepresented and are preserved with the authors' historical Proto-Polynesian homorganicity explanation rather than forced into a purely synchronic place label.

## Validation / repository integrity

- GitHub round-trip reads succeeded for all three new JSONL batches after the correction. The intended UTF-8/IPA data, record ordering, parent/dependency links and corrected `/m...v/` values are retrievable from the shard branch.
- GitHub comparison from baseline `cf3a57be804e5b01c649ad35c0c6ae4b71585dac` to corrected empirical head `de06b76c9b308826e5e8bcfaa486adc4bebea724` reports **4 commits ahead, 0 behind**.
- The comparison reports exactly three added staging files with **11 + 8 + 11 = 30 additions/atomic records**. No pre-existing file, shared curated table, or denominator is modified/deleted in the net diff.
- The fourth commit is a correction within newly created batch49 and does not change the 30-record increment.
- Parent/dependency links explicitly tie syllable/nucleus analyses to stress, positional segment biases to apparent consonant-order effects, and cell-level exceptions to the general co-occurrence records.
- Existing read-only validators/auditors were not rewritten merely to create tool churn. This connector runtime still does not expose an executable mounted clone, so GitHub round-trip/compare validation is reported instead of falsely claiming a local whole-shard Python run.

## Source-access notes

- The main source was the directly accessible PDF of Alderete & Bradshaw, *Samoan Root Phonotactics: Digging Deeper into the Data* (Linguistic Discovery 11.1). Relevant tables/pages were read directly, including the syllable/consonant-frequency tables, CV table, V-V matrices, C-C matrices, and Table 17 aggregate comparison.
- Direct ANU access to the relevant *Handbook of Australian Languages* volume for Crowley's Yaygir chapter timed out in this pass. No pseudo-primary Yaygir records were generated from inaccessible pages.
- Previously staged Samoan synopsis/model records were left untouched. The direct 2013 records have distinct source IDs/dedup keys so later reconciliation can distinguish direct corpus evidence, a descriptive synopsis, and learned/model-derived constraints.

## High-yield next queue

1. **Samoan direct reconciliation:** mine the remaining Alderete & Bradshaw model/constraint sections and any accessible supplemental root tables; reconcile direct O/E evidence against Kuo and Zuraw–Yu–Orfitelli without replacing gradient observations with categorical constraints.
2. **Mosel & Hovdhaugen Samoan:** obtain direct grammar pages for register, vowel sequence, stress, reduction and prosodic-word domains currently represented via later summaries.
3. **Yaygir:** retry Crowley through alternate ANU/archival access; target §§2.2/2.3.1 and preserve underlying `/d/` versus surface initial `[l]` neutralization.
4. **Gumbaynggir:** obtain direct Eades 1979 pp. 264–269 and reconcile the existing secondary-source cluster inventory cell by cell, especially one-root laminal-nasal exceptions and unusual labial-velar patterns.
5. **Tongan:** direct JIPA/phonetics article for `(C)V`, stress/definitive accent, quantity, and loan-conditioned deletion/length, avoiding duplicates with the already staged loan batch.
6. **Jewish Arabic of Gabes:** remaining emphasis/assimilation distributions, guttural conditioning, cross-word variability and marginal vowel strata.
7. **Campidanese/Sestu Sardinian:** full fortition-lenition table reconciliation with stress-conditioned deletion, rhotic metathesis and lexical triggers.
8. **Kalmyk/Oirat:** direct spoken positional distributions and exceptions, preserving traditional phonemic-length versus modern stress-based analyses as competing descriptions.
9. **Wargamay:** empirical support/violation mapping for the already staged 57 Hayes-Wilson weighted constraints if a usable Dixon-derived lexicon becomes available.
10. **Validation:** when an executable clone/mount is available, run JSON parse, record/dedup uniqueness, parent/dependency resolution, staging summary, conflict audit and weighted-constraint audit over the full shard.
