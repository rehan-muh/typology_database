from __future__ import annotations

import io
import json
import math
import os
import re
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import requests
import yaml

OUT = Path('audit_output')
OUT.mkdir(exist_ok=True)

OSF_PROJECTS = {
    'cohn_zellou_2023_clear_speech': 'n3fzj',
    'schertz_adil_kravchuk_2023': 'zve4c',
    'swehvd_2023_2024': 'ruxnb',
    'mitra_dutta_2023_bengali_english': 'dsb2x',
    'xi_li_prieto_2024_l2_vowels': 'mnfxb',
    'chaturvedi_shaw_2025_vowel_errors': 'x8akq',
    'chang_chien_lu_2026_l2_imitation': '43dyh',
    'cox_dideriksen_kerenportnoy_2023_danish_ids': 'ywf9m',
    'oschkinat_reinisch_hoole_2026': 'rsytu',
    'carignan_earbuds_nasalance_2024': '3wq9t',
}

TAB_EXTS = {'.csv', '.tsv', '.txt', '.xlsx', '.xls', '.json'}
PROFILE_MAX_BYTES = 30_000_000

session = requests.Session()
session.headers.update({'User-Agent': 'MPPD-coarticulation-audit/1.0'})


def get_json(url: str):
    r = session.get(url, timeout=60)
    r.raise_for_status()
    return r.json()


def iter_paginated(url: str):
    while url:
        obj = get_json(url)
        for x in obj.get('data', []):
            yield x
        url = (obj.get('links') or {}).get('next')


def osf_files(node: str):
    providers = list(iter_paginated(f'https://api.osf.io/v2/nodes/{node}/files/'))
    for provider in providers:
        pname = provider.get('attributes', {}).get('name', provider.get('id', 'provider'))
        root = ((provider.get('relationships') or {}).get('files') or {}).get('links', {}).get('related', {}).get('href')
        if root:
            yield from osf_walk(root, pname, '')


def osf_walk(url: str, provider: str, prefix: str):
    for item in iter_paginated(url):
        a = item.get('attributes', {})
        name = a.get('name') or item.get('id')
        kind = a.get('kind')
        path = f'{prefix}/{name}'.lstrip('/')
        if kind == 'file':
            yield {
                'provider': provider,
                'path': path,
                'name': name,
                'size': a.get('size'),
                'modified': a.get('modified'),
                'download': (item.get('links') or {}).get('download'),
            }
        elif kind == 'folder':
            nxt = ((item.get('relationships') or {}).get('files') or {}).get('links', {}).get('related', {}).get('href')
            if nxt:
                yield from osf_walk(nxt, provider, path)


def read_table_bytes(name: str, content: bytes):
    ext = Path(name).suffix.lower()
    if ext == '.csv':
        return pd.read_csv(io.BytesIO(content), low_memory=False)
    if ext == '.tsv':
        return pd.read_csv(io.BytesIO(content), sep='\t', low_memory=False)
    if ext == '.txt':
        try:
            return pd.read_csv(io.BytesIO(content), sep=None, engine='python', low_memory=False)
        except Exception:
            return None
    if ext in {'.xlsx', '.xls'}:
        return pd.read_excel(io.BytesIO(content))
    if ext == '.json':
        try:
            obj = json.loads(content)
            if isinstance(obj, list):
                return pd.json_normalize(obj)
            if isinstance(obj, dict):
                for v in obj.values():
                    if isinstance(v, list) and v and isinstance(v[0], dict):
                        return pd.json_normalize(v)
        except Exception:
            pass
    return None


def profile_df(source_id, path, df):
    cols = [str(c) for c in df.columns]
    lower = ' | '.join(c.lower() for c in cols)
    keywords = ['speaker','subject','participant','language','style','rate','task','vowel','phone','segment','prev','next','context','time','f0','f1','f2','f3','formant','a1','p0','nasal','cpp','h1','h2','vot','duration','burst','voice','onset','offset']
    hits = [k for k in keywords if k in lower]
    return {
        'source_id': source_id,
        'path': path,
        'nrow': len(df),
        'ncol': len(df.columns),
        'columns': ' || '.join(cols),
        'coarticulation_keywords': ' '.join(hits),
    }


def audit_osf():
    manifest = []
    profiles = []
    failures = []
    sample_dir = OUT / 'tables'
    sample_dir.mkdir(exist_ok=True)
    for source_id, node in OSF_PROJECTS.items():
        try:
            files = list(osf_files(node))
        except Exception as e:
            failures.append({'source_id': source_id, 'stage': 'list', 'error': repr(e)})
            continue
        for f in files:
            ext = Path(f['name']).suffix.lower()
            row = {'source_id': source_id, 'osf_node': node, **f, 'ext': ext}
            manifest.append(row)
            if ext not in TAB_EXTS or not f.get('download'):
                continue
            if f.get('size') and f['size'] > PROFILE_MAX_BYTES:
                continue
            try:
                r = session.get(f['download'], timeout=120)
                r.raise_for_status()
                df = read_table_bytes(f['name'], r.content)
                if df is None:
                    continue
                profiles.append(profile_df(source_id, f['path'], df))
                # Persist only small tabular source data, namespaced, to the workflow artifact.
                if len(r.content) <= 8_000_000 and ext in {'.csv','.tsv','.txt'}:
                    safe = re.sub(r'[^A-Za-z0-9_.-]+','_',f['path'])
                    (sample_dir / f'{source_id}__{safe}').write_bytes(r.content)
            except Exception as e:
                failures.append({'source_id': source_id, 'stage': 'profile', 'path': f['path'], 'error': repr(e)})
    pd.DataFrame(manifest).to_csv(OUT/'osf_manifest.csv', index=False)
    pd.DataFrame(profiles).to_csv(OUT/'table_profiles.csv', index=False)
    pd.DataFrame(failures).to_csv(OUT/'failures.csv', index=False)


PAVOQUE_STYLES = {
    'angry': 'https://raw.githubusercontent.com/marytts/pavoque-data/master/pavoque-angry.yaml',
    'happy': 'https://raw.githubusercontent.com/marytts/pavoque-data/master/pavoque-happy.yaml',
    'neutral': 'https://raw.githubusercontent.com/marytts/pavoque-data/master/pavoque-neutral.yaml',
    'poker': 'https://raw.githubusercontent.com/marytts/pavoque-data/master/pavoque-poker.yaml',
    'sad': 'https://raw.githubusercontent.com/marytts/pavoque-data/master/pavoque-sad.yaml',
}

VOWELS = set('a a: e: E E: i: I o: O u: U y: Y 2: 9 9~ @ 6 aI aU OY o~'.split())
SIL = {'_', 'H#'}


def analyze_pavoque():
    rows=[]
    for style,url in PAVOQUE_STYLES.items():
        r=session.get(url,timeout=120); r.raise_for_status()
        data=yaml.safe_load(r.text)
        for utt in data:
            segs=utt.get('segments') or []
            prev_end=0.0
            for i,s in enumerate(segs):
                end=float(s['end']); dur=end-prev_end; lab=str(s['lab'])
                prev_lab=str(segs[i-1]['lab']) if i>0 else ''
                next_lab=str(segs[i+1]['lab']) if i+1<len(segs) else ''
                if dur>0 and lab not in SIL:
                    rows.append({'style':style,'prompt':utt.get('prompt'),'segment':lab,'duration_s':dur,'prev':prev_lab,'next':next_lab,'is_vowel':lab in VOWELS})
                prev_end=end
    d=pd.DataFrame(rows)
    d.to_csv(OUT/'pavoque_segments.csv',index=False)
    # Segment-identity adjusted flexibility: log duration residualized within phone label.
    d=d[d.duration_s.between(.01,.8)].copy()
    d['logdur']=np.log(d.duration_s)
    counts=d.groupby('segment').size()
    keep=counts[counts>=20].index
    dd=d[d.segment.isin(keep)].copy()
    dd['phone_mean']=dd.groupby('segment').logdur.transform('mean')
    dd['resid_logdur']=dd.logdur-dd.phone_mean
    style=dd.groupby('style').agg(n=('resid_logdur','size'),mean_resid_logdur=('resid_logdur','mean'),sd_resid_logdur=('resid_logdur','std')).reset_index()
    style['duration_ratio_vs_phone_mean']=np.exp(style.mean_resid_logdur)
    style.to_csv(OUT/'pavoque_style_flexibility.csv',index=False)
    # Vowel duration by following segment class as descriptive temporal context.
    nasal={'m','n','N'}
    stop={'p','b','t','d','k','g','?'}
    fric={'f','v','s','z','S','Z','C','x','h'}
    def cls(x):
        if x in nasal:return 'nasal'
        if x in stop:return 'stop'
        if x in fric:return 'fricative'
        return 'other'
    vd=d[d.is_vowel].copy(); vd['next_class']=vd['next'].map(cls)
    vc=vd.groupby(['style','next_class']).agg(n=('duration_s','size'),mean_duration_s=('duration_s','mean'),median_duration_s=('duration_s','median')).reset_index()
    vc.to_csv(OUT/'pavoque_vowel_duration_by_next_class.csv',index=False)


if __name__=='__main__':
    audit_osf()
    analyze_pavoque()
    print('Audit complete:', sorted(str(p) for p in OUT.rglob('*') if p.is_file()))
