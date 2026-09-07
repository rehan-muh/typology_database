#!/usr/bin/env python3
"""Materialize the VoxAngeles manually audited layer without duplicating inherited UCLA audio.

Downloads the six public phonetic-measurement TSVs from pacscilab/voxangeles,
preserves source-faithful copies, profiles every variable, and produces linked
long-form duration/F0/formant tables with namespaced IDs. Decile and quartile
representations are lineage-linked rather than counted as independent tokens.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
import pandas as pd
import requests

SOURCE_ID = "voxangeles_manual_layer_2024"
BASE = "https://raw.githubusercontent.com/pacscilab/voxangeles/main/data/phonetic_measurements"
FILES = [
    "voxangeles_durations.tsv",
    "voxangeles_f0_deciles.tsv",
    "voxangeles_f0_quartiles.tsv",
    "voxangeles_formants_deciles.tsv",
    "voxangeles_formants_quartiles.tsv",
    "voxangeles_meanf0_file.tsv",
]

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def main() -> None:
    root = Path(__file__).resolve().parents[1]
    raw = root / "data" / "warehouse" / "source_faithful" / SOURCE_ID
    out = root / "data" / "warehouse" / "harmonized" / SOURCE_ID
    raw.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    tables = {}
    inventory = []
    vardict = []
    for fn in FILES:
        p = raw / fn
        if not p.exists():
            r = requests.get(f"{BASE}/{fn}", timeout=120)
            r.raise_for_status()
            p.write_bytes(r.content)
        df = pd.read_csv(p, sep="\t", dtype_backend="numpy_nullable")
        tables[fn] = df
        inventory.append({"source_id": SOURCE_ID, "file": fn, "rows": len(df), "columns": len(df.columns), "sha256": sha256(p), "bytes": p.stat().st_size})
        for c in df.columns:
            s = df[c]
            vardict.append({"source_id": SOURCE_ID, "file_table": fn, "original_variable": c, "datatype": str(s.dtype), "nonmissing_n": int(s.notna().sum()), "unique_n": int(s.nunique(dropna=True))})
    pd.DataFrame(inventory).to_csv(out / "table_inventory.csv", index=False)
    pd.DataFrame(vardict).to_csv(out / "variable_profile.csv", index=False)

    d = tables["voxangeles_durations.tsv"].copy()
    d["recording_id"] = SOURCE_ID + "::" + d["file"].astype(str)
    d["token_id"] = d["recording_id"] + "::phone::" + d["int"].astype(str)
    d["phone_duration_s"] = pd.to_numeric(d["pend"], errors="coerce") - pd.to_numeric(d["pstart"], errors="coerce")
    d["word_duration_s"] = pd.to_numeric(d["wend"], errors="coerce") - pd.to_numeric(d["wstart"], errors="coerce")
    d.to_csv(out / "segment_tokens.csv", index=False)

    trajectory_frames = []
    for fn, measure, prefix, n in [
        ("voxangeles_f0_deciles.tsv", "f0", "f0_", 10),
        ("voxangeles_formants_deciles.tsv", "f1", "f1_", 10),
        ("voxangeles_formants_deciles.tsv", "f2", "f2_", 10),
        ("voxangeles_formants_deciles.tsv", "f3", "f3_", 10),
        ("voxangeles_f0_quartiles.tsv", "f0", "f0_", 4),
        ("voxangeles_formants_quartiles.tsv", "f1", "f1_", 4),
        ("voxangeles_formants_quartiles.tsv", "f2", "f2_", 4),
        ("voxangeles_formants_quartiles.tsv", "f3", "f3_", 4),
    ]:
        df = tables[fn].copy()
        id_cols = [c for c in ["lang","file","word","phone","prec","foll","int","pstart","pend","wstart","wend"] if c in df.columns]
        val_cols = [f"{prefix}{i}" for i in range(1, n + 1) if f"{prefix}{i}" in df.columns]
        long = df.melt(id_vars=id_cols, value_vars=val_cols, var_name="source_time_variable", value_name="value_raw")
        long["sampling_grid"] = "deciles" if n == 10 else "quartiles"
        long["sample_index"] = long["source_time_variable"].str.extract(r"(\d+)$").astype("Int64")
        long["normalized_time"] = long["sample_index"] / n
        long["measure"] = measure
        long["units"] = "Hz"
        long["recording_id"] = SOURCE_ID + "::" + long["file"].astype(str)
        long["token_id"] = long["recording_id"] + "::phone::" + long["int"].astype(str)
        trajectory_frames.append(long)
    pd.concat(trajectory_frames, ignore_index=True).to_csv(out / "acoustic_trajectories.csv", index=False)

if __name__ == "__main__":
    main()
