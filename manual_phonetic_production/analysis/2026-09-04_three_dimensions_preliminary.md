# Preliminary coarticulation analysis: magnitude, temporal extent, flexibility

Date: 2026-09-04

This analysis uses only manually grounded accepted production sources. It distinguishes three quantities:

1. **Magnitude** — how large the contextual phonetic effect is.
2. **Temporal extent** — how the effect evolves across normalized segment time / when it is expressed.
3. **Flexibility** — how magnitude or temporal expression changes with style, task, session, talker, etc.

## Cohn & Zellou (2023): anticipatory nasal coarticulation

27 California English speakers; 811 CVN utterances; 3,431 retained A1-P0 measurements at five vowel timepoints. Their mixed model includes speaker random effects/slopes.

- Magnitude: slow-clear has greater overall nasalization than casual (A1-P0 coefficient = -0.83, t=-2.66, p<.05; lower A1-P0 means more nasal).
- Temporal extent/trajectory: nasalization increases toward the nasal coda (timepoint coefficient = -1.55, t=-11.58, p<.001).
- Flexibility: fast-clear shows a shallower increase over vowel time than casual (style x timepoint = +0.43, t=3.16, p<.01).
- Interpretation: this is not the prediction of a pure rate/overlap account; the authors explicitly note that slower speech would mechanically be expected to reduce overlap. The observed slow-clear increase supports selective/listener-oriented tuning.

## Schertz, Adil & Kravchuk (2023): VOT and following-vowel timing

42 English speakers; manual burst, periodicity-onset, and vowel-offset landmarks.

- VOT imitation magnitude: +18.469 ms overall (SE 2.932, p<.001).
- Flexibility: VOT imitation changes with session/talker context; Session x TalkerMatch = +23.583 ms (p=.024) and the three-way interaction = -39.172 ms (p=.014).
- Temporal coupling magnitude: vowels are +6.53 ms overall after modified-VOT productions (SE 1.599, p<.001).
- Strong asymmetry: lengthened VOT is accompanied by about +14 ms vowel duration, whereas shortened VOT is accompanied by ~0 ms vowel change.

## New raw reanalysis: PAVOQUE temporal context

Source: one male native German speaker/actor, five expressive styles, manually corrected phone segmentations. This source is **descriptive within-speaker evidence only**, not language-level evidence.

Raw analysis coverage after duration plausibility filtering and phone-count threshold:
- 228,978 segment tokens
- 89,061 vowel tokens

### Style-dependent segment duration

OLS: `log(duration) ~ phone identity + style`, with SEs clustered by prompt; angry is reference.

| Style | Duration change vs angry | 95% CI | p |
|---|---:|---:|---:|
| Happy | +0.6% | -0.7% to +1.9% | .360 |
| Neutral | +0.03% | -1.2% to +1.3% | .967 |
| Poker | +4.6% | +3.3% to +6.0% | 8.25e-12 |
| Sad | +11.6% | +9.6% to +13.6% | 1.31e-33 |

This is strong within-speaker **temporal flexibility**.

### Vowel timing by following context

OLS on vowels: `log(duration) ~ vowel identity + style * following_context`, with SEs clustered by prompt. The contrast below is vowel duration before a nasal relative to before a stop.

| Style | Nasal/stop duration ratio | 95% CI | p | Approx. shorter before nasal |
|---|---:|---:|---:|---:|
| Angry | 0.832 | 0.807–0.858 | 6.9e-32 | 16.8% |
| Happy | 0.912 | 0.886–0.939 | 4.7e-10 | 8.8% |
| Neutral | 0.828 | 0.819–0.836 | 2.1e-285 | 17.2% |
| Poker | 0.859 | 0.833–0.886 | 4.7e-22 | 14.1% |
| Sad | 0.854 | 0.827–0.880 | 1.6e-23 | 14.6% |

The contextual timing effect is significant in all five styles, but its magnitude changes substantially. Relative to angry, the nasal-vs-stop contrast is about 9.7% weaker in happy style (interaction p=7.96e-10), about 3.3% weaker in poker (p=.028), not detectably different in neutral (p=.761), and not detectably different in sad (p=.113).

This is a **temporal contextual effect**, not an acoustic nasality measurement; it should not be interpreted as direct nasal coarticulation.

## Current empirical synthesis

The strongest repeated result across independently collected sources is **flexibility**: coarticulatory or intersegmental effects change with communicative style, imitation context, and expressive style. Magnitude is also clearly estimable. True temporal extent requires trajectory data and is currently strongest for nasal coarticulation; duration-only sources cannot identify onset/offset of an acoustic coarticulatory effect.

A language-level variance estimate is not yet warranted: PAVOQUE is one German speaker and the current multi-speaker trajectory benchmark is English. The next high-value step is standardized extraction from manually phone-aligned multi-speaker sources such as CCOST, L2-ARCTIC manual subset, and Parker.
