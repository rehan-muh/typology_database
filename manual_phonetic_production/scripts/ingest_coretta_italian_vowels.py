#!/usr/bin/env python3
"""Ingest the public Coretta Northwestern Italian vowel-production package.

This converter preserves source-faithful CSVs, then emits linked token,
landmark/temporal, acoustic, and long trajectory tables. It deliberately does
not infer IPA and does not double-count the package's overlapping formants.rda
object. Source: https://github.com/stefanocoretta/coretta2018itaegg (CC-BY-4.0).
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import shutil
import urllib.request
import pandas as pd

SOURCE_ID = "coretta_italian_vowel_2018_2026"
BASE = "https://raw.githubusercontent.com/stefanocoretta/coretta2018itaegg/main/data-raw/datasets"
FILES = ["measurements.csv", "stimuli.csv", "formants-ids.csv", "words.csv"]
WINDOWS = {1: (0.0, 0.2, 0.1), 2: (0.2, 0.4, 0.3), 3: (0.4, 0.6, 0.5), 4: (0.6, 0.8, 0.7), 5: (0.8, 1.0, 0.9)}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def get(url: str, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as r, dst.open("wb") as w:
        shutil.copyfileobj(r, w)


def namespaced(kind: str, value) -> str:
    return f"{SOURCE_ID}::{kind}::{value}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    root = args.root
    raw_dir = root / "data" / "warehouse" / "source_faithful" / SOURCE_ID
    out_dir = root / "data" / "warehouse" / "harmonized" / SOURCE_ID
    raw_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for fn in FILES:
        p = raw_dir / fn
        if not p.exists():
            get(f"{BASE}/{fn}", p)
        manifest.append({"source_id": SOURCE_ID, "file": fn, "bytes": p.stat().st_size, "sha256": sha256(p)})
    pd.DataFrame(manifest).to_csv(out_dir / "file_manifest_runtime.csv", index=False)

    m = pd.read_csv(raw_dir / "measurements.csv", na_values=["--undefined--"])
    s = pd.read_csv(raw_dir / "stimuli.csv")
    fid = pd.read_csv(raw_dir / "formants-ids.csv")
    words = pd.read_csv(raw_dir / "words.csv")

    # Preserve all source variables before harmonization. Do not overwrite raw files.
    # The source R pipeline uses a full join with stimuli; merge on shared columns only.
    shared = [c for c in s.columns if c in m.columns]
    if shared:
        merged = m.merge(s, how="outer", on=shared, suffixes=("", "_stimuli"))
    else:
        merged = m.copy()

    # Namespace speakers and create stable row-level token IDs without assuming a
    # linguistic segmentation beyond source-supplied landmarks.
    if "speaker" not in merged.columns:
        raise ValueError("Expected source variable 'speaker' not found")
    merged["speaker_id"] = merged["speaker"].map(lambda x: namespaced("speaker", x))
    merged["token_id"] = [namespaced("token", i + 1) for i in range(len(merged))]

    token_cols = [c for c in [
        "token_id", "speaker_id", "speaker", "ipu", "stimulus", "stimulus_id",
        "sentence", "word", "c1", "vowel", "c2", "backness", "height",
        "c1_place", "c2_place", "file"
    ] if c in merged.columns]
    merged[token_cols].to_csv(out_dir / "tokens.csv", index=False)

    landmark_cols = [c for c in [
        "token_id", "sentence_ons", "sentence_off", "word_ons", "word_off",
        "v1_ons", "c2_ons", "v2_ons", "voice_ons", "voice_off", "c1_rel", "c2_rel"
    ] if c in merged.columns]
    merged[landmark_cols].to_csv(out_dir / "landmarks_wide.csv", index=False)

    # Reproduce source-derived durations from source landmarks as separate fields.
    temp = merged[["token_id"]].copy()
    formulas = {
        "v1_duration_ms": ("c2_ons", "v1_ons", 1000.0),
        "c2_closure_duration_ms": ("c2_rel", "c2_ons", 1000.0),
        "c1_release_to_v1_offset_ms": ("c2_ons", "c1_rel", 1000.0),
        "sentence_duration_s": ("sentence_off", "sentence_ons", 1.0),
        "voicing_duration_ms": ("voice_off", "voice_ons", 1000.0),
        "vot_ms": ("voice_ons", "c1_rel", 1000.0),
        "c2_closure_voicing_ms": ("voice_off", "c2_ons", 1000.0),
        "c1_to_c2_release_ms": ("c2_rel", "c1_rel", 1000.0),
    }
    for out, (a, b, scale) in formulas.items():
        if a in merged and b in merged:
            temp[out] = (merged[a] - merged[b]) * scale
    if "sentence_duration_s" in temp:
        temp["speech_rate_syll_s"] = 8.0 / temp["sentence_duration_s"]
    temp.to_csv(out_dir / "temporal_measurements.csv", index=False)

    # Preserve any already-supplied acoustic/duration values independently.
    supplied = [c for c in ["fo", "cutoff", "v1_duration", "c2_clos_duration", "rel_voff",
                             "sent_duration", "speech_rate", "speech_rate_c", "voice_duration",
                             "vot", "voi_clo", "rel_rel"] if c in merged.columns]
    merged[["token_id"] + supplied].to_csv(out_dir / "source_derived_measures.csv", index=False)

    # Long-form F1/F2/F3 trajectories. Original 20%-wide windows are retained;
    # normalized_time is the derived window center and never replaces window bounds.
    rows = []
    for i, r in merged.iterrows():
        tid = r["token_id"]
        for tp, (lo, hi, center) in WINDOWS.items():
            for formant in (1, 2, 3):
                col = f"f{formant}{tp}"
                if col not in merged.columns:
                    continue
                rows.append({
                    "source_id": SOURCE_ID,
                    "token_id": tid,
                    "measure": f"F{formant}",
                    "value_hz": r[col],
                    "source_variable": col,
                    "source_window_start_norm": lo,
                    "source_window_end_norm": hi,
                    "normalized_time": center,
                    "normalized_time_provenance": "DERIVED_WINDOW_CENTER",
                })
    traj = pd.DataFrame(rows)
    traj.to_csv(out_dir / "formant_trajectories_long.csv", index=False)

    # Source-file linkage tables are preserved rather than merged destructively.
    fid.to_csv(out_dir / "formant_id_linkage_source.csv", index=False)
    words.to_csv(out_dir / "words_source.csv", index=False)

    # Minimal integrity checks.
    assert merged["token_id"].is_unique
    assert merged["speaker_id"].notna().all()
    assert set(traj["measure"].dropna().unique()).issubset({"F1", "F2", "F3"})
    assert traj["normalized_time"].dropna().between(0, 1).all()
    if not traj.empty:
        assert set(traj["token_id"]).issubset(set(merged["token_id"]))

    print({
        "source_id": SOURCE_ID,
        "source_measurement_rows": len(m),
        "harmonized_token_rows": len(merged),
        "trajectory_rows": len(traj),
        "speakers": merged["speaker"].nunique(dropna=True),
        "source_files": len(FILES),
    })


if __name__ == "__main__":
    main()
