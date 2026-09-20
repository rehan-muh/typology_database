# Ingestion/discovery audit — 2026-09-20 16:10 -07:00

## Backlog ingestion completed

### PAVOQUE angry style: spike0006–spike0008

Authoritative upstream: `marytts/pavoque-data/pavoque-angry.yaml` (blob SHA recorded in rows: `bff79d978f740f6c2b09bc595ade03b6bdf33423`). The corpus documentation describes the phonetic segments as manually corrected. Only this human-verified segment layer is admitted.

Created `data/harmonized/pavoque_angry_spike0006_0008_segments_2026-09-20_1610.csv` with 58 segment rows: spike0006 = 33, spike0007 = 18, spike0008 = 7. Every row preserves prompt, original German text, style, utterance start/end, original SAMPA-like label, supplied relative segment endpoint, reconstructed relative start from the immediately preceding endpoint, and absolute start/end obtained by adding the utterance start. No IPA mapping or unsupplied linguistic context was invented. Final segment endpoints (3.835, 2.995, 1.915 s) remain source-faithful rather than being forced to equal nominal utterance duration.

Integrity checks: segment indices are contiguous within each prompt; relative endpoints are strictly increasing; reconstructed starts equal the preceding endpoint; absolute times equal utterance start plus relative times; all 58 IDs are namespaced `pavoque::...`; no duplicate prompt/segment-index pairs occur in this batch.

Next exact PAVOQUE cursor: `spike0009` in the same upstream YAML.

## Fresh discovery / screening

Searches covered Zenodo, OSF, and GitHub-oriented queries for manually annotated/corrected production speech, TextGrids, formants, VOT, and speech corpora.

* `PodcastFillers` (Zenodo 7121457): 85,803 manually annotated events, but the underlying audio is a third-party SoundCloud podcast collection. **EXCLUDE under the explicit third-party-media rule**, despite useful filler/breath/laughter labels.
* `Code-Switching Speech Corpus` (Zenodo 4434251): resegments a subset of the pre-existing German Spoken Wikipedia Corpus. The surfaced record says SWC recordings were already manually annotated at word/segment level; no independently established new manual phonetic annotation layer was found in this pass. **REVIEW/likely exclude as secondary reuse** until a genuinely new isolatable human annotation layer is demonstrated.
* `MRPL2` (Zenodo 20365865): reconfirmed as high-value manual non-native production corpus (4,500 utterances, 23 speakers, 14 L1s) but files remain restricted. **Do not ingest inaccessible observations.**
* Singing datasets surfaced in GitHub searches (ACV series) were rejected immediately under the non-singing rule.

No discovery candidate was promoted solely from keyword evidence.

## Provenance / lineage / license discipline

No raw audio was committed. PAVOQUE rows point to the authoritative upstream annotation object and immutable blob SHA. The batch is observation-level, not merely a registry entry. No automatic-only labels were admitted.

## Backlog priorities

1. Continue PAVOQUE from spike0009, preserving every manually corrected segment.
2. Parse Tibetan diphthong F1/F2 trajectories without midpoint reduction.
3. Enumerate and ingest TaL manual segmentation/transcription CSVs while linking rather than copying bulk media.
4. Continue JSUT manual symbol coverage from BASIC5000_1371.
5. Resume Marathi / Chenghai / CCOST / Russian Fricatives accepted backlogs.
6. Resolve public observation-level availability for the 1,043 manually bounded Spanish validation vowels.
