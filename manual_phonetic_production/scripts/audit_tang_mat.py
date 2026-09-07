from __future__ import annotations
import csv, hashlib, json, math, os, re, sys, tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests
from scipy.io import loadmat

SOURCE_ID='tang_parrell_niziolek_2022_variability'
NODE='stjc9'
OUT=Path('tang_mat_audit'); OUT.mkdir(exist_ok=True)
S=requests.Session(); S.headers['User-Agent']='manual-phonetic-production-db/1.0'


def osf_files():
    # enumerate all providers, folders, files recursively
    node=S.get(f'https://api.osf.io/v2/nodes/{NODE}/files/', timeout=90); node.raise_for_status()
    providers=node.json()['data']; out=[]
    def walk(url,prefix,provider):
        while url:
            r=S.get(url,timeout=90); r.raise_for_status(); js=r.json()
            for it in js.get('data',[]):
                a=it.get('attributes',{}); name=a.get('name',''); kind=a.get('kind','')
                path=(prefix+'/'+name).lstrip('/')
                if kind=='file':
                    out.append({'provider':provider,'path':path,'size':a.get('size') or 0,
                                'download':it.get('links',{}).get('download'),
                                'md5':(a.get('extra') or {}).get('hashes',{}).get('md5'),
                                'sha256':(a.get('extra') or {}).get('hashes',{}).get('sha256')})
                elif kind=='folder':
                    rel=it.get('relationships',{}).get('files',{}).get('links',{}).get('related',{}).get('href')
                    if rel: walk(rel,path,provider)
            url=js.get('links',{}).get('next')
    for p in providers:
        pname=p.get('attributes',{}).get('name') or p.get('id')
        rel=p.get('relationships',{}).get('files',{}).get('links',{}).get('related',{}).get('href')
        if rel: walk(rel,'',pname)
    return out


def describe(x):
    if isinstance(x,dict): return 'dict', len(x), ''
    if isinstance(x,np.ndarray): return str(x.dtype), int(x.size), 'x'.join(map(str,x.shape))
    if isinstance(x,(list,tuple)): return type(x).__name__, len(x), str(len(x))
    return type(x).__name__,1,''

profiles=[]; candidates=[]; errors=[]


def clean_scalar(x):
    if isinstance(x,np.generic): return x.item()
    if isinstance(x,(str,int,float,bool)) or x is None: return x
    return str(x)


def scalar_vector(x):
    """Return a simple 1-D sequence if x can safely be represented as one column."""
    if isinstance(x,np.ndarray):
        if x.ndim==0: return None
        if x.ndim==1:
            vals=x.tolist()
        elif x.ndim==2 and 1 in x.shape:
            vals=x.reshape(-1).tolist()
        else: return None
    elif isinstance(x,(list,tuple)):
        vals=list(x)
    else: return None
    out=[]
    for v in vals:
        if isinstance(v,np.ndarray):
            if v.size==1: v=v.reshape(-1)[0]
            else: return None
        if isinstance(v,(dict,list,tuple)): return None
        out.append(clean_scalar(v))
    return out


def numeric_matrix(x):
    if isinstance(x,np.ndarray) and x.ndim==2 and np.issubdtype(x.dtype,np.number) and min(x.shape)>=2:
        return x
    return None


def walk_obj(x,path,file_path,depth=0):
    if depth>12: return
    typ,n,shape=describe(x)
    interesting=bool(re.search(r'f\s*[0-5]|formant|intens|onset|offset|vowel|trial|phase|word|duration|perturb|feedback|aud|mel|hz|error|valid',path,re.I))
    profiles.append({'source_id':SOURCE_ID,'source_path':file_path,'object_path':path,'type':typ,'n_values':n,'shape':shape,'interesting':interesting})
    if isinstance(x,dict):
        # candidate rectangular table from equal-length scalar vectors
        cols={}
        for k,v in x.items():
            sv=scalar_vector(v)
            if sv is not None and 2<=len(sv)<=2_000_000: cols[str(k)]=sv
        lens=Counter(len(v) for v in cols.values())
        if lens:
            best_n,best_k=lens.most_common(1)[0]
            same={k:v for k,v in cols.items() if len(v)==best_n}
            if best_n>=5 and len(same)>=2:
                score=sum(bool(re.search(r'f\s*[0-5]|formant|intens|onset|offset|vowel|trial|phase|word|duration|perturb|feedback',k,re.I)) for k in same)
                candidates.append((file_path,path,best_n,score,same))
        for k,v in x.items(): walk_obj(v,f'{path}.{k}' if path else str(k),file_path,depth+1)
    elif isinstance(x,(list,tuple)):
        # profile first 50 elements; all if short
        for i,v in enumerate(x[:50]): walk_obj(v,f'{path}[{i}]',file_path,depth+1)
    elif isinstance(x,np.ndarray) and x.dtype==object:
        for i,v in enumerate(x.reshape(-1)[:50]): walk_obj(v,f'{path}[{i}]',file_path,depth+1)

files=osf_files()
pd.DataFrame(files).to_csv(OUT/'file_manifest.csv',index=False)
matfiles=[f for f in files if f['path'].lower().endswith('.mat') and f.get('download')]
print('OSF files',len(files),'MAT',len(matfiles))

for j,f in enumerate(matfiles,1):
    # keep the audit bounded; participant MATs are expected to be modest research files
    if f['size'] and f['size']>250_000_000:
        errors.append({'source_path':f['path'],'error':'SKIPPED_GT_250MB'}) ; continue
    try:
        rr=S.get(f['download'],timeout=180); rr.raise_for_status(); raw=rr.content
        sha=hashlib.sha256(raw).hexdigest()
        with tempfile.NamedTemporaryFile(suffix='.mat',delete=False) as tf:
            tf.write(raw); fn=tf.name
        try:
            obj=loadmat(fn,simplify_cells=True)
        except NotImplementedError:
            import h5py
            # HDF5 v7.3: profile raw hierarchy, no speculative decoding
            with h5py.File(fn,'r') as h:
                def hv(name,o):
                    profiles.append({'source_id':SOURCE_ID,'source_path':f['path'],'object_path':name,'type':type(o).__name__,'n_values':getattr(o,'size',''),'shape':'x'.join(map(str,getattr(o,'shape',()))) if hasattr(o,'shape') else '','interesting':bool(re.search(r'f[0-5]|formant|intens|onset|offset|vowel|trial|phase|word|duration',name,re.I))})
                h.visititems(hv)
            obj={}
        finally:
            os.unlink(fn)
        obj={k:v for k,v in obj.items() if not k.startswith('__')}
        walk_obj(obj,'',f['path'])
        f['downloaded_sha256']=sha
        print(j,'/',len(matfiles),f['path'],len(raw))
    except Exception as e:
        errors.append({'source_path':f['path'],'error':repr(e)})

prof=pd.DataFrame(profiles).drop_duplicates()
prof.to_csv(OUT/'mat_object_profile.csv',index=False)
if errors: pd.DataFrame(errors).to_csv(OUT/'errors.csv',index=False)

# prioritize and write candidate tables. Duplicate structural candidates can occur; retain lineage.
idx=[]
for i,(fp,op,n,score,cols) in enumerate(sorted(candidates,key=lambda z:(-z[3],-z[2],z[0],z[1]))):
    # Avoid exploding artifact size: store all high-value candidates; otherwise first 100 candidates.
    if score==0 and i>=100: continue
    safe=re.sub(r'[^A-Za-z0-9_.-]+','_',f'{Path(fp).stem}__{op or "root"}')[-180:]
    outpath=OUT/'tables'/f'{i:04d}_{safe}.csv'; outpath.parent.mkdir(exist_ok=True)
    df=pd.DataFrame(cols)
    df.insert(0,'source_id',SOURCE_ID); df.insert(1,'source_path',fp); df.insert(2,'source_object_path',op)
    df.to_csv(outpath,index=False)
    idx.append({'table_file':str(outpath.relative_to(OUT)),'source_path':fp,'object_path':op,'rows':n,'columns':len(cols),'phonetic_field_score':score,'column_names':' | '.join(cols.keys())})
pd.DataFrame(idx).to_csv(OUT/'candidate_table_inventory.csv',index=False)

# compact inventory of all fields that appear to be phonetic/trial relevant
interesting=prof[prof['interesting']==True].copy() if not prof.empty else prof
interesting.to_csv(OUT/'interesting_fields.csv',index=False)
print('profiles',len(prof),'candidate tables',len(idx),'interesting',len(interesting),'errors',len(errors))
