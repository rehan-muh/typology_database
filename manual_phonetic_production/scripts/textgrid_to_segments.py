#!/usr/bin/env python3
"""Convert Praat TextGrid interval tiers to a normalized segment table.
Usage: python scripts/textgrid_to_segments.py INPUT.TextGrid OUTPUT.csv [TIER]
"""
import csv, sys
from pathlib import Path
from praatio import textgrid
inp=Path(sys.argv[1]); out=Path(sys.argv[2]); tier_name=sys.argv[3] if len(sys.argv)>3 else None
tg=textgrid.openTextgrid(str(inp),includeEmptyIntervals=True)
if tier_name is None: tier_name=tg.tierNames[0]
tier=tg.getTier(tier_name)
with out.open('w',encoding='utf-8',newline='') as f:
 fields=['recording_id','tier','label','start_s','end_s','duration_s']
 w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
 for ent in tier.entries:
  start,end,label=ent.start,ent.end,ent.label
  w.writerow({'recording_id':inp.stem,'tier':tier_name,'label':label,'start_s':start,'end_s':end,'duration_s':end-start})
print(out)
