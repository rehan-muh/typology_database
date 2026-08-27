#!/usr/bin/env python3
from pathlib import Path
import csv, sys
ROOT=Path(__file__).resolve().parents[1]
required={
 'sources.csv':['source_id','repository_url','annotation_provenance','primary_collection','decision','verified_date'],
 'exclusions.csv':['source_id','exclusion_code','reason','verified_date'],
 'review_queue.csv':['candidate_id','url','open_question','priority']
}
errors=[]
for fn,cols in required.items():
 p=ROOT/'data'/'registry'/fn
 with p.open(encoding='utf-8',newline='') as f:
  rows=list(csv.DictReader(f))
  if not rows: errors.append(f'{fn}: empty')
  for c in cols:
   if c not in (rows[0].keys() if rows else []): errors.append(f'{fn}: missing column {c}')
 ids=[]
 key='source_id' if fn!='review_queue.csv' else 'candidate_id'
 for i,r in enumerate(rows,2):
  if not r.get(key): errors.append(f'{fn}:{i}: missing {key}')
  ids.append(r.get(key))
 if len(ids)!=len(set(ids)): errors.append(f'{fn}: duplicate IDs')
if errors:
 print('\n'.join(errors)); sys.exit(1)
print('registry validation OK')
