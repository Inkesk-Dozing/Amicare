# Non-Diagnostic Chatbot & Stress Engine Specification

## Scoring Scale Architecture

AmiCare implements a simplified 4-item Perceived Stress Scale (PSS-4) logic tailored for university students:

1. **Items Evaluated**:
   - Frequency of feeling overwhelmed by academic workload.
   - Frequency of feeling unable to control important student life tasks.
   - Frequency of feeling confident handling personal problems (reverse scored).
   - Frequency of feeling things were going your way (reverse scored).

2. **Scoring Breakdown**:
   - `0 - 5`: Low Stress (Empathetic reassurance + preventive self-care tools)
   - `6 - 10`: Moderate Stress (Targeted self-care strategies + campus counseling referral)
   - `11 - 16`: Elevated Stress (High-priority hotline referral + direct click-to-call support buttons)

## Non-Diagnostic Guarantee

The chatbot explicitly informs the user prior to assessment that all output is non-diagnostic and serves solely as a self-reflection tool.
