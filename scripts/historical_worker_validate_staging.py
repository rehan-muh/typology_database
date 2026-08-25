#!/usr/bin/env python3
"""Fail-closed validator for historical-processes worker JSONL staging batches.

Usage:
  python scripts/historical_worker_validate_staging.py data/grammar_extractions_staging/historical_worker_*.jsonl

This validator never edits canonical/shared data.
"""
from __future__ import annotations
import argparse, json, sys
from collections import Counter
from pathlib import Path

REQUIRED = {
    "record_type", "source_id", "lect_scope", "reconstruction_level", "input", "output",
    "environment", "process", "scope", "chronology", "relative_ordering",
    "exceptions_or_diffusion", "contact_status", "evidence_type", "competing_analysis",
    "provenance", "confidence", "note", "dedup_key"
}
PROV_REQUIRED = {"printed_page", "pdf_page", "section"}
ALLOWED_CONF = {"high", "medium", "low"}


def validate(paths: list[Path]) -> int:
    rows = []
    errors = []
    for path in paths:
        if "grammar_extractions_staging" not in path.parts:
            errors.append(f"{path}: outside staging path")
        with path.open(encoding="utf-8") as fh:
            for lineno, raw in enumerate(fh, 1):
                if not raw.strip():
                    continue
                try:
                    row = json.loads(raw)
                except Exception as exc:
                    errors.append(f"{path}:{lineno}: invalid JSON: {exc}")
                    continue
                missing = sorted(REQUIRED - row.keys())
                if missing:
                    errors.append(f"{path}:{lineno}: missing fields {missing}")
                prov = row.get("provenance")
                if not isinstance(prov, dict):
                    errors.append(f"{path}:{lineno}: provenance is not an object")
                else:
                    pmiss = sorted(PROV_REQUIRED - prov.keys())
                    if pmiss:
                        errors.append(f"{path}:{lineno}: provenance missing {pmiss}")
                    for k in PROV_REQUIRED:
                        if k in prov and (prov[k] is None or str(prov[k]).strip() == ""):
                            errors.append(f"{path}:{lineno}: blank provenance.{k}")
                if row.get("record_type") != "historical_sound_change":
                    errors.append(f"{path}:{lineno}: unexpected record_type")
                if row.get("confidence") not in ALLOWED_CONF:
                    errors.append(f"{path}:{lineno}: bad confidence {row.get('confidence')!r}")
                for k in ("source_id", "lect_scope", "input", "output", "environment", "process", "dedup_key"):
                    if not str(row.get(k, "")).strip():
                        errors.append(f"{path}:{lineno}: blank {k}")
                rows.append((path, lineno, row))

    dups = Counter(r["dedup_key"] for _, _, r in rows)
    for k, n in dups.items():
        if n > 1:
            where = [(str(p), ln) for p, ln, r in rows if r["dedup_key"] == k]
            errors.append(f"duplicate dedup_key {k}: {where}")

    sources = Counter(r["source_id"] for _, _, r in rows)
    confidence = Counter(r["confidence"] for _, _, r in rows)
    contact = Counter(r["contact_status"] for _, _, r in rows)
    print(json.dumps({
        "files": len(paths), "records": len(rows), "unique_dedup_keys": len(dups),
        "sources": dict(sorted(sources.items())),
        "confidence": dict(sorted(confidence.items())),
        "contact_status": dict(sorted(contact.items())),
        "errors": errors,
    }, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", type=Path)
    args = ap.parse_args()
    return validate(args.paths)

if __name__ == "__main__":
    raise SystemExit(main())
