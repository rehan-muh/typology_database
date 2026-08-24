#!/usr/bin/env python3
import re,sys,json
from pathlib import Path
cats={
"inventory":r"\b(phoneme|inventory|consonant|vowel|contrast|allophon)",
"phonotactics":r"\b(syllab|coda|onset|cluster|diphthong|hiatus)",
"process":r"\b(assimilat|dissimilat|delete|deletion|epenth|insert|lenit|palatal|nasal|glide)",
"morphophonology":r"\b(morphophon|suffix|prefix|allomorph|reduplic|stem|root)",
"prosody":r"\b(stress|tone|pitch|accent|mora|prosod|inton)",
"history_contact":r"\b(histor|loan|borrow|contact|dialect|older|younger|Spanish|Portuguese|English)",
"uncertainty":r"\b(uncertain|perhaps|possibly|seems|problem|unresolved|analysis|interpret)"
}
text=Path(sys.argv[1]).read_text(encoding="utf-8",errors="ignore")
pages=text.split("\f")
out=[]
for i,p in enumerate(pages,1):
 h={k:len(re.findall(v,p,re.I)) for k,v in cats.items()}
 breadth=sum(v>0 for v in h.values())
 score=sum(min(v,12) for v in h.values())+3*breadth
 if score: out.append({"page":i,"score":score,"breadth":breadth,"hits":h,"preview":" ".join(p.split())[:300]})
print(json.dumps(sorted(out,key=lambda x:(-x["score"],-x["breadth"],x["page"]))[:80],ensure_ascii=False,indent=2))
