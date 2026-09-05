#!/usr/bin/env python3
"""Validate canonical coarticulation tables.

Usage:
    python scripts/validate_coarticulation.py data/coarticulation/derived

The directory may contain any of:
    coarticulation_tokens.csv
    coarticulation_trajectories.csv
    coarticulation_events.csv

Validation is deliberately strict about IDs, provenance, canonical measures/events,
and referential integrity. Missing files are reported but are not errors because a
source may support only a subset of the ten analyses.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

CANONICAL_MEASURES = {
    "F0_HZ", "F0_ST", "F1_HZ", "F2_HZ", "F3_HZ", "H1H2_DB", "H2H4_DB",
    "CPP_DB", "A1P0_DB", "A1P1_DB", "NASALANCE", "RMS_DB", "COG_HZ",
    "SPECTRAL_SLOPE_DB_OCT", "SPECTRAL_SKEWNESS", "SPECTRAL_KURTOSIS",
    "BURST_PEAK_HZ",
}
CANONICAL_EVENTS = {
    "SEGMENT_ONSET", "SEGMENT_OFFSET", "CLOSURE_ONSET", "CLOSURE_OFFSET",
    "BURST", "VOICING_ONSET", "FRICATION_ONSET", "FRICATION_OFFSET",
    "ASPIRATION_ONSET", "ASPIRATION_OFFSET", "NASAL_ONSET", "NASAL_OFFSET",
}
PROVENANCE = {
    "MANUAL_FROM_SCRATCH", "AUTO_THEN_ALL_CORRECTED", "AUTO_THEN_ALL_VERIFIED",
    "MANUAL_MEASUREMENT_ONLY", "MANUAL",
}

TOKEN_REQUIRED = {
    "source_id", "dataset_id", "speaker_uid", "speaker_source_id", "language",
    "glottocode", "recording_id", "utterance_id", "token_id", "target_segment_ipa",
    "target_start_s", "target_end_s", "target_duration_ms", "annotation_provenance",
    "manual_scope", "source_url", "quality_flag",
}
TRAJ_REQUIRED = {
    "source_id", "dataset_id", "speaker_uid", "token_id", "measure", "time_norm",
    "value", "unit", "measurement_origin", "manual_verification", "quality_flag",
}
EVENT_REQUIRED = {
    "source_id", "dataset_id", "speaker_uid", "token_id", "event_id", "event_type",
    "annotation_provenance", "manual_scope", "measurement_origin",
    "manual_verification", "quality_flag",
}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return list(r), set(r.fieldnames or [])


def blank(x):
    return x is None or str(x).strip() == ""


def as_float(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def require_columns(path, fields, required, errors):
    miss = sorted(required - fields)
    if miss:
        errors.append(f"{path.name}: missing columns: {', '.join(miss)}")


def validate_tokens(path, errors, warnings):
    rows, fields = read_csv(path)
    require_columns(path, fields, TOKEN_REQUIRED, errors)
    ids = set()
    for i, r in enumerate(rows, start=2):
        tid = (r.get("source_id", ""), r.get("token_id", ""))
        if blank(tid[0]) or blank(tid[1]):
            errors.append(f"{path.name}:{i}: blank source_id/token_id")
        elif tid in ids:
            errors.append(f"{path.name}:{i}: duplicate source_id+token_id {tid}")
        ids.add(tid)
        uid = r.get("speaker_uid", "")
        src = r.get("source_id", "")
        if src and uid and not uid.startswith(src + "::"):
            errors.append(f"{path.name}:{i}: speaker_uid must be namespaced as source_id::speaker")
        s = as_float(r.get("target_start_s"))
        e = as_float(r.get("target_end_s"))
        d = as_float(r.get("target_duration_ms"))
        if s is not None and e is not None:
            if e <= s:
                errors.append(f"{path.name}:{i}: target_end_s must exceed target_start_s")
            if d is not None and abs(d - (e - s) * 1000) > max(2.0, 0.02 * d):
                warnings.append(f"{path.name}:{i}: target_duration_ms disagrees with boundaries")
        prov = r.get("annotation_provenance", "")
        if prov and prov not in PROVENANCE:
            warnings.append(f"{path.name}:{i}: non-canonical provenance label {prov}")
    return ids


def validate_trajectories(path, token_ids, errors, warnings):
    rows, fields = read_csv(path)
    require_columns(path, fields, TRAJ_REQUIRED, errors)
    seen = set()
    for i, r in enumerate(rows, start=2):
        key = (r.get("source_id", ""), r.get("token_id", ""))
        if token_ids is not None and key not in token_ids:
            errors.append(f"{path.name}:{i}: trajectory references unknown token {key}")
        m = r.get("measure", "")
        if m not in CANONICAL_MEASURES:
            errors.append(f"{path.name}:{i}: non-canonical measure {m}")
        t = as_float(r.get("time_norm"))
        if t is None or not 0 <= t <= 1:
            errors.append(f"{path.name}:{i}: time_norm must be numeric in [0,1]")
        if as_float(r.get("value")) is None:
            errors.append(f"{path.name}:{i}: value must be finite numeric")
        dedup = (key, m, r.get("time_norm", ""))
        if dedup in seen:
            warnings.append(f"{path.name}:{i}: duplicate token+measure+time point {dedup}")
        seen.add(dedup)


def validate_events(path, token_ids, errors, warnings):
    rows, fields = read_csv(path)
    require_columns(path, fields, EVENT_REQUIRED, errors)
    event_ids = set()
    for i, r in enumerate(rows, start=2):
        key = (r.get("source_id", ""), r.get("token_id", ""))
        if token_ids is not None and key not in token_ids:
            errors.append(f"{path.name}:{i}: event references unknown token {key}")
        eid = (r.get("source_id", ""), r.get("event_id", ""))
        if eid in event_ids:
            errors.append(f"{path.name}:{i}: duplicate source_id+event_id {eid}")
        event_ids.add(eid)
        et = r.get("event_type", "")
        if et not in CANONICAL_EVENTS:
            errors.append(f"{path.name}:{i}: non-canonical event_type {et}")
        point = as_float(r.get("event_time_s"))
        start = as_float(r.get("event_start_s"))
        end = as_float(r.get("event_end_s"))
        if point is None and (start is None or end is None):
            errors.append(f"{path.name}:{i}: supply event_time_s or both interval boundaries")
        if start is not None and end is not None and end <= start:
            errors.append(f"{path.name}:{i}: event_end_s must exceed event_start_s")


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/coarticulation/derived")
    errors, warnings = [], []
    token_path = root / "coarticulation_tokens.csv"
    traj_path = root / "coarticulation_trajectories.csv"
    event_path = root / "coarticulation_events.csv"

    token_ids = None
    if token_path.exists():
        token_ids = validate_tokens(token_path, errors, warnings)
    else:
        warnings.append(f"missing optional file: {token_path}")
    if traj_path.exists():
        validate_trajectories(traj_path, token_ids, errors, warnings)
    else:
        warnings.append(f"missing optional file: {traj_path}")
    if event_path.exists():
        validate_events(event_path, token_ids, errors, warnings)
    else:
        warnings.append(f"missing optional file: {event_path}")

    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        raise SystemExit(1)
    print(f"OK: {len(warnings)} warning(s)")


if __name__ == "__main__":
    main()
