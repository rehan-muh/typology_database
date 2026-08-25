#!/usr/bin/env python3
"""Read-only summary/audit for PHONOTACTICS/DISTRIBUTION staging JSONL.

Reports exact batch/record counts, distributions by lect/source/domain/confidence,
duplicate record_id/dedup_key values, and unresolved parent/dependency links. It
never edits staging or curated data.
"""
from __future__ import annotations
import argparse, collections, json, pathlib, sys


def load(paths):
    rows=[]
    errors=[]
    for p in paths:
        with p.open(encoding="utf-8") as f:
            for n,line in enumerate(f,1):
                if not line.strip():
                    continue
                try:
                    r=json.loads(line)
                except Exception as e:
                    errors.append(f"{p}:{n}: invalid JSON: {e}")
                    continue
                rows.append((p,n,r))
    return rows,errors


def counts(rows,key):
    c=collections.Counter(r.get(key,"<missing>") for _,_,r in rows)
    return dict(sorted(c.items(), key=lambda x:(-x[1],str(x[0]))))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("path", type=pathlib.Path, help="staging directory or one JSONL file")
    ap.add_argument("--pattern", default="*.jsonl")
    a=ap.parse_args()
    paths=[a.path] if a.path.is_file() else sorted(a.path.glob(a.pattern))
    rows,errors=load(paths)
    ids=collections.defaultdict(list); dks=collections.defaultdict(list)
    for p,n,r in rows:
        loc=f"{p}:{n}"
        ids[r.get("record_id")].append(loc)
        dks[r.get("dedup_key")].append(loc)
    dup_ids={k:v for k,v in ids.items() if k and len(v)>1}
    dup_dk={k:v for k,v in dks.items() if k and len(v)>1}
    all_ids={k for k in ids if k}
    unresolved=[]
    for p,n,r in rows:
        for field in ("parent_links","dependency_links"):
            for ref in r.get(field,[]) if isinstance(r.get(field),list) else []:
                if ref not in all_ids:
                    unresolved.append({"location":f"{p}:{n}","field":field,"ref":ref})
    out={
        "batch_files":len(paths),"records":len(rows),
        "by_confidence":counts(rows,"confidence"),
        "by_lect":counts(rows,"lect"),
        "by_source":counts(rows,"source_id"),
        "by_domain":counts(rows,"domain"),
        "duplicate_record_ids":dup_ids,"duplicate_dedup_keys":dup_dk,
        "unresolved_links":unresolved,"parse_errors":errors,
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))
    raise SystemExit(1 if errors or dup_ids or dup_dk or unresolved else 0)

if __name__=="__main__":
    main()
