#!/usr/bin/env python3
"""Fail-closed validator for PHONOTACTICS/DISTRIBUTION shard JSONL staging files."""
from __future__ import annotations
import argparse, json, pathlib, sys

REQUIRED = {
    "record_id", "source_id", "lect", "time_scope", "domain", "claim",
    "source_forms", "formal_environment", "normalized_environment",
    "restriction_type", "scope", "exceptions_or_counterexamples",
    "publication_page", "section", "table_figure", "confidence",
    "parent_links", "dependency_links", "dedup_key",
}
CONFIDENCE = {"high", "medium", "low"}


def load(path: pathlib.Path):
    rows = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"{path}:{n}: invalid JSON: {e}") from e
        if not isinstance(row, dict):
            raise ValueError(f"{path}:{n}: row must be a JSON object")
        rows.append((path, n, row))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    ap.add_argument("--allow-external-links", action="store_true",
                    help="Allow parent/dependency IDs not present in the supplied file set")
    args = ap.parse_args()
    rows = []
    for p in args.files:
        if not p.exists():
            print(f"ERROR missing file: {p}", file=sys.stderr); return 2
        rows.extend(load(p))

    errors = []
    ids, dedups = {}, {}
    for p, n, r in rows:
        missing = sorted(REQUIRED - set(r))
        if missing:
            errors.append(f"{p}:{n}: missing keys {missing}")
        for key in ("record_id", "source_id", "lect", "domain", "claim", "publication_page", "section", "dedup_key"):
            if key in r and (not isinstance(r[key], str) or not r[key].strip()):
                errors.append(f"{p}:{n}: {key} must be a non-empty string")
        if r.get("confidence") not in CONFIDENCE:
            errors.append(f"{p}:{n}: invalid confidence={r.get('confidence')!r}")
        if not isinstance(r.get("source_forms"), dict):
            errors.append(f"{p}:{n}: source_forms must be an object")
        for key in ("parent_links", "dependency_links"):
            if not isinstance(r.get(key), list) or not all(isinstance(x, str) for x in r.get(key, [])):
                errors.append(f"{p}:{n}: {key} must be a list of record IDs")
        rid = r.get("record_id")
        if rid:
            if rid in ids: errors.append(f"{p}:{n}: duplicate record_id {rid}; first at {ids[rid]}")
            else: ids[rid] = f"{p}:{n}"
        dk = r.get("dedup_key")
        if dk:
            if dk in dedups: errors.append(f"{p}:{n}: duplicate dedup_key {dk}; first at {dedups[dk]}")
            else: dedups[dk] = f"{p}:{n}"

    if not args.allow_external_links:
        idset = set(ids)
        for p, n, r in rows:
            for key in ("parent_links", "dependency_links"):
                for target in r.get(key, []):
                    if target not in idset:
                        errors.append(f"{p}:{n}: unresolved {key} target {target}")

    if errors:
        print("VALIDATION FAILED", file=sys.stderr)
        for e in errors: print(" -", e, file=sys.stderr)
        return 1
    print(f"VALIDATION OK: {len(rows)} records; {len(ids)} unique IDs; {len(dedups)} unique dedup keys")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
