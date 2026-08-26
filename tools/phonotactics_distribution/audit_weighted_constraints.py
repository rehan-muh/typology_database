#!/usr/bin/env python3
"""Read-only audit for staged weighted phonotactic constraint tables.

Designed for model-output batches such as Hayes & Wilson's Wargamay Appendix D.
It never rewrites source data. For each (source_id, lect) group whose records use
restriction_type=weighted_model_constraint, it checks:
  * integer constraint numbers and numeric weights;
  * duplicate and missing constraint numbers;
  * non-increasing weights in constraint-number order (optional table invariant);
  * equality of source_forms.constraint and formal_environment;
  * unique record IDs and dedup keys across supplied JSONL files.

This catches table-transcription omissions/reordering without promoting model output
to empirical grammatical facts.
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys


def iter_rows(paths):
    for path in paths:
        with path.open(encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except Exception as exc:
                    yield path, lineno, None, f"invalid JSON: {exc}"
                    continue
                yield path, lineno, row, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    ap.add_argument(
        "--allow-weight-increase",
        action="store_true",
        help="do not require weights to be non-increasing by constraint number",
    )
    args = ap.parse_args()

    errors = []
    groups = collections.defaultdict(list)
    seen_ids = {}
    seen_dedup = {}
    weighted_records = 0

    for path, lineno, row, parse_error in iter_rows(args.files):
        loc = f"{path}:{lineno}"
        if parse_error:
            errors.append(f"{loc}: {parse_error}")
            continue

        rid = row.get("record_id")
        dedup = row.get("dedup_key")
        if rid:
            if rid in seen_ids:
                errors.append(f"{loc}: duplicate record_id; first {seen_ids[rid]}")
            else:
                seen_ids[rid] = loc
        if dedup:
            if dedup in seen_dedup:
                errors.append(f"{loc}: duplicate dedup_key; first {seen_dedup[dedup]}")
            else:
                seen_dedup[dedup] = loc

        if row.get("restriction_type") != "weighted_model_constraint":
            continue
        weighted_records += 1
        sf = row.get("source_forms")
        if not isinstance(sf, dict):
            errors.append(f"{loc}: source_forms must be an object")
            continue
        num = sf.get("constraint_number")
        weight = sf.get("weight")
        constraint = sf.get("constraint")
        if not isinstance(num, int):
            errors.append(f"{loc}: constraint_number must be integer, got {num!r}")
            continue
        if not isinstance(weight, (int, float)) or isinstance(weight, bool):
            errors.append(f"{loc}: weight must be numeric, got {weight!r}")
        formal = row.get("formal_environment")
        if isinstance(constraint, str) and isinstance(formal, str) and constraint != formal:
            errors.append(
                f"{loc}: source_forms.constraint != formal_environment: "
                f"{constraint!r} != {formal!r}"
            )
        key = (row.get("source_id"), row.get("lect"))
        groups[key].append((num, weight, loc, rid))

    summaries = []
    for key, items in sorted(groups.items(), key=lambda x: repr(x[0])):
        nums = [x[0] for x in items]
        dup_nums = sorted(n for n, c in collections.Counter(nums).items() if c > 1)
        if dup_nums:
            errors.append(f"{key}: duplicate constraint numbers {dup_nums}")
        lo, hi = min(nums), max(nums)
        missing = sorted(set(range(lo, hi + 1)) - set(nums))
        if missing:
            errors.append(f"{key}: missing constraint numbers {missing}")

        ordered = sorted(items)
        if not args.allow_weight_increase:
            for prev, cur in zip(ordered, ordered[1:]):
                if isinstance(prev[1], (int, float)) and isinstance(cur[1], (int, float)):
                    if cur[1] > prev[1] + 1e-12:
                        errors.append(
                            f"{key}: weight increases from #{prev[0]}={prev[1]} "
                            f"to #{cur[0]}={cur[1]}"
                        )

        weights = [x[1] for x in items if isinstance(x[1], (int, float))]
        summaries.append(
            {
                "source_id": key[0],
                "lect": key[1],
                "records": len(items),
                "constraint_number_min": lo,
                "constraint_number_max": hi,
                "missing_numbers": missing,
                "duplicate_numbers": dup_nums,
                "weight_max": max(weights) if weights else None,
                "weight_min": min(weights) if weights else None,
            }
        )

    report = {
        "files": len(args.files),
        "weighted_records": weighted_records,
        "groups": summaries,
        "errors": len(errors),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    for err in errors:
        print(err, file=sys.stderr)
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
