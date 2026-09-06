#!/usr/bin/env python3
"""Convert the released Cohn & Zellou (2023) vowel table to canonical F1/F2 tables.

Input is the OSF file `utterance_nasality_formant_measurements.csv`, harvested by
`audit_open_data.py`. Only F1/F2 are emitted as target acoustic outcomes. A1-P0,
F0, duration, and other source measurements remain available only as metadata and
are not emitted as target trajectories.

The paper documents seven time-normalized vowel windows, with endpoints 0 and 1
omitted for formant analysis. Retained windows are 14.3–28.6%, 28.6–42.9%,
42.9–57.2%, 57.2–71.5%, and 71.5–85.8%. Canonical `time_norm` uses each documented
window midpoint; source window start/end are retained explicitly.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
import numpy as np
import pandas as pd

SOURCE_ID = "cohn_zellou_2023_clear_speech"
DATASET_ID = SOURCE_ID
SOURCE_URL = "https://osf.io/n3fzj/"
TIME_START = np.array([0.143, 0.286, 0.429, 0.572, 0.715])
TIME_END = np.array([0.286, 0.429, 0.572, 0.715, 0.858])
TIME_MID = (TIME_START + TIME_END) / 2


def clean_id(x):
    if pd.isna(x):
        return ""
    s = str(x)
    return s[:-2] if s.endswith(".0") else s


def convert(input_csv: Path, outdir: Path):
    d = pd.read_csv(input_csv, low_memory=False)
    fcols = [f"target_word_vowel_F{f}_time{i}" for f in (1, 2) for i in range(2, 7)]
    required = {"Participant", "Filename", "Utterance", "target_word_vowel", "target_word_vowel_duration", *fcols}
    missing = sorted(required - set(d.columns))
    if missing:
        raise ValueError("Missing expected source columns: " + ", ".join(missing))

    keep = d["Participant"].notna() & d["target_word_vowel"].notna() & d[fcols].notna().any(axis=1)
    d = d.loc[keep].reset_index(drop=True)
    outdir.mkdir(parents=True, exist_ok=True)

    tokens = []
    trajectories = []
    for i, r in d.iterrows():
        source_speaker = clean_id(r["Participant"])
        speaker_uid = f"{SOURCE_ID}::{source_speaker}"
        token_id = f"{SOURCE_ID}::token_{i + 1:05d}"
        dur_ms = ""
        if pd.notna(r.get("target_word_vowel_duration")):
            dur_ms = float(r["target_word_vowel_duration"]) * 1000.0

        # The released analysis table does not provide absolute target-vowel
        # boundaries or canonical IPA for every token. Do not reconstruct either
        # from orthography. Preserve the source's own vowel/context labels instead.
        tokens.append({
            "source_id": SOURCE_ID,
            "dataset_id": DATASET_ID,
            "speaker_uid": speaker_uid,
            "speaker_source_id": source_speaker,
            "language": "California English",
            "glottocode": "stan1293",
            "recording_id": r.get("Filename", ""),
            "utterance_id": r.get("Utterance", ""),
            "token_id": token_id,
            "prev_segment_ipa": "",
            "target_segment_ipa": "",
            "next_segment_ipa": "",
            "prev_start_s": "",
            "prev_end_s": "",
            "target_start_s": "",
            "target_end_s": "",
            "next_start_s": "",
            "next_end_s": "",
            "target_duration_ms": dur_ms,
            "annotation_provenance": "AUTO_THEN_ALL_CORRECTED",
            "manual_scope": "all analyzed target-vowel boundaries hand-corrected after MFA; productions reviewed by trained RAs",
            "source_url": SOURCE_URL,
            "quality_flag": "PASS",
            "source_target_word": r.get("TargetWord", ""),
            "source_vowel_label": r.get("target_word_vowel", ""),
            "source_structure": r.get("Structure", ""),
            "source_prev_sound_label": r.get("target_word_vowel_previous_sound", ""),
            "source_next_sound_label": r.get("target_word_vowel_next_sound", ""),
            "style": r.get("Style", ""),
            "repetition": r.get("Repetition", ""),
            "age": r.get("Age", ""),
            "gender": r.get("Gender", ""),
            "l1": r.get("L1", ""),
        })

        for j, tp in enumerate(range(2, 7)):
            for formant in (1, 2):
                source_col = f"target_word_vowel_F{formant}_time{tp}"
                value = pd.to_numeric(pd.Series([r[source_col]]), errors="coerce").iloc[0]
                if pd.isna(value) or not np.isfinite(float(value)):
                    continue
                trajectories.append({
                    "source_id": SOURCE_ID,
                    "dataset_id": DATASET_ID,
                    "speaker_uid": speaker_uid,
                    "token_id": token_id,
                    "measure": f"F{formant}_HZ",
                    "time_norm": round(float(TIME_MID[j]), 4),
                    "time_s": "",
                    "value": float(value),
                    "unit": "Hz",
                    "measurement_origin": "ORIGINAL",
                    "algorithm": "Fast Track / Praat",
                    "settings_json": "{}",
                    "manual_verification": "TARGET_VOWEL_BOUNDARY_HAND_CORRECTED;FORMANT_AUTOMATIC",
                    "quality_flag": "PASS",
                    "source_measure_name": source_col,
                    "source_time_window_start": TIME_START[j],
                    "source_time_window_end": TIME_END[j],
                })

    tok = pd.DataFrame(tokens)
    traj = pd.DataFrame(trajectories)
    tok.to_csv(outdir / "coarticulation_tokens.csv", index=False)
    traj.to_csv(outdir / "coarticulation_trajectories.csv", index=False)
    return tok, traj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_csv", type=Path)
    ap.add_argument("outdir", type=Path)
    ap.add_argument("--validator", type=Path, default=Path(__file__).with_name("validate_coarticulation.py"))
    args = ap.parse_args()
    tok, traj = convert(args.input_csv, args.outdir)
    print(f"Wrote {len(tok)} tokens, {len(traj)} F1/F2 trajectory rows, {tok.speaker_uid.nunique()} speakers")
    if args.validator.exists():
        subprocess.run([sys.executable, str(args.validator), str(args.outdir)], check=True)


if __name__ == "__main__":
    main()
