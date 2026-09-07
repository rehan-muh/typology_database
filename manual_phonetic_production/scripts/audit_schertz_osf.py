from __future__ import annotations
import io, os, re, tempfile, zipfile
from pathlib import Path
import pandas as pd
import requests

SOURCE_ID='schertz_adil_kravchuk_2023'
NODE='zve4c'
OUT=Path('schertz_audit'); OUT.mkdir(exist_ok=True)
S=requests.Session(); S.headers['User-Agent']='manual-phonetic-production-ingest/1.0'

def walk(url,prefix=''):
    rows=[]
    while url:
        r=S.get(url,timeout=90); r.raise_for_status(); js=r.json()
        for item in js.get('data',[]):
            a=item.get('attributes',{}); name=a.get('name',''); kind=a.get('kind')
            path=(prefix+'/'+name).lstrip('/')
            if kind=='file':
                rows.append({'source_id':SOURCE_ID,'path':path,'size':a.get('size'),'download_url':item.get('links',{}).get('download'),'date_modified':a.get('date_modified')})
            elif kind=='folder':
                rel=item.get('relationships',{}).get('files',{}).get('links',{}).get('related',{}).get('href')
                if rel: rows.extend(walk(rel,path))
        url=js.get('links',{}).get('next')
    return rows

def read_table(raw,name):
    ext=Path(name.lower()).suffix
    out={}
    if ext in ('.csv','.tsv','.txt'):
        for sep in [',','\t',';']:
            try:
                d=pd.read_csv(io.BytesIO(raw),sep=sep,engine='python')
                if d.shape[1]>1:
                    out['table']=d; return out
            except Exception: pass
    if ext in ('.xlsx','.xls'):
        try:
            xls=pd.ExcelFile(io.BytesIO(raw))
            for sh in xls.sheet_names:
                out[sh]=pd.read_excel(io.BytesIO(raw),sheet_name=sh)
        except Exception: pass
    if ext in ('.rds','.rda','.rdata'):
        try:
            import pyreadr
            with tempfile.NamedTemporaryFile(suffix=ext,delete=False) as f:
                f.write(raw); fn=f.name
            res=pyreadr.read_r(fn); os.unlink(fn)
            for k,v in res.items():
                if hasattr(v,'columns'): out[str(k or 'object')]=v
        except Exception: pass
    return out

def iter_payloads(raw,path):
    if path.lower().endswith('.zip'):
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                for n in z.namelist():
                    if n.endswith('/'): continue
                    try: yield f'{path}::{n}',z.read(n)
                    except Exception: pass
        except Exception: return
    else:
        yield path,raw

files=walk(f'https://api.osf.io/v2/nodes/{NODE}/files/osfstorage/')
pd.DataFrame(files).to_csv(OUT/'file_manifest.csv',index=False)
profiles=[]; candidates=[]; vardict=[]; archive_manifest=[]
pat=re.compile(r'burst|period|voic|vot|vowel|offset|onset|duration|dur|f1|f2|f3|f0|formant|speaker|subject|participant|word|item|condition|trial|repetition|accent|imit|error|response',re.I)
for f in files:
    p=f['path']; size=f.get('size') or 0
    if size>150_000_000: continue
    try:
        raw=S.get(f['download_url'],timeout=180).content
        for inner,blob in iter_payloads(raw,p):
            archive_manifest.append({'source_id':SOURCE_ID,'container':p,'member':inner,'size':len(blob)})
            if not re.search(r'\.(csv|tsv|txt|xlsx|xls|rds|rda|rdata)$',inner,re.I): continue
            objs=read_table(blob,inner)
            for sh,d in objs.items():
                profiles.append({'source_id':SOURCE_ID,'path':inner,'sheet':sh,'rows':len(d),'cols':len(d.columns),'columns':' | '.join(map(str,d.columns))})
                for c in d.columns:
                    s=d[c]
                    vardict.append({'source_id':SOURCE_ID,'path':inner,'sheet':sh,'original_variable':c,'dtype':str(s.dtype),'n_nonmissing':int(s.notna().sum()),'n_unique':int(s.nunique(dropna=True)),'sample_values':' | '.join(map(str,s.dropna().astype(str).unique()[:8]))})
                hits=[str(c) for c in d.columns if pat.search(str(c))]
                if hits:
                    candidates.append({'source_id':SOURCE_ID,'path':inner,'sheet':sh,'rows':len(d),'matched_columns':' | '.join(hits)})
                    safe=re.sub(r'[^A-Za-z0-9_.-]+','_',inner+'__'+sh)[:180]
                    if len(d)<=200000: d.to_csv(OUT/(safe+'.csv'),index=False)
    except Exception as e:
        profiles.append({'source_id':SOURCE_ID,'path':p,'sheet':'ERROR','rows':0,'cols':0,'columns':repr(e)})
pd.DataFrame(archive_manifest).to_csv(OUT/'archive_manifest.csv',index=False)
pd.DataFrame(profiles).to_csv(OUT/'table_profiles.csv',index=False)
pd.DataFrame(vardict).to_csv(OUT/'variable_dictionary_raw.csv',index=False)
pd.DataFrame(candidates).to_csv(OUT/'candidate_tables.csv',index=False)
print('FILES',len(files),'ARCHIVE_MEMBERS',len(archive_manifest),'TABLES',len(profiles),'VARIABLES',len(vardict),'CANDIDATES',len(candidates))
print(pd.DataFrame(candidates).to_string(index=False,max_colwidth=120))
