#!/usr/bin/env python3
"""Generate reproducible query strings for the daily literature/repository crawl.
Actual web retrieval is intentionally external to this script; this file defines the search surface and triage vocabulary.
"""
from datetime import date
journals=['Journal of Phonetics','Laboratory Phonology','Phonetica','Journal of the International Phonetic Association','JASA','Language and Speech','Speech Communication','Language Variation and Change']
repos=['OSF','Zenodo','GitHub']
terms=['manually annotated','manually segmented','hand-corrected','manually corrected','manual VOT','TextGrid']
print(f'# MPPD discovery queries — {date.today().isoformat()}')
for j in journals:
 for r in repos:
  print(f'"{j}" {r} ("manually annotated" OR "hand-corrected" OR "manually segmented" OR TextGrid) phonetic production')
for r in repos:
 for t in terms:
  print(f'{r} "{t}" phonetic acoustic production data')
