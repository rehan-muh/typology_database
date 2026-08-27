#!/usr/bin/env python3
"""Harvest OSF public project metadata and file inventory.
Usage: python scripts/harvest_osf.py NODE_ID [OUT.json]
"""
import json, sys, urllib.request
node=sys.argv[1]
out=sys.argv[2] if len(sys.argv)>2 else f'osf_{node}.json'
base=f'https://api.osf.io/v2/nodes/{node}/'
with urllib.request.urlopen(base) as r: project=json.load(r)
with urllib.request.urlopen(base+'files/') as r: providers=json.load(r)
result={'project':project.get('data',{}),'providers':providers.get('data',[])}
with open(out,'w',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2)
print(out)
