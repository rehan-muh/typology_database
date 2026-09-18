# Ingestion + discovery audit — 2026-09-18 08:10 -0700

## Backlog ingestion

### AutoVOT tutorial manual VOT
- Continued the already accepted, narrowly isolated manual VOT layer.
- Directly opened upstream `experiments/data/tutorialExample/test/voiceless/cas7D_1054_27_3.TextGrid` (blob `1328cfae3e2842b806d922e73a972150e8bd5191`).
- Ingested exactly one new manual VOT interval: 0.7200010000000001–0.85 s, duration 0.1299989999999999 s / 129.9989999999999 ms.
- Context supplied by the same TextGrid: phone `P`, word `PATCH`.
- Provenance safeguard retained: AutoVOT documentation establishes manual VOT labels; phone/word tiers are contextual only and are not asserted to be manual.
- Raw WAV not copied.
- Namespaced recording ID: `autovot_tutorial_manual_vot::cas7D_1054_27_3`.

## Discovery pass

### Karl Eberhards Corpus (KEC) — review / potentially isolatable manual word layer
Public University of Tübingen documentation describes 40 spontaneous southern-German dialogues, including articulography for 20 speakers. It states that word boundaries are manually corrected but segment boundaries are automatically aligned; annotations are Praat format. This makes the manually corrected word-boundary layer potentially admissible if it can be isolated file/tier-wise, while automatic segment tiers must remain excluded. Primary recordings appear to have been collected for the corpus. Priority: resolve repository package/license, enumerate TextGrids, identify exact word tier and correction provenance, and ingest only the qualifying manual layer plus primary articulatory trajectories if their provenance satisfies the inclusion rule.

### IFCASL — remains review
Revalidated that the corpus contains about 100 speakers and word/phone segmentation with >50% manually corrected data. This still does not justify admitting the entire segmentation layer because the publicly surfaced description does not identify which individual observations were manually corrected. Priority remains finding an identifier-level correction flag or an isolatable fully human-verified subset.

### L2-ARCTIC — high-priority backlog
Revalidated official documentation: 26,867 utterances / 24 speakers overall; human annotators manually examined 3,599 utterances and marked 14,098 substitutions, 3,420 deletions, and 1,092 additions. Corpus-wide forced alignment remains excluded. Priority: obtain the official annotation package and ingest the 3,599 manually examined utterances only, retaining error labels and corrected phone information source-faithfully.

### HAMATAC — review
Primary L2 German map-task recordings from 24 adults. Repository documentation exposes manual disfluency annotation and orthographic transcription, but the latest additional POS/lemma layer is manually corrected linguistic annotation rather than necessarily phonetic segmentation. Keep in review pending file-level inspection for admissible temporal/manual production annotations.

### Exclusion reconfirmed: AdoVoc Pro
Singing/flamenco vocal-resource dataset. Excluded categorically under the non-singing rule despite manual temporal annotations.

## Integrity / continuation
- No unrelated repository paths modified.
- No automatic phone boundaries admitted as manual observations.
- No IPA, speaker metadata, units, or annotation method invented beyond explicit upstream evidence.
- New observation rows this run: 1.
- Next AutoVOT continuation: enumerate remaining tutorial test/train TextGrids not already represented, prioritizing direct source verification and deduplication against earlier `bin/test_data_in` lineage.
- Discovery priorities: KEC tier-level isolation; L2-ARCTIC manual package; IFCASL correction flags; public primary articulatory datasets with manual landmarks/intervals.
