#!/usr/bin/env python3
"""Convert PAVOQUE's manually corrected YAML phone segmentation to canonical tables.

Input: one or more pavoque-*.yaml files from marytts/pavoque-data.
Output directory receives coarticulation_tokens.csv and coarticulation_events.csv.
No acoustic trajectories are invented; those remain REEXTRACT from the licensed audio.

PAVOQUE labels are SAMPA. A conservative documented SAMPA->IPA map is applied only
for labels whose interpretation is unambiguous in the corpus conventions. Unknown
labels remain blank in *_segment_ipa and are reported to stderr; source labels are
retained in source_annotation_id. Silence/boundary labels are retained for timing but
are not emitted as target tokens.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml

SOURCE_ID = "pavoque"
DATASET_ID = "pavoque_expressive_speech"
SPEAKER_SOURCE_ID = "Stefan_Roettig"
SPEAKER_UID = f"{SOURCE_ID}::{SPEAKER_SOURCE_ID}"
LANGUAGE = "German"
GLOTTOCODE = "stan1295"
SOURCE_URL = "https://github.com/marytts/pavoque-data"
SOURCE_LICENSE = "CC-BY-NC-SA-4.0"
ANNOTATION_PROVENANCE = "AUTO_THEN_ALL_CORRECTED"
MANUAL_SCOPE = "phonetic segments manually corrected; segment end times relative to utterance start"

# PAVOQUE README states labels are SAMPA. This map is intentionally conservative.
SAMPA_TO_IPA = {
    "a": "a", "a:": "aː", "e:": "eː", "E": "ɛ", "E:": "ɛː",
    "i:": "iː", "I": "ɪ", "o:": "oː", "O": "ɔ", "u:": "uː", "U": "ʊ",
    "y:": "yː", "Y": "ʏ", "2:": "øː", "9": "œ", "@": "ə", "6": "ɐ",
    "aI": "aɪ", "aU": "aʊ", "OY": "ɔʏ",
    "p": "p", "b": "b", "t": "t", "d": "d", "k": "k", "g": "ɡ",
    "?": "ʔ", "f": "f", "v": "v", "s": "s", "z": "z", "S": "ʃ",
    "Z": "ʒ", "C": "ç", "x": "x", "h": "h", "m": "m", "n": "n",
    "N": "ŋ", "l": "l", "R": "ʁ", "j": "j", "ts": "ts", "pf": "pf",
}
BOUNDARY_LABELS = {"_", "H#", "#"}

TOKEN_FIELDS = [
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
EVENT_FIELDS = [
    "source_id","dataset_id","speaker_uid","token_id","event_id","event_type",
    "event_time_s","event_start_s","event_end_s","annotation_provenance","manual_scope",
    "measurement_origin","manual_verification","source_event_name","source_annotation_id",
    "source_url","quality_flag"
]


def ipa(label: str) -> str:
    return SAMPA_TO_IPA.get(label, "")


def empty_row(fields):
    return {k: "" for k in fields}


def parse_yaml(path: Path):
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    style_from_name = path.stem.removeprefix("pavoque-")
    for utt in data:
        segs = utt.get("segments") or []
        if not segs:
            continue
        utterance_start = float(utt.get("start", 0.0))
        style = utt.get("style") or style_from_name
        recording_id = f"pavoque-{style}"
        utterance_id = str(utt.get("prompt", ""))
        local_prev = 0.0
        parsed = []
        for idx, seg in enumerate(segs):
            label = str(seg.get("lab", ""))
            local_end = float(seg["end"])
            local_start = local_prev
            local_prev = local_end
            parsed.append({
                "idx": idx,
                "label": label,
                "ipa": ipa(label),
                "start": utterance_start + local_start,
                "end": utterance_start + local_end,
            })
        yield recording_id, utterance_id, style, parsed


def nearest_phone(parsed, i, step):
    j = i + step
    while 0 <= j < len(parsed):
        if parsed[j]["label"] not in BOUNDARY_LABELS:
            return parsed[j]
        j += step
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("--outdir", required=True, type=Path)
    ap.add_argument("--retrieved-at", default="")
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    tokens, events, unmapped = [], [], set()
    for path in args.inputs:
        for recording_id, utterance_id, style, parsed in parse_yaml(path):
            for i, seg in enumerate(parsed):
                if seg["label"] in BOUNDARY_LABELS:
                    continue
                if not seg["ipa"]:
                    unmapped.add(seg["label"])
                prev = nearest_phone(parsed, i, -1)
                nxt = nearest_phone(parsed, i, +1)
                token_id = f"{recording_id}::{utterance_id}::seg{seg['idx']:05d}"
                r = empty_row(TOKEN_FIELDS)
                r.update({
                    "source_id": SOURCE_ID,
                    "dataset_id": DATASET_ID,
                    "speaker_uid": SPEAKER_UID,
                    "speaker_source_id": SPEAKER_SOURCE_ID,
                    "language": LANGUAGE,
                    "glottocode": GLOTTOCODE,
                    "variety": "Standard German; expressive read/acted speech",
                    "recording_id": recording_id,
                    "utterance_id": utterance_id,
                    "token_id": token_id,
                    "task": "acted/read expressive speech",
                    "style": style,
                    "speaker_sex_gender": "male",
                    "target_segment_ipa": seg["ipa"],
                    "target_start_s": f"{seg['start']:.6f}",
                    "target_end_s": f"{seg['end']:.6f}",
                    "target_duration_ms": f"{(seg['end']-seg['start'])*1000:.6f}",
                    "prev_segment_ipa": prev["ipa"] if prev else "",
                    "prev_start_s": f"{prev['start']:.6f}" if prev else "",
                    "prev_end_s": f"{prev['end']:.6f}" if prev else "",
                    "next_segment_ipa": nxt["ipa"] if nxt else "",
                    "next_start_s": f"{nxt['start']:.6f}" if nxt else "",
                    "next_end_s": f"{nxt['end']:.6f}" if nxt else "",
                    "annotation_provenance": ANNOTATION_PROVENANCE,
                    "manual_scope": MANUAL_SCOPE,
                    "source_annotation_id": f"{path.name}:{utterance_id}:{seg['idx']}:{seg['label']}",
                    "audio_uri": f"{recording_id}.flac",
                    "source_url": SOURCE_URL,
                    "source_license": SOURCE_LICENSE,
                    "retrieved_at": args.retrieved_at,
                    "quality_flag": "OK" if seg["ipa"] else "UNMAPPED_SOURCE_PHONE",
                })
                tokens.append(r)
                for kind, t in (("SEGMENT_ONSET", seg["start"]), ("SEGMENT_OFFSET", seg["end"])):
                    e = empty_row(EVENT_FIELDS)
                    e.update({
                        "source_id": SOURCE_ID,
                        "dataset_id": DATASET_ID,
                        "speaker_uid": SPEAKER_UID,
                        "token_id": token_id,
                        "event_id": f"{token_id}::{kind}",
                        "event_type": kind,
                        "event_time_s": f"{t:.6f}",
                        "annotation_provenance": ANNOTATION_PROVENANCE,
                        "manual_scope": MANUAL_SCOPE,
                        "measurement_origin": "ORIGINAL",
                        "manual_verification": "YES",
                        "source_event_name": "segment_start_derived_from_previous_end" if kind == "SEGMENT_ONSET" else "segment_end",
                        "source_annotation_id": r["source_annotation_id"],
                        "source_url": SOURCE_URL,
                        "quality_flag": r["quality_flag"],
                    })
                    events.append(e)

    for name, fields, rows in [
        ("coarticulation_tokens.csv", TOKEN_FIELDS, tokens),
        ("coarticulation_events.csv", EVENT_FIELDS, events),
    ]:
        with (args.outdir / name).open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader(); w.writerows(rows)

    print(f"wrote {len(tokens)} tokens and {len(events)} events to {args.outdir}")
    if unmapped:
        print("unmapped SAMPA labels (IPA left blank): " + ", ".join(sorted(unmapped)), file=sys.stderr)


if __name__ == "__main__":
    main()
