#!/usr/bin/env python3
"""Validate PHONOTACTICS/DISTRIBUTION shard JSONL batches without touching curated data.

Checks JSON syntax, required provenance/schema fields, confidence vocabulary,
within-input record/dedup uniqueness, and parent/dependency references.  References
may resolve either inside the supplied files or against an optional newline-delimited
record-id index.  This validator reports only; it never edits input files.
"""
from __future__ import annotations
import argparse, json, pathlib, sys

REQUIRED = {
    "record_id","source_id","lect","time_scope","domain","claim","source_forms",
    "formal_environment","normalized_environment","restriction_type","scope",
    "exceptions_or_counterexamples","publication_page","section","table_figure",
    "confidence","parent_links","dependency_links","dedup_key"
}
CONFIDENCE = {"high","medium","low"}

def load_jsonl(path: pathlib.Path):
    rows=[]
    with path.open(encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            if not line.strip(): continue
            try: row=json.loads(line)
            except Exception as e:
                raise ValueError(f"{path}:{n}: invalid JSON: {e}") from e
            rows.append((n,row))
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    ap.add_argument("--known-record-ids", type=pathlib.Path)
    a=ap.parse_args()
    known=set()
    if a.known_record_ids:
        known={x.strip() for x in a.known_record_ids.read_text(encoding="utf-8").splitlines() if x.strip()}
    parsed=[]; errors=[]; seen_id={}; seen_dedup={}
    for p in a.files:
        try: rows=load_jsonl(p)
        except ValueError as e:
            errors.append(str(e)); continue
        for n,r in rows:
            loc=f"{p}:{n}"
            miss=sorted(REQUIRED-set(r))
            if miss: errors.append(f"{loc}: missing fields: {', '.join(miss)}")
            if r.get("confidence") not in CONFIDENCE:
                errors.append(f"{loc}: invalid confidence {r.get('confidence')!r}")
            for k in ("record_id","source_id","lect","claim","publication_page","section","dedup_key"):
                if not isinstance(r.get(k),str) or not r.get(k," ").strip():
                    errors.append(f"{loc}: empty/non-string {k}")
            rid=r.get("record_id"); dk=r.get("dedup_key")
            if rid in seen_id: errors.append(f"{loc}: duplicate record_id; first {seen_id[rid]}")
            elif rid: seen_id[rid]=loc
            if dk in seen_dedup: errors.append(f"{loc}: duplicate dedup_key; first {seen_dedup[dk]}")
            elif dk: seen_dedup[dk]=loc
            for lk in ("parent_links","dependency_links"):
                if not isinstance(r.get(lk),list): errors.append(f"{loc}: {lk} must be list")
            parsed.append((loc,r))
    allids=set(seen_id)|known
    for loc,r in parsed:
        for lk in ("parent_links","dependency_links"):
            for ref in r.get(lk,[]) if isinstance(r.get(lk),list) else []:
                if ref not in allids:
                    errors.append(f"{loc}: unresolved {lk} reference {ref}")
    print(json.dumps({"files":len(a.files),"records":len(parsed),"unique_record_ids":len(seen_id),"unique_dedup_keys":len(seen_dedup),"errors":len(errors)}, indent=2))
    for e in errors: print(e, file=sys.stderr)
    raise SystemExit(1 if errors else 0)

if __name__ == "__main__": main()
