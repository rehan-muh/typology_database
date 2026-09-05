from __future__ import annotations
import re
from pathlib import Path
import numpy as np
import pandas as pd
import requests, yaml

OUT=Path('pavoque_output'); OUT.mkdir(exist_ok=True)
BASE='https://raw.githubusercontent.com/marytts/pavoque-data/master/'
FILES={'angry':'pavoque-angry.yaml','happy':'pavoque-happy.yaml','neutral':'pavoque-neutral.yaml','poker':'pavoque-poker.yaml','sad':'pavoque-sad.yaml'}
VOWELS=set('a a: e: E E: i: I o: O u: U y: Y 2: 9 @ 6 aI aU OY o~'.split())
NASALS={'m','n','N'}; STOPS={'p','b','t','d','k','g','?'}; FRICS={'f','v','s','z','S','Z','C','x','h'}
SIL={'_','H#'}
rows=[]
for style,fn in FILES.items():
    r=requests.get(BASE+fn,timeout=60); r.raise_for_status(); data=yaml.safe_load(r.text)
    for utt in data:
        segs=utt.get('segments') or []; prev_end=0.0
        for i,s in enumerate(segs):
            end=float(s['end']); dur=end-prev_end; lab=str(s['lab']); prev_end=end
            if dur<=0 or lab in SIL: continue
            prev=str(segs[i-1]['lab']) if i else ''
            nxt=str(segs[i+1]['lab']) if i+1<len(segs) else ''
            rows.append([style,utt.get('prompt'),lab,dur,prev,nxt,lab in VOWELS])
d=pd.DataFrame(rows,columns=['style','prompt','segment','duration_s','prev','next','is_vowel'])
d=d[d.duration_s.between(.01,.8)].copy(); d.to_csv(OUT/'segments.csv',index=False)
# Phone-identity adjusted duration: residual log duration relative to each segment's grand mean.
d['logdur']=np.log(d.duration_s); cnt=d.groupby('segment').size(); d=d[d.segment.isin(cnt[cnt>=20].index)].copy()
d['segment_mean']=d.groupby('segment').logdur.transform('mean'); d['resid']=d.logdur-d.segment_mean
sty=d.groupby('style').agg(n=('resid','size'),mean_resid=('resid','mean'),se=('resid',lambda x:x.std()/np.sqrt(len(x)))).reset_index()
sty['ratio_to_segment_typical']=np.exp(sty.mean_resid); sty['ci_low']=np.exp(sty.mean_resid-1.96*sty.se); sty['ci_high']=np.exp(sty.mean_resid+1.96*sty.se)
sty.to_csv(OUT/'style_adjusted_duration.csv',index=False)
# Vowels: context class of following phone and style-specific timing.
def cls(x):
    if x in NASALS:return 'nasal'
    if x in STOPS:return 'stop'
    if x in FRICS:return 'fricative'
    return 'other'
vd=d[d.is_vowel].copy(); vd['next_class']=vd.next.map(cls)
# remove sparse vowel labels and residualize by vowel identity
vcnt=vd.groupby('segment').size(); vd=vd[vd.segment.isin(vcnt[vcnt>=20].index)].copy()
vd['vowel_mean']=vd.groupby('segment').logdur.transform('mean'); vd['vowel_resid']=vd.logdur-vd.vowel_mean
ctx=vd.groupby(['style','next_class']).agg(n=('vowel_resid','size'),mean_resid=('vowel_resid','mean'),se=('vowel_resid',lambda x:x.std()/np.sqrt(len(x)))).reset_index()
ctx['duration_ratio']=np.exp(ctx.mean_resid); ctx.to_csv(OUT/'vowel_context_style.csv',index=False)
# Within-style contextual contrast: nasal vs stop following context, adjusted for vowel identity.
piv=ctx.pivot(index='style',columns='next_class',values='mean_resid').reset_index()
if 'nasal' in piv and 'stop' in piv:
    piv['nasal_minus_stop_log']=piv.nasal-piv.stop; piv['nasal_vs_stop_ratio']=np.exp(piv.nasal_minus_stop_log)
piv.to_csv(OUT/'nasal_vs_stop_by_style.csv',index=False)
print('TOKENS',len(d),'VOWELS',len(vd))
print('\nSTYLE_ADJUSTED_DURATION\n',sty.to_string(index=False))
print('\nVOWEL_CONTEXT_STYLE\n',ctx.to_string(index=False))
print('\nNASAL_VS_STOP\n',piv.to_string(index=False))
