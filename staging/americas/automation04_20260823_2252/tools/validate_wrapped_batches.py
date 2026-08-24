#!/usr/bin/env python3
import json,gzip,base64,hashlib,re,sys
from pathlib import Path
REQ=["id","language","family","source_id","source_locator","section","claim","dependency_family","dependency_links","confidence","dedup_key","lect_scope","time_scope","verification_status","worker_shard","staging_status"]
rows=[]; errors=[]; files={}
for fn in sys.argv[1:]:
 p=Path(fn); o=json.loads(p.read_text(encoding="utf-8"))
 raw=gzip.decompress(base64.b64decode(o["payload_base64"]))
 sha=hashlib.sha256(raw).hexdigest()
 rr=[json.loads(x) for x in raw.decode("utf-8").splitlines() if x.strip()]
 files[p.name]={"rows":len(rr),"sha256":sha,"expected_sha256":o["uncompressed_sha256"],"bytes":len(raw)}
 if sha!=o["uncompressed_sha256"]: errors.append([p.name,"sha256"])
 if len(rr)!=o["rows"]: errors.append([p.name,"row_count"])
 for r in rr:
  for k in REQ:
   if k not in r or (r[k] in ("",None) and k!="dependency_links"): errors.append([r.get("id"),"missing",k])
  if r.get("worker_shard")!="AMERICAS": errors.append([r.get("id"),"shard"])
  if r.get("staging_status")!="staging_only": errors.append([r.get("id"),"status"])
 rows.extend(rr)
ids=[r["id"] for r in rows]; dks=[r["dedup_key"] for r in rows]; idset=set(ids)
if len(ids)!=len(idset): errors.append(["duplicate_ids"])
if len(dks)!=len(set(dks)): errors.append(["duplicate_dedup_keys"])
broken=[(r["id"],x) for r in rows for x in r["dependency_links"] if x not in idset]
if broken: errors.append(["broken_dependencies",broken])
by={}
for r in rows: by.setdefault(r["source_id"],[]).append(r)
seq={}
for sid,rr in by.items():
 nums=sorted(int(re.search(r"_(\d+)$",r["id"]).group(1)) for r in rr)
 ok=nums==list(range(1,len(rr)+1))
 seq[sid]={"rows":len(rr),"contiguous":ok,"first":min(r["id"] for r in rr),"last":max(r["id"] for r in rr)}
 if not ok: errors.append([sid,"noncontiguous"])
out={"rows":len(rows),"files":files,"sources":seq,"unique_ids":len(ids)==len(idset),"unique_dedup_keys":len(dks)==len(set(dks)),"broken_dependency_links":broken,"all_AMERICAS":all(r["worker_shard"]=="AMERICAS" for r in rows),"all_staging_only":all(r["staging_status"]=="staging_only" for r in rows),"errors":errors,"valid":not errors}
print(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 1)
