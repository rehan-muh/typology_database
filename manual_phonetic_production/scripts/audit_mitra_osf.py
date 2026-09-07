from __future__ import annotations
import io, json, os, re, zipfile, hashlib, tempfile
from pathlib import Path
import pandas as pd
import requests

SOURCE_ID='mitra_dutta_2023_bengali_english'
NODE='dsb2x'
OUT=Path('mitra_deep_audit'); OUT.mkdir(exist_ok=True)
S=requests.Session(); S.headers['User-Agent']='MPPD-Mitra-deep-audit/1.0'

def walk(url,prefix=''):
    out=[]
    while url:
        r=S.get(url,timeout=90); r.raise_for_status(); j=r.json()
        for x in j.get('data',[]):
            a=x.get('attributes',{}); name=a.get('name',''); kind=a.get('kind'); path=(prefix+'/'+name).lstrip('/')
            if kind=='file':
                out.append({'source_id':SOURCE_ID,'path':path,'size':a.get('size'),'modified':a.get('date_modified'),'download':x.get('links',{}).get('download')})
            elif kind=='folder':
                u=x.get('relationships',{}).get('files',{}).get('links',{}).get('related',{}).get('href')
                if u: out.extend(walk(u,path))
        url=j.get('links',{}).get('next')
    return out

def read_tables(raw,name):
    ret={}; ext=Path(name.lower()).suffix
    if ext in ('.csv','.tsv','.txt'):
        for sep in [',','\t',';','|']:
            try:
                d=pd.read_csv(io.BytesIO(raw),sep=sep,engine='python',on_bad_lines='skip')
                if d.shape[1]>1:
                    ret['table']=d; return ret
            except Exception: pass
    if ext in ('.xlsx','.xls'):
        try:
            xf=pd.ExcelFile(io.BytesIO(raw))
            for sh in xf.sheet_names[:30]: ret[sh]=pd.read_excel(io.BytesIO(raw),sheet_name=sh)
        except Exception: pass
    if ext in ('.rds','.rda','.rdata'):
        try:
            import pyreadr
            with tempfile.NamedTemporaryFile(suffix=ext,delete=False) as f: f.write(raw); fn=f.name
            z=pyreadr.read_r(fn); os.unlink(fn)
            for k,v in z.items():
                if hasattr(v,'columns'): ret[str(k or 'object')]=v
        except Exception: pass
    return ret

def classify(c):
    s=str(c).lower()
    tests=[
      ('formant',r'(^|[^a-z])f[1-5]([^a-z0-9]|$)|formant'),('pitch_f0',r'(^|[^a-z])f0([^a-z0-9]|$)|pitch|semitone'),
      ('duration_timing',r'dur|duration|vot|onset|offset|start|end|time|latency'),('voice_quality',r'cpp|hnr|jitter|shimmer|h1|h2|spectral.?tilt|creak|breath'),
      ('nasality',r'nasal|a1.?p0|a1.?p1|nasalance'),('intensity',r'intens|amplitude|rms|db'),('segment_label',r'phone|phoneme|segment|vowel|consonant|ipa'),
      ('speaker',r'speaker|participant|subject|subj|talker'),('language',r'language|lang|bengali|english|code.?switch|l1|l2'),
      ('condition',r'task|condition|context|session|repetition|rep|trial|style|rate'),('lexical',r'word|item|stim|sentence|lex'),
      ('demographic',r'age|gender|sex|education|proficiency|residence')]
    for k,p in tests:
        if re.search(p,s): return k
    return 'source_specific'

files=walk(f'https://api.osf.io/v2/nodes/{NODE}/files/osfstorage/')
pd.DataFrame(files).to_csv(OUT/'file_manifest.csv',index=False)
prof=[]; vard=[]; failures=[]; processed=0
for f in files:
    path=f['path']; size=f.get('size') or 0
    if size>100_000_000: continue
    if not re.search(r'\.(csv|tsv|txt|xlsx|xls|rds|rda|rdata|zip)$',path,re.I): continue
    try:
        rr=S.get(f['download'],timeout=180); rr.raise_for_status(); raw=rr.content
        sha=hashlib.sha256(raw).hexdigest()
        members=[(path,raw)]
        if path.lower().endswith('.zip'):
            members=[]
            try:
                with zipfile.ZipFile(io.BytesIO(raw)) as zf:
                    for n in zf.namelist():
                        if n.endswith('/') or not re.search(r'\.(csv|tsv|txt|xlsx|xls|rds|rda|rdata)$',n,re.I): continue
                        info=zf.getinfo(n)
                        if info.file_size<=100_000_000: members.append((path+'::'+n,zf.read(n)))
            except Exception as e: failures.append({'path':path,'error':'zip:'+repr(e)})
        for mname,mraw in members:
            tabs=read_tables(mraw,mname)
            for sheet,d in tabs.items():
                if not isinstance(d,pd.DataFrame) or d.empty: continue
                processed+=1
                prof.append({'source_id':SOURCE_ID,'container_path':path,'table_path':mname,'sheet':sheet,'rows':len(d),'columns':len(d.columns),'source_sha256':sha,'column_names':' | '.join(map(str,d.columns))})
                for c in d.columns:
                    s=d[c]; vals=s.dropna().astype(str)
                    vard.append({'source_id':SOURCE_ID,'table_path':mname,'sheet':sheet,'original_variable':str(c),'variable_domain':classify(c),'dtype':str(s.dtype),'nonmissing_n':int(s.notna().sum()),'missing_n':int(s.isna().sum()),'unique_n':int(s.nunique(dropna=True)),'example_values':' | '.join(vals.unique()[:8])[:1000]})
    except Exception as e: failures.append({'path':path,'error':repr(e)})
pd.DataFrame(prof).to_csv(OUT/'table_inventory.csv',index=False)
pd.DataFrame(vard).to_csv(OUT/'variable_dictionary_raw.csv',index=False)
pd.DataFrame(failures).to_csv(OUT/'failures.csv',index=False)
summary=pd.DataFrame([{'source_id':SOURCE_ID,'files_discovered':len(files),'tables_parsed':len(prof),'rows_parsed':sum(x['rows'] for x in prof),'variable_records':len(vard),'failed_files':len(failures)}])
summary.to_csv(OUT/'summary.csv',index=False)
print(summary.to_string(index=False)); print(pd.DataFrame(prof).sort_values('rows',ascending=False).head(30).to_string(index=False,max_colwidth=80))
