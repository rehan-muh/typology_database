from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
from pathlib import Path

import requests
import yaml

SOURCE_ID = "pavoque_expressive_german"
BASE = "https://raw.githubusercontent.com/marytts/pavoque-data/master/"
FILES = [
    ("angry", "pavoque-angry.yaml", "bff79d978f740f6c2b09bc595ade03b6bdf33423", "core"),
    ("happy", "pavoque-happy.yaml", "9ed4b66625a6c6df746730b6bf45ae35b9baaa38", "core"),
    ("neutral", "pavoque-neutral.yaml", "29deb5aa1b75b1aaa98d51896f9d849e12bc7bc0", "core"),
    ("poker", "pavoque-poker.yaml", "20a8bdc3cee75f3e19517dfeeda1a2230cb033c9", "core"),
    ("sad", "pavoque-sad.yaml", "199a4dde1e3a50576a1a691664473aa9f35f41ed", "core"),
    ("outtakes", "pavoque-outtakes.yaml", "a72da519c13068f8c05b6fd038cd8ecac540b80c", "outtake"),
]

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "warehouse" / "pavoque"
OUT.mkdir(parents=True, exist_ok=True)


def get_text(url: str) -> str:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    return r.text


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


utterances = []
segments = []
manifest = []
raw_variable_names = set()

for declared_style, fn, blob_sha, scope in FILES:
    url = BASE + fn
    text = get_text(url)
    sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    data = yaml.safe_load(text)
    if not isinstance(data, list):
        raise ValueError(f"Unexpected top-level YAML object in {fn}: {type(data)}")

    file_utt = 0
    file_seg = 0
    for ui, utt in enumerate(data, start=1):
        if not isinstance(utt, dict):
            raise ValueError(f"Unexpected utterance object in {fn} at {ui}")
        raw_variable_names.update(utt.keys())
        prompt = utt.get("prompt")
        uid = f"{SOURCE_ID}::{fn}::{prompt if prompt is not None else ui}"
        ustart = float(utt.get("start")) if utt.get("start") is not None else None
        uend = float(utt.get("end")) if utt.get("end") is not None else None
        style_original = utt.get("style")
        segs = utt.get("segments") or []
        utterances.append({
            "source_id": SOURCE_ID,
            "utterance_id": uid,
            "source_file": fn,
            "source_scope": scope,
            "utterance_index_source_file": ui,
            "prompt_original": prompt,
            "text_original": utt.get("text"),
            "style_original": style_original,
            "style_file_label": declared_style,
            "utterance_start_s_original": ustart,
            "utterance_end_s_original": uend,
            "utterance_duration_s_derived": (uend - ustart) if ustart is not None and uend is not None else None,
            "segment_count": len(segs),
            "provenance_url": url,
            "upstream_git_blob_sha": blob_sha,
        })
        file_utt += 1

        prev_local_end = 0.0
        for si, seg in enumerate(segs, start=1):
            if not isinstance(seg, dict):
                raise ValueError(f"Unexpected segment object in {fn}/{ui}/{si}")
            raw_variable_names.update("segments." + k for k in seg.keys())
            lab = seg.get("lab")
            local_end = float(seg["end"])
            local_start = prev_local_end
            prev_lab = segs[si - 2].get("lab") if si > 1 else None
            next_lab = segs[si].get("lab") if si < len(segs) else None
            sid = f"{uid}::seg{si:04d}"
            segments.append({
                "source_id": SOURCE_ID,
                "segment_id": sid,
                "utterance_id": uid,
                "source_file": fn,
                "source_scope": scope,
                "segment_index_original": si,
                "segment_label_original": lab,
                "segment_end_s_local_original": local_end,
                "segment_start_s_local_derived": local_start,
                "segment_duration_s_derived": local_end - local_start,
                "segment_start_s_absolute_derived": (ustart + local_start) if ustart is not None else None,
                "segment_end_s_absolute_derived": (ustart + local_end) if ustart is not None else None,
                "preceding_segment_original": prev_lab,
                "following_segment_original": next_lab,
                "prompt_original": prompt,
                "text_original": utt.get("text"),
                "style_original": style_original,
                "style_file_label": declared_style,
                "provenance_url": url,
                "upstream_git_blob_sha": blob_sha,
            })
            prev_local_end = local_end
            file_seg += 1

    manifest.append({
        "source_id": SOURCE_ID,
        "file": fn,
        "scope": scope,
        "authoritative_url": url,
        "upstream_git_blob_sha": blob_sha,
        "retrieved_sha256": sha256,
        "bytes_utf8": len(text.encode("utf-8")),
        "utterances_parsed": file_utt,
        "segments_parsed": file_seg,
        "status": "parsed",
        "notes": "Source reference/checksum retained; raw audio not mirrored. Outtakes kept explicitly distinguishable from core styles.",
    })

write_csv(
    OUT / "utterances_source_faithful.csv",
    ["source_id", "utterance_id", "source_file", "source_scope", "utterance_index_source_file", "prompt_original", "text_original", "style_original", "style_file_label", "utterance_start_s_original", "utterance_end_s_original", "utterance_duration_s_derived", "segment_count", "provenance_url", "upstream_git_blob_sha"],
    utterances,
)
write_csv(
    OUT / "segments_source_faithful.csv",
    ["source_id", "segment_id", "utterance_id", "source_file", "source_scope", "segment_index_original", "segment_label_original", "segment_end_s_local_original", "segment_start_s_local_derived", "segment_duration_s_derived", "segment_start_s_absolute_derived", "segment_end_s_absolute_derived", "preceding_segment_original", "following_segment_original", "prompt_original", "text_original", "style_original", "style_file_label", "provenance_url", "upstream_git_blob_sha"],
    segments,
)
write_csv(
    OUT / "file_manifest.csv",
    ["source_id", "file", "scope", "authoritative_url", "upstream_git_blob_sha", "retrieved_sha256", "bytes_utf8", "utterances_parsed", "segments_parsed", "status", "notes"],
    manifest,
)

vd = [
    {"original_variable": "prompt", "standardized_variable": "source_utterance_label", "variable_domain": "recording_utterance", "description": "Original prompt identifier", "units": "", "datatype": "string", "coding_levels": "source values", "missing_value_conventions": "YAML null/absent", "measurement_annotation_method": "author-supplied annotation", "time_reference_window": "utterance", "anatomical_acoustic_target": "", "provenance": "PAVOQUE YAML", "notes": "preserved verbatim"},
    {"original_variable": "text", "standardized_variable": "orthographic_transcription_original", "variable_domain": "recording_utterance", "description": "Original German utterance text", "units": "", "datatype": "string", "coding_levels": "free text", "missing_value_conventions": "YAML null/absent", "measurement_annotation_method": "author-supplied annotation", "time_reference_window": "utterance", "anatomical_acoustic_target": "", "provenance": "PAVOQUE YAML", "notes": "No IPA invented from orthography"},
    {"original_variable": "style", "standardized_variable": "speaking_style", "variable_domain": "condition", "description": "Expressive speaking style", "units": "", "datatype": "string", "coding_levels": "angry;happy;neutral;poker;sad;source-specific outtake values", "missing_value_conventions": "YAML null/absent", "measurement_annotation_method": "elicitation condition label", "time_reference_window": "utterance", "anatomical_acoustic_target": "", "provenance": "PAVOQUE YAML", "notes": "file-derived style also retained separately"},
    {"original_variable": "start", "standardized_variable": "utterance_start_s", "variable_domain": "temporal", "description": "Utterance start in source recording", "units": "seconds", "datatype": "float", "coding_levels": "continuous", "missing_value_conventions": "YAML null/absent", "measurement_annotation_method": "author annotation", "time_reference_window": "recording timeline", "anatomical_acoustic_target": "utterance boundary", "provenance": "PAVOQUE YAML", "notes": "original value retained"},
    {"original_variable": "end", "standardized_variable": "utterance_end_s", "variable_domain": "temporal", "description": "Utterance end in source recording", "units": "seconds", "datatype": "float", "coding_levels": "continuous", "missing_value_conventions": "YAML null/absent", "measurement_annotation_method": "author annotation", "time_reference_window": "recording timeline", "anatomical_acoustic_target": "utterance boundary", "provenance": "PAVOQUE YAML", "notes": "original value retained"},
    {"original_variable": "segments.lab", "standardized_variable": "segment_label_original", "variable_domain": "segment_annotation", "description": "Original SAMPA-style phone/silence label", "units": "", "datatype": "string", "coding_levels": "source values", "missing_value_conventions": "YAML null/absent", "measurement_annotation_method": "manually corrected phone segmentation per corpus documentation", "time_reference_window": "segment", "anatomical_acoustic_target": "phone interval", "provenance": "PAVOQUE YAML", "notes": "No IPA normalization invented"},
    {"original_variable": "segments.end", "standardized_variable": "segment_end_s_local", "variable_domain": "temporal", "description": "Cumulative segment endpoint within utterance", "units": "seconds", "datatype": "float", "coding_levels": "continuous", "missing_value_conventions": "YAML null/absent", "measurement_annotation_method": "manually corrected phone segmentation per corpus documentation", "time_reference_window": "utterance-local timeline", "anatomical_acoustic_target": "phone boundary", "provenance": "PAVOQUE YAML", "notes": "segment starts/durations are derived separately; original endpoint retained"},
]
for r in vd:
    r = r
    r["source_id"] = SOURCE_ID
    r["file_table"] = "PAVOQUE YAML / parsed linked tables"
write_csv(
    OUT / "variable_dictionary.csv",
    ["source_id", "file_table", "original_variable", "standardized_variable", "variable_domain", "description", "units", "datatype", "coding_levels", "missing_value_conventions", "measurement_annotation_method", "time_reference_window", "anatomical_acoustic_target", "provenance", "notes"],
    vd,
)

summary = {
    "source_id": SOURCE_ID,
    "files_parsed": len(manifest),
    "core_files": sum(m["scope"] == "core" for m in manifest),
    "outtake_files": sum(m["scope"] == "outtake" for m in manifest),
    "utterance_rows": len(utterances),
    "segment_rows": len(segments),
    "core_utterance_rows": sum(u["source_scope"] == "core" for u in utterances),
    "core_segment_rows": sum(s["source_scope"] == "core" for s in segments),
    "variable_dictionary_rows": len(vd),
    "raw_variables_observed": sorted(raw_variable_names),
    "integrity": {
        "unique_utterance_ids": len({u["utterance_id"] for u in utterances}) == len(utterances),
        "unique_segment_ids": len({s["segment_id"] for s in segments}) == len(segments),
        "all_segment_utterance_ids_resolve": {s["utterance_id"] for s in segments}.issubset({u["utterance_id"] for u in utterances}),
        "nonnegative_segment_durations": all(float(s["segment_duration_s_derived"]) >= 0 for s in segments),
    },
}
(OUT / "ingestion_status.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2, ensure_ascii=False))

# The existing Actions workflow runs this script after pushes to this file. In CI,
# commit only generated PAVOQUE warehouse outputs back under the permitted subtree.
if os.getenv("GITHUB_ACTIONS") == "true":
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
    subprocess.run(["git", "add", str(OUT.relative_to(Path.cwd()))], check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if diff.returncode != 0:
        subprocess.run(["git", "commit", "-m", "Ingest PAVOQUE YAML annotations into warehouse"], check=True)
        subprocess.run(["git", "push"], check=True)
