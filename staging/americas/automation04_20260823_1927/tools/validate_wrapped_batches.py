#!/usr/bin/env python3
import json,gzip,base64,hashlib,re,sys
from pathlib import Path
REQ=["id","language","family","source_id","source_locator","section","claim","dependency_family","dependency_links","confidence","dedup_key","lect_scope","time_scope","verification_status","worker_shard","staging_status"]
rows=[]; errors=[]; sources={}
for fn in sys.argv[1:]:
 p=Path(fn); o=json.loads(p.read_text(encoding="utf-8"))
 raw=gzip.decompress(base64.b64decode(o["payload_base64"]))
 if hashlib.sha256(raw).hexdigest()!=o["uncompressed_sha256"]: errors.append([p.name,"sha256"])
 rr=[json.loads(x) for x in raw.decode().splitlines() if x.strip()]
 if len(rr)!=o["rows"]: errors.append([p.name,"row_count"])
 rows.extend(rr)
for r in rows:
 for k in REQ:
  if k not in r or (r[k] in ("",None) and k!="dependency_links"): errors.append([r.get("id"),"missing",k])
 if r.get("worker_shard")!="AMERICAS": errors.append([r.get("id"),"shard"])
 if r.get("staging_status")!="staging_only": errors.append([r.get("id"),"status"])
ids=[r["id"] for r in rows]; dks=[r["dedup_key"] for r in rows]; idset=set(ids)
if len(ids)!=len(set(ids)): errors.append(["duplicate_ids"])
if len(dks)!=len(set(dks)): errors.append(["duplicate_dedup_keys"])
broken=[(r["id"],x) for r in rows for x in r["dependency_links"] if x not in idset]
if broken: errors.append(["broken_links",broken])
by={}
for r in rows: by.setdefault(r["source_id"],[]).append(r)
for sid,rr in by.items():
 nums=sorted(int(re.search(r"_(\d+)$",r["id"]).group(1)) for r in rr)
 ok=nums==list(range(1,len(rr)+1))
 sources[sid]={"rows":len(rr),"contiguous":ok}
 if not ok: errors.append([sid,"noncontiguous"])
print(json.dumps({"rows":len(rows),"sources":sources,"unique_ids":len(ids)==len(set(ids)),"unique_dedup_keys":len(dks)==len(set(dks)),"broken_dependency_links":broken,"valid":not errors,"errors":errors},ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 1)
