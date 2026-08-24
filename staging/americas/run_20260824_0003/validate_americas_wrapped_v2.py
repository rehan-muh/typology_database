#!/usr/bin/env python3
import json,gzip,base64,hashlib,re,sys
from pathlib import Path
rows=[]; errors=[]
for fn in sys.argv[1:]:
 p=Path(fn); o=json.loads(p.read_text(encoding='utf-8'))
 raw=gzip.decompress(base64.b64decode(o['payload_base64']))
 if hashlib.sha256(raw).hexdigest()!=o['uncompressed_sha256']: errors.append([p.name,'sha256'])
 rr=[json.loads(x) for x in raw.decode('utf-8').splitlines() if x.strip()]
 if len(rr)!=o['rows']: errors.append([p.name,'row_count'])
 rows.extend(rr)
ids=[r['id'] for r in rows]; dks=[r['dedup_key'] for r in rows]; idset=set(ids)
if len(ids)!=len(set(ids)): errors.append(['duplicate_ids'])
if len(dks)!=len(set(dks)): errors.append(['duplicate_dedup_keys'])
broken=[(r['id'],x) for r in rows for x in r.get('dependency_links',[]) if x not in idset]
if broken: errors.append(['broken_links',broken])
by={}
for r in rows: by.setdefault(r['source_id'],[]).append(r)
for sid,rr in by.items():
 nums=sorted(int(re.search(r'_(\\d+)$',r['id']).group(1)) for r in rr)
 if nums!=list(range(1,len(rr)+1)): errors.append([sid,'noncontiguous'])
print(json.dumps({'rows':len(rows),'broken_dependency_links':broken,'errors':errors,'valid':not errors},ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 1)
