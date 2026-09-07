#!/usr/bin/env python3
"""Materialize the VoxAngeles manually audited layer without duplicating inherited UCLA audio.

Downloads the six public phonetic-measurement TSVs from pacscilab/voxangeles,
preserves source-faithful copies, profiles every original variable, and produces
linked duration/F0/formant tables with namespaced IDs.

IMPORTANT lineage rule: decile and quartile trajectory files are alternate
representations of the same vowel tokens. Deciles are the canonical trajectory
representation; quartiles are retained in a separate alternate table and MUST
NOT be row-counted as independent phonetic observations.
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
GIT_BLOBS = {
    "voxangeles_durations.tsv": "312cc96927ad4e2a1d79957499e82d9a5cf0340c",
    "voxangeles_f0_deciles.tsv": "2d20c3de967ca03c80dfe78d22e29fb1383148c9",
    "voxangeles_f0_quartiles.tsv": "afccf9eb747835743cd59607576361bed556b3d2",
    "voxangeles_formants_deciles.tsv": "e0d8e6de5a5a85c3d1b45fc8c2d8bad8716597c6",
    "voxangeles_formants_quartiles.tsv": "216ee5c99310ac5bfa0fd744370cb0f3912b20f7",
    "voxangeles_meanf0_file.tsv": "9492dd2ed35044219aed483613fd3f7a44f292d3",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def namespaced_token_id(df: pd.DataFrame) -> pd.Series:
    """Stable token ID: source + recording + audited interval index."""
    if "file" not in df or "int" not in df:
        raise ValueError("VoxAngeles token tables must contain file and int")
    return SOURCE_ID + "::" + df["file"].astype(str) + "::phone::" + df["int"].astype(str)


def trajectory_long(df: pd.DataFrame, measure: str, prefix: str, n: int, grid: str) -> pd.DataFrame:
    id_cols = [c for c in ["lang", "file", "word", "phone", "prec", "foll", "int", "pstart", "pend", "wstart", "wend"] if c in df.columns]
    val_cols = [f"{prefix}{i}" for i in range(1, n + 1) if f"{prefix}{i}" in df.columns]
    if not val_cols:
        raise ValueError(f"No {prefix} trajectory columns found for {grid}")
    long = df.melt(id_vars=id_cols, value_vars=val_cols,
                   var_name="source_time_variable", value_name="value_raw")
    long["sampling_grid"] = grid
    long["sample_index"] = long["source_time_variable"].str.extract(r"(\d+)$")[0].astype("Int64")
    # Source sampling is equally spaced across the audited vowel interval.
    # normalized_time is derived; source_time_variable is always retained.
    long["normalized_time"] = long["sample_index"] / n
    long["measure"] = measure
    long["units"] = "Hz"
    long["recording_id"] = SOURCE_ID + "::" + long["file"].astype(str)
    long["token_id"] = namespaced_token_id(long)
    long["lineage_id"] = long["token_id"] + "::" + measure
    long["representation_role"] = "canonical" if grid == "deciles" else "alternate_overlapping"
    return long


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    raw = root / "data" / "warehouse" / "source_faithful" / SOURCE_ID
    out = root / "data" / "warehouse" / "harmonized" / SOURCE_ID
    raw.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)

    tables: dict[str, pd.DataFrame] = {}
    inventory: list[dict] = []
    vardict: list[dict] = []

    for fn in FILES:
        p = raw / fn
        if not p.exists():
            r = requests.get(f"{BASE}/{fn}", timeout=120)
            r.raise_for_status()
            p.write_bytes(r.content)
        df = pd.read_csv(p, sep="\t", dtype_backend="numpy_nullable", keep_default_na=False)
        tables[fn] = df
        inventory.append({
            "source_id": SOURCE_ID,
            "file": fn,
            "source_url": f"{BASE}/{fn}",
            "upstream_git_blob": GIT_BLOBS[fn],
            "rows": len(df),
            "columns": len(df.columns),
            "sha256": sha256(p),
            "bytes": p.stat().st_size,
            "processed": True,
            "source_faithful_preserved": True,
        })
        for c in df.columns:
            s = df[c]
            vardict.append({
                "source_id": SOURCE_ID,
                "file_table": fn,
                "original_variable": c,
                "standardized_variable": "",
                "variable_domain": "source_specific_unmapped",
                "description_meaning": "Retained source variable; semantic mapping handled separately where defensible.",
                "units": "",
                "datatype": str(s.dtype),
                "coding_levels": "" if s.nunique(dropna=False) > 50 else " | ".join(map(str, pd.unique(s)[:50])),
                "missing_value_conventions": "Source literals preserved; no silent recoding in source-faithful layer.",
                "measurement_annotation_method": "VoxAngeles audited/manual layer or derived public measurement table; see source provenance.",
                "time_reference_window": "",
                "anatomical_acoustic_target": "",
                "provenance": f"{fn}; git_blob={GIT_BLOBS[fn]}",
                "notes": f"nonmissing_n={int(s.notna().sum())}; unique_n={int(s.nunique(dropna=False))}",
            })

    pd.DataFrame(inventory).to_csv(out / "table_inventory.csv", index=False)
    pd.DataFrame(vardict).to_csv(out / "variable_profile.csv", index=False)

    # Audited segment timing/context table.
    d = tables["voxangeles_durations.tsv"].copy()
    required = {"file", "int", "pstart", "pend", "wstart", "wend", "phone"}
    missing = required - set(d.columns)
    if missing:
        raise ValueError(f"Duration table missing required columns: {sorted(missing)}")
    d["recording_id"] = SOURCE_ID + "::" + d["file"].astype(str)
    d["token_id"] = namespaced_token_id(d)
    if d["token_id"].duplicated().any():
        raise ValueError("Duplicate namespaced VoxAngeles segment token IDs")
    for c in ["pstart", "pend", "wstart", "wend"]:
        d[c + "_numeric"] = pd.to_numeric(d[c], errors="coerce")
    d["phone_duration_s"] = d["pend_numeric"] - d["pstart_numeric"]
    d["word_duration_s"] = d["wend_numeric"] - d["wstart_numeric"]
    if (d["phone_duration_s"].dropna() < 0).any() or (d["word_duration_s"].dropna() < 0).any():
        raise ValueError("Negative duration detected")
    d.to_csv(out / "segment_tokens.csv", index=False)

    # Canonical decile trajectory representation.
    canonical = [
        trajectory_long(tables["voxangeles_f0_deciles.tsv"], "f0", "f0_", 10, "deciles"),
        trajectory_long(tables["voxangeles_formants_deciles.tsv"], "f1", "f1_", 10, "deciles"),
        trajectory_long(tables["voxangeles_formants_deciles.tsv"], "f2", "f2_", 10, "deciles"),
        trajectory_long(tables["voxangeles_formants_deciles.tsv"], "f3", "f3_", 10, "deciles"),
    ]
    canonical_df = pd.concat(canonical, ignore_index=True)
    canonical_df.to_csv(out / "acoustic_trajectories.csv", index=False)

    # Preserve quartiles, but isolate them from canonical/analysis row counting.
    alternate = [
        trajectory_long(tables["voxangeles_f0_quartiles.tsv"], "f0", "f0_", 4, "quartiles"),
        trajectory_long(tables["voxangeles_formants_quartiles.tsv"], "f1", "f1_", 4, "quartiles"),
        trajectory_long(tables["voxangeles_formants_quartiles.tsv"], "f2", "f2_", 4, "quartiles"),
        trajectory_long(tables["voxangeles_formants_quartiles.tsv"], "f3", "f3_", 4, "quartiles"),
    ]
    alternate_df = pd.concat(alternate, ignore_index=True)
    alternate_df.to_csv(out / "acoustic_trajectories_alternate_quartiles.csv", index=False)

    # Explicit lineage summary for future warehouse builders.
    lineage = pd.DataFrame([
        {"source_id": SOURCE_ID, "lineage_group": "vowel_f0", "canonical_file": "voxangeles_f0_deciles.tsv", "alternate_file": "voxangeles_f0_quartiles.tsv", "dedup_rule": "same underlying audited vowel tokens; count canonical deciles only"},
        {"source_id": SOURCE_ID, "lineage_group": "vowel_formants", "canonical_file": "voxangeles_formants_deciles.tsv", "alternate_file": "voxangeles_formants_quartiles.tsv", "dedup_rule": "same underlying audited vowel tokens; count canonical deciles only"},
    ])
    lineage.to_csv(out / "trajectory_lineage.csv", index=False)

    validation = pd.DataFrame([{
        "source_id": SOURCE_ID,
        "segment_rows": len(d),
        "canonical_trajectory_rows": len(canonical_df),
        "alternate_quartile_rows": len(alternate_df),
        "unique_segment_token_ids": int(d["token_id"].nunique()),
        "negative_phone_durations": int((d["phone_duration_s"].dropna() < 0).sum()),
        "negative_word_durations": int((d["word_duration_s"].dropna() < 0).sum()),
        "canonical_only_for_row_counting": True,
    }])
    validation.to_csv(out / "validation_summary.csv", index=False)


if __name__ == "__main__":
    main()
