# Ingestion/discovery audit — 2026-09-21 21:09 -0700

## Backlog ingestion
- Continued accepted PAVOQUE from the source-faithful angry YAML.
- Promoted `spike0006`: 1 utterance + 33 manually corrected segment/silence observations.
- Preserved original labels and relative endpoints; derived starts, durations, and absolute times are separate fields. `normalized_ipa` remains blank because no explicit mapping was applied.
- Source utterance: `Also, in welchem Zustand bist du heute?`, angry, 20.16–24.0 s.
- Final annotated endpoint is 3.835 s relative to utterance start, leaving the source's 5 ms terminal residual to the 3.84 s utterance end; retained without repair.
- Upstream authoritative file: https://github.com/marytts/pavoque-data/blob/master/pavoque-angry.yaml

## Discovery
Fresh repository/web sweep emphasized manually corrected/verified production annotations. Screened:
- HAMATAC: primary L2 German map-task speech; manual disfluency annotation and manually corrected POS/lemma layers. Potentially relevant production metadata, but no new phonetic interval/measurement layer established in this pass; do not admit to core on linguistic annotation alone.
- BulPhonC: utterance segmentation manually verified, but phoneme annotations automatic; exclude automatic phone layer under current criteria.
- L2-ARCTIC: known accepted/manual subset; fresh documentation confirms 3,599 manually examined utterances and corrected word/phone boundaries plus 14,098 substitutions, 3,420 deletions, 1,092 additions. No duplicate registry entry created.
- IFCASL: known review source; >50% manually corrected word/phone segmentation, but public-file separation of corrected vs automatic material remains unresolved.
- LibriSpeech keywords derivative: secondary LibriSpeech reuse with some manually corrected keyword segmentations; not admitted pending proof that the new manual correction layer is isolatable and useful without duplicating inherited recordings.
- MEG-MASC: perception/listening dataset, not production; exclude.

## Validation
- 34 new scientific rows: 1 utterance + 33 segment intervals.
- 2 new logical source-faithful tables.
- Segment endpoints monotone; all durations nonnegative; last endpoint 23.995 s absolute <= utterance end 24.0 s.
- All writes confined to `manual_phonetic_production/`.

## Next priorities
1. Continue PAVOQUE contiguous angry backlog at `spike0007` while reconciling previously promoted m-series records to avoid duplicates.
2. Decode RVD manually corrected NPY array coding/timebase from upstream code before counting frame observations.
3. Resolve IFCASL manual-vs-automatic file lineage.
4. Continue source discovery in JASA/JSLHR/JPhon/LabPhon/Phonetica/JIPA and repository deposits, prioritizing public token/trajectory tables over registry-only records.
