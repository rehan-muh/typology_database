#!/usr/bin/env python3
"""Normalize PAVOQUE YAML phone segments into long CSV.
Requires PyYAML.
"""
import csv, sys, yaml
from pathlib import Path
src=Path(sys.argv[1]); out=Path(sys.argv[2])
items=yaml.safe_load(src.read_text(encoding='utf-8'))
fields=['source_id','utterance_id','style','utterance_text','segment_original','start_s','end_s','duration_s','annotation_provenance']
with out.open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
 for u in items:
  prev=0.0
  for seg in u.get('segments') or []:
   end=float(seg['end']); start=prev; prev=end
   w.writerow({'source_id':'pavoque','utterance_id':u['prompt'],'style':u.get('style'),'utterance_text':u.get('text'),'segment_original':seg['lab'],'start_s':start,'end_s':end,'duration_s':end-start,'annotation_provenance':'AUTO_THEN_ALL_CORRECTED'})
print(out)
