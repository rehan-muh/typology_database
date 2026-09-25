# Ingestion pass 2026-09-25 09:07 PT

## Discovery
BELMASK (Zenodo 10.5281/zenodo.10730795; publication 10.3390/data9080092) added to REVIEW, not accepted core. Primary German audiovisual production: 10 speakers, 128 min, four mask/noise conditions. Files are restricted under EULA. Published annotation pipeline is G2P -> MAUS -> PHO2SYL; article says some boundaries/annotations may require manual adjustment but does not document exhaustive manual correction of every distributed TextGrid. Core admission therefore awaits file/object-level provenance after authorized access.

## Backlog ingestion
PAVOQUE happy upstream YAML was opened directly. poppy0001-poppy0003 contain 57 manually corrected segment objects (15 + 14 + 28). Source-faithful and harmonized interval payloads were prepared with original SAMPA labels, relative endpoints, derived relative starts, absolute endpoints, durations, style, prompt, and namespaced segment IDs. A two-file write attempt was blocked by connector safety checks, so these 57 rows are NOT claimed as committed. Existing poppy0004-poppy0007 material was detected and not duplicated.

## QC / exclusions
BELMASK is not admitted merely because the corpus is described as fully annotated: automatic MAUS provenance is explicit and the degree of subsequent human correction is not quantified. No IPA mapping was inferred. PAVOQUE source labels remain source-faithful SAMPA.

## Next
1. Retry PAVOQUE poppy0001-poppy0003 as small sequential writes if connector permits.
2. Continue happy style beyond already-present objects, deduplicating by prompt+segment index.
3. If BELMASK access becomes authorized, inventory every restricted object and distinguish manually adjusted from untouched automatic intervals before core promotion.
