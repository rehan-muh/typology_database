from __future__ import annotations
import io, json, os, re, sys, traceback
from pathlib import Path
import pandas as pd
import requests

PROJECTS = {
    'twi_vowel_harmony_2026':'z268r',
    'swehvd_2023_2024':'ruxnb',
    'mitra_dutta_2023_bengali_english':'dsb2x',
    'cohn_zellou_2023_clear_speech':'n3fzj',
    'xi_li_prieto_2024_l2_vowels':'mnfxb',
    'cox_dideriksen_kerenportnoy_2023_danish_ids':'ywf9m',
    'chang_chien_lu_2026_l2_imitation':'43dyh',
    'chaturvedi_shaw_2025_vowel_errors':'x8akq',
}
OUT=Path('f1f2_inventory'); OUT.mkdir(exist_ok=True)
S=requests.Session(); S.headers['User-Agent']='MPPD-f1f2-audit/1.0'

def walk(url, prefix=''):
    out=[]
    while url:
        r=S.get(url,timeout=90); r.raise_for_status(); js=r.json()
        for item in js.get('data',[]):
            a=item.get('attributes',{}); kind=a.get('kind'); name=a.get('name','')
            path=(prefix+'/'+name).lstrip('/')
            if kind=='file':
                out.append({'path':path,'size':a.get('size'),'download':item.get('links',{}).get('download')})
            elif kind=='folder':
                rel=item.get('relationships',{}).get('files',{}).get('links',{}).get('related',{}).get('href')
                if rel: out.extend(walk(rel,path))
        url=js.get('links',{}).get('next')
    return out

def role_cols(cols):
    low={c:str(c).lower() for c in cols}
    pats={
      'f1':r'(^|[^a-z])f\s*1([^0-9a-z]|$)|formant.?1',
      'f2':r'(^|[^a-z])f\s*2([^0-9a-z]|$)|formant.?2',
      'speaker':r'speaker|participant|subject|subj|talker|spkr|^id$',
      'vowel':r'vowel|phone|segment|phoneme|target',
      'time':r'time|percent|pct|point|sample|window|norm',
      'prev':r'prev|preced|left|onset|c1|pre_',
      'next':r'next|follow|right|coda|c2|post_',
      'word':r'word|item|stim|lex',
      'style':r'style|condition|speech|register|rate|task',
      'language':r'language|lang|l1|l2',
    }
    found={k:[c for c,l in low.items() if re.search(p,l)] for k,p in pats.items()}
    return found

def read_table(raw,name):
    ext=Path(name.lower()).suffix
    if ext in ('.csv','.txt','.tsv'):
        for sep in [',','\t',';']:
            try:
                df=pd.read_csv(io.BytesIO(raw),sep=sep,engine='python')
                if df.shape[1]>1:return {'table':df}
            except Exception:pass
    if ext in ('.xlsx','.xls'):
        try:
            xls=pd.ExcelFile(io.BytesIO(raw)); return {s:pd.read_excel(io.BytesIO(raw),sheet_name=s) for s in xls.sheet_names[:10]}
        except Exception:pass
    if ext in ('.rds','.rda','.rdata'):
        try:
            import pyreadr, tempfile
            with tempfile.NamedTemporaryFile(suffix=ext,delete=False) as f:
                f.write(raw); fn=f.name
            res=pyreadr.read_r(fn); os.unlink(fn)
            return {str(k or 'object'):v for k,v in res.items() if hasattr(v,'columns')}
        except Exception:pass
    return {}

rows=[]; manifest=[]
for source,node in PROJECTS.items():
    try:
        root=f'https://api.osf.io/v2/nodes/{node}/files/osfstorage/'
        files=walk(root)
        for f in files:
            manifest.append({'source_id':source,'node':node,**f})
            name=f['path']; size=f.get('size') or 0
            if not re.search(r'\.(csv|tsv|txt|xlsx|xls|rds|rda|rdata)$',name,re.I): continue
            if size and size>80_000_000: continue
            try:
                rr=S.get(f['download'],timeout=120); rr.raise_for_status()
                objs=read_table(rr.content,name)
                for sheet,df in objs.items():
                    if not isinstance(df,pd.DataFrame) or df.empty: continue
                    rc=role_cols(df.columns)
                    has_f1=bool(rc['f1']); has_f2=bool(rc['f2'])
                    if not (has_f1 or has_f2): continue
                    sample={}
                    for role in ['speaker','vowel','time','prev','next','word','style','language']:
                        vals=[]
                        for c in rc[role][:3]:
                            try:
                                u=df[c].dropna().astype(str).unique()[:8]
                                vals.append(c+'='+ '|'.join(u))
                            except:pass
                        sample[role+'_sample']=' || '.join(vals)
                    rows.append({
                      'source_id':source,'node':node,'path':name,'sheet':sheet,
                      'n_rows':len(df),'n_cols':len(df.columns),'columns':' | '.join(map(str,df.columns)),
                      **{k+'_cols':' | '.join(map(str,v)) for k,v in rc.items()},**sample
                    })
            except Exception as e:
                rows.append({'source_id':source,'node':node,'path':name,'sheet':'ERROR','n_rows':0,'n_cols':0,'columns':repr(e)})
    except Exception as e:
        manifest.append({'source_id':source,'node':node,'path':'ERROR','size':0,'download':repr(e)})

pd.DataFrame(manifest).to_csv(OUT/'osf_manifest.csv',index=False)
pd.DataFrame(rows).to_csv(OUT/'f1f2_tables.csv',index=False)
print('F1F2 TABLES')
if rows:
    z=pd.DataFrame(rows)
    print(z[['source_id','path','sheet','n_rows','f1_cols','f2_cols','speaker_cols','vowel_cols','time_cols','prev_cols','next_cols','word_cols','style_cols']].to_string(index=False,max_colwidth=100))
else: print('NONE')
