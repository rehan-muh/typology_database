# PHONOTACTICS / DISTRIBUTION shard — 2026-08-24 checkpoint

## Scope
Continuation from `agent/phonotactics-worker-20260823-1754` only. No shared curated denominator or canonical table was edited.

## New staged batches

| batch | source focus | atomic records | confidence |
|---|---|---:|---|
| `2026-08-24_samoan_batch04.jsonl` | Kuo 2023 dissertation + Kuo 2024 Journal of Phonetics: Samoan/Proto-Polynesian | 12 | 12 high |
| `2026-08-24_smith_initial_position_batch05.jsonl` | Smith 2002 positional augmentation: Sestu/Iglesias + cross-language initial-position summaries | 11 | 4 high, 7 medium |
| `2026-08-24_hayes_wilson_shona_wargamay_batch06.jsonl` | Hayes & Wilson 2008: Shona vowel harmony + Wargamay edge phonotactics | 9 | 9 high |
| **new this run** |  | **32** | **25 high, 7 medium** |

Prior checkpoint contained 38 atomic staged records, so the shard now contains **70 atomic staged records across six batch files**.

## New empirical coverage

### Samoan / Proto-Polynesian
- `(C)V(V)` template; optional onset; no codas or consonant clusters.
- Noncontrastive stress: final long vowel, otherwise penultimate; suffix-size-conditioned shifts.
- Hiatus vs diphthong nucleus analysis and explicit disagreement over diphthong inventory.
- Initial /ʔ/ instability/elision in non-careful speech.
- /k r h/ loan/interjection stratum; /r/ frequently [l].
- `tautala leaga` register mergers /t,k/→/k/, /n,ŋ/→/ŋ/, /r,l/→/l/.
- Gradient OCP-place effects, with significant OCP-LAB, OCP-COR-SON, and OCP-BACK but non-significant general OCP-place and several refinements.
- Explicit accidental-gap treatment of unattested /ŋ...m/ and /ŋ...v/.
- Parallel Proto-Polynesian OCP effects and cross-morpheme reanalysis evidence.
- Acoustic similarity qualification: coronal spectral distance vs phonotactic Harmony R²=.74; weaker labial correlation due ceiling-like Harmony range.

### Smith positional-initial systems
- Sestu Campidanian: initial true-onset /j w r/ restriction, medial licensing, initial /l/ licensing, single initial-[w] loan exception `whisky`, no CGV/rising diphthongs, and rapid-speech-transcription qualification.
- Iglesias Campidanian contrast: initial-liquid restriction with surface initial glides analyzed as nuclear onglides; CGV allowed.
- Secondary-summary candidates for Mongolian, Kuman, Guugu Yimidhirr, Pitta-Pitta, Mbabaram, and Bakairi. These are deliberately marked medium confidence and require direct descriptive-source verification before canonical promotion.

### Shona / Wargamay
- Shona nonlocal vowel-height harmony in the verb domain, including quantified lexical exceptions.
- Explicit weak-trigger gradient: o...i=23 (O/E .13), o...u=20 (O/E .07), versus e...i=2 (O/E .01).
- Wargamay: no initial vowels, no VV, no initial/final consonant clusters; initial /r,l/ ban; restricted final-sonorant set.
- Wargamay frequency qualification: final /m/ and /r/ are grammatical but exceptionally rare, which causes model overpenalization.
- Wargamay loan-stratum exceptions retained explicitly instead of weakening native phonotactics.

## Validation and safeguards
- `batch04` + `batch05`: local schema/JSONL validation completed successfully for **23/23 records, 0 errors** using the shard validator schema.
- `batch06`: GitHub contents round-trip succeeded and the complete JSONL was re-fetched after commit; all nine records retain required provenance/confidence/dependency fields.
- A full six-file validator pass was attempted from the execution container but the container had no DNS access to `raw.githubusercontent.com`; this is an environment transport limitation, not a detected data error.
- No claims were promoted to canonical/shared tables.
- Secondary-source summaries are explicitly downgraded where direct grammar verification remains pending.

## Reusable tooling added
`tools/phonotactics_distribution/reconcile_constraints.py`
- canonicalizes Unicode/whitespace/common arrow notation;
- detects exact dedup-key collisions;
- groups same-lect + same-normalized-environment + same-restriction-type candidates for source-level reconciliation;
- reports only; never mutates staging data.

## Checkpoints created this run
- `dd7a9b0589717bb28294a036fd7d16dbc97c72b8` — Samoan / Proto-Polynesian batch 04
- `1ba9fe5943a04ef6a049e4f042f05346486feb91` — Smith initial-position batch 05
- `8c34e02687c1af6aa4f11c5aa666752bee4a0fd8` — Hayes & Wilson Shona/Wargamay batch 06
- `2c06431db3d5de0afc736b218b8d52f915e55cab` — conservative reconciliation tool

## High-yield next queue
1. **Wargamay continuation (Hayes & Wilson §8.3–8.5):** medial cluster inventory/restrictions, vowel/quantity conditions, stress pattern, explicit overfit/accidental-gap cases.
2. **Direct-source verification for Smith summary candidates:** Bolognesi 1998 (Sestu/Iglesias), Wetzels & Mascaró 2001 (Bakairi), and the original Mongolian/Kuman/Guugu Yimidhirr/Pitta-Pitta/Mbabaram descriptions cited by Smith.
3. **Shona specialist source triangulation:** Fortune 1955 + Beckman 1997, especially morphological-domain boundaries, root-initial privilege, suffix harmony, and exception strata.
4. **Samoan direct grammar triangulation:** Mosel & Hovdhaugen 1992 and Zuraw et al. 2014 for register, initial /ʔ/, diphthongs, stress and suffix-size conditioning.
5. **Existing grammar queue from taxonomy catalog:** target grammars with explicit phonotactics/syllable/stress chapters, prioritizing tables and sections with cluster inventories, harmony domains, positional neutralization, and loan strata.
