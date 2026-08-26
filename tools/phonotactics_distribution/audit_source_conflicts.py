#!/usr/bin/env python3
"""Read-only audit for cross-source phonotactic disagreements in staging JSONL.

Groups records by normalized lect + normalized_environment (or a fallback domain key),
then flags groups with multiple source IDs and potentially incompatible restriction types.
Never edits staging or curated data.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
from collections import defaultdict


def norm_text(value):
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).strip().casefold())


def load_records(paths):
    for path in paths:
        with path.open("r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError as exc:
                    yield {"_parse_error": str(exc), "_path": str(path), "_line": lineno}
                    continue
                rec["_path"] = str(path)
                rec["_line"] = lineno
                yield rec


def group_key(rec):
    lect = norm_text(rec.get("lect"))
    env = norm_text(rec.get("normalized_environment"))
    if not env:
        env = "domain:" + norm_text(rec.get("domain")) + "|scope:" + norm_text(rec.get("scope"))
    return lect, env


def classify(group):
    types = {norm_text(r.get("restriction_type")) for r in group if r.get("restriction_type")}
    sources = {r.get("source_id") for r in group if r.get("source_id")}
    claims = {norm_text(r.get("claim")) for r in group if r.get("claim")}
    explicit_conflict = any(
        norm_text(r.get("domain")) in {"source_disagreement", "analysis_uncertainty"}
        or "conflict" in norm_text(r.get("restriction_type"))
        or "uncertainty" in norm_text(r.get("restriction_type"))
        for r in group
    )
    # This intentionally over-flags: it is a review queue, not an adjudicator.
    heterogeneous = len(types) > 1 or len(claims) > 1
    return explicit_conflict, heterogeneous, sources, types


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default="staging/phonotactics_distribution")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of TSV-like text")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    paths = sorted(root.glob("*.jsonl")) if root.is_dir() else [root]
    groups = defaultdict(list)
    parse_errors = []
    for rec in load_records(paths):
        if "_parse_error" in rec:
            parse_errors.append(rec)
        else:
            groups[group_key(rec)].append(rec)

    flagged = []
    for key, group in sorted(groups.items()):
        explicit, heterogeneous, sources, types = classify(group)
        if len(sources) < 2 and not explicit:
            continue
        if not (explicit or heterogeneous):
            continue
        flagged.append({
            "lect": group[0].get("lect"),
            "normalized_environment": group[0].get("normalized_environment"),
            "explicit_conflict": explicit,
            "sources": sorted(sources),
            "restriction_types": sorted(types),
            "records": [
                {
                    "record_id": r.get("record_id"),
                    "source_id": r.get("source_id"),
                    "claim": r.get("claim"),
                    "confidence": r.get("confidence"),
                    "path": r.get("_path"),
                    "line": r.get("_line"),
                }
                for r in group
            ],
        })

    summary = {
        "files_scanned": len(paths),
        "records_scanned": sum(len(g) for g in groups.values()),
        "parse_errors": len(parse_errors),
        "flagged_groups": len(flagged),
    }
    if args.json:
        print(json.dumps({"summary": summary, "parse_errors": parse_errors, "flagged": flagged}, ensure_ascii=False, indent=2))
    else:
        print("\t".join(f"{k}={v}" for k, v in summary.items()))
        for item in flagged:
            ids = ",".join(r["record_id"] or "?" for r in item["records"])
            print(f"FLAG\t{item['lect']}\t{item['normalized_environment']}\t{ids}")
        for err in parse_errors:
            print(f"PARSE_ERROR\t{err['_path']}:{err['_line']}\t{err['_parse_error']}")


if __name__ == "__main__":
    main()
