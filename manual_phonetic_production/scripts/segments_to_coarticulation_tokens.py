#!/usr/bin/env python3
"""Convert a harmonized segment table into canonical coarticulation target/context rows.

This converter does not infer IPA features. It preserves source IPA labels and creates
previous/target/next context from manually valid segment intervals. Feature enrichment
(place, manner, nasal, labial, rhotic, lateral, etc.) is a separate deterministic step.

Required input columns:
source_id,dataset_id,speaker_id,recording_id,utterance_id,language,glottocode,
segment_ipa,start_s,end_s,annotation_provenance,manual_scope

Optional columns are propagated where possible: variety, task, style, word_id,
source_annotation_id,source_url,source_license,retrieved_at.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED = {
    "source_id", "dataset_id", "speaker_id", "recording_id", "utterance_id",
    "language", "glottocode", "segment_ipa", "start_s", "end_s",
    "annotation_provenance", "manual_scope",
}

OUT_FIELDS = [
    "source_id","dataset_id","speaker_uid","speaker_source_id","speaker_l1_glottocode",
    "speaker_l2_glottocode","language","glottocode","variety","recording_id","utterance_id",
    "word_id","token_id","task","style","speech_rate_syll_s","speaker_age",
    "speaker_sex_gender","clinical_status","target_segment_ipa","target_class",
    "target_vowel_height","target_vowel_backness","target_rounding","target_stress",
    "target_start_s","target_end_s","target_duration_ms","prev_segment_ipa","prev_class",
    "prev_place","prev_manner","prev_laryngeal_class","prev_is_nasal",
    "prev_is_labial_or_rounded","prev_is_rhotic","prev_is_lateral","prev_start_s","prev_end_s",
    "next_segment_ipa","next_class","next_place","next_manner","next_laryngeal_class",
    "next_is_nasal","next_is_labial_or_rounded","next_is_rhotic","next_is_lateral",
    "next_start_s","next_end_s","syllable_position","word_position","annotation_provenance",
    "manual_scope","source_annotation_id","audio_uri","source_url","source_license",
    "retrieved_at","quality_flag"
]


def f(x):
    return float(x) if x not in (None, "") else None


def segment_class(seg: str) -> str:
    # Conservative: do not guess IPA class without a validated feature mapper.
    return ""


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: segments_to_coarticulation_tokens.py INPUT_SEGMENTS.csv OUTPUT_TOKENS.csv")
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    with src.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = set(reader.fieldnames or [])
        missing = sorted(REQUIRED - fields)
        if missing:
            raise SystemExit("missing required columns: " + ", ".join(missing))
        rows = list(reader)

    groups = defaultdict(list)
    for r in rows:
        groups[(r["source_id"], r["recording_id"], r["utterance_id"])].append(r)

    out = []
    for key, segs in groups.items():
        segs.sort(key=lambda r: (f(r.get("start_s")) if f(r.get("start_s")) is not None else float("inf"),
                                 f(r.get("end_s")) if f(r.get("end_s")) is not None else float("inf")))
        for i, r in enumerate(segs):
            prev = segs[i-1] if i > 0 else {}
            nxt = segs[i+1] if i + 1 < len(segs) else {}
            start, end = f(r.get("start_s")), f(r.get("end_s"))
            duration = (end - start) * 1000 if start is not None and end is not None else ""
            speaker = r.get("speaker_id", "")
            source_id = r.get("source_id", "")
            token_id = r.get("token_id") or f"{r.get('recording_id','')}::{r.get('utterance_id','')}::seg{i:05d}"
            row = {k: "" for k in OUT_FIELDS}
            row.update({
                "source_id": source_id,
                "dataset_id": r.get("dataset_id", ""),
                "speaker_uid": f"{source_id}::{speaker}",
                "speaker_source_id": speaker,
                "language": r.get("language", ""),
                "glottocode": r.get("glottocode", ""),
                "variety": r.get("variety", ""),
                "recording_id": r.get("recording_id", ""),
                "utterance_id": r.get("utterance_id", ""),
                "word_id": r.get("word_id", ""),
                "token_id": token_id,
                "task": r.get("task", ""),
                "style": r.get("style", ""),
                "target_segment_ipa": r.get("segment_ipa", ""),
                "target_class": segment_class(r.get("segment_ipa", "")),
                "target_start_s": r.get("start_s", ""),
                "target_end_s": r.get("end_s", ""),
                "target_duration_ms": f"{duration:.6f}" if isinstance(duration, float) else "",
                "prev_segment_ipa": prev.get("segment_ipa", ""),
                "prev_class": segment_class(prev.get("segment_ipa", "")),
                "prev_start_s": prev.get("start_s", ""),
                "prev_end_s": prev.get("end_s", ""),
                "next_segment_ipa": nxt.get("segment_ipa", ""),
                "next_class": segment_class(nxt.get("segment_ipa", "")),
                "next_start_s": nxt.get("start_s", ""),
                "next_end_s": nxt.get("end_s", ""),
                "annotation_provenance": r.get("annotation_provenance", ""),
                "manual_scope": r.get("manual_scope", ""),
                "source_annotation_id": r.get("source_annotation_id", ""),
                "audio_uri": r.get("audio_uri", ""),
                "source_url": r.get("source_url", ""),
                "source_license": r.get("source_license", ""),
                "retrieved_at": r.get("retrieved_at", ""),
                "quality_flag": r.get("quality_flag", "OK") or "OK",
            })
            out.append(row)

    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=OUT_FIELDS)
        writer.writeheader()
        writer.writerows(out)
    print(f"wrote {len(out)} target/context rows to {dst}")


if __name__ == "__main__":
    main()
