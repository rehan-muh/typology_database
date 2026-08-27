#!/usr/bin/env python3
"""Harvest Zenodo record metadata/files without mirroring large media.
Usage: python scripts/harvest_zenodo.py RECORD_ID [OUT.json]
"""
import json, sys, urllib.request
record=sys.argv[1]
out=sys.argv[2] if len(sys.argv)>2 else f'zenodo_{record}.json'
url=f'https://zenodo.org/api/records/{record}'
with urllib.request.urlopen(url) as r: data=json.load(r)
slim={
 'id':data.get('id'),'doi':data.get('doi'),'metadata':data.get('metadata',{}),
 'files':[{'key':x.get('key'),'size':x.get('size'),'checksum':x.get('checksum'),'links':x.get('links',{})} for x in data.get('files',[])]
}
with open(out,'w',encoding='utf-8') as f: json.dump(slim,f,ensure_ascii=False,indent=2)
print(out)
