#!/usr/bin/env python3
import csv, io, json, hashlib, os, re, zipfile
from pathlib import Path
import requests
import xml.etree.ElementTree as ET

SOURCE_ID='rog_slovenian_1_0_1_1_manual_prosody'
URL='https://www.clarin.si/repository/xmlui/bitstream/handle/11356/2062/ROG.zip?isAllowed=y&sequence=1'
EXPECTED_MD5='f1e8a28e42008f634f157572bdfcf902'
OUT=Path('rog11_output'); OUT.mkdir(exist_ok=True)

r=requests.get(URL,timeout=120); r.raise_for_status(); blob=r.content
md5=hashlib.md5(blob).hexdigest(); sha256=hashlib.sha256(blob).hexdigest()
if md5 != EXPECTED_MD5: raise SystemExit(f'MD5 mismatch {md5}')
zf=zipfile.ZipFile(io.BytesIO(blob))

# Complete archive inventory.
manifest=[]
for zi in zf.infolist():
    if zi.is_dir(): continue
    data=zf.read(zi.filename)
    manifest.append({
        'source_id':SOURCE_ID,'archive':'ROG.zip','path':zi.filename,'size_bytes':zi.file_size,
        'crc32':f'{zi.CRC:08x}','sha256':hashlib.sha256(data).hexdigest(),
        'extension':Path(zi.filename).suffix.lower(),'processed':'NO','notes':''})

# TSV source-faithful layers.
def write_rows(path, rows, fields):
    with open(OUT/path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)

def read_tsv_member(name):
    txt=zf.read(name).decode('utf-8-sig')
    return list(csv.DictReader(io.StringIO(txt),delimiter='\t'))

speaker_member=next((n for n in zf.namelist() if n.endswith('/METADATA/ROG-speakers.tsv')),None)
speech_member=next((n for n in zf.namelist() if n.endswith('/METADATA/ROG-speeches.tsv')),None)
split_member=next((n for n in zf.namelist() if n.endswith('/ROG-TrainDevTest-split.tsv')),None)
metadata_counts={}
for label,member in [('speakers',speaker_member),('speeches',speech_member),('split',split_member)]:
    if not member: continue
    rows=read_tsv_member(member); metadata_counts[label]=len(rows)
    fields=list(rows[0].keys()) if rows else []
    # retain original names/values, add namespaced IDs only if an obvious source ID exists
    write_rows(f'{label}_source_faithful.tsv.csv',rows,fields)
    for m in manifest:
        if m['path']==member: m['processed']='YES'; m['notes']=f'parsed source-faithfully: {len(rows)} rows'

# Generic EXMARaLDA parser: retain EVERY timeline/event/tier label.
exb_rows=[]; timeline_rows=[]; exb_files=0
for name in zf.namelist():
    if not name.lower().endswith('.exb'): continue
    exb_files += 1
    root=ET.fromstring(zf.read(name))
    times={}
    for tli in root.findall('.//common-timeline/tli'):
        tid=tli.attrib.get('id',''); tv=tli.attrib.get('time','')
        times[tid]=tv
        timeline_rows.append({'source_id':SOURCE_ID,'file':name,'timeline_id_original':tid,'time_seconds_original':tv})
    for tier in root.findall('.//tier'):
        ta=tier.attrib
        tier_id=ta.get('id',''); category=ta.get('category',''); typ=ta.get('type',''); speaker=ta.get('speaker',''); display=ta.get('display-name','')
        for i,event in enumerate(tier.findall('./event'),1):
            st=event.attrib.get('start',''); en=event.attrib.get('end','')
            exb_rows.append({
                'source_id':SOURCE_ID,'file':name,'event_id':f'{SOURCE_ID}::{name}::{tier_id}::{i}',
                'tier_id_original':tier_id,'tier_category_original':category,'tier_type_original':typ,
                'tier_speaker_original':speaker,'tier_display_name_original':display,
                'start_tli_original':st,'end_tli_original':en,
                'start_time_seconds_original':times.get(st,''),'end_time_seconds_original':times.get(en,''),
                'annotation_original':''.join(event.itertext()),
                'manual_provenance':'ROG 1.1 release: manual multilayer annotations; Prosodic Unit annotations explicitly manually corrected in v1.1',
            })
    for m in manifest:
        if m['path']==name: m['processed']='YES'; m['notes']='parsed all EXMARaLDA tiers/events source-faithfully'

write_rows('exb_events_source_faithful.csv',exb_rows,[
    'source_id','file','event_id','tier_id_original','tier_category_original','tier_type_original','tier_speaker_original','tier_display_name_original',
    'start_tli_original','end_tli_original','start_time_seconds_original','end_time_seconds_original','annotation_original','manual_provenance'])
write_rows('exb_timeline_source_faithful.csv',timeline_rows,['source_id','file','timeline_id_original','time_seconds_original'])

# Parse TRS turns/events source-faithfully.
trs_rows=[]; trs_files=0
for name in zf.namelist():
    if not name.lower().endswith('.trs'): continue
    trs_files += 1
    root=ET.fromstring(zf.read(name)); idx=0
    for turn in root.findall('.//Turn'):
        idx+=1
        trs_rows.append({'source_id':SOURCE_ID,'file':name,'turn_id':f'{SOURCE_ID}::{name}::turn::{idx}',
            'speaker_original':turn.attrib.get('speaker',''),'start_time_seconds_original':turn.attrib.get('startTime',''),
            'end_time_seconds_original':turn.attrib.get('endTime',''),'text_original':' '.join(''.join(turn.itertext()).split())})
    for m in manifest:
        if m['path']==name: m['processed']='YES'; m['notes']='parsed TRS turns source-faithfully'
write_rows('trs_turns_source_faithful.csv',trs_rows,['source_id','file','turn_id','speaker_original','start_time_seconds_original','end_time_seconds_original','text_original'])

# Parse TEI generically into time-anchored utterance/segment-like elements when attributes exist.
tei_rows=[]; tei_files=0
for name in zf.namelist():
    low=name.lower()
    if not (low.endswith('.xml') or low.endswith('.tei')): continue
    if 'rog-art' not in low: continue
    try: root=ET.fromstring(zf.read(name))
    except Exception: continue
    tei_files += 1; idx=0
    for el in root.iter():
        tag=el.tag.split('}')[-1]
        if tag not in {'u','seg','w','incident','vocal','pause'}: continue
        idx+=1
        a=el.attrib
        tei_rows.append({'source_id':SOURCE_ID,'file':name,'tei_event_id':f'{SOURCE_ID}::{name}::{tag}::{idx}',
            'element_original':tag,'xml_id_original':a.get('{http://www.w3.org/XML/1998/namespace}id',''),
            'who_original':a.get('who',''),'start_ref_original':a.get('start',a.get('synch','')),
            'end_ref_original':a.get('end',''),'type_original':a.get('type',''),'subtype_original':a.get('subtype',''),
            'text_original':' '.join(''.join(el.itertext()).split())})
    for m in manifest:
        if m['path']==name: m['processed']='YES'; m['notes']='parsed selected TEI speech/event elements source-faithfully'
write_rows('tei_events_source_faithful.csv',tei_rows,['source_id','file','tei_event_id','element_original','xml_id_original','who_original','start_ref_original','end_ref_original','type_original','subtype_original','text_original'])

# CONLL-U: preserve token-level source data. Comments retained in sentence metadata only through file/sentence ids.
conllu_rows=[]; conllu_files=0
for name in zf.namelist():
    if not name.lower().endswith('.conllu'): continue
    conllu_files += 1; sent=1
    text=zf.read(name).decode('utf-8-sig')
    for line in text.splitlines():
        if not line.strip(): sent+=1; continue
        if line.startswith('#'): continue
        cols=line.split('\t')
        if len(cols)!=10: continue
        conllu_rows.append(dict(zip(['id','form','lemma','upos','xpos','feats','head','deprel','deps','misc'],cols),source_id=SOURCE_ID,file=name,sentence_index=sent))
    for m in manifest:
        if m['path']==name: m['processed']='YES'; m['notes']='parsed all CONLL-U token rows source-faithfully'
write_rows('conllu_tokens_source_faithful.csv',conllu_rows,['source_id','file','sentence_index','id','form','lemma','upos','xpos','feats','head','deprel','deps','misc'])

# Variable dictionary derived from retained source layers + documented semantics.
vd=[]
def add(table,var,std,domain,desc,units='',dtype='string',coding='',missing='',method='',time_ref='',target='',prov='',notes=''):
    vd.append({'source_id':SOURCE_ID,'file_table':table,'original_variable':var,'standardized_variable':std,'variable_domain':domain,'description_meaning':desc,'units':units,'datatype':dtype,'coding_levels':coding,'missing_value_conventions':missing,'measurement_annotation_method':method,'time_reference_window':time_ref,'anatomical_acoustic_target':target,'provenance':prov,'notes':notes})
for v,std,desc in [('tier_id_original','source_tier_id','EXMARaLDA tier identifier'),('tier_category_original','annotation_category','EXMARaLDA tier category'),('tier_type_original','annotation_tier_type','EXMARaLDA tier type'),('tier_speaker_original','source_speaker_id','speaker linked by tier'),('start_time_seconds_original','start_time_s','event start'),('end_time_seconds_original','end_time_s','event end'),('annotation_original','annotation_label_original','verbatim annotation text')]:
    add('exb_events_source_faithful.csv',v,std,'annotation/prosody',desc,'seconds' if 'time_' in v else '',method='manual multilayer annotation; Prosodic Unit tier explicitly manually corrected in ROG 1.1',prov='ROG 1.1 EXMARaLDA')
for v in ['speaker_original','start_time_seconds_original','end_time_seconds_original','text_original']:
    add('trs_turns_source_faithful.csv',v,{'speaker_original':'source_speaker_id','start_time_seconds_original':'start_time_s','end_time_seconds_original':'end_time_s','text_original':'transcription_original'}[v],'recording/utterance','TRS turn field','seconds' if 'time_' in v else '',prov='ROG 1.1 TRS')
for v in ['element_original','xml_id_original','who_original','start_ref_original','end_ref_original','type_original','subtype_original','text_original']:
    add('tei_events_source_faithful.csv',v,'','annotation/TEI','Verbatim TEI event field',prov='ROG 1.1 ISO TEI')
for v in ['id','form','lemma','upos','xpos','feats','head','deprel','deps','misc']:
    add('conllu_tokens_source_faithful.csv',v,'','linguistic annotation','Verbatim CONLL-U field',prov='ROG 1.1 ROG-SST')
write_rows('variable_dictionary.csv',vd,list(vd[0].keys()))
write_rows('file_manifest.csv',manifest,['source_id','archive','path','size_bytes','crc32','sha256','extension','processed','notes'])

status={
 'source_id':SOURCE_ID,'source_url':URL,'archive_md5':md5,'archive_sha256':sha256,'archive_files':len(manifest),
 'speakers_rows':metadata_counts.get('speakers',0),'speeches_rows':metadata_counts.get('speeches',0),'split_rows':metadata_counts.get('split',0),
 'exb_files':exb_files,'exb_event_rows':len(exb_rows),'timeline_rows':len(timeline_rows),'trs_files':trs_files,'trs_turn_rows':len(trs_rows),
 'tei_files':tei_files,'tei_event_rows':len(tei_rows),'conllu_files':conllu_files,'conllu_token_rows':len(conllu_rows),'variable_dictionary_rows':len(vd),
 'license':'CC BY-SA 4.0','manual_scope':'ROG 1.1 explicitly manually corrects Prosodic Unit annotations; corpus is multilayer manually annotated; alternate formats represent overlapping underlying recordings and must not be double-counted',
 'integrity':{'archive_md5_matches':md5==EXPECTED_MD5,'exb_event_ids_unique':len({r['event_id'] for r in exb_rows})==len(exb_rows),'trs_turn_ids_unique':len({r['turn_id'] for r in trs_rows})==len(trs_rows)}
}
(OUT/'ingestion_status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(status,indent=2))
