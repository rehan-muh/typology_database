from __future__ import annotations

import io
import zipfile
from pathlib import Path
import pandas as pd
import requests

SOURCE_ID = "schertz_adil_kravchuk_2023"
DATA_URL = "https://osf.io/download/rbxmq/"


def _read_zip_tables(raw: bytes) -> dict[str, pd.DataFrame]:
    wanted = {
        "macro_production.txt",
        "micro_production.txt",
        "macro_perception.txt",
        "micro_perception.txt",
        "sub_info.txt",
    }
    out = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        for name in wanted:
            out[name] = pd.read_csv(io.BytesIO(zf.read(name)), sep="\t")
    return out


def _prefix_source_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={c: f"source_{c}" for c in df.columns})


def build(output_dir: str | Path) -> None:
    out = Path(output_dir)
    faithful = out / "source_faithful"
    linked = out / "linked"
    faithful.mkdir(parents=True, exist_ok=True)
    linked.mkdir(parents=True, exist_ok=True)

    r = requests.get(DATA_URL, timeout=180)
    r.raise_for_status()
    tables = _read_zip_tables(r.content)

    # Immutable/source-faithful parse: original column names and values are retained.
    for name, df in tables.items():
        df.to_csv(faithful / name.replace(".txt", ".csv"), index=False)

    info = tables["sub_info.txt"].copy()
    speakers = pd.DataFrame({
        "source_id": SOURCE_ID,
        "speaker_id": SOURCE_ID + "::" + info["sub"].astype(str),
        "source_speaker_id": info["sub"].astype(str),
        "experimental_group": info.get("group"),
        "birth_year": info.get("dob.year"),
        "gender_source": info.get("gender"),
        "residence_country_source": info.get("current_residence_country"),
        "english_l1_source": info.get("engL1"),
        "other_l1_source": info.get("otherL1"),
        "l2_source": info.get("L2"),
    })
    speakers.to_csv(linked / "speakers.csv", index=False)

    token_frames = []
    measurement_frames = []
    for table_name in ("macro_production.txt", "micro_production.txt"):
        df = tables[table_name].copy().reset_index(drop=True)
        layer = "macro" if table_name.startswith("macro") else "micro"
        token_id = [f"{SOURCE_ID}::{layer}::{i+1}" for i in range(len(df))]

        base = pd.DataFrame({
            "source_id": SOURCE_ID,
            "token_id": token_id,
            "speaker_id": SOURCE_ID + "::" + df["sub"].astype(str),
            "source_speaker_id": df["sub"].astype(str),
            "source_table": table_name,
            "target_segment_source": df["seg"].astype(str) if "seg" in df else pd.NA,
            "word_source": df["word"].astype(str) if "word" in df else pd.NA,
            "sentence_source": df["sen"].astype(str) if "sen" in df else pd.NA,
            "session_source": df["session"] if "session" in df else pd.NA,
            "repetition_source": df["rep"] if "rep" in df else pd.NA,
            "trial_source": df["trial"] if "trial" in df else pd.NA,
            "experimental_group_source": df["group"] if "group" in df else pd.NA,
        })
        # Retain all original production variables alongside the harmonized keys.
        source = _prefix_source_columns(df)
        base = pd.concat([base, source], axis=1)
        token_frames.append(base)

        measure_specs = []
        if "vot" in df:
            # Do not silently standardize units: macro and micro source tables use visibly
            # different numeric scales. Unit remains source-specific until code/docs confirm it.
            measure_specs.append(("vot", "VOT_RAW", "source_table_scale"))
        if "vDur" in df:
            measure_specs.append(("vDur", "VOWEL_DURATION", "s"))
        if "f0.mean" in df:
            measure_specs.append(("f0.mean", "F0_MEAN", "Hz"))
        if "f0.st" in df:
            measure_specs.append(("f0.st", "F0_SEMITONE_SOURCE", "semitone_source"))
        if "f0.norm" in df:
            measure_specs.append(("f0.norm", "F0_NORMALIZED_SOURCE", "source_normalized"))

        for source_var, measure, unit in measure_specs:
            m = pd.DataFrame({
                "source_id": SOURCE_ID,
                "token_id": token_id,
                "speaker_id": SOURCE_ID + "::" + df["sub"].astype(str),
                "source_table": table_name,
                "measure": measure,
                "value_raw": df[source_var],
                "unit": unit,
                "source_variable": source_var,
                "measurement_provenance": "author-released derived measurement; manual acoustic landmarks documented in Schertz et al. (2023)",
            })
            measurement_frames.append(m)

    tokens = pd.concat(token_frames, ignore_index=True)
    measurements = pd.concat(measurement_frames, ignore_index=True)
    tokens.to_csv(linked / "production_tokens.csv", index=False)
    measurements.to_csv(linked / "measurements_long.csv", index=False)

    # Perception data are retained because they can serve as individual-difference covariates,
    # but they are explicitly separated from production outcomes.
    perception = []
    for table_name in ("macro_perception.txt", "micro_perception.txt"):
        df = tables[table_name].copy().reset_index(drop=True)
        layer = "macro" if table_name.startswith("macro") else "micro"
        x = _prefix_source_columns(df)
        x.insert(0, "source_table", table_name)
        x.insert(0, "response_id", [f"{SOURCE_ID}::{layer}_perception::{i+1}" for i in range(len(df))])
        x.insert(0, "speaker_id", SOURCE_ID + "::" + df["sub"].astype(str))
        x.insert(0, "source_id", SOURCE_ID)
        perception.append(x)
    pd.concat(perception, ignore_index=True, sort=False).to_csv(linked / "perception_covariates.csv", index=False)

    # Integrity checks.
    assert speakers["speaker_id"].is_unique
    assert tokens["token_id"].is_unique
    assert set(tokens["speaker_id"]).issubset(set(speakers["speaker_id"]))
    assert set(measurements["token_id"]).issubset(set(tokens["token_id"]))

    summary = pd.DataFrame([
        {"table": "speakers", "rows": len(speakers)},
        {"table": "production_tokens", "rows": len(tokens)},
        {"table": "measurements_long", "rows": len(measurements)},
        {"table": "perception_covariates", "rows": sum(len(tables[x]) for x in ("macro_perception.txt", "micro_perception.txt"))},
    ])
    summary.to_csv(out / "ingestion_summary.csv", index=False)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="schertz_warehouse")
    args = p.parse_args()
    build(args.output)
