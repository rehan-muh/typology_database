#!/usr/bin/env python3
"""Find candidate duplicates/conflicts across phonotactics staging JSONL files.

This is deliberately conservative: it never edits data. It canonicalizes common
orthographic differences in lect/environment labels and emits reconciliation groups
for human/source-level adjudication.
"""
from __future__ import annotations
import argparse, glob, json, re, unicodedata
from collections import defaultdict
from pathlib import Path


def norm_text(x):
    if x is None:
        return ""
    s = unicodedata.normalize("NFKC", str(x)).casefold()
    s = s.replace("→", ">").replace("⇒", ">").replace("…", "...")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def read_rows(paths):
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            for i, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                row = json.loads(line)
                row["_file"] = str(p)
                row["_line"] = i
                yield row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", help="JSONL files or globs")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args()

    expanded = []
    for spec in args.paths:
        hits = sorted(glob.glob(spec))
        expanded.extend(hits or [spec])

    rows = list(read_rows(expanded))
    by_signature = defaultdict(list)
    by_dedup = defaultdict(list)
    for r in rows:
        sig = (
            norm_text(r.get("lect")),
            norm_text(r.get("normalized_environment")),
            norm_text(r.get("restriction_type")),
        )
        by_signature[sig].append(r)
        by_dedup[norm_text(r.get("dedup_key"))].append(r)

    exact_dupes = []
    for key, group in by_dedup.items():
        if key and len(group) > 1:
            exact_dupes.append({"dedup_key": key, "records": [r["record_id"] for r in group]})

    candidates = []
    for sig, group in by_signature.items():
        keys = {norm_text(r.get("dedup_key")) for r in group}
        if len(group) > 1 and len(keys) > 1:
            candidates.append({
                "signature": {"lect": sig[0], "environment": sig[1], "restriction_type": sig[2]},
                "records": [
                    {
                        "record_id": r.get("record_id"),
                        "source_id": r.get("source_id"),
                        "claim": r.get("claim"),
                        "file": r.get("_file"),
                        "line": r.get("_line"),
                    } for r in group
                ],
            })

    out = {
        "n_records": len(rows),
        "n_exact_duplicate_keys": len(exact_dupes),
        "n_reconciliation_groups": len(candidates),
        "exact_duplicate_keys": exact_dupes,
        "reconciliation_groups": candidates,
    }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"records={len(rows)} exact_duplicate_keys={len(exact_dupes)} reconciliation_groups={len(candidates)}")
        for item in exact_dupes:
            print("DUP", item["dedup_key"], ", ".join(item["records"]))
        for i, item in enumerate(candidates, 1):
            print(f"\nGROUP {i}: {item['signature']}")
            for r in item["records"]:
                print(f"  {r['record_id']} [{r['source_id']}] {r['claim']}")


if __name__ == "__main__":
    main()
