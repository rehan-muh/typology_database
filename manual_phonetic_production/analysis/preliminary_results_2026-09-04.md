# Preliminary coarticulation results — 2026-09-04

## Scope

This is the first empirical benchmark pass for the ten-target coarticulation project. It uses numerical mixed-model results from two accepted, manually grounded primary-production sources whose target phenomena are already analysis-ready: Cohn & Zellou (2023) for anticipatory nasal coarticulation and Schertz, Adil & Kravchuk (2023) for VOT-vowel and temporal coupling.

These estimates are **not yet a pooled re-fit of harmonized token-level data**. The repository's canonical coarticulation directory currently contains the schema, capability matrix, ingestion queue, and templates, while the source token tables are still being normalized. These results therefore serve as reproducible source-level benchmarks against which the later harmonized re-analysis will be checked.

## NASAL — Cohn & Zellou 2023

Data scope reported by the source: 27 analyzed California English speakers; 811 CVN utterances; 3,431 retained A1-P0 observations in the CVN analysis. The mixed model included speaker and vowel random effects/slopes.

Key effects:

- Slow-clear vs casual: beta = -0.83, t = -2.66. Because lower A1-P0 means more nasalization, slow-clear speech is more nasal overall.
- Timepoint: beta = -1.55, t = -11.58. Anticipatory nasalization rises sharply across the vowel as the following nasal consonant approaches.
- Fast-clear x timepoint: beta = +0.43, t = 3.16. The anticipatory rise is shallower in fast-clear than casual speech.

Interpretation: anticipatory nasal coarticulation is not merely an automatic function of segment adjacency. Its magnitude/time course is systematically modulated by speaking style even after speaker-level heterogeneity is modeled.

## VOT_VOWEL — Schertz, Adil & Kravchuk 2023

The accent-imitation mixed model included participant and sentence random intercepts and participant/item slopes.

Key effects:

- Overall expected-direction VOT imitation: beta = 18.469 ms, SE = 2.932, p < .001.
- Session: beta = 10.141 ms, SE = 1.865, p < .001.
- Session x TalkerMatch: beta = 23.583 ms, SE = 10.071, p = .024.
- Session x TalkerMatch x AccentType: beta = -39.172 ms, SE = 15.191, p = .014.

The source also reports mean expected-direction imitation of 6 ms in Session1-DifferentVoice, 21 ms in Session1-SameVoice, 28 ms in Session2-DifferentVoice, and 18 ms in Session2-SameVoice. In a /k/-only post-hoc subset, imitation was 30 ms for lengthened VOT versus 8 ms for shortened VOT.

Interpretation: VOT adaptation is robust but highly speaker/task-context dependent, and shortened vs lengthened VOT do not behave as simple mirror images.

## TEMPORAL — Schertz, Adil & Kravchuk 2023

Following-vowel duration changes alongside manipulated VOT:

- Overall modified-minus-canonical vowel-duration difference: beta = 6.53 ms, SE = 1.599, p < .001.
- TalkerMatch: beta = -3.853 ms, SE = 1.275, p = .004.
- AccentType: beta = -13.524 ms, SE = 2.317, p < .001.

Source follow-ups show approximately +14 ms vowel duration for lengthened-VOT imitation and ~0 ms for shortened-VOT imitation.

Interpretation: temporal compensation/coupling is asymmetric. Increasing VOT tends to lengthen the following vowel as part of a broader durational adjustment, whereas shortening VOT does not trigger a corresponding vowel shortening.

## What can and cannot be claimed yet

The current accepted corpus gives clear within-language evidence for NASAL, VOT_VOWEL, and TEMPORAL. It does **not yet support a defensible cross-language pooled estimate**, because harmonized token-level tables for the multi-language phone-aligned sources (especially CCOST, L2-ARCTIC manual subset, Parker, and PAVOQUE) are not yet checked into the canonical tables. Language-level variance should not be estimated until those source data are ingested and study effects can be separated from language effects.

Next priority: normalize source-level token tables, then fit the common hierarchical model with measurements nested in tokens, tokens in speakers, speaker slopes, language effects, and crossed study/source effects.
