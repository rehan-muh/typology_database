#!/usr/bin/env python3
"""Validate Eurasia shard staging JSONL without touching curated denominators."""
from __future__ import annotations
import argparse, json, pathlib, sys
from collections import Counter, defaultdict

REQUIRED = {"id", "language", "family", "source_id", "domain", "claim", "confidence", "dedup_key"}
PROVENANCE = {"page", "pages", "section", "table"}
CONFIDENCE = {"high", "medium_high", "medium", "medium_low", "low"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=str(pathlib.Path(__file__).resolve().parents[1] / "sources"))
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    files = sorted(root.glob("*.jsonl"))
    if not files:
        print(f"ERROR no JSONL files under {root}", file=sys.stderr)
        return 2

    rows = []
    errors = []
    by_file = Counter()
    for path in files:
        with path.open("r", encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except Exception as exc:
                    errors.append(f"{path.name}:{lineno}: JSON parse error: {exc}")
                    continue
                by_file[path.name] += 1
                row["__file"] = path.name
                row["__line"] = lineno
                rows.append(row)
                missing = sorted(REQUIRED - row.keys())
                if missing:
                    errors.append(f"{path.name}:{lineno}: missing required keys {missing}")
                if not (PROVENANCE & row.keys()):
                    errors.append(f"{path.name}:{lineno}: no page/pages/section/table provenance")
                if row.get("confidence") not in CONFIDENCE:
                    errors.append(f"{path.name}:{lineno}: unsupported confidence={row.get('confidence')!r}")
                if not isinstance(row.get("claim"), str) or not row.get("claim", "").strip():
                    errors.append(f"{path.name}:{lineno}: empty/non-string claim")
                if row.get("dependency_ids") is not None and not isinstance(row["dependency_ids"], list):
                    errors.append(f"{path.name}:{lineno}: dependency_ids must be list")

    ids = defaultdict(list)
    keys = defaultdict(list)
    exact_claims = defaultdict(list)
    for r in rows:
        loc = f"{r['__file']}:{r['__line']}"
        ids[r.get("id")].append(loc)
        keys[r.get("dedup_key")].append(loc)
        exact_claims[(r.get("language"), r.get("source_id"), r.get("claim"))].append(loc)
    for label, mapping in (("duplicate id", ids), ("duplicate dedup_key", keys), ("duplicate exact claim", exact_claims)):
        for key, locs in mapping.items():
            if key is not None and len(locs) > 1:
                errors.append(f"{label}: {key!r}: {locs}")

    known_ids = {r.get("id") for r in rows}
    for r in rows:
        for dep in r.get("dependency_ids", []):
            if dep not in known_ids:
                errors.append(f"{r['__file']}:{r['__line']}: missing dependency id {dep!r}")

    print(json.dumps({
        "root": str(root),
        "files": len(files),
        "rows": len(rows),
        "languages": len({r.get('language') for r in rows}),
        "families": len({r.get('family') for r in rows}),
        "sources": len({r.get('source_id') for r in rows}),
        "rows_by_file": dict(sorted(by_file.items())),
        "errors": len(errors),
    }, ensure_ascii=False, indent=2))
    if errors:
        print("\nVALIDATION ERRORS", file=sys.stderr)
        for e in errors:
            print("- " + e, file=sys.stderr)
        return 1
    print("VALIDATION OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
